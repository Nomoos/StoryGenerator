#!/usr/bin/env python3
"""
Whisper subprocess wrapper for C# integration.
Handles JSON-based communication for transcription operations.
"""

import sys
import json
import argparse
from pathlib import Path
from typing import Optional, Dict, Any

try:
    from faster_whisper import WhisperModel
    FASTER_WHISPER_AVAILABLE = True
except ImportError:
    FASTER_WHISPER_AVAILABLE = False
    print(json.dumps({
        "error": "faster-whisper not installed. Install with: pip install faster-whisper",
        "success": False
    }))
    sys.exit(1)


def transcribe_audio(
    audio_path: str,
    model_size: str = "large-v3",
    device: str = "auto",
    compute_type: str = "float16",
    language: Optional[str] = None,
    task: str = "transcribe",
    word_timestamps: bool = True,
    vad_filter: bool = True
) -> Dict[str, Any]:
    """
    Transcribe audio file using faster-whisper.
    
    Args:
        audio_path: Path to audio file
        model_size: Model size (tiny, base, small, medium, large-v2, large-v3)
        device: Device to use (cpu, cuda, auto)
        compute_type: Computation type (float16, float32, int8)
        language: Language code or None for auto-detection
        task: Task type (transcribe or translate)
        word_timestamps: Include word-level timestamps
        vad_filter: Apply voice activity detection filter
        
    Returns:
        Dictionary with transcription results
    """
    try:
        # Determine device
        if device == "auto":
            try:
                import torch
                device = "cuda" if torch.cuda.is_available() else "cpu"
            except ImportError:
                device = "cpu"
        
        # Load model
        model = WhisperModel(
            model_size,
            device=device,
            compute_type=compute_type if device == "cuda" else "float32"
        )
        
        # Transcribe
        segments, info = model.transcribe(
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
                "confidence": segment.avg_logprob if hasattr(segment, "avg_logprob") else None
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
            "success": True,
            "text": " ".join(text_parts).strip(),
            "segments": segment_list,
            "words": word_list if word_timestamps else None,
            "language": info.language,
            "languageProbability": info.language_probability
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


def detect_language(
    audio_path: str,
    model_size: str = "large-v3",
    device: str = "auto",
    compute_type: str = "float16"
) -> Dict[str, Any]:
    """
    Detect language of audio file.
    
    Args:
        audio_path: Path to audio file
        model_size: Model size
        device: Device to use
        compute_type: Computation type
        
    Returns:
        Dictionary with language detection results
    """
    try:
        # Determine device
        if device == "auto":
            try:
                import torch
                device = "cuda" if torch.cuda.is_available() else "cpu"
            except ImportError:
                device = "cpu"
        
        # Load model
        model = WhisperModel(
            model_size,
            device=device,
            compute_type=compute_type if device == "cuda" else "float32"
        )
        
        # Detect language (transcribe first 30 seconds)
        segments, info = model.transcribe(
            audio_path,
            language=None,
            task="transcribe"
        )
        
        # Consume first segment to trigger language detection
        _ = next(segments, None)
        
        return {
            "success": True,
            "language": info.language,
            "confidence": info.language_probability
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


def main():
    """Main entry point for command-line usage."""
    parser = argparse.ArgumentParser(
        description="Whisper ASR subprocess wrapper for C# integration"
    )
    parser.add_argument(
        "command",
        choices=["transcribe", "detect_language"],
        help="Command to execute"
    )
    parser.add_argument(
        "--audio-path",
        required=True,
        help="Path to audio file"
    )
    parser.add_argument(
        "--model-size",
        default="large-v3",
        help="Model size (default: large-v3)"
    )
    parser.add_argument(
        "--device",
        default="auto",
        help="Device to use: cpu, cuda, or auto (default: auto)"
    )
    parser.add_argument(
        "--compute-type",
        default="float16",
        help="Computation type: float16, float32, int8 (default: float16)"
    )
    parser.add_argument(
        "--language",
        help="Language code (e.g., en, es) or None for auto-detection"
    )
    parser.add_argument(
        "--task",
        default="transcribe",
        choices=["transcribe", "translate"],
        help="Task type (default: transcribe)"
    )
    parser.add_argument(
        "--word-timestamps",
        action="store_true",
        default=True,
        help="Include word-level timestamps (default: True)"
    )
    parser.add_argument(
        "--no-word-timestamps",
        action="store_false",
        dest="word_timestamps",
        help="Disable word-level timestamps"
    )
    parser.add_argument(
        "--vad-filter",
        action="store_true",
        default=True,
        help="Apply voice activity detection filter (default: True)"
    )
    parser.add_argument(
        "--no-vad-filter",
        action="store_false",
        dest="vad_filter",
        help="Disable VAD filter"
    )
    
    args = parser.parse_args()
    
    # Check if audio file exists
    if not Path(args.audio_path).exists():
        print(json.dumps({
            "success": False,
            "error": f"Audio file not found: {args.audio_path}"
        }))
        sys.exit(1)
    
    # Execute command
    if args.command == "transcribe":
        result = transcribe_audio(
            audio_path=args.audio_path,
            model_size=args.model_size,
            device=args.device,
            compute_type=args.compute_type,
            language=args.language,
            task=args.task,
            word_timestamps=args.word_timestamps,
            vad_filter=args.vad_filter
        )
    elif args.command == "detect_language":
        result = detect_language(
            audio_path=args.audio_path,
            model_size=args.model_size,
            device=args.device,
            compute_type=args.compute_type
        )
    else:
        result = {
            "success": False,
            "error": f"Unknown command: {args.command}"
        }
    
    # Output result as JSON
    print(json.dumps(result, indent=2))
    
    # Exit with appropriate code
    sys.exit(0 if result.get("success", False) else 1)


if __name__ == "__main__":
    main()
