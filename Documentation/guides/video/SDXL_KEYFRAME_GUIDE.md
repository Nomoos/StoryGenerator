# SDXL Keyframe Generation Guide

## Overview

The StoryGenerator now supports **Stable Diffusion XL (SDXL)** for high-quality keyframe generation at 1080×1920 resolution (9:16 aspect ratio), perfect for vertical video formats like Reels, Shorts, and TikTok.

## Features

### ✨ Key Capabilities

- **SDXL Base + Refiner Pipeline**: Two-stage generation for maximum quality
- **1080×1920 Resolution**: Native 9:16 aspect ratio for vertical video
- **60 FPS Target**: Optimized keyframe density for smooth 60 FPS output
- **Style Presets**: Pre-configured styles (cinematic, photorealistic, dramatic, etc.)
- **Negative Prompts**: Automatic quality filtering
- **GPU Optimizations**: Memory-efficient with attention slicing and VAE slicing
- **Reproducibility**: Seed control for consistent results
- **Metadata Tracking**: Complete generation parameters saved with each keyframe

### 🎨 Style Presets

Available styles:
- `cinematic` - Professional cinematic look
- `photorealistic` - Ultra-realistic photography
- `dramatic` - High contrast, dramatic lighting
- `soft` - Gentle, dreamy aesthetic
- `vibrant` - Bold, saturated colors
- `moody` - Dark, atmospheric
- `natural` - Documentary-style
- `stylized` - Artistic interpretation

## Installation

### Requirements

```bash
# Install required dependencies
pip install -r requirements.txt

# Key packages:
# - torch>=2.0.0
# - diffusers>=0.25.0
# - transformers>=4.35.0
# - accelerate>=0.25.0
# - Pillow>=10.4.0
```

### GPU Requirements

- **Minimum**: 12GB VRAM (base model only)
- **Recommended**: 16GB+ VRAM (base + refiner)
- **CPU Mode**: Available but slower (for testing)

## Usage

### Basic Usage

```python
from Python.Generators.GKeyframeGenerator import KeyframeGenerator
from Python.Models.StoryIdea import StoryIdea

# Initialize generator with SDXL
generator = KeyframeGenerator(
    use_refiner=True,  # Use refiner for higher quality
    style_preset="cinematic"  # Apply cinematic style
)

# Generate keyframes for a story
story_idea = StoryIdea.load_from_file("path/to/story")
scenes = generator.generate_keyframes(story_idea)

# Cleanup GPU memory
generator.cleanup()
```

### Advanced Configuration

```python
# Custom configuration
generator = KeyframeGenerator(
    model_id="stabilityai/stable-diffusion-xl-base-1.0",  # Custom model
    device="cuda",  # Force GPU
    num_inference_steps=50,  # More steps = higher quality
    use_refiner=True,  # Enable refiner
    style_preset="photorealistic"  # Choose style
)

# Apply different style preset
generator.apply_style_preset("dramatic")

# Generate keyframes
scenes = generator.generate_keyframes(story_idea)
```

### Without Refiner (Faster)

For faster generation on limited VRAM:

```python
generator = KeyframeGenerator(
    use_refiner=False,  # Disable refiner
    num_inference_steps=30  # Fewer steps
)
```

## Configuration

Edit `config/sdxl_config.py` to customize:

```python
# Resolution settings
DEFAULT_WIDTH = 1080  # 9:16 aspect ratio
DEFAULT_HEIGHT = 1920

# Generation settings
DEFAULT_STEPS = 40  # Base model steps
DEFAULT_REFINER_STEPS = 20  # Refiner steps
DEFAULT_GUIDANCE_SCALE = 7.5

# Target FPS
TARGET_FPS = 60  # For keyframe density calculation

# Memory optimizations
ENABLE_ATTENTION_SLICING = True
ENABLE_VAE_SLICING = True
ENABLE_CPU_OFFLOAD = False  # Enable if low VRAM
```

## Style Presets

Customize or add styles in `prompts/style_presets.json`:

```json
{
  "mystyle": {
    "description": "My custom style",
    "prompt_additions": "custom keywords, specific look",
    "guidance_scale": 7.5,
    "steps": 40
  }
}
```

## Negative Prompts

Customize quality filters in `prompts/negative_prompts.txt`:

```
# Add unwanted elements (one per line)
blurry, low quality
watermark, text
distorted, deformed
```

## Performance

### Generation Times (RTX 4090)

- **Base only**: ~5-7 seconds per keyframe
- **Base + Refiner**: ~8-10 seconds per keyframe

### VRAM Usage

- **Base only**: ~8-10GB
- **Base + Refiner**: ~12-14GB
- **With optimizations**: ~6-8GB (base only)

### Optimization Tips

1. **Enable memory optimizations** in config (already enabled by default)
2. **Use base only** for faster generation
3. **Reduce inference steps** (30-35 still produces good results)
4. **Enable CPU offload** if VRAM limited (slower but works)

## Output Structure

Generated keyframes are saved in:

```
Stories/4_Titles/[Story_Title]/keyframes/
├── scene_001_keyframe_00_t0.00.png
├── scene_001_keyframe_00_t0.00.json  # Metadata
├── scene_001_keyframe_01_t2.50.png
├── scene_001_keyframe_01_t2.50.json
└── ...
```

### Metadata Format

Each keyframe includes metadata in JSON:

```json
{
  "scene_id": 1,
  "image_path": "/path/to/keyframe.png",
  "prompt": "Full generation prompt...",
  "negative_prompt": "Quality filters...",
  "seed": 42,
  "width": 1080,
  "height": 1920,
  "steps": 40,
  "guidance_scale": 7.5,
  "style_preset": "cinematic",
  "generation_time": 8.5,
  "keyframe_index": 0,
  "timestamp": 0.0,
  "position": 0.0,
  "use_refiner": true,
  "refiner_steps": 20
}
```

## Troubleshooting

### Out of Memory

1. Set `use_refiner=False`
2. Enable `ENABLE_CPU_OFFLOAD = True` in config
3. Reduce `num_inference_steps`
4. Close other GPU applications

### Poor Quality

1. Enable refiner: `use_refiner=True`
2. Increase steps: `num_inference_steps=50`
3. Try different style presets
4. Improve scene descriptions in shotlist

### Slow Generation

1. Disable refiner for faster generation
2. Reduce inference steps (30-35)
3. Ensure GPU is being used (check `device="cuda"`)

## Model Information

### SDXL Base Model

- **Model**: `stabilityai/stable-diffusion-xl-base-1.0`
- **Size**: ~6.9GB
- **Resolution**: Up to 1024×1024 natively (we use 1080×1920)
- **Quality**: State-of-the-art image generation

### SDXL Refiner Model

- **Model**: `stabilityai/stable-diffusion-xl-refiner-1.0`
- **Size**: ~6.1GB
- **Purpose**: Enhances details and quality from base model
- **Strategy**: Two-stage generation (base → refiner)

## Next Steps

After keyframe generation, the pipeline continues to:

1. **Video Interpolation**: Smooth transitions between keyframes
2. **Audio Sync**: Align with voiceover
3. **Subtitle Overlay**: Add synchronized text
4. **Final Rendering**: Export complete video

## References

- [SDXL Documentation](https://huggingface.co/docs/diffusers/en/using-diffusers/sdxl)
- [Stable Diffusion XL Paper](https://arxiv.org/abs/2307.01952)
- [Diffusers Library](https://github.com/huggingface/diffusers)
