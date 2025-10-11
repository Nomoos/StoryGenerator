# YouTube Subtitle Analyzer - Quick Start Guide

## Installation

### Step 1: Install Python Dependencies

```bash
pip install yt-dlp
```

### Step 2: Install FFmpeg

**Linux (Ubuntu/Debian)**:
```bash
sudo apt-get update
sudo apt-get install ffmpeg
```

**macOS**:
```bash
brew install ffmpeg
```

**Windows**:
Download from [ffmpeg.org](https://ffmpeg.org/download.html) and add to PATH.

## Usage

### Analyze Any YouTube Video

```bash
# Navigate to the StoryGenerator directory
cd /path/to/StoryGenerator

# Run the analyzer with a YouTube URL
python research/python/youtube_subtitle_analyzer.py <youtube_url>
```

### Examples

#### Analyze YouTube Shorts
```bash
python research/python/youtube_subtitle_analyzer.py https://www.youtube.com/shorts/41QD8C6tqIU
```

#### Analyze Regular YouTube Video
```bash
python research/python/youtube_subtitle_analyzer.py https://www.youtube.com/watch?v=dQw4w9WgXcQ
```

#### Analyze with Custom Output Directory
```bash
# Modify the script or use Python directly
python -c "
from research.python.youtube_subtitle_analyzer import YouTubeSubtitleAnalyzer

analyzer = YouTubeSubtitleAnalyzer(output_dir='./my_analysis')
analyzer.analyze_video('https://www.youtube.com/shorts/41QD8C6tqIU')
"
```

## What Gets Generated

After running the analyzer, you'll find these files in `/tmp/youtube_research/`:

1. **`{video_id}.mp4`** - Downloaded video file
2. **`{video_id}.srt`** - Extracted subtitle file
3. **`{video_id}_report.md`** - Comprehensive analysis report (human-readable)
4. **`{video_id}_analysis.json`** - Analysis data (machine-readable)

### Example Output Structure

```
/tmp/youtube_research/
├── 41QD8C6tqIU.mp4                    # Video file
├── 41QD8C6tqIU.srt                    # Subtitle file
├── 41QD8C6tqIU_report.md              # Analysis report
└── 41QD8C6tqIU_analysis.json          # JSON data
```

## Understanding the Analysis Report

The report includes:

### 1. Summary Statistics
- Total segments and duration
- Average, min, max segment durations
- Words per segment
- Characters per segment
- Reading speed (words per second)

### 2. Timing Analysis
- Number of gaps between segments
- Average gap duration
- Number of overlapping segments (should be 0)

### 3. Detailed Segment Breakdown
Table showing each subtitle segment with:
- Start and end times
- Duration
- Text content
- Word count
- Character count
- Reading speed

### 4. Key Findings
- Recommended subtitle duration ranges
- Optimal text length guidelines
- Reading speed recommendations
- Timing recommendations

### 5. Implementation Guidelines
Ready-to-use configuration for StoryGenerator pipeline

## Analyzing Existing SRT Files

If you already have subtitle files:

```python
from research.python.youtube_subtitle_analyzer import YouTubeSubtitleAnalyzer

analyzer = YouTubeSubtitleAnalyzer()

# Parse existing SRT file
segments = analyzer.parse_srt_file('path/to/subtitles.srt')

# Analyze the segments
analysis = analyzer.analyze_subtitles(
    segments,
    video_id='my_video',
    video_url='https://example.com/video'
)

# Generate report
analyzer.generate_report(analysis, 'my_analysis_report.md')
```

## Troubleshooting

### Error: "yt-dlp is not installed"
**Solution**: Run `pip install yt-dlp`

### Error: "ffmpeg is not installed"
**Solution**: Install ffmpeg using your system's package manager

### Error: "Could not retrieve subtitles"
**Possible causes**:
1. Video doesn't have subtitles
2. Subtitles are disabled
3. Network/firewall blocking YouTube

**Solutions**:
1. Try a different video with known subtitles
2. Check if you can access YouTube in your browser
3. Use a VPN if YouTube is blocked

### Error: "Unable to download API page"
**Possible causes**:
1. Network connectivity issues
2. YouTube blocking the request
3. Video is private or deleted

**Solutions**:
1. Check internet connection
2. Verify the video URL is accessible
3. Try with a different video

### Warning: "Video download failed"
If only video download fails but subtitles work, this is normal. The analyzer will continue with subtitle analysis.

## Advanced Usage

### Custom Analysis Parameters

```python
from research.python.youtube_subtitle_analyzer import YouTubeSubtitleAnalyzer

# Create analyzer with custom output directory
analyzer = YouTubeSubtitleAnalyzer(output_dir='/path/to/output')

# Analyze video
analysis = analyzer.analyze_video('https://www.youtube.com/shorts/...')

# Access analysis data
print(f"Total segments: {analysis.total_segments}")
print(f"Average duration: {analysis.avg_segment_duration:.2f}s")
print(f"Reading speed: {analysis.avg_reading_speed_wps:.2f} WPS")

# Iterate over segments
for segment in analysis.segments:
    print(f"{segment.start_time:.2f}s - {segment.end_time:.2f}s: {segment.text}")
```

### Batch Analysis

Analyze multiple videos:

```python
from research.python.youtube_subtitle_analyzer import YouTubeSubtitleAnalyzer

urls = [
    'https://www.youtube.com/shorts/video1',
    'https://www.youtube.com/shorts/video2',
    'https://www.youtube.com/shorts/video3',
]

analyzer = YouTubeSubtitleAnalyzer()

for url in urls:
    print(f"\nAnalyzing: {url}")
    analysis = analyzer.analyze_video(url)
    if analysis:
        print(f"✅ Success: {analysis.total_segments} segments")
    else:
        print("❌ Failed")
```

### Export to CSV

```python
import csv
from research.python.youtube_subtitle_analyzer import YouTubeSubtitleAnalyzer

analyzer = YouTubeSubtitleAnalyzer()
segments = analyzer.parse_srt_file('subtitles.srt')

# Export to CSV
with open('subtitle_analysis.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['Index', 'Start', 'End', 'Duration', 'Text', 'Words', 'Chars', 'WPS'])
    
    for seg in segments:
        writer.writerow([
            seg.index,
            seg.start_time,
            seg.end_time,
            seg.duration,
            seg.text,
            seg.word_count,
            seg.char_count,
            seg.words_per_second
        ])
```

## Integration with StoryGenerator

The analysis results can be directly applied to improve subtitle generation:

### Step 1: Analyze Target Videos

Analyze successful videos in your target demographic:

```bash
# Analyze viral emotional storytelling videos
python research/python/youtube_subtitle_analyzer.py https://youtube.com/shorts/example1
python research/python/youtube_subtitle_analyzer.py https://youtube.com/shorts/example2
python research/python/youtube_subtitle_analyzer.py https://youtube.com/shorts/example3
```

### Step 2: Review Analysis Reports

Check the generated reports for common patterns:
- Average segment duration
- Words per segment
- Reading speed
- Gap timing

### Step 3: Update GTitles.py Configuration

Apply findings to `Generators/GTitles.py`:

```python
# Based on analysis of target videos
SUBTITLE_CONFIG = {
    'target_duration': 2.5,        # from analysis
    'max_words': 8,                # from analysis
    'target_wps': 3.0,             # from analysis
    'gap_duration': 0.1,           # from analysis
}
```

### Step 4: Validate Generated Subtitles

Use the analyzer to validate your own generated subtitles:

```python
# After generating subtitles in GTitles.py
analyzer = YouTubeSubtitleAnalyzer()
segments = analyzer.parse_srt_file('data/Stories/4_Titles/my_video.srt')
analysis = analyzer.analyze_subtitles(segments, 'my_video', 'local')

# Check if metrics match target
if 2.0 < analysis.avg_segment_duration < 3.5:
    print("✅ Segment duration optimal")
else:
    print("⚠️ Adjust segment duration")

if 2.0 < analysis.avg_reading_speed_wps < 3.5:
    print("✅ Reading speed optimal")
else:
    print("⚠️ Adjust reading speed")
```

## Performance Expectations

- **Download time**: 5-30 seconds per video
- **Analysis time**: <1 second for subtitle parsing
- **Report generation**: <1 second
- **Total time**: ~30-60 seconds per video

## Best Practices

1. **Start with sample videos** - Test with known good videos first
2. **Analyze multiple examples** - Get averages across 5-10 videos
3. **Focus on your niche** - Analyze videos similar to what you're creating
4. **Document findings** - Keep notes on what works in your target demographic
5. **Iterate and refine** - Use analysis to continuously improve your subtitles

## Need Help?

- **Documentation**: See `research/YOUTUBE_SUBTITLE_RESEARCH.md`
- **Examples**: See `research/subtitle_analysis/README.md`
- **Sample Analysis**: See `research/subtitle_analysis/sample_analysis_report.md`

---

**Quick Command Reference**:

```bash
# Install dependencies
pip install yt-dlp
sudo apt-get install ffmpeg  # Linux
brew install ffmpeg          # macOS

# Analyze a video
python research/python/youtube_subtitle_analyzer.py <url>

# View results
cat /tmp/youtube_research/*_report.md
```
