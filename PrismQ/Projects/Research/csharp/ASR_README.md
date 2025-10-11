# ASR Module - Whisper Implementation

## Overview

The ASR (Automatic Speech Recognition) module provides C# interfaces for speech-to-text transcription using faster-whisper large-v3. This implementation uses subprocess calls to Python's faster-whisper library, providing high-quality transcription with word-level timestamps.

## Features

- **Multiple Model Sizes**: Support for tiny, base, small, medium, large-v2, and large-v3 models
- **Word-Level Timestamps**: Precise word timing for accurate subtitle generation
- **Language Detection**: Automatic language detection with confidence scores
- **Multiple Output Formats**: Generate SRT and VTT subtitle files
- **GPU Acceleration**: Automatic GPU detection and utilization when available
- **Voice Activity Detection**: Built-in VAD filtering for cleaner transcription
- **Task Types**: Support for both transcription and translation tasks
- **Cross-Platform**: Windows, Linux, and macOS compatible with automatic platform detection
- **Async/Await**: Full async support throughout for non-blocking operations
- **Comprehensive Error Handling**: Structured error responses with detailed messages

## Platform Compatibility

The ASR module is designed to work seamlessly across all major platforms:

| Platform | Python Executable | Path Separator | Status |
|----------|-------------------|----------------|--------|
| Windows | `python` (auto-detected) | `\` | ✅ Fully Supported |
| Linux | `python3` (auto-detected) | `/` | ✅ Fully Supported |
| macOS | `python3` (auto-detected) | `/` | ✅ Fully Supported |

**Key Platform Features:**
- Automatic Python executable detection (python vs python3)
- Platform-specific path handling using `Path.Combine()`
- Cross-platform command-line argument escaping
- Windows-compatible backslash and quote handling

## Installation

### Prerequisites

1. **Python 3.8+** with faster-whisper installed:
   ```bash
   pip install faster-whisper>=0.10.0
   ```

2. **.NET 9.0+** for C# components

3. **CUDA-capable GPU** (optional but recommended for faster processing)

### Python Dependencies

The required Python dependencies are listed in `requirements.txt`:
```
faster-whisper>=0.10.0
```

Install with:
```bash
pip install -r requirements.txt
```

## Architecture

### Components

1. **IWhisperClient.cs** - Interface defining ASR operations
2. **WhisperClient.cs** - C# implementation using subprocess calls
3. **whisper_subprocess.py** - Python wrapper for faster-whisper
4. **WhisperExample.cs** - Example usage and demonstrations

### Communication Flow

```
C# WhisperClient
    ↓ (subprocess with JSON)
Python whisper_subprocess.py
    ↓ (loads model)
faster-whisper library
    ↓ (processes audio)
JSON Response
    ↓ (parsed)
C# TranscriptionResult
```

## Usage

### Basic Transcription

```csharp
using StoryGenerator.Research;

// Initialize client (Python executable auto-detected based on platform)
var client = new WhisperClient(
    modelSize: "large-v3",
    device: "auto",
    computeType: "float16"
);

// Transcribe audio
var result = await client.TranscribeAsync(
    audioPath: "audio.mp3",
    language: "en",
    wordTimestamps: true
);

Console.WriteLine($"Transcription: {result.Text}");
Console.WriteLine($"Language: {result.Language} ({result.LanguageProbability:P2})");
Console.WriteLine($"Words: {result.Words.Count}");
```

### Windows-Specific Configuration

On Windows, the Python executable is automatically detected as `python`. If you have a custom Python installation:

```csharp
// Specify custom Python executable on Windows
var client = new WhisperClient(
    modelSize: "large-v3",
    pythonExecutable: @"C:\Python39\python.exe",  // Custom Python path
    scriptPath: @"C:\Projects\StoryGenerator\research\python\whisper_subprocess.py"
);

// Windows paths work seamlessly
var result = await client.TranscribeAsync(
    audioPath: @"C:\Audio\interview.mp3",
    language: "en"
);
```

### Language Detection

```csharp
var client = new WhisperClient(modelSize: "base");

var (language, confidence) = await client.DetectLanguageAsync("audio.mp3");
Console.WriteLine($"Detected: {language} with {confidence:P2} confidence");
```

### Generate SRT Subtitles

```csharp
var client = new WhisperClient(modelSize: "large-v3");

var srtContent = await client.TranscribeToSrtAsync(
    audioPath: "audio.mp3",
    outputPath: "subtitles.srt",
    language: "en",
    maxWordsPerLine: 10
);

// SRT content is also returned as string
Console.WriteLine(srtContent);
```

### Generate VTT Subtitles

```csharp
var client = new WhisperClient(modelSize: "large-v3");

var vttContent = await client.TranscribeToVttAsync(
    audioPath: "audio.mp3",
    outputPath: "subtitles.vtt",
    language: "en",
    maxWordsPerLine: 10
);
```

### Custom Configuration

```csharp
var client = new WhisperClient(
    modelSize: "large-v3",
    device: "cuda",              // Force GPU
    computeType: "float16",      // Use float16 for GPU
    pythonExecutable: "python3", // Custom Python path
    scriptPath: "/path/to/whisper_subprocess.py" // Custom script path
);

var result = await client.TranscribeAsync(
    audioPath: "audio.mp3",
    language: null,              // Auto-detect language
    task: "transcribe",          // or "translate" to English
    wordTimestamps: true,
    vadFilter: true              // Apply VAD filtering
);
```

## API Reference

### IWhisperClient Interface

#### TranscribeAsync
```csharp
Task<TranscriptionResult> TranscribeAsync(
    string audioPath,
    string language = null,
    string task = "transcribe",
    bool wordTimestamps = true,
    bool vadFilter = true,
    CancellationToken cancellationToken = default
);
```
Transcribe audio file with full control over options.

**Parameters:**
- `audioPath`: Path to audio file (MP3, WAV, FLAC, etc.)
- `language`: Language code (e.g., "en", "es") or null for auto-detection
- `task`: "transcribe" or "translate" (translate to English)
- `wordTimestamps`: Include word-level timestamps
- `vadFilter`: Apply voice activity detection filter
- `cancellationToken`: Cancellation token for async operation

**Returns:** `TranscriptionResult` with text, segments, words, and language info

#### TranscribeToSrtAsync
```csharp
Task<string> TranscribeToSrtAsync(
    string audioPath,
    string outputPath = null,
    string language = null,
    int maxWordsPerLine = 10,
    CancellationToken cancellationToken = default
);
```
Generate SRT subtitle file from audio.

**Parameters:**
- `audioPath`: Path to audio file
- `outputPath`: Path to save SRT file (optional)
- `language`: Language code or null for auto-detection
- `maxWordsPerLine`: Maximum words per subtitle line
- `cancellationToken`: Cancellation token

**Returns:** SRT content as string

#### TranscribeToVttAsync
```csharp
Task<string> TranscribeToVttAsync(
    string audioPath,
    string outputPath = null,
    string language = null,
    int maxWordsPerLine = 10,
    CancellationToken cancellationToken = default
);
```
Generate VTT subtitle file from audio.

**Parameters:** Same as TranscribeToSrtAsync

**Returns:** VTT content as string

#### DetectLanguageAsync
```csharp
Task<(string Language, double Confidence)> DetectLanguageAsync(
    string audioPath,
    CancellationToken cancellationToken = default
);
```
Detect the language of an audio file.

**Parameters:**
- `audioPath`: Path to audio file
- `cancellationToken`: Cancellation token

**Returns:** Tuple of language code and confidence (0.0 to 1.0)

### Data Models

#### TranscriptionResult
```csharp
public class TranscriptionResult
{
    public string Text { get; set; }                    // Full transcription text
    public string Language { get; set; }                // Detected/specified language
    public double LanguageProbability { get; set; }     // Language confidence
    public List<TranscriptionSegment> Segments { get; set; }
    public List<WordTimestamp> Words { get; set; }      // null if wordTimestamps=false
}
```

#### TranscriptionSegment
```csharp
public class TranscriptionSegment
{
    public int Id { get; set; }           // Segment ID
    public double Start { get; set; }     // Start time in seconds
    public double End { get; set; }       // End time in seconds
    public string Text { get; set; }      // Segment text
    public double? Confidence { get; set; } // Average log probability
}
```

#### WordTimestamp
```csharp
public class WordTimestamp
{
    public string Word { get; set; }      // Word text (with spaces)
    public double Start { get; set; }     // Start time in seconds
    public double End { get; set; }       // End time in seconds
    public double Confidence { get; set; } // Word probability
}
```

## Model Sizes and Performance

| Model | Parameters | VRAM | Speed (CPU) | Speed (GPU) | Accuracy |
|-------|-----------|------|-------------|-------------|----------|
| tiny | 39M | ~1GB | ~32x | ~100x | Good |
| base | 74M | ~1GB | ~16x | ~50x | Better |
| small | 244M | ~2GB | ~6x | ~25x | Good |
| medium | 769M | ~5GB | ~2x | ~10x | Very Good |
| large-v2 | 1550M | ~10GB | ~1x | ~5x | Excellent |
| large-v3 | 1550M | ~10GB | ~1x | ~5x | Best |

Speed is relative to real-time (1x = real-time, 10x = 10 times faster than real-time)

**Recommendations:**
- **Testing/Development**: Use `base` or `small` for faster iteration
- **Production**: Use `large-v3` for best quality
- **CPU-only**: Use `tiny` or `base` for reasonable performance
- **GPU Available**: Use `large-v3` for best quality at good speed

## Supported Audio Formats

The module supports all audio formats that FFmpeg can decode:
- MP3
- WAV
- FLAC
- M4A
- OGG
- OPUS
- WMA
- And more...

## Language Support

Whisper supports 99+ languages with multilingual capabilities. Common languages include:
- English (en)
- Spanish (es)
- French (fr)
- German (de)
- Italian (it)
- Portuguese (pt)
- Russian (ru)
- Japanese (ja)
- Korean (ko)
- Chinese (zh)
- And many more...

For a complete list, see: https://github.com/openai/whisper#available-models-and-languages

## Error Handling

```csharp
try
{
    var result = await client.TranscribeAsync("audio.mp3");
    Console.WriteLine(result.Text);
}
catch (FileNotFoundException ex)
{
    Console.WriteLine($"Audio file not found: {ex.Message}");
}
catch (Exception ex)
{
    Console.WriteLine($"Transcription failed: {ex.Message}");
}
```

Common errors:
- `FileNotFoundException`: Audio file or Python script not found
- `Exception`: Python execution error, missing dependencies, or model loading failure

## Performance Optimization

### GPU Acceleration
```csharp
// Force GPU usage
var client = new WhisperClient(
    modelSize: "large-v3",
    device: "cuda",
    computeType: "float16"  // float16 is faster on GPU
);
```

### CPU Optimization
```csharp
// CPU-optimized settings
var client = new WhisperClient(
    modelSize: "base",      // Smaller model
    device: "cpu",
    computeType: "int8"     // int8 quantization for faster CPU inference
);
```

### Disable Unnecessary Features
```csharp
// Faster transcription without word timestamps
var result = await client.TranscribeAsync(
    audioPath: "audio.mp3",
    wordTimestamps: false,  // Skip word-level alignment
    vadFilter: false        // Skip VAD processing
);
```

## Testing

Run the example program to test the implementation:

```bash
cd research/csharp
dotnet run --project WhisperExample.cs path/to/audio.mp3
```

This will demonstrate:
1. Basic transcription with word timestamps
2. Language detection
3. SRT subtitle generation
4. VTT subtitle generation
5. Comparison of different model sizes

## Troubleshooting

### Python Script Not Found
**Error:** `FileNotFoundException: Could not find whisper_subprocess.py`

**Solution:** Ensure the script is in `research/python/whisper_subprocess.py` or provide the full path:
```csharp
var client = new WhisperClient(
    scriptPath: "/full/path/to/whisper_subprocess.py"
);
```

### faster-whisper Not Installed
**Error:** `faster-whisper not installed`

**Solution:**
```bash
pip install faster-whisper>=0.10.0
```

### CUDA Out of Memory
**Error:** `CUDA out of memory`

**Solutions:**
1. Use a smaller model: `base` or `small`
2. Use CPU instead: `device: "cpu"`
3. Use int8 quantization: `computeType: "int8"`

### Slow Performance
**Issue:** Transcription is very slow

**Solutions:**
1. Check GPU availability: The module auto-detects GPU
2. Use smaller model for faster processing
3. Disable word timestamps if not needed
4. Ensure CUDA drivers are properly installed

## References

- [faster-whisper GitHub](https://github.com/guillaumekln/faster-whisper)
- [Hugging Face Model](https://huggingface.co/Systran/faster-whisper-large-v3)
- [OpenAI Whisper](https://github.com/openai/whisper)
- [SRT Format Specification](https://en.wikipedia.org/wiki/SubRip)
- [WebVTT Format Specification](https://w3c.github.io/webvtt/)

## Future Enhancements

- [ ] Batch processing of multiple audio files
- [ ] Real-time streaming transcription
- [ ] Speaker diarization support
- [ ] Custom model loading from local files
- [ ] Progress callbacks for long transcriptions
- [ ] Caching of loaded models
- [ ] Support for ONNX runtime
- [ ] Direct integration without subprocess (using CTranslate2 bindings)

## License

Same as the main StoryGenerator project.
