# Scenes: Shot List Creation

**ID:** `06-scenes-02-shotlist`  
**Priority:** P1  
**Effort:** 3-4 hours  
**Status:** ✅ Completed (Merged with Beat Sheet)

## Overview

Generate detailed shot lists from scripts. This task was merged with `06-scenes-01-beat-sheet` as the beat sheet already includes comprehensive shot information. The shot list is effectively the `shots` array within the beat sheet JSON.

## Dependencies

**Requires:**
- `05-script-04` (GPT-improved scripts)
- `06-scenes-01` (Beat sheet generation - same implementation)

**Blocks:**
- `07-images-01` (Prompt building)
- `08-video-01` (Video synthesis)

## Acceptance Criteria

- [x] Shot list generation implemented (as part of beat sheet)
- [x] Each shot contains detailed metadata
- [x] Shots include timing, descriptions, and visual prompts
- [x] Sequential shot numbering
- [x] Documentation updated
- [x] Tests passing

## Task Details

### Implementation

Shot lists are generated as part of the beat sheet structure. The beat sheet's `shots` array serves as the detailed shot list.

**Using Python:**
```python
from core.scene_planning import ScenePlanner

planner = ScenePlanner(output_root="./Generator")

# Generate beat sheet (includes shot list)
beat_sheet = planner.generate_beat_sheet(
    script_text=script_content,
    title_id="story_001",
    total_duration=45.0
)

# Access shot list
for shot in beat_sheet.shots:
    print(f"Shot {shot.shot_number}: {shot.duration}s")
    print(f"  Description: {shot.scene_description}")
    print(f"  Visual: {shot.visual_prompt}")
```

**Using C#:**
```csharp
using StoryGenerator.Generators;

var beatsGenerator = new SimpleSceneBeatsGenerator();
var shotsPath = await beatsGenerator.GenerateAndSaveBeatsAsync(
    scriptText, titleId, segment, age, audioDuration
);

// Shot list is in the "shots" array of the JSON
```

### Shot List Structure

Each shot in the list contains:
- `shotNumber`: Sequential shot identifier (1, 2, 3, ...)
- `startTime`: Shot start time in seconds
- `endTime`: Shot end time in seconds
- `duration`: Shot duration in seconds
- `sceneDescription`: Brief description of the scene
- `visualPrompt`: Prompt for image generation
- `narration`: Voiceover text for this shot

### Testing

```bash
# Test shot list generation
python -m pytest tests/test_scene_planning.py::TestScenePlanner::test_generate_beat_sheet -v

# Verify shot structure
python -m pytest tests/test_scene_planning.py::TestShot -v
```

## Output Files

**Directory:** `Generator/scenes/json/{gender}/{age}/`

**Files Created:**
- `{title_id}_shots.json` - Contains shot list in `shots` array
  - Format: JSON
  - Example: `story_001_shots.json`

**Example Structure:**
```json
{
  "titleId": "story_001",
  "totalDuration": 45.0,
  "totalShots": 5,
  "shots": [
    {
      "shotNumber": 1,
      "startTime": 0.0,
      "endTime": 9.0,
      "duration": 9.0,
      "sceneDescription": "Opening establishing shot",
      "visualPrompt": "Wide angle cinematic shot of...",
      "narration": "In a world where..."
    }
  ]
}
```

## Related Files

**Python:**
- `core/scene_planning.py` - Shot list generation in beat sheet
- `tests/test_scene_planning.py` - Tests for shot structure

**C#:**
- `src/CSharp/Generators/SimpleSceneBeatsGenerator.cs` - Shot list implementation
- `src/CSharp/Generators/SceneBeatsGenerator.cs` - LLM-enhanced version

**Documentation:**
- `src/CSharp/Generators/README_BEATS_SUBTITLES.md` - Implementation guide
- `docs/PIPELINE_OUTPUT_FILES.md` - File format reference

## Notes

- Shot list and beat sheet are unified in a single JSON structure
- This avoids duplication and ensures consistency
- Shot timing is automatically calculated based on script word count
- Visual prompts can be enhanced using LLM (see `SceneBeatsGenerator.cs`)
- Shots are designed to align with video synthesis requirements

## Next Steps

After completion:
- ✅ `06-scenes-03` - Generate draft subtitles with timing
- ⏭️  `07-images-01` - Use visual prompts for image generation
- ⏭️  `08-video-01` - Use shot timing for video clip synthesis
- ⏭️  `09-post-01` - Use shot boundaries for video concatenation
