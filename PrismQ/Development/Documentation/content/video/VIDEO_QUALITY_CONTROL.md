# Video Quality Control (QC) Documentation

## Overview

The Video Quality Checker is an automated system for validating final video output in the StoryGenerator pipeline. It performs comprehensive checks on video files and generates detailed quality control reports saved as JSON files.

## Features

- **7 Comprehensive Quality Checks**:
  1. File Properties - Validates file existence and size
  2. Codec & Format - Verifies H.264 codec and MP4 format
  3. Resolution & Legibility - Checks 1080x1920 vertical format
  4. Bitrate Analysis - Validates video and audio bitrate
  5. File Size - Ensures reasonable file size for duration
  6. A/V Sync - Verifies audio/video synchronization
  7. Duration - Validates video length

- **Quality Scoring**: Each video receives a 0-100 quality score
- **Detailed Reports**: JSON reports with pass/fail status for each check
- **Automatic Integration**: Runs automatically after video composition
- **Batch Processing**: Check multiple videos in a directory

## Quality Standards

### Target Video Specifications

| Property | Target Value | Minimum | Maximum |
|----------|-------------|---------|---------|
| Resolution | 1080x1920 (9:16) | 720x1280 | - |
| Video Codec | H.264 (libx264) | - | - |
| Audio Codec | AAC | - | - |
| Video Bitrate | 8000 kbps | 2000 kbps | - |
| Audio Bitrate | 192 kbps | 128 kbps | - |
| Frame Rate | 30 fps | 24 fps | - |
| File Size | - | 1 MB | 100 MB |
| Duration | - | 5 seconds | 180 seconds |
| A/V Sync | ±0.0s | - | ±0.5s |

## Usage

### 1. Automatic Integration (Recommended)

Quality checks run automatically when using `VideoCompositor`:

```python
from Generators.GVideoCompositor import VideoCompositor

# Initialize with quality checks enabled (default)
compositor = VideoCompositor(perform_quality_check=True)

# Compose video - quality check runs automatically
video_path = compositor.compose_final_video(story_idea)

# QC report is saved to {video_directory}/{title_id}_qc.json
```

To disable automatic quality checks:

```python
compositor = VideoCompositor(perform_quality_check=False)
```

### 2. Standalone CLI Tool

Use the standalone script to check existing videos:

```bash
# Check a single video
python scripts/check_video_quality.py /path/to/video.mp4

# Check all videos in a directory
python scripts/check_video_quality.py /final/men/25-34/

# Check with custom title ID
python scripts/check_video_quality.py video.mp4 --title-id my_title_001

# Check without saving report
python scripts/check_video_quality.py video.mp4 --no-save

# Save report to custom directory
python scripts/check_video_quality.py video.mp4 --output-dir /custom/path/

# Batch process with custom pattern
python scripts/check_video_quality.py /videos/ --pattern "*.mp4"
```

### 3. Programmatic Usage

Direct API usage in Python code:

```python
from Tools.VideoQualityChecker import VideoQualityChecker

# Initialize checker
checker = VideoQualityChecker()

# Perform quality check
passed, report = checker.check_video_quality(
    video_path="/path/to/video.mp4",
    title_id="my_story_title",
    save_report=True,
    output_dir="/custom/output/dir"  # Optional
)

# Check results
if passed:
    print(f"✅ Quality check passed! Score: {report['quality_score']}/100")
else:
    print(f"❌ Quality issues detected. Score: {report['quality_score']}/100")

# Access individual check results
for check_name, check_data in report['checks'].items():
    print(f"{check_name}: {'PASSED' if check_data['passed'] else 'FAILED'}")
    print(f"  Message: {check_data['message']}")
```

## QC Report Structure

Quality check reports are saved as JSON files with the following structure:

```json
{
  "video_path": "/final/men/25-34/my_story_title.mp4",
  "title_id": "my_story_title",
  "checked_at": "2025-10-07T20:00:00.000000",
  "overall_status": "passed",
  "quality_score": 95,
  "checks_passed": 7,
  "checks_total": 7,
  "pass_rate": 100.0,
  "report_path": "/final/men/25-34/my_story_title_qc.json",
  "checks": {
    "file_properties": {
      "name": "File Properties",
      "passed": true,
      "message": "File exists (15.0 MB)",
      "details": {
        "file_exists": true,
        "size_bytes": 15728640,
        "size_mb": 15.0
      }
    },
    "codec_format": {
      "name": "Codec & Format",
      "passed": true,
      "message": "Using recommended codec: h264",
      "details": {
        "format": "mp4",
        "video_codec": "h264",
        "audio_codec": "aac",
        "pixel_format": "yuv420p"
      }
    },
    "resolution_legibility": {
      "name": "Resolution & Legibility",
      "passed": true,
      "message": "Perfect resolution: 1080x1920",
      "details": {
        "width": 1080,
        "height": 1920,
        "resolution": "1080x1920",
        "aspect_ratio": 0.56,
        "fps": 30.0,
        "fps_status": "good"
      }
    },
    "bitrate": {
      "name": "Bitrate Analysis",
      "passed": true,
      "message": "Good video bitrate: 8000.0 kbps",
      "details": {
        "overall_bitrate_kbps": 8192.0,
        "video_bitrate_kbps": 8000.0,
        "audio_bitrate_kbps": 192.0
      }
    },
    "file_size": {
      "name": "File Size",
      "passed": true,
      "message": "File size acceptable: 15.0 MB",
      "details": {
        "size_mb": 15.0,
        "min_size_mb": 1.0,
        "max_size_mb": 100.0
      }
    },
    "av_sync": {
      "name": "Audio/Video Sync",
      "passed": true,
      "message": "Audio/video in sync (diff: 0.02s)",
      "details": {
        "video_duration": 60.05,
        "audio_duration": 60.03,
        "sync_difference": 0.02
      }
    },
    "duration": {
      "name": "Duration",
      "passed": true,
      "message": "Duration acceptable: 60.05s",
      "details": {
        "duration_seconds": 60.05,
        "duration_formatted": "1m 0s"
      }
    }
  }
}
```

## Report File Locations

QC reports are saved with the naming pattern: `{title_id}_qc.json`

### Default Locations

1. **Same directory as video file** (default)
   ```
   /path/to/video/my_video.mp4
   /path/to/video/my_video_qc.json
   ```

2. **Organized by segment/age** (recommended for production)
   ```
   /final/men/25-34/story_title.mp4
   /final/men/25-34/story_title_qc.json
   ```

3. **Custom directory** (via `output_dir` parameter)
   ```python
   checker.check_video_quality(
       video_path="/path/to/video.mp4",
       output_dir="/custom/qc/reports/"
   )
   ```

## Quality Scoring

The quality score (0-100) is calculated based on weighted checks:

| Check | Weight | Description |
|-------|--------|-------------|
| File Properties | 10% | Basic file validation |
| Codec & Format | 15% | Proper codec usage |
| Resolution | 20% | Target resolution match |
| Bitrate | 20% | Sufficient quality bitrate |
| File Size | 15% | Reasonable file size |
| A/V Sync | 10% | Audio/video synchronization |
| Duration | 10% | Acceptable video length |

### Score Interpretation

- **90-100**: Excellent - Production ready
- **80-89**: Good - Minor issues, acceptable
- **70-79**: Fair - Some issues, review recommended
- **60-69**: Poor - Multiple issues, re-encode recommended
- **Below 60**: Failed - Significant issues, must fix

## Troubleshooting

### Common Issues

#### 1. Low Quality Score

**Symptoms**: Score below 70
**Possible Causes**:
- Wrong codec (not H.264)
- Low bitrate (below 2000 kbps)
- Wrong resolution (not 1080x1920)
- A/V sync issues

**Solutions**:
- Re-encode with proper settings
- Use VideoCompositor default settings
- Check source material quality

#### 2. A/V Sync Failures

**Symptoms**: Audio/video out of sync check fails
**Possible Causes**:
- Audio file duration mismatch
- Frame rate issues
- Encoding errors

**Solutions**:
- Re-generate with matching audio/video durations
- Verify source audio file integrity
- Use consistent frame rate (30 fps)

#### 3. File Size Issues

**Symptoms**: File too small or too large
**Possible Causes**:
- Bitrate too low/high
- Duration mismatch
- Wrong compression settings

**Solutions**:
- Adjust target bitrate
- Check video duration
- Use recommended encoding settings

## Integration with Video Pipeline

The quality checker integrates seamlessly with the existing video pipeline:

```
Story Idea → Script → Voice → Subtitles → Video Segments → 
Final Video → Quality Check → QC Report
```

### Pipeline Flow

1. **Video Composition**: `VideoCompositor.compose_final_video()`
   - Concatenates video segments
   - Adds audio and subtitles
   - Creates final video file

2. **Quality Check** (automatic if enabled):
   - Analyzes final video file
   - Performs all 7 quality checks
   - Calculates quality score

3. **Report Generation**:
   - Creates JSON report
   - Saves to appropriate location
   - Logs summary to console

4. **Result Handling**:
   - Returns video path regardless of QC result
   - QC warnings don't stop pipeline
   - Reports available for review

## Best Practices

1. **Always Enable QC**: Keep `perform_quality_check=True` in production
2. **Review Failed Reports**: Investigate videos with scores below 80
3. **Archive QC Reports**: Keep reports with final videos for audit trail
4. **Batch Process**: Use CLI tool to check multiple videos efficiently
5. **Monitor Trends**: Track quality scores over time to identify issues
6. **Set Up Alerts**: Notify team when quality scores drop

## Examples

See `examples/demo_quality_checker.py` for:
- Sample perfect quality report (100/100 score)
- Sample failed quality report (42/100 score)
- Usage examples and code snippets
- Complete demonstration

Run the demo:
```bash
python examples/demo_quality_checker.py
```

## Testing

Run the quality checker test suite:

```bash
# Run all tests
python tests/test_quality_checker.py

# Expected output:
# ✅ Basic Functionality tests passed
# ✅ Quality Thresholds tests passed
# ✅ Sample Video tests passed
# Total: 3/3 tests passed
```

## API Reference

### VideoQualityChecker Class

```python
class VideoQualityChecker:
    """Perform quality checks on final videos."""
    
    def check_video_quality(
        self,
        video_path: str,
        title_id: Optional[str] = None,
        save_report: bool = True,
        output_dir: Optional[str] = None
    ) -> Tuple[bool, Dict[str, Any]]:
        """
        Perform comprehensive quality check.
        
        Args:
            video_path: Path to video file
            title_id: Optional title ID for report
            save_report: Whether to save JSON report
            output_dir: Custom output directory
            
        Returns:
            Tuple of (passed, qc_report_dict)
        """
```

### Configuration Options

All thresholds are configurable via class attributes:

```python
checker = VideoQualityChecker()

# Customize thresholds
checker.MIN_VIDEO_SIZE_MB = 2.0
checker.MAX_VIDEO_SIZE_MB = 50.0
checker.TARGET_RESOLUTION = (1920, 1080)
checker.MIN_BITRATE_KBPS = 3000
```

## Future Enhancements

Planned improvements:
- [ ] Visual quality analysis (blur detection, artifacts)
- [ ] Subtitle legibility checks (contrast, size)
- [ ] Frame-by-frame analysis for issues
- [ ] Automated re-encoding for failed videos
- [ ] Quality trend dashboard
- [ ] Email/Slack notifications for failures
- [ ] Integration with publishing workflow

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Review existing quality reports for patterns
3. Run the demo script for examples
4. Check test suite for expected behavior

---

**Last Updated**: 2025-10-07  
**Version**: 1.0.0  
**Status**: Production Ready ✅
