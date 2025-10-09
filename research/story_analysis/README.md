# Story Pattern Analysis Tools

This directory contains tools and analysis results for extracting success patterns from viral YouTube stories.

## Tools

### 1. Story Pattern Analyzer (`research/python/story_pattern_analyzer.py`)

Analyzes subtitle files from successful YouTube stories to extract patterns, rules, and best practices.

**Features:**
- Extracts story structure (hook, conflict, escalation, climax, resolution)
- Identifies emotional trigger words
- Analyzes time progression markers
- Detects dialogue usage
- Calculates optimal content length
- Generates comprehensive reports

**Usage:**
```bash
python research/python/story_pattern_analyzer.py subtitle1.txt subtitle2.txt ...
```

**Output:**
- Markdown report with patterns and rules
- JSON data for further processing

### 2. YouTube Channel Scraper (`research/python/youtube_channel_scraper.py`)

Scrapes comprehensive metadata from YouTube Shorts on a channel (shorts only).

**Features:**
- **Shorts-focused analysis** - Scrapes only YouTube Shorts for relevant story insights
- Extracts titles, descriptions, tags
- Downloads subtitles (if available)
- Collects view counts, likes, comments
- Analyzes common patterns across shorts
- **Story video detection and filtering** - Identifies story videos vs non-story content
- Generates comprehensive reports with story analysis

**Usage:**
```bash
# By channel handle (scrapes top 10 shorts)
python research/python/youtube_channel_scraper.py @channelname --top 10

# By channel URL
python research/python/youtube_channel_scraper.py https://www.youtube.com/@channelname --top 10

# By channel ID
python research/python/youtube_channel_scraper.py UC1234567890 --top 20

# Filter to include ONLY story shorts (recommended for story generation pipeline)
python research/python/youtube_channel_scraper.py @channelname --top 10 --story-only
```

**Output:**
- Markdown report with shorts metadata and story analysis
- JSON data with all scraped information including story confidence scores
- Individual video info files
- Subtitle files (where available)

**Story Detection:**
The scraper automatically detects story videos based on:
- Title keywords (story, AITA, revenge, relationship, etc.)
- Description content
- Tags
- Subtitle content (first-person narratives)
- Exclusion of non-story content (tutorials, reviews, vlogs, etc.)

Use `--story-only` flag to filter out non-story videos and focus analysis on story content only.

**Note:** The scraper now focuses exclusively on YouTube Shorts (≤3min, vertical format) for more relevant story analysis.

## Analysis Results

### Story Patterns Report

**File:** `story_patterns_report.md`

Comprehensive analysis of 6 successful YouTube stories revealing:

**Key Findings:**
- **Optimal Length:** 582-682 words per story
- **Hook Length:** 6-16 words (average: 10.5 words)
- **Story Structure:** Setup → Conflict → Escalation → Climax → Resolution
- **Dialogue Usage:** 83% of stories use dialogue
- **Resolution Rate:** 100% have clear resolution
- **Sentences:** Average 67 sentences, 9.9 words per sentence

**Common Patterns:**
- Strong opening hook presenting immediate conflict
- Clear time progression with markers (later, then, after, finally)
- Natural escalation of conflict
- Emotional engagement through relatable situations
- Satisfying resolution or payoff

**Content Guidelines:**
- Focus on relatable conflicts (neighbors, family, work, school)
- Include specific details and direct quotes
- Show clear character reactions
- Create justice/karma moments
- End with closure or lesson learned

### Application to StoryGenerator

The extracted patterns should guide:

1. **Script Generation (GScript.py)**
   - Target 632 words (±50)
   - Create compelling hook (10-15 words)
   - Follow 5-part story arc
   - Include dialogue (83% probability)
   - Ensure clear resolution

2. **Quality Validation**
   - Check word count: 580-680 words
   - Verify story structure completeness
   - Confirm dialogue presence
   - Validate resolution exists
   - Check engagement elements

3. **Content Creation**
   - Use emotional trigger words strategically
   - Include time markers for pacing
   - Build conflict naturally
   - Create satisfying payoffs

## Data Files

### story_patterns_analysis.json

Machine-readable analysis data containing:
- Individual story metrics
- Extracted patterns
- Success rules
- Common elements

### story_patterns_report.md

Human-readable analysis report with:
- Individual story breakdowns
- Success patterns and rules
- Implementation guidelines
- Configuration recommendations

## Usage in Pipeline

### For Script Improvement

```python
from research.python.story_pattern_analyzer import StoryPatternAnalyzer

# Analyze successful stories
analyzer = StoryPatternAnalyzer()
analyzer.analyze_batch(['story1.txt', 'story2.txt', 'story3.txt'])

# Get patterns
patterns = analyzer.extract_success_patterns()

# Use in generation
STORY_CONFIG = {
    'target_word_count': patterns['average_word_count'],
    'hook_max_words': 15,
    'use_dialogue': patterns['dialogue_usage'],
    'story_arc': patterns['typical_story_arc'],
}
```

### For Channel Research

```bash
# Scrape competitor channel (all videos)
python research/python/youtube_channel_scraper.py @competitorname --top 20

# Scrape ONLY story videos for story pattern analysis
python research/python/youtube_channel_scraper.py @competitorname --top 20 --story-only

# Analyze top performing videos
cd /tmp/youtube_channel_data
cat channel_report.md

# Use insights to improve content strategy
# - Check story video detection accuracy
# - Analyze story confidence scores
# - Identify patterns in successful story videos
```

## Requirements

Both tools require:
- Python 3.8+
- yt-dlp: `pip install yt-dlp`
- Standard library modules (no additional dependencies)

## Examples

### Analyze Downloaded Subtitles

```bash
# Download subtitles from DownSub.com or YouTube
# Place in a directory

# Run analysis
python research/python/story_pattern_analyzer.py /path/to/subtitles/*.txt

# View results
cat /tmp/story_patterns_report.md
```

### Scrape Channel Data

```bash
# Scrape top 10 videos from a channel
python research/python/youtube_channel_scraper.py @storytimechannel --top 10

# Scrape ONLY story videos (recommended for story generation pipeline)
python research/python/youtube_channel_scraper.py @storytimechannel --top 10 --story-only

# View results
cat /tmp/youtube_channel_data/channel_report.md

# Access raw data
cat /tmp/youtube_channel_data/channel_data.json
```

## Integration Points

### Current Pipeline

These tools complement the existing subtitle research:

1. **Subtitle Analysis** (`youtube_subtitle_analyzer.py`)
   - Analyzes subtitle timing and formatting
   - Focuses on technical specifications

2. **Story Pattern Analysis** (`story_pattern_analyzer.py`)
   - Analyzes story content and structure
   - Focuses on narrative patterns

3. **Channel Scraping** (`youtube_channel_scraper.py`)
   - Gathers competitive intelligence
   - Collects performance metrics

### Enhanced Workflow

```
1. Identify successful channels
   ↓
2. Scrape top videos (youtube_channel_scraper.py)
   ↓
3. Analyze subtitle patterns (youtube_subtitle_analyzer.py)
   ↓
4. Extract story patterns (story_pattern_analyzer.py)
   ↓
5. Apply findings to pipeline (GScript.py, GTitles.py)
   ↓
6. Validate against extracted rules
```

## Key Success Rules

From the analysis of 6 successful stories:

### 1. Hook Formula
- Start with immediate conflict or intrigue
- Keep it under 15 words
- Use action-oriented language
- Create curiosity gap

### 2. Story Length
- Target 632 words (±50 words)
- Break into ~67 sentences
- Keep sentences conversational (9-10 words average)

### 3. Structure Requirements
✅ Clear setup/introduction
✅ Immediate conflict presentation
✅ Progressive escalation
✅ Dramatic climax/turning point
✅ Satisfying resolution

### 4. Engagement Tactics
- Use dialogue (83% of successful stories do)
- Include emotional trigger words
- Show clear time progression
- Build conflict naturally
- Provide resolution/payoff

### 5. Content Guidelines
- Focus on relatable conflicts
- Include specific details and quotes
- Show character reactions
- Create justice/karma moments
- End with closure or lesson learned

## Further Research

Recommended next steps:

1. **Expand Dataset**
   - Analyze 20-50 more successful stories
   - Compare across different demographics
   - Track patterns over time

2. **A/B Testing**
   - Test different hook styles
   - Compare story lengths
   - Experiment with dialogue density

3. **Demographic Analysis**
   - Analyze patterns by age group
   - Compare men vs women preferences
   - Regional differences

4. **Performance Correlation**
   - Link patterns to view counts
   - Measure engagement metrics
   - Track retention rates

## References

- Sample stories analyzed from successful YouTube channels
- Subtitle files from high-performing videos
- Pattern extraction based on narrative structure theory
- Engagement optimization based on platform best practices

---

**Created:** October 2025
**Tools:** 2 Python scripts
**Analysis:** 6 successful stories
**Status:** Ready for use
