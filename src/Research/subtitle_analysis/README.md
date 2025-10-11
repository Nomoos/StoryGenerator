# YouTube Shorts Subtitle Analysis Examples

This directory contains analysis examples of subtitle patterns commonly used in YouTube Shorts and short-form video content.

## Sample Files

### 1. `sample_emotional_story.srt`
**Pattern**: Phrase-based with moderate pace
- **Duration**: 26.5 seconds
- **Style**: Emotional storytelling
- **Reading Speed**: 3.76 WPS (fast but readable)
- **Segment Count**: 10
- **Key Features**:
  - Consistent segment duration (~2.5s)
  - Natural phrase breaks
  - 9-10 words per segment
  - 100ms gaps between segments

**Use Case**: Dramatic storytelling, emotional content, narrated videos

### 2. `sample_fast_paced_action.srt` (Example Pattern)
**Pattern**: Quick cuts, word-by-word highlighting
- **Duration**: 15 seconds
- **Style**: High energy, rapid delivery
- **Reading Speed**: 4.5+ WPS
- **Segment Count**: 20-25
- **Key Features**:
  - Short segments (1-1.5s)
  - 2-4 words per segment
  - Minimal gaps
  - Dynamic, attention-grabbing

**Use Case**: Action sequences, viral trends, TikTok-style content

### 3. `sample_tutorial_slow.srt` (Example Pattern)
**Pattern**: Clear instruction, slower pace
- **Duration**: 45 seconds
- **Style**: Educational, instructional
- **Reading Speed**: 2.0 WPS
- **Segment Count**: 12-15
- **Key Features**:
  - Longer segments (3-4s)
  - 6-8 words per segment
  - Emphasis on key terms
  - Pauses for comprehension

**Use Case**: How-to videos, educational content, tutorials

## Analysis Results Summary

### Optimal Settings by Content Type

#### Emotional/Storytelling Content
```python
SUBTITLE_CONFIG = {
    'target_duration': 2.5,
    'target_words': 9,
    'reading_speed_wps': 3.5,
    'gap_duration': 0.1,
    'style': 'phrase-based'
}
```

#### Fast-Paced/Viral Content
```python
SUBTITLE_CONFIG = {
    'target_duration': 1.2,
    'target_words': 3,
    'reading_speed_wps': 4.5,
    'gap_duration': 0.05,
    'style': 'word-by-word'
}
```

#### Educational/Tutorial Content
```python
SUBTITLE_CONFIG = {
    'target_duration': 3.5,
    'target_words': 7,
    'reading_speed_wps': 2.0,
    'gap_duration': 0.2,
    'style': 'phrase-based-slow'
}
```

## Key Insights

### Reading Speed Correlations

| Content Type | WPS | Engagement | Readability |
|--------------|-----|------------|-------------|
| Educational | 2.0 | Medium | Excellent |
| Storytelling | 3.5 | High | Good |
| Viral/Action | 4.5 | Very High | Moderate |
| Too Fast | >5.0 | Low | Poor |

### Segment Duration Sweet Spots

- **1.0-1.5s**: Word-level highlights, very fast content
- **1.5-2.5s**: Standard short-form video pace
- **2.5-3.5s**: Storytelling, emotional content
- **3.5-5.0s**: Educational, complex information
- **>5.0s**: Too long, viewer attention drops

### Character Limits by Platform

```
YouTube Shorts:  ~50 chars (2 lines max)
TikTok:         ~40 chars (1-2 lines)
Instagram Reels: ~45 chars (2 lines max)
```

## Styling Patterns Observed

### Pattern A: High-Contrast Simple
```css
Background: None or subtle shadow
Text Color: White (#FFFFFF)
Outline: Black, 3-4px
Font: Arial Bold, 60-70px
```
**Best for**: Clear backgrounds, minimal interference

### Pattern B: Box Background
```css
Background: Semi-transparent black (rgba(0,0,0,0.7))
Text Color: White (#FFFFFF)
Padding: 10-15px
Font: Arial Bold, 60-70px
```
**Best for**: Busy backgrounds, guaranteed readability

### Pattern C: Emphasis Highlighting
```css
Default: White (#FFFFFF)
Emphasis: Yellow (#FFD700) or Red (#FF4444)
Background: Semi-transparent black
Font: Montserrat Bold, 65-75px
```
**Best for**: Key words, emotional emphasis, viral content

## Implementation Recommendations

### For StoryGenerator Pipeline

1. **Default to Pattern: Emotional Storytelling**
   - Target demographic (10-30) prefers this style
   - Good balance of pace and readability
   - Works well across platforms

2. **Segment Breaking Algorithm**
   ```python
   def break_into_segments(words, target_duration=2.5, wps=3.5):
       target_words = int(target_duration * wps)
       # Break at natural pauses (punctuation)
       # Aim for target_words ± 2
       # Never exceed 50 characters
   ```

3. **Quality Validation**
   ```python
   def validate_segment(seg):
       checks = {
           'duration': 1.0 < seg.duration < 5.0,
           'words': 3 <= seg.word_count <= 12,
           'chars': seg.char_count <= 50,
           'wps': 2.0 <= seg.wps <= 4.5,
       }
       return all(checks.values())
   ```

4. **Adaptive Styling**
   - Detect scene brightness
   - Adjust subtitle color/background
   - Ensure minimum contrast ratio (4.5:1)

## Testing Methodology

To evaluate subtitle effectiveness:

1. **Readability Test**
   - Display on 6" mobile screen
   - Verify all text readable at arm's length
   - Test with various background brightnesses

2. **Timing Test**
   - Verify synchronization with audio (±100ms)
   - Check no overlaps or large gaps
   - Ensure natural reading rhythm

3. **Engagement Test**
   - Monitor viewer retention at subtitle transitions
   - A/B test different styles
   - Track completion rate

## Sample Analysis Output

See `sample_emotional_story_analysis.json` for complete analysis output including:
- Per-segment metrics
- Timing statistics
- Reading speed analysis
- Gap/overlap detection
- Quality recommendations

## Further Research

Areas requiring additional investigation:

1. **Multi-language Support**
   - Character limits vary by language
   - Reading speeds differ culturally
   - Font rendering for non-Latin scripts

2. **Accessibility**
   - WCAG 2.1 compliance
   - Color blind friendly palettes
   - Screen reader compatibility

3. **Platform-Specific Optimization**
   - YouTube Shorts algorithm preferences
   - TikTok engagement patterns
   - Instagram Reels best practices

4. **Dynamic Adaptation**
   - Real-time style adjustments
   - AI-powered emphasis detection
   - Sentiment-based color selection

## References

- Sample analysis tool: `youtube_subtitle_analyzer.py`
- Research documentation: `../YOUTUBE_SUBTITLE_RESEARCH.md`
- Pipeline integration: `../../obsolete/issues/step-08-subtitle-timing/`
- Quality checks: `../../obsolete/issues/step-12-quality-checks/`

---

**Last Updated**: October 2025
**Tools Used**: yt-dlp, WhisperX, FFmpeg
**Analysis Count**: 1 sample (emotional storytelling pattern)
