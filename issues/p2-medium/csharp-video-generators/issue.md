# C# Video Pipeline: Keyframe & Video Generation

**ID:** `csharp-video-generators`  
**Priority:** P2 (Medium)  
**Effort:** 30-40 hours  
**Status:** Not Started  
**Phase:** 5 - Video Pipeline (New)

## Overview

Implement the video generation pipeline in C#, including keyframe generation (SDXL), video synthesis (LTX-Video or Stable Video Diffusion), and post-production. This completes the visual component of the StoryGenerator pipeline.

## Dependencies

**Requires:**
- Phase 1: Core Infrastructure (✅ Complete)
- Phase 2: API Providers (✅ Complete)
- Phase 3: Generators (🔄 Must be complete)
- Phase 4: Pipeline Orchestration (📋 Must be complete)

**Blocks:**
- Complete feature parity with Python
- Full production deployment

## Acceptance Criteria

### Keyframe Generation
- [ ] SDXL integration for high-quality image generation
- [ ] Scene-based prompt generation from scripts
- [ ] Style consistency across frames
- [ ] Quality validation and regeneration
- [ ] Support for 1080×1920 vertical format

### Video Synthesis
- [ ] LTX-Video or Stable Video Diffusion integration
- [ ] Frame interpolation between keyframes
- [ ] Smooth transitions
- [ ] Audio synchronization
- [ ] Performance optimization

### Scene Planning
- [ ] Beat sheet generation from scripts
- [ ] Scene description generation
- [ ] Visual guidance integration (LLaVA-OneVision or Phi-3.5-vision)
- [ ] Scene timing and pacing

### Post-Production
- [ ] Subtitle overlay with dynamic styling
- [ ] Audio-visual synchronization
- [ ] Final rendering and format optimization
- [ ] Quality control checks

### Testing
- [ ] Unit tests for each component
- [ ] Integration tests for video pipeline
- [ ] Visual quality validation
- [ ] Performance benchmarks

### Documentation
- [ ] Video pipeline guide
- [ ] Model integration documentation
- [ ] Configuration examples
- [ ] Troubleshooting guide

## Task Details

### 1. Scene Planning Generator (6-8 hours)

```csharp
public interface ISceneGenerator
{
    Task<List<Scene>> GenerateScenesAsync(
        string script,
        SceneGenerationOptions options,
        CancellationToken cancellationToken = default);
}

public class Scene
{
    public int SceneNumber { get; set; }
    public string Description { get; set; }
    public TimeSpan StartTime { get; set; }
    public TimeSpan Duration { get; set; }
    public string VisualPrompt { get; set; }
    public List<string> DialogueSegments { get; set; }
}
```

**Implementation:**
- Parse script into beats/scenes
- Generate visual descriptions using LLM
- Time scene breaks based on audio
- Create SDXL prompts for each scene

### 2. Keyframe Generator (10-12 hours)

```csharp
public interface IKeyframeGenerator
{
    Task<KeyframeResult> GenerateKeyframeAsync(
        string prompt,
        KeyframeOptions options,
        CancellationToken cancellationToken = default);
        
    Task<List<KeyframeResult>> GenerateKeyframesAsync(
        List<Scene> scenes,
        KeyframeOptions options,
        IProgress<KeyframeProgress> progress = null,
        CancellationToken cancellationToken = default);
}

public class KeyframeOptions
{
    public int Width { get; set; } = 1080;
    public int Height { get; set; } = 1920;
    public string Style { get; set; } = "cinematic";
    public int Steps { get; set; } = 50;
    public float GuidanceScale { get; set; } = 7.5f;
}
```

**SDXL Integration:**
- Use Stable Diffusion XL for 1024×1024 base
- Upscale to 1080×1920 for vertical video
- Apply consistent style/theme across frames
- Quality validation (reject blurry/malformed)

### 3. Video Synthesizer (10-12 hours)

```csharp
public interface IVideoSynthesizer
{
    Task<VideoResult> SynthesizeVideoAsync(
        List<KeyframeResult> keyframes,
        AudioFile audio,
        VideoSynthesisOptions options,
        IProgress<VideoProgress> progress = null,
        CancellationToken cancellationToken = default);
}

public class VideoSynthesisOptions
{
    public int Fps { get; set; } = 24;
    public string OutputFormat { get; set; } = "mp4";
    public int Bitrate { get; set; } = 5000; // kbps
    public bool EnableInterpolation { get; set; } = true;
    public int InterpolationFrames { get; set; } = 8;
}
```

**LTX-Video Integration:**
- Generate intermediate frames between keyframes
- Smooth transitions using interpolation
- Sync with audio timeline
- Handle variable scene lengths

**Alternative: Stable Video Diffusion:**
- Image-to-video conversion per keyframe
- Motion control for dynamic scenes
- Frame blending for transitions

### 4. Post-Production Compositor (6-8 hours)

```csharp
public interface IVideoCompositor
{
    Task<VideoResult> ComposeVideoAsync(
        VideoFile baseVideo,
        AudioFile audio,
        SubtitleFile subtitles,
        CompositionOptions options,
        CancellationToken cancellationToken = default);
}

public class CompositionOptions
{
    public SubtitleStyle SubtitleStyle { get; set; }
    public bool EnableBackgroundMusic { get; set; }
    public float MusicVolume { get; set; } = 0.2f;
    public string OutputFormat { get; set; } = "mp4";
    public VideoQuality Quality { get; set; }
}
```

**Features:**
- Subtitle overlay with animations
- Background music mixing
- Color grading/correction
- Final encoding optimization

### 5. Vision Guidance (Optional, 4-6 hours)

```csharp
public interface IVisionGuidance
{
    Task<SceneValidation> ValidateSceneAsync(
        byte[] imageData,
        string expectedDescription,
        CancellationToken cancellationToken = default);
}
```

**LLaVA-OneVision or Phi-3.5-vision:**
- Validate generated frames match scene intent
- Suggest improvements for off-target frames
- Ensure visual consistency

## Model Integration

### SDXL (Stable Diffusion XL)
```bash
# C# Integration options:
# 1. Python interop via PythonScriptBridge
# 2. ONNX Runtime with optimized SDXL model
# 3. External API (Stability AI, Replicate)
```

### LTX-Video
```bash
# Integration:
# 1. Python interop (recommended initially)
# 2. Direct model inference (if ONNX available)
# 3. External API
```

### Vision Models (Optional)
```bash
# LLaVA-OneVision or Phi-3.5-vision
# Use for scene validation and guidance
```

## Testing Strategy

### Unit Tests
```csharp
[Fact]
public async Task KeyframeGenerator_GeneratesValidImage()
{
    var generator = CreateKeyframeGenerator();
    var result = await generator.GenerateKeyframeAsync(
        "a cinematic scene of...", options);
    
    Assert.NotNull(result.ImageData);
    Assert.Equal(1080, result.Width);
    Assert.Equal(1920, result.Height);
}
```

### Integration Tests
```csharp
[Fact]
public async Task CompleteVideoPipeline_GeneratesVideo()
{
    // Test: Script → Scenes → Keyframes → Video → Post-Production
}
```

### Visual Quality Tests
- Manual review of generated keyframes
- Visual consistency across scenes
- Audio-visual synchronization validation
- Subtitle positioning and timing

## Performance Considerations

- **GPU Requirements**: CUDA-capable GPU recommended (8GB+ VRAM)
- **Batch Processing**: Generate multiple keyframes in parallel
- **Caching**: Cache generated frames for regeneration
- **Memory Management**: Stream large video files
- **Optimization**: Use FP16 for faster inference

## Output Files

**Code:**
- `src/CSharp/StoryGenerator.Video/SceneGenerator.cs`
- `src/CSharp/StoryGenerator.Video/KeyframeGenerator.cs`
- `src/CSharp/StoryGenerator.Video/VideoSynthesizer.cs`
- `src/CSharp/StoryGenerator.Video/VideoCompositor.cs`
- `src/CSharp/StoryGenerator.Video.Tests/*.cs`

**Configuration:**
- `src/CSharp/appsettings.Video.json`
- Model download scripts
- GPU configuration guide

**Documentation:**
- `src/CSharp/VIDEO_PIPELINE_GUIDE.md` (new)
- `src/CSharp/MODEL_INTEGRATION_GUIDE.md` (new)

## Related Files

- `src/Python/Generators/GKeyframeGenerator.py` - Reference (OBSOLETE)
- `src/Python/Generators/GVideo.py` - Reference (OBSOLETE)
- `src/Python/Generators/GVideoCompositor.py` - Reference (OBSOLETE)
- `docs/VIDEO_SYNTHESIS_SUMMARY.md` - Video synthesis documentation

## Validation

```bash
# Build solution
cd src/CSharp
dotnet build StoryGenerator.sln

# Run video tests (may require GPU)
dotnet test --filter "Category=Video"

# Generate test video
dotnet run --project StoryGenerator.CLI -- \
  video generate \
  --script ./test-script.txt \
  --audio ./test-audio.mp3 \
  --output ./test-video.mp4
```

## Hardware Requirements

**Minimum:**
- 16GB RAM
- NVIDIA GPU with 8GB VRAM
- 50GB free disk space (for models)

**Recommended:**
- 32GB RAM
- NVIDIA GPU with 12GB+ VRAM
- 100GB free disk space
- SSD for faster I/O

## Notes

- Video generation is computationally expensive
- Consider cloud GPU options (Azure, AWS, GCP)
- May need Python interop initially for ML models
- Plan for incremental implementation (keyframes first, then video)
- Test with short videos before full-length content

## Success Metrics

- Generate keyframes in <2 minutes per frame
- Video synthesis in <5 minutes per 30-second video
- Visual quality comparable to Python implementation
- Smooth transitions and audio sync
- Production-ready video output

## Next Steps

After completion:
1. Performance optimization and GPU tuning
2. Batch processing for multiple videos
3. Cloud deployment guide
4. Cost analysis and optimization
5. User acceptance testing with real content
