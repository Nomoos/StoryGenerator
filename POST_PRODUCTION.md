# Post-Production Automation

This document describes the automated post-production features for video generation.

## Overview

The post-production system automates the following tasks:
- **Crop clips to 9:16 aspect ratio** - Automatically converts videos to vertical format (1080x1920) for social media
- **Overlay SRT subtitles** - Adds styled subtitles from ASR output with customizable fonts and colors
- **Add background music** - Mixes background music with voiceover at appropriate volume levels
- **Concatenate clips with transitions** - Combines multiple video segments with smooth transitions
- **Apply Ken Burns effect** - Adds dynamic zoom/pan effects to static images
- **Style filters** - Applies consistent cinematic filters across all clips

## Features Implemented

### 1. Video Cropping to 9:16

The `VideoCompositor.crop_to_vertical()` method automatically crops and scales videos to 1080x1920 (9:16 aspect ratio) suitable for Instagram Reels, TikTok, and YouTube Shorts.

```python
from Generators.GVideoCompositor import VideoCompositor

compositor = VideoCompositor()
compositor.crop_to_vertical(
    input_video="input.mp4",
    output_video="output_vertical.mp4"
)
```

### 2. Subtitle Overlay

Subtitles are automatically converted from SRT to ASS format with custom styling optimized for vertical videos. The system:
- Converts SRT timestamps to ASS format
- Applies custom fonts and colors
- Positions subtitles appropriately for 9:16 videos
- Adds background/shadow for readability

```python
compositor._add_subtitles(
    video_path="video.mp4",
    subtitles_path="subtitles.txt",
    output_path="video_with_subs.mp4"
)
```

### 3. Background Music Integration

Background music is automatically mixed with voiceover audio at appropriate volume levels:

```python
compositor._add_background_music(
    video_path="video_with_audio.mp4",
    music_path="background_music.mp3",
    output_path="final_video.mp4",
    music_volume=0.1  # 10% volume for background music
)
```

### 4. Video Concatenation with Transitions

The system can concatenate multiple video segments with or without transitions:

```python
# Enable smooth transitions
compositor = VideoCompositor(
    enable_transitions=True,
    transition_duration=0.5  # 0.5 second crossfade
)

# Concatenate segments
compositor._concatenate_video_segments(
    segments_dir="video_segments/",
    output_path="concatenated.mp4"
)
```

### 5. Ken Burns Effect (Zoom & Pan)

Apply dynamic zoom and pan effects to static images:

```python
from Tools.VideoEffects import VideoEffects

effects = VideoEffects()
effects.apply_ken_burns_effect(
    input_image="image.jpg",
    output_video="output.mp4",
    audio_path="audio.mp3",
    duration=5.0,
    zoom_direction="in",  # 'in' or 'out'
    pan_direction="right"  # 'left', 'right', 'up', 'down', 'center'
)
```

Or use the compositor method:

```python
compositor.apply_ken_burns_to_segment(
    image_path="image.jpg",
    audio_path="audio.mp3",
    output_path="video.mp4",
    duration=5.0,
    zoom_direction="in",
    pan_direction="center"
)
```

### 6. Style Filters

Apply consistent cinematic filters across all clips:

```python
effects.apply_style_filter(
    input_video="input.mp4",
    output_video="output.mp4",
    filter_type="cinematic"  # 'cinematic', 'warm', 'cold', 'vintage', 'dramatic'
)
```

Available filter presets:
- **cinematic**: Vignette + balanced color grading
- **warm**: Inviting warm color temperature
- **cold**: Cool blue atmosphere
- **vintage**: Nostalgic faded look
- **dramatic**: High-contrast impact

## Complete Post-Production Pipeline

The `compose_final_video()` method orchestrates the entire post-production workflow:

```python
from Models.StoryIdea import StoryIdea
from Generators.GVideoCompositor import VideoCompositor

# Create compositor with options
compositor = VideoCompositor(
    output_format="mp4",
    enable_transitions=True,
    transition_duration=0.5,
    apply_ken_burns=False
)

# Compose final video
story_idea = StoryIdea(story_title="My Story")
final_video_path = compositor.compose_final_video(
    story_idea=story_idea,
    add_subtitles=True,
    background_music="path/to/music.mp3"
)
```

This method automatically:
1. ✅ Concatenates video segments (with optional transitions)
2. ✅ Adds voiceover audio
3. ✅ Overlays subtitles with custom styling
4. ✅ Mixes in background music at appropriate volume
5. ✅ Cleans up temporary files

## Testing

A comprehensive test suite validates all post-production features:

```bash
python test_post_production.py
```

Tests include:
- ✅ Crop to 9:16 aspect ratio
- ✅ Subtitle overlay with SRT files
- ✅ Background music mixing
- ✅ Smooth concatenation with transitions
- ✅ Ken Burns effect application
- ✅ Style filter consistency
- ✅ Complete pipeline integration

All tests create temporary videos and verify:
- Output file existence and non-zero size
- Correct video dimensions (1080x1920 for vertical videos)
- Audio/subtitle synchronization
- Style consistency

## Technical Details

### Video Specifications

All output videos conform to these specifications:
- **Resolution**: 1080x1920 (9:16 vertical)
- **Codec**: H.264 (libx264)
- **Video Bitrate**: 8 Mbps
- **Frame Rate**: 30 fps
- **Pixel Format**: yuv420p
- **Audio Codec**: AAC
- **Audio Bitrate**: 192k

### Subtitle Styling

ASS subtitle format is used with the following defaults:
- **Font**: Arial
- **Font Size**: 48px (scaled for 1080x1920 resolution)
- **Color**: White with black outline
- **Position**: Bottom margin of 150px
- **Alignment**: Bottom center

### Background Music Mixing

Audio mixing uses FFmpeg's `amix` filter:
- Voiceover volume: 100% (1.0)
- Music volume: 10-30% (0.1-0.3, configurable)
- Duration: Matches video length (music loops if needed)

## Dependencies

Required packages (from requirements.txt):
- `ffmpeg-python==0.2.0` - Python FFmpeg bindings
- `Pillow==10.4.0` - Image processing
- `moviepy==1.0.3` - Video editing (optional)

System requirements:
- `ffmpeg` - Must be installed and available in PATH

## Usage Examples

### Example 1: Basic Post-Production

```python
from Generators.GVideoCompositor import VideoCompositor
from Models.StoryIdea import StoryIdea

# Initialize compositor
compositor = VideoCompositor()

# Prepare story
story = StoryIdea(story_title="My First Story")

# Run post-production
final_video = compositor.compose_final_video(
    story_idea=story,
    add_subtitles=True
)

print(f"Final video created: {final_video}")
```

### Example 2: Advanced with Custom Options

```python
from Generators.GVideoCompositor import VideoCompositor
from Models.StoryIdea import StoryIdea

# Initialize with custom options
compositor = VideoCompositor(
    output_format="mp4",
    enable_transitions=True,      # Enable smooth transitions
    transition_duration=0.8,      # 0.8s crossfade
    apply_ken_burns=True          # Apply Ken Burns to images
)

# Prepare story
story = StoryIdea(story_title="Advanced Story")

# Run post-production with background music
final_video = compositor.compose_final_video(
    story_idea=story,
    add_subtitles=True,
    background_music="resources/music.mp3"
)

print(f"Final video with transitions and music: {final_video}")
```

### Example 3: Individual Operations

```python
from Generators.GVideoCompositor import VideoCompositor
from Tools.VideoEffects import VideoEffects

compositor = VideoCompositor()
effects = VideoEffects()

# 1. Crop video to vertical
compositor.crop_to_vertical("input.mp4", "vertical.mp4")

# 2. Apply Ken Burns effect to image
effects.apply_ken_burns_effect(
    "image.jpg", "video_kb.mp4", "audio.mp3", 
    duration=5.0, zoom_direction="in"
)

# 3. Add style filter
effects.apply_style_filter(
    "video_kb.mp4", "video_styled.mp4", 
    filter_type="cinematic"
)

# 4. Add subtitles
compositor._add_subtitles(
    "video_styled.mp4", "subs.txt", "video_final.mp4"
)
```

## Troubleshooting

### Common Issues

1. **FFmpeg not found**
   ```
   Solution: Install FFmpeg system-wide
   - Ubuntu/Debian: sudo apt-get install ffmpeg
   - macOS: brew install ffmpeg
   - Windows: Download from ffmpeg.org
   ```

2. **Video dimensions incorrect**
   ```
   Solution: Use crop_to_vertical() to ensure 9:16 aspect ratio
   compositor.crop_to_vertical(input, output)
   ```

3. **Audio/subtitle sync issues**
   ```
   Solution: Ensure subtitle timestamps match audio duration
   - Check SRT file timestamps
   - Verify audio file duration matches video
   ```

4. **Transitions not working**
   ```
   Solution: The system falls back to simple concatenation if xfade fails
   This is expected behavior to ensure reliability
   ```

## Performance Notes

- **Video processing is CPU-intensive** - Expect several minutes for a typical 60-second video
- **Transitions require re-encoding** - Simple concatenation is faster
- **Ken Burns effect** - Simplified version prioritizes reliability over complex animations
- **Test suite execution** - Takes ~30-60 seconds to run all tests

## Future Enhancements

Potential improvements for future releases:
- [ ] More transition types (wipe, slide, zoom)
- [ ] Advanced Ken Burns with true zoom/pan animation
- [ ] Subtitle animations (fade, slide, bounce)
- [ ] Multiple subtitle style presets
- [ ] Intro/outro template system
- [ ] Watermark positioning
- [ ] Multi-format export (different resolutions)
- [ ] GPU acceleration support

## Related Files

- `Python/Generators/GVideoCompositor.py` - Main compositor class
- `Python/Tools/VideoEffects.py` - Video effects utilities
- `Python/Tools/Utils.py` - Video rendering utilities
- `test_post_production.py` - Comprehensive test suite

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Review test examples in `test_post_production.py`
3. Open an issue on GitHub with:
   - FFmpeg version (`ffmpeg -version`)
   - Python version
   - Error messages and logs
   - Sample input files (if possible)
