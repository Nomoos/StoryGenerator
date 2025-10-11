# Video Clip Generation - Quick Start

Generate video clips from shots using either LTX-Video or frame interpolation.

## 🚀 Quick Start

### 1. Install Dependencies

```bash
# For LTX-Video (Variant A)
pip install torch diffusers transformers accelerate

# For Interpolation (Variant B)
# Install FFmpeg first, then:
pip install opencv-python numpy pillow
```

### 2. Configure

Edit `data/config/pipeline.yaml`:

```yaml
switches:
  use_ltx: true              # Default: LTX-Video
  use_interpolation: false   # Set true for interpolation
```

### 3. Generate Clips

**Using Python:**

```python
from Generators.GVideoClipGenerator import GVideoClipGenerator

# Initialize
generator = GVideoClipGenerator(use_ltx=True)

# Define shots
shots = [
    {
        "image_path": "keyframe_001.png",
        "motion": "zoom in",
        "intensity": 0.5,
        "duration": 10.0
    }
]

# Generate
clips = generator.generate_clips_for_story(
    shots=shots,
    segment="tech",
    age="18-23",
    title_id="my_story"
)

# Output: videos/ltx/tech/18-23/my_story/shot_0.mp4
```

**Using CLI:**

```bash
python src/research/python/generate_video_clips.py \
  --shots examples/video_clips/example_shots.yaml \
  --segment tech \
  --age 18-23 \
  --title-id my_story
```

## 📁 Output Structure

```
videos/
├── ltx/                    # LTX-Video variant
│   └── tech/
│       └── 18-23/
│           └── my_story/
│               ├── shot_0.mp4
│               ├── shot_1.mp4
│               └── shot_2.mp4
│
└── interp/                 # Interpolation variant
    └── lifestyle/
        └── 24-30/
            └── another_story/
                ├── shot_0.mp4
                └── shot_1.mp4
```

## 🎬 Shot Format

### LTX-Video Shots

```yaml
- image_path: "keyframe.png"
  motion: "slow zoom in"      # Optional
  intensity: 0.3              # Optional: 0.0-1.0
  duration: 10.0              # Optional: 10-20s recommended
```

### Interpolation Shots

```yaml
- keyframes:
    - "keyframe1.png"
    - "keyframe2.png"
    - "keyframe3.png"
  duration: 15.0
```

## 📚 Documentation

- **Full API docs**: `docs/VIDEO_CLIP_GENERATION.md`
- **Examples**: `examples/video_clip_generation_example.py`
- **Example data**: `examples/video_clips/example_shots.yaml`

## 🧪 Testing

```bash
# Run tests
python tests/test_video_clips.py

# Run examples
python examples/video_clip_generation_example.py
```

## 🔧 Options

| Option | Default | Description |
|--------|---------|-------------|
| `use_ltx` | `true` (from config) | Use LTX-Video |
| `fps` | `30` | Target frame rate |
| `device` | `auto` | Device (auto/cuda/cpu) |
| `seed` | From config | Random seed |

## ⚡ Quick Commands

```bash
# LTX-Video generation
python src/research/python/generate_video_clips.py \
  --shots my_shots.yaml --segment tech --age 18-23 \
  --title-id story_001 --use-ltx

# Frame interpolation
python src/research/python/generate_video_clips.py \
  --shots my_shots.yaml --segment lifestyle --age 24-30 \
  --title-id story_002 --use-interpolation

# Custom config
python src/research/python/generate_video_clips.py \
  --shots my_shots.yaml --config my_config.yaml \
  --segment gaming --age 14-17 --title-id story_003
```

## 🆘 Common Issues

**Error: "No module named 'torch'"**
→ Install PyTorch: `pip install torch diffusers transformers`

**Error: "'ffmpeg' not found"**
→ Install FFmpeg: `sudo apt-get install ffmpeg` (Ubuntu) or `brew install ffmpeg` (macOS)

**Error: "CUDA out of memory"**
→ Use `--device cpu` or reduce clip duration

## 🎯 Integration

Integrates with existing pipeline:

1. `GKeyframeGenerator` → Generates keyframes
2. `GVideoClipGenerator` → Creates video clips
3. `VideoPostProducer` → Assembles final video

## 📝 Notes

- LTX-Video requires GPU (12GB+ VRAM recommended)
- Interpolation works on CPU but GPU is faster
- Research prototypes in `src/research/python/` are gitignored
- Production interface: `src/Python/Generators/GVideoClipGenerator.py`
