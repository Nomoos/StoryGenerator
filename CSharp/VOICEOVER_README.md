# Voiceover Generation and Normalization

This implementation provides local Text-to-Speech (TTS) generation and audio normalization for voiceover content, organized by audience segments (gender/age).

## Features

- **Local TTS Generation**: Uses Piper TTS for fast, offline voice synthesis
- **Voice Gender Selection**: Automatically selects male or female voice per segment based on content and audience
- **Audio Normalization**: Applies FFmpeg loudnorm filter to -14 LUFS for consistent loudness
- **Segment Organization**: Organizes audio files by gender and age segments
- **Loudness Metadata**: Saves normalization parameters as JSON for reference

## Architecture

### Components

1. **ITTSClient**: Interface for TTS operations
2. **PiperTTSClient**: Implementation using Piper TTS
3. **IFFmpegClient**: Interface for FFmpeg operations
4. **FFmpegClient**: Implementation for audio normalization
5. **IVoiceRecommender**: Interface for voice gender selection
6. **SimpleVoiceRecommender**: Content-aware voice recommendation
7. **VoiceoverGenerator**: Main orchestrator for TTS + normalization workflow

### Directory Structure

Audio files are organized as follows:

```
audio/
├── tts/
│   ├── men/
│   │   ├── 10-13/
│   │   │   └── {title_id}.wav
│   │   ├── 14-17/
│   │   ├── 18-23/
│   │   └── 24-30/
│   └── women/
│       ├── 10-13/
│       ├── 14-17/
│       ├── 18-23/
│       └── 24-30/
└── normalized/
    ├── men/
    │   └── 18-23/
    │       ├── {title_id}_lufs.wav
    │       └── {title_id}_lufs.json
    └── women/
        └── 18-23/
            ├── {title_id}_lufs.wav
            └── {title_id}_lufs.json
```

## Setup

### Prerequisites

1. **Piper TTS** (for local TTS generation)
   ```bash
   # Install Piper TTS
   # See: https://github.com/rhasspy/piper
   
   # Download voice models
   wget https://huggingface.co/rhasspy/piper-voices/resolve/main/en/en_US/lessac/medium/en_US-lessac-medium.onnx
   wget https://huggingface.co/rhasspy/piper-voices/resolve/main/en/en_US/amy/medium/en_US-amy-medium.onnx
   ```

2. **FFmpeg** (for audio normalization)
   ```bash
   # Ubuntu/Debian
   sudo apt-get install ffmpeg
   
   # macOS
   brew install ffmpeg
   
   # Windows
   choco install ffmpeg
   ```

## Usage

### Basic Example

```csharp
using StoryGenerator.Models;
using StoryGenerator.Tools;

// Initialize components
var ttsClient = new PiperTTSClient(
    piperExecutable: "piper",
    maleModelPath: "en_US-lessac-medium.onnx",
    femaleModelPath: "en_US-amy-medium.onnx"
);

var ffmpegClient = new FFmpegClient();
var voiceRecommender = new SimpleVoiceRecommender();

var voiceoverGenerator = new VoiceoverGenerator(
    ttsClient,
    ffmpegClient,
    voiceRecommender,
    audioRoot: "audio"
);

// Generate voiceover for a segment
var segment = new AudienceSegment("men", "18-23");

var result = await voiceoverGenerator.GenerateVoiceoverAsync(
    titleId: "story_001",
    title: "The Future of Technology",
    text: "Welcome to this amazing story...",
    segment: segment
);

Console.WriteLine($"TTS: {result.TTSPath}");
Console.WriteLine($"Normalized: {result.NormalizedPath}");
Console.WriteLine($"LUFS JSON: {result.LufsJsonPath}");
```

### Running the Example

```bash
cd CSharp/Examples
dotnet run --project VoiceoverGenerationExample.cs
```

## API Reference

### VoiceoverGenerator

#### GenerateVoiceoverAsync

Generates and normalizes voiceover for a title and audience segment.

**Parameters:**
- `titleId` (string): Unique identifier for the title
- `title` (string): The title text for content analysis
- `text` (string): Text to convert to speech
- `segment` (AudienceSegment): Audience segment (gender/age)
- `cancellationToken` (CancellationToken): Optional cancellation token

**Returns:** `VoiceoverResult` containing paths to generated files

**Output Files:**
1. TTS audio: `/audio/tts/{gender}/{age}/{titleId}.wav` (48 kHz)
2. Normalized audio: `/audio/normalized/{gender}/{age}/{titleId}_lufs.wav` (48 kHz, -14 LUFS)
3. LUFS parameters: `/audio/normalized/{gender}/{age}/{titleId}_lufs.json`

### PiperTTSClient

#### GenerateVoiceoverAsync

Generates voiceover audio using Piper TTS.

**Parameters:**
- `text` (string): Text to convert to speech
- `outputPath` (string): Output path for WAV file
- `voiceGender` (VoiceGender): Male or Female
- `sampleRate` (int): Sample rate in Hz (default: 48000)
- `cancellationToken` (CancellationToken): Optional cancellation token

### FFmpegClient

#### NormalizeAudioAsync

Normalizes audio to target LUFS using FFmpeg loudnorm filter.

**Parameters:**
- `inputPath` (string): Input audio file path
- `outputPath` (string): Output audio file path
- `targetLufs` (double): Target integrated loudness in LUFS (default: -14.0)
- `targetLra` (double): Target loudness range in LU (default: 7.0)
- `targetTp` (double): Target true peak in dBTP (default: -1.0)
- `twoPass` (bool): Use two-pass normalization (default: true)
- `sampleRate` (int): Output sample rate in Hz (default: 48000)
- `cancellationToken` (CancellationToken): Optional cancellation token

**Returns:** `NormalizationResult` with success status and measurements

## Voice Recommendation Logic

The `SimpleVoiceRecommender` uses content-aware logic:

- **Tech/Gaming/Sports** → Male voice
- **Beauty/Fashion/Lifestyle** → Female voice
- **Mystery/Horror/Crime** → Male voice
- **Educational content** → Matches audience gender
- **General content** → Matches audience gender (default: Female)

## LUFS JSON Format

The loudnorm parameters are saved as JSON:

```json
{
  "titleId": "story_001",
  "segment": "men/18-23",
  "voiceGender": "Male",
  "targetLufs": -14.0,
  "targetLra": 7.0,
  "targetTp": -1.0,
  "measurements": {
    "input_i": "-23.5",
    "input_lra": "11.2",
    "input_tp": "-3.8",
    "input_thresh": "-34.1",
    "target_offset": "0.5"
  }
}
```

## Testing

The implementation includes example code in:
- `CSharp/Examples/VoiceoverGenerationExample.cs`

Run tests:
```bash
cd CSharp/Examples
dotnet run
```

## Alternative TTS Engines

While this implementation uses Piper TTS, the `ITTSClient` interface allows easy integration with other TTS engines:

- **System.Speech.Synthesis** (Windows-only)
- **Azure Cognitive Services**
- **Google Cloud Text-to-Speech**
- **Coqui TTS**

Simply implement the `ITTSClient` interface for your preferred TTS engine.

## Performance Notes

- **Piper TTS**: Fast, local inference (< 1 second for short texts)
- **FFmpeg Normalization**: Two-pass for accuracy (2-5 seconds per file)
- **Parallel Processing**: Generate multiple segments concurrently for faster pipeline

## Troubleshooting

### Piper TTS not found
```
Error: Piper TTS is not available
Solution: Install Piper and ensure it's in your PATH
```

### FFmpeg not found
```
Error: ffmpeg error: No such file or directory
Solution: Install FFmpeg and ensure it's in your PATH
```

### Voice models not found
```
Error: Model file not found: en_US-lessac-medium.onnx
Solution: Download Piper voice models from Hugging Face
```

## References

- [Piper TTS](https://github.com/rhasspy/piper) - Fast, local neural TTS
- [FFmpeg loudnorm](https://ffmpeg.org/ffmpeg-filters.html#loudnorm) - Audio normalization filter
- [EBU R128](https://tech.ebu.ch/loudness) - Loudness recommendation
