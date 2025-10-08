# Research: C# Whisper Client

**ID:** `01-research-07-csharp-whisper`  
**Priority:** P1  
**Effort:** 4-6 hours  
**Status:** ✅ Complete

## Overview

C# client implementation for Whisper ASR (Automatic Speech Recognition) integration. This research prototype validates calling Python's faster-whisper from C# for high-quality speech-to-text with word-level timestamps. The implementation supports multiple model sizes and provides detailed transcription metadata essential for subtitle timing and audio alignment.

## Dependencies

**Requires:**
- `00-setup-04`: C# project structure
- Python 3.8+ with faster-whisper installed
- CUDA toolkit (optional, for GPU acceleration)

**Blocks:**
- Phase 3 subtitle creation tasks
- Audio transcription and timing tasks
- Voiceover quality validation

## Acceptance Criteria

- [x] C# can call Python faster-whisper subprocess
- [x] Supports multiple model sizes (tiny to large-v3)
- [x] Returns word-level timestamps
- [x] Handles audio file paths correctly
- [x] Async/await with cancellation support
- [x] JSON deserialization of transcription results
- [x] Documentation and usage examples provided

## Task Details

### Implementation

The `WhisperClient` class in `StoryGenerator.Research` wraps faster-whisper via subprocess:

```csharp
public class WhisperClient : IWhisperClient
{
    private readonly string _modelSize;
    private readonly string _device;
    private readonly string _computeType;

    public WhisperClient(
        string modelSize = "large-v3",
        string device = "auto",
        string computeType = "float16",
        string pythonExecutable = null,
        string scriptPath = null)
    {
        // Auto-detects Python and script path
        // Supports: tiny, base, small, medium, large-v2, large-v3
    }

    public async Task<TranscriptionResult> TranscribeAsync(
        string audioPath,
        string language = null,
        bool wordTimestamps = true,
        CancellationToken cancellationToken = default)
    {
        // Calls: python whisper_subprocess.py <audioPath> --model <size>
        // Returns structured JSON with segments and word timings
    }
}
```

**Key Features:**
- **Model Sizes**: tiny (39M) → large-v3 (1.5GB)
  - `tiny`: Fast, lower accuracy (~1 GB RAM)
  - `base`: Good balance (~1 GB RAM)
  - `medium`: High accuracy (~5 GB RAM)
  - `large-v3`: Best accuracy (~10 GB RAM, GPU recommended)
- **Word Timestamps**: Precise start/end times for each word
- **Language Detection**: Auto-detect or specify language code
- **Device Selection**: CPU, CUDA (GPU), or auto
- **Compute Types**: float16, float32, int8 for memory/speed tradeoff

**Transcription Result Structure:**
```csharp
public class TranscriptionResult
{
    public string Text { get; set; }              // Full transcript
    public string Language { get; set; }          // Detected/specified language
    public List<Segment> Segments { get; set; }   // Time-aligned segments
}

public class Segment
{
    public double Start { get; set; }    // Start time in seconds
    public double End { get; set; }      // End time in seconds
    public string Text { get; set; }     // Segment text
    public List<Word> Words { get; set; } // Word-level timestamps
}

public class Word
{
    public string Text { get; set; }     // Word text
    public double Start { get; set; }    // Start time
    public double End { get; set; }      // End time
    public float Probability { get; set; } // Confidence (0.0-1.0)
}
```

**Process Management:**
- Spawns Python subprocess with whisper_subprocess.py helper script
- Passes audio file path and parameters via command-line args
- Reads JSON output from stdout
- Deserializes into strongly-typed C# models
- Handles process cleanup and error reporting

### Testing

```bash
# Install faster-whisper (Python)
pip install faster-whisper

# Build C# research project
cd src/CSharp
dotnet build StoryGenerator.Research/StoryGenerator.Research.csproj

# Test with sample audio file
ffmpeg -f lavfi -i "sine=frequency=1000:duration=3" -ar 16000 test_audio.wav

# Run demo (if orchestrator includes Whisper test)
cd StoryGenerator.Research
dotnet run
```

**Example Usage:**
```csharp
var client = new WhisperClient(
    modelSize: "large-v3",
    device: "cuda",  // or "cpu" or "auto"
    computeType: "float16"
);

var result = await client.TranscribeAsync(
    audioPath: "path/to/audio.wav",
    language: "en",  // or null for auto-detect
    wordTimestamps: true
);

Console.WriteLine($"Transcript: {result.Text}");
Console.WriteLine($"Language: {result.Language}");

foreach (var segment in result.Segments)
{
    Console.WriteLine($"[{segment.Start:F2}s - {segment.End:F2}s]: {segment.Text}");
    
    foreach (var word in segment.Words)
    {
        Console.WriteLine($"  {word.Text} ({word.Start:F2}s)");
    }
}
```

## Output Files

- `/src/CSharp/StoryGenerator.Research/WhisperClient.cs` - Main implementation (600+ lines)
- `/src/CSharp/StoryGenerator.Research/IWhisperClient.cs` - Interface definition
- `/src/CSharp/StoryGenerator.Research/Models.cs` - Transcription result models
- `research/python/whisper_subprocess.py` - Python helper script (if exists)

## Related Files

- `/config/pipeline.yaml` - ASR model configuration (faster-whisper-large-v3)
- Whisper documentation: https://github.com/openai/whisper
- faster-whisper: https://github.com/guillaumekln/faster-whisper

## Validation

```bash
# Verify implementation
ls -la src/CSharp/StoryGenerator.Research/WhisperClient.cs

# Check project builds
cd src/CSharp && dotnet build StoryGenerator.Research/StoryGenerator.Research.csproj

# Test Python faster-whisper installation
python -c "import faster_whisper; print('OK')"

# Download test audio
ffmpeg -f lavfi -i "sine=frequency=440:duration=1" -ar 16000 test.wav
```

## Notes

**Integration Approach:**
- Uses Python subprocess for faster-whisper (no C# native bindings exist)
- Communicates via command-line args and JSON stdout
- Alternative: Could use HTTP API if running whisper as service

**Model Requirements:**
- First run downloads model from Hugging Face (~1.5 GB for large-v3)
- Models cached in `~/.cache/huggingface/`
- GPU (CUDA) highly recommended for large models

**Performance Characteristics:**
- `tiny`: ~32x real-time (1 min audio = 2 sec processing)
- `base`: ~16x real-time
- `medium`: ~8x real-time (CPU), ~50x (GPU)
- `large-v3`: ~3x real-time (CPU), ~30x (GPU)

**Accuracy Considerations:**
- Word timestamps ±50ms typically
- Better with clear speech, worse with background noise
- Language auto-detection works well for major languages
- Consider forced alignment for subtitle precision

**Known Limitations:**
- Requires Python environment with faster-whisper
- GPU support needs CUDA toolkit
- Long audio files (>30 min) may need chunking
- No speaker diarization (who is speaking)

**Memory Requirements:**
- `tiny/base`: 1-2 GB RAM
- `medium`: 5 GB RAM
- `large-v3`: 10 GB RAM (6 GB VRAM for GPU)

## Next Steps

After completion:
- Phase 3 subtitle creation tasks can use word timestamps
- Audio transcription for quality validation
- Voiceover accuracy checks
- Consider VAD (voice activity detection) preprocessing
