"""
Whisper ASR (Automatic Speech Recognition) module.

This module provides speech-to-text transcription using Whisper.
Currently returns mock data; real model integration pending.

Operations:
    - asr.transcribe: Transcribe audio file to text with timestamps
"""

import sys
from common.io_json import run_jsonl_loop


def handle_request(request_id: str, op: str, args: dict):
    """
    Handle ASR operations.
    
    Args:
        request_id: Request identifier
        op: Operation to perform
        args: Operation arguments
        
    Returns:
        Operation result
        
    Raises:
        ValueError: If operation is unknown
    """
    if op == "echo":
        # Echo test operation
        return {"echo": args}
    elif op == "asr.transcribe":
        # Mock transcription response
        audio_path = args.get("audio_path")
        language = args.get("language", "auto")
        
        # TODO: Load and use real Whisper model
        # from faster_whisper import WhisperModel
        # model = WhisperModel("base", device="cpu")
        # segments, info = model.transcribe(audio_path, language=language)
        
        return {
            "text": "[MOCK] Transcribed text will appear here.",
            "segments": [
                {
                    "start": 0.0,
                    "end": 2.5,
                    "text": "[MOCK] First segment"
                },
                {
                    "start": 2.5,
                    "end": 5.0,
                    "text": "[MOCK] Second segment"
                }
            ],
            "language": language
        }
    else:
        raise ValueError(f"Unknown operation: {op}")


if __name__ == "__main__":
    run_jsonl_loop(handle_request)
