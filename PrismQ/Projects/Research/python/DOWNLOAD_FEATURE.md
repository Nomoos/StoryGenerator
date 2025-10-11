# YouTube Channel Scraper - Download Feature

## Overview

The YouTube Channel Scraper now supports automatic downloading of high-view shorts. This feature allows you to identify and download viral content from YouTube channels for analysis or reference.

## Feature: Download High-View Shorts

### What It Does

When enabled, the scraper will automatically download any shorts that exceed a specified view threshold (default: 10 million views). This is useful for:

- **Content Analysis**: Study successful viral shorts
- **Trend Research**: Analyze what makes high-performing content
- **Reference Material**: Keep copies of successful shorts for inspiration
- **Data Collection**: Build a dataset of high-performing content

### How to Use

#### Basic Usage

Download shorts with over 10 million views:

```bash
python youtube_channel_scraper.py @channelname --top 20 --download-high-views
```

#### Custom View Threshold

Download shorts with over 5 million views:

```bash
python youtube_channel_scraper.py @channelname --top 20 --download-high-views --view-threshold 5000000
```

#### Combined with Story Filtering

Download only story videos with high views:

```bash
python youtube_channel_scraper.py @channelname --top 20 --story-only --download-high-views
```

### Command Line Arguments

| Argument | Type | Default | Description |
|----------|------|---------|-------------|
| `--download-high-views` | flag | disabled | Enable downloading of high-view shorts |
| `--view-threshold` | integer | 10000000 | Minimum view count to download (10 million by default) |

### Output Structure

When downloads are enabled, the scraper creates a `downloads/` subdirectory within the channel-specific output folder:

```
/tmp/youtube_channel_data/
└── {channel_id}_{channel_name}/
    ├── channel_report.md           # Comprehensive report with download info
    ├── channel_data.json            # JSON data with download statistics
    ├── channel_data_summary.md      # Markdown summary
    ├── downloads/                   # Downloaded videos (when enabled)
    │   ├── {video_id1}.mp4
    │   ├── {video_id2}.mp4
    │   └── ...
    ├── {video_id}.info.json         # Video metadata
    ├── {video_id}.info.md           # Video metadata (markdown)
    └── {video_id}.srt               # Subtitles (when available)
```

### Report Information

The generated report includes download statistics:

```markdown
## Video Downloads (High Views)

- **Download Threshold**: 10,000,000 views
- **Videos Above Threshold**: 3 (15.0% of total)
- **Videos Downloaded**: 3
- **Downloads Directory**: `downloads/`
```

### JSON Data

The JSON output includes download information:

```json
{
  "download_info": {
    "download_enabled": true,
    "view_threshold": 10000000,
    "videos_above_threshold": 3,
    "videos_downloaded": 3,
    "downloaded_video_ids": [
      "abc123",
      "def456",
      "ghi789"
    ]
  }
}
```

## Examples

### Example 1: Basic High-View Download

```bash
# Download shorts with over 10M views from a channel
python youtube_channel_scraper.py @mrbeast --top 30 --download-high-views
```

**Output:**
```
📺 Channel: @mrbeast
📊 Shorts to scrape: Top 30
📖 Story-Only Mode: DISABLED (will include all videos)
📥 Download Mode: ENABLED (will download shorts with >10,000,000 views)

[Processing...]

✅ Scraping complete!
📁 Channel-specific output directory: /tmp/youtube_channel_data/UC_x5XG1O...
📄 Report: /tmp/youtube_channel_data/UC_x5XG1O.../channel_report.md
💾 JSON data: /tmp/youtube_channel_data/UC_x5XG1O.../channel_data.json
📥 Downloaded 5 shorts with >10,000,000 views
📁 Downloads directory: /tmp/youtube_channel_data/UC_x5XG1O.../downloads
```

### Example 2: Lower Threshold (5M Views)

```bash
# Download shorts with over 5M views
python youtube_channel_scraper.py @channel --top 20 --download-high-views --view-threshold 5000000
```

### Example 3: Story Videos Only with Downloads

```bash
# Download high-view story videos only
python youtube_channel_scraper.py @storyChannel --top 50 --story-only --download-high-views --view-threshold 8000000
```

## Technical Details

### Download Process

1. **Scraping Phase**: Metadata is scraped first for all videos
2. **Threshold Check**: For each video, the view count is checked against the threshold
3. **Download**: If views >= threshold, the video is downloaded using yt-dlp
4. **Quality**: Videos are downloaded in the best available quality (`-f best`)
5. **Tracking**: Downloaded video IDs are tracked for reporting

### Performance Considerations

- **Bandwidth**: Downloading videos consumes significant bandwidth
- **Storage**: Each short can be 5-50 MB depending on quality and length
- **Time**: Downloads typically take 30 seconds to 2 minutes per video, depending on:
  - Network connection speed
  - Video resolution and quality
  - File size (shorts can range from a few MB to 50+ MB)
  - YouTube server response times
- **Timeout**: Each download has a 5-minute timeout to prevent hanging

### Best Practices

1. **Start Small**: Test with `--top 5` first to see how many videos qualify
2. **Check Storage**: Ensure you have enough disk space for downloads
3. **Network**: Use on a stable, fast internet connection
4. **Threshold**: Adjust `--view-threshold` based on your needs
5. **Review First**: Run without `--download-high-views` first to see which videos qualify

## Troubleshooting

### No Videos Downloaded

**Problem**: Scraper runs but no videos are downloaded.

**Solution**:
- Check if any videos actually exceed the threshold
- Lower the `--view-threshold` value
- Verify the channel has shorts with high view counts

### Download Timeouts

**Problem**: Downloads timeout frequently.

**Solution**:
- Check your internet connection
- Try downloading fewer videos at once
- Some videos may be region-restricted or age-restricted

### Permission Errors

**Problem**: Cannot write to download directory.

**Solution**:
- Use a different `--output` directory where you have write permissions
- Use `/tmp/youtube_channel_data` (default) which should be writable

## Testing

Run the test suite to verify the download feature:

```bash
cd research/python
python test_download_feature.py
```

Expected output:
```
======================================================================
YouTube Channel Scraper - Download Feature Tests
======================================================================
...
✅ All tests passed!
```

## Version History

- **v2.0**: Added download feature with configurable view threshold
- **v1.0**: Initial release with metadata scraping only
