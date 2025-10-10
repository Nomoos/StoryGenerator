# Audio: LUFS Normalization

**ID:** `07-audio-02-normalization`  
**Priority:** P1  
**Effort:** 2-3 hours  
**Status:** ✅ COMPLETE

## Overview

Normalize audio to standard LUFS levels (-14.0 for YouTube/TikTok) for consistent loudness across all videos. Uses two-pass normalization for accuracy and validates output meets targets.

**Implementation:** `AudioNormalizationStage` in `StoryGenerator.Pipeline/Stages/AudioProductionStages.cs`

## Status

✅ **COMPLETE:** Audio normalization fully implemented

**Features:**
- LUFS normalization to -14.0 (configurable)
- Two-pass normalization for better accuracy
- Input/output LUFS measurement
- Target validation (±1.0 LUFS tolerance)
- Loudness range (LRA) and true peak (TP) control

**Tests:** 5 unit tests passing in `AudioProductionStagesTests.cs`

## Dependencies

**Requires:**
- `07-audio-01` - TTS generated audio
- `01-research-03` - FFmpeg integration

**Blocks:**
- `08-subtitles-01` - Subtitle alignment needs normalized audio
- `11-post-01` - Post-production needs final audio

## Acceptance Criteria

- [x] Audio normalization stage implemented
- [x] LUFS measurement functionality
- [x] Two-pass normalization support
- [x] Target validation (±1.0 LUFS tolerance)
- [x] Output directory structure created
- [x] Documentation updated
- [x] Tests passing (5 tests)
- [x] Code reviewed and merged

## Task Details

### Implementation

[TODO: Add implementation details, code examples, schemas]

### Testing

```bash
# Add test commands
```

## Output Files

- `data/Generator/audio/normalized/{gender}/{age}/{title_id}.mp3` - Normalized audio at -14.0 LUFS

## Related Files

- [List related source files or docs]

## Notes

- [Add any important notes or considerations]

## Next Steps

After completion:
- [List tasks that can proceed]
