# StoryGenerator Python Scripts

This directory contains Python scripts for ML operations in the StoryGenerator pipeline.

## Structure

```
src/scripts/
├── common/
│   ├── __init__.py
│   └── io_json.py          # JSONL protocol for C# subprocess communication
├── whisper_asr.py          # Speech-to-text transcription
├── sdxl_generation.py      # Text-to-image generation
├── ltx_synthesis.py        # Video synthesis
├── requirements.txt        # Base dependencies
└── pyproject.toml          # Python project configuration
```

## Protocol

Communication between C# orchestrator and Python scripts uses JSONL (JSON Lines):

**Request format:**
```json
{"id": "<uuid>", "op": "<command>", "args": {...}}
```

**Response format:**
```json
{"id": "<uuid>", "ok": true, "data": {...}, "error": null}
```

## Installation

### Base installation (minimal):
```bash
pip install -r requirements.txt
```

### With ML dependencies:
```bash
pip install -e ".[ml]"
```

### Development:
```bash
pip install -e ".[dev]"
```

## Testing

Run tests with pytest:
```bash
pytest
```

Run with coverage:
```bash
pytest --cov=common --cov-report=term-missing
```

## Usage

Each script can be run standalone for testing:

```bash
# Echo test
echo '{"id":"test-1","op":"echo","args":{"message":"hello"}}' | python whisper_asr.py

# Mock transcription
echo '{"id":"test-2","op":"asr.transcribe","args":{"audio_path":"test.mp3"}}' | python whisper_asr.py
```

## Operations

### whisper_asr.py
- `asr.transcribe`: Transcribe audio to text with timestamps

### sdxl_generation.py
- `img.generate`: Generate image from text prompt

### ltx_synthesis.py
- `video.synthesize`: Synthesize video from frames and audio

## Notes

- Current implementations return mock data
- Real model loading will be added in Phase 9
- Heavy model dependencies are optional and can be installed separately
