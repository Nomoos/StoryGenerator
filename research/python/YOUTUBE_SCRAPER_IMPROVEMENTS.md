# YouTube Channel Scraper - Recent Improvements

## Overview

The YouTube Channel Scraper has been enhanced to address organization and file format issues for better GitHub compatibility and data management.

## Key Improvements

### 1. Channel-Specific Output Directories

**Problem**: Previously, all scraped data was saved to a single directory, causing files to overwrite each other when scraping multiple channels.

**Solution**: Each channel now gets its own dedicated subdirectory:

```
/tmp/youtube_channel_data/
├── UCxxx_ChannelName1/
│   ├── channel_report.md
│   ├── channel_data.json
│   ├── channel_data_summary.md
│   ├── video1.info.json
│   ├── video1.info.md
│   └── ...
├── UCyyy_ChannelName2/
│   ├── channel_report.md
│   ├── channel_data.json
│   ├── channel_data_summary.md
│   └── ...
```

Directory naming format: `{channel_id}_{sanitized_channel_name}`

**Benefits**:
- No more file overwrites
- Easy to identify which channel's data you're viewing
- Better organization for analyzing multiple channels
- Historical data preservation

### 2. Channel Information in Reports

**Enhancement**: Channel reports now include:
- Channel ID in the report title
- Channel name prominently displayed
- Scrape timestamp
- Dedicated "Channel Information" section

Example report title:
```markdown
# YouTube Channel Scraping Report - Mr Beast (UCX6OQ3DkcsbYNE6H8uQQuVA)

## Channel Information

- **Channel Name**: Mr Beast
- **Channel ID**: UCX6OQ3DkcsbYNE6H8uQQuVA
- **Scrape Date**: 2025-01-09 14:30:45
```

### 3. JSON to Markdown Conversion

**Problem**: GitHub's file attachment/viewing limitations with `.json` files make them harder to share and preview.

**Solution**: Automatic Markdown versions created for all data files:

#### A. Channel Data Summary (`channel_data_summary.md`)

Converts `channel_data.json` into a readable Markdown format including:
- Summary statistics
- Format breakdown (shorts vs long videos)
- Engagement metrics
- Content quality metrics
- Video durations
- Complete video list with key metrics

**Example**:
```markdown
# Channel Data Summary

**Generated**: 2025-01-09 14:30:45
**Channel**: Mr Beast (UCX6OQ3DkcsbYNE6H8uQQuVA)

## Summary Statistics

- **Total Videos**: 20
- **Shorts Count**: 10
- **Long Videos Count**: 10
- **Total Views**: 150,234,567
...
```

#### B. Individual Video Info (`{video_id}.info.md`)

Converts each `{video_id}.info.json` into Markdown including:
- Basic information
- Viewership & engagement metrics
- Video quality specs
- Content analysis
- Description (truncated)
- Tags
- Subtitle text preview

**Example**:
```markdown
# 🎬 This is How I Got Rich

## Basic Information

- **Video ID**: dQw4w9WgXcQ
- **URL**: https://www.youtube.com/watch?v=dQw4w9WgXcQ
- **Format**: SHORT
- **Views**: 1,234,567
...
```

### 4. File Organization Summary

Each channel scrape now produces:

| File | Format | Purpose |
|------|--------|---------|
| `channel_report.md` | Markdown | Comprehensive human-readable report |
| `channel_data.json` | JSON | Machine-readable complete dataset |
| `channel_data_summary.md` | Markdown | GitHub-friendly JSON summary |
| `{video_id}.info.json` | JSON | Complete video metadata |
| `{video_id}.info.md` | Markdown | GitHub-friendly video info |
| `{video_id}.srt` | SRT | Video subtitles (if available) |

## Usage

### Basic Usage (Unchanged)

```bash
# Interactive mode
python youtube_channel_scraper.py

# With channel argument
python youtube_channel_scraper.py @channel_handle --top 10
python youtube_channel_scraper.py UCxxx_channel_id --top 20
```

### Output Location

The scraper will:
1. Extract channel ID and name from first video
2. Create channel-specific directory: `{output_dir}/{channel_id}_{channel_name}/`
3. Save all files in that directory

### Example Output

```
📺 Channel: @MrBeast
📁 Channel-specific output directory: /tmp/youtube_channel_data/UCX6OQ3DkcsbYNE6H8uQQuVA_MrBeast

✅ Scraping complete!
📁 Channel-specific output directory: /tmp/youtube_channel_data/UCX6OQ3DkcsbYNE6H8uQQuVA_MrBeast
📄 Report: /tmp/youtube_channel_data/UCX6OQ3DkcsbYNE6H8uQQuVA_MrBeast/channel_report.md
💾 JSON data: /tmp/youtube_channel_data/UCX6OQ3DkcsbYNE6H8uQQuVA_MrBeast/channel_data.json
📄 Markdown summary: /tmp/youtube_channel_data/UCX6OQ3DkcsbYNE6H8uQQuVA_MrBeast/channel_data_summary.md
```

## Benefits for GitHub

### Easier Sharing

- Markdown files can be directly viewed in GitHub
- Can attach `.md` files to issues/comments without conversion
- Better preview in pull requests

### Better Organization

- Channel-specific folders keep data separated
- Easy to navigate through multiple channel analyses
- Historical data preserved without overwrites

### Improved Collaboration

- Team members can easily view data without downloading
- Markdown format is readable in GitHub UI
- JSON still available for programmatic access

## Migration Guide

### For Existing Scraped Data

If you have existing scraped data in the old format (all files in one directory):

1. The scraper will now create new channel-specific directories
2. Old data will remain in the base output directory
3. Consider manually organizing old data into channel folders:

```bash
# Example manual organization
mkdir -p /tmp/youtube_channel_data/UCxxx_OldChannel
mv /tmp/youtube_channel_data/video*.* /tmp/youtube_channel_data/UCxxx_OldChannel/
mv /tmp/youtube_channel_data/channel_*.* /tmp/youtube_channel_data/UCxxx_OldChannel/
```

### Backward Compatibility

The scraper maintains backward compatibility:
- Old JSON structure unchanged (just with added channel_id/channel_name fields)
- All existing analysis scripts continue to work
- New Markdown files are additions, not replacements

## Technical Details

### Channel Directory Creation

```python
def _get_channel_output_dir(self) -> Path:
    """
    Get channel-specific output directory.
    Creates: {output_dir}/{channel_id}_{sanitized_channel_name}/
    
    Falls back to:
    - {channel_id} only if name unavailable
    - channel_{timestamp} if no channel info
    """
```

### Markdown Conversion

- Automated during scrape process
- No additional steps required
- Preserves all key metrics and information
- Truncates long text fields for readability

## Future Enhancements

Potential additions:
- Comparison reports across multiple channels
- Trend analysis over time with multiple scrapes
- Aggregate statistics for related channels
- Channel network analysis

## Troubleshooting

### Issue: Old directory structure

**Solution**: Delete old files or move them to channel-specific folders

### Issue: Permission errors creating directories

**Solution**: Ensure write permissions on output directory

### Issue: Channel name has special characters

**Solution**: Automatically sanitized to filesystem-safe characters (letters, numbers, hyphens, underscores)

## Summary

These improvements make the YouTube Channel Scraper:
- ✅ Better organized (channel-specific directories)
- ✅ More GitHub-friendly (Markdown versions)
- ✅ Easier to share (attachable .md files)
- ✅ Less error-prone (no overwrites)
- ✅ More maintainable (clear data structure)
- ✅ Backward compatible (existing scripts work)
- ✅ **NEW: Download high-view shorts** (10M+ views by default)

## NEW: Download High-View Shorts Feature

### Overview

The scraper can now automatically download shorts that exceed a view threshold (default: 10 million views). This is useful for analyzing viral content and understanding what makes shorts successful.

### Usage

```bash
# Download shorts with over 10M views
python youtube_channel_scraper.py @channel --top 20 --download-high-views

# Custom threshold (e.g., 5M views)
python youtube_channel_scraper.py @channel --top 20 --download-high-views --view-threshold 5000000

# Combined with story filtering
python youtube_channel_scraper.py @channel --top 30 --story-only --download-high-views
```

### Output Structure

When downloads are enabled, a `downloads/` subdirectory is created:

```
/tmp/youtube_channel_data/
└── UCxxx_ChannelName/
    ├── channel_report.md
    ├── channel_data.json
    ├── channel_data_summary.md
    ├── downloads/              # NEW: Downloaded videos
    │   ├── video1.mp4
    │   ├── video2.mp4
    │   └── ...
    ├── video1.info.json
    └── ...
```

### Command Line Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `--download-high-views` | flag | disabled | Enable downloading of high-view shorts |
| `--view-threshold` | integer | 10000000 | Minimum view count to download (10 million) |

### Example Output

```
📺 Channel: @channel
📊 Shorts to scrape: Top 20
📖 Story-Only Mode: DISABLED (will include all videos)
📥 Download Mode: ENABLED (will download shorts with >10,000,000 views)

[Processing...]

✅ Scraping complete!
📁 Channel-specific output directory: /tmp/youtube_channel_data/UCxxx_Channel
📄 Report: channel_report.md
💾 JSON data: channel_data.json
📥 Downloaded 5 shorts with >10,000,000 views
📁 Downloads directory: downloads/
```

For complete documentation on the download feature, see [DOWNLOAD_FEATURE.md](DOWNLOAD_FEATURE.md).

---

**Updated**: January 2025
**Version**: 2.1
