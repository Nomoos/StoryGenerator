# Video Production from Keyframes, Subtitles, and Script

## Overview

The `VideoProducer` class provides a complete video production pipeline that orchestrates:
- Video generation from keyframes
- Subtitle generation from SRT files or script text
- Audio integration (voiceover and background music)
- Post-production processing (cropping, subtitles, audio mixing)

This is a high-level abstraction that combines `KeyframeVideoSynthesizer` and `VideoPostProducer` into a single, easy-to-use interface.

## Features

✅ **Video from Keyframes**: Generate smooth videos from static keyframe images using frame interpolation  
✅ **Cinematic Camera Motion**: Add professional pan, zoom, and tilt effects for smooth transitions  
✅ **Multiple Subtitle Sources**: Use existing SRT files or auto-generate from script text  
✅ **Audio Integration**: Add voiceover narration and background music with ducking  
✅ **Post-Production**: Automatic cropping, subtitle burn-in, and audio mixing  
✅ **Flexible Configuration**: Extensive configuration options for all aspects of video production

## Quick Start

### Basic Usage

```csharp
using StoryGenerator.Models;
using StoryGenerator.Tools;

// Create producer
var producer = new VideoProducer();

// Configure video production
var config = new VideoProductionConfig
{
    // Input keyframes (minimum 2 required)
    KeyframePaths = new List<string>
    {
        "keyframes/frame_001.png",
        "keyframes/frame_002.png",
        "keyframes/frame_003.png"
    },
    
    // Duration
    DurationSeconds = 30.0,
    
    // Output
    OutputPath = "output/my_video.mp4"
};

// Produce video
var result = await producer.ProduceVideoAsync(config);

if (result.Success)
{
    Console.WriteLine($"Video produced: {result.OutputPath}");
    Console.WriteLine($"Duration: {result.VideoDurationSeconds}s");
    Console.WriteLine($"Size: {result.FileSizeMB:F2} MB");
}
```

### With Subtitles from Script Text

```csharp
var config = new VideoProductionConfig
{
    KeyframePaths = new List<string>
    {
        "keyframes/scene1.png",
        "keyframes/scene2.png"
    },
    
    DurationSeconds = 45.0,
    
    // Auto-generate subtitles from script
    ScriptText = @"
        Welcome to our tutorial. 
        Today we'll learn about video production.
        Let's get started with the basics.
    ",
    GenerateSubtitlesFromScript = true,
    WordsPerMinute = 150,
    
    OutputPath = "output/tutorial.mp4"
};

var result = await producer.ProduceVideoAsync(config);
```

### With Audio and Background Music

```csharp
var config = new VideoProductionConfig
{
    KeyframePaths = new List<string>
    {
        "keyframes/intro.png",
        "keyframes/main.png",
        "keyframes/outro.png"
    },
    
    DurationSeconds = 60.0,
    
    // Subtitles from SRT file
    SrtPath = "subtitles/video.srt",
    BurnInSubtitles = true,
    
    // Audio
    AudioPath = "audio/narration.mp3",
    BackgroundMusicPath = "audio/bgm.mp3",
    MusicVolume = 0.2,
    EnableDucking = true,  // Lower music when voiceover is speaking
    
    OutputPath = "output/complete_video.mp4"
};

var result = await producer.ProduceVideoAsync(config);
```

### With Cinematic Camera Motion

```csharp
var config = new VideoProductionConfig
{
    KeyframePaths = new List<string>
    {
        "keyframes/landscape_001.png",
        "keyframes/landscape_002.png",
        "keyframes/landscape_003.png"
    },
    
    DurationSeconds = 20.0,
    
    // Enable cinematic camera effects
    EnableCameraMotion = true,
    CameraMotion = CameraMotionType.ZoomAndPan,  // Ken Burns effect
    CameraMotionIntensity = 0.4,  // 0.0-1.0, controls effect strength
    
    OutputPath = "output/cinematic_video.mp4"
};

var result = await producer.ProduceVideoAsync(config);
```

### Production-Ready Configuration

```csharp
var config = new VideoProductionConfig
{
    // Input
    KeyframePaths = new List<string>
    {
        "keyframes/frame_001.png",
        "keyframes/frame_002.png",
        "keyframes/frame_003.png",
        "keyframes/frame_004.png",
        "keyframes/frame_005.png"
    },
    
    // Duration
    DurationSeconds = 90.0,
    
    // Output path following recommended format
    // /final/{segment}/{age}/{title_id}_draft.mp4
    Segment = "tech",
    Age = "18-23",
    Gender = "men",
    TitleId = "ai_future_2024",
    OutputPath = "final/tech/18-23/ai_future_2024_draft.mp4",
    
    // Subtitles
    SrtPath = "subtitles/ai_future.srt",
    BurnInSubtitles = true,
    SafeMargins = new SafeTextMargins
    {
        Top = 100,
        Bottom = 150,
        Left = 50,
        Right = 50
    },
    
    // Audio
    AudioPath = "audio/voiceover.mp3",
    BackgroundMusicPath = "audio/bgm/tech_ambient.mp3",
    MusicVolume = 0.2,
    EnableDucking = true,
    
    // Video specs
    Fps = 30,
    TargetWidth = 1080,
    TargetHeight = 1920,  // 9:16 vertical for social media
    VideoBitrate = "8M",
    AudioBitrate = "192k",
    
    // Frame interpolation
    InterpolationMethod = "RIFE"  // Options: RIFE, FILM, DAIN
};

var result = await producer.ProduceVideoAsync(config);
```

## Configuration Options

### VideoProductionConfig

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `KeyframePaths` | `List<string>` | - | Keyframe image paths (minimum 2 required) |
| `DurationSeconds` | `double` | - | Total video duration in seconds |
| `OutputPath` | `string` | - | Output video file path |
| `SrtPath` | `string?` | null | SRT subtitle file (optional) |
| `ScriptText` | `string?` | null | Script text for subtitle generation |
| `AudioPath` | `string?` | null | Voiceover/narration audio file |
| `BackgroundMusicPath` | `string?` | null | Background music file |
| `Fps` | `int` | 30 | Target frames per second |
| `TargetWidth` | `int` | 1080 | Target video width |
| `TargetHeight` | `int` | 1920 | Target video height (9:16 vertical) |
| `BurnInSubtitles` | `bool` | true | Burn in subtitles vs soft subtitles |
| `MusicVolume` | `double` | 0.2 | Background music volume (0.0-1.0) |
| `EnableDucking` | `bool` | true | Lower music during voiceover |
| `VideoBitrate` | `string` | "8M" | Video encoding bitrate |
| `AudioBitrate` | `string` | "192k" | Audio encoding bitrate |
| `InterpolationMethod` | `string` | "RIFE" | Frame interpolation method |
| `GenerateSubtitlesFromScript` | `bool` | true | Auto-generate SRT from script text |
| `WordsPerMinute` | `int` | 150 | Words per minute for subtitle timing |
| `EnableCameraMotion` | `bool` | true | Enable cinematic camera motion effects |
| `CameraMotion` | `CameraMotionType` | Dynamic | Type of camera motion (see below) |
| `CameraMotionIntensity` | `double` | 0.3 | Camera motion intensity (0.0-1.0) |

### CameraMotionType Options

| Type | Description | Use Case |
|------|-------------|----------|
| `None` | No camera motion, static slideshow | Presentations, technical documentation |
| `ZoomIn` | Slow zoom in effect on each keyframe | Portraits, focus on details |
| `ZoomOut` | Slow zoom out effect revealing context | Establishing shots, big reveals |
| `PanRight` | Pan left to right with subtle zoom | Landscape scenes, horizontal movement |
| `PanLeft` | Pan right to left with subtle zoom | Landscape scenes, horizontal movement |
| `ZoomAndPan` | Ken Burns effect combining zoom and pan | Professional documentaries, photo slideshows |
| `Dynamic` | Varies effects between keyframes (default) | Story-driven content, visual variety |

### VideoProductionResult

| Property | Type | Description |
|----------|------|-------------|
| `Success` | `bool` | Whether production succeeded |
| `OutputPath` | `string?` | Path to produced video |
| `VideoDurationSeconds` | `double` | Output video duration |
| `FileSizeBytes` | `long` | Output file size in bytes |
| `FileSizeMB` | `double` | Output file size in megabytes |
| `ProcessingTimeSeconds` | `double` | Total processing time |
| `GeneratedSrtPath` | `string?` | Path to generated SRT file (if created) |
| `ErrorMessage` | `string?` | Error message if failed |
| `ProcessingNotes` | `List<string>` | Additional processing notes |

## Pipeline Overview

The VideoProducer orchestrates the following pipeline:

```
┌─────────────────────────────────────────────────────────────┐
│ 1. Subtitle Generation (if needed)                          │
│    • Generate SRT from script text using word timing        │
│    • Split text into sentences with timestamps              │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ 2. Video Generation from Keyframes                          │
│    • Apply cinematic camera motion to each keyframe         │
│    • Interpolate frames between keyframes (optional)        │
│    • Assemble video with FFmpeg                             │
│    • Sync with audio if provided                            │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ 3. Post-Production                                           │
│    • Crop to target aspect ratio (9:16)                     │
│    • Burn in subtitles with safe margins                    │
│    • Mix background music with ducking                      │
│    • Final encode with target bitrates                      │
└─────────────────────────────────────────────────────────────┘
                            ↓
                      Final Video
```

## Cinematic Camera Motion

The VideoProducer supports professional camera motion effects to create smooth, engaging videos from static keyframes. This feature transforms simple slideshows into dynamic, cinematic content.

### How It Works

Camera motion is applied using FFmpeg's `zoompan` filter, which creates smooth zoom and pan effects on static images. Each keyframe is processed with motion effects before being concatenated into the final video.

### Camera Motion Types

**1. Dynamic (Default)**
- Automatically alternates between different effects for visual variety
- Best for story-driven content with multiple scenes
- Creates a professional, varied viewing experience

**2. ZoomIn**
- Gradual zoom in from 100% to max zoom level
- Creates focus and draws attention to details
- Perfect for portraits and close-up shots

**3. ZoomOut**
- Starts zoomed in and gradually reveals the full scene
- Great for establishing shots and big reveals
- Creates a sense of discovery

**4. PanRight / PanLeft**
- Smooth horizontal pan across the image
- Includes subtle zoom for added depth
- Ideal for landscape and wide shots

**5. ZoomAndPan (Ken Burns Effect)**
- Combines diagonal pan with zoom in
- Classic documentary and photo slideshow style
- Most cinematic and professional looking

**6. None**
- Disables camera motion for static presentation
- Use for technical documentation or when motion is distracting

### Intensity Control

The `CameraMotionIntensity` parameter (0.0-1.0) controls the strength of effects:

- **0.1-0.2**: Subtle motion, barely noticeable
- **0.3-0.4**: Moderate motion (recommended for most content)
- **0.5-0.7**: Strong motion, very noticeable
- **0.8-1.0**: Extreme motion, use sparingly

### Examples

**Cinematic Documentary:**
```csharp
EnableCameraMotion = true,
CameraMotion = CameraMotionType.ZoomAndPan,
CameraMotionIntensity = 0.4
```

**Dynamic Storytelling:**
```csharp
EnableCameraMotion = true,
CameraMotion = CameraMotionType.Dynamic,
CameraMotionIntensity = 0.3
```

**Static Presentation:**
```csharp
EnableCameraMotion = false
```

## Use Cases

### 1. Story-Driven Content

```csharp
var config = new VideoProductionConfig
{
    KeyframePaths = new List<string>
    {
        "story/beginning.png",
        "story/middle.png",
        "story/end.png"
    },
    DurationSeconds = 90.0,
    ScriptText = "Once upon a time...",
    AudioPath = "narration.mp3",
    BackgroundMusicPath = "piano.mp3",
    MusicVolume = 0.15,
    OutputPath = "stories/fairytale.mp4"
};
```

### 2. Educational Content

```csharp
var config = new VideoProductionConfig
{
    KeyframePaths = new List<string>
    {
        "lesson/concept1.png",
        "lesson/concept2.png",
        "lesson/summary.png"
    },
    DurationSeconds = 120.0,
    SrtPath = "subtitles/lesson.srt",
    AudioPath = "teacher_voiceover.mp3",
    BurnInSubtitles = true,
    OutputPath = "education/chapter1.mp4"
};
```

### 3. Social Media Content

```csharp
var config = new VideoProductionConfig
{
    KeyframePaths = new List<string>
    {
        "social/hook.png",
        "social/content.png",
        "social/cta.png"
    },
    DurationSeconds = 15.0,  // Short-form
    ScriptText = "Quick tip: Did you know...",
    WordsPerMinute = 180,  // Faster pacing
    BackgroundMusicPath = "upbeat.mp3",
    MusicVolume = 0.3,
    OutputPath = "social/tip001.mp4"
};
```

## Requirements

- **FFmpeg**: Required for video processing
- **FFprobe**: Required for video analysis
- .NET 9.0 or later

### Optional Dependencies

- **KeyframeVideoSynthesizer**: For advanced frame interpolation (RIFE, FILM, DAIN)
  - If not provided, falls back to FFmpeg-based slideshow
- **Python**: Required for advanced interpolation methods
- **CUDA**: Optional for GPU-accelerated processing

## Error Handling

The VideoProducer validates all inputs and provides detailed error messages:

```csharp
var result = await producer.ProduceVideoAsync(config);

if (!result.Success)
{
    Console.WriteLine($"Production failed: {result.ErrorMessage}");
    
    foreach (var note in result.ProcessingNotes)
    {
        Console.WriteLine($"Note: {note}");
    }
}
```

### Common Errors

- **Missing keyframes**: At least 2 keyframes required
- **Invalid duration**: Duration must be > 0
- **Missing output path**: OutputPath is required
- **File not found**: Keyframe, audio, or subtitle files don't exist

## Performance Considerations

- **Keyframe count**: More keyframes = longer processing time but smoother video
- **Duration**: Longer videos take proportionally longer to process
- **Resolution**: Higher resolutions (4K) significantly increase processing time
- **Interpolation method**: RIFE (fast) → FILM (balanced) → DAIN (slow but best quality)
- **GPU acceleration**: Use CUDA-enabled interpolation for faster processing

## Tips

1. **Keyframe Distribution**: Distribute keyframes evenly across the video timeline for best results
2. **Subtitle Timing**: For generated subtitles, adjust `WordsPerMinute` based on content complexity
3. **Music Ducking**: Enable ducking for better voiceover clarity
4. **Safe Margins**: Use larger margins for mobile playback to avoid text cutoff
5. **Bitrate**: Use 8M for high quality, 4M for web, 2M for mobile-optimized

## Examples

See `Examples/VideoProductionExample.cs` for complete working examples demonstrating:
- Complete video production with all features
- Video production with script-to-subtitle generation
- Minimal configuration for simple use cases
- Configuration examples for different demographics

## Related Components

- **KeyframeVideoSynthesizer**: Generates video from keyframes with interpolation
- **VideoPostProducer**: Handles post-production (cropping, subtitles, audio)
- **KeyframeGenerationService**: Generates keyframes from scene descriptions

## License

MIT License - See LICENSE file for details
