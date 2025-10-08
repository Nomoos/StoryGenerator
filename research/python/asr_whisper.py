"""
Faster-Whisper ASR (Automatic Speech Recognition) wrapper.
Research prototype for local-only speech-to-text transcription.
"""

from typing import Optional, List, Dict, Tuple
from pathlib import Path


class WhisperASR:
    """
    Wrapper for faster-whisper for efficient speech recognition.
    
    This is a research prototype demonstrating how to:
    - Load and run faster-whisper models
    - Perform word-level transcription with timestamps
    - Handle multiple audio formats
    - Implement language detection
    """
    
    def __init__(
        self,
        model_size: str = "large-v2",
        device: str = "auto",
        compute_type: str = "float16"
    ):
        """
        Initialize faster-whisper model.
        
        Args:
            model_size: Model size ("tiny", "base", "small", "medium", "large-v2", "large-v3")
            device: Device to use ("cpu", "cuda", "auto")
            compute_type: Computation type ("float16", "float32", "int8")
        """
        self.model_size = model_size
        self.device = self._get_device(device)
        self.compute_type = compute_type
        self.model = None
        
    def _get_device(self, device: str) -> str:
        """Determine the device to use."""
        if device == "auto":
            try:
                import torch
                return "cuda" if torch.cuda.is_available() else "cpu"
            except ImportError:
                return "cpu"
        return device
    
    def load_model(self):
        """Load the faster-whisper model."""
        try:
            from faster_whisper import WhisperModel
            
            self.model = WhisperModel(
                self.model_size,
                device=self.device,
                compute_type=self.compute_type
            )
            print(f"Loaded {self.model_size} model on {self.device}")
        except ImportError:
            raise ImportError(
                "faster-whisper not installed. "
                "Install with: pip install faster-whisper"
            )
    
    def transcribe(
        self,
        audio_path: str,
        language: Optional[str] = None,
        task: str = "transcribe",
        word_timestamps: bool = True,
        vad_filter: bool = True
    ) -> Dict:
        """
        Transcribe audio file.
        
        Args:
            audio_path: Path to audio file
            language: Language code (e.g., "en", "es") or None for auto-detection
            task: "transcribe" or "translate" (translate to English)
            word_timestamps: Include word-level timestamps
            vad_filter: Apply voice activity detection filter
            
        Returns:
            Dictionary with:
                - text: Full transcription
                - segments: List of segments with timestamps
                - words: List of words with timestamps (if word_timestamps=True)
                - language: Detected language
        """
        if self.model is None:
            self.load_model()
        
        # Transcribe
        segments, info = self.model.transcribe(
            audio_path,
            language=language,
            task=task,
            word_timestamps=word_timestamps,
            vad_filter=vad_filter
        )
        
        # Process results
        text_parts = []
        segment_list = []
        word_list = []
        
        for segment in segments:
            segment_dict = {
                "id": segment.id,
                "start": segment.start,
                "end": segment.end,
                "text": segment.text,
                "confidence": getattr(segment, "avg_logprob", None)
            }
            segment_list.append(segment_dict)
            text_parts.append(segment.text)
            
            # Extract word-level timestamps if available
            if word_timestamps and hasattr(segment, "words"):
                for word in segment.words:
                    word_list.append({
                        "word": word.word,
                        "start": word.start,
                        "end": word.end,
                        "confidence": word.probability
                    })
        
        return {
            "text": " ".join(text_parts),
            "segments": segment_list,
            "words": word_list if word_timestamps else None,
            "language": info.language,
            "language_probability": info.language_probability
        }
    
    def transcribe_to_srt(
        self,
        audio_path: str,
        output_path: Optional[str] = None,
        language: Optional[str] = None,
        max_words_per_line: int = 10
    ) -> str:
        """
        Transcribe audio and generate SRT subtitle file.
        
        Args:
            audio_path: Path to audio file
            output_path: Path to save SRT file (optional)
            language: Language code or None for auto-detection
            max_words_per_line: Maximum words per subtitle line
            
        Returns:
            SRT content as string
        """
        # Transcribe with word timestamps
        result = self.transcribe(
            audio_path,
            language=language,
            word_timestamps=True
        )
        
        # Generate SRT from words
        srt_content = self._words_to_srt(
            result["words"],
            max_words_per_line=max_words_per_line
        )
        
        # Save if output path provided
        if output_path:
            Path(output_path).write_text(srt_content, encoding="utf-8")
        
        return srt_content
    
    def _words_to_srt(
        self,
        words: List[Dict],
        max_words_per_line: int = 10
    ) -> str:
        """
        Convert word timestamps to SRT format.
        
        Args:
            words: List of word dictionaries with start, end, word
            max_words_per_line: Maximum words per subtitle
            
        Returns:
            SRT formatted string
        """
        if not words:
            return ""
        
        srt_entries = []
        entry_id = 1
        
        # Group words into subtitle lines
        i = 0
        while i < len(words):
            # Take up to max_words_per_line words
            line_words = words[i:i + max_words_per_line]
            
            # Get timing from first and last word
            start_time = line_words[0]["start"]
            end_time = line_words[-1]["end"]
            
            # Combine words into text
            text = " ".join(w["word"].strip() for w in line_words)
            
            # Format as SRT entry
            srt_entry = (
                f"{entry_id}\n"
                f"{self._format_timestamp(start_time)} --> {self._format_timestamp(end_time)}\n"
                f"{text}\n"
            )
            srt_entries.append(srt_entry)
            
            entry_id += 1
            i += max_words_per_line
        
        return "\n".join(srt_entries)
    
    @staticmethod
    def _format_timestamp(seconds: float) -> str:
        """Format seconds as SRT timestamp (HH:MM:SS,mmm)."""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        millis = int((seconds % 1) * 1000)
        return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"
    
    def detect_language(self, audio_path: str) -> Tuple[str, float]:
        """
        Detect the language of an audio file.
        
        Args:
            audio_path: Path to audio file
            
        Returns:
            Tuple of (language_code, confidence)
        """
        if self.model is None:
            self.load_model()
        
        # Transcribe just the first 30 seconds for language detection
        segments, info = self.model.transcribe(
            audio_path,
            language=None,
            task="transcribe"
        )
        
        return info.language, info.language_probability


# Example usage
if __name__ == "__main__":
    # Initialize ASR
    asr = WhisperASR(model_size="base", device="auto")
    
    # Example audio file path
    audio_file = "path/to/audio.mp3"
    
    # Transcribe
    result = asr.transcribe(audio_file, language="en")
    print("Transcription:")
    print(result["text"])
    print(f"\nDetected language: {result['language']} ({result['language_probability']:.2%})")
    
    # Generate SRT
    srt_content = asr.transcribe_to_srt(audio_file, output_path="output.srt")
    print("\nSRT generated")
    
    # Detect language
    lang, conf = asr.detect_language(audio_file)
    print(f"\nLanguage: {lang} (confidence: {conf:.2%})")
