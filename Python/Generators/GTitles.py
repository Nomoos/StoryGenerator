import os
import shutil
import re
import time
from difflib import SequenceMatcher

import whisperx
import torch

from Models.StoryIdea import StoryIdea
from Tools.Utils import (
    VOICEOVER_PATH,
    TITLES_PATH,
    sanitize_filename,
    SUBTITLESWBW_NAME,
)
from Tools.Monitor import logger, PerformanceMonitor, log_error, log_info
from Tools.Retry import retry_with_exponential_backoff
from Tools.Validator import OutputValidator

VOICEOVER_FILE = "voiceover_normalized.mp3"
REVISED_FILE = "Revised.txt"


class TitleGenerator:
    def __init__(self, model_size="large-v2"):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model = whisperx.load_model(model_size, self.device, compute_type="float32", language="en")
        self.alignment_model, self.metadata = whisperx.load_align_model(language_code="en", device=self.device)
        self._ensure_paths()

    def _ensure_paths(self):
        for path in [VOICEOVER_PATH, TITLES_PATH]:
            os.makedirs(path, exist_ok=True)

    def generate_titles(self):
        for folder_name in os.listdir(VOICEOVER_PATH):
            self._move_folder_by_name(folder_name)
            output_path = os.path.join(TITLES_PATH, folder_name)

            mp3_path = os.path.join(output_path, VOICEOVER_FILE)
            revised_path = os.path.join(output_path, REVISED_FILE)

            if not os.path.isfile(mp3_path):
                print(f"⚠️ Skipping '{folder_name}': {VOICEOVER_FILE} not found")
                continue
            if not os.path.isfile(revised_path):
                print(f"⚠️ Skipping '{folder_name}': {REVISED_FILE} not found")
                continue

            srt_output = os.path.join(output_path, SUBTITLESWBW_NAME)
            
            # Time the alignment operation
            operation_start = time.time()
            success = False
            error_msg = None
            metrics = {}
            
            try:
                self.align_script_to_word_level_srt(mp3_path, revised_path, srt_output)
                success = True
                
                # Validate subtitle output
                is_valid, validation_metrics = OutputValidator.validate_text_file(srt_output, min_length=50)
                metrics.update(validation_metrics)
                
                if not is_valid:
                    error_msg = "Generated subtitle file failed validation"
                    success = False
                
            except Exception as e:
                error_msg = str(e)
                log_error("Title Generation", folder_name, e)
            finally:
                duration = time.time() - operation_start
                PerformanceMonitor.log_operation(
                    operation="Alignment_Generation",
                    story_title=folder_name,
                    duration=duration,
                    success=success,
                    error=error_msg,
                    metrics=metrics
                )

    def align_script_to_word_level_srt(self, audio_path: str, script_path: str, output_srt: str, log_mismatches: bool = True):
        print(f"🎧 Aligning script to audio using WhisperX: {audio_path}")
        
        alignment_start = time.time()
        transcribe_start = time.time()

        with open(script_path, "r", encoding="utf-8") as f:
            script_text = f.read()
        script_words = self._normalize_text(script_text)

        try:
            audio = whisperx.load_audio(audio_path)
            result = self._transcribe_with_retry(audio)
            
            transcribe_duration = time.time() - transcribe_start
            log_info(f"✅ Transcription completed in {transcribe_duration:.2f}s")
            
            align_start = time.time()
            result_aligned = whisperx.align(result["segments"], self.alignment_model, self.metadata, audio, self.device)
            align_duration = time.time() - align_start
            log_info(f"✅ Alignment completed in {align_duration:.2f}s")

            spoken_words = result_aligned["word_segments"]
            spoken_clean = [self._normalize_word(w["word"]) for w in spoken_words]

            matcher = SequenceMatcher(None, script_words, spoken_clean)
            opcodes = matcher.get_opcodes()

            segments = []
            for tag, i1, i2, j1, j2 in opcodes:
                if tag == "equal":
                    for i, j in zip(range(i1, i2), range(j1, j2)):
                        segments.append({
                            "word": script_words[i],
                            "start": spoken_words[j]["start"],
                            "end": spoken_words[j]["end"]
                        })
                else:
                    for i in range(i1, i2):
                        est_start, est_end = self._estimate_time(i, segments)
                        segments.append({
                            "word": script_words[i],
                            "start": est_start,
                            "end": est_end
                        })

            if log_mismatches:
                estimated = sum(1 for s in segments if s["start"] == s["end"])
                print(f"🧾 Estimated {estimated} timestamps out of {len(segments)} words.")
                log_info(f"Alignment accuracy: {((len(segments) - estimated) / len(segments) * 100):.1f}%")

            self._export_word_srt(segments, output_srt)
            
            total_duration = time.time() - alignment_start
            log_info(f"✅ Total alignment time: {total_duration:.2f}s")

        except Exception as e:
            log_error("Alignment", audio_path, e)
            print(f"❌ Error during alignment: {e}")
            raise
    
    @retry_with_exponential_backoff(
        max_retries=2,
        base_delay=1.0,
        max_delay=20.0,
        exceptions=(Exception,)
    )
    def _transcribe_with_retry(self, audio):
        """Transcribe audio with retry logic."""
        return self.model.transcribe(audio, batch_size=16)

    def _estimate_time(self, index, segments):
        prev_time = None
        next_time = None

        for i in range(index - 1, -1, -1):
            if i < len(segments) and segments[i]["start"] != segments[i]["end"]:
                prev_time = segments[i]["end"]
                break

        for i in range(index + 1, len(segments)):
            if i < len(segments) and segments[i]["start"] != segments[i]["end"]:
                next_time = segments[i]["start"]
                break

        if prev_time is not None and next_time is not None:
            mid = (prev_time + next_time) / 2
            return max(0, mid - 0.05), mid + 0.05
        elif prev_time is not None:
            return prev_time, prev_time + 0.1
        elif next_time is not None:
            return max(0, next_time - 0.1), next_time
        else:
            return 0.0, 0.1

    def _export_word_srt(self, segments, output_path):
        def format_time(seconds):
            h = int(seconds // 3600)
            m = int((seconds % 3600) // 60)
            s = int(seconds % 60)
            ms = int((seconds % 1) * 1000)
            return f"{h:02}:{m:02}:{s:02},{ms:03}"

        with open(output_path, "w", encoding="utf-8") as f:
            for idx, word in enumerate(segments, 1):
                start = format_time(word["start"])
                end = format_time(word["end"])
                f.write(f"{idx}\n{start} --> {end}\n{word['word']}\n\n")

    def _normalize_text(self, text):
        return re.findall(r"\b\w+\b", text.lower())

    def _normalize_word(self, word):
        return re.sub(r"[^\w]", "", word.lower())

    def _move_folder_by_name(self, folder_name: str):
        src = os.path.join(VOICEOVER_PATH, folder_name)
        dst = os.path.join(TITLES_PATH, folder_name)

        print(f"📦 Moving folder: {src} → {dst}")
        try:
            shutil.move(src, dst)
        except Exception as e:
            print(f"❌ Error moving folder '{folder_name}': {e}")

    def move_folder_by_story_idea(self, story_idea: StoryIdea):
        input_path = os.path.join(VOICEOVER_PATH, sanitize_filename(story_idea.story_title))
        output_path = os.path.join(TITLES_PATH, sanitize_filename(story_idea.story_title))

        if not os.path.exists(input_path):
            print(f"⚠️ Source folder does not exist: {input_path}")
            return

        if os.path.exists(output_path):
            print(f"⚠️ Destination folder already exists. Removing: {output_path}")
            shutil.rmtree(output_path)

        try:
            shutil.move(input_path, output_path)
            print(f"✅ Moved story folder from '{input_path}' to '{output_path}'")
        except Exception as e:
            print(f"❌ Error moving folder: {e}")
