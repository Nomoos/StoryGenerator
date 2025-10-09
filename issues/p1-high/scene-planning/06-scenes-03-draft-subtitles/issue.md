# Scenes: Draft Subtitle Lines

**ID:** `06-scenes-03-draft-subtitles`  
**Priority:** P1  
**Effort:** 2-3 hours  
**Status:** ✅ Completed

## Overview

Generate draft SRT subtitle files from final scripts with estimated timing. These draft subtitles provide initial timing based on word count and speaking rate, which will be refined later using forced alignment with actual audio (in Phase 6: Subtitle Creation).

## Dependencies

**Requires:**
- `05-script-04` (GPT-improved scripts)
- Final script files in `Generator/scripts/gpt_improved/{gender}/{age}/`

**Blocks:**
- `09-post-02` (Subtitle burning into video)
- `11-subtitles-01` (Forced alignment with audio)
- `11-subtitles-02` (Scene mapping)

## Acceptance Criteria

- [x] Draft subtitle generator implemented in Python (`core/scene_planning.py`)
- [x] Draft subtitle generator implemented in C# (`src/CSharp/Generators/SubtitleGenerator.cs`)
- [x] Generates SRT files with proper format
- [x] Subtitle timing based on word count and speaking rate
- [x] Subtitle text follows natural speech breaks
- [x] Maximum characters per line respected (~42 chars)
- [x] Output saved to correct directory structure
- [x] Documentation updated
- [x] Tests passing

## Task Details

### Implementation

**Python Implementation:**
```python
from core.scene_planning import ScenePlanner

planner = ScenePlanner(output_root="./Generator")

# Generate draft subtitles
subtitles = planner.generate_draft_subtitles(
    script_text=script_content,
    total_duration=45.0  # Optional for better accuracy
)

# Save to SRT file
output_path = planner.save_draft_subtitles(
    subtitles=subtitles,
    title_id="story_001",
    gender="women",
    age="18-24"
)
```

**C# Implementation:**
```csharp
using StoryGenerator.Generators;

var subtitleGenerator = new SubtitleGenerator("./Generator/subtitles");

var srtPath = await subtitleGenerator.GenerateAndSaveSubtitlesAsync(
    scriptText: scriptContent,
    titleId: "story_001",
    segment: "women",
    age: "18-24",
    audioDuration: 45.0f
);
```

### SRT Format

Standard SRT subtitle format:
```srt
1
00:00:00,000 --> 00:00:05,000
In a world where books are banned

2
00:00:05,000 --> 00:00:09,500
one woman fights to preserve knowledge

3
00:00:09,500 --> 00:00:14,000
She discovers a hidden library
```

### Features

- **Automatic Text Splitting**: Long sentences split into subtitle-sized chunks
- **Character Limit**: Respects ~42 character maximum per subtitle line
- **Natural Breaks**: Splits at natural speech boundaries when possible
- **Estimated Timing**: Uses 150 words per minute speaking rate
- **Duration Scaling**: If total duration provided, scales timing to match

### Testing

```bash
# Run Python tests
python -m pytest tests/test_scene_planning.py::TestScenePlanner::test_generate_draft_subtitles -v
python -m pytest tests/test_scene_planning.py::TestSubtitleEntry -v

# Test SRT format
python -m pytest tests/test_scene_planning.py::TestScenePlanner::test_subtitle_srt_format -v

# Run C# tests
cd src/CSharp
dotnet test --filter "FullyQualifiedName~Subtitle"
```

## Output Files

**Directory:** `Generator/subtitles/srt/{gender}/{age}/`

**Files Created:**
- `{title_id}_draft.srt` - Draft subtitle file with estimated timing
  - Contains: Subtitle entries with index, timing, and text
  - Format: SRT (SubRip Text)
  - Example: `story_001_draft.srt`

**Note:** The `_draft` suffix indicates these are preliminary timings that should be refined with actual audio in the Subtitle Creation phase.

## Related Files

**Python:**
- `core/scene_planning.py` - Main implementation
  - `generate_draft_subtitles()` - Generate subtitle entries
  - `save_draft_subtitles()` - Save to SRT file
  - `SubtitleEntry` class - Subtitle data structure
- `tests/test_scene_planning.py` - Comprehensive tests

**C#:**
- `src/CSharp/Generators/SubtitleGenerator.cs` - C# implementation
- `src/CSharp/Examples/SceneBeatsAndSubtitlesExample.cs` - Usage example

**Documentation:**
- `src/CSharp/Generators/README_BEATS_SUBTITLES.md` - Detailed guide
- `docs/PIPELINE_OUTPUT_FILES.md` - Output file reference
- `obsolete/research/python/srt_tools.py` - SRT utilities (research)

## Notes

- Draft subtitles use estimated timing based on word count
- Timing will be refined in Phase 6 using forced alignment (Whisper/WhisperX)
- The `_draft` suffix is important to distinguish from final timed subtitles
- Character limit ensures readability on mobile devices
- SRT format is industry standard and supported by all video players
- Long sentences are automatically split for better readability

## Next Steps

After completion:
- ⏭️  `07-audio-01` - Generate TTS voiceover audio
- ⏭️  `11-subtitles-01` - Forced alignment with actual audio timestamps
- ⏭️  `11-subtitles-02` - Map aligned subtitles to video scenes
- ⏭️  `09-post-02` - Burn final subtitles into video
