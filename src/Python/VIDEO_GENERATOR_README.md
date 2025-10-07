# Video Generator - Short Video Creation Pipeline

## Overview

The Video Generator implements a minimal pipeline for creating short-form vertical videos (1080×1920) suitable for TikTok, YouTube Shorts, and Instagram Reels.

## Pipeline Flow

```
story_text + (optional images) → audio (voice) + visuals → alignment/subtitles → assembly & rendering → final video
```

### Integration with Existing Generators

1. **Story Generation** (`GScript`) - Creates 100-200 word stories
2. **Voice Generation** (`GVoice`) - Generates audio using ElevenLabs TTS
3. **Subtitle Alignment** (`GTitles`) - Creates word-by-word subtitles using WhisperX
4. **Video Assembly** (`GVideo`) - **NEW** - Combines audio, visuals, and subtitles into final video

## Installation

Install required dependencies:

```bash
pip install -r requirements.txt
```

New dependencies added:
- `moviepy==1.0.3` - Video editing and assembly
- `Pillow==10.4.0` - Image processing

## Usage

### Batch Video Generation

Process all stories in the TITLES_PATH folder:

```python
from Generators.GVideo import VideoGenerator

generator = VideoGenerator(width=1080, height=1920, fps=30)
generator.batch_create_videos()
```

Or use the manual script:

```bash
python Generation/Manual/MVideo.py
```

### Single Video Generation

Create video for a specific story folder:

```python
from Generators.GVideo import VideoGenerator

generator = VideoGenerator()
generator.create_video_from_folder("My_Story_Title")
```

### Custom Background Image

Use a custom background image instead of the default:

```python
generator = VideoGenerator()
generator.batch_create_videos(background_image="/path/to/image.jpg")
```

## Output Format

- **Resolution**: 1080×1920 (portrait/vertical)
- **Frame Rate**: 30 fps
- **Video Codec**: H.264
- **Audio Codec**: AAC
- **Bitrate**: 5000k
- **Format**: MP4

## Video Structure

Each video consists of:

1. **Background Image**: Static or custom image scaled to 1080×1920
2. **Audio Track**: Voiceover from GVoice (normalized MP3)
3. **Subtitle Overlay**: Word-by-word captions from GTitles
   - Font: Arial, 48pt
   - Color: White with black stroke
   - Position: 80% down the screen
   - Timing: Synced with audio using WhisperX alignment

## File Organization

The generator expects the following structure in each story folder under `TITLES_PATH`:

```
Stories/4_Titles/My_Story_Title/
├── voiceover_normalized.mp3      # Audio from GVoice
├── Subtitles_Word_By_Word.txt    # SRT subtitles from GTitles
└── video_final.mp4                # OUTPUT: Final video
```

Background images are stored in:
```
Stories/Resources/baground.jpg
```

## API Reference

### VideoGenerator Class

#### `__init__(width=1080, height=1920, fps=30)`

Initialize the video generator with custom dimensions and frame rate.

**Parameters:**
- `width` (int): Video width in pixels (default: 1080)
- `height` (int): Video height in pixels (default: 1920)
- `fps` (int): Frames per second (default: 30)

#### `make_scene_clip(image_path, subtitle, start, duration)`

Create a single scene clip with image and subtitle overlay.

**Parameters:**
- `image_path` (str): Path to background image
- `subtitle` (str): Text to display as subtitle
- `start` (float): Start time in seconds
- `duration` (float): Duration in seconds

**Returns:** `CompositeVideoClip` with image and text overlay

#### `parse_srt_file(srt_path)`

Parse SRT subtitle file into segments.

**Parameters:**
- `srt_path` (str): Path to SRT file

**Returns:** List of subtitle segments with text, start, and end times

#### `assemble_video(scenes, audio_path, output_path)`

Assemble final video from scenes and audio.

**Parameters:**
- `scenes` (list): List of scene dictionaries with keys:
  - `image`: path to background image
  - `text`: subtitle text
  - `start`: start time in seconds
  - `duration`: duration in seconds
- `audio_path` (str): Path to audio file (MP3)
- `output_path` (str): Path for output video file

#### `create_video_from_folder(folder_name, background_image=None)`

Create video from a story folder in TITLES_PATH.

**Parameters:**
- `folder_name` (str): Name of folder in TITLES_PATH
- `background_image` (str, optional): Path to background image

#### `batch_create_videos(background_image=None)`

Create videos for all folders in TITLES_PATH.

**Parameters:**
- `background_image` (str, optional): Path to background image for all videos

## Example Workflow

Complete workflow from story idea to final video:

```python
from Models.StoryIdea import StoryIdea
from Generators.GScript import ScriptGenerator
from Generators.GVoice import VoiceMaker
from Generators.GTitles import TitleGenerator
from Generators.GVideo import VideoGenerator

# 1. Generate story script
idea = StoryIdea(story_title="My Story", narrator_gender="female")
script_gen = ScriptGenerator()
script_gen.generate_from_storyidea(idea)

# 2. Generate voiceover
voice_maker = VoiceMaker()
voice_maker.generate_audio()
voice_maker.normalize_audio()

# 3. Generate subtitles
title_gen = TitleGenerator()
title_gen.generate_titles()

# 4. Generate video
video_gen = VideoGenerator()
video_gen.batch_create_videos()
```

## Advanced Usage

### Custom Video Settings

Fine-tune encoding with FFmpeg directly:

```bash
ffmpeg -i input.mp4 \
  -c:v libx264 -preset slow -crf 20 \
  -c:a aac -b:a 128k \
  -pix_fmt yuv420p \
  -vf "scale=1080:1920,format=yuv420p" \
  output.mp4
```

**Parameters:**
- `crf`: Quality (18-23 recommended, lower = better quality)
- `preset`: Encoding speed (slow/medium/fast)
- `b:a`: Audio bitrate (128k recommended)

### Multiple Scene Support

For future enhancements with multiple images per video:

```python
scenes = [
    {
        'image': '/path/to/scene1.jpg',
        'text': 'Opening scene',
        'start': 0.0,
        'duration': 5.0
    },
    {
        'image': '/path/to/scene2.jpg',
        'text': 'Middle scene',
        'start': 5.0,
        'duration': 5.0
    },
]

generator.assemble_video(scenes, audio_path, output_path)
```

## Troubleshooting

### Font Not Found Error

If you see font-related errors, ensure Arial is installed or modify the font in `make_scene_clip()`:

```python
txt = TextClip(
    subtitle,
    fontsize=48,
    color='white',
    stroke_color='black',
    stroke_width=2,
    method='caption',
    size=(int(self.width * 0.9), None),
    font='DejaVu-Sans'  # Alternative font
)
```

### Video Not Creating

Check that all required files exist:
1. `voiceover_normalized.mp3` - Run GVoice first
2. `Subtitles_Word_By_Word.txt` - Run GTitles first
3. Background image in `Resources/baground.jpg`

### Memory Issues

For large batches, process one video at a time or reduce video quality:

```python
generator = VideoGenerator()
for folder in folders:
    generator.create_video_from_folder(folder)
    # Memory is freed after each video
```

## Performance Tips

1. **Use SSD storage** for faster I/O during rendering
2. **Adjust thread count** in `write_videofile()` based on CPU cores
3. **Lower bitrate** for faster encoding: `bitrate='3000k'`
4. **Use 'fast' preset** instead of 'medium' for quicker renders

## Future Enhancements

Potential improvements to the pipeline:

1. **Multi-scene support**: Different images for different parts of the story
2. **Transition effects**: Fade in/out between scenes
3. **Dynamic text animations**: Word-by-word reveal with effects
4. **Background music**: Add ambient music track
5. **Logo overlay**: Add branding to videos
6. **Batch optimization**: Parallel processing with multiprocessing
7. **Cloud rendering**: Integration with cloud video processing services

## License

Part of the StoryGenerator project.
