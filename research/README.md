# Research Prototypes

This directory contains research prototypes for local-only model orchestration and media processing.

## 🆕 YouTube Subtitle Research (NEW)

**Complete toolkit for analyzing YouTube video subtitles**

### Quick Access
- **Tool**: [`python/youtube_subtitle_analyzer.py`](python/youtube_subtitle_analyzer.py) - Production-ready analysis tool
- **Guide**: [`YOUTUBE_SUBTITLE_RESEARCH.md`](YOUTUBE_SUBTITLE_RESEARCH.md) - Comprehensive best practices
- **Examples**: [`subtitle_analysis/`](subtitle_analysis/) - Sample analyses and patterns
- **Quick Start**: [`subtitle_analysis/QUICKSTART.md`](subtitle_analysis/QUICKSTART.md) - Get started in 5 minutes

### What's Included
✅ Download and analyze any YouTube video  
✅ Extract timing and readability metrics  
✅ Generate comprehensive reports  
✅ Validate subtitle quality  
✅ Ready-to-use pipeline configurations  

### Usage
```bash
pip install yt-dlp
python research/python/youtube_subtitle_analyzer.py https://www.youtube.com/shorts/41QD8C6tqIU
```

📖 **Full documentation**: [`subtitle_analysis/INDEX.md`](subtitle_analysis/INDEX.md)

---

## 🔬 Architecture Decision Documents

**NEW: Comprehensive analysis of C# vs Python vs Hybrid approaches:**
- **[../docs/CSHARP_VS_PYTHON_COMPARISON.md](../docs/CSHARP_VS_PYTHON_COMPARISON.md)** - Complete comparison with decision matrix and stage-by-stage recommendations
- **[../docs/HYBRID_ARCHITECTURE_QUICKREF.md](../docs/HYBRID_ARCHITECTURE_QUICKREF.md)** - Quick reference guide for developers

**Key Recommendation**: **Hybrid Architecture** with C# as primary orchestration language and strategic Python integration for ML-heavy tasks (ASR, SDXL, LTX-Video).

---

## Purpose

These prototypes demonstrate how to integrate various AI models and media processing tools for video generation pipelines. They serve as:

1. **Reference Implementations**: Show how to interact with different tools and models
2. **API Design**: Define clean interfaces for future production implementations
3. **Local-First**: Focus on running models locally without cloud dependencies
4. **Educational**: Demonstrate best practices for working with AI models

## Research Documents

This directory also contains comprehensive research documents on various aspects of video content generation:

### Content Strategy
- **[YOUTUBE_CONTENT_STRATEGY.md](YOUTUBE_CONTENT_STRATEGY.md)** - Comprehensive research on YouTube content formats
  - Short-form content (Shorts) pros and cons
  - Long-form content pros and cons
  - Aspect ratio comparison (16:9 vs 9:16)
  - Hybrid strategies for maximizing reach and monetization
  - Implementation recommendations for StoryGenerator

### Video Synthesis
- **[VIDEO_SYNTHESIS_RESEARCH.md](VIDEO_SYNTHESIS_RESEARCH.md)** - Research on video generation approaches
  - LTX-Video for short-form content
  - SDXL + Frame Interpolation for high-quality videos
  - Implementation guides and C# examples

### Platform & Trends
- **[VIRAL_VIDEO_REQUIREMENTS.md](VIRAL_VIDEO_REQUIREMENTS.md)** - Specifications for viral video content
  - Platform requirements and metadata
  - Regions, languages, and localization
  - Trend aggregation and scoring
  - Database schema and storage

- **[SOCIAL_PLATFORMS_TRENDS.md](SOCIAL_PLATFORMS_TRENDS.md)** - Social media trend collection research
  - YouTube Data API integration
  - TikTok and Instagram trend sources
  - Multi-platform aggregation strategies

## Python Implementations

Located in `/research/python/`:

> **Note:** Most Python research files have been moved to `obsolete/research/python/` as they were part of the obsolete Python implementation. Only files actively used by the C# implementation remain here.

### Active Components (Used by C#)

#### `whisper_subprocess.py` - Whisper Subprocess Wrapper
- Command-line wrapper for faster-whisper
- JSON-based communication for C# integration
- Supports all faster-whisper features
- **Used by C# WhisperClient via subprocess**

**Key Features:**
- JSON input/output for easy integration
- Command-line interface
- Automatic device detection (CPU/GPU)
- Error handling with structured responses

**Usage:**
```bash
# Transcribe audio
python3 whisper_subprocess.py transcribe \
  --audio-path audio.mp3 \
  --model-size large-v3 \
  --language en \
  --word-timestamps

# Detect language
python3 whisper_subprocess.py detect_language \
  --audio-path audio.mp3 \
  --model-size base
```

#### `test_whisper_integration.py` - Whisper Integration Tests
- Test script to verify whisper_subprocess.py functionality
- Validates transcription and language detection
- Used for integration testing with C# WhisperClient

### Obsolete Components (Archived)

The following Python research files have been moved to `obsolete/research/python/` as they were part of the Python implementation research and are no longer actively used:

- `llm_call.py` - Ollama CLI wrapper (C# now uses OllamaClient.cs directly)
- `asr_whisper.py` - Faster-Whisper ASR library (C# uses whisper_subprocess.py instead)
- `sdxl_keyframe.py` - SDXL image generation (C# generates inline Python scripts)
- `ltx_generate.py` - Video generation (C# generates inline Python scripts)
- `lufs_normalize.py` - Audio normalization (C# uses FFmpeg directly)
- `srt_tools.py` - SRT subtitle tools (C# has native implementations)
- `interpolation.py` - Frame interpolation (C# generates inline Python scripts)
- `README_VIDEO_CLIPS.md` - Documentation for video clip generation
    "output_60fps.mp4",
    target_fps=60
)
```

## C# Implementations

Located in `/research/csharp/`:

### Core Components

#### Interfaces

The C# implementation follows interface-based design for better testability and dependency injection:

- **`IOllamaClient`** - Interface for Ollama LLM operations
- **`IWhisperClient`** - Interface for Whisper ASR operations
- **`IFFmpegClient`** - Interface for FFmpeg media processing

#### `OllamaClient.cs`
- C# wrapper for Ollama CLI
- Implements `IOllamaClient` interface
- Async/await support
- Chat completion format
- Model management

**Usage:**
```csharp
IOllamaClient client = new OllamaClient(model: "llama2");
var response = await client.GenerateAsync(
    prompt: "Tell me a story",
    system: "You are a storyteller",
    temperature: 0.8f
);
```

#### `WhisperClient.cs`
- C# implementation for Whisper ASR using faster-whisper large-v3
- Implements `IWhisperClient` interface
- Uses subprocess to call Python faster-whisper implementation
- Word-level timestamps with high precision
- SRT and VTT subtitle generation
- Language detection with confidence scores
- Multiple model size support (tiny to large-v3)
- GPU acceleration support

**Features:**
- Transcription with word timestamps
- SRT subtitle generation
- VTT subtitle generation  
- Language auto-detection
- Translation to English
- Voice Activity Detection (VAD)

**Usage:**
```csharp
IWhisperClient whisper = new WhisperClient(
    modelSize: "large-v3",
    device: "auto",
    computeType: "float16"
);

// Transcribe with word timestamps
var result = await whisper.TranscribeAsync("audio.mp3", language: "en");
Console.WriteLine(result.Text);

// Generate SRT subtitles
await whisper.TranscribeToSrtAsync("audio.mp3", "subtitles.srt");

// Generate VTT subtitles
await whisper.TranscribeToVttAsync("audio.mp3", "subtitles.vtt");

// Detect language
var (lang, confidence) = await whisper.DetectLanguageAsync("audio.mp3");
```

**See Also:** [ASR_README.md](csharp/ASR_README.md) for detailed documentation

#### `FFmpegClient.cs`
- C# wrapper for FFmpeg/FFprobe
- Implements `IFFmpegClient` interface
- Audio normalization (LUFS)
- Media file processing
- Format conversion

**Usage:**
```csharp
IFFmpegClient ffmpeg = new FFmpegClient();
var result = await ffmpeg.NormalizeAudioAsync(
    inputPath: "input.mp3",
    outputPath: "output.mp3",
    targetLufs: -16.0,
    twoPass: true
);

// Get audio info
var info = await ffmpeg.GetAudioInfoAsync("audio.mp3");
```

#### `Orchestrator.cs`
- High-level pipeline orchestration
- Coordinates all components via interfaces
- End-to-end video generation
- Batch processing
- Dependency injection ready

**Usage:**
```csharp
// Default constructor creates concrete implementations
var orchestrator = new Orchestrator();

// Or inject custom implementations (useful for testing/mocking)
IOllamaClient ollamaClient = new OllamaClient();
IWhisperClient whisperClient = new WhisperClient();
IFFmpegClient ffmpegClient = new FFmpegClient();
var orchestrator = new Orchestrator(ollamaClient, whisperClient, ffmpegClient);

// Generate complete story
var story = await orchestrator.GenerateStoryAsync(
    topic: "A robot learning to paint",
    style: "dramatic"
);

// Process audio
var audioResult = await orchestrator.ProcessAudioAsync(
    audioPath: "voiceover.mp3",
    outputDir: "output/"
);

// Full pipeline
var videoResult = await orchestrator.CreateVideoAsync(
    topic: "Space exploration",
    outputDir: "video_output/"
);
```

## Architecture

### Pipeline Flow

```
1. LLM Generation (Ollama)
   ↓ Story idea & script
2. TTS Generation (External service)
   ↓ Voiceover audio
3. Audio Processing (FFmpeg)
   ↓ Normalized audio
4. ASR Processing (Whisper)
   ↓ Transcription & SRT
5. Image Generation (SDXL)
   ↓ Keyframes
6. Video Generation (LTX/SVD)
   ↓ Video clips
7. Frame Interpolation (RIFE)
   ↓ Smooth video
8. Final Composition (FFmpeg)
   ↓ Final video with audio & subtitles
```

### Design Principles

1. **Local-First**: All models run locally (no API dependencies except for TTS)
2. **Modular**: Each component is independent and reusable
3. **Async**: C# implementations use async/await for better performance
4. **Type-Safe**: Strong typing for reliability
5. **Interface-Based**: C# implementations use interfaces for dependency injection and testability
6. **Extensible**: Easy to add new models or replace components

## Requirements

### Python Dependencies
```
faster-whisper
diffusers
transformers
accelerate
torch
ffmpeg-python
Pillow
```

### System Requirements
- FFmpeg installed and in PATH
- For GPU acceleration: CUDA-capable GPU with drivers
- For Ollama: Ollama installed and running
- Python 3.8+
- .NET 8.0+ (for C#)

## Installation

### Python Setup
```bash
cd research/python

# Install dependencies
pip install faster-whisper diffusers transformers accelerate torch Pillow

# Ensure FFmpeg is installed
ffmpeg -version

# Install Ollama (macOS/Linux)
curl -fsSL https://ollama.ai/install.sh | sh

# Pull a model
ollama pull llama2
```

### C# Setup
```bash
cd research/csharp

# Ensure .NET 8.0 is installed
dotnet --version

# These are stubs - compile with your project
```

## Usage Examples

### End-to-End Story Generation (Python)

```python
from llm_call import OllamaClient
from asr_whisper import WhisperASR
from lufs_normalize import LUFSNormalizer
from sdxl_keyframe import SDXLKeyframeGenerator
from ltx_generate import LTXVideoGenerator

# 1. Generate story script
llm = OllamaClient(model="llama2")
script = llm.generate(
    prompt="Write a short story about AI and creativity",
    system="You are a creative writer"
)

# 2. After TTS generates audio...
# 3. Normalize audio
normalizer = LUFSNormalizer()
normalizer.normalize("voiceover.mp3", "voiceover_norm.mp3", two_pass=True)

# 4. Generate subtitles
asr = WhisperASR()
asr.transcribe_to_srt("voiceover_norm.mp3", "subtitles.srt")

# 5. Generate keyframes
sdxl = SDXLKeyframeGenerator()
keyframes = sdxl.generate_keyframe_sequence(
    prompts=["Scene 1 description", "Scene 2 description"],
    output_dir="keyframes/"
)

# 6. Generate video clips
ltx = LTXVideoGenerator()
clips = ltx.batch_generate_clips(
    shots=[
        {"image_path": kf, "intensity": 0.5, "duration": 2.0}
        for kf in keyframes
    ],
    output_dir="clips/"
)
```

### End-to-End Story Generation (C#)

```csharp
using StoryGenerator.Research;

var orchestrator = new Orchestrator();

// Generate complete video from topic
var result = await orchestrator.CreateVideoAsync(
    topic: "A day in the life of a sentient AI",
    outputDir: "output/video_001/",
    style: "cinematic"
);

if (result.Success)
{
    Console.WriteLine($"Video created: {result.FinalVideoPath}");
    Console.WriteLine($"Script: {result.ScriptPath}");
    Console.WriteLine($"Generated {result.KeyframePaths.Count} keyframes");
}
```

## Notes

- **Research Prototypes**: These are proof-of-concept implementations
- **Production Use**: Requires additional error handling, validation, and optimization
- **GPU Memory**: Image/video generation requires significant VRAM
- **Model Downloads**: First run will download models (can be several GB)
- **Processing Time**: Video generation is computationally intensive

## Future Enhancements

- [ ] Better error handling and retry logic
- [ ] Progress callbacks for long operations
- [ ] Caching for generated assets
- [ ] More style presets and templates
- [ ] REST API wrapper for remote access
- [ ] Docker containers for easy deployment
- [ ] Web UI for non-programmers

## Contributing

These prototypes are for research purposes. Contributions and improvements are welcome.

## License

Same as the main StoryGenerator project.
