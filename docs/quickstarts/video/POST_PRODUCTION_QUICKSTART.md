# Post-Production Quick Start

Automated video post-production for 9:16 vertical videos (Instagram Reels, TikTok, YouTube Shorts).

## Quick Example

```python
from Generators.GVideoCompositor import VideoCompositor
from Models.StoryIdea import StoryIdea

# Initialize compositor with transitions enabled
compositor = VideoCompositor(
    enable_transitions=True,
    transition_duration=0.5
)

# Create final video with all post-production features
story = StoryIdea(story_title="My Story")
final_video = compositor.compose_final_video(
    story_idea=story,
    add_subtitles=True,
    background_music="path/to/music.mp3"
)
```

## What It Does

✅ **Crops to 9:16** - Converts videos to 1080x1920 vertical format  
✅ **Adds Subtitles** - Overlays SRT subtitles with custom styling  
✅ **Background Music** - Mixes music with voiceover at proper levels  
✅ **Smooth Transitions** - Concatenates clips with fade effects  
✅ **Ken Burns Effect** - Adds zoom/pan to static images  
✅ **Style Filters** - Applies cinematic filters for consistency  

## Run Tests

```bash
python test_post_production.py
```

All 7 tests should pass:
- Crop to 9:16 ✅
- Subtitle Overlay ✅
- Background Music ✅
- Smooth Transitions ✅
- Ken Burns Effect ✅
- Style Filters ✅
- Complete Pipeline ✅

## Requirements

System:
- FFmpeg installed (`sudo apt-get install ffmpeg` on Ubuntu)

Python packages:
- `ffmpeg-python==0.2.0`
- `Pillow==10.4.0`
- `moviepy==1.0.3`

Install all: `pip install -r requirements.txt`

## Full Documentation

See [POST_PRODUCTION.md](POST_PRODUCTION.md) for complete documentation including:
- Detailed feature descriptions
- API reference
- Usage examples
- Troubleshooting guide
- Technical specifications
