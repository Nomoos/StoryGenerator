# YouTube Video Subtitle Research Guide

## Purpose

This guide documents research findings on YouTube video subtitles, particularly for short-form content (YouTube Shorts, TikTok, Instagram Reels), to inform the subtitle generation system in the StoryGenerator pipeline.

## Research Tool

The `youtube_subtitle_analyzer.py` tool in this directory can be used to analyze YouTube videos and extract subtitle metrics. See the tool documentation for usage details.

### Usage

```bash
# Analyze any YouTube video or Short
python research/python/youtube_subtitle_analyzer.py <youtube_url>

# Example
python research/python/youtube_subtitle_analyzer.py https://www.youtube.com/shorts/41QD8C6tqIU
```

### Requirements

- Python 3.8+
- yt-dlp (`pip install yt-dlp`)
- ffmpeg

## General Subtitle Guidelines for Short-Form Video

Based on research of popular YouTube Shorts and short-form content:

### Timing Specifications

| Metric | Recommendation | Notes |
|--------|---------------|-------|
| **Segment Duration** | 1.5 - 3.5 seconds | Optimal reading time for mobile viewers |
| **Minimum Duration** | 0.8 seconds | Below this, text becomes hard to read |
| **Maximum Duration** | 5.0 seconds | Above this, viewer attention drops |
| **Gap Between Segments** | 0.05 - 0.2 seconds | Brief pause for mental processing |
| **Words per Segment** | 3 - 8 words | Fits on mobile screen without crowding |
| **Characters per Segment** | 30 - 50 characters | Readable at subtitle font sizes |

### Reading Speed

| Speed | Words per Second | Use Case |
|-------|-----------------|----------|
| **Slow** | 1.5 - 2.0 WPS | Emphasis, dramatic moments |
| **Normal** | 2.0 - 3.0 WPS | Standard narration |
| **Fast** | 3.0 - 4.0 WPS | Action sequences, excitement |
| **Too Fast** | > 4.0 WPS | Avoid - hard to read |

### Text Length Constraints

```
For 9:16 vertical video (1080×1920):
- Maximum 2 lines of text
- 42 characters per line maximum
- Font size: 60-80px (for readability on mobile)
- Line height: 1.2-1.4x font size
```

### Subtitle Positioning

```
Top Margin: 8% of screen height (clear of UI elements)
Bottom Margin: 10% of screen height (clear of UI elements)
Horizontal: Centered
Background: Semi-transparent box or strong outline/shadow
```

## Subtitle Style Patterns

### Pattern 1: Word-by-Word Highlighting
- Each word appears and is highlighted in sequence
- Duration per word: 0.2-0.4 seconds
- Creates dynamic, engaging effect
- Popular on TikTok and Instagram

### Pattern 2: Phrase-Based
- Complete phrases appear at once
- Duration: 1.5-3.0 seconds per phrase
- More traditional, easier to read
- Common on YouTube Shorts

### Pattern 3: Karaoke Style
- Full sentence visible, words highlight as spoken
- Combines readability with timing precision
- Good for music or rhythmic content

## Color and Styling

### High-Contrast Schemes

```css
/* White on dark/video background */
color: #FFFFFF
background: rgba(0, 0, 0, 0.7)
outline: 3px black

/* Yellow accent (high attention) */
color: #FFD700
background: rgba(0, 0, 0, 0.8)
outline: 3px black

/* Multi-color (emphasis) */
primary: #FFFFFF
emphasis: #FFD700 or #FF6B6B
background: rgba(0, 0, 0, 0.7)
```

### Font Recommendations

1. **Arial Bold** - Clean, readable, universal
2. **Montserrat Bold** - Modern, stylish
3. **Impact** - High impact, attention-grabbing
4. **Bebas Neue** - Tall, condensed, dramatic

## Implementation for StoryGenerator

### Configuration Template

```python
SUBTITLE_CONFIG = {
    # Timing
    'min_duration': 0.8,          # seconds
    'max_duration': 5.0,          # seconds
    'target_duration': 2.5,       # seconds
    'gap_between_segments': 0.1,  # seconds
    
    # Text constraints
    'max_words_per_segment': 8,
    'max_chars_per_segment': 50,
    'max_lines': 2,
    
    # Reading speed
    'target_reading_speed_wps': 2.5,  # words per second
    'min_reading_speed_wps': 1.5,
    'max_reading_speed_wps': 3.5,
    
    # Positioning (percentage of screen height)
    'top_margin': 0.08,
    'bottom_margin': 0.10,
    'horizontal_align': 'center',
    
    # Styling
    'font_family': 'Arial Bold',
    'font_size': 70,              # pixels for 1080x1920
    'font_color': '#FFFFFF',
    'outline_color': '#000000',
    'outline_width': 3,
    'background_opacity': 0.7,
    
    # Animation
    'fade_in_duration': 0.1,
    'fade_out_duration': 0.1,
}
```

### Quality Checks

```python
def validate_subtitle_segment(segment):
    """
    Validate a subtitle segment against best practices.
    
    Returns: (is_valid, warnings)
    """
    warnings = []
    
    # Check duration
    if segment.duration < 0.8:
        warnings.append(f"Duration too short: {segment.duration:.2f}s")
    elif segment.duration > 5.0:
        warnings.append(f"Duration too long: {segment.duration:.2f}s")
    
    # Check word count
    word_count = len(segment.text.split())
    if word_count > 8:
        warnings.append(f"Too many words: {word_count}")
    
    # Check character count
    if len(segment.text) > 50:
        warnings.append(f"Too many characters: {len(segment.text)}")
    
    # Check reading speed
    wps = word_count / segment.duration if segment.duration > 0 else 0
    if wps > 3.5:
        warnings.append(f"Reading speed too fast: {wps:.2f} WPS")
    elif wps < 1.5:
        warnings.append(f"Reading speed too slow: {wps:.2f} WPS")
    
    return len(warnings) == 0, warnings
```

## Research Sources

### Analyzed Videos

1. **YouTube Shorts** - General entertainment, storytelling
   - Typical duration: 15-60 seconds
   - Subtitle style: Phrase-based with emphasis words
   - Average segment duration: 2-3 seconds

2. **TikTok** - Viral content, trends
   - Typical duration: 15-60 seconds
   - Subtitle style: Word-by-word highlighting
   - Fast-paced, high energy

3. **Instagram Reels** - Lifestyle, tutorial content
   - Typical duration: 15-90 seconds
   - Subtitle style: Phrase-based, clean
   - Professional, polished look

### Key Learnings

1. **Mobile-First Design**: All subtitle decisions should prioritize mobile viewing experience
2. **High Contrast**: Subtitles must be readable over any background
3. **Brevity**: Keep subtitle segments short and punchy
4. **Timing Precision**: Word-level timing creates professional polish
5. **Consistent Style**: Maintain consistent formatting throughout video
6. **Safe Zones**: Avoid top/bottom screen areas (UI overlays)

## Integration Points

### Current Pipeline Integration

```
Step 6: ASR & Subtitle Generation (GTitles.py)
├── Input: Normalized audio (3_VoiceOver/)
├── Process: WhisperX word-level alignment
└── Output: SRT files (4_Titles/)
    ├── Word-level timestamps
    ├── Grouped into phrases
    └── Validated against guidelines

Step 9: Post-Production (Planned)
├── Input: Video + SRT files
├── Process: Subtitle overlay with styling
└── Output: Final video with burned-in subtitles
    ├── FFmpeg subtitle filter
    ├── ASS/SSA styling
    └── Quality validation
```

### Recommended Enhancements

1. **Dynamic Styling**
   - Emphasize key words with color changes
   - Animate important phrases
   - Adjust font size for impact words

2. **Smart Phrase Breaking**
   - Use natural speech pauses
   - Respect sentence structure
   - Consider emotional beats

3. **Adaptive Timing**
   - Adjust based on content density
   - Slow down for complex information
   - Speed up for action sequences

4. **Background Adaptation**
   - Detect bright/dark backgrounds
   - Adjust subtitle colors accordingly
   - Ensure minimum contrast ratio

## Testing Checklist

When implementing subtitle system:

- [ ] Subtitles readable on mobile (6" screen)
- [ ] Duration between 1-4 seconds per segment
- [ ] No more than 8 words per segment
- [ ] Reading speed 2-3 WPS average
- [ ] High contrast against all backgrounds
- [ ] No overlapping segments
- [ ] Consistent gaps between segments
- [ ] Safe margins respected (top 8%, bottom 10%)
- [ ] Font size appropriate (60-80px for 1080x1920)
- [ ] Synchronization accurate (±100ms tolerance)

## Sample Code

### Generate Subtitle Overlay with FFmpeg

```bash
# Basic subtitle overlay
ffmpeg -i input.mp4 -vf "subtitles=subtitles.srt:force_style='FontName=Arial Bold,FontSize=70,PrimaryColour=&HFFFFFF&,OutlineColour=&H000000&,Outline=3,Shadow=0,MarginV=100'" output.mp4

# Advanced styling with background box
ffmpeg -i input.mp4 -vf "subtitles=subtitles.ass" output.mp4
```

### Create ASS-styled Subtitles

```python
def create_ass_subtitles(srt_path, ass_path, style_config):
    """
    Convert SRT to ASS format with advanced styling.
    """
    ass_header = f"""[Script Info]
Title: StoryGenerator Subtitles
ScriptType: v4.00+

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,{style_config['font']},{style_config['size']},&HFFFFFF&,&HFFFFFF&,&H000000&,&H80000000&,-1,0,0,0,100,100,0,0,1,3,0,2,10,10,100,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    
    # Parse SRT and convert to ASS format
    # ... implementation
    
    with open(ass_path, 'w', encoding='utf-8') as f:
        f.write(ass_header)
        # Write dialogue lines
```

## Future Research

Areas for continued investigation:

1. **Accessibility**
   - WCAG compliance for subtitles
   - Support for multiple languages
   - Subtitle positioning preferences

2. **Platform-Specific Optimization**
   - TikTok style trends
   - Instagram Reels formatting
   - YouTube Shorts requirements

3. **AI-Powered Enhancements**
   - Automatic emphasis detection
   - Sentiment-based styling
   - Context-aware positioning

4. **Performance Metrics**
   - Correlation between subtitle style and engagement
   - A/B testing different formats
   - Viewer retention analysis

## References

- [YouTube Creator Academy - Subtitles Best Practices](https://creatoracademy.youtube.com/)
- [WCAG 2.1 Guidelines for Captions](https://www.w3.org/WAI/WCAG21/Understanding/)
- [TikTok Creator Portal - Accessibility](https://www.tiktok.com/creators/)
- WhisperX Documentation - Word-level alignment
- FFmpeg Documentation - Subtitle filters

## Conclusion

Effective subtitle implementation requires balancing readability, timing precision, and aesthetic appeal. The guidelines in this document provide a foundation for creating professional-quality subtitles optimized for short-form vertical video content.

Key priorities:
1. Mobile-first readability
2. Precise word-level timing
3. High contrast styling
4. Natural phrase breaking
5. Platform-appropriate formatting

By following these guidelines, the StoryGenerator pipeline can produce videos with subtitles that enhance rather than distract from the content.
