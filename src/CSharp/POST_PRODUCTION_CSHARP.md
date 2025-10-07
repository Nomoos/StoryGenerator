# Video Post-Production C# Implementation

## Overview

This C# implementation provides comprehensive video post-production capabilities for the StoryGenerator project. It automates the process of converting raw video segments into polished, social-media-ready content.

## Features

### Core Capabilities

1. **Video Cropping to 9:16 Aspect Ratio**
   - Automatically crops and scales videos to 1080×1920 (vertical format)
   - Maintains aspect ratio and centers content
   - Configurable frame rate (default: 30 fps)
   - Optimized for Instagram Reels, TikTok, and YouTube Shorts

2. **Subtitle Integration**
   - Supports SRT subtitle format
   - Burn-in subtitles (hardcoded) or soft subtitles (separate stream)
   - Configurable safe text margins
   - Automatic positioning for vertical videos
   - Styled with readable fonts, outline, and shadow

3. **Background Music & Audio Mixing**
   - Mixes licensed background music with voiceover
   - Audio ducking: automatically reduces music volume during speech
   - Configurable music volume levels
   - Automatic looping for shorter music tracks
   - Maintains audio quality at 192k bitrate

4. **Video Concatenation with Transitions**
   - Concatenates multiple video segments seamlessly
   - Support for fade transitions between clips
   - Configurable transition duration
   - Fallback to simple concatenation for reliability

5. **Final Encoding with Specifications**
   - H.264 codec (libx264) for maximum compatibility
   - 8 Mbps video bitrate for high quality
   - 30 fps frame rate
   - AAC audio codec
   - Fast-start flag for web streaming

## Architecture

### Core Components

```
StoryGenerator.Interfaces/
  └── IVideoPostProducer.cs          # Post-production interface

StoryGenerator.Models/
  └── VideoPostProductionConfig.cs    # Configuration models
      - VideoPostProductionConfig
      - SafeTextMargins
      - VideoPostProductionResult

StoryGenerator.Tools/
  └── VideoPostProducer.cs            # Main implementation

StoryGenerator.Examples/
  └── VideoPostProductionExample.cs   # Usage examples
```

## Usage

### Complete Post-Production Pipeline

```csharp
using StoryGenerator.Models;
using StoryGenerator.Tools;

// Create post-producer
var producer = new VideoPostProducer();

// Configure pipeline
var config = new VideoPostProductionConfig
{
    // Input segments
    SegmentPaths = new List<string>
    {
        "videos/segment_1.mp4",
        "videos/segment_2.mp4",
        "videos/segment_3.mp4"
    },

    // Output path: /final/{segment}/{age}/{title_id}_draft.mp4
    Segment = "tech",
    Age = "18-23",
    Gender = "men",
    TitleId = "ai_revolution_2024",
    OutputPath = "final/tech/18-23/ai_revolution_2024_draft.mp4",

    // Subtitles
    SrtPath = "subtitles/ai_revolution_2024.srt",
    BurnInSubtitles = true,
    SafeMargins = new SafeTextMargins
    {
        Top = 100,
        Bottom = 150,
        Left = 50,
        Right = 50
    },

    // Audio
    BackgroundMusicPath = "audio/bgm/tech_ambient.mp3",
    MusicVolume = 0.2,
    EnableDucking = true,

    // Video specs
    Fps = 30,
    TargetWidth = 1080,
    TargetHeight = 1920,
    VideoBitrate = "8M",
    AudioBitrate = "192k",

    // Transitions
    TransitionType = "fade",
    TransitionDuration = 0.5
};

// Execute post-production
var outputPath = await producer.ProduceVideoAsync(config);
Console.WriteLine($"Video produced: {outputPath}");
```

### Individual Operations

#### 1. Crop Video to Vertical Format

```csharp
var producer = new VideoPostProducer();

await producer.CropToVerticalAsync(
    inputPath: "videos/horizontal_video.mp4",
    outputPath: "videos/vertical_video.mp4",
    fps: 30
);
```

#### 2. Add Subtitles

```csharp
var producer = new VideoPostProducer();

await producer.AddSubtitlesAsync(
    inputPath: "videos/video.mp4",
    outputPath: "videos/video_with_subs.mp4",
    srtPath: "subtitles/video.srt",
    burnIn: true,
    safeMargins: new SafeTextMargins
    {
        Top = 100,
        Bottom = 150,
        Left = 50,
        Right = 50
    }
);
```

#### 3. Add Background Music with Ducking

```csharp
var producer = new VideoPostProducer();

await producer.AddBackgroundMusicAsync(
    inputPath: "videos/video.mp4",
    outputPath: "videos/video_with_music.mp4",
    musicPath: "audio/bgm/background.mp3",
    musicVolume: 0.2,
    duckingEnabled: true
);
```

#### 4. Concatenate Videos

```csharp
var producer = new VideoPostProducer();

await producer.ConcatenateVideosAsync(
    segmentPaths: new List<string>
    {
        "videos/intro.mp4",
        "videos/main.mp4",
        "videos/outro.mp4"
    },
    outputPath: "videos/final.mp4",
    transitionType: "fade",
    transitionDuration: 0.5
);
```

## Configuration Options

### VideoPostProductionConfig

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `SegmentPaths` | `List<string>` | - | Input video segments to process |
| `OutputPath` | `string` | - | Final output video path |
| `SrtPath` | `string` | null | SRT subtitle file (optional) |
| `BackgroundMusicPath` | `string` | null | Background music file (optional) |
| `SoundEffectsPaths` | `List<string>` | null | Sound effects files (optional) |
| `Fps` | `int` | 30 | Target frame rate |
| `TargetWidth` | `int` | 1080 | Target width for 9:16 |
| `TargetHeight` | `int` | 1920 | Target height for 9:16 |
| `BurnInSubtitles` | `bool` | true | Burn in vs soft subtitles |
| `SafeMargins` | `SafeTextMargins` | default | Text positioning margins |
| `MusicVolume` | `double` | 0.2 | Background music volume (0.0-1.0) |
| `EnableDucking` | `bool` | true | Audio ducking during voiceover |
| `TransitionType` | `string` | "fade" | Transition type (fade, xfade, none) |
| `TransitionDuration` | `double` | 0.5 | Transition duration in seconds |
| `VideoBitrate` | `string` | "8M" | Video bitrate for encoding |
| `AudioBitrate` | `string` | "192k" | Audio bitrate for encoding |

### SafeTextMargins

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `Top` | `int` | 100 | Top margin in pixels |
| `Bottom` | `int` | 150 | Bottom margin in pixels |
| `Left` | `int` | 50 | Left margin in pixels |
| `Right` | `int` | 50 | Right margin in pixels |

## Output Path Format

Videos are saved following this structure:

```
/final/{segment}/{age}/{title_id}_draft.mp4
```

**Examples:**
- `/final/tech/18-23/ai_revolution_2024_draft.mp4`
- `/final/lifestyle/10-13/morning_routine_tips_draft.mp4`
- `/final/gaming/24-30/top_strategies_draft.mp4`

**Parameters:**
- `{segment}`: Content category (e.g., "tech", "lifestyle", "gaming")
- `{age}`: Target age group (e.g., "10-13", "14-17", "18-23", "24-30")
- `{title_id}`: Unique video identifier

## Technical Specifications

### Video Output Specifications

- **Resolution**: 1080×1920 (9:16 vertical)
- **Codec**: H.264 (libx264)
- **Bitrate**: 8 Mbps (configurable)
- **Frame Rate**: 30 fps (configurable)
- **Pixel Format**: yuv420p
- **Preset**: Medium

### Audio Output Specifications

- **Codec**: AAC
- **Bitrate**: 192k (configurable)
- **Sample Rate**: 48 kHz
- **Channels**: Stereo

### Subtitle Styling

- **Font**: Default system font
- **Font Size**: 24px (scaled for 1080×1920)
- **Color**: White with black outline
- **Position**: Bottom-centered with safe margins
- **Background**: Optional shadow for readability

## Dependencies

### Required Software

- **FFmpeg**: Must be installed and available in PATH
  - Windows: Download from [ffmpeg.org](https://ffmpeg.org)
  - Linux: `apt-get install ffmpeg`
  - macOS: `brew install ffmpeg`

### NuGet Packages

No additional NuGet packages required beyond .NET 8.0 standard libraries.

## Error Handling

The implementation includes comprehensive error handling:

- File existence validation
- FFmpeg execution error detection
- Automatic cleanup of temporary files
- Detailed error messages with context

### Common Issues

1. **FFmpeg not found**
   - Solution: Install FFmpeg and add to system PATH
   - Or specify path: `new VideoPostProducer(ffmpegPath: "/path/to/ffmpeg")`

2. **Invalid video dimensions**
   - Solution: Use `CropToVerticalAsync()` to ensure correct aspect ratio

3. **Subtitle sync issues**
   - Solution: Verify SRT timestamps match video duration

4. **Audio ducking not working**
   - Solution: Check FFmpeg version supports sidechaincompress filter

## Performance Considerations

- **CPU-Intensive**: Video encoding is CPU-intensive
- **Processing Time**: Expect 2-5x real-time for encoding
- **Memory Usage**: Moderate; primarily FFmpeg process
- **Temp Files**: Automatically cleaned up after processing
- **Parallel Processing**: Can process multiple videos concurrently

### Optimization Tips

1. Use appropriate `preset` values (faster = quicker, lower quality)
2. Adjust `crf` value for quality vs file size trade-off
3. Process videos in batches for efficiency
4. Consider using hardware acceleration if available

## Examples

See `Examples/VideoPostProductionExample.cs` for:
- Complete pipeline demonstration
- Individual operation examples
- Configuration examples for different demographics
- Error handling patterns

Run the example:

```bash
cd CSharp/Examples
dotnet run VideoPostProductionExample.cs
```

## Testing

### Manual Testing

1. Prepare test videos in various formats
2. Create SRT subtitle file
3. Prepare licensed background music
4. Run the example with test files
5. Verify output meets specifications

### Validation Checklist

- [ ] Video dimensions are 1080×1920
- [ ] Frame rate is 30 fps
- [ ] Subtitles are visible and positioned correctly
- [ ] Background music is audible but not overpowering
- [ ] Audio ducking works during voiceover
- [ ] Transitions are smooth between segments
- [ ] Output file size is reasonable
- [ ] Video plays correctly in target platforms

## Integration

### Pipeline Integration

```csharp
// In your video generation pipeline
var postProducer = new VideoPostProducer();

// After generating video segments
var config = new VideoPostProductionConfig
{
    SegmentPaths = generatedSegments,
    OutputPath = DetermineOutputPath(story),
    SrtPath = GetSubtitlesPath(story),
    BackgroundMusicPath = SelectBackgroundMusic(story),
    // ... other config
};

var finalVideo = await postProducer.ProduceVideoAsync(config);
```

### Dependency Injection

```csharp
// In Startup.cs or Program.cs
services.AddSingleton<IVideoPostProducer, VideoPostProducer>();

// In your service
public class VideoGenerationService
{
    private readonly IVideoPostProducer _postProducer;
    
    public VideoGenerationService(IVideoPostProducer postProducer)
    {
        _postProducer = postProducer;
    }
    
    public async Task<string> GenerateVideo(VideoConfig config)
    {
        // Generate segments...
        
        // Post-production
        var finalVideo = await _postProducer.ProduceVideoAsync(postConfig);
        return finalVideo;
    }
}
```

## Future Enhancements

Potential improvements for future versions:

- [ ] GPU acceleration support (NVENC, QSV)
- [ ] More transition types (wipe, slide, zoom)
- [ ] Animated subtitle effects
- [ ] Multiple subtitle style presets
- [ ] Intro/outro template system
- [ ] Watermark positioning and overlay
- [ ] Multi-format export (multiple resolutions)
- [ ] Progress reporting and cancellation
- [ ] Batch processing queue
- [ ] Cloud rendering integration

## License & Attribution

Ensure all background music and sound effects are properly licensed before use. This implementation assumes you have rights to use all audio files.

## Support

For issues or questions:
1. Check FFmpeg is properly installed (`ffmpeg -version`)
2. Verify input file formats are supported
3. Review error messages for specific issues
4. Consult FFmpeg documentation for filter details

## Related Files

- `CSharp/Interfaces/IVideoPostProducer.cs` - Interface definition
- `CSharp/Models/VideoPostProductionConfig.cs` - Configuration models
- `CSharp/Tools/VideoPostProducer.cs` - Main implementation
- `CSharp/Examples/VideoPostProductionExample.cs` - Usage examples
- `POST_PRODUCTION.md` - Python implementation reference
- `research/csharp/FFmpegClient.cs` - Audio processing utilities
