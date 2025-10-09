# Distribution: Batch Export and Platform Optimization

**ID:** `distribution-batch-export`  
**Priority:** P2  
**Effort:** 6-10 hours  
**Status:** Not Started

## Overview

Implement batch export capabilities and platform-specific optimization for distributing videos to multiple social media platforms efficiently. This includes:

1. **Batch Exporter** - Export multiple videos in a single operation
2. **Platform Exporter** - Platform-specific format optimization (TikTok, YouTube Shorts, Instagram Reels, Facebook)
3. **Export Registry** - Track export status, metadata, and distribution history

This functionality was present in the obsolete Python implementation (`BatchExporter.py`, `PlatformExporter.py`, `ExportRegistry.py`) and is essential for efficient content distribution.

## Dependencies

**Requires:**
- `13-export-01-final-encode` (Final video encoding)
- `13-export-02-thumbnail` (Thumbnail generation)
- `13-export-03-metadata` (Metadata generation)

**Blocks:**
- `14-dist-01-youtube-upload`
- `14-dist-02-tiktok-upload`
- `14-dist-03-instagram-upload`
- `14-dist-04-facebook-upload`

## Acceptance Criteria

- [ ] Batch export multiple videos in one operation
- [ ] Platform-specific video optimization (resolution, bitrate, format)
- [ ] Platform-specific metadata formatting
- [ ] Export registry with tracking
- [ ] Duplicate detection (avoid re-exporting)
- [ ] Export status reporting
- [ ] Error handling and retry logic
- [ ] CLI commands for batch operations
- [ ] Documentation with examples
- [ ] Unit and integration tests

## Platform Specifications

| Platform | Resolution | Max Duration | Max File Size | Bitrate | Format |
|----------|-----------|--------------|---------------|---------|--------|
| YouTube Shorts | 1080x1920 | 60s | 256 MB | 8 Mbps | H.264 |
| TikTok | 1080x1920 | 60s | 287 MB | 6 Mbps | H.264 |
| Instagram Reels | 1080x1920 | 90s | 250 MB | 8 Mbps | H.264 |
| Facebook Reels | 1080x1920 | 90s | 250 MB | 8 Mbps | H.264 |

## Storage Structure

```
data/exports/
├── registry.json
└── {segment}/
    └── {age}/
        └── {title_id}/
            ├── youtube.mp4
            ├── tiktok.mp4
            ├── instagram.mp4
            └── metadata_youtube.json
```

## CLI Commands

```bash
# Export single video to all platforms
dotnet run --project CLI -- export --title "my-story" --platforms "youtube,tiktok,instagram"

# Batch export multiple videos
dotnet run --project CLI -- export-batch --segment women --age 18-23 --platforms "youtube,tiktok"
```

## Related Documentation

- `obsolete/Python/Tools/BatchExporter.py` - Original batch export
- `obsolete/Python/Tools/PlatformExporter.py` - Platform optimization
- `obsolete/Python/Tools/ExportRegistry.py` - Export tracking
- `docs/VIDEO_EXPORT.md` - Current export documentation

## Definition of Done

- [ ] Batch exporter implemented and tested
- [ ] Platform-specific optimizations working
- [ ] Export registry tracking exports
- [ ] CLI commands functional
- [ ] Documentation complete
- [ ] Tests passing
- [ ] Code reviewed and merged
