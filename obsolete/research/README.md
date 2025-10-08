# Obsolete Research - Python Implementation

This directory contains research prototypes and scripts that were created for the obsolete Python implementation of StoryGenerator.

## Overview

These Python scripts were part of the research and prototyping phase for the Python-based implementation. They have been archived here for historical reference as the project has migrated to C# as the primary implementation.

## Archived Python Research Files

### `python/` Directory

The following Python research scripts have been moved here from `research/python/`:

#### LLM Integration
- **`llm_call.py`** - Ollama CLI wrapper for local LLM inference
  - Used for testing Ollama integration with Python
  - C# now uses OllamaClient.cs directly

#### Speech Recognition
- **`asr_whisper.py`** - Faster-Whisper ASR library wrapper
  - Python library-based approach to speech recognition
  - C# now uses whisper_subprocess.py via subprocess instead

#### Image Generation
- **`sdxl_keyframe.py`** - SDXL (Stable Diffusion XL) keyframe generation
  - Text-to-image generation for video keyframes
  - C# now generates inline Python scripts for SDXL operations

#### Video Generation
- **`ltx_generate.py`** - LTX-Video generation wrapper
  - Image-to-video and text-to-video generation
  - C# now generates inline Python scripts for video synthesis

#### Audio Processing
- **`lufs_normalize.py`** - FFmpeg LUFS audio normalization
  - Professional audio loudness normalization
  - C# now uses FFmpeg directly via FFmpegClient

#### Subtitle Tools
- **`srt_tools.py`** - SRT subtitle parsing and manipulation
  - Parse, merge, and convert SRT subtitle files
  - C# has native implementations for subtitle handling

#### Frame Interpolation
- **`interpolation.py`** - AI-based frame interpolation
  - RIFE, DAIN, and FILM model wrappers
  - C# now generates inline Python scripts for interpolation

#### Documentation
- **`README_VIDEO_CLIPS.md`** - Documentation for video clip generation workflows

## Active Research Files

**Note:** The following files remain in the active `research/python/` directory as they are actively used by the C# implementation:

- `whisper_subprocess.py` - Command-line wrapper used by C# WhisperClient
- `test_whisper_integration.py` - Integration tests for whisper_subprocess.py

## Status

⚠️ **OBSOLETE - Historic Reference Only**

These files are maintained solely for historical reference and learning purposes. They represent research and prototyping work done for the Python implementation.

**DO NOT USE FOR NEW DEVELOPMENT**

All active development has moved to C#. See the main `research/` directory for active C# research implementations.

## Related Documentation

- [/research/README.md](../../research/README.md) - Active C# research prototypes
- [/obsolete/Python/README.md](../Python/README.md) - Obsolete Python implementation
- [/obsolete/docs/PYTHON_OBSOLETE_NOTICE.md](../docs/PYTHON_OBSOLETE_NOTICE.md) - Python obsolescence notice
- [/src/CSharp/README.md](../../src/CSharp/README.md) - Active C# implementation

---

**Last Updated:** 2025-10-08  
**Status:** Archived
