# Step 12: Quality Checks

**Status:** Not Started  
**Priority:** High  
**Dependencies:** Step 11 (Post-Production Draft Videos)

## Overview

Perform comprehensive quality checks on all draft videos to ensure they meet platform standards and user experience requirements.

## Target Audience
- Segments: `women/{age}` and `men/{age}`
- Age buckets: `10-13`, `14-17`, `18-23`
- Check all 30 draft videos

## Checklist

### 12.1 Phone Preview
- [ ] Test on **iOS devices** (iPhone)
  - Test on iPhone 12 or newer
  - Check portrait orientation
  - Verify playback smoothness
- [ ] Test on **Android devices**
  - Test on Samsung/Pixel devices
  - Check portrait orientation
  - Verify playback smoothness
- [ ] Document preview results per video

### 12.2 Subtitle Legibility
- [ ] Check **font size** (60-80px range)
  - Readable from 12-18 inches
  - Test on 6-7 inch screens
- [ ] Verify **contrast** (white text on varied backgrounds)
  - Outline/shadow visibility
  - Background box effectiveness
- [ ] Confirm **safe margins** respected
  - Top: 8% clear
  - Bottom: 10% clear
- [ ] Test **character limit** (≤42 chars per subtitle)

### 12.3 Audio-Video Sync
- [ ] Verify **subtitles match voiceover**
  - Word-level alignment
  - No drift over duration
  - Proper timing on key phrases
- [ ] Check **lip-sync** (if characters speaking)
- [ ] Validate **audio clarity**
  - No clipping or distortion
  - Proper -14 LUFS level
  - BGM not overpowering VO

### 12.4 Technical Specifications
- [ ] Verify **file size** reasonable (50-100MB)
- [ ] Confirm **codec**: H.264
- [ ] Check **pixel format**: yuv420p
- [ ] Validate **bitrate**: 8-12 Mbps
- [ ] Ensure **resolution**: 1080×1920
- [ ] Verify **fps**: 30
- [ ] Check **duration**: 45-60 seconds

### 12.5 Content Quality
- [ ] Verify **visual quality**
  - No artifacts or compression issues
  - Consistent color grading
  - Smooth transitions
- [ ] Check **narrative flow**
  - Story makes sense
  - Pacing appropriate
  - Clear message
- [ ] Validate **age-appropriateness**
  - Content suitable for target age
  - No inappropriate imagery
  - Language appropriate

### 12.6 Platform Compatibility
- [ ] Test **YouTube Shorts** compatibility
  - Aspect ratio: 9:16 ✓
  - Max duration: 60 seconds ✓
  - Vertical orientation ✓
- [ ] Test **Instagram Reels** compatibility
  - Aspect ratio: 9:16 ✓
  - Max duration: 90 seconds ✓
- [ ] Test **TikTok** compatibility
  - Aspect ratio: 9:16 ✓
  - Max duration: 60 seconds ✓

### 12.7 Generate QC Report
- [ ] Create quality check report per video
- [ ] Save to: `/final/{segment}/{age}/{title_id}_qc.json`
- [ ] Include pass/fail status per check
- [ ] Document any issues found
- [ ] Provide remediation suggestions

## QC Report Schema

### Format (`{title_id}_qc.json`)
```json
{
  "title_id": "uuid",
  "segment": "women|men",
  "age_bucket": "10-13|14-17|18-23",
  "video_file": "{title_id}_draft.mp4",
  "qc_timestamp": "2024-01-01T12:00:00Z",
  "checks": {
    "phone_preview": {
      "status": "pass",
      "ios": {"tested": true, "device": "iPhone 13", "result": "pass"},
      "android": {"tested": true, "device": "Pixel 6", "result": "pass"}
    },
    "subtitle_legibility": {
      "status": "pass",
      "font_size": {"value": 70, "status": "pass"},
      "contrast": {"status": "pass", "notes": "Good visibility"},
      "margins": {"top": "pass", "bottom": "pass"},
      "char_limit": {"max_found": 38, "status": "pass"}
    },
    "sync": {
      "status": "pass",
      "subtitle_vo_sync": {"status": "pass", "max_drift_ms": 50},
      "audio_clarity": {"status": "pass", "lufs": -14.2}
    },
    "technical_specs": {
      "status": "pass",
      "file_size_mb": 68.7,
      "codec": "h264",
      "pixel_format": "yuv420p",
      "bitrate_mbps": 10.5,
      "resolution": "1080x1920",
      "fps": 30,
      "duration_s": 52.3
    },
    "content_quality": {
      "status": "pass",
      "visual_quality": {"status": "pass", "artifacts": false},
      "narrative_flow": {"status": "pass", "score": 8.5},
      "age_appropriate": {"status": "pass", "verified": true}
    },
    "platform_compatibility": {
      "youtube_shorts": "pass",
      "instagram_reels": "pass",
      "tiktok": "pass"
    }
  },
  "overall_status": "pass",
  "issues_found": [],
  "remediation_required": false,
  "approved_for_export": true,
  "qc_notes": "All checks passed. Ready for final export."
}
```

## Failure Criteria

### Critical Issues (Must Fix)
- Audio-video sync drift > 200ms
- Subtitles unreadable on mobile
- Codec incompatible with platforms
- Duration exceeds 60 seconds
- Age-inappropriate content

### Major Issues (Should Fix)
- File size > 150MB
- Subtitle overlap or gaps
- Poor color consistency
- Compression artifacts visible
- Audio levels incorrect

### Minor Issues (Nice to Fix)
- Transition timing slightly off
- BGM volume could be adjusted
- Thumbnail could be better
- Minor subtitle formatting

## Testing Checklist

### Per Video
- [ ] Play full video on iOS device
- [ ] Play full video on Android device
- [ ] Check first 3 seconds (hook effectiveness)
- [ ] Check mid-point (retention)
- [ ] Check ending (CTA clarity)
- [ ] Verify subtitle timing at 3 random points
- [ ] Test audio with headphones
- [ ] Test audio with phone speaker
- [ ] Check file properties with MediaInfo

## Acceptance Criteria

- [ ] All 30 videos tested on iOS device
- [ ] All 30 videos tested on Android device
- [ ] QC reports generated for all videos
- [ ] All critical issues identified and documented
- [ ] Videos marked as "pass" or "needs_remediation"
- [ ] Remediation plan created for failed videos
- [ ] At least 90% of videos pass all checks
- [ ] Platform compatibility verified for all

## Related Files

- `/final/{segment}/{age}/` - Draft videos and QC reports
- `/scripts/check_video_quality.py` - Automated QC script (if available)
- `/docs/VIDEO_QUALITY_CONTROL.md` - QC guidelines documentation

## Microstep Validation

Use the MicrostepValidator for tracking:
- Step 19: final (QC stage)

Comment `@copilot check` when quality checks are complete.

## Notes

- Use MediaInfo CLI for technical spec validation
- Create automated QC script for batch processing
- Manual review still required for content quality
- Document device models used for testing
- Total testing time: ~3-5 hours for 30 videos
- Re-test after any remediation work
