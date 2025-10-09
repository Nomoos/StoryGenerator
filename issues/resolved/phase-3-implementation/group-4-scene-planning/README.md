# Scene Planning Group

**Phase:** 3 - Implementation  
**Tasks:** 3  
**Priority:** P1  
**Duration:** 1-2 days  
**Team Size:** 2 developers  
**Status:** ✅ **COMPLETED**

## Overview

Break scripts into scenes, shots, and draft subtitles for video production. This group provides the foundational timing and structure for video synthesis, image generation, and subtitle creation.

## Completed Tasks

1. ✅ **06-scenes-01-beat-sheet** (P1) - Create beat sheets from scripts
2. ✅ **06-scenes-02-shotlist** (P1) - Generate detailed shot lists (merged with beat sheet)
3. ✅ **06-scenes-03-draft-subtitles** (P1) - Create draft subtitle lines

## Implementation Summary

### Python Implementation
- **Module:** `core/scene_planning.py`
- **Classes:** 
  - `ScenePlanner` - Main scene planning functionality
  - `BeatSheet` - Beat sheet data structure
  - `Shot` - Individual shot data
  - `SubtitleEntry` - Subtitle entry data
- **Tests:** `tests/test_scene_planning.py` (comprehensive coverage)

### C# Implementation
- **Module:** `src/CSharp/Generators/`
- **Classes:**
  - `SimpleSceneBeatsGenerator` - Beat sheet and shot list generation
  - `SubtitleGenerator` - Draft SRT subtitle generation
  - `SceneBeatsGenerator` - LLM-enhanced version (optional)
- **Examples:** `src/CSharp/Examples/SceneBeatsAndSubtitlesExample.cs`
- **Documentation:** `src/CSharp/Generators/README_BEATS_SUBTITLES.md`

## Dependencies

**Requires:** Script Development group (final scripts)  
**Blocks:** Image Generation, Video Production, Subtitle Creation

## Output Files

```
Generator/
├── scenes/
│   └── json/{gender}/{age}/
│       └── {title_id}_shots.json      # Beat sheet with shot list
└── subtitles/
    └── srt/{gender}/{age}/
        └── {title_id}_draft.srt       # Draft subtitles with estimated timing
```

## Key Features

### Beat Sheet & Shot List
- Automatic scene splitting based on script structure
- Timed shots with start/end times and duration
- Visual prompts for each shot (for image generation)
- Scene descriptions and narration text
- Scales to match audio duration

### Draft Subtitles
- SRT format generation from script text
- Estimated timing based on speaking rate (150 WPM)
- Automatic text splitting to respect character limits (~42 chars)
- Natural speech breaks
- Ready for forced alignment in Phase 6

## Usage Examples

### Python
```python
from core.scene_planning import ScenePlanner

planner = ScenePlanner(output_root="./Generator")

# Generate complete scene plan
paths = planner.generate_scene_plan(
    script_text=script_content,
    title_id="story_001",
    gender="women",
    age="18-24",
    total_duration=45.0
)

# Returns:
# {
#   'beat_sheet': Path('Generator/scenes/json/women/18-24/story_001_shots.json'),
#   'subtitles': Path('Generator/subtitles/srt/women/18-24/story_001_draft.srt')
# }
```

### C#
```csharp
using StoryGenerator.Generators;

// Generate beat sheet
var beatsGen = new SimpleSceneBeatsGenerator("./Generator/scenes");
var shotsPath = await beatsGen.GenerateAndSaveBeatsAsync(
    scriptText, titleId, segment, age, audioDuration);

// Generate subtitles
var subsGen = new SubtitleGenerator("./Generator/subtitles");
var srtPath = await subsGen.GenerateAndSaveSubtitlesAsync(
    scriptText, titleId, segment, age, audioDuration);
```

## Testing

```bash
# Python tests
python -m pytest tests/test_scene_planning.py -v

# C# tests
cd src/CSharp
dotnet test --filter "FullyQualifiedName~SceneBeats|Subtitle"
```

## Next Steps

With Scene Planning complete, the following Phase 3 groups can proceed:

✅ **Completed Groups:**
1. Content Pipeline (Group 1)
2. Idea Generation (Group 2)  
3. Script Development (Group 3)
4. **Scene Planning (Group 4)** ← YOU ARE HERE

⏭️ **Ready to Implement:**
5. **Audio Production (Group 5)** - TTS generation and normalization
6. **Image Generation (Group 7)** - Keyframe generation from visual prompts
7. **Video Production (Group 8)** - Video clip synthesis from images

📋 **Dependent on Above:**
8. Subtitle Creation (Group 6) - Requires audio for forced alignment
9. Post-Production (Group 9) - Requires video clips
10. Quality Control (Group 10) - Requires final video
11. Export & Delivery (Group 11) - Requires QC pass

## Documentation

- ✅ Issue templates filled with detailed information
- ✅ Python implementation documented in code
- ✅ C# implementation documented in README_BEATS_SUBTITLES.md
- ✅ Tests provide usage examples
- ✅ Output file formats documented in PIPELINE_OUTPUT_FILES.md
