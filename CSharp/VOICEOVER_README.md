# Voiceover Generation and Normalization

This implementation provides local Text-to-Speech (TTS) generation and audio normalization for voiceover content, organized by audience segments (gender/age) with **versioning support** for quality tracking and comparison.

## Key Features

- **Local TTS Generation**: Uses Piper TTS for fast, offline voice synthesis
- **Voice Gender Selection**: Automatically selects male or female voice per segment based on content and audience
- **Audio Normalization**: Applies FFmpeg loudnorm filter to -14 LUFS for consistent loudness
- **Segment Organization**: Organizes audio files by gender and age segments
- **Version Management**: Generates multiple versions (v1, v2, etc.) for quality comparison and A/B testing
- **Loudness Metadata**: Saves normalization parameters as JSON for reference
- **Separate from Python**: Does not interfere with existing Python voiceover generation

## Design Philosophy

1. **Modularity**: Each component (TTS, normalization, voice selection) has a clear interface
2. **Versioning**: Multiple versions coexist for quality comparison without overwriting
3. **Non-invasive**: Python voiceover generation remains completely untouched
4. **Quality Tracking**: Each version has separate files to track quality improvements

## Architecture

### Components

1. **IVoiceoverOrchestrator**: Main interface for voiceover workflow with versioning
2. **VoiceoverOrchestrator**: Implementation with version tracking and file management
3. **ITTSClient**: Interface for TTS operations
4. **PiperTTSClient**: Implementation using Piper TTS
5. **IFFmpegClient**: Interface for FFmpeg operations
6. **FFmpegClient**: Implementation for audio normalization
7. **IVoiceRecommender**: Interface for voice gender selection
8. **SimpleVoiceRecommender**: Content-aware voice recommendation

### Versioned Directory Structure

Audio files are organized with version identifiers:

```
audio/
├── tts/
│   ├── men/
│   │   ├── 18-23/
│   │   │   ├── story_001_v1.wav
│   │   │   ├── story_001_v2.wav
│   │   │   └── story_001_v3.wav
│   │   └── 24-30/
│   └── women/
│       ├── 18-23/
│       └── 24-30/
└── normalized/
    ├── men/
    │   └── 18-23/
    │       ├── story_001_v1_lufs.wav
    │       ├── story_001_v1_lufs.json
    │       ├── story_001_v2_lufs.wav
    │       └── story_001_v2_lufs.json
    └── women/
        └── 18-23/
```

**Benefits:**
- Compare different TTS engines or settings
- Track quality improvements across versions
- A/B test different voiceover approaches
- Never lose previous versions during iteration

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

### Basic Example with Versioning

```csharp
using StoryGenerator.Interfaces;
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

// Create orchestrator with version identifier
var orchestrator = new VoiceoverOrchestrator(
    ttsClient,
    ffmpegClient,
    voiceRecommender,
    versionIdentifier: "v1",  // Track version for quality comparison
    audioRoot: "audio"
);

// Generate voiceover for a segment
var request = new VoiceoverRequest
{
    TitleId = "story_001",
    Title = "The Future of Technology",
    Text = "Welcome to this amazing story...",
    Segment = new AudienceSegment("men", "18-23")
};

var result = await orchestrator.GenerateVoiceoverAsync(request);

if (result.Success)
{
    Console.WriteLine($"Version: {result.Version}");
    Console.WriteLine($"TTS: {result.TTSPath}");
    Console.WriteLine($"Normalized: {result.NormalizedPath}");
    Console.WriteLine($"LUFS JSON: {result.LufsJsonPath}");
}
```

### Generating Multiple Versions for Comparison

```csharp
// Create orchestrators for different versions
var orchestratorV1 = new VoiceoverOrchestrator(
    ttsClient, ffmpegClient, voiceRecommender, 
    versionIdentifier: "v1"
);

var orchestratorV2 = new VoiceoverOrchestrator(
    ttsClient, ffmpegClient, voiceRecommender, 
    versionIdentifier: "v2"
);

// Generate v1
var resultV1 = await orchestratorV1.GenerateVoiceoverAsync(request);

// Generate v2 (different TTS settings, for example)
var resultV2 = await orchestratorV2.GenerateVoiceoverAsync(request);

// Both versions are saved separately:
// audio/tts/men/18-23/story_001_v1.wav
// audio/tts/men/18-23/story_001_v2.wav
// audio/normalized/men/18-23/story_001_v1_lufs.wav
// audio/normalized/men/18-23/story_001_v2_lufs.wav
```

### Running the Example

```bash
cd CSharp/Examples
dotnet run --project VoiceoverGenerationExample.cs
```

## API Reference

### IVoiceoverOrchestrator

Main interface for voiceover generation workflow.

#### GenerateVoiceoverAsync

Generates and normalizes voiceover with versioning support.

**Parameters:**
- `request` (VoiceoverRequest): Request containing title, text, and segment info
- `cancellationToken` (CancellationToken): Optional cancellation token

**Returns:** `VoiceoverGenerationResult` with paths and metrics

**Output Files:**
1. TTS audio: `/audio/tts/{gender}/{age}/{titleId}_{version}.wav` (48 kHz)
2. Normalized audio: `/audio/normalized/{gender}/{age}/{titleId}_{version}_lufs.wav` (48 kHz, -14 LUFS)
3. LUFS parameters: `/audio/normalized/{gender}/{age}/{titleId}_{version}_lufs.json`

### VoiceoverRequest

Request object for voiceover generation.

**Properties:**
- `TitleId` (string): Unique identifier for the content
- `Title` (string): Title text for content analysis
- `Text` (string): Text to convert to speech
- `Segment` (AudienceSegment): Target audience segment
- `VersionSuffix` (string?): Optional version override

### VoiceoverGenerationResult

Result object with generation details.

**Properties:**
- `Success` (bool): Whether generation succeeded
- `TitleId` (string): Title identifier
- `Segment` (AudienceSegment): Audience segment
- `VoiceGender` (VoiceGender): Selected voice gender
- `Version` (string): Version identifier used
- `TTSPath` (string): Path to TTS audio file
- `NormalizedPath` (string): Path to normalized audio
- `LufsJsonPath` (string): Path to LUFS metadata
- `ErrorMessage` (string?): Error message if failed
- `TtsDuration` (double?): TTS generation time in seconds
- `NormalizationDuration` (double?): Normalization time in seconds

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

The loudnorm parameters are saved as JSON with versioning info:

```json
{
  "titleId": "story_001",
  "segment": "men/18-23",
  "voiceGender": "Male",
  "version": "v1",
  "targetLufs": -14.0,
  "targetLra": 7.0,
  "targetTp": -1.0,
  "measurements": {
    "input_i": "-23.5",
    "input_lra": "11.2",
    "input_tp": "-3.8",
    "input_thresh": "-34.1",
    "target_offset": "0.5"
  },
  "generationTimings": {
    "ttsDuration": 1.23,
    "normalizationDuration": 2.45
  }
}
```

## Separation from Python Implementation

This C# implementation is **completely separate** from the existing Python voiceover generation:

- **Python voiceover**: Uses ElevenLabs API, saves to different paths
- **C# voiceover**: Uses local Piper TTS, uses versioned file names
- **No conflicts**: Different file naming conventions prevent overwrites
- **Coexistence**: Both systems can run independently

### Python Files (Unchanged)
```
Python/Generators/GVoice.py          # Original voiceover generator
Python/Generation/Manual/MVoice.py    # Manual voice generation script
```

### C# Files (New)
```
CSharp/Interfaces/IVoiceoverOrchestrator.cs
CSharp/Interfaces/ITTSClient.cs
CSharp/Interfaces/IFFmpegClient.cs
CSharp/Interfaces/IVoiceRecommender.cs
CSharp/Tools/VoiceoverOrchestrator.cs
CSharp/Tools/PiperTTSClient.cs
CSharp/Tools/FFmpegClient.cs
CSharp/Tools/SimpleVoiceRecommender.cs
CSharp/Examples/VoiceoverGenerationExample.cs
```

## Quality Tracking Workflow

1. **Generate Version 1**: Initial implementation with baseline TTS settings
   ```csharp
   var v1 = new VoiceoverOrchestrator(..., versionIdentifier: "v1");
   await v1.GenerateVoiceoverAsync(request);
   ```

2. **Generate Version 2**: Improved settings or different TTS engine
   ```csharp
   var v2 = new VoiceoverOrchestrator(..., versionIdentifier: "v2");
   await v2.GenerateVoiceoverAsync(request);
   ```

3. **Compare Quality**: Listen to both versions
   - `audio/normalized/men/18-23/story_001_v1_lufs.wav`
   - `audio/normalized/men/18-23/story_001_v2_lufs.wav`

4. **Review Metadata**: Check LUFS measurements and timings
   - `audio/normalized/men/18-23/story_001_v1_lufs.json`
   - `audio/normalized/men/18-23/story_001_v2_lufs.json`

5. **Iterate**: Generate v3, v4, etc. as needed for continuous improvement

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
