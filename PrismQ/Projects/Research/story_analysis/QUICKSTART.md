# Story Analysis Quick Start Guide

## Overview

This guide shows you how to use the story analysis tools to extract success patterns from YouTube videos and apply them to the StoryGenerator pipeline.

## Tools

1. **Story Pattern Analyzer** - Analyzes subtitle files for narrative patterns
2. **YouTube Channel Scraper** - Scrapes video metadata from channels

## Installation

```bash
# Required dependency
pip install yt-dlp

# Already included in requirements.txt
```

## Quick Start

### Option 1: Analyze Existing Subtitle Files

If you have subtitle files (from DownSub.com or other sources):

```bash
# Analyze one or more subtitle files
python research/python/story_pattern_analyzer.py subtitle1.txt subtitle2.txt subtitle3.txt

# Or use wildcards
python research/python/story_pattern_analyzer.py /path/to/subtitles/*.txt

# Output will be saved to:
# - /tmp/story_patterns_report.md (comprehensive report)
# - /tmp/story_patterns_analysis.json (machine-readable data)
```

### Option 2: Scrape and Analyze Channel Videos

To scrape top videos from a YouTube channel:

```bash
# Scrape top 10 videos from a channel
python research/python/youtube_channel_scraper.py @channelname --top 10

# Or use full URL
python research/python/youtube_channel_scraper.py https://www.youtube.com/@storytimechannel --top 10

# Or use channel ID
python research/python/youtube_channel_scraper.py UC1234567890 --top 20

# Specify output directory
python research/python/youtube_channel_scraper.py @channel --top 10 --output /path/to/output

# Output includes:
# - channel_report.md (comprehensive analysis)
# - channel_data.json (all metadata)
# - {video_id}.info.json (per-video metadata)
# - {video_id}.srt (subtitles, if available)
```

### Option 3: Combined Workflow

Complete analysis of a competitor channel:

```bash
# Step 1: Scrape channel
python research/python/youtube_channel_scraper.py @competitorname --top 20 --output /tmp/competitor

# Step 2: Analyze subtitle patterns (if subtitles were downloaded)
python research/python/story_pattern_analyzer.py /tmp/competitor/*.srt

# Step 3: Review reports
cat /tmp/competitor/channel_report.md
cat /tmp/story_patterns_report.md
```

## Understanding the Output

### Story Pattern Report

The report includes:

1. **Individual Story Analyses**
   - Word count, sentence count
   - Hook analysis (first sentence effectiveness)
   - Story arc structure
   - Dialogue usage
   - Emotional elements

2. **Success Patterns**
   - Average optimal length
   - Hook strategy guidelines
   - Story structure recommendations
   - Emotional engagement tactics
   - Time progression patterns

3. **Implementation Guidelines**
   - Ready-to-use configuration for GScript.py
   - Quality validation code
   - Best practices

### Channel Scraping Report

The report includes:

1. **Summary Statistics**
   - Total videos analyzed
   - Average views, likes, comments
   - Subtitle availability

2. **Per-Video Details**
   - Title and description
   - View counts and engagement
   - Tags and metadata
   - Subtitle text

3. **Pattern Analysis**
   - Most common tags
   - Title word patterns
   - Top performing videos
   - Content trends

## Example Analysis

### Sample Output - Story Patterns

From analyzing 6 successful stories:

```
Optimal Length: 632 words (±50)
Hook Length: 10.5 words average
Story Structure: Setup → Conflict → Escalation → Climax → Resolution
Dialogue Usage: 83% of stories
Resolution Rate: 100%
Common Emotional Words: angry, crazy, happy, horrified
Time Markers: later, after, months, years, then, finally
```

### Implementation in Pipeline

```python
# In GScript.py
STORY_CONFIG = {
    'target_word_count': 632,
    'target_sentences': 67,
    'words_per_sentence': 9.9,
    'hook_max_words': 15,
    'use_dialogue': 0.83,  # 83% probability
    'require_resolution': True,
    'story_arc': ['Setup/Introduction', 'Conflict/Problem', 
                  'Escalation', 'Climax/Turning Point', 'Resolution'],
}
```

## Use Cases

### 1. Competitive Analysis

**Goal:** Understand what makes competitors successful

```bash
# Scrape top 10 videos from 3 competitors
python research/python/youtube_channel_scraper.py @competitor1 --top 10 --output /tmp/comp1
python research/python/youtube_channel_scraper.py @competitor2 --top 10 --output /tmp/comp2
python research/python/youtube_channel_scraper.py @competitor3 --top 10 --output /tmp/comp3

# Analyze all subtitles together
python research/python/story_pattern_analyzer.py /tmp/comp*/*.srt

# Compare patterns across competitors
```

### 2. Content Optimization

**Goal:** Optimize your story generation based on successful patterns

```bash
# Scrape your own channel
python research/python/youtube_channel_scraper.py @yourchannel --top 20

# Identify top performers
# Analyze patterns in top 5 videos
python research/python/story_pattern_analyzer.py /tmp/youtube_channel_data/{top_5_ids}.srt

# Apply patterns to pipeline configuration
```

### 3. Trend Analysis

**Goal:** Track evolving content patterns over time

```bash
# Scrape channel monthly
python research/python/youtube_channel_scraper.py @channel --top 30 --output /tmp/channel_$(date +%Y%m)

# Analyze patterns
python research/python/story_pattern_analyzer.py /tmp/channel_*/*.srt

# Compare reports month-over-month
```

### 4. A/B Testing Preparation

**Goal:** Establish baseline metrics for testing

```bash
# Analyze current successful videos
python research/python/story_pattern_analyzer.py current_stories/*.srt

# Use extracted patterns as control
# Generate test variations
# Compare against baseline
```

## Integration with Existing Tools

### Combined with Subtitle Analysis

The story pattern tools complement the subtitle analyzer:

```bash
# Technical subtitle analysis (timing, formatting)
python research/python/youtube_subtitle_analyzer.py https://youtube.com/video1

# Content pattern analysis (story structure, hooks)
python research/python/story_pattern_analyzer.py /tmp/youtube_research/*.srt

# Channel-wide analysis
python research/python/youtube_channel_scraper.py @channel --top 10
```

### Full Research Workflow

```
1. Identify target channels/videos
   ↓
2. Scrape metadata (youtube_channel_scraper.py)
   ↓
3. Analyze subtitle timing (youtube_subtitle_analyzer.py)
   ↓
4. Extract story patterns (story_pattern_analyzer.py)
   ↓
5. Apply to GScript.py and GTitles.py
   ↓
6. Generate test videos
   ↓
7. Validate against extracted patterns
   ↓
8. Iterate based on performance
```

## Tips & Best Practices

### For Story Pattern Analysis

1. **Sample Size**: Analyze at least 10 stories for reliable patterns
2. **Diversity**: Include various story types (conflict, romance, revenge, etc.)
3. **Recency**: Prioritize recent successful videos (last 3-6 months)
4. **Performance**: Focus on videos with >100K views for proven patterns
5. **Demographics**: Match your target audience's preferences

### For Channel Scraping

1. **Top Videos**: Start with top 10-20 most viewed videos
2. **Regular Updates**: Scrape monthly to track trends
3. **Multiple Channels**: Compare 3-5 similar channels
4. **Tags Analysis**: Pay attention to common tags across top videos
5. **Engagement**: Look for high like/view and comment/view ratios

### For Pipeline Integration

1. **Start Conservative**: Apply patterns gradually
2. **A/B Test**: Compare generated content with/without patterns
3. **Measure Results**: Track engagement metrics
4. **Iterate**: Refine based on performance data
5. **Document**: Keep records of pattern changes and results

## Troubleshooting

### Story Pattern Analyzer

**Issue:** No patterns detected
- **Solution:** Ensure subtitle files contain actual story content, not just timecodes

**Issue:** Incomplete analysis
- **Solution:** Check that subtitle files are complete (not truncated)

### YouTube Channel Scraper

**Issue:** No videos found
- **Solution:** Verify channel URL/handle is correct
- **Solution:** Try with `/videos` suffix: `@channel/videos`

**Issue:** No subtitles downloaded
- **Solution:** Videos may not have subtitles enabled
- **Solution:** Try different videos or channels

**Issue:** Rate limiting
- **Solution:** Add delays between requests
- **Solution:** Reduce number of videos scraped at once

## Next Steps

After analyzing patterns:

1. **Update Configuration**
   - Apply optimal word counts to GScript.py
   - Update subtitle timing in GTitles.py
   - Adjust quality checks

2. **Test Generation**
   - Generate 5-10 test stories using new patterns
   - Compare against analyzed stories
   - Validate structure and engagement

3. **Monitor Performance**
   - Track view counts, retention
   - Measure engagement metrics
   - Compare to baseline

4. **Iterate**
   - Refine patterns based on results
   - Re-analyze successful content
   - Continuously improve

## Support

- **Tool Documentation**: `research/story_analysis/README.md`
- **Sample Analysis**: `research/story_analysis/story_patterns_report.md`
- **Subtitle Research**: `research/subtitle_analysis/`

## References

- Story Pattern Analyzer: `research/python/story_pattern_analyzer.py`
- YouTube Channel Scraper: `research/python/youtube_channel_scraper.py`
- Analysis Results: `research/story_analysis/`

---

**Created:** October 2025  
**Tools Version:** 1.0  
**Status:** Production ready
