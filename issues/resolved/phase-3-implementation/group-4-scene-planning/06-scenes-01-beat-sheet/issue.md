# Scenes: Beat Sheet Generation

**ID:** `06-scenes-01-beat-sheet`  
**Priority:** P1  
**Effort:** 3-4 hours  
**Status:** ✅ Completed

## Overview

Generate structured beat sheets from final scripts. Beat sheets break down the narrative into timed scenes/shots with visual descriptions, forming the foundation for image generation and video production.

## Dependencies

**Requires:**
- `05-script-04` (GPT-improved scripts)
- Final script files in `Generator/scripts/gpt_improved/{gender}/{age}/`

**Blocks:**
- `07-images-01` (Prompt building for image generation)
- `08-video-01` (LTX video synthesis)
- `06-scenes-02` (Shot list generation)

## Acceptance Criteria

- [x] Beat sheet generator implemented in Python (`core/scene_planning.py`)
- [x] Beat sheet generator implemented in C# (`src/CSharp/Generators/SimpleSceneBeatsGenerator.cs`)
- [x] Generates JSON files with shot timing and descriptions
- [x] Each shot includes: number, start/end time, duration, description, visual prompt, narration
- [x] Total duration matches audio duration
- [x] Shots are properly sequenced (1, 2, 3, ...)
- [x] Output saved to correct directory structure
- [x] Documentation updated
- [x] Tests passing

## Task Details

### Implementation

**Python Implementation:**
```python
from core.scene_planning import ScenePlanner

planner = ScenePlanner(output_root="./Generator")

# Generate beat sheet from script
beat_sheet = planner.generate_beat_sheet(
    script_text=script_content,
    title_id="story_001",
    total_duration=45.0  # Audio duration in seconds
)

# Save to file
output_path = planner.save_beat_sheet(
    beat_sheet=beat_sheet,
    gender="women",
    age="18-24"
)
```

**C# Implementation:**
```csharp
using StoryGenerator.Generators;

var beatsGenerator = new SimpleSceneBeatsGenerator("./Generator/scenes");

var shotsPath = await beatsGenerator.GenerateAndSaveBeatsAsync(
    scriptText: scriptContent,
    titleId: "story_001",
    segment: "women",
    age: "18-24",
    audioDuration: 45.0f
);
```

### JSON Schema

Beat sheet output format (`{title_id}_shots.json`):

```json
{
  "titleId": "story_001",
  "totalDuration": 45.0,
  "totalShots": 5,
  "generatedAt": "2024-01-01T00:00:00Z",
  "shots": [
    {
      "shotNumber": 1,
      "startTime": 0.0,
      "endTime": 8.0,
      "duration": 8.0,
      "sceneDescription": "Opening scene description...",
      "visualPrompt": "Cinematic establishing shot...",
      "narration": "In a world where books are banned..."
    }
  ]
}
```

### Testing

```bash
# Run Python tests
cd /home/runner/work/StoryGenerator/StoryGenerator
python -m pytest tests/test_scene_planning.py::TestScenePlanner::test_generate_beat_sheet -v

# Run C# tests
cd src/CSharp
dotnet test --filter "FullyQualifiedName~SceneBeats"
```

## Output Files

**Directory:** `Generator/scenes/json/{gender}/{age}/`

**Files Created:**
- `{title_id}_shots.json` - Beat sheet with timed shots
  - Contains: Shot array with timing, descriptions, visual prompts
  - Format: JSON
  - Example: `story_001_shots.json`

## Related Files

**Python:**
- `core/scene_planning.py` - Main implementation
- `tests/test_scene_planning.py` - Comprehensive tests

**C#:**
- `src/CSharp/Generators/SimpleSceneBeatsGenerator.cs` - C# implementation
- `src/CSharp/Generators/SceneBeatsGenerator.cs` - LLM-based version
- `src/CSharp/Examples/SceneBeatsAndSubtitlesExample.cs` - Usage example

**Documentation:**
- `src/CSharp/Generators/README_BEATS_SUBTITLES.md` - Detailed C# docs
- `docs/PIPELINE_OUTPUT_FILES.md` - Output file reference

## Notes

- Beat sheets use simple sentence-based splitting (no LLM required)
- Shot duration calculated based on word count and speaking rate (150 WPM)
- Visual prompts are basic in this version; can be enhanced with LLM
- Timing is scaled to match total audio duration
- For LLM-enhanced beat sheets, use `SceneBeatsGenerator.cs` (C# only)

## Next Steps

After completion:
- ✅ `06-scenes-02` - Generate detailed shot lists (if separate from beats)
- ✅ `06-scenes-03` - Create draft subtitle timing
- ⏭️  `07-images-01` - Build image generation prompts from visual descriptions
- ⏭️  `08-video-01` - Use shot timing for video synthesis
