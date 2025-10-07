# Video Synthesis - C# Implementation

This directory contains C# implementation examples and utilities for video synthesis research in the StoryGenerator pipeline.

## Overview

The video synthesis module provides implementations for generating videos from keyframes and text prompts using two primary approaches:

1. **LTX-Video**: Fast generation for short-form vertical videos (10-20 seconds)
2. **SDXL + Frame Interpolation**: High-quality keyframe generation with smooth interpolation

## Directory Structure

```
CSharp/
├── Generators/
│   ├── IVideoSynthesizer.cs              # Core interfaces for video synthesis
│   ├── IVideoSynthesizerFactory.cs       # Factory interface and implementation
│   ├── VideoSynthesisBase.cs             # Base class with common functionality
│   ├── LTXVideoSynthesizer.cs            # LTX-Video implementation
│   └── KeyframeVideoSynthesizer.cs       # SDXL + interpolation implementation
├── Models/
│   └── VideoClip.cs                      # Video clip data models
├── Tools/
│   └── VideoSynthesisComparator.cs       # Comparison utility
├── Examples/
│   └── VideoSynthesisExample.cs          # Usage examples
├── INTERFACES_GUIDE.md                   # Interface documentation
└── README_VIDEO_SYNTHESIS.md             # This file
```

## Components

### 1. Interfaces

**IVideoSynthesizer, ISceneVideoSynthesizer, IKeyframeVideoSynthesizer**
- Core interfaces defining video synthesis contracts
- Enable polymorphic usage and dependency injection
- Support factory pattern and testability
- See `INTERFACES_GUIDE.md` for detailed documentation

**IVideoSynthesizerFactory**
- Factory interface for creating synthesizer instances
- Supports multiple synthesis methods
- Centralized configuration and creation logic

### 2. VideoSynthesisBase

Base class providing common functionality for all video synthesis implementations:
- Python script execution
- File validation
- Path normalization
- Error handling

### 2. LTXVideoSynthesizer

Implementation for LTX-Video approach:
- Fast generation (20-30s per 10s clip)
- Native vertical video support (1080x1920)
- Simple text-to-video generation
- Optional keyframe conditioning

**Key Features:**
- 5-25 second video duration
- 24-30 FPS output
- VRAM: ~12GB
- Best for: TikTok, YouTube Shorts, Instagram Reels

### 3. KeyframeVideoSynthesizer

Implementation for SDXL + frame interpolation approach:
- Highest quality keyframes
- Multiple interpolation methods (RIFE, FILM, DAIN)
- Fine-grained composition control
- Flexible video length

**Key Features:**
- Customizable keyframes per scene
- Multiple interpolation algorithms
- Style presets support
- Best for: High-quality cinematic content

### 4. VideoClip Model

Data model representing generated video clips:
- Metadata (duration, resolution, FPS)
- Quality metrics
- Generation information
- Scene associations

### 5. VideoSynthesisComparator

Utility for comparing different approaches:
- Side-by-side testing
- Performance metrics
- Quality analysis
- Automated recommendations

## Usage Examples

### Example 1: Using Interfaces with Factory Pattern

```csharp
using StoryGenerator.Generators;

// Create factory
IVideoSynthesizerFactory factory = new VideoSynthesizerFactory();

// Create synthesizer using factory
IVideoSynthesizer synthesizer = factory.CreateSynthesizer(
    VideoSynthesisMethod.LTXVideo,
    width: 1080,
    height: 1920,
    fps: 30
);

// Use polymorphically
await synthesizer.GenerateVideoAsync(
    prompt: "A serene lake at sunset, camera panning right, cinematic",
    outputPath: "output/video.mp4",
    duration: 10
);
```

### Example 2: Basic LTX-Video Generation

```csharp
using StoryGenerator.Generators;

var synthesizer = new LTXVideoSynthesizer(
    width: 1080,
    height: 1920,
    fps: 30
);

string prompt = "A serene lake at sunset, camera panning right, cinematic";
string outputPath = "output/video.mp4";

bool success = await synthesizer.GenerateVideoAsync(
    prompt: prompt,
    outputPath: outputPath,
    duration: 10
);
```

### Example 2: SDXL + Frame Interpolation

```csharp
using StoryGenerator.Generators;

var config = new KeyframeVideoConfig
{
    TargetFps = 30,
    Method = InterpolationMethod.RIFE,
    KeyframesPerScene = 3
};

var synthesizer = new KeyframeVideoSynthesizer(config);

var stylePrompts = new List<string>
{
    "cinematic lighting",
    "photorealistic"
};

bool success = await synthesizer.GenerateSceneAsync(
    sceneDescription: "A mystical forest path",
    outputPath: "output/video.mp4",
    duration: 8.0,
    stylePrompts: stylePrompts
);
```

### Example 3: Motion Control

```csharp
var synthesizer = new LTXVideoSynthesizer();

bool success = await synthesizer.GenerateSceneClipAsync(
    sceneDescription: "City skyline at night",
    motionHint: "camera slowly panning right",
    outputPath: "output/scene.mp4",
    duration: 5.0
);
```

### Example 4: Compare Approaches

```csharp
using StoryGenerator.Tools;

var comparator = new VideoSynthesisComparator();

var results = await comparator.CompareApproachesAsync(
    testPrompt: "Beautiful sunset over ocean waves",
    duration: 10.0,
    outputDir: "output/comparison"
);
```

## Configuration

See `config/video_synthesis_config.json` for detailed configuration options:

- **Model settings**: Inference steps, guidance scale
- **Quality presets**: Fast, balanced, high_quality, maximum
- **Platform presets**: TikTok, YouTube, Instagram specific settings
- **Motion presets**: Predefined camera movements
- **Encoding settings**: Video codec, bitrate, quality

## Requirements

### Software Requirements

- .NET 6.0 or later
- Python 3.8+ with required packages
- FFmpeg (for video assembly)
- CUDA-capable GPU (recommended)

### Python Dependencies

```bash
pip install torch>=2.0.0
pip install diffusers>=0.25.0
pip install transformers
pip install accelerate
pip install pillow
pip install opencv-python
pip install ffmpeg-python
```

### For LTX-Video:
```bash
pip install diffusers[torch]
```

### For Frame Interpolation:
```bash
# RIFE (recommended - fastest)
pip install rife-ncnn-vulkan

# FILM (balanced)
pip install film-net

# DAIN (best quality, requires separate installation)
# See: https://github.com/baowenbo/DAIN
```

## Performance Comparison

| Approach | Speed | Quality | VRAM | Best For |
|----------|-------|---------|------|----------|
| LTX-Video | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | 12GB | Short vertical videos |
| SDXL+RIFE | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | 12GB | High-quality content |
| SDXL+FILM | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | 14GB | Large motion scenes |
| SDXL+DAIN | ⭐⭐ | ⭐⭐⭐⭐⭐ | 16GB | Maximum quality |

## Integration with StoryGenerator Pipeline

The video synthesis module integrates with existing pipeline components:

```
Story Idea → Script → Voice → Subtitles → [Video Synthesis] → Final Video
                                          ↓
                                    Keyframes → Interpolation → Assembly
```

### Pipeline Integration Example

```csharp
// 1. Generate keyframes from scene descriptions
var keyframeGen = new KeyframeVideoSynthesizer();
await keyframeGen.GenerateSceneAsync(sceneDesc, outputPath, duration);

// 2. Synchronize with audio
// (Audio path passed to GenerateFromKeyframesAsync)

// 3. Add subtitles overlay
// (Done in post-processing step)

// 4. Apply transitions
// (Configured in SceneComposition)
```

## Troubleshooting

### Common Issues

**1. Python script execution fails**
- Verify Python is in PATH
- Check Python packages are installed
- Ensure correct Python version (3.8+)

**2. CUDA out of memory**
- Reduce inference steps
- Use memory optimization flags
- Lower resolution or duration

**3. FFmpeg not found**
- Install FFmpeg and add to PATH
- Verify with `ffmpeg -version`

**4. Slow generation times**
- Enable GPU acceleration
- Use faster interpolation method (RIFE)
- Reduce keyframes per scene

## Best Practices

1. **Choose the right approach:**
   - Short vertical videos (10-20s) → LTX-Video
   - High-quality content → SDXL + RIFE
   - Character-driven stories → SDXL + FILM

2. **Optimize prompts:**
   - Include camera movement descriptions
   - Add lighting and quality keywords
   - Be specific about composition

3. **Memory management:**
   - Enable attention slicing for large models
   - Clean up temporary files
   - Use batch processing with breaks

4. **Quality vs Speed:**
   - Start with "balanced" preset
   - Adjust based on requirements
   - Profile with comparator tool

## Research References

For detailed research and comparison, see:
- `/research/VIDEO_SYNTHESIS_RESEARCH.md` - Comprehensive research document
- `/config/video_synthesis_config.json` - Configuration options

## Contributing

When adding new synthesis methods:

1. Extend `VideoSynthesisBase` class
2. Implement required generation methods
3. Add to comparator utility
4. Update configuration
5. Add usage examples

## License

This implementation is part of the StoryGenerator project.

## Support

For issues or questions:
- Check research documentation
- Review configuration examples
- Run comparison tool for diagnostics
