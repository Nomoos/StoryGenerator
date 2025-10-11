# YouTube Video Subtitle Analysis Report

## Video Information
- **Video ID**: sample_emotional_story
- **Video URL**: https://example.com/sample
- **Analysis Date**: 2025-10-09 07:57:03

## Summary Statistics

### Segment Overview
- **Total Segments**: 10
- **Total Duration**: 26.50 seconds
- **Average Segment Duration**: 2.56 seconds
- **Min Segment Duration**: 2.40 seconds
- **Max Segment Duration**: 2.70 seconds

### Text Metrics
- **Average Words per Segment**: 9.6
- **Average Characters per Segment**: 47.2
- **Average Reading Speed**: 3.76 words/second

### Timing Analysis
- **Total Gaps**: 9
- **Average Gap Duration**: 0.100 seconds
- **Overlapping Segments**: 0

## Detailed Segment Breakdown

| Index | Start | End | Duration | Text | Words | Chars | WPS |
|-------|-------|-----|----------|------|-------|-------|-----|
| 1 | 0.00s | 2.50s | 2.50s | When I was 12, I found a letter in my dad's drawer... | 12 | 50 | 4.80 |
| 2 | 2.60s | 5.00s | 2.40s | It was from my mom who passed away when I was born... | 12 | 50 | 5.00 |
| 3 | 5.10s | 7.80s | 2.70s | She wrote it before she died, knowing she wouldn't... | 11 | 58 | 4.07 |
| 4 | 7.90s | 10.50s | 2.60s | "My darling, I'm so sorry I won't be there for you... | 11 | 51 | 4.23 |
| 5 | 10.60s | 13.20s | 2.60s | "But promise me you'll live the life I couldn't"... | 9 | 48 | 3.46 |
| 6 | 13.30s | 15.80s | 2.50s | "Dance in the rain, laugh until you cry"... | 8 | 40 | 3.20 |
| 7 | 15.90s | 18.50s | 2.60s | "And always remember, you were loved"... | 6 | 37 | 2.31 |
| 8 | 18.60s | 21.20s | 2.60s | I cried for hours holding that letter... | 7 | 37 | 2.69 |
| 9 | 21.30s | 24.00s | 2.70s | Now it's framed next to my bed, reminding me every... | 11 | 54 | 4.07 |
| 10 | 24.10s | 26.50s | 2.40s | That even in death, a mother's love never fades... | 9 | 47 | 3.75 |


## Key Findings

### Subtitle Duration Guidelines
Based on this video's analysis:
- Optimal segment duration: 2.56 seconds
- Recommended range: 2.40s - 2.70s

### Text Length Guidelines
- Words per segment: ~9 words
- Characters per segment: ~47 characters

### Reading Speed
- Average reading speed: 3.76 words/second
- This corresponds to about 226 words/minute

### Timing Recommendations
- Gap between segments: ~0.100 seconds
- Avoid overlapping segments (found 0 overlaps in this video)

## Application to StoryGenerator Pipeline

### Subtitle Timing Module (`Generators/GTitles.py`)
```python
# Recommended settings based on this analysis
SUBTITLE_CONFIG = {
    'min_duration': 2.40,
    'max_duration': 2.70,
    'target_duration': 2.56,
    'max_words_per_segment': 14,
    'max_chars_per_segment': 57,
    'gap_between_segments': 0.100,
    'target_reading_speed_wps': 3.76
}
```

### Quality Check Criteria
- ✅ Segment duration between 2.40s and 2.70s
- ✅ Reading speed around 3.76 words/second
- ✅ No overlapping segments
- ✅ Consistent gaps between segments (~0.100s)

