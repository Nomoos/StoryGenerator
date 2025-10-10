# YouTube Channel Scraper - Quick Reference

## Installation

```bash
pip install yt-dlp
```

## Basic Commands

### Scrape Metadata Only

```bash
# Scrape top 10 shorts from a channel
python youtube_channel_scraper.py @channelname --top 10

# Interactive mode (prompts for channel)
python youtube_channel_scraper.py
```

### Download High-View Shorts

```bash
# Download shorts with 10M+ views (default threshold)
python youtube_channel_scraper.py @channelname --top 20 --download-high-views

# Custom threshold (5 million views)
python youtube_channel_scraper.py @channelname --top 20 --download-high-views --view-threshold 5000000

# Lower threshold (1 million views)
python youtube_channel_scraper.py @channelname --top 20 --download-high-views --view-threshold 1000000
```

### Combined Features

```bash
# Story videos only + high-view downloads
python youtube_channel_scraper.py @channelname --top 30 --story-only --download-high-views

# Custom output directory
python youtube_channel_scraper.py @channelname --output /path/to/output --download-high-views
```

## Command-Line Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `channel` | positional | (prompt) | Channel URL, @handle, or ID |
| `--top` | integer | 10 | Number of shorts to scrape |
| `--output` | path | /tmp/youtube_channel_data | Output directory |
| `--story-only` | flag | disabled | Filter story videos only |
| `--download-high-views` | flag | disabled | Download high-view shorts |
| `--view-threshold` | integer | 10000000 | Minimum views to download |

## Output Files

Every scrape creates a channel-specific folder with:

```
{channel_id}_{channel_name}/
├── channel_report.md          # Human-readable report
├── channel_data.json           # Machine-readable data
├── channel_data_summary.md     # Markdown version of JSON
├── downloads/                  # Downloaded videos (if enabled)
│   └── {video_id}.mp4
├── {video_id}.info.json        # Video metadata
├── {video_id}.info.md          # Video metadata (markdown)
└── {video_id}.srt              # Subtitles (when available)
```

## Common Use Cases

### Research Viral Content

```bash
# Find and download all shorts with 10M+ views
python youtube_channel_scraper.py @mrbeast --top 50 --download-high-views
```

### Analyze Story Videos

```bash
# Scrape only story videos from a channel
python youtube_channel_scraper.py @storyChannel --top 30 --story-only
```

### Bulk Download Popular Shorts

```bash
# Download all shorts with 5M+ views
python youtube_channel_scraper.py @channel --top 100 --download-high-views --view-threshold 5000000
```

### Quick Metadata Check

```bash
# Just get metadata for top 5 shorts
python youtube_channel_scraper.py @channel --top 5
```

## Testing

```bash
# Test download feature
python test_download_feature.py

# Integration tests
python test_integration.py

# Full verification
./test_final_verification.sh
```

## Tips

1. **Start Small**: Use `--top 5` first to test
2. **Check Storage**: Downloads can be 5-50 MB per video
3. **Network Speed**: Downloads work best on fast connections
4. **Threshold Tuning**: Adjust `--view-threshold` based on channel size
5. **Story Filtering**: Use `--story-only` to focus on narrative content

## Troubleshooting

### No Downloads

**Problem**: Scraper runs but nothing downloads.

**Solution**: Lower the `--view-threshold` or check if channel has high-view shorts.

### yt-dlp Error

**Problem**: "yt-dlp is not installed"

**Solution**: `pip install yt-dlp`

### Slow Downloads

**Problem**: Downloads take too long.

**Solution**: Check internet connection, reduce `--top` value, or run during off-peak hours.

## Documentation

- **DOWNLOAD_FEATURE.md** - Complete download feature guide
- **UPDATE_SUMMARY.md** - Detailed change summary
- **YOUTUBE_SCRAPER_IMPROVEMENTS.md** - All improvements and features

## Support

For issues or questions, see the documentation files or run:
```bash
python youtube_channel_scraper.py --help
```

---

**Version**: 2.1  
**Last Updated**: January 2025
