# Subtitles: Map to Scenes

**ID:** `08-subtitles-02-scene-mapping`  
**Priority:** P1  
**Effort:** 2-3 hours  
**Status:** ✅ Implementation Complete (Testing Required)

## Overview

Map subtitle time ranges to shot IDs from the shotlist, creating a comprehensive mapping file that links each subtitle segment to its corresponding video scene. This enables precise subtitle-to-video coordination during post-production.

**Implementation:** C# service `StoryGenerator.Core.Services.SubtitleAligner` includes scene mapping functionality that correlates subtitle timestamps with shot timing information.

## Dependencies

**Requires:**
- `08-subtitles-01` - Aligned subtitles with word-level timestamps
- `06-scenes-02` - Shot list with scene timing information

**Blocks:**
- `11-post-02` - Subtitle burn-in benefits from shot mapping
- `12-qc-02` - Sync checking requires subtitle-to-shot correlation

## Acceptance Criteria

- [x] C# implementation complete (`SubtitleAligner.MapSubtitlesToShotsAsync`)
- [ ] Integration testing with shotlist data
- [ ] Subtitle segments correctly mapped to shot IDs
- [ ] JSON mapping file generated
- [ ] Handles edge cases (overlapping shots, gaps)
- [ ] Validation for misaligned timings
- [ ] Error handling for invalid shotlist
- [ ] Progress reporting implemented
- [ ] Documentation updated

## Task Details

### Implementation

**C# Service:** `StoryGenerator.Core.Services.SubtitleAligner`

```csharp
public interface ISubtitleAligner
{
    Task<SubtitleToShotMapping> MapSubtitlesToShotsAsync(
        string audioPath,
        Shotlist shotlist,
        string titleId,
        string language = null,
        int maxWordsPerLine = 10,
        CancellationToken cancellationToken = default);

    Task<string> MapAndSaveSubtitlesToShotsAsync(
        string audioPath,
        Shotlist shotlist,
        string titleId,
        string outputPath,
        string language = null,
        int maxWordsPerLine = 10,
        CancellationToken cancellationToken = default);
}
```

**Key Features:**
- Maps subtitle time ranges to shot IDs
- Handles multiple subtitles per shot
- Validates timing consistency
- Exports comprehensive JSON mapping
- Supports subtitle-to-shot queries

**Example Usage:**

```csharp
var aligner = new SubtitleAligner(whisperClient);

// Load shotlist
var shotlist = await LoadShotlistAsync("data/Generator/scenes/json/women/18-23/story_001_shotlist.json");

// Generate mapping
var mapping = await aligner.MapSubtitlesToShotsAsync(
    audioPath: "data/Generator/audio/women/18-23/story_001.wav",
    shotlist: shotlist,
    titleId: "story_001",
    language: "en"
);

// Save to JSON
await aligner.MapAndSaveSubtitlesToShotsAsync(
    audioPath: "data/Generator/audio/women/18-23/story_001.wav",
    shotlist: shotlist,
    titleId: "story_001",
    outputPath: "data/Generator/scenes/json/women/18-23/story_001_subs_to_shots.json"
);
```

**Mapping Algorithm:**

```
For each subtitle segment:
  1. Get subtitle start and end times
  2. Find all shots that overlap this time range
  3. Calculate overlap percentage
  4. Assign subtitle to shot with maximum overlap
  5. Record mapping in JSON structure
```

### Data Models

**SubtitleToShotMapping:**

```csharp
public class SubtitleToShotMapping
{
    public string TitleId { get; set; }
    public List<SubtitleSegment> Subtitles { get; set; }
    public Dictionary<int, List<int>> ShotToSubtitles { get; set; }
    public DateTime GeneratedAt { get; set; }
}

public class SubtitleSegment
{
    public int Index { get; set; }
    public double StartTime { get; set; }
    public double EndTime { get; set; }
    public string Text { get; set; }
    public int ShotId { get; set; }
    public double OverlapPercentage { get; set; }
}
```

### Testing

```bash
# C# unit tests
cd src/CSharp
dotnet test --filter "FullyQualifiedName~SubtitleMapping"

# Integration test with sample data
cd src/CSharp/SubtitleAlignment.Example
dotnet run -- \
  data/Generator/audio/women/18-23/story_001.wav \
  women \
  18-23 \
  story_001 \
  --with-mapping

# Verify mapping output
cat data/Generator/scenes/json/women/18-23/story_001_subs_to_shots.json | jq

# Python tests (if needed)
pytest tests/pipeline/test_subtitle_creation.py::test_scene_mapping -v
```

### Output Format Example

**JSON Mapping Structure:**

```json
{
  "titleId": "story_001",
  "generatedAt": "2024-01-15T10:30:00Z",
  "subtitles": [
    {
      "index": 1,
      "startTime": 0.0,
      "endTime": 2.5,
      "text": "Have you ever wondered what",
      "shotId": 1,
      "overlapPercentage": 100.0
    },
    {
      "index": 2,
      "startTime": 2.5,
      "endTime": 5.0,
      "text": "happens when you trust the wrong person?",
      "shotId": 1,
      "overlapPercentage": 80.0
    },
    {
      "index": 3,
      "startTime": 5.0,
      "endTime": 8.5,
      "text": "This is the story of Sarah's betrayal.",
      "shotId": 2,
      "overlapPercentage": 100.0
    }
  ],
  "shotToSubtitles": {
    "1": [1, 2],
    "2": [3],
    "3": [4, 5]
  }
}
```

## Output Files

**Primary Outputs:**
```
data/Generator/scenes/json/{gender}/{age}/
└── {title_id}_subs_to_shots.json    # Subtitle-to-shot mapping
```

**Example:**
```
data/Generator/scenes/json/women/18-23/
└── story_001_subs_to_shots.json
```

**Related Files (inputs):**
```
data/Generator/subtitles/timed/{gender}/{age}/{title_id}.srt
data/Generator/scenes/json/{gender}/{age}/{title_id}_shotlist.json
```

## Related Files

**C# Implementation:**
- `src/CSharp/StoryGenerator.Core/Services/SubtitleAligner.cs`
- `src/CSharp/StoryGenerator.Core/Interfaces/ISubtitleAligner.cs`
- `src/CSharp/StoryGenerator.Core/Models/SubtitleToShotMapping.cs`
- `src/CSharp/SubtitleAlignment.Example/Program.cs`

**Documentation:**
- `src/CSharp/SUBTITLE_ALIGNMENT.md` (Section: "Shot Mapping Algorithm")
- `src/CSharp/README_SUBTITLE_ALIGNMENT.md`

**Tests:**
- `tests/pipeline/test_subtitle_creation.py`

## Notes

### Mapping Strategy

**Overlap Calculation:**
```
overlap = min(subtitle_end, shot_end) - max(subtitle_start, shot_start)
overlap_percentage = (overlap / subtitle_duration) * 100
```

**Edge Cases:**
1. **Subtitle spans multiple shots:** Assign to shot with maximum overlap
2. **Gaps between shots:** Subtitle assigned to nearest shot
3. **Overlapping shots:** Use first shot in sequence
4. **Subtitle starts before first shot:** Assign to shot 1
5. **Subtitle ends after last shot:** Assign to last shot

### Validation

The mapping process validates:
- All subtitles assigned to valid shot IDs
- No orphaned subtitles (unassigned)
- Shot timing consistency
- Total coverage percentage

### Performance

- Mapping is fast: O(n*m) where n=subtitles, m=shots
- Typical processing time: < 1 second for 50 subtitles, 20 shots
- Memory efficient: entire mapping held in memory

### Use Cases

**Post-Production:**
- Determine which subtitles appear in each video clip
- Synchronize subtitle burn-in with shot transitions
- Apply shot-specific subtitle styling

**Quality Control:**
- Verify subtitle timing relative to visual scenes
- Check for misaligned subtitles
- Validate subtitle-shot coherence

## Next Steps

After completion:
- ✅ `11-post-02-subtitle-burn` - Use mapping for precise subtitle placement
- ✅ `12-qc-02-sync-check` - Validate subtitle-to-shot synchronization
- Test with various shot list structures
- Validate mapping accuracy with visual review
- Document common mapping patterns and edge cases
