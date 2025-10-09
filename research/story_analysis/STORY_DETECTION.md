# Story Video Detection Feature

## Overview

The YouTube Channel Scraper now includes intelligent story video detection to help focus analysis on story content only, filtering out non-story videos like tutorials, reviews, vlogs, and gameplay videos.

## Problem Statement

Previously, the channel scraper analyzed ALL videos from a channel without distinguishing between:
- Story videos (AITA, personal stories, revenge stories, relationship stories)
- Non-story content (tutorials, reviews, vlogs, gameplay, news)

This made the analysis less relevant for the story generation pipeline, as insights were diluted by non-story content.

## Solution

Added automatic story video detection with the following features:

### Story Detection Logic

The scraper analyzes multiple signals to determine if a video is a story:

1. **Title Keywords** (weighted scoring):
   - High confidence (weight: 3): story, storytime, aita, am i the, tifu, confession, revenge
   - Medium confidence (weight: 2): relationship, breakup, cheating, caught, ex boyfriend/girlfriend, drama
   - Low confidence (weight: 1): experience, happened, crazy, shocking, drama

2. **Description Analysis**:
   - Checks for story-related phrases like "story", "happened to me", "true story", "let me tell you"

3. **Tags**:
   - Looks for story-related tags like "story", "storytime", "personal story", "aita", etc.

4. **Subtitle Analysis**:
   - Detects first-person narratives in subtitles ("i was", "i had", "this happened")

5. **Anti-patterns** (negative signals):
   - Filters out videos with keywords like: tutorial, review, vlog, gameplay, how to, walkthrough, etc.

### Confidence Scoring

- Videos receive a confidence score from 0 to 1
- Threshold for story classification: 0.3 (permissive but effective)
- Scores are included in reports for transparency

## Usage

### Basic Usage (All Videos)

```bash
# Scrape all videos (default behavior)
python research/python/youtube_channel_scraper.py @channelname --top 10
```

### Story-Only Mode (Recommended for Story Analysis)

```bash
# Filter to include ONLY story videos
python research/python/youtube_channel_scraper.py @channelname --top 10 --story-only
```

### Interactive Mode

```bash
# No arguments - will prompt for channel
python research/python/youtube_channel_scraper.py

# Then choose to enable story-only filtering when prompted
```

## Output

### Reports Include Story Analysis

When running in default mode, reports show:
- Total story videos detected
- Non-story videos detected
- Average story confidence score
- Story vs non-story breakdown by format (shorts/long)

When running in `--story-only` mode, reports show:
- Number of story videos included
- Number of non-story videos filtered out
- Average story confidence of included videos

### JSON Output

The JSON output includes for each video:
- `is_story_video`: boolean
- `story_confidence_score`: float (0-1)
- `story_indicators`: list of matched indicators

Summary statistics include:
```json
{
  "story_analysis": {
    "story_only_mode": true/false,
    "story_videos_count": 8,
    "non_story_videos_count": 2,
    "filtered_out_count": 5,
    "average_story_confidence": 0.67,
    "story_videos_percentage": 80.0
  }
}
```

## Benefits

1. **More Relevant Analysis**: Focus on story content for story generation pipeline
2. **Better Insights**: Extract patterns from actual story videos, not mixed content
3. **Transparency**: Confidence scores show detection accuracy
4. **Flexibility**: Optional filtering - can analyze all videos or stories only
5. **Quality Control**: Identify channels with high story content percentage

## Testing

Comprehensive tests verify detection accuracy:

```bash
cd research/python
python test_story_detection.py
```

Test coverage includes:
- Story videos with various indicators (AITA, revenge, personal stories)
- Non-story videos (tutorials, reviews, vlogs, gameplay)
- Edge cases and borderline content
- Filtering functionality

All tests pass (9/9) with high accuracy.

## Examples

### Story Videos (Correctly Detected)

✅ "My Crazy Story Time - AITA for kicking out my roommate?" (confidence: 0.50)
✅ "I Caught My Ex Cheating - Revenge Story" (confidence: 0.50)
✅ "The Day My Life Changed Forever" + description with "true story" (confidence: 0.40)

### Non-Story Videos (Correctly Filtered)

❌ "How to Cook Pasta - Tutorial" (confidence: 0.00)
❌ "iPhone 15 Review - Unboxing" (confidence: 0.00)
❌ "My Daily Vlog - Day 123" (confidence: 0.00)

## Integration with Story Pattern Analyzer

After scraping story videos, you can analyze their patterns:

```bash
# 1. Scrape story videos
python research/python/youtube_channel_scraper.py @storyChannel --top 20 --story-only

# 2. Analyze subtitle patterns
cd /tmp/youtube_channel_data
python ../../research/python/story_pattern_analyzer.py *.srt

# 3. Use insights to improve story generation
```

## Future Enhancements

Possible improvements:
- Machine learning-based detection (train on labeled data)
- Category-specific detection (relationship stories vs revenge stories)
- Adjustable confidence threshold
- Detection quality metrics and A/B testing
- Integration with story pattern analyzer for automatic workflow
