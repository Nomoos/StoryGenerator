# Subtitle Alignment Implementation

This directory contains the C# implementation for aligning subtitles to audio and mapping them to scene shots.

## Structure

```
CSharp/
├── StoryGenerator.Research/         # Whisper client for speech recognition
│   ├── IWhisperClient.cs
│   └── WhisperClient.cs
├── StoryGenerator.Core/             # Core subtitle alignment library
│   ├── Interfaces/
│   │   └── ISubtitleAligner.cs
│   ├── Models/
│   │   ├── SubtitleToShotMapping.cs
│   │   └── Shotlist.cs
│   └── Services/
│       └── SubtitleAligner.cs
├── SubtitleAlignment.Example/       # Example console application
│   └── Program.cs
└── SUBTITLE_ALIGNMENT.md            # Detailed documentation
```

## Prerequisites

- **.NET 8.0 SDK** or higher
- **Python 3.8+** with faster-whisper installed
- **CUDA-capable GPU** (optional, but recommended for faster processing)

### Install Python Dependencies

```bash
pip install faster-whisper>=0.10.0
```

## Building

Build all projects:

```bash
cd CSharp
dotnet build StoryGenerator.Research/StoryGenerator.Research.csproj
dotnet build StoryGenerator.Core/StoryGenerator.Core.csproj
dotnet build SubtitleAlignment.Example/StoryGenerator.SubtitleAlignment.Example.csproj
```

## Usage

### Command Line Example

```bash
cd CSharp/SubtitleAlignment.Example
dotnet run -- <audio_path> [segment] [age_bucket] [title_id]
```

**Example:**
```bash
dotnet run -- ../../audio/tts/women/18-23/story_001.mp3 women 18-23 story_001
```

**Parameters:**
- `audio_path` (required): Path to audio file
- `segment` (optional): "women" or "men" (default: "women")
- `age_bucket` (optional): "10-13", "14-17", "18-23", or "24-30" (default: "18-23")
- `title_id` (optional): Story identifier (default: "example_title_001")

### Programmatic Usage

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

// Generate SRT file
var srtPath = await subtitleAligner.GenerateAndSaveSrtAsync(
    audioPath: "audio.mp3",
    outputPath: "subtitles/timed/women/18-23/story_001.srt",
    language: "en"
);

// Map subtitles to shots
var mappingPath = await subtitleAligner.MapAndSaveSubtitlesToShotsAsync(
    audioPath: "audio.mp3",
    shotlist: shotlist,
    titleId: "story_001",
    outputPath: "scenes/json/women/18-23/story_001_subs_to_shots.json"
);
```

## Output Files

The implementation follows the project's folder structure:

### Subtitle Files
- **SRT**: `/subtitles/timed/{segment}/{age}/{title_id}.srt`
- **VTT**: `/subtitles/timed/{segment}/{age}/{title_id}.vtt`

### Shot Mapping JSON
- **Location**: `/scenes/json/{segment}/{age}/{title_id}_subs_to_shots.json`
- **Format**:
```json
{
  "titleId": "story_001",
  "totalDuration": 60.0,
  "subtitleMappings": [
    {
      "subtitleIndex": 1,
      "text": "Once upon a time",
      "startTime": 0.0,
      "endTime": 2.5,
      "shotNumber": 1,
      "words": [
        {
          "word": "Once",
          "start": 0.0,
          "end": 0.5,
          "confidence": 0.98
        }
      ]
    }
  ]
}
```

## Key Features

1. **Forced Alignment**: Uses faster-whisper for word-level timestamp precision (±50ms)
2. **Multiple Formats**: Generates both SRT and VTT subtitle files
3. **Shot Mapping**: Maps subtitle time ranges to shot/scene IDs
4. **Automatic Directory Management**: Creates output directories as needed
5. **Flexible Configuration**: Supports custom language, words per line, and model settings

## Model Configuration

### Quality vs Speed

```csharp
// Best quality (production)
var whisperClient = new WhisperClient(modelSize: "large-v3");

// Faster processing (development)
var whisperClient = new WhisperClient(modelSize: "base");

// CPU-optimized
var whisperClient = new WhisperClient(
    modelSize: "base",
    device: "cpu",
    computeType: "int8"
);
```

## Performance

| Model | Speed (GPU) | Speed (CPU) | VRAM | Accuracy |
|-------|------------|-------------|------|----------|
| tiny | ~100x | ~32x | ~1GB | Good |
| base | ~50x | ~16x | ~1GB | Better |
| small | ~25x | ~6x | ~2GB | Good |
| medium | ~10x | ~2x | ~5GB | Very Good |
| large-v3 | ~5x | ~1x | ~10GB | Best |

*Speed relative to real-time (1x = real-time, 5x = 5 times faster than real-time)*

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
    modelSize: "base",
    device: "cpu"
);
```

## Documentation

- [SUBTITLE_ALIGNMENT.md](SUBTITLE_ALIGNMENT.md) - Detailed API documentation
- [research/csharp/ASR_README.md](../../research/csharp/ASR_README.md) - Whisper client documentation
- [FOLDER_STRUCTURE.md](../../FOLDER_STRUCTURE.md) - Project directory structure

## Integration

This module integrates with the StoryGenerator pipeline:

1. After audio generation (TTS)
2. Generate subtitles with forced alignment
3. After shotlist generation
4. Map subtitles to shots for video composition

## Future Enhancements

- [ ] Batch processing of multiple audio files
- [ ] Real-time subtitle generation
- [ ] Custom subtitle styling options
- [ ] Support for multiple language tracks
- [ ] Integration with video composition pipeline

## License

Same as the main StoryGenerator project.
