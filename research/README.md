# Research Prototypes

This directory contains research prototypes for local-only model orchestration and media processing.

## Purpose

These prototypes demonstrate how to integrate various AI models and media processing tools for video generation pipelines. They serve as:

1. **Reference Implementations**: Show how to interact with different tools and models
2. **API Design**: Define clean interfaces for future production implementations
3. **Local-First**: Focus on running models locally without cloud dependencies
4. **Educational**: Demonstrate best practices for working with AI models

## Python Implementations

Located in `/research/python/`:

### Core Components

#### `llm_call.py` - Ollama CLI Wrapper
- Wrapper for local LLM inference using Ollama
- Supports both generation and chat completion
- Command-line interface to Ollama models
- Example models: Llama2, Mistral, etc.

**Key Features:**
- Simple text generation
- Chat message format support
- Model listing and downloading
- Temperature and token control

**Usage:**
```python
from llm_call import OllamaClient

client = OllamaClient(model="llama2")
response = client.generate(
    prompt="Write a story about a robot",
    system="You are a creative writer",
    temperature=0.8
)
```

#### `asr_whisper.py` - Faster-Whisper ASR
- Speech-to-text transcription using faster-whisper
- Word-level timestamp alignment
- SRT subtitle generation
- Language detection

**Key Features:**
- Multiple model sizes (tiny to large-v3)
- Word-level timestamps
- Automatic SRT generation
- Language auto-detection
- GPU acceleration support

**Usage:**
```python
from asr_whisper import WhisperASR

asr = WhisperASR(model_size="base")
result = asr.transcribe("audio.mp3", language="en")
print(result["text"])

# Generate SRT subtitles
asr.transcribe_to_srt("audio.mp3", "subtitles.srt")
```

#### `lufs_normalize.py` - FFmpeg LUFS Normalization
- Professional audio normalization using EBU R128 standard
- Two-pass normalization for accuracy
- Audio metadata extraction
- Batch processing support

**Key Features:**
- LUFS-based loudness normalization
- Two-pass accurate normalization
- Audio file information extraction
- Batch processing

**Usage:**
```python
from lufs_normalize import LUFSNormalizer

normalizer = LUFSNormalizer(target_lufs=-16.0)
result = normalizer.normalize(
    "input.mp3",
    "output.mp3",
    two_pass=True
)
```

#### `srt_tools.py` - SRT Subtitle Tools
- Parse, build, and manipulate SRT subtitle files
- Merge multiple SRT files
- Adjust timing and synchronization
- Convert between SRT and JSON formats

**Key Features:**
- SRT parsing and generation
- Subtitle merging
- Timing adjustments
- Format conversion (SRT ↔ JSON)
- Statistics extraction

**Usage:**
```python
from srt_tools import SRTTools

# Parse SRT
entries = SRTTools.parse_srt("input.srt")

# Merge files
SRTTools.merge_srt_files(
    ["part1.srt", "part2.srt"],
    "merged.srt",
    time_offsets=[0.0, 30.0]
)

# Convert to JSON
SRTTools.srt_to_json("input.srt", "output.json")
```

#### `sdxl_keyframe.py` - SDXL Image Generation
- Text-to-image generation using Stable Diffusion XL
- Generate video keyframes from descriptions
- Style presets for consistent look
- Batch generation support

**Key Features:**
- SDXL base + refiner support
- Multiple style presets
- Seed control for reproducibility
- Keyframe sequence generation
- Memory optimization

**Usage:**
```python
from sdxl_keyframe import SDXLKeyframeGenerator

gen = SDXLKeyframeGenerator(use_refiner=False)
image = gen.generate_keyframe(
    prompt="A sunset over mountains",
    width=1024,
    height=768,
    seed=42,
    output_path="keyframe.png"
)
```

#### `ltx_generate.py` - Video Generation
- Image-to-video generation
- Shot-to-clip conversion
- Motion control and camera movement
- Batch video generation

**Key Features:**
- Image-to-video (animate static images)
- Motion intensity control
- Ken Burns effects
- Multi-clip generation

**Usage:**
```python
from ltx_generate import LTXVideoGenerator

gen = LTXVideoGenerator(fps=24)
video = gen.image_to_video(
    image_path="keyframe.png",
    output_path="clip.mp4",
    motion_bucket_id=127
)
```

#### `interpolation.py` - Frame Interpolation
- AI-based frame interpolation for smooth video
- Support for RIFE, DAIN, and FILM models
- Increase framerate (e.g., 24fps → 60fps)
- Batch processing

**Key Features:**
- Multiple interpolation methods
- FPS upscaling
- FFmpeg fallback for basic interpolation
- Batch video processing

**Usage:**
```python
from interpolation import VideoInterpolator

interpolator = VideoInterpolator(method="rife")
interpolator.interpolate_video(
    "input.mp4",
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
- C# implementation for Whisper ASR
- Implements `IWhisperClient` interface
- Word-level timestamps
- SRT generation
- Language detection

**Usage:**
```csharp
IWhisperClient whisper = new WhisperClient(modelSize: "base");
var result = await whisper.TranscribeAsync("audio.mp3", language: "en");
Console.WriteLine(result.Text);

// Generate SRT
await whisper.TranscribeToSrtAsync("audio.mp3", "subtitles.srt");
```

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
