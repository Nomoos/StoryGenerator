# Video Clip Generation

This module generates video clips for shots using either **LTX-Video** (Variant A) or **Frame Interpolation** (Variant B).

## Features

- **Variant A: LTX-Video Generation**
  - Generates 10-20 second clips per shot
  - Uses AI image-to-video models (Stable Video Diffusion, LTX-Video)
  - Saves to `/videos/ltx/{segment}/{age}/{title_id}/shot_{k}.mp4`

- **Variant B: Frame Interpolation**
  - Interpolates between keyframes using RIFE/DAIN/FILM
  - Assembles smooth video clips from keyframes
  - Saves to `/videos/interp/{segment}/{age}/{title_id}/shot_{k}.mp4`

- **Configuration-Driven**
  - Uses `switches.use_ltx` in `pipeline.yaml` to control default method
  - Supports command-line overrides
  - Reproducible with seed control

## Quick Start

### 1. Configuration

The `data/config/pipeline.yaml` file contains the switches to control video generation:

```yaml
# Feature Switches
switches:
  use_ltx: true              # Use LTX-Video (true) or interpolation (false)
  use_interpolation: false   # Enable interpolation variant
```

### 2. Prepare Shot Data

Create a YAML file with your shot descriptions:

```yaml
# examples/video_clips/example_shots.yaml
shots:
  - image_path: "keyframes/shot_000.png"
    motion: "slow zoom in"
    intensity: 0.3
    duration: 10.0
  
  - image_path: "keyframes/shot_001.png"
    motion: "pan right"
    intensity: 0.5
    duration: 12.0
  
  - keyframes:
      - "keyframes/shot_002_kf1.png"
      - "keyframes/shot_002_kf2.png"
    duration: 15.0

metadata:
  segment: "tech"
  age: "18-23"
  title_id: "ai_revolution_2024"
```

### 3. Generate Clips

#### Using Python Module

```python
from generate_video_clips import VideoClipGenerator

# Initialize generator (uses config defaults)
generator = VideoClipGenerator()

# Define shots
shots = [
    {
        "image_path": "keyframe_001.png",
        "motion": "zoom in",
        "intensity": 0.5,
        "duration": 10.0
    },
    {
        "keyframes": ["keyframe_002a.png", "keyframe_002b.png"],
        "duration": 12.0
    }
]

# Generate clips for a story
clip_paths = generator.generate_clips_for_story(
    shots=shots,
    segment="tech",
    age="18-23",
    title_id="my_story_001",
    base_output_dir="videos"
)

print(f"Generated {len(clip_paths)} clips")

# Clean up
generator.cleanup()
```

#### Using Command Line

```bash
# Generate clips using LTX-Video (default from config)
python src/research/python/generate_video_clips.py \
  --shots examples/video_clips/example_shots.yaml \
  --segment tech \
  --age 18-23 \
  --title-id ai_revolution_2024

# Force use of frame interpolation
python src/research/python/generate_video_clips.py \
  --shots examples/video_clips/example_shots.yaml \
  --segment tech \
  --age 18-23 \
  --title-id ai_revolution_2024 \
  --use-interpolation

# Force use of LTX-Video (override config)
python src/research/python/generate_video_clips.py \
  --shots examples/video_clips/example_shots.yaml \
  --segment lifestyle \
  --age 24-30 \
  --title-id morning_routine \
  --use-ltx

# Use custom config file
python src/research/python/generate_video_clips.py \
  --shots my_shots.yaml \
  --config custom_pipeline.yaml \
  --segment gaming \
  --age 14-17 \
  --title-id top_strategies
```

## Output Structure

Videos are saved in a hierarchical directory structure:

```
videos/
├── ltx/                          # LTX-Video variant
│   └── {segment}/                # Content category (tech, lifestyle, gaming, etc.)
│       └── {age}/                # Target age group (18-23, 24-30, etc.)
│           └── {title_id}/       # Unique story identifier
│               ├── shot_0.mp4    # First shot clip
│               ├── shot_1.mp4    # Second shot clip
│               └── shot_2.mp4    # Third shot clip
│
└── interp/                       # Interpolation variant
    └── {segment}/
        └── {age}/
            └── {title_id}/
                ├── shot_0.mp4
                ├── shot_1.mp4
                └── shot_2.mp4
```

### Examples

- **LTX variant**: `/videos/ltx/tech/18-23/ai_revolution_2024/shot_0.mp4`
- **Interpolation variant**: `/videos/interp/lifestyle/24-30/morning_routine/shot_1.mp4`

## Shot Format

### LTX-Video Shots

For LTX-Video generation, shots should include:

```yaml
- image_path: "path/to/keyframe.png"  # Required: Base image
  motion: "slow zoom in"              # Optional: Motion description
  intensity: 0.5                      # Optional: Motion intensity (0.0-1.0)
  duration: 10.0                      # Optional: Duration in seconds (default: 10.0)
```

**Motion types**: zoom in, zoom out, pan left, pan right, pan up, pan down, rotate clockwise, rotate counterclockwise, subtle movement

**Intensity**: 
- 0.0-0.3: Minimal motion
- 0.3-0.6: Medium motion
- 0.6-1.0: Strong motion

### Interpolation Shots

For frame interpolation, shots should include multiple keyframes:

```yaml
- keyframes:                          # Required: List of keyframe images
    - "path/to/keyframe1.png"
    - "path/to/keyframe2.png"
    - "path/to/keyframe3.png"
  duration: 15.0                      # Optional: Total duration in seconds
```

## Configuration Options

### VideoClipGenerator Parameters

```python
generator = VideoClipGenerator(
    config_path="path/to/pipeline.yaml",  # Path to config (optional)
    use_ltx=True,                         # Override: use LTX (True) or interp (False)
    fps=30,                               # Target frames per second
    device="auto"                         # Device: "auto", "cuda", "cpu"
)
```

### CLI Arguments

| Argument | Description | Default |
|----------|-------------|---------|
| `--shots` | Path to shots YAML file | Required |
| `--segment` | Content segment (tech, lifestyle, etc.) | Required |
| `--age` | Target age group (18-23, 24-30, etc.) | Required |
| `--title-id` | Unique story identifier | Required |
| `--config` | Path to pipeline.yaml | Auto-detect |
| `--output-dir` | Base output directory | "videos" |
| `--use-ltx` | Force LTX-Video variant | Config default |
| `--use-interpolation` | Force interpolation variant | Config default |
| `--fps` | Target FPS | 30 |
| `--device` | Device (auto/cuda/cpu) | auto |
| `--seed` | Random seed for reproducibility | From config |

## Technical Details

### LTX-Video (Variant A)

**Model**: Stable Video Diffusion or LTX-Video models  
**Duration**: 10-20 seconds per clip  
**Quality**: High-quality AI-generated motion  
**Speed**: ~30 seconds to generate 10-second clip (GPU)  
**Requirements**: 
- GPU with 12GB+ VRAM recommended
- PyTorch + diffusers + transformers

**Process**:
1. Load keyframe image
2. Apply motion parameters (intensity, direction)
3. Generate video frames using AI model
4. Export to MP4 (H.264, 30fps, 1080x1920)

### Frame Interpolation (Variant B)

**Methods**: RIFE (default), DAIN, FILM  
**Duration**: Flexible based on keyframes  
**Quality**: Smooth transitions between keyframes  
**Speed**: Fast (~0.1s per frame with RIFE)  
**Requirements**:
- FFmpeg for video assembly
- RIFE/DAIN/FILM models (optional, falls back to FFmpeg)

**Process**:
1. Load all keyframes for shot
2. Create basic video from keyframes (even spacing)
3. Interpolate additional frames between keyframes
4. Export to MP4 (H.264, 30fps, 1080x1920)

### Video Specifications

All generated clips use these specifications:

- **Resolution**: 1080×1920 (9:16 portrait)
- **Codec**: H.264 (libx264)
- **Frame Rate**: 30 fps (configurable)
- **Pixel Format**: yuv420p
- **Aspect Ratio**: 9:16 (TikTok/YouTube Shorts/Instagram Reels)

## Testing

Run the test suite to validate configuration and functionality:

```bash
# Run video clip tests
python tests/test_video_clips.py

# Run all config tests
python tests/test_config.py
```

## Troubleshooting

### LTX-Video Issues

**Problem**: Out of memory (OOM) error  
**Solution**: Reduce duration, use smaller model, or switch to CPU

**Problem**: Model not loading  
**Solution**: Install required packages:
```bash
pip install diffusers transformers accelerate torch
```

### Interpolation Issues

**Problem**: FFmpeg not found  
**Solution**: Install FFmpeg:
```bash
# Ubuntu/Debian
sudo apt-get install ffmpeg

# macOS
brew install ffmpeg

# Windows
# Download from https://ffmpeg.org/download.html
```

**Problem**: Interpolation quality is poor  
**Solution**: 
- Use more keyframes (3-5 per scene)
- Try different interpolation methods (RIFE vs FILM)
- Increase keyframe image resolution

### General Issues

**Problem**: Config file not found  
**Solution**: Specify config path explicitly:
```bash
python generate_video_clips.py --config data/config/pipeline.yaml ...
```

**Problem**: Shot images not found  
**Solution**: Use absolute paths or ensure working directory is correct

## Examples

See `examples/video_clips/example_shots.yaml` for a complete example.

## Integration with Pipeline

This module integrates with the existing StoryGenerator pipeline:

1. **GKeyframeGenerator** → Generates keyframe images
2. **generate_video_clips** → Converts keyframes to video clips
3. **VideoPostProducer** → Assembles clips with audio/subtitles

```python
# Complete pipeline example
from Generators.GKeyframeGenerator import KeyframeGenerator
from research.python.generate_video_clips import VideoClipGenerator
from Tools.VideoPostProducer import VideoPostProducer

# 1. Generate keyframes
keyframe_gen = KeyframeGenerator()
keyframes = keyframe_gen.generate_keyframes(story_idea)

# 2. Create shots from keyframes
shots = [
    {"image_path": kf, "duration": 10.0}
    for kf in keyframes
]

# 3. Generate video clips
clip_gen = VideoClipGenerator()
clips = clip_gen.generate_clips_for_story(
    shots=shots,
    segment="tech",
    age="18-23",
    title_id="my_story"
)

# 4. Post-process and assemble final video
post_producer = VideoPostProducer()
final_video = post_producer.ProduceVideoAsync({
    "SegmentPaths": clips,
    "OutputPath": "final/tech/18-23/my_story_draft.mp4",
    ...
})
```

## API Reference

### VideoClipGenerator

#### Methods

##### `__init__(config_path, use_ltx, fps, device)`

Initialize the video clip generator.

##### `generate_shot_clip(shot, output_path, duration, seed)`

Generate a single video clip for a shot.

**Parameters**:
- `shot` (Dict): Shot description
- `output_path` (str): Output file path
- `duration` (float): Duration in seconds
- `seed` (int, optional): Random seed

**Returns**: str - Path to generated clip

##### `generate_clips_for_story(shots, segment, age, title_id, base_output_dir, base_seed)`

Generate all clips for a story.

**Parameters**:
- `shots` (List[Dict]): List of shot descriptions
- `segment` (str): Content segment
- `age` (str): Age group
- `title_id` (str): Story identifier
- `base_output_dir` (str): Base output directory
- `base_seed` (int, optional): Base random seed

**Returns**: List[str] - Paths to generated clips

##### `cleanup()`

Free resources and GPU memory.

## License

See repository LICENSE file.

## Contributing

Contributions welcome! Please ensure:
1. Tests pass (`python tests/test_video_clips.py`)
2. Code follows existing style
3. Documentation is updated

## Support

For issues or questions, please open a GitHub issue in the repository.
