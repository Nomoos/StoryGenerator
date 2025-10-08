# Video Clip Generation - Research Prototypes

This directory contains research prototypes for video clip generation.

## Files

### `generate_video_clips.py` (Main Module)
Complete implementation of video clip generation supporting both LTX-Video and frame interpolation variants.

**Features:**
- Variant A: LTX-Video generation (10-20s clips)
- Variant B: Frame interpolation (RIFE/DAIN/FILM)
- Configuration-driven (uses pipeline.yaml)
- CLI interface with argparse
- Batch processing support
- Reproducible with seed control

**Usage:**
```bash
# Command line
python generate_video_clips.py \
  --shots examples/video_clips/example_shots.yaml \
  --segment tech \
  --age 18-23 \
  --title-id my_story

# Python API
from generate_video_clips import VideoClipGenerator

generator = VideoClipGenerator(use_ltx=True)
clips = generator.generate_clips_for_story(
    shots=[...],
    segment="tech",
    age="18-23",
    title_id="my_story"
)
```

### `ltx_generate.py` (LTX-Video Wrapper)
Wrapper for LTX-Video and Stable Video Diffusion models.

**Features:**
- Image-to-video generation
- Motion control (intensity, direction)
- Batch processing
- GPU memory management

### `interpolation.py` (Frame Interpolation Wrapper)
Wrapper for RIFE, DAIN, and FILM interpolation models.

**Features:**
- Video frame rate increase
- Frame-to-frame interpolation
- Multiple method support
- FFmpeg fallback

## Integration

These research prototypes are integrated into the main codebase via:

`src/Python/Generators/GVideoClipGenerator.py`

This provides a clean Generator (G*) interface following the project conventions.

## Output Structure

Videos are saved in hierarchical structure:

```
videos/
├── ltx/{segment}/{age}/{title_id}/shot_{k}.mp4
└── interp/{segment}/{age}/{title_id}/shot_{k}.mp4
```

## Configuration

Uses `data/config/pipeline.yaml`:

```yaml
switches:
  use_ltx: true              # Default: Use LTX-Video
  use_interpolation: false   # Enable interpolation
```

## Documentation

See: `docs/VIDEO_CLIP_GENERATION.md`

## Note

These are research prototypes. Files in `src/research/` are gitignored by design.
The production interface is in `src/Python/Generators/GVideoClipGenerator.py`.
