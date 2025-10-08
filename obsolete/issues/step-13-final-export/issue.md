# Step 13: Final Export

**Status:** Not Started  
**Priority:** High  
**Dependencies:** Step 12 (Quality Checks Passed)

## Overview

Export final production-ready videos with metadata, thumbnails, and platform-specific optimizations.

## Target Audience
- Segments: `women/{age}` and `men/{age}`
- Age buckets: `10-13`, `14-17`, `18-23`
- Export all 30 quality-approved videos

## Checklist

### 13.1 Final Video Export
- [ ] Take QC-approved draft videos
- [ ] Apply any last-minute fixes from QC
- [ ] Export final version with optimal settings
- [ ] Save to: `/final/{segment}/{age}/{title_id}.mp4`
- [ ] Verify file integrity (not corrupted)
- [ ] Calculate file checksums (MD5/SHA256)

### 13.2 Thumbnail Generation
- [ ] Extract frame at 3 seconds (or best representative frame)
- [ ] Generate 1080×1920 thumbnail
- [ ] Apply thumbnail overlay/branding (optional)
- [ ] Save as PNG: `/final/{segment}/{age}/{title_id}_thumbnail.png`
- [ ] Create platform-specific thumbnails if needed
  - YouTube Shorts: 1080×1920
  - Instagram: 1080×1920
  - TikTok: 1080×1920

### 13.3 Metadata Generation
- [ ] Compile final metadata JSON
- [ ] Include: title, description, tags, category
- [ ] Add segment and age bucket information
- [ ] Include all technical specifications
- [ ] Save to: `/final/{segment}/{age}/{title_id}_metadata.json`

### 13.4 Platform-Specific Preparation
- [ ] Validate filenames (platform-safe, no special chars)
- [ ] Check file size limits per platform
- [ ] Prepare description templates per platform
- [ ] Generate hashtag suggestions
- [ ] Create scheduling recommendations

## Final Export Specifications

### Video Settings (Final)
```
Container: MP4
Video Codec: H.264 (libx264)
Profile: High
Level: 4.1
Resolution: 1080×1920 (9:16)
Frame Rate: 30 fps
Pixel Format: yuv420p
Color Space: bt709
Bitrate: 10-12 Mbps (VBR)
CRF: 20 (high quality)

Audio Codec: AAC
Bitrate: 192 kbps
Sample Rate: 48000 Hz
Channels: Stereo (2)

Optimization:
- movflags +faststart (web streaming)
- Two-pass encoding (optional, better quality)
```

## Metadata Schema

### Final Metadata (`{title_id}_metadata.json`)
```json
{
  "video": {
    "id": "uuid",
    "title": "Final Video Title",
    "file": "{title_id}.mp4",
    "thumbnail": "{title_id}_thumbnail.png",
    "segment": "women|men",
    "age_bucket": "10-13|14-17|18-23",
    "duration_s": 52.3,
    "created_at": "2024-01-01T12:00:00Z",
    "checksum_md5": "abc123...",
    "checksum_sha256": "def456..."
  },
  "content": {
    "title": "Engaging Video Title Here",
    "description": "Compelling description that hooks viewers and provides context...",
    "tags": [
      "story", "mystery", "women", "young_adult",
      "shorts", "viral", "trending"
    ],
    "category": "Entertainment",
    "language": "en",
    "age_rating": "General|Teen|Young Adult"
  },
  "technical": {
    "resolution": "1080x1920",
    "aspect_ratio": "9:16",
    "fps": 30,
    "codec": "h264",
    "audio_codec": "aac",
    "bitrate_mbps": 10.5,
    "file_size_mb": 68.7,
    "has_subtitles": true,
    "has_audio": true
  },
  "platform_info": {
    "youtube_shorts": {
      "compatible": true,
      "optimal": true,
      "description": "Platform-specific description...",
      "hashtags": ["#Shorts", "#Story", "#Mystery"]
    },
    "instagram_reels": {
      "compatible": true,
      "optimal": true,
      "caption": "Hook caption for Instagram...",
      "hashtags": ["#Reels", "#Story", "#Viral"]
    },
    "tiktok": {
      "compatible": true,
      "optimal": true,
      "caption": "TikTok-optimized caption...",
      "hashtags": ["#FYP", "#Story", "#Trending"]
    }
  },
  "production": {
    "script_version": "v2",
    "title_version": "improved",
    "voice_gender": "female|male",
    "num_shots": 7,
    "generation_method": "ltx_video|interpolation",
    "total_production_time_hours": 2.3
  },
  "performance": {
    "viral_score": 85,
    "predicted_views": "10k-50k",
    "target_ctr": "5-8%",
    "target_retention": "60-70%"
  }
}
```

## Description Templates

### Template Structure
```
[Hook - First Line]
[2-3 sentences expanding on the story]
[Call-to-action]

#hashtag1 #hashtag2 #hashtag3

---
Target Audience: [Women/Men, Age X-Y]
Genre: [Mystery/Drama/etc.]
```

### Example
```
What if everything you knew was a lie?

This story follows someone who discovers a hidden truth that changes everything. Watch to see how it all unfolds in just 60 seconds.

Like and follow for more stories!

#Shorts #Story #Mystery #MustWatch

---
Target Audience: Women, Age 18-23
Genre: Mystery/Drama
```

## Hashtag Guidelines

### Per Platform
**YouTube Shorts:**
- #Shorts (required)
- 2-3 content tags
- 1-2 trending tags

**Instagram Reels:**
- #Reels (recommended)
- 5-10 relevant tags
- Mix popular + niche

**TikTok:**
- #FYP or #ForYou
- 3-5 content tags
- Trending sounds/tags

## File Organization

### Final Structure
```
/final/{segment}/{age}/
├── {title_id}.mp4                    # Final video
├── {title_id}_thumbnail.png          # Main thumbnail
├── {title_id}_metadata.json          # Complete metadata
├── {title_id}_qc.json               # Quality check report
└── {title_id}_draft.mp4             # Keep draft for reference
```

## Acceptance Criteria

- [ ] All 30 final videos exported
- [ ] File format: 1080×1920, 30fps, H.264, AAC
- [ ] File sizes: 50-100MB per video
- [ ] All thumbnails generated (1080×1920 PNG)
- [ ] Metadata JSON files created for all videos
- [ ] Checksums calculated for all videos
- [ ] Platform descriptions prepared
- [ ] Hashtags selected per platform
- [ ] All files organized in final directory structure
- [ ] Final verification: playback test on mobile device
- [ ] Ready for upload to platforms

## Verification Steps

### Final Checks (Per Video)
1. [ ] Play video start-to-end (no corruption)
2. [ ] Verify thumbnail loads correctly
3. [ ] Read metadata JSON (valid structure)
4. [ ] Check file size reasonable
5. [ ] Verify checksum matches
6. [ ] Test on one target platform (upload test)

## Related Files

- `/final/{segment}/{age}/` - Final output directory
- `/config/pipeline.yaml` - Export configuration
- `/docs/VIDEO_EXPORT.md` - Export guidelines

## Microstep Validation

Use the MicrostepValidator for tracking:
- Step 19: final (export complete)

Comment `@copilot check` when final export is complete.

## Notes

- Keep draft versions for comparison/rollback
- Store original quality versions (before platform compression)
- Consider batch upload tools for efficiency
- Document upload dates and platform-specific optimizations
- Total final output: ~2-3GB (30 videos + thumbnails + metadata)
- Archive project files after successful upload
- Create backup of final directory

## Next Steps After Export

1. Upload to platforms (YouTube, Instagram, TikTok)
2. Schedule releases (optimal posting times)
3. Monitor performance (views, engagement, retention)
4. A/B test different titles/thumbnails
5. Analyze results for future improvements
6. Document lessons learned
