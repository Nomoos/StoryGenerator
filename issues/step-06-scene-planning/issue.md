# Step 6: Scene Planning

**Status:** Not Started  
**Priority:** High  
**Dependencies:** Step 4 (Final Scripts), Step 5 (Final Titles)

## Overview

Create detailed scene breakdowns from final scripts, including beat-sheets, shotlists, and draft subtitles.

## Target Audience
- Segments: `women/{age}` and `men/{age}`
- Age buckets: `10-13`, `14-17`, `18-23`
- Apply to 30 final scripts (5 per segment/age)

## Checklist

### 6.1 Beat-Sheet & Shotlist
- [ ] Analyze final script structure
- [ ] Create beat-sheet (narrative beats)
- [ ] Generate shotlist with scene descriptions
- [ ] Produce `beats` and `shots` (JSON)
- [ ] Save to: `/scenes/json/{segment}/{age}/{title_id}_shots.json`

### 6.2 Subtitles (Draft from Script)
- [ ] Build SRT lines from final script
- [ ] Use logical phrasing (natural speech breaks)
- [ ] Estimate timing based on word count
- [ ] Save to: `/subtitles/srt/{segment}/{age}/{title_id}_draft.srt`
- [ ] Prepare for timing alignment in Step 8

## JSON Schema

### Shots JSON (`{title_id}_shots.json`)
```json
{
  "title_id": "uuid",
  "segment": "women|men",
  "age_bucket": "10-13|14-17|18-23",
  "final_title": "Title text",
  "total_duration_s": 55.0,
  "shots": [
    {
      "id": "shot-001",
      "sequence": 1,
      "text": "Hook line from script",
      "shot_description": "Visual description for this shot",
      "prompt": "SDXL prompt for keyframe generation",
      "duration_s": 6.0,
      "subtitle_ref": [1, 2],
      "beat": "hook",
      "camera_movement": "slow_zoom_in",
      "mood": "mysterious"
    },
    {
      "id": "shot-002",
      "sequence": 2,
      "text": "Story development line",
      "shot_description": "Visual description",
      "prompt": "SDXL prompt",
      "duration_s": 8.0,
      "subtitle_ref": [3, 4, 5],
      "beat": "build",
      "camera_movement": "static",
      "mood": "contemplative"
    }
  ],
  "beats": {
    "hook": {"shots": ["shot-001"], "duration_s": 6.0},
    "build": {"shots": ["shot-002", "shot-003"], "duration_s": 20.0},
    "climax": {"shots": ["shot-004", "shot-005"], "duration_s": 18.0},
    "resolution": {"shots": ["shot-006"], "duration_s": 11.0}
  }
}
```

## Draft SRT Format

```srt
1
00:00:00,000 --> 00:00:03,500
Hook line that grabs attention

2
00:00:03,500 --> 00:00:08,000
Next phrase continuing the story

3
00:00:08,000 --> 00:00:12,500
Building the narrative further
```

## Shot Planning Guidelines

### Duration per Shot
- **Hook shots:** 5-8 seconds
- **Build shots:** 6-10 seconds
- **Climax shots:** 8-12 seconds
- **Resolution shots:** 5-8 seconds

### Shot Count
- Target: 6-10 shots per 45-60 second video
- Minimum: 5 shots
- Maximum: 12 shots

### Visual Variety
- Mix of close-ups, medium, and wide shots
- Vary camera movements (static, zoom, pan)
- Consider transitions between shots

## Acceptance Criteria

- [ ] Shots JSON files exist for all 30 scripts
- [ ] Each shot has: id, text, description, prompt, duration, subtitle refs
- [ ] Total duration per video: 45-60 seconds
- [ ] Shots properly sequenced (1, 2, 3, ...)
- [ ] Beat structure included (hook, build, climax, resolution)
- [ ] Draft SRT files exist for all 30 scripts
- [ ] SRT timing estimates are reasonable
- [ ] Subtitle breaks follow natural speech patterns

## Related Files

- `/scenes/json/{segment}/{age}/` - Scene descriptions directory
- `/subtitles/srt/{segment}/{age}/` - Draft SRT files
- `/scripts/gpt_improved/{segment}/{age}/` - Final scripts (input)

## Microstep Validation

Use the MicrostepValidator for tracking:
- Step 14: scenes
- Step 12: subtitles_srt

Comment `@copilot check` when scene planning is complete.

## Notes

- SDXL prompts will be refined in Step 9
- Subtitle timing will be finalized in Step 8 after audio generation
- Consider 9:16 vertical format for shot composition
- Plan for safe text margins (top 8%, bottom 10%)
