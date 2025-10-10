# Step 00: Research Prototypes

## Purpose

Create research prototype stubs in Python and C# for testing local model integrations. These prototypes serve as proof-of-concept implementations before full pipeline integration. This step validates that we can:
- Call local LLMs (Ollama with Qwen2.5 and Llama3.1)
- Run Whisper ASR with word-level timestamps
- Generate images with SDXL (base + refiner)
- Synthesize video with LTX-Video
- Process audio/video with FFmpeg

## Status

**Implementation:** ⚠️ Partial (prototypes exist, build errors present)  
**Testing:** ⚠️ Needs Testing (blocked by build errors)  
**Documentation:** ✅ Complete (this README + issue.md)

## Dependencies

**Requires:**
- **Previous steps:** None (this is step 0)
- **API services:** None (local-only prototypes)
- **Models/Libraries:**
  - Ollama (for local LLM)
  - faster-whisper (for ASR)
  - Diffusers + SDXL (for image generation)
  - LTX-Video (for video synthesis)
  - FFmpeg (for audio/video processing)

**Outputs used by:**
- These are prototypes; patterns used throughout Steps 01-13
- C# Orchestrator patterns inform production pipeline

## Implementation

### Code Location

**C# Research Prototypes:**
- Primary: `src/CSharp/StoryGenerator.Research/`
  - `OllamaClient.cs` - Spawn Ollama process, stream tokens
  - `WhisperClient.cs` - Subprocess to Python or ONNX
  - `FFmpegClient.cs` - Encode, crop 9:16, loudnorm
  - `Orchestrator.cs` - Orchestrates calls to Python for SDXL/LTX

**Python Research Prototypes:**
- Primary: `research/python/`
- Production Scripts: `src/scripts/`
  - `whisper_asr.py` - faster-whisper with word_timestamps=True
  - `sdxl_generation.py` - Diffusers SDXL base+refiner
  - `ltx_synthesis.py` - Shot → short clip generation

### Key Classes/Functions

**C# Research:**
- `OllamaClient` - Interface to local Ollama LLM server
- `WhisperClient` - Wrapper for Whisper ASR (Python subprocess)
- `FFmpegClient` - Audio/video processing utilities
- `Orchestrator` - Demonstration of hybrid C#/Python architecture

**Python Scripts:**
- `whisper_asr.py:transcribe()` - ASR with word timestamps
- `sdxl_generation.py:generate()` - Image generation
- `ltx_synthesis.py:synthesize()` - Video generation

## Input/Output

### Input Format

**For Research Prototypes:**
- Test audio files (`.wav`, `.mp3`)
- Test prompts (text strings)
- Sample configurations (JSON)

**Example locations:**
- Test audio: `research/test_audio/sample.wav`
- Test prompts: Inline in code or `research/test_prompts.txt`

### Output Format

**Prototype outputs:**
- ASR transcriptions (JSON with word timestamps)
- Generated images (PNG files)
- Generated video clips (MP4 files)
- Normalized audio (WAV files)

**Location:** Typically written to temp directories or `research/output/`

## Usage

### CLI Command

⚠️ **Currently Blocked:** Build errors prevent CLI execution

**Once fixed:**
```bash
# Build Research project
dotnet build src/CSharp/StoryGenerator.Research/

# Run Ollama client test
dotnet run --project src/CSharp/StoryGenerator.Research/ -- ollama

# Run Whisper client test  
dotnet run --project src/CSharp/StoryGenerator.Research/ -- whisper path/to/audio.wav

# Run FFmpeg client test
dotnet run --project src/CSharp/StoryGenerator.Research/ -- ffmpeg path/to/video.mp4
```

### Programmatic Usage

**C# Example:**
```csharp
// Ollama LLM
var ollama = new OllamaClient();
var response = await ollama.GenerateAsync("Tell me a story");

// Whisper ASR
var whisper = new WhisperClient();
var transcription = await whisper.TranscribeAsync("audio.wav");

// FFmpeg processing
var ffmpeg = new FFmpegClient();
await ffmpeg.NormalizeAudioAsync("input.wav", "output.wav", targetLufs: -14);
```

**Python Example:**
```python
# Whisper ASR
from src.scripts.whisper_asr import transcribe
result = transcribe("audio.wav", word_timestamps=True)

# SDXL Image Generation
from src.scripts.sdxl_generation import generate
image = generate(prompt="A beautiful landscape", steps=50)

# LTX Video Synthesis
from src.scripts.ltx_synthesis import synthesize
video = synthesize(frames=[...], fps=24)
```

### Configuration

**Ollama Configuration:**
```json
{
  "model": "qwen2.5:latest",
  "temperature": 0.7,
  "max_tokens": 500
}
```

**Whisper Configuration:**
```json
{
  "model_size": "base",
  "language": "en",
  "word_timestamps": true
}
```

**SDXL Configuration:**
```json
{
  "base_model": "stabilityai/stable-diffusion-xl-base-1.0",
  "refiner_model": "stabilityai/stable-diffusion-xl-refiner-1.0",
  "steps": 50,
  "guidance_scale": 7.5
}
```

## Testing

### Manual Test

⚠️ **Prerequisite:** Fix build errors first

```bash
# 1. Install Ollama and pull model
ollama pull qwen2.5:latest

# 2. Test Ollama client
dotnet run --project src/CSharp/StoryGenerator.Research/ -- ollama
# Verify: Should see generated text response

# 3. Test Whisper (requires Python environment)
python3 src/scripts/whisper_asr.py --input test_audio.wav
# Verify: Should output JSON with word timestamps

# 4. Test SDXL
python3 src/scripts/sdxl_generation.py --prompt "Test image"
# Verify: Should generate image file

# 5. Test FFmpeg
dotnet run --project src/CSharp/StoryGenerator.Research/ -- ffmpeg test.mp4
# Verify: Should process video successfully
```

### Automated Tests

**Test Files:**
- `src/CSharp/StoryGenerator.Research.Tests/` (need to create)
- `src/scripts/tests/` (exists, needs expansion)

**Run Tests:**
```bash
# C# tests (after creating test project)
dotnet test src/CSharp/StoryGenerator.Research.Tests/

# Python tests
cd src/scripts
pytest tests/
```

## Error Handling

**Common Errors:**

1. **CS8625: Cannot convert null literal to non-nullable reference type**
   - Cause: Nullable reference type violations in C# code
   - Solution: Fix by adding `?` to nullable types or initializing to non-null values
   - Status: 24 errors currently in Research project

2. **Ollama not running**
   - Cause: Ollama server not started
   - Solution: Start Ollama with `ollama serve`

3. **Model not found**
   - Cause: Required model not downloaded
   - Solution: `ollama pull qwen2.5:latest`

4. **Python dependencies missing**
   - Cause: Virtual environment not set up
   - Solution: `pip install -r requirements.txt`

5. **CUDA/GPU errors**
   - Cause: GPU not available or drivers missing
   - Solution: Use CPU mode or install proper drivers

**Retry Policy:** Prototypes typically don't retry automatically

**Graceful Degradation:** Fall back to CPU if GPU unavailable

## Performance

**Expected Runtime:**
- Ollama LLM call: 2-10 seconds (depends on length)
- Whisper ASR: 1-5 seconds per minute of audio
- SDXL generation: 10-30 seconds per image (with GPU)
- LTX-Video synthesis: 30-120 seconds per clip (with GPU)
- FFmpeg operations: Varies by file size

**Resource Requirements:**
- **CPU:** Multi-core recommended (4+ cores)
- **Memory:** 8GB minimum, 16GB recommended
- **GPU:** Optional but strongly recommended for SDXL and LTX-Video
  - NVIDIA GPU with 8GB+ VRAM for SDXL
  - NVIDIA GPU with 12GB+ VRAM for LTX-Video
- **Storage:** 10GB for models, varies for outputs
- **API Calls:** None (all local)

**Optimization Tips:**
- Use GPU for image and video generation (10-50x speedup)
- Cache model downloads to avoid re-downloading
- Use smaller Whisper models for faster transcription
- Enable half-precision (fp16) for faster inference with minimal quality loss

## Related Documentation

- [Main Issue](./issue.md) - Detailed requirements and checklist
- [Research Directory](../../research/README.md) - Research documentation
- [Python Scripts](../../src/scripts/README.md) - Production Python scripts
- [Pipeline Guide](../../src/CSharp/PIPELINE_GUIDE.md) - Overall pipeline architecture
- [Quick Start](../../issues/QUICKSTART.md) - Getting started guide

## Examples

### Example 1: Test Ollama LLM

**Input:**
```json
{
  "prompt": "Write a short story about a brave knight",
  "model": "qwen2.5:latest",
  "temperature": 0.7
}
```

**Command:**
```bash
# Start Ollama server
ollama serve

# Run client (once build fixed)
dotnet run --project src/CSharp/StoryGenerator.Research/ -- ollama
```

**Expected Output:**
```
Once upon a time, in a distant kingdom, there lived a brave knight named...
```

### Example 2: Test Whisper ASR

**Input:** `test_audio.wav` (sample audio file)

**Command:**
```bash
python3 src/scripts/whisper_asr.py --input test_audio.wav --output transcription.json
```

**Expected Output:**
```json
{
  "text": "This is a test transcription",
  "segments": [...],
  "words": [
    {"word": "This", "start": 0.0, "end": 0.2},
    {"word": "is", "start": 0.2, "end": 0.3},
    ...
  ]
}
```

### Example 3: Test SDXL Image Generation

**Command:**
```bash
python3 src/scripts/sdxl_generation.py \
  --prompt "A serene mountain landscape at sunset" \
  --output test_image.png \
  --steps 50
```

**Expected Output:**
- Generated image file: `test_image.png`
- Console log showing generation progress

## Troubleshooting

**Q: Build fails with nullable reference errors**  
A: This is a known issue. The Research project needs nullable reference type fixes. Track progress in VERIFICATION_REPORT.md. Fix by:
```csharp
// Change this:
string value = null;

// To this:
string? value = null;  // or ensure it's always initialized
```

**Q: Ollama returns "model not found"**  
A: Pull the model first: `ollama pull qwen2.5:latest`

**Q: Whisper fails with "No module named 'faster_whisper'"**  
A: Install Python dependencies: `pip install faster-whisper`

**Q: SDXL crashes with CUDA out of memory**  
A: Either:
1. Use a smaller resolution (`--width 512 --height 512`)
2. Enable CPU mode (`--device cpu`)
3. Use half-precision (`--fp16`)

**Q: LTX-Video is extremely slow**  
A: Video synthesis requires a powerful GPU. Expect 30-120 seconds per short clip. Use smaller frame counts or lower resolution for faster prototyping.

**Q: FFmpeg command not found**  
A: Install FFmpeg:
- Ubuntu/Debian: `sudo apt install ffmpeg`
- macOS: `brew install ffmpeg`
- Windows: Download from https://ffmpeg.org/

## Changelog

- **2025-10-10**: Added comprehensive README documentation
- **2024**: Initial prototype implementations created

---

**Last Updated:** 2025-10-10  
**Maintained By:** StoryGenerator Development Team  
**Status:** ⚠️ Build errors need fixing before testing
