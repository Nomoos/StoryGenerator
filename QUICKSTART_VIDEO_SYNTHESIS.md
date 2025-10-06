# Video Synthesis - Quick Start Guide

This guide provides a quick overview of implementing video synthesis in the StoryGenerator pipeline.

## Overview

Two primary approaches are available for synthesizing videos from keyframes and prompts:

1. **Variant A: LTX-Video** - Fast, optimized for short vertical videos (10-20s)
2. **Variant B: SDXL + Frame Interpolation** - High quality, flexible length

## Quick Decision Guide

Choose **LTX-Video** if:
- ✅ Creating TikTok, YouTube Shorts, or Instagram Reels
- ✅ Need fast generation (20-30s per 10s clip)
- ✅ Limited VRAM (~12GB available)
- ✅ Video duration is 5-25 seconds

Choose **SDXL + Interpolation** if:
- ✅ Need highest quality output
- ✅ Require character consistency across frames
- ✅ Video length > 25 seconds
- ✅ Need precise composition control

## C# Implementation - Quick Start

### 1. LTX-Video (Fastest)

```csharp
using StoryGenerator.Generators;

// Initialize synthesizer
var synthesizer = new LTXVideoSynthesizer(
    width: 1080,
    height: 1920,
    fps: 30
);

// Generate video
await synthesizer.GenerateVideoAsync(
    prompt: "A serene lake at sunset, camera panning right, cinematic",
    outputPath: "output/video.mp4",
    duration: 10
);
```

### 2. SDXL + Frame Interpolation (Highest Quality)

```csharp
using StoryGenerator.Generators;

// Configure
var config = new KeyframeVideoConfig
{
    TargetFps = 30,
    Method = InterpolationMethod.RIFE,  // Fast interpolation
    KeyframesPerScene = 3
};

var synthesizer = new KeyframeVideoSynthesizer(config);

// Generate video
await synthesizer.GenerateSceneAsync(
    sceneDescription: "A mystical forest path",
    outputPath: "output/video.mp4",
    duration: 8.0,
    stylePrompts: new List<string> { "cinematic", "photorealistic" }
);
```

### 3. Compare Approaches

```csharp
using StoryGenerator.Tools;

var comparator = new VideoSynthesisComparator();

var results = await comparator.CompareApproachesAsync(
    testPrompt: "Beautiful sunset over ocean",
    duration: 10.0,
    outputDir: "output/comparison"
);
```

## Python Setup

### Required Packages

```bash
# Core dependencies
pip install torch>=2.0.0
pip install diffusers>=0.25.0
pip install transformers accelerate

# For LTX-Video
pip install diffusers[torch]

# For frame interpolation
pip install rife-ncnn-vulkan  # RIFE (recommended)
pip install film-net          # FILM (alternative)

# Utilities
pip install pillow opencv-python ffmpeg-python
```

### Verify Installation

```bash
python -c "import torch; print(f'PyTorch: {torch.__version__}')"
python -c "import diffusers; print(f'Diffusers: {diffusers.__version__}')"
python -c "import torch; print(f'CUDA: {torch.cuda.is_available()}')"
```

## Configuration

Copy the example configuration:

```bash
cp CSharp/video_synthesis_config.example.json config/video_synthesis_config.json
```

Key configuration options:

```json
{
  "video_synthesis": {
    "default_method": "ltx-video",  // or "sdxl+rife"
    "ltx_video": {
      "default_width": 1080,
      "default_height": 1920,
      "default_fps": 30,
      "max_duration": 25
    },
    "quality_presets": {
      "fast": { "method": "ltx-video", "inference_steps": 30 },
      "balanced": { "method": "ltx-video", "inference_steps": 50 },
      "high_quality": { "method": "sdxl+rife" }
    }
  }
}
```

## Motion Presets

Use predefined camera movements:

```csharp
var motionPresets = new Dictionary<string, string>
{
    { "pan_right", "camera slowly panning right" },
    { "zoom_in", "camera slowly zooming in" },
    { "dolly_forward", "camera moving forward" },
    { "static", "static camera, no movement" }
};

await synthesizer.GenerateSceneClipAsync(
    sceneDescription: "City skyline at night",
    motionHint: motionPresets["pan_right"],
    outputPath: "output/scene.mp4",
    duration: 5.0
);
```

## Platform Presets

Optimize for specific platforms:

```csharp
// TikTok / YouTube Shorts / Instagram Reels
var tiktokSynthesizer = new LTXVideoSynthesizer(
    width: 1080,
    height: 1920,
    fps: 30
);

// YouTube (horizontal)
var youtubeSynthesizer = new LTXVideoSynthesizer(
    width: 1920,
    height: 1080,
    fps: 30
);
```

## Performance Tips

### For Faster Generation:
1. Use LTX-Video method
2. Reduce inference steps (30 instead of 50)
3. Lower keyframes per scene (2 instead of 3)
4. Enable memory optimization

### For Best Quality:
1. Use SDXL + RIFE/FILM
2. Increase inference steps (50-60)
3. More keyframes per scene (4-5)
4. Use style prompts effectively

## Troubleshooting

### Common Issues

**1. Python script fails to execute**
```bash
# Check Python path
which python
python --version

# Verify packages
pip list | grep torch
pip list | grep diffusers
```

**2. CUDA out of memory**
```json
// In config, enable optimizations:
"memory_optimization": {
    "enable_attention_slicing": true
}
```

Or reduce parameters:
```csharp
var config = new KeyframeVideoConfig
{
    InferenceSteps = 30,  // Reduce from 50
    KeyframesPerScene = 2  // Reduce from 3
};
```

**3. FFmpeg not found**
```bash
# Install FFmpeg
# Ubuntu/Debian:
sudo apt-get install ffmpeg

# macOS:
brew install ffmpeg

# Verify:
ffmpeg -version
```

**4. Video generation too slow**
- Switch to LTX-Video method
- Reduce video duration
- Lower FPS (24 instead of 30)
- Use GPU acceleration

## Integration with Pipeline

### Complete Story-to-Video Flow

```csharp
// 1. Generate story and script (existing pipeline)
var story = GenerateStory();
var script = GenerateScript(story);

// 2. Generate voice and subtitles (existing)
var audio = GenerateVoice(script);
var subtitles = GenerateSubtitles(audio);

// 3. NEW: Generate video with synthesis
var synthesizer = new LTXVideoSynthesizer();
await synthesizer.GenerateVideoAsync(
    prompt: script.VisualDescription,
    outputPath: "output/video.mp4",
    duration: (int)audio.Duration
);

// 4. Add audio and subtitles (post-processing)
await AddAudioAndSubtitles("output/video.mp4", audio, subtitles);
```

## Next Steps

1. **Read Full Documentation**: See `research/VIDEO_SYNTHESIS_RESEARCH.md` for detailed information
2. **Review Examples**: Check `CSharp/Examples/VideoSynthesisExample.cs` for more examples
3. **Run Comparison**: Use the comparator to test both approaches
4. **Optimize Configuration**: Adjust settings based on your needs

## Performance Benchmarks

| Method | Duration | Generation Time | Quality | VRAM |
|--------|----------|----------------|---------|------|
| LTX-Video | 10s | 20-30s | ⭐⭐⭐⭐ | 12GB |
| SDXL+RIFE | 10s | 45-60s | ⭐⭐⭐⭐⭐ | 12GB |
| SDXL+FILM | 10s | 60-90s | ⭐⭐⭐⭐⭐ | 14GB |
| SDXL+DAIN | 10s | 120-180s | ⭐⭐⭐⭐⭐ | 16GB |

## Resources

- **Research Document**: `research/VIDEO_SYNTHESIS_RESEARCH.md`
- **C# Guide**: `CSharp/README_VIDEO_SYNTHESIS.md`
- **Configuration**: `CSharp/video_synthesis_config.example.json`
- **Examples**: `CSharp/Examples/VideoSynthesisExample.cs`

## References

- LTX-Video: https://huggingface.co/Lightricks/LTX-Video
- Stable Video Diffusion: https://stability.ai/stable-video
- SDXL: https://huggingface.co/docs/diffusers/en/using-diffusers/sdxl
- RIFE: https://github.com/hzwer/RIFE
- FILM: https://github.com/google-research/frame-interpolation

---

**Ready to get started?** Run the comparison tool first to see which approach works best for your use case!
