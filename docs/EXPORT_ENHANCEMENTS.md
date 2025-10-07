# Export Enhancements - Complete Implementation Guide

## Overview

This guide covers all the export enhancements implemented for the StoryGenerator video pipeline:

1. **Export Registry System** - Track all exported videos with publish status and performance metrics
2. **Batch Export Processing** - Export multiple videos efficiently with progress tracking
3. **Custom Thumbnail Options** - Generate multiple thumbnail options and find best frames
4. **Platform-Specific Export** - Optimize metadata for YouTube, TikTok, and Instagram
5. **Analytics Integration** - Track export events and generate performance reports

## Features

### 1. Export Registry System

Track all exported videos with comprehensive metadata and performance tracking.

**Key Features:**
- Automatic registration of all exports
- Publish status tracking per platform
- Performance metrics (views, likes, shares, engagement)
- Statistical reports and analytics
- JSON-based storage for easy querying

**Usage:**

```python
from Tools.ExportRegistry import ExportRegistry

# Initialize registry
registry = ExportRegistry()

# Register an export
registry.register_export(
    title_id="abc12345",
    title="My Story",
    segment="women",
    age_group="18-23",
    video_path="/path/to/video.mp4",
    thumbnail_path="/path/to/thumb.jpg",
    metadata_path="/path/to/meta.json"
)

# Update publish status
registry.update_publish_status(
    "abc12345",
    platform="youtube",
    status="published",
    url="https://youtube.com/shorts/xyz"
)

# Update performance metrics
registry.update_performance(
    "abc12345",
    views=50000,
    likes=2500,
    shares=150
)

# Generate report
report = registry.generate_report()
print(report)
```

### 2. Batch Export Processing

Export multiple videos at once with parallel processing and error handling.

**Key Features:**
- Sequential or parallel processing
- Progress tracking with callbacks
- Error handling and retry logic
- Detailed batch summaries
- Automatic registry integration

**Usage:**

```python
from Tools.BatchExporter import BatchExporter

# Initialize batch exporter
exporter = BatchExporter(max_workers=4)

# Export multiple videos
results = exporter.export_batch(
    story_ideas=[story1, story2, story3],
    source_videos=["video1.mp4", "video2.mp4", "video3.mp4"],
    parallel=True,
    export_thumbnails=True,
    export_metadata=True
)

# Check results
print(f"Successful: {results['successful']}/{results['total']}")
print(f"Duration: {results['duration_seconds']}s")

# Retry failed exports
if results['failed'] > 0:
    retry_results = exporter.retry_failed(results, story_ideas, source_videos)
```

### 3. Custom Thumbnail Options

Generate multiple thumbnail options with frame analysis.

**Key Features:**
- Multiple timestamps selection
- Thumbnail grid generation (3x3, 4x4, etc.)
- Best frame detection using image analysis
- Brightness, sharpness, and contrast analysis
- Multiple output options for A/B testing

**Usage:**

```python
from Tools.ThumbnailGenerator import ThumbnailGenerator

# Initialize generator
generator = ThumbnailGenerator(1080, 1920)

# Generate thumbnails at specific timestamps
thumbnails = generator.generate_at_timestamps(
    "video.mp4",
    output_dir="thumbnails/",
    timestamps=[0.5, 2.0, 5.0, 10.0]
)

# Generate 3x3 grid
grid = generator.generate_grid(
    "video.mp4",
    "grid.jpg",
    grid_size=(3, 3)
)

# Find best frame automatically
best_frame = generator.find_best_frame(
    "video.mp4",
    "best_thumb.jpg",
    num_candidates=30,
    method="sharpness"  # or 'brightness', 'contrast'
)

# Generate multiple options for selection
options = generator.generate_multiple_options(
    "video.mp4",
    "thumbs/",
    title_id="abc123",
    num_options=5
)
```

### 4. Platform-Specific Export

Generate optimized metadata for each social media platform.

**Key Features:**
- Platform-specific hashtag strategies
- Character limit optimization
- Best practices integration
- Multi-platform export
- Platform configuration details

**Supported Platforms:**
- YouTube Shorts
- TikTok
- Instagram Reels

**Usage:**

```python
from Tools.PlatformExporter import PlatformExporter

# Initialize exporter
exporter = PlatformExporter()

# Generate YouTube-specific metadata
youtube_meta = exporter.generate_platform_metadata(
    story_idea,
    platform="youtube"
)

# Generate for all platforms
all_metadata = exporter.generate_all_platforms(story_idea)

# Save to files
platform_files = exporter.save_platform_metadata(
    story_idea,
    output_dir="platforms/"
)

# Get platform info
youtube_config = exporter.get_platform_info("youtube")
print(f"Max title length: {youtube_config['metadata_limits']['title']}")
```

### 5. Enhanced Video Compositor Integration

All features are integrated into the VideoCompositor for seamless workflow.

**Usage:**

```python
from Generators.GVideoCompositor import VideoCompositor

# Initialize compositor (includes all new tools)
compositor = VideoCompositor()

# Enhanced export with all features
result = compositor.export_with_enhancements(
    story_idea=story,
    source_video_path="final_video.mp4",
    generate_multiple_thumbnails=True,
    generate_platform_metadata=True,
    thumbnail_options=5,
    register_in_registry=True
)

# Check results
if result["success"]:
    print(f"Video: {result['video_path']}")
    print(f"Thumbnails: {len(result['thumbnails']['options'])} options")
    print(f"Platforms: {len(result['metadata']['platforms'])} configured")
```

## File Structure

```
data/final/{segment}/{age}/
├── {title_id}.mp4                          # Main video
├── {title_id}_thumbnail.jpg                # Default thumbnail
├── {title_id}_metadata.json                # Base metadata
├── thumbnails/                             # Multiple thumbnail options
│   ├── {title_id}_option1.jpg
│   ├── {title_id}_option2.jpg
│   └── ...
└── platforms/                              # Platform-specific metadata
    ├── {title_id}_youtube_metadata.json
    ├── {title_id}_tiktok_metadata.json
    └── {title_id}_instagram_metadata.json
```

## Registry File Structure

Located at: `data/final/export_registry.json`

```json
{
  "version": "1.0",
  "created_at": "2025-01-01T00:00:00",
  "last_updated": "2025-01-01T12:00:00",
  "total_exports": 10,
  "videos": {
    "abc12345": {
      "title": "Story Title",
      "title_id": "abc12345",
      "segment": "women",
      "age_group": "18-23",
      "export_date": "2025-01-01T10:00:00",
      "publish_status": "published",
      "platforms": {
        "youtube": {
          "status": "published",
          "url": "https://youtube.com/...",
          "published_date": "2025-01-01T11:00:00"
        }
      },
      "performance": {
        "views": 50000,
        "likes": 2500,
        "shares": 150,
        "engagement_rate": 5.3
      }
    }
  }
}
```

## Platform Metadata Structure

### YouTube Shorts

```json
{
  "platform": "youtube",
  "platform_title": "Story Title",
  "platform_description": "Full description with CTA",
  "platform_hashtags": ["#shorts", "#story", "#viral", "#theme", "#tone"],
  "platform_config": {
    "video_specs": {
      "max_duration": 60,
      "resolution": "1080x1920"
    },
    "metadata_limits": {
      "title": 100,
      "description": 5000
    }
  },
  "publishing_tips": [
    "First 3 seconds are crucial",
    "Add end screen with subscribe prompt"
  ]
}
```

### TikTok

```json
{
  "platform": "tiktok",
  "platform_title": "Story Title",
  "platform_description": "Engaging caption with trending hashtags",
  "platform_hashtags": [
    "#fyp", "#foryou", "#story", "#viral", 
    "#trending", "#storytime", "#theme"
  ],
  "hashtag_strategy": "aggressive"
}
```

### Instagram Reels

```json
{
  "platform": "instagram",
  "platform_title": "Story Title",
  "platform_description": "Visual description with emojis",
  "platform_hashtags": [
    "#reels", "#story", "#viral", "#explore",
    "#storytelling", "#instareels"
  ],
  "hashtag_strategy": "balanced"
}
```

## Best Practices

### Registry Management
1. **Regular Updates**: Update performance metrics daily or weekly
2. **Backup**: Regularly backup the registry JSON file
3. **Reports**: Generate monthly reports for analysis
4. **Filtering**: Use filters to track specific segments or age groups

### Batch Processing
1. **Parallel Workers**: Use 4-8 workers for optimal performance
2. **Error Handling**: Always check batch results and retry failures
3. **Progress Tracking**: Implement callbacks for long-running batches
4. **Resource Management**: Monitor CPU/memory usage with large batches

### Thumbnail Generation
1. **Multiple Options**: Generate 3-5 options for A/B testing
2. **Best Frame**: Use sharpness analysis for action videos, brightness for portraits
3. **Grid Previews**: Useful for reviewing video content
4. **Timing**: Extract thumbnails from key moments (0.5s, 25%, 50%, 75%)

### Platform Optimization
1. **Hashtags**: Use platform-specific strategies (aggressive for TikTok, moderate for YouTube)
2. **Descriptions**: Optimize for character limits and CTAs
3. **Testing**: A/B test different metadata variations
4. **Timing**: Post at platform-specific optimal times

## Examples

See the `examples/` directory for complete working examples:
- `example_export_registry.py` - Registry system usage
- `example_batch_export.py` - Batch processing examples
- More examples coming soon!

## Testing

Run comprehensive tests:

```bash
python3 tests/test_export_enhancements.py
```

All tests should pass (4/4):
- ✅ ExportRegistry
- ✅ ThumbnailGenerator
- ✅ PlatformExporter
- ✅ Integration

## Performance

### Export Times (Approximate)
- Standard export: ~2-5 seconds per video
- With thumbnails (5 options): +2-3 seconds
- With platform metadata (3 platforms): +1 second
- **Total enhanced export: ~5-10 seconds per video**

### Batch Processing
- Sequential (1 worker): ~10 seconds × N videos
- Parallel (4 workers): ~10 seconds × N/4 videos (with overhead)
- **Example**: 20 videos with 4 workers ≈ 60-70 seconds

## Troubleshooting

### Registry Issues
- **Problem**: Registry file locked or corrupted
- **Solution**: Check file permissions, backup and recreate if needed

### Batch Export Failures
- **Problem**: Some exports fail in batch
- **Solution**: Use `retry_failed()` method after fixing source issues

### Thumbnail Generation
- **Problem**: FFmpeg errors
- **Solution**: Ensure FFmpeg is installed and video files are valid

### Platform Metadata
- **Problem**: Hashtags not showing correctly
- **Solution**: Check platform limits and hashtag strategies

## API Reference

### ExportRegistry
- `register_export()` - Register new export
- `update_publish_status()` - Update platform publish status
- `update_performance()` - Update performance metrics
- `get_video_info()` - Get single video information
- `list_videos()` - List with optional filtering
- `get_statistics()` - Get overall statistics
- `generate_report()` - Generate text report

### BatchExporter
- `export_batch()` - Batch export with options
- `retry_failed()` - Retry failed exports
- `_export_single()` - Internal single export method

### ThumbnailGenerator
- `generate_at_timestamps()` - Generate at specific times
- `generate_grid()` - Create thumbnail grid
- `find_best_frame()` - Auto-select best frame
- `generate_multiple_options()` - Create multiple options

### PlatformExporter
- `generate_platform_metadata()` - Single platform
- `generate_all_platforms()` - All platforms
- `save_platform_metadata()` - Save to files
- `get_platform_info()` - Get platform configuration
- `list_platforms()` - List supported platforms

## Support

For issues or questions:
1. Check this documentation
2. Review example files
3. Run tests to verify installation
4. Check GitHub issues for known problems

## License

See project LICENSE file.
