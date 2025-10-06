# StoryGenerator - Complete Pipeline Documentation

A complete pipeline for generating viral social media stories with automated text generation, voice-over, and video production.

## Overview

StoryGenerator automates the creation of short-form vertical videos optimized for TikTok, YouTube Shorts, and Instagram Reels. The pipeline handles everything from idea generation to final video output with thumbnails and metadata.

## Pipeline Architecture

```
1. Ideas Generation (0_Ideas/)
   ↓
2. Script Generation (1_Scripts/)
   ↓
3. Script Revision (2_Revised/)
   ↓
4. Voice Generation (3_VoiceOver/)
   ↓
5. Title Generation (4_Titles/)
   ↓
6. Video Generation (5_Videos/) ← NEW!
   ↓
7. Publishing (Future)
```

## New Features: Video Pipeline Integration (Step 4)

The video pipeline has been fully integrated with the following capabilities:

### ✅ Modular Components

1. **VideoRenderer** - Core video generation
   - Renders videos from audio and images
   - Automatic fallback to solid backgrounds
   - Metadata embedding
   - Thumbnail generation (1080x1920)

2. **SceneComposer** - Scene management
   - Multi-scene composition
   - Scene transitions
   - Automatic text-to-scene splitting

3. **VideoPipeline** - Batch processing
   - Process all stories at once
   - Parallel/sequential processing options
   - Error handling and recovery
   - Comprehensive statistics

### ✅ Error Handling & Fallbacks

- **Image Generation Failure**: Automatically creates solid color background with title text
- **TTS Failure**: Skips story and continues with batch processing
- **Missing Files**: Comprehensive validation before processing
- **Failed Videos**: Cleanup utilities to remove incomplete files

### ✅ Metadata & Thumbnails

- Embeds title, description, artist, and album metadata
- Generates 1080x1920 thumbnails (customizable)
- Saves metadata.json for reference
- Copies script to video folder

### ✅ Batch Processing

- Sequential or parallel processing
- Configurable worker threads
- Skip existing videos automatically
- Force regeneration option

## Installation

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Install FFmpeg

FFmpeg is required for video processing:

**Ubuntu/Debian:**
```bash
sudo apt-get install ffmpeg
```

**MacOS:**
```bash
brew install ffmpeg
```

**Windows:**
Download from [https://ffmpeg.org/download.html](https://ffmpeg.org/download.html)

### 3. Configure Paths

Update `Tools/Utils.py` with your story root path:

```python
STORY_ROOT = "C:\\Users\\YourName\\PROJECTS\\VideoMaking\\StoryGenerator\\Stories"
```

## Usage

### Complete Workflow

#### 1. Generate Ideas
```python
from Generators.GStoryIdeas import StoryIdeaGenerator

generator = StoryIdeaGenerator()
# Generate and save ideas
```

#### 2. Generate Scripts
```python
from Generators.GScript import ScriptGenerator
from Models.StoryIdea import StoryIdea

generator = ScriptGenerator()
idea = StoryIdea.from_file("path/to/idea.json")
generator.generate_from_storyidea(idea)
```

#### 3. Revise Scripts
```python
from Generators.GRevise import RevisedScriptGenerator

generator = RevisedScriptGenerator()
generator.Revise(idea)
```

#### 4. Enhance Scripts (Add Voice Tags)
```python
from Generators.GEnhanceScript import EnhanceScriptGenerator

generator = EnhanceScriptGenerator()
generator.Enhance(folder_name)
```

#### 5. Generate Voice-Overs
```python
from Generators.GVoice import VoiceMaker

maker = VoiceMaker()
maker.generate_audio()
maker.normalize_audio()
```

Or use the manual script:
```bash
python Generation/Manual/MVoice.py
```

#### 6. Generate Videos (NEW!)

**Recommended Method - Full Pipeline:**
```bash
python Generation/Manual/MVideoPipeline.py
```

**Programmatic Usage:**
```python
from Video.VideoPipeline import VideoPipeline

pipeline = VideoPipeline(
    max_workers=2,
    default_resolution=(1080, 1920)
)

# Process all stories
stats = pipeline.batch_process(
    parallel=False,
    force_regenerate=False
)

print(f"Success: {stats['successful']}/{stats['processed']}")
```

**Process Single Story:**
```python
pipeline = VideoPipeline()
success = pipeline.process_story(
    story_folder="My_Story_Name",
    generate_thumbnail=True
)
```

### Manual Processing Scripts

All manual scripts are in `Generation/Manual/`:

- `MIdea.py` - Generate ideas
- `MScript.py` - Generate scripts
- `MRevise.py` - Revise scripts
- `MEnhanceScript.py` - Add voice tags
- `MVoice.py` - Generate voice-overs
- `MVideoPipeline.py` - Generate videos (NEW!)
- `MConvertMP3ToMP4.py` - Legacy converter (now uses VideoRenderer)

## Project Structure

```
StoryGenerator/
├── Models/
│   └── StoryIdea.py              # Story data model
├── Generators/
│   ├── GStoryIdeas.py            # Idea generation
│   ├── GScript.py                # Script generation
│   ├── GRevise.py                # Script revision
│   ├── GEnhanceScript.py         # Voice tag enhancement
│   └── GVoice.py                 # Voice generation
├── Video/                         # NEW: Video pipeline
│   ├── VideoRenderer.py          # Core video rendering
│   ├── SceneComposer.py          # Scene management
│   ├── VideoPipeline.py          # Batch processing
│   └── README.md                 # Detailed video docs
├── Generation/Manual/
│   ├── MVideoPipeline.py         # NEW: Video pipeline script
│   └── ...                       # Other manual scripts
├── Tools/
│   └── Utils.py                  # Utilities and paths
└── Stories/                      # Output directory
    ├── 0_Ideas/
    ├── 1_Scripts/
    ├── 2_Revised/
    ├── 3_VoiceOver/
    ├── 4_Titles/
    └── 5_Videos/                 # NEW: Final videos
```

## Video Pipeline Features

### Resolution Options

Default is 1080x1920 (vertical), but you can customize:

```python
# Square (Instagram)
pipeline = VideoPipeline(default_resolution=(1080, 1080))

# Horizontal (YouTube)
pipeline = VideoPipeline(default_resolution=(1920, 1080))
```

### Parallel Processing

Speed up batch processing with parallel execution:

```python
stats = pipeline.batch_process(
    parallel=True,  # Enable parallel processing
    force_regenerate=False
)
```

**Note**: Parallel processing uses more CPU/memory but is significantly faster for large batches.

### Custom Video Settings

```python
from Video.VideoRenderer import VideoRenderer

renderer = VideoRenderer(
    default_resolution=(1080, 1920),
    default_fps=30,
    default_bitrate="256k"  # Higher quality audio
)
```

### Fallback Behavior

If the background image is missing:
1. Automatically generates a solid color (dark blue-gray) background
2. Adds story title as text overlay (centered, white)
3. Continues video generation without interruption
4. Logs warning about using fallback

### Metadata

Each video includes embedded metadata:
- Title (from StoryIdea)
- Description (generated from story attributes)
- Artist ("Nom")
- Album ("Noms Stories")

Metadata is also saved to `metadata.json` in the video folder for reference.

### Thumbnail Generation

Automatically generates thumbnails:
- Resolution: 1080x1920 (matches video)
- Extracted from video at 0.5 seconds
- Saved as `thumbnail.jpg` in video folder
- Can be customized or regenerated

## Configuration

### API Keys

API keys are required for:
- OpenAI (text generation): `Generators/GScript.py`
- ElevenLabs (voice generation): `Generators/GVoice.py`

**Note**: API keys should be stored securely (e.g., environment variables) in production.

### Story Root Path

Update `STORY_ROOT` in `Tools/Utils.py` to match your local setup:

```python
STORY_ROOT = "C:\\Users\\YourName\\PROJECTS\\VideoMaking\\StoryGenerator\\Stories"
```

### Video Settings

Default settings in `Video/VideoRenderer.py`:
- Resolution: 1080x1920 (vertical)
- FPS: 30
- Video Codec: H.264
- Audio Codec: AAC
- Audio Bitrate: 192k

## Future Enhancements

### Publishing Stage (Not Yet Implemented)

The next step is automated publishing:

1. **Platform APIs**:
   - YouTube Shorts upload
   - TikTok upload (via unofficial APIs)
   - Instagram Reels (via scheduling partners)

2. **Scheduling**:
   - Queue videos for optimal posting times
   - A/B testing with different thumbnails
   - Analytics integration

3. **Automation Considerations**:
   - Many platforms restrict automation
   - May require manual posting or scheduling partners
   - Check platform ToS before automating

### Other Future Features

- Multi-scene video composition with transitions
- Dynamic image generation from text prompts
- Subtitle/caption overlay
- Background music integration
- Video quality presets (draft/final)
- Progress webhooks/notifications

## Troubleshooting

### FFmpeg Not Found
Make sure FFmpeg is installed and in your PATH:
```bash
ffmpeg -version
```

### Empty Videos
Check:
1. Audio file exists and is not empty
2. Audio file has valid duration (use `ffprobe`)
3. Background image path is correct

### Memory Issues
If parallel processing causes memory issues:
```python
# Reduce workers
pipeline = VideoPipeline(max_workers=1)

# Or disable parallel processing
stats = pipeline.batch_process(parallel=False)
```

### Missing Dependencies
Install all required packages:
```bash
pip install -r requirements.txt
```

Check for missing system dependencies:
- FFmpeg
- DejaVu fonts (for fallback text rendering)

## Contributing

When adding new features:
1. Follow existing code structure
2. Add error handling and fallbacks
3. Update documentation
4. Test with edge cases

## License

[Your License Here]

## Credits

- Video pipeline by Copilot AI Assistant
- Story generation using OpenAI GPT models
- Voice generation using ElevenLabs
- Video processing with FFmpeg

---

For detailed video pipeline documentation, see [Video/README.md](Video/README.md)
