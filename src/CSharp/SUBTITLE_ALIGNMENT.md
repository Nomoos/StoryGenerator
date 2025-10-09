# Subtitle Alignment and Scene Mapping

This module provides functionality for aligning subtitles to audio using forced alignment (faster-whisper word timestamps) and mapping subtitle time ranges to shot IDs.

## Projects

### StoryGenerator.Research
Contains the WhisperClient implementation for speech recognition and subtitle generation.
- **IWhisperClient.cs** - Interface for Whisper ASR operations
- **WhisperClient.cs** - Implementation using faster-whisper Python subprocess

### StoryGenerator.Core
Core library containing subtitle alignment and scene mapping services.
- **Interfaces/ISubtitleAligner.cs** - Interface for subtitle alignment operations
- **Models/SubtitleToShotMapping.cs** - Data models for subtitle-to-shot mappings
- **Models/Shotlist.cs** - Shotlist and Shot data models
- **Services/SubtitleAligner.cs** - Implementation of subtitle alignment and shot mapping

### StoryGenerator.SubtitleAlignment.Example
Console application demonstrating subtitle alignment and shot mapping.

## Quick Start

1. **Build the projects:**
```bash
cd CSharp
dotnet build StoryGenerator.Research/StoryGenerator.Research.csproj
dotnet build StoryGenerator.Core/StoryGenerator.Core.csproj
dotnet build SubtitleAlignment.Example/StoryGenerator.SubtitleAlignment.Example.csproj
```

2. **Run the example:**
```bash
cd SubtitleAlignment.Example
dotnet run -- path/to/audio.mp3 women 18-23 my_story_001
```

## Features

- **Forced Alignment**: Uses faster-whisper large-v3 for word-level timestamp precision (±50ms)
- **Multiple Formats**: Generates both SRT and VTT subtitle files
- **Shot Mapping**: Maps subtitle time ranges to shot/scene IDs from shotlists
- **Automatic Directory Management**: Creates output directories following the project structure
- **Flexible Configuration**: Supports custom language, words per line, and model settings

## Architecture

### Components

1. **SubtitleToShotMapping.cs** - Data models for subtitle-to-shot mappings
2. **ISubtitleAligner.cs** - Interface defining subtitle alignment operations
3. **SubtitleAligner.cs** - Implementation of subtitle alignment and shot mapping
4. **SubtitleAlignmentExample.cs** - Example/demonstration program

### Dependencies

- `StoryGenerator.Research.WhisperClient` - For speech recognition and word timestamps
- `faster-whisper` Python library - Must be installed (see requirements.txt)
- `.NET 9.0` or higher

## Directory Structure

The module follows the project's folder structure conventions:

```
/subtitles/timed/{segment}/{age}/{title_id}.srt    # Aligned SRT files
/subtitles/timed/{segment}/{age}/{title_id}.vtt    # Aligned VTT files
/scenes/json/{segment}/{age}/{title_id}_subs_to_shots.json  # Shot mappings
```

Where:
- `{segment}` = "women" or "men"
- `{age}` = "10-13", "14-17", "18-23", or "24-30"
- `{title_id}` = unique identifier for the story/video

## Usage

### Basic Subtitle Generation

```csharp
using StoryGenerator.Core.Services;
using StoryGenerator.Research;

// Initialize Whisper client
var whisperClient = new WhisperClient(
    modelSize: "large-v3",
    device: "auto",
    computeType: "float16"
);

// Initialize subtitle aligner
var subtitleAligner = new SubtitleAligner(whisperClient);

// Generate aligned SRT file
var srtPath = await subtitleAligner.GenerateAndSaveSrtAsync(
    audioPath: "audio/tts/women/18-23/story_001.mp3",
    outputPath: "subtitles/timed/women/18-23/story_001.srt",
    language: "en",
    maxWordsPerLine: 10
);

Console.WriteLine($"SRT saved to: {srtPath}");
```

### Generate VTT Subtitles

```csharp
// Generate aligned VTT file
var vttPath = await subtitleAligner.GenerateAndSaveVttAsync(
    audioPath: "audio/tts/women/18-23/story_001.mp3",
    outputPath: "subtitles/timed/women/18-23/story_001.vtt",
    language: "en",
    maxWordsPerLine: 10
);

Console.WriteLine($"VTT saved to: {vttPath}");
```

### Map Subtitles to Shots

```csharp
using StoryGenerator.Core.Interfaces;

// Load or create a shotlist
var shotlist = new Shotlist
{
    StoryTitle = "My Story",
    TotalDuration = 60.0f,
    Shots = new List<Shot>
    {
        new Shot
        {
            ShotNumber = 1,
            StartTime = 0.0f,
            EndTime = 15.0f,
            Duration = 15.0f,
            SceneDescription = "Opening scene"
        },
        new Shot
        {
            ShotNumber = 2,
            StartTime = 15.0f,
            EndTime = 30.0f,
            Duration = 15.0f,
            SceneDescription = "Second scene"
        }
        // ... more shots
    }
};

// Map subtitles to shots and save as JSON
var mappingPath = await subtitleAligner.MapAndSaveSubtitlesToShotsAsync(
    audioPath: "audio/tts/women/18-23/story_001.mp3",
    shotlist: shotlist,
    titleId: "story_001",
    outputPath: "scenes/json/women/18-23/story_001_subs_to_shots.json",
    language: "en",
    maxWordsPerLine: 10
);

Console.WriteLine($"Mapping saved to: {mappingPath}");
```

## Output Format

### SRT Format

Standard SubRip format with word-aligned timestamps:

```srt
1
00:00:00,000 --> 00:00:03,456
Once upon a time in a distant

2
00:00:03,456 --> 00:00:06,789
land there lived a brave hero
```

### VTT Format

WebVTT format with word-aligned timestamps:

```vtt
WEBVTT

00:00:00.000 --> 00:00:03.456
Once upon a time in a distant

00:00:03.456 --> 00:00:06.789
land there lived a brave hero
```

### Subtitle-to-Shot Mapping JSON

```json
{
  "titleId": "story_001",
  "totalDuration": 60.0,
  "subtitleMappings": [
    {
      "subtitleIndex": 1,
      "text": "Once upon a time in a distant",
      "startTime": 0.0,
      "endTime": 3.456,
      "shotNumber": 1,
      "words": [
        {
          "word": "Once",
          "start": 0.0,
          "end": 0.5,
          "confidence": 0.98
        },
        {
          "word": "upon",
          "start": 0.5,
          "end": 0.8,
          "confidence": 0.99
        }
        // ... more words
      ]
    }
    // ... more subtitle entries
  ]
}
```

## Running the Example

```bash
cd CSharp/Examples
dotnet run --project SubtitleAlignmentExample.cs path/to/audio.mp3 women 18-23 my_story_001
```

Arguments:
- `audio_path` (required): Path to audio file
- `segment` (optional): "women" or "men" (default: "women")
- `age_bucket` (optional): Age range (default: "18-23")
- `title_id` (optional): Story identifier (default: "example_title_001")

## Configuration

### Model Selection

Choose the appropriate model based on your needs:

```csharp
// Best quality (recommended for production)
var whisperClient = new WhisperClient(modelSize: "large-v3");

// Faster processing (good for development/testing)
var whisperClient = new WhisperClient(modelSize: "base");

// CPU-optimized
var whisperClient = new WhisperClient(
    modelSize: "base",
    device: "cpu",
    computeType: "int8"
);
```

### Language Settings

```csharp
// Auto-detect language
var srtPath = await subtitleAligner.GenerateAndSaveSrtAsync(
    audioPath: "audio.mp3",
    outputPath: "subtitles.srt",
    language: null  // Auto-detect
);

// Specify language
var srtPath = await subtitleAligner.GenerateAndSaveSrtAsync(
    audioPath: "audio.mp3",
    outputPath: "subtitles.srt",
    language: "en"  // English
);
```

Supported languages: en, es, fr, de, it, pt, ru, ja, ko, zh, and 99+ more

### Words Per Line

Control subtitle line length:

```csharp
// Short lines (faster reading)
maxWordsPerLine: 6

// Medium lines (default)
maxWordsPerLine: 10

// Longer lines
maxWordsPerLine: 15
```

## Shot Mapping Algorithm

The subtitle-to-shot mapping uses a two-stage algorithm:

1. **Midpoint Matching**: Uses the midpoint of each subtitle's time range to find the containing shot
2. **Overlap Fallback**: If no shot contains the midpoint, finds the shot with maximum temporal overlap

This ensures accurate mapping even when subtitles span multiple shots or there are gaps in timing.

## Integration with Pipeline

To integrate this into the video generation pipeline:

```csharp
// After audio generation
var audioPath = await voiceGenerator.GenerateAndSaveAudioAsync(...);

// Generate subtitles
var subtitleAligner = new SubtitleAligner(whisperClient);
var srtPath = await subtitleAligner.GenerateAndSaveSrtAsync(
    audioPath,
    $"subtitles/timed/{segment}/{age}/{titleId}.srt"
);

// After shotlist generation
var shotlist = await shotlistGenerator.GenerateShotlistAsync(...);

// Map subtitles to shots
var mappingPath = await subtitleAligner.MapAndSaveSubtitlesToShotsAsync(
    audioPath,
    shotlist,
    titleId,
    $"scenes/json/{segment}/{age}/{titleId}_subs_to_shots.json"
);
```

## Performance

- **Model**: large-v3 (1550M parameters)
- **Speed**: ~5x real-time on GPU, ~1x real-time on CPU
- **Accuracy**: ±50ms word-level timestamp precision
- **VRAM**: ~10GB for large-v3 on GPU

For faster processing during development, use the `base` model (~16x faster on CPU).

## Troubleshooting

### Python Script Not Found

Ensure `research/python/whisper_subprocess.py` exists or specify the path:

```csharp
var whisperClient = new WhisperClient(
    scriptPath: "/full/path/to/whisper_subprocess.py"
);
```

### faster-whisper Not Installed

```bash
pip install faster-whisper>=0.10.0
```

### CUDA Out of Memory

Use a smaller model or CPU:

```csharp
var whisperClient = new WhisperClient(
    modelSize: "base",  // or "small"
    device: "cpu"
);
```

## Related Documentation

- [ASR_README.md](../../research/csharp/ASR_README.md) - Whisper client documentation
- [FOLDER_STRUCTURE.md](../../FOLDER_STRUCTURE.md) - Project directory structure
- [POST_PRODUCTION.md](../../POST_PRODUCTION.md) - Video post-production features

## Future Enhancements

- [ ] Batch processing of multiple audio files
- [ ] Real-time subtitle generation
- [ ] Custom subtitle styling options
- [ ] Support for multiple language tracks
- [ ] Subtitle editing and correction UI
- [ ] Integration with video composition pipeline

## License

Same as the main StoryGenerator project.
