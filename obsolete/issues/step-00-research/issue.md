# Step 0: Research Prototypes (Local Only)

**Status:** Not Started  
**Priority:** High  
**Dependencies:** None

## Overview

Create research prototype stubs in Python and C# for testing local model integrations. These prototypes serve as proof-of-concept implementations before full pipeline integration.

## Target Audience
- All segments: `women/men` 
- All age buckets: `10-13`, `14-17`, `18-23`

## Checklist

### Python Prototypes (`/research/python/`)

- [ ] `llm_call.py` - Ollama CLI wrapper for Qwen2.5 & Llama3.1
- [ ] `asr_whisper.py` - faster-whisper with `word_timestamps=True`
- [ ] `sdxl_keyframe.py` - Diffusers SDXL base+refiner
- [ ] `ltx_generate.py` - Shot → short clip generation
- [ ] `lufs_normalize.py` - ffmpeg loudnorm to -14 LUFS
- [ ] `srt_tools.py` - SRT/JSON build & merge
- [ ] `interpolation.py` - RIFE/DAIN/FILM wrapper

### C# Prototypes (`/research/csharp/`)

- [ ] `OllamaClient.cs` - Spawn process, stream tokens
- [ ] `WhisperClient.cs` - Subprocess to python or ONNX
- [ ] `FFmpegClient.cs` - Encode, crop 9:16, loudnorm
- [ ] `Orchestrator.cs` - Calls out to Python for SDXL/LTX as needed

## Acceptance Criteria

- [ ] All Python stub files exist in `/research/python/`
- [ ] All C# stub files exist in `/research/csharp/`
- [ ] Each file contains basic function/class signatures
- [ ] Documentation comments explain the purpose of each prototype
- [ ] No full implementation required - stubs only

## Related Files

- `/research/python/` - Python research prototypes directory
- `/research/csharp/` - C# research prototypes directory

## Validation

Comment `@copilot check` when all stub files exist and are documented.

## Notes

These are **prototypes only** - not production code. They demonstrate feasibility and API patterns for the main pipeline implementation.
