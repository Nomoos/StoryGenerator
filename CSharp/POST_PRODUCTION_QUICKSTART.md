# Video Post-Production Quick Start Guide

## Prerequisites

1. **FFmpeg Installation** (Required)
   ```bash
   # Ubuntu/Debian
   sudo apt-get install ffmpeg
   
   # macOS
   brew install ffmpeg
   
   # Windows
   # Download from https://ffmpeg.org/download.html
   # Add to PATH
   ```

2. **Verify FFmpeg**
   ```bash
   ffmpeg -version
   ffprobe -version
   ```

## Quick Start

### 1. Basic Usage

```csharp
using StoryGenerator.Models;
using StoryGenerator.Tools;

// Initialize
var producer = new VideoPostProducer();

// Configure
var config = new VideoPostProductionConfig
{
    SegmentPaths = new List<string>
    {
        "videos/segment1.mp4",
        "videos/segment2.mp4"
    },
    OutputPath = "final/tech/18-23/my_video_draft.mp4",
    SrtPath = "subtitles/my_video.srt",
    BackgroundMusicPath = "audio/bgm/music.mp3",
    
    // Optional settings (these are defaults)
    Fps = 30,
    TargetWidth = 1080,
    TargetHeight = 1920,
    BurnInSubtitles = true,
    MusicVolume = 0.2,
    EnableDucking = true,
    TransitionType = "fade",
    TransitionDuration = 0.5
};

// Execute
string outputPath = await producer.ProduceVideoAsync(config);
Console.WriteLine($"Video created: {outputPath}");
```

### 2. Individual Operations

#### Crop to Vertical (9:16)
```csharp
await producer.CropToVerticalAsync(
    "input.mp4",
    "output_vertical.mp4",
    fps: 30
);
```

#### Add Subtitles
```csharp
await producer.AddSubtitlesAsync(
    "input.mp4",
    "output_with_subs.mp4",
    "subtitles.srt",
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

#### Add Background Music
```csharp
await producer.AddBackgroundMusicAsync(
    "input.mp4",
    "output_with_music.mp4",
    "music.mp3",
    musicVolume: 0.2,
    duckingEnabled: true
);
```

#### Concatenate Videos
```csharp
await producer.ConcatenateVideosAsync(
    new List<string> { "intro.mp4", "main.mp4", "outro.mp4" },
    "final.mp4",
    transitionType: "fade",
    transitionDuration: 0.5
);
```

## Output Path Format

Videos must be saved following this structure:

```
/final/{segment}/{age}/{title_id}_draft.mp4
```

**Examples:**
```
final/tech/18-23/ai_revolution_2024_draft.mp4
final/lifestyle/10-13/morning_routine_draft.mp4
final/gaming/24-30/top_strategies_draft.mp4
```

**Path Components:**
- `segment`: Content category (tech, lifestyle, gaming, wellness, etc.)
- `age`: Target age group (10-13, 14-17, 18-23, 24-30)
- `title_id`: Unique identifier for the video

## Configuration Options

### Required Settings
- `SegmentPaths`: List of input video files
- `OutputPath`: Final output file path

### Optional Settings
- `SrtPath`: Subtitle file (optional)
- `BackgroundMusicPath`: Background music (optional)
- `Fps`: Frame rate (default: 30)
- `TargetWidth/Height`: Resolution (default: 1080×1920)
- `BurnInSubtitles`: True for burned-in, false for soft (default: true)
- `MusicVolume`: 0.0-1.0 (default: 0.2)
- `EnableDucking`: Reduce music during speech (default: true)
- `TransitionType`: "fade", "xfade", or "none" (default: "fade")
- `TransitionDuration`: Seconds (default: 0.5)

### Safe Text Margins
Prevents subtitles from being cut off:
```csharp
SafeMargins = new SafeTextMargins
{
    Top = 100,      // pixels from top
    Bottom = 150,   // pixels from bottom
    Left = 50,      // pixels from left
    Right = 50      // pixels from right
}
```

## Video Specifications

**Output Format:**
- Resolution: 1080×1920 (9:16 vertical)
- Frame Rate: 30 fps
- Video Codec: H.264 (libx264)
- Video Bitrate: 8 Mbps
- Audio Codec: AAC
- Audio Bitrate: 192k
- Pixel Format: yuv420p

## Common Use Cases

### 1. Social Media Short (Teen Audience)
```csharp
var config = new VideoPostProductionConfig
{
    SegmentPaths = segments,
    OutputPath = "final/lifestyle/10-13/morning_tips_draft.mp4",
    SrtPath = "subs.srt",
    BackgroundMusicPath = "upbeat_music.mp3",
    MusicVolume = 0.25,  // Higher for energetic content
    TransitionType = "fade"
};
```

### 2. Educational Content (Young Adults)
```csharp
var config = new VideoPostProductionConfig
{
    SegmentPaths = segments,
    OutputPath = "final/tech/18-23/ai_explained_draft.mp4",
    SrtPath = "subs.srt",
    BackgroundMusicPath = "ambient_tech.mp3",
    MusicVolume = 0.15,  // Lower for voiceover clarity
    EnableDucking = true,
    TransitionType = "fade"
};
```

### 3. No Music, Subtitles Only
```csharp
var config = new VideoPostProductionConfig
{
    SegmentPaths = segments,
    OutputPath = "final/wellness/24-30/meditation_draft.mp4",
    SrtPath = "subs.srt",
    BackgroundMusicPath = null,  // No music
    TransitionType = "fade"
};
```

## Troubleshooting

### Issue: FFmpeg not found
**Solution:**
```csharp
var producer = new VideoPostProducer(
    ffmpegPath: "/usr/local/bin/ffmpeg",
    ffprobePath: "/usr/local/bin/ffprobe"
);
```

### Issue: Video dimensions incorrect
**Solution:** Use `CropToVerticalAsync()` first:
```csharp
await producer.CropToVerticalAsync(input, cropped, fps: 30);
```

### Issue: Subtitles not visible
**Solution:** Increase bottom margin:
```csharp
SafeMargins = new SafeTextMargins { Bottom = 200 }
```

### Issue: Music too loud
**Solution:** Reduce volume:
```csharp
MusicVolume = 0.1  // 10% instead of 20%
```

### Issue: Processing too slow
**Solution:** 
- Use simpler transitions: `TransitionType = "none"`
- Process fewer segments at once
- Consider hardware acceleration (future enhancement)

## Performance

**Typical Processing Times:**
- 10-second video: ~30-60 seconds
- 30-second video: ~1-3 minutes
- 60-second video: ~3-5 minutes

**Factors affecting speed:**
- Input video quality
- Transition complexity
- Number of segments
- CPU performance

## Best Practices

1. **Organize Input Files**
   ```
   videos/
     segment_1.mp4
     segment_2.mp4
   subtitles/
     video.srt
   audio/
     bgm/
       music.mp3
   ```

2. **Use Licensed Audio**
   - Only use properly licensed music
   - Keep track of licenses for background music
   - Credit sources as required

3. **Test Subtitle Positioning**
   - Preview on different devices
   - Adjust safe margins if needed
   - Test with longest subtitle text

4. **Maintain Aspect Ratios**
   - Always crop to 9:16 before processing
   - Use `CropToVerticalAsync()` if needed

5. **Error Handling**
   ```csharp
   try
   {
       var output = await producer.ProduceVideoAsync(config);
       Console.WriteLine($"Success: {output}");
   }
   catch (FileNotFoundException ex)
   {
       Console.WriteLine($"File not found: {ex.Message}");
   }
   catch (Exception ex)
   {
       Console.WriteLine($"Error: {ex.Message}");
   }
   ```

## Integration Example

```csharp
public class VideoGenerationPipeline
{
    private readonly VideoPostProducer _postProducer;
    
    public VideoGenerationPipeline()
    {
        _postProducer = new VideoPostProducer();
    }
    
    public async Task<string> GenerateFinalVideo(
        List<string> segments,
        string titleId,
        string ageGroup,
        string category)
    {
        var config = new VideoPostProductionConfig
        {
            SegmentPaths = segments,
            OutputPath = $"final/{category}/{ageGroup}/{titleId}_draft.mp4",
            SrtPath = $"subtitles/{titleId}.srt",
            BackgroundMusicPath = SelectMusic(category),
            
            Segment = category,
            Age = ageGroup,
            TitleId = titleId,
            
            Fps = 30,
            BurnInSubtitles = true,
            MusicVolume = 0.2,
            EnableDucking = true
        };
        
        return await _postProducer.ProduceVideoAsync(config);
    }
    
    private string SelectMusic(string category)
    {
        return category switch
        {
            "tech" => "audio/bgm/tech_ambient.mp3",
            "lifestyle" => "audio/bgm/upbeat.mp3",
            "gaming" => "audio/bgm/energetic.mp3",
            _ => "audio/bgm/default.mp3"
        };
    }
}
```

## Next Steps

1. Review the [full documentation](POST_PRODUCTION_CSHARP.md)
2. Check the [example code](Examples/VideoPostProductionExample.cs)
3. Prepare your input videos and audio files
4. Test with sample content
5. Integrate into your pipeline

## Support

For issues:
1. Verify FFmpeg is installed and in PATH
2. Check input file formats
3. Review error messages
4. Consult the full documentation

## Related Files

- `POST_PRODUCTION_CSHARP.md` - Complete documentation
- `Examples/VideoPostProductionExample.cs` - Detailed examples
- `Interfaces/IVideoPostProducer.cs` - Interface definition
- `Models/VideoPostProductionConfig.cs` - Configuration models
- `Tools/VideoPostProducer.cs` - Implementation
