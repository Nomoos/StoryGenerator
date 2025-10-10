# Story Generator - Enhanced Features

This document describes the new enhancement features added to the Story Generator.

## Overview

The following enhancements have been implemented based on Step 6 requirements:

1. ✅ **Animated Transitions & Ken Burns Effect** - Zoom and pan on images
2. ✅ **Style Transfer & Filters** - Apply consistent mood and filters
3. ✅ **Background Music** - Add licensed/royalty-free background music
4. ✅ **Voice Inflection & Variation** - More expressive TTS with control parameters
5. ✅ **Multi-lingual Stories** - Support for multiple languages
6. ✅ **User Personalization** - Name insertion and customization

## New Features

### 1. Ken Burns Effect (Zoom & Pan)

The `VideoEffects` class in `Tools/VideoEffects.py` provides Ken Burns effect capabilities:

```python
from Tools.VideoEffects import VideoEffects

VideoEffects.apply_ken_burns_effect(
    input_image="path/to/image.jpg",
    output_video="path/to/output.mp4",
    audio_path="path/to/audio.mp3",
    duration=60.0,
    zoom_direction="in",  # or "out"
    pan_direction="right",  # "left", "right", "up", "down", "center"
    zoom_intensity=1.2
)
```

### 2. Video Style Filters

Apply cinematic filters for consistent mood:

```python
VideoEffects.apply_style_filter(
    input_video="path/to/video.mp4",
    output_video="path/to/filtered.mp4",
    filter_type="cinematic",  # "warm", "cold", "vintage", "dramatic"
    intensity=0.5
)
```

Available filters:
- **cinematic**: Slight vignette and color grading
- **warm**: Warm color temperature
- **cold**: Cool/blue tones
- **vintage**: Faded, nostalgic look
- **dramatic**: High contrast

### 3. Background Music

Add background music to videos with voice:

```python
VideoEffects.add_background_music(
    video_path="path/to/video.mp4",
    music_path="path/to/music.mp3",
    output_path="path/to/output.mp4",
    voice_volume=1.0,
    music_volume=0.3  # Lower for background
)
```

Or use the enhanced `convert_to_mp4` function:

```python
from Tools.Utils import convert_to_mp4

convert_to_mp4(
    mp3_file="voiceover.mp3",
    output_file="video.mp4",
    use_ken_burns=True,
    video_style="cinematic",
    background_music="path/to/music.mp3"
)
```

### 4. Voice Inflection & Variation

Control voice characteristics in `StoryIdea`:

```python
from Models.StoryIdea import StoryIdea

idea = StoryIdea(
    story_title="My Story",
    narrator_gender="female",
    voice_stability=0.5,  # 0.0-1.0, lower = more variation
    voice_similarity_boost=0.75,  # 0.0-1.0, higher = closer to voice
    voice_style_exaggeration=0.2,  # 0.0-1.0, style intensity
    # ... other fields
)
```

Parameters:
- **voice_stability** (0.0-1.0): Lower values add more variation and emotion
- **voice_similarity_boost** (0.0-1.0): How closely to match the voice model
- **voice_style_exaggeration** (0.0-1.0): Intensity of style application

### 5. Multi-lingual Support

Generate stories in different languages:

```python
idea = StoryIdea(
    story_title="El Secreto de Mi Hermana",
    narrator_gender="male",
    language="es",  # Language code: es, fr, de, it, pt, ja, ko, zh, ar, hi, ru
    # ... other fields
)
```

Supported languages:
- English (en)
- Spanish (es)
- French (fr)
- German (de)
- Italian (it)
- Portuguese (pt)
- Japanese (ja)
- Korean (ko)
- Chinese (zh)
- Arabic (ar)
- Hindi (hi)
- Russian (ru)

### 6. User Personalization

Insert custom names and values into stories:

```python
idea = StoryIdea(
    story_title="My Friend {friend_name} Changed My Life",
    narrator_gender="female",
    personalization={
        "friend_name": "Sarah",
        "city": "Seattle",
        "age": "sixteen"
    },
    # ... other fields
)
```

Use placeholders in curly braces `{placeholder}` anywhere in the story, and they will be replaced with the personalized values.

### 7. Video Style Presets

Set video style in `StoryIdea`:

```python
idea = StoryIdea(
    story_title="My Story",
    narrator_gender="female",
    video_style="cinematic",  # "warm", "cold", "vintage", "dramatic", "none"
    # ... other fields
)
```

## Usage Examples

### Example 1: Enhanced Video Generation

See `Generation/Manual/MConvertEnhanced.py`:

```python
python Generation/Manual/MConvertEnhanced.py
```

This creates multiple versions of videos with different effects.

### Example 2: Personalized Stories

See `Generation/Manual/MPersonalized.py`:

```python
python Generation/Manual/MPersonalized.py
```

Demonstrates:
- Personalized English stories
- Spanish language stories
- French language stories
- Multi-cultural personalized stories

### Example 3: Custom Video with All Features

```python
from Models.StoryIdea import StoryIdea
from Generators.GScript import ScriptGenerator
from Generators.GVoice import VoiceMaker
from Tools.Utils import convert_to_mp4
import os

# 1. Create personalized multi-lingual idea
idea = StoryIdea(
    story_title="When {protagonist} Met Love in {city}",
    narrator_gender="female",
    tone="romantic, dreamy",
    theme="first love",
    language="en",
    personalization={
        "protagonist": "Emma",
        "city": "Paris"
    },
    voice_stability=0.6,
    voice_similarity_boost=0.8,
    voice_style_exaggeration=0.2,
    video_style="cinematic"
)

# 2. Generate script
script_gen = ScriptGenerator()
script_gen.generate_from_storyidea(idea)

# 3. Generate voice with inflection
voice_maker = VoiceMaker()
voice_maker.generate_audio()

# 4. Create enhanced video
folder_name = sanitize_filename(idea.story_title)
mp3_path = os.path.join(VOICEOVER_PATH, folder_name, "voiceover_normalized.mp3")
video_path = os.path.join(TITLES_PATH, folder_name, "final_video.mp4")
music_path = os.path.join(RESOURCES_PATH, "background_music.mp3")

convert_to_mp4(
    mp3_file=mp3_path,
    output_file=video_path,
    use_ken_burns=True,
    video_style=idea.video_style,
    background_music=music_path if os.path.exists(music_path) else None
)
```

## File Structure

```
StoryGenerator/
├── Tools/
│   ├── Utils.py              # Enhanced with video effects
│   └── VideoEffects.py       # NEW: Video enhancement tools
├── Models/
│   └── StoryIdea.py          # Enhanced with new fields
├── Generators/
│   ├── GScript.py            # Enhanced with multi-lingual & personalization
│   └── GVoice.py             # Enhanced with voice inflection
└── Generation/Manual/
    ├── MConvertEnhanced.py   # NEW: Enhanced video conversion examples
    └── MPersonalized.py      # NEW: Personalization examples
```

## Configuration

### Background Music

Place royalty-free background music at:
```
Stories/Resources/background_music.mp3
```

### Voice Settings Recommendations

For different story types:

**Emotional/Dramatic:**
- voice_stability: 0.4-0.6
- voice_similarity_boost: 0.7-0.8
- voice_style_exaggeration: 0.2-0.4

**Calm/Informative:**
- voice_stability: 0.6-0.8
- voice_similarity_boost: 0.8-0.9
- voice_style_exaggeration: 0.0-0.1

**Energetic/Chaotic:**
- voice_stability: 0.3-0.5
- voice_similarity_boost: 0.6-0.7
- voice_style_exaggeration: 0.3-0.5

## Notes

- Background music should be royalty-free or properly licensed
- Ken Burns effect works best with high-resolution images
- Multi-lingual support requires appropriate TTS voices
- Personalization placeholders are case-sensitive
- Video filters can be combined with Ken Burns effect

## Future Enhancements

Potential additions not yet implemented:
- LTX-Video integration for AI-generated video backgrounds
- Multiple image transitions within a single video
- Interactive elements
- Advanced audio effects (reverb, echo)
- Text-to-speech emotion tagging
