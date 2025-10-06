import os
from elevenlabs import ElevenLabs, Voice, VoiceSettings, save
import shutil
import time

from pydub import AudioSegment
from pydub.silence import detect_leading_silence

import numpy as np
import pyloudnorm as pyln
import ffmpeg

from Models.StoryIdea import StoryIdea
from Tools.Utils import RESOURCES_PATH, SCRIPTS_PATH, VOICEOVER_PATH, REVISED_PATH, sanitize_filename, convert_to_mp4, \
    REVISED_NAME, ENHANCED_NAME
from Tools.Monitor import logger, PerformanceMonitor, log_error, log_info
from Tools.Retry import retry_with_exponential_backoff, with_circuit_breaker
from Tools.Validator import OutputValidator

API_KEY = 'sk_8b119f95dfca190665b8bc19a24e3be40e32d39c7c50a4d8'

class VoiceMaker:
    def __init__(self):
        self.client = ElevenLabs(api_key=API_KEY)

    def trim_silence(audio_segment, silence_threshold=-45.0, chunk_size=10):
        """Trim excessive silence and add 200 ms of leading and trailing silence."""

        # Detect and trim leading silence
        start_trim = detect_leading_silence(audio_segment, silence_threshold=silence_threshold, chunk_size=chunk_size)
        # Detect and trim trailing silence (reverse the audio to detect from the end)
        end_trim = detect_leading_silence(audio_segment.reverse(), silence_threshold=silence_threshold,
                                          chunk_size=chunk_size)

        # Trim the audio segment
        duration = len(audio_segment)
        trimmed_sound = audio_segment[start_trim:duration - end_trim]

        # Create 200 ms of silence to add to the start and end
        silence_segment = AudioSegment.silent(duration=200)

        # Add 200 ms of silence at the beginning and end of the trimmed audio
        final_audio = silence_segment + trimmed_sound + silence_segment

        return final_audio

    def normalize_lufs(self, audio_segment, target_lufs=-14.0):
        # Convert pydub audio to numpy array
        samples = np.array(audio_segment.get_array_of_samples()).astype(np.float32)
        samples /= (2 ** 15)  # Convert 16-bit PCM to float32 in range [-1, 1]

        meter = pyln.Meter(audio_segment.frame_rate)  # create LUFS meter
        loudness = meter.integrated_loudness(samples)

        # Calculate needed gain
        loudness_change = target_lufs - loudness
        normalized_segment = audio_segment.apply_gain(loudness_change)

        return normalized_segment

    def normalize_audio(self, audio_segment, target_dBFS=-3.0):
        """Normalizuje zvuk na zadanou úroveň dBFS (ideálně pro voiceover)."""
        # Vypočítá rozdíl mezi aktuální průměrnou hlasitostí a cílovou hlasitostí
        change_in_dBFS = target_dBFS - audio_segment.dBFS
        # Aplikuje tuto změnu na celou zvukovou stopu
        return audio_segment.apply_gain(change_in_dBFS)

    @retry_with_exponential_backoff(
        max_retries=3,
        base_delay=2.0,
        max_delay=30.0,
        exceptions=(Exception,)
    )
    @with_circuit_breaker("elevenlabs")
    def _generate_tts_with_retry(self, script: str):
        """Generate TTS with retry logic and circuit breaker."""
        return self.client.generate(
            model='eleven_v3',
            text=script,
            output_format='mp3_44100_192',
            voice=Voice(
                voice_id='BZgkqPqms7Kj9ulSkVzn',
                style='Creative'
            )
        )


    def generate_audio(self):
        # Projdeme všechny soubory ve složce '01_Scripts'
        for folder_name in os.listdir(REVISED_PATH):
            INPUT_PATH = os.path.join(REVISED_PATH, folder_name)
            idea_file = os.path.join(INPUT_PATH, "idea.json")
            if not os.path.exists(idea_file):
                print(f"⚠️ Skipping '{folder_name}': missing idea.json")
                continue
            idea = StoryIdea.from_file(idea_file)
            self.moveFolder(idea)
            OUTPUT_PATH = os.path.join(VOICEOVER_PATH, folder_name)

            operation_start = time.time()
            success = False
            error_msg = None
            metrics = {}

            try:
                print(f"\n--- Make voiceover for: {idea.story_title} ---")
                voiceover_path = os.path.join(OUTPUT_PATH, 'voiceover.mp3')
                script = self.loadScript(idea)
                
                try:
                    # if voiceover already exists, skip
                    if os.path.exists(voiceover_path):
                        print(f"Voiceover for '{folder_name}' already exists. Skipping...")
                        continue
                except Exception as e:
                    print(f"Error reading file: {e}")

                # Generate TTS with timing and retry
                tts_start = time.time()
                try:
                    audio = self._generate_tts_with_retry(script)
                    save(audio, voiceover_path)
                    tts_duration = time.time() - tts_start
                    metrics['tts_duration'] = round(tts_duration, 2)
                    log_info(f"✅ TTS completed in {tts_duration:.2f}s")
                except Exception as e:
                    error_msg = f"Error generating voiceover: {e}"
                    log_error("TTS Generation", idea.story_title, e)
                    print(f"❌ {error_msg}")
                    continue

                # Normalize audio with timing
                normalize_start = time.time()
                try:
                    audio_segment = AudioSegment.from_mp3(voiceover_path)
                    normalized_voiceover = self.normalize_lufs(audio_segment)
                    voiceover_path = os.path.join(OUTPUT_PATH, 'voiceover_normalized.mp3')
                    normalized_voiceover.export(voiceover_path, format='mp3',
                                                tags={"artist": "Nom", "album": "Noms Stories"})
                    normalize_duration = time.time() - normalize_start
                    metrics['normalize_duration'] = round(normalize_duration, 2)
                    log_info(f"✅ Audio normalized in {normalize_duration:.2f}s")
                    # pokud je vše v pořádku uloženo smažeme původní soubory
                    # os.remove(os.path.join(OUTPUT_PATH, 'voiceover.mp3'))
                except Exception as e:
                    error_msg = f"Error normalizing audio: {e}"
                    log_error("Audio Normalization", idea.story_title, e)
                    print(f"❌ {error_msg}")
                    continue
                
                # Validate output
                is_valid, validation_metrics = OutputValidator.validate_audio_file(voiceover_path)
                metrics.update(validation_metrics)
                
                if not is_valid:
                    error_msg = "Generated audio file failed validation"
                    log_error("Audio Validation", idea.story_title, Exception(error_msg))
                else:
                    success = True

            except Exception as e:
                error_msg = str(e)
                log_error("Audio Generation", idea.story_title, e)
                print(f"❌ Failed to generate audio for '{folder_name}': {e}")
            finally:
                # Log performance metrics
                total_duration = time.time() - operation_start
                PerformanceMonitor.log_operation(
                    operation="TTS_Generation",
                    story_title=idea.story_title,
                    duration=total_duration,
                    success=success,
                    error=error_msg,
                    metrics=metrics
                )

    def normalize_audio(self):
        for folder_name in os.listdir(VOICEOVER_PATH):
            OUTPUT_PATH = os.path.join(VOICEOVER_PATH, folder_name)
            input_path = os.path.join(OUTPUT_PATH, 'voiceover.mp3')
            output_path = os.path.join(OUTPUT_PATH, 'voiceover_normalized.mp3')

            if not os.path.exists(input_path):
                print(f"⚠️ Skipping '{folder_name}': No voiceover.mp3 found.")
                continue

            if os.path.exists(output_path):
                print(f"✅ Normalized voiceover already exists for '{folder_name}'. Skipping...")
                continue

            try:
                print(f"🎧 Normalizing audio for '{folder_name}'...")
                audio_segment = AudioSegment.from_mp3(input_path)
                normalized = self.normalize_lufs(audio_segment)
                normalized.export(output_path, format='mp3',
                                  tags={"artist": "Nom", "album": "Noms Stories"})
                os.remove(input_path)
                print(f"✅ Saved: {output_path}")
            except Exception as e:
                print(f"❌ Error normalizing audio for '{folder_name}': {e}")

    def moveFolder(self, storyIdea: StoryIdea):
        INPUT_PATH = os.path.join(REVISED_PATH, sanitize_filename(storyIdea.story_title))
        OUTPUT_PATH = os.path.join(VOICEOVER_PATH, sanitize_filename(storyIdea.story_title))

        if not os.path.exists(INPUT_PATH):
            print(f"Source folder does not exist: {INPUT_PATH}")
            return

        if os.path.exists(OUTPUT_PATH):
            print(f"Destination folder already exists. Removing: {OUTPUT_PATH}")
            shutil.rmtree(OUTPUT_PATH)

        try:
            shutil.move(INPUT_PATH, OUTPUT_PATH)
            print(f"Moved story folder from '{INPUT_PATH}' to '{OUTPUT_PATH}'")
        except Exception as e:
            print(f"Error moving folder: {e}")

    def loadScript(self, storyIdea: StoryIdea):
        folder_path = os.path.join(VOICEOVER_PATH, sanitize_filename(storyIdea.story_title))
        script_file = os.path.join(folder_path, ENHANCED_NAME)  # Adjust filename as needed

        if not os.path.exists(script_file):
            raise FileNotFoundError(f"Script file not found: {script_file}")

        with open(script_file, "r", encoding="utf-8") as f:
            return f.read().strip()
