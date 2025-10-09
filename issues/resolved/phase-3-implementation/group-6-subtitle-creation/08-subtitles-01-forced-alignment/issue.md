# Subtitles: Forced Alignment

**ID:** `08-subtitles-01-forced-alignment`  
**Priority:** P1  
**Effort:** 4-5 hours  
**Status:** ✅ Implementation Complete (Testing Required)

## Overview

Generate precisely timed subtitles from audio using forced alignment with faster-whisper. This task produces word-level timestamps with ±50ms accuracy, creating both SRT and VTT subtitle files.

**Implementation:** C# service `StoryGenerator.Core.Services.SubtitleAligner` provides full forced alignment functionality using faster-whisper large-v3 model via Python interop.

## Dependencies

**Requires:**
- `07-audio-02` - Normalized audio (LUFS -14.0)
- `06-scenes-03` - Draft subtitle text (for validation)
- faster-whisper Python library installed

**Blocks:**
- `08-subtitles-02` - Scene mapping requires aligned subtitles
- `11-post-02` - Subtitle burn-in requires timed subtitles

## Acceptance Criteria

- [x] C# implementation complete (`SubtitleAligner.cs`)
- [ ] Integration testing with audio pipeline
- [ ] Word-level timestamps accurate to ±50ms
- [ ] SRT format output generated
- [ ] VTT format output generated
- [ ] Language auto-detection working
- [ ] Manual language override supported
- [ ] Error handling for invalid audio
- [ ] Progress reporting implemented
- [ ] Documentation updated

## Task Details

### Implementation

**C# Service:** `StoryGenerator.Core.Services.SubtitleAligner`

```csharp
public interface ISubtitleAligner
{
    Task<string> GenerateAlignedSubtitlesAsync(
        string audioPath,
        string language = null,
        int maxWordsPerLine = 10,
        CancellationToken cancellationToken = default);
}
```

**Key Features:**
- Uses faster-whisper large-v3 for word-level timestamps
- Supports both SRT and VTT output formats
- Auto-detects language or accepts language code
- Configurable words per subtitle line (default: 10)
- Progress reporting and cancellation support

**Example Usage:**

```csharp
var aligner = new SubtitleAligner(whisperClient);

// Generate SRT subtitles
string srtContent = await aligner.GenerateAlignedSubtitlesAsync(
    audioPath: "data/Generator/audio/women/18-23/story_001.wav",
    language: "en",
    maxWordsPerLine: 10
);

// Save to file
var outputPath = "data/Generator/subtitles/timed/women/18-23/story_001.srt";
await File.WriteAllTextAsync(outputPath, srtContent);
```

**Python Integration:**

The service uses faster-whisper via Python subprocess:

```python
# Whisper alignment happens in WhisperClient
import faster_whisper

model = faster_whisper.WhisperModel("large-v3")
result = model.transcribe(
    audio_path,
    language=language,
    word_timestamps=True
)

# Returns word-level timestamps
for segment in result["segments"]:
    for word in segment["words"]:
        print(f"{word['start']:.3f} -> {word['end']:.3f}: {word['text']}")
```

### Testing

```bash
# C# unit tests
cd src/CSharp
dotnet test --filter "FullyQualifiedName~SubtitleAligner"

# Integration test with sample audio
cd src/CSharp/SubtitleAlignment.Example
dotnet run -- \
  data/Generator/audio/women/18-23/story_001.wav \
  women \
  18-23 \
  story_001

# Verify output
cat data/Generator/subtitles/timed/women/18-23/story_001.srt

# Python tests (if needed)
pytest tests/pipeline/test_subtitle_creation.py::test_forced_alignment -v
```

### Output Format Examples

**SRT Format:**
```srt
1
00:00:00,000 --> 00:00:02,500
Have you ever wondered what

2
00:00:02,500 --> 00:00:05,000
happens when you trust the wrong person?

3
00:00:05,000 --> 00:00:08,500
This is the story of Sarah's betrayal.
```

**VTT Format:**
```vtt
WEBVTT

00:00:00.000 --> 00:00:02.500
Have you ever wondered what

00:00:02.500 --> 00:00:05.000
happens when you trust the wrong person?

00:00:05.000 --> 00:00:08.500
This is the story of Sarah's betrayal.
```

## Output Files

**Primary Outputs:**
```
data/Generator/subtitles/timed/{gender}/{age}/
├── {title_id}.srt          # Standard SRT subtitle file
└── {title_id}.vtt          # WebVTT subtitle file
```

**Example:**
```
data/Generator/subtitles/timed/women/18-23/
├── story_001.srt
└── story_001.vtt
```

## Related Files

**C# Implementation:**
- `src/CSharp/StoryGenerator.Core/Services/SubtitleAligner.cs`
- `src/CSharp/StoryGenerator.Core/Interfaces/ISubtitleAligner.cs`
- `src/CSharp/SubtitleAlignment.Example/Program.cs`

**Python Integration:**
- `src/CSharp/StoryGenerator.Research/WhisperClient.cs`
- Python faster-whisper library (external dependency)

**Documentation:**
- `src/CSharp/SUBTITLE_ALIGNMENT.md`
- `src/CSharp/README_SUBTITLE_ALIGNMENT.md`

**Tests:**
- `tests/pipeline/test_subtitle_creation.py`

## Notes

### Performance Considerations
- Whisper large-v3 requires GPU for acceptable performance
- Expect ~30 seconds processing time per minute of audio
- CPU-only mode is 5-10x slower

### Accuracy
- Word-level timestamps accurate to ±50ms
- Accuracy depends on audio quality and speech clarity
- Background noise can reduce alignment precision

### Language Support
- Supports 99 languages via Whisper
- Auto-detection works well for common languages
- Manual language override recommended for mixed content

### Configuration Options
- `maxWordsPerLine`: Controls subtitle line length (default: 10)
- `language`: ISO language code or null for auto-detect
- Model size: Currently hardcoded to "large-v3" (best accuracy)

## Next Steps

After completion:
- ✅ `08-subtitles-02-scene-mapping` - Map subtitles to shots
- ✅ `11-post-02-subtitle-burn` - Burn subtitles into video
- Test with various audio qualities and languages
- Benchmark performance on target hardware
- Validate timestamp accuracy with manual review
