# Video Pipeline Quick Start

## Overview

The StoryGenerator now includes a complete video generation pipeline that can automatically create short-form vertical videos (1080x1920) from story scripts. This guide will help you get started.

## Prerequisites

### Required Software
- ✅ .NET 8.0 SDK
- ✅ FFmpeg (must be in PATH)
- ✅ Python 3.8+ with:
  - PyTorch (with CUDA support recommended)
  - Diffusers library (`pip install diffusers`)
  - Pillow (`pip install Pillow`)

### Hardware Recommendations
- **GPU**: NVIDIA GPU with 12GB+ VRAM (for LTX) or 16GB+ (for keyframe method)
- **CPU**: Multi-core processor (for FFmpeg encoding)
- **RAM**: 16GB+ system RAM
- **Storage**: 10GB+ free space per video project

## Quick Start

### 1. Configure the Pipeline

Edit `config/pipeline_config.yaml`:

```yaml
generation:
  video:
    synthesis_method: "ltx"  # or "keyframe" for higher quality
    resolution:
      width: 1080
      height: 1920
    fps: 30
```

### 2. Run the Pipeline

```bash
cd src/CSharp/StoryGenerator.Pipeline
dotnet run
```

The pipeline will execute all steps:
1. Generate story idea
2. Create script
3. Revise script
4. Enhance script with voice tags
5. Generate voiceover (ElevenLabs)
6. Generate word-level subtitles (WhisperX)
7. **Analyze scenes** ← Video pipeline starts here
8. **Generate visual descriptions**
9. **Generate keyframes** (integrated into video gen)
10. **Generate video clips**
11. **Compose final video**

### 3. Find Your Video

Output location: `Stories/final/{story_title}/{story_title}.mp4`

## Synthesis Methods

### LTX-Video (Fast, Default)
- **Speed**: 2-5 minutes per scene
- **Quality**: Good, smooth motion
- **VRAM**: ~12GB
- **Best for**: Quick iteration, testing, consistent style

```yaml
synthesis_method: "ltx"
```

### Keyframe Interpolation (High Quality)
- **Speed**: 5-10 minutes per scene
- **Quality**: Excellent, high detail
- **VRAM**: ~16GB
- **Best for**: Final production, maximum quality

```yaml
synthesis_method: "keyframe"
```

## Output Structure

```
Stories/
├── 0_Ideas/
│   └── {story_title}.json          # Story metadata
├── 1_Scripts/
│   └── {story_title}.txt           # Generated script
├── 2_Revised/
│   └── {story_title}.txt           # Revised script
├── 3_VoiceOver/
│   └── {story_title}.mp3           # ElevenLabs audio
├── 4_Titles/
│   └── {story_title}.srt           # Word-level subtitles
├── scenes/
│   └── {story_title}_scenes.json   # Scene breakdown
├── videos/
│   └── {story_title}/
│       ├── clip_000.mp4            # Individual clips
│       ├── clip_001.mp4
│       └── ...
└── final/
    └── {story_title}/
        └── {story_title}.mp4       # ✨ Final video!
```

## Configuration Options

### Video Settings

```yaml
generation:
  video:
    synthesis_method: "ltx"  # "ltx" or "keyframe"
    resolution:
      width: 1080
      height: 1920
    fps: 30
    codec: "libx264"
    audio_codec: "aac"
    bitrate: "8M"
    quality: "high"
```

### Pipeline Steps (Enable/Disable)

```yaml
pipeline:
  steps:
    story_idea: true
    script_generation: true
    script_revision: true
    script_enhancement: true
    voice_synthesis: true
    asr_subtitles: true
    scene_analysis: true      # Video pipeline
    scene_description: true   # Video pipeline
    keyframe_generation: true # Video pipeline
    video_interpolation: true # Video pipeline
    video_composition: true   # Video pipeline
```

## Troubleshooting

### "FFmpeg not found"
- Install FFmpeg: https://ffmpeg.org/download.html
- Ensure it's in your PATH: `ffmpeg -version`

### "CUDA out of memory"
- Reduce video resolution in config
- Use LTX method instead of keyframe
- Close other GPU-intensive applications
- Generate fewer scenes at once

### "Python module not found"
```bash
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
pip install diffusers transformers accelerate
pip install Pillow
```

### "No video clips found"
- Check `Stories/videos/{story_title}/` for individual clips
- Review pipeline logs for errors during video generation
- Ensure Python dependencies are installed
- Verify GPU is accessible: `python -c "import torch; print(torch.cuda.is_available())"`

## Advanced Usage

### Run Specific Steps Only

Disable unwanted steps in config:

```yaml
pipeline:
  steps:
    story_idea: false          # Use existing story
    script_generation: false   # Use existing script
    # ... keep only video steps enabled
    scene_analysis: true
    scene_description: true
    video_interpolation: true
    video_composition: true
```

### Custom Scene Duration

Edit `SceneAnalysisService.cs`:

```csharp
private List<Shot> SegmentIntoScenes(...)
{
    var targetSceneDuration = 15.0f; // Change from 10.0f
    // ...
}
```

### Test Without Video Generation

For faster testing, skip video steps:

```yaml
pipeline:
  steps:
    # ... enable steps 1-6
    scene_analysis: true
    scene_description: true
    keyframe_generation: false  # Skip
    video_interpolation: false  # Skip
    video_composition: false    # Skip
```

## Performance Tips

1. **Use LTX for Development**: Much faster iteration time
2. **Switch to Keyframe for Final**: Better quality for production
3. **Batch Process**: Generate multiple stories overnight
4. **Monitor VRAM**: Use `nvidia-smi` to check GPU usage
5. **Cleanup Intermediates**: Delete `videos/` folder after composition

## API Reference

See `docs/VIDEO_PIPELINE_IMPLEMENTATION.md` for detailed API documentation.

## Examples

### Generate Single Video

```bash
cd src/CSharp/StoryGenerator.Pipeline
dotnet run
```

### Generate Multiple Videos

Run the pipeline multiple times, or modify `Program.cs` to loop.

### Custom Integration

```csharp
// In your code
var config = PipelineConfig.Load("config/pipeline_config.yaml");
var orchestrator = new PipelineOrchestrator(config, ...);
var outputPath = await orchestrator.RunFullPipelineAsync();
Console.WriteLine($"Video created: {outputPath}");
```

## Support

For issues or questions:
- Check `docs/VIDEO_PIPELINE_IMPLEMENTATION.md`
- Review test examples in `src/CSharp/StoryGenerator.Tests/Pipeline/`
- Open an issue on GitHub

## What's Next?

Optional enhancements you can implement:
- Vision guidance for quality validation
- Character consistency (IP-Adapter)
- ControlNet for pose/composition control
- Background music integration
- Intro/outro templates
- Batch processing optimization

Happy video creating! 🎬
