# Research: C# FFmpeg Client

**ID:** `01-research-08-csharp-ffmpeg`  
**Priority:** P1  
**Effort:** 4-6 hours  
**Status:** ✅ Complete

## Overview

C# client implementation for FFmpeg media processing operations. This research prototype validates approaches for audio normalization, video cropping, format conversion, and media analysis from C#. The implementation provides essential media manipulation capabilities for the content pipeline, particularly audio loudness normalization to broadcast standards and 9:16 aspect ratio video processing.

## Dependencies

**Requires:**
- `00-setup-04`: C# project structure
- FFmpeg and FFprobe installed (available in PATH)

**Blocks:**
- Phase 3 audio production (normalization)
- Video post-production (aspect ratio, effects)
- Export/delivery (format conversion, encoding)

## Acceptance Criteria

- [x] C# can execute FFmpeg commands via subprocess
- [x] Audio normalization to target LUFS (loudness)
- [x] Two-pass loudnorm for accurate results
- [x] Video cropping and aspect ratio conversion
- [x] Media information extraction via FFprobe
- [x] Async/await with cancellation support
- [x] Error handling and progress tracking
- [x] Documentation and usage examples provided

## Task Details

### Implementation

The `FFmpegClient` class in `StoryGenerator.Research` provides comprehensive FFmpeg operations:

```csharp
public class FFmpegClient : IFFmpegClient
{
    private readonly string _ffmpegPath;
    private readonly string _ffprobePath;

    public FFmpegClient(string ffmpegPath = "ffmpeg", string ffprobePath = "ffprobe")
    {
        // Auto-detects FFmpeg in PATH or uses custom paths
    }

    // Audio normalization to broadcast loudness standards
    public async Task<NormalizationResult> NormalizeAudioAsync(
        string inputPath,
        string outputPath,
        double targetLufs = -14.0,      // Typical: -14 for streaming, -16 for broadcast
        double targetLra = 7.0,         // Loudness range
        double targetTp = -1.0,         // True peak (prevent clipping)
        bool twoPass = true,            // Two-pass for accuracy
        int sampleRate = 48000,
        CancellationToken cancellationToken = default)
    {
        // Uses loudnorm filter with two-pass analysis
    }

    // Convert video to 9:16 portrait aspect ratio (for shorts/reels)
    public async Task<CropResult> CropTo9x16Async(
        string inputPath,
        string outputPath,
        CropPosition position = CropPosition.Center,
        int targetWidth = 1080,
        int targetHeight = 1920,
        string videoCodec = "libx264",
        string preset = "medium",
        int crf = 23,
        CancellationToken cancellationToken = default)
    {
        // Smart cropping with configurable position
    }

    // Extract media information (duration, codecs, bitrate, etc.)
    public async Task<MediaInfo> GetMediaInfoAsync(
        string filePath,
        CancellationToken cancellationToken = default)
    {
        // Uses ffprobe to get detailed media metadata
    }
}
```

**Key Features:**

**Audio Normalization:**
- **Two-Pass Loudnorm**: Analyzes audio first, then normalizes accurately
- **LUFS Targeting**: -14 LUFS for streaming platforms (YouTube, Spotify)
- **True Peak Control**: Prevents clipping and distortion
- **Loudness Range**: Controls dynamic range (LRA)
- **Sample Rate Conversion**: Resamples to target rate (48kHz standard)

**Video Cropping:**
- **9:16 Aspect Ratio**: For YouTube Shorts, TikTok, Instagram Reels
- **Crop Positions**: Center, Top, Bottom, Left, Right, Custom
- **Codec Options**: H.264, H.265/HEVC for compression
- **Quality Control**: CRF (Constant Rate Factor) for size/quality balance
- **Preset Selection**: ultrafast → veryslow for speed/compression tradeoff

**Media Information:**
- **Duration**: Total length in seconds
- **Video Streams**: Resolution, frame rate, codec, bitrate
- **Audio Streams**: Sample rate, channels, codec, bitrate
- **Format**: Container format and metadata

**Result Models:**
```csharp
public class NormalizationResult
{
    public bool Success { get; set; }
    public string OutputPath { get; set; }
    public double InputLufs { get; set; }      // Measured input loudness
    public double OutputLufs { get; set; }     // Achieved output loudness
    public double InputTruePeak { get; set; }
    public double OutputTruePeak { get; set; }
    public string ErrorMessage { get; set; }
}

public class CropResult
{
    public bool Success { get; set; }
    public string OutputPath { get; set; }
    public int SourceWidth { get; set; }
    public int SourceHeight { get; set; }
    public int CroppedWidth { get; set; }
    public int CroppedHeight { get; set; }
    public string ErrorMessage { get; set; }
}

public class MediaInfo
{
    public double Duration { get; set; }
    public List<VideoStream> VideoStreams { get; set; }
    public List<AudioStream> AudioStreams { get; set; }
    public string FormatName { get; set; }
    public long Size { get; set; }
    public int BitRate { get; set; }
}
```

**Process Management:**
- Spawns FFmpeg/FFprobe subprocesses
- Redirects stdin/stdout/stderr for control and monitoring
- Parses progress output for status updates
- Handles errors from stderr
- Proper cleanup and cancellation support

### Testing

```bash
# Verify FFmpeg installation
ffmpeg -version
ffprobe -version

# Build research project
cd src/CSharp
dotnet build StoryGenerator.Research/StoryGenerator.Research.csproj

# Create test audio file
ffmpeg -f lavfi -i "sine=frequency=1000:duration=5" -ar 44100 test_input.wav

# Test normalization
dotnet run --project StoryGenerator.Research

# Manual FFmpeg test
ffmpeg -i test_input.wav -af loudnorm=I=-14:LRA=7:TP=-1 test_output.wav
```

**Example Usage:**

**Audio Normalization:**
```csharp
var client = new FFmpegClient();

// Normalize to streaming standard (-14 LUFS)
var result = await client.NormalizeAudioAsync(
    inputPath: "voiceover.wav",
    outputPath: "voiceover_normalized.wav",
    targetLufs: -14.0,
    targetLra: 7.0,
    targetTp: -1.0,
    twoPass: true,
    sampleRate: 48000
);

Console.WriteLine($"Input LUFS: {result.InputLufs:F2}");
Console.WriteLine($"Output LUFS: {result.OutputLufs:F2}");
```

**Video Cropping to 9:16:**
```csharp
var client = new FFmpegClient();

// Crop 16:9 video to 9:16 portrait
var result = await client.CropTo9x16Async(
    inputPath: "landscape_video.mp4",
    outputPath: "portrait_video.mp4",
    position: CropPosition.Center,
    targetWidth: 1080,
    targetHeight: 1920,
    videoCodec: "libx264",
    preset: "medium",
    crf: 23
);

Console.WriteLine($"Cropped from {result.SourceWidth}x{result.SourceHeight} " +
                  $"to {result.CroppedWidth}x{result.CroppedHeight}");
```

**Media Information:**
```csharp
var client = new FFmpegClient();

var info = await client.GetMediaInfoAsync("video.mp4");

Console.WriteLine($"Duration: {info.Duration:F2} seconds");
Console.WriteLine($"Video: {info.VideoStreams[0].Width}x{info.VideoStreams[0].Height} " +
                  $"@ {info.VideoStreams[0].FrameRate} fps");
Console.WriteLine($"Audio: {info.AudioStreams[0].SampleRate} Hz, " +
                  $"{info.AudioStreams[0].Channels} channels");
```

## Output Files

- `/src/CSharp/StoryGenerator.Research/FFmpegClient.cs` - Main implementation (800+ lines)
- `/src/CSharp/StoryGenerator.Research/IFFmpegClient.cs` - Interface definition
- `/src/CSharp/StoryGenerator.Research/Models.cs` - Result and info models

## Related Files

- `/config/pipeline.yaml` - Audio/video settings (LUFS -14, sample rate 48kHz, 1080x1920)
- FFmpeg documentation: https://ffmpeg.org/documentation.html
- loudnorm filter: https://ffmpeg.org/ffmpeg-filters.html#loudnorm

## Validation

```bash
# Verify implementation
ls -la src/CSharp/StoryGenerator.Research/FFmpegClient.cs

# Check project builds
cd src/CSharp && dotnet build StoryGenerator.Research/StoryGenerator.Research.csproj

# Verify FFmpeg installation
which ffmpeg && which ffprobe
ffmpeg -version | head -1

# Test basic operation
ffmpeg -f lavfi -i sine -t 1 -ar 48000 test.wav
ffprobe -v error -show_format -show_streams test.wav
```

## Notes

**Integration Approach:**
- Uses FFmpeg CLI via subprocess (standard approach for C#)
- Alternative: Could use FFmpeg libraries via P/Invoke (more complex)
- Cross-platform compatible (Windows, Linux, macOS)

**Audio Normalization Details:**
- **Two-Pass vs Single-Pass**: Two-pass analyzes first for accuracy
- **LUFS Standards**: 
  - YouTube/Spotify: -14 LUFS
  - Apple Music: -16 LUFS
  - Broadcast (EBU R128): -23 LUFS
- **True Peak**: Prevents inter-sample peaks that cause clipping
- **LRA (Loudness Range)**: 7 LU typical for dialog, higher for music

**Video Cropping Strategy:**
- **Source 16:9 → Target 9:16**: Crops horizontally
- **Crop Position**: 
  - Center: Default, works for most content
  - Top: Keep upper portion (faces, titles)
  - Bottom: Keep lower portion (captions, actions)
- **Quality Settings**:
  - CRF 18-23: High quality (larger files)
  - CRF 24-28: Medium quality (smaller files)
  - Preset: faster = larger files, slower = smaller files

**Performance Considerations:**
- Audio normalization: ~2-5x real-time (two-pass)
- Video cropping: Depends on codec/preset
  - ultrafast: ~10x real-time
  - medium: ~2-5x real-time
  - veryslow: ~0.5-1x real-time
- GPU encoding (NVENC, QuickSync) much faster if available

**Known Limitations:**
- Requires FFmpeg installed and in PATH
- No built-in retry logic for transient failures
- Progress parsing is best-effort (FFmpeg output varies)
- Large files may need streaming/chunking approach

**Best Practices:**
- Always use two-pass normalization for final audio
- Test crop position with sample frames first
- Use CRF for variable bitrate (better quality)
- Consider GPU encoding for faster processing
- Monitor stderr for detailed error messages

## Next Steps

After completion:
- Phase 3 audio production can normalize voiceovers
- Video post-production can crop to 9:16
- Export tasks can convert formats and codecs
- Consider adding more operations (concat, overlay, filters)
