# Quick Start Guide - ASR Module

Get up and running with the ASR (Automatic Speech Recognition) module in 5 minutes!

## Prerequisites

1. **Python 3.8+** installed
2. **faster-whisper** library:
   ```bash
   pip install faster-whisper>=0.10.0
   ```
3. **.NET 8.0+** (for C# components)

## Quick Test (Python Only)

Test the Python backend without C#:

```bash
# Navigate to the project directory
cd StoryGenerator

# Test with help command (will show if faster-whisper is installed)
python3 research/python/whisper_subprocess.py --help

# Run integration tests
python3 research/python/test_whisper_integration.py
```

## Usage from C#

### Minimal Example

```csharp
using StoryGenerator.Research;

// Create client
var client = new WhisperClient();

// Transcribe
var result = await client.TranscribeAsync("your-audio.mp3");
Console.WriteLine(result.Text);
```

### Full Example with All Features

```csharp
using System;
using System.Threading.Tasks;
using StoryGenerator.Research;

class Program
{
    static async Task Main(string[] args)
    {
        // Initialize client with custom settings
        var client = new WhisperClient(
            modelSize: "large-v3",    // Best quality
            device: "auto",            // Auto-detect GPU/CPU
            computeType: "float16"     // GPU optimization
        );

        string audioFile = "interview.mp3";

        // 1. Transcribe with word timestamps
        Console.WriteLine("Transcribing...");
        var result = await client.TranscribeAsync(
            audioFile,
            language: "en",           // or null for auto-detect
            wordTimestamps: true
        );

        Console.WriteLine($"Text: {result.Text}");
        Console.WriteLine($"Language: {result.Language} ({result.LanguageProbability:P2})");
        Console.WriteLine($"Words: {result.Words.Count}");

        // 2. Generate SRT subtitles
        Console.WriteLine("\nGenerating SRT...");
        await client.TranscribeToSrtAsync(
            audioFile,
            "output.srt",
            maxWordsPerLine: 10
        );
        Console.WriteLine("SRT saved to output.srt");

        // 3. Generate VTT subtitles
        Console.WriteLine("\nGenerating VTT...");
        await client.TranscribeToVttAsync(
            audioFile,
            "output.vtt",
            maxWordsPerLine: 10
        );
        Console.WriteLine("VTT saved to output.vtt");

        // 4. Detect language
        Console.WriteLine("\nDetecting language...");
        var (lang, confidence) = await client.DetectLanguageAsync(audioFile);
        Console.WriteLine($"Language: {lang} (confidence: {confidence:P2})");
    }
}
```

## Command-Line Usage (Python)

### Transcribe Audio

```bash
python3 research/python/whisper_subprocess.py transcribe \
  --audio-path audio.mp3 \
  --model-size large-v3 \
  --language en \
  --word-timestamps \
  --vad-filter
```

Output:
```json
{
  "success": true,
  "text": "Your transcription here...",
  "language": "en",
  "languageProbability": 0.98,
  "segments": [...],
  "words": [...]
}
```

### Detect Language

```bash
python3 research/python/whisper_subprocess.py detect_language \
  --audio-path audio.mp3 \
  --model-size base
```

Output:
```json
{
  "success": true,
  "language": "en",
  "confidence": 0.95
}
```

## Common Use Cases

### Use Case 1: Generate Subtitles for Video

```csharp
var client = new WhisperClient();

// Extract audio from video (use FFmpeg separately)
// Then transcribe to SRT
await client.TranscribeToSrtAsync(
    "video-audio.mp3",
    "video-subtitles.srt",
    maxWordsPerLine: 8  // Shorter lines for readability
);

// Use with FFmpeg to add to video:
// ffmpeg -i video.mp4 -vf subtitles=video-subtitles.srt output.mp4
```

### Use Case 2: Multi-Language Detection

```csharp
var client = new WhisperClient(modelSize: "base");  // Fast for detection

string[] audioFiles = { "audio1.mp3", "audio2.mp3", "audio3.mp3" };

foreach (var file in audioFiles)
{
    var (lang, confidence) = await client.DetectLanguageAsync(file);
    Console.WriteLine($"{file}: {lang} ({confidence:P2})");
}
```

### Use Case 3: Batch Transcription

```csharp
var client = new WhisperClient();

var files = Directory.GetFiles("audio_folder", "*.mp3");

foreach (var file in files)
{
    try
    {
        var result = await client.TranscribeAsync(file);
        
        // Save transcription
        var txtFile = Path.ChangeExtension(file, ".txt");
        await File.WriteAllTextAsync(txtFile, result.Text);
        
        // Save SRT
        var srtFile = Path.ChangeExtension(file, ".srt");
        await client.TranscribeToSrtAsync(file, srtFile);
        
        Console.WriteLine($"✓ Processed: {Path.GetFileName(file)}");
    }
    catch (Exception ex)
    {
        Console.WriteLine($"✗ Failed: {Path.GetFileName(file)} - {ex.Message}");
    }
}
```

## Performance Tips

### For Speed (Development/Testing)
```csharp
var client = new WhisperClient(
    modelSize: "tiny",        // Fastest model
    device: "cpu",            // No GPU needed
    computeType: "int8"       // Fast CPU inference
);
```

### For Accuracy (Production)
```csharp
var client = new WhisperClient(
    modelSize: "large-v3",    // Most accurate
    device: "cuda",           // Use GPU
    computeType: "float16"    // GPU optimization
);
```

### For Balanced Performance
```csharp
var client = new WhisperClient(
    modelSize: "small",       // Good balance
    device: "auto",           // Auto-detect
    computeType: "float16"    // Default
);
```

## Troubleshooting

### Error: "faster-whisper not installed"
**Solution:**
```bash
pip install faster-whisper>=0.10.0
```

### Error: "Could not find whisper_subprocess.py"
**Solution:**
```csharp
// Provide explicit path
var client = new WhisperClient(
    scriptPath: "/full/path/to/whisper_subprocess.py"
);
```

### Error: "CUDA out of memory"
**Solutions:**
1. Use smaller model: `modelSize: "base"`
2. Use CPU: `device: "cpu"`
3. Use int8: `computeType: "int8"`

### Slow Performance
**Check:**
1. GPU is detected: Should show "cuda" in device auto-detection
2. CUDA drivers installed
3. Model size appropriate for hardware
4. Not running on battery (laptop may throttle)

## Model Selection Guide

| Model | When to Use | Speed | Quality |
|-------|-------------|-------|---------|
| tiny | Quick tests, drafts | Very Fast | Basic |
| base | Development, language detection | Fast | Good |
| small | Balanced use | Medium | Good |
| medium | High quality needed | Slow | Very Good |
| large-v3 | Production, best accuracy | Slowest | Excellent |

## Next Steps

1. **Read Full Documentation**: `research/csharp/ASR_README.md`
2. **Run Example**: `research/csharp/WhisperExample.cs`
3. **Read Implementation Details**: `research/csharp/ASR_IMPLEMENTATION_SUMMARY.md`
4. **Integration**: Add to your video processing pipeline

## Support

- **Documentation**: See `research/csharp/ASR_README.md`
- **Examples**: See `research/csharp/WhisperExample.cs`
- **Issues**: Report on GitHub issue tracker
- **faster-whisper Docs**: https://github.com/guillaumekln/faster-whisper

## License

Same as StoryGenerator project.
