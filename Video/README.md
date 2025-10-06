# Video Generation Pipeline

This module provides a complete video generation pipeline that integrates with the StoryGenerator system. It converts text stories and voiceovers into final videos with thumbnails and metadata.

## Features

### 1. **VideoRenderer** - Core Video Generation
- Renders videos from audio and images
- **Error Handling**: Automatic fallback to solid background if image generation fails
- **Metadata Embedding**: Embeds title, description, artist info
- **Thumbnail Generation**: Creates 1080x1920 thumbnails for social media
- Supports custom resolutions (default: 1080x1920 for vertical video)

### 2. **SceneComposer** - Scene Management
- Manages multiple scenes in a video
- Splits text into scenes automatically
- Supports transitions between scenes
- Saves/loads scene compositions

### 3. **VideoPipeline** - Batch Processing
- Processes multiple stories in batch
- **Parallel Processing**: Optional multi-threaded video generation
- **Error Recovery**: Continues processing even if individual videos fail
- Comprehensive statistics and reporting

## Architecture

```
Stories/
├── 3_VoiceOver/          # Input: Audio files + metadata
│   └── Story_Name/
│       ├── idea.json
│       ├── voiceover_normalized.mp3
│       └── Revised_with_eleven_labs_tags.txt
│
└── 5_Videos/             # Output: Final videos
    └── Story_Name/
        ├── final_video.mp4
        ├── thumbnail.jpg
        ├── metadata.json
        └── script.txt
```

## Usage

### Basic Usage - Process All Stories

```python
from Video.VideoPipeline import VideoPipeline

# Initialize pipeline
pipeline = VideoPipeline(
    max_workers=2,              # Number of parallel tasks
    default_resolution=(1080, 1920)  # Vertical video
)

# Process all stories
stats = pipeline.batch_process(
    parallel=False,             # Set True for parallel processing
    force_regenerate=False      # Set True to regenerate existing videos
)
```

### Manual Script

Run the manual script to process all voiceovers:

```bash
python Generation/Manual/MVideoPipeline.py
```

### Process Single Story

```python
from Video.VideoPipeline import VideoPipeline

pipeline = VideoPipeline()
success = pipeline.process_story(
    story_folder="My_Story_Name",
    force_regenerate=False,
    generate_thumbnail=True
)
```

### Using VideoRenderer Directly

```python
from Video.VideoRenderer import VideoRenderer

renderer = VideoRenderer(
    default_resolution=(1080, 1920),
    default_fps=30,
    default_bitrate="192k"
)

# Render video with fallback support
success = renderer.render_video(
    audio_file="path/to/audio.mp3",
    output_file="path/to/output.mp4",
    image_file="path/to/image.jpg",  # Optional - uses fallback if missing
    title="My Story",
    metadata={
        'title': 'My Story',
        'description': 'A great story',
        'artist': 'Nom'
    }
)

# Generate thumbnail
renderer.generate_thumbnail(
    video_file="path/to/video.mp4",
    output_file="path/to/thumbnail.jpg",
    timestamp=0.5
)
```

### Using SceneComposer

```python
from Video.SceneComposer import SceneComposer

composer = SceneComposer()

# Add scenes manually
composer.add_scene("Scene 1 text", duration=5.0, image_path="scene1.jpg")
composer.add_scene("Scene 2 text", duration=7.0, image_path="scene2.jpg")

# Or split text automatically
composer.split_text_into_scenes(
    text="Long story text...",
    total_duration=60.0,
    sentences_per_scene=2
)

# Save composition
composer.save_composition("composition.json")

# Validate scenes
if composer.validate_scenes():
    print(f"Ready to render {composer.get_scene_count()} scenes")
```

## Error Handling & Fallbacks

The pipeline includes multiple layers of error handling:

### 1. Image Fallback
If the background image is missing or fails to load:
- Automatically generates a solid color background
- Optionally adds the story title as text overlay
- Video generation continues without interruption

### 2. Audio Validation
Before rendering:
- Checks if audio file exists
- Validates file size (detects empty files)
- Reads duration to ensure valid audio

### 3. Batch Processing Resilience
- Individual failures don't stop the batch
- Detailed error reporting for each story
- Statistics track success/failure rates
- Option to clean up failed video files

### 4. Metadata Handling
If metadata is missing:
- Uses folder name as fallback title
- Continues with default description
- Saves available metadata to JSON file

## Configuration

### Video Settings

Default settings optimized for social media (TikTok, Instagram Reels, YouTube Shorts):

- **Resolution**: 1080x1920 (vertical)
- **FPS**: 30
- **Video Codec**: H.264 (libx264)
- **Audio Codec**: AAC
- **Audio Bitrate**: 192k
- **Pixel Format**: yuv420p (universal compatibility)

### Customization

```python
# Custom resolution (e.g., 1080x1080 for Instagram square)
pipeline = VideoPipeline(default_resolution=(1080, 1080))

# Custom renderer settings
renderer = VideoRenderer(
    default_resolution=(1920, 1080),  # Horizontal
    default_fps=24,                    # Cinematic
    default_bitrate="256k"             # Higher quality audio
)
```

## Integration Points

The video pipeline integrates with existing StoryGenerator components:

1. **After Text Generation** (GScript.py)
2. **After Voice Generation** (GVoice.py)
3. **Before Publishing** (Future: API upload modules)

### Pipeline Flow

```
1. Ideas → Scripts → Revised → Enhanced
                                  ↓
2. Voice Generation (TTS) → Normalized Audio
                                  ↓
3. Video Pipeline:
   - Load audio + metadata
   - Find/generate background image
   - Render video with metadata
   - Generate thumbnail
   - Save composition info
                                  ↓
4. Final Output: Videos ready for publishing
```

## Parallel Processing

For faster batch processing, enable parallel mode:

```python
stats = pipeline.batch_process(
    parallel=True,
    max_workers=4  # Process 4 videos simultaneously
)
```

**Note**: Parallel processing uses more CPU/memory but significantly speeds up batch operations.

## Cleanup

Remove incomplete or failed video files:

```python
pipeline = VideoPipeline()
cleaned = pipeline.cleanup_failed()
print(f"Removed {cleaned} failed video files")
```

## Future Enhancements

Planned features (not yet implemented):

- [ ] Multi-scene video composition with transitions
- [ ] Dynamic image generation from text prompts
- [ ] Subtitle/caption overlay
- [ ] Background music integration
- [ ] API upload to YouTube/TikTok/Instagram
- [ ] A/B testing with multiple thumbnails
- [ ] Video quality presets (draft/final)
- [ ] Progress webhooks/notifications

## Dependencies

Required packages:
- `ffmpeg-python` - Video processing
- `Pillow` - Image manipulation
- `pyloudnorm` - Audio normalization

System requirements:
- FFmpeg must be installed on the system
- Python 3.8+

## Troubleshooting

### FFmpeg Not Found
```bash
# Ubuntu/Debian
sudo apt-get install ffmpeg

# MacOS
brew install ffmpeg

# Windows
# Download from https://ffmpeg.org/download.html
```

### Empty Videos
Check that:
1. Audio file exists and is not empty
2. Audio file has valid duration
3. Background image path is correct or fallback is working

### Memory Issues with Parallel Processing
Reduce `max_workers` or disable parallel processing:
```python
pipeline = VideoPipeline(max_workers=1)
stats = pipeline.batch_process(parallel=False)
```

## License

Part of the StoryGenerator project.
