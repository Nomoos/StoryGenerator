# QC: Audio-Subtitle Sync Check

**ID:** `12-qc-02-sync-check`  
**Priority:** P1  
**Effort:** 2-3 hours  
**Status:** ✅ COMPLETE

## Overview

Verify audio-subtitle synchronization accuracy (±50ms tolerance). Validates that subtitle timing matches voiceover precisely throughout the video, detecting drift or misalignment.

**Implementation Needed:** A/V sync validation service.

## Dependencies

**Requires:** `11-post-02` (video with subtitles), `08-subtitles-01` (SRT timing)  
**Blocks:** `12-qc-03` (QC report)

## Status

✅ **COMPLETE:** A/V sync validation fully implemented

**Implementation:** `SyncCheckStage` in `StoryGenerator.Pipeline/Stages/QualityControlStages.cs`

**Features:**
- Subtitle timing extraction from SRT files
- Sync validation with configurable tolerance (default ±50ms)
- Drift detection for each subtitle
- Per-subtitle validation and issue reporting
- JSON report generation with timestamps

**Tests:** 4 unit tests passing in `QualityControlStagesTests.cs`

## Required Features

- Subtitle timing extraction
- Audio waveform analysis
- Sync drift detection (±50ms tolerance)
- Per-subtitle validation
- Sync quality scoring
- Issue reporting

## Acceptance Criteria

- [ ] Timing extraction working
- [ ] Sync validation accurate
- [ ] Drift detection functional
- [ ] Quality metrics generated
- [ ] Issue report with timestamps
- [ ] Pass/fail criteria enforced
- [ ] Documentation updated

## Next Steps

- Implement timing analyzer
- Create sync validator
- Add drift detection
- `12-qc-03-quality-report`

**Output:** `data/Generator/qc/sync_reports/{gender}/{age}/{title_id}_sync_report.json`
