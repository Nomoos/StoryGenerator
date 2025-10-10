# SDXL Keyframe Generation - Quick Start

## What's New? 🎉

The StoryGenerator now uses **Stable Diffusion XL (SDXL)** for professional-quality keyframe generation!

### Key Improvements

| Feature | Before (SD 1.5) | Now (SDXL) |
|---------|----------------|------------|
| **Resolution** | 512×512 → scaled | **1080×1920 native** |
| **Quality** | Good | **Excellent** |
| **Styles** | None | **8 professional presets** |
| **Refiner** | No | **Yes (optional)** |
| **Target FPS** | N/A | **60 FPS optimized** |

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

This will install:
- PyTorch 2.0+
- Diffusers 0.25+
- Transformers 4.35+
- Accelerate 0.25+

### 2. Basic Usage

```python
from Python.Generators.GKeyframeGenerator import KeyframeGenerator
from Python.Models.StoryIdea import StoryIdea

# Load your story
story = StoryIdea.from_file("Your Story Title")

# Create generator
generator = KeyframeGenerator(
    use_refiner=True,        # High quality (slower)
    style_preset="cinematic" # Choose your style
)

# Generate keyframes
scenes = generator.generate_keyframes(story)

# Cleanup
generator.cleanup()
```

### 3. Fast Mode (No Refiner)

For testing or limited VRAM:

```python
generator = KeyframeGenerator(
    use_refiner=False,       # Faster generation
    num_inference_steps=30   # Fewer steps
)
```

## Style Presets

Choose from 8 professional styles:

1. **cinematic** - Film-quality with professional lighting
2. **photorealistic** - Ultra-realistic photography
3. **dramatic** - High contrast, intense shadows
4. **soft** - Gentle, dreamy aesthetic
5. **vibrant** - Bold, saturated colors
6. **moody** - Dark, atmospheric
7. **natural** - Documentary-style
8. **stylized** - Artistic interpretation

## System Requirements

### Minimum (Base Only)
- GPU: 12GB VRAM
- Generation: ~5-7 sec/keyframe

### Recommended (Base + Refiner)
- GPU: 16GB+ VRAM
- Generation: ~8-10 sec/keyframe

### CPU Mode
- Available but very slow
- For testing only

## Output

Keyframes are saved as:
```
Stories/4_Titles/[Story]/keyframes/
├── scene_001_keyframe_00_t0.00.png
├── scene_001_keyframe_00_t0.00.json  ← Metadata
├── scene_001_keyframe_01_t2.50.png
└── ...
```

Each image comes with JSON metadata containing:
- Prompt used
- Generation parameters
- Timing information
- Style settings

## Configuration

Edit `config/sdxl_config.py` to customize:

```python
# Resolution
DEFAULT_WIDTH = 1080
DEFAULT_HEIGHT = 1920

# Quality vs Speed
DEFAULT_STEPS = 40           # Higher = better quality
USE_REFINER = True           # True = better quality
ENABLE_ATTENTION_SLICING = True  # True = less VRAM

# Reproducibility
SEED = 42  # Fixed seed for consistent results
```

## Examples

See `examples/sdxl_keyframe_example.py` for interactive examples:

```bash
python3 examples/sdxl_keyframe_example.py
```

## Documentation

- **Full Guide**: `docs/SDXL_KEYFRAME_GUIDE.md`
- **Pipeline Status**: `PIPELINE.md`
- **Tests**: `tests/test_keyframes.py`

## Troubleshooting

### Out of Memory?
1. Set `use_refiner=False`
2. Set `ENABLE_CPU_OFFLOAD = True` in config
3. Reduce `num_inference_steps` to 30

### Slow Generation?
1. Use base only (no refiner)
2. Reduce inference steps
3. Check GPU is being used

### Poor Quality?
1. Enable refiner
2. Increase inference steps to 50
3. Try different style presets
4. Improve scene descriptions

## Next Steps

After keyframe generation:
1. **Video Interpolation** - Create smooth transitions
2. **Audio Sync** - Align with voiceover
3. **Subtitle Overlay** - Add text
4. **Final Rendering** - Export video

---

**Need Help?** Check the full documentation in `docs/SDXL_KEYFRAME_GUIDE.md`
