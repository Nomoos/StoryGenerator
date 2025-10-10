# QC: Device Preview Testing

**ID:** `12-qc-01-device-preview`  
**Priority:** P1  
**Effort:** 2-3 hours  
**Status:** ❌ Not Implemented

## Overview

Generate device-specific preview renders to test video appearance on target platforms (iPhone, Android, various screen sizes). Validates safe zones, subtitle readability, and visual quality across devices.

**Implementation Needed:** Device preview generation service.

## Dependencies

**Requires:** `11-post-06` (final video with all post-production)  
**Blocks:** `12-qc-03` (QC report)

## Status

❌ **Not Implemented:** Device preview system not built

## Required Features

- Device-specific rendering (iPhone 14, Samsung Galaxy, etc.)
- Screen size adaptation testing
- Safe zone validation
- Subtitle readability checks
- Quality preview generation

## Acceptance Criteria

- [ ] Multiple device profiles supported
- [ ] Preview renders generated
- [ ] Safe zone overlay visualization
- [ ] Readability scoring
- [ ] Comparison view created
- [ ] Documentation updated

## Next Steps

- Implement device profile system
- Create preview renderer
- Add validation metrics
- `12-qc-02-sync-check`

**Output:** `data/Generator/qc/device_tests/{gender}/{age}/{title_id}/`
