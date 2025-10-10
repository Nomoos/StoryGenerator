# Style Consistency System Guide

Comprehensive guide for using the Style Consistency System to maintain visual coherence across SDXL-generated keyframes.

## Overview

The Style Consistency System ensures that all images generated for a video maintain a unified visual style, creating a cohesive viewing experience. It uses IP-Adapter technology with Stable Diffusion XL to apply consistent styling across multiple keyframes.

## Installation

### Prerequisites

1. **Python 3.8+** with pip
2. **CUDA-capable GPU with 12GB+ VRAM** (recommended for SDXL)
   - Can work with 8GB VRAM using optimizations
   - CPU mode available but very slow
3. **PyTorch with CUDA** support

### Install Dependencies

```bash
# Install requirements
pip install -r requirements.txt

# Verify installation
python -c "from diffusers import StableDiffusionXLPipeline; print('SDXL ready')"
python -c "from PIL import Image; import numpy as np; print('Image processing ready')"
```

## Quick Start

### 1. Create a Style Reference

```python
from pathlib import Path
from core.pipeline.style_consistency import StyleConsistencyManager

# Initialize manager
manager = StyleConsistencyManager(
    style_library_dir=Path("data/styles"),
    device="cuda"  # or "cpu" for CPU mode
)

# Create a style reference from a prompt
style_profile = manager.create_style_reference(
    prompt="cinematic, dramatic lighting, blue and orange color grading, film noir",
    style_name="cinematic_noir",
    output_path=Path("data/styles/cinematic_noir_ref.png"),
    width=1024,
    height=1024
)

print(f"Style profile created: {style_profile.name}")
print(f"Color palette: {style_profile.color_palette}")
print(f"Style tags: {style_profile.style_tags}")
```

### 2. Generate Keyframes with Consistent Style

```python
# Define prompts for your video keyframes
prompts = [
    "A detective walking down a dark alley at night",
    "Close-up of the detective's face, suspicious expression",
    "The detective discovers a clue under a streetlight",
    "Wide shot of the city skyline at night"
]

# Generate keyframes with consistent style
output_dir = Path("output/keyframes/cinematic_noir")
keyframe_paths = manager.generate_with_style(
    prompts=prompts,
    style_name="cinematic_noir",
    output_dir=output_dir,
    width=1080,
    height=1920  # Vertical video format
)

print(f"Generated {len(keyframe_paths)} keyframes:")
for i, path in enumerate(keyframe_paths):
    print(f"  {i+1}. {path}")
```

### 3. Validate Visual Consistency

```python
# Validate consistency across generated keyframes
metrics = manager.validate_consistency(
    image_paths=keyframe_paths,
    output_report_path=Path("output/consistency_report.json")
)

print(f"Consistency Analysis:")
print(f"  Color Similarity: {metrics.color_similarity:.2%}")
print(f"  Structural Similarity: {metrics.structural_similarity:.2%}")
print(f"  Style Consistency: {metrics.style_consistency:.2%}")
print(f"  Overall Score: {metrics.overall_score:.2%}")

if metrics.overall_score < 0.7:
    print("⚠️  Warning: Low consistency detected")
elif metrics.overall_score > 0.85:
    print("✅ Excellent consistency!")
```

## Advanced Usage

### Managing Style Library

#### List Available Styles

```python
# Get all styles
all_styles = manager.get_style_profiles()

print(f"Available styles ({len(all_styles)}):")
for profile in all_styles:
    print(f"  - {profile.name}: {profile.style_prompt}")
    print(f"    Tags: {', '.join(profile.style_tags)}")
```

#### Filter Styles by Tags

```python
# Get only cinematic styles
cinematic_styles = manager.get_style_profiles(tags=["cinematic"])

# Get anime styles
anime_styles = manager.get_style_profiles(tags=["anime"])

print(f"Found {len(cinematic_styles)} cinematic styles")
```

#### Export/Import Style Library

```python
# Export entire style library
manager.export_style_library(Path("backup/styles_2024.json"))

# Import styles from backup
manager.import_style_library(Path("backup/styles_2024.json"))
```

### Custom Style Profiles

#### Create Style from Existing Image

While the system primarily generates style references, you can manually create profiles:

```python
# Create a style profile from an existing reference image
from core.pipeline.style_consistency import StyleProfile

# Extract color palette manually
reference_img = Image.open("path/to/reference.jpg")
color_palette = manager._extract_color_palette(reference_img)

# Create profile
custom_profile = StyleProfile(
    name="custom_anime_style",
    reference_image_path="path/to/reference.jpg",
    style_prompt="anime, vibrant colors, cel shading",
    ip_adapter_scale=0.85,
    color_palette=color_palette,
    style_tags=["anime", "vibrant", "colorful"],
    metadata={"source": "custom", "artist": "Studio XYZ"}
)

# Add to library
manager.style_profiles[custom_profile.name] = custom_profile
manager._save_style_profile(custom_profile)
```

### Adjusting Style Strength

Control how strongly the style is applied:

```python
# Create style with different IP-Adapter scales
light_style = manager.create_style_reference(
    prompt="watercolor painting, soft pastel colors",
    style_name="watercolor_light",
    output_path=Path("styles/watercolor_light.png")
)
light_style.ip_adapter_scale = 0.5  # Lighter application

heavy_style = manager.create_style_reference(
    prompt="oil painting, thick brushstrokes, impressionist",
    style_name="oil_painting_heavy",
    output_path=Path("styles/oil_heavy.png")
)
heavy_style.ip_adapter_scale = 0.95  # Heavier application

# Save updated profiles
manager._save_style_profile(light_style)
manager._save_style_profile(heavy_style)
```

### Batch Processing

Generate multiple video sequences with different styles:

```python
def generate_video_variations(base_prompts, style_names, output_base_dir):
    """Generate multiple styled versions of the same sequence."""
    results = {}
    
    for style_name in style_names:
        output_dir = output_base_dir / style_name
        output_dir.mkdir(parents=True, exist_ok=True)
        
        keyframes = manager.generate_with_style(
            prompts=base_prompts,
            style_name=style_name,
            output_dir=output_dir
        )
        
        metrics = manager.validate_consistency(keyframes)
        
        results[style_name] = {
            'keyframes': keyframes,
            'consistency': metrics.overall_score
        }
        
        print(f"✓ Generated {style_name}: {metrics.overall_score:.2%} consistent")
    
    return results

# Use it
base_prompts = [
    "A hero standing on a mountain peak",
    "The hero draws their sword",
    "Epic battle scene with dramatic lighting"
]

styles = ["cinematic_noir", "anime_vibrant", "realistic_photo"]
variations = generate_video_variations(
    base_prompts,
    styles,
    Path("output/style_variations")
)
```

## Best Practices

### Style Reference Creation

1. **Be Specific in Prompts**
   ```python
   # Good: Detailed, specific style description
   prompt = "cinematic, anamorphic lens, teal and orange color grading, volumetric lighting, film grain"
   
   # Less effective: Vague description
   prompt = "nice looking, good style"
   ```

2. **Use Consistent Style Keywords**
   - Art styles: "cinematic", "anime", "oil painting", "watercolor"
   - Lighting: "dramatic lighting", "soft lighting", "volumetric"
   - Color: "vibrant", "muted", "monochrome", "pastel"
   - Technical: "sharp focus", "bokeh", "film grain"

3. **Test Style References**
   ```python
   # Generate and review before using in production
   test_ref = manager.create_style_reference(
       prompt="your style description",
       style_name="test_style",
       output_path=Path("tests/style_test.png")
   )
   
   # Visual inspection before committing
   # If not satisfied, adjust prompt and regenerate
   ```

### Keyframe Generation

1. **Maintain Prompt Structure**
   ```python
   # Keep similar structure across prompts
   prompts = [
       "A character walking in a forest, morning light",
       "The character stops and looks around, morning light",
       "Close-up of character's face, morning light"
   ]
   # Note: "morning light" mentioned consistently
   ```

2. **Progressive Scene Changes**
   ```python
   # Gradual transitions work better than sudden changes
   # Good:
   prompts = [
       "Wide shot of character in field",
       "Medium shot of character in field",
       "Close-up of character's face"
   ]
   
   # Problematic (too abrupt):
   prompts = [
       "Wide shot of character in field",
       "Interior of spaceship cockpit"  # Sudden location change
   ]
   ```

3. **Use Aspect Ratios Wisely**
   ```python
   # For vertical video (TikTok, Instagram Reels)
   width, height = 1080, 1920
   
   # For horizontal video (YouTube)
   width, height = 1920, 1080
   
   # For square (Instagram posts)
   width, height = 1080, 1080
   ```

### Consistency Validation

1. **Set Quality Thresholds**
   ```python
   metrics = manager.validate_consistency(keyframes)
   
   if metrics.overall_score < 0.70:
       print("❌ Poor consistency - consider regenerating")
   elif metrics.overall_score < 0.85:
       print("⚠️  Acceptable but could be improved")
   else:
       print("✅ Excellent consistency")
   ```

2. **Analyze Individual Metrics**
   ```python
   if metrics.color_similarity < 0.75:
       print("Issue: Color palette inconsistency")
       print("Solution: Use stronger IP-Adapter scale or adjust prompts")
   
   if metrics.structural_similarity < 0.70:
       print("Issue: Structural changes too drastic")
       print("Solution: Use more gradual scene transitions")
   ```

### Performance Optimization

1. **GPU Memory Management**
   ```python
   import torch
   
   # Clear cache between generations if running out of memory
   torch.cuda.empty_cache()
   
   # Use lower precision for faster generation
   manager = StyleConsistencyManager(
       model_id="stabilityai/stable-diffusion-xl-base-1.0",
       device="cuda"
   )
   # Model automatically uses float16 on CUDA
   ```

2. **Batch Size Optimization**
   ```python
   # Process keyframes in batches if memory limited
   def generate_in_batches(prompts, style_name, output_dir, batch_size=5):
       all_paths = []
       
       for i in range(0, len(prompts), batch_size):
           batch_prompts = prompts[i:i + batch_size]
           batch_paths = manager.generate_with_style(
               batch_prompts,
               style_name,
               output_dir
           )
           all_paths.extend(batch_paths)
           
           # Clear cache between batches
           torch.cuda.empty_cache()
       
       return all_paths
   ```

3. **Reduce Inference Steps for Speed**
   ```python
   # Fast mode (lower quality but faster)
   keyframes = manager.generate_with_style(
       prompts,
       style_name,
       output_dir,
       num_inference_steps=25,  # Default: 50
       guidance_scale=7.0       # Default: 7.5
   )
   ```

## Production Workflow

### Complete Pipeline

```python
from pathlib import Path
from core.pipeline.style_consistency import StyleConsistencyManager
import json

def create_consistent_video_assets(
    video_title: str,
    scene_prompts: list[str],
    style_description: str,
    output_base: Path
):
    """Complete workflow for creating consistent video assets."""
    
    # Setup
    output_base.mkdir(parents=True, exist_ok=True)
    manager = StyleConsistencyManager(
        style_library_dir=output_base / "styles",
        device="cuda"
    )
    
    # 1. Create style reference
    print("📐 Creating style reference...")
    style_name = video_title.lower().replace(" ", "_")
    style_ref_path = output_base / f"{style_name}_style_ref.png"
    
    style_profile = manager.create_style_reference(
        prompt=style_description,
        style_name=style_name,
        output_path=style_ref_path
    )
    print(f"✓ Style reference: {style_ref_path}")
    
    # 2. Generate keyframes
    print(f"🎨 Generating {len(scene_prompts)} keyframes...")
    keyframes_dir = output_base / "keyframes"
    keyframe_paths = manager.generate_with_style(
        prompts=scene_prompts,
        style_name=style_name,
        output_dir=keyframes_dir,
        width=1080,
        height=1920
    )
    print(f"✓ Generated {len(keyframe_paths)} keyframes")
    
    # 3. Validate consistency
    print("🔍 Validating consistency...")
    report_path = output_base / "consistency_report.json"
    metrics = manager.validate_consistency(
        keyframe_paths,
        report_path
    )
    
    print(f"✓ Consistency Report:")
    print(f"  Overall Score: {metrics.overall_score:.2%}")
    print(f"  Color Similarity: {metrics.color_similarity:.2%}")
    print(f"  Structural Similarity: {metrics.structural_similarity:.2%}")
    print(f"  Style Consistency: {metrics.style_consistency:.2%}")
    
    # 4. Create summary
    summary = {
        'video_title': video_title,
        'style_name': style_name,
        'style_description': style_description,
        'num_keyframes': len(keyframe_paths),
        'keyframe_paths': [str(p) for p in keyframe_paths],
        'consistency_metrics': metrics.to_dict(),
        'style_profile': style_profile.to_dict()
    }
    
    summary_path = output_base / "summary.json"
    with open(summary_path, 'w') as f:
        json.dump(summary, f, indent=2)
    
    print(f"✓ Summary saved: {summary_path}")
    
    # 5. Quality check
    if metrics.overall_score < 0.70:
        print("⚠️  WARNING: Low consistency score!")
        print("   Consider regenerating with adjusted prompts")
        return False
    elif metrics.overall_score >= 0.85:
        print("✅ Excellent consistency achieved!")
        return True
    else:
        print("✓ Acceptable consistency")
        return True

# Usage
scene_prompts = [
    "A cyberpunk city street at night, neon lights, rain-soaked pavement",
    "Close-up of a hacker's face illuminated by monitor glow, focused expression",
    "Wide shot of towering skyscrapers with holographic advertisements",
    "The hacker types rapidly on a futuristic keyboard, code on screens"
]

style_desc = "cyberpunk, neon lights, dark atmosphere, cinematic, blue and purple color scheme, film noir lighting, highly detailed"

success = create_consistent_video_assets(
    video_title="Cyberpunk Heist",
    scene_prompts=scene_prompts,
    style_description=style_desc,
    output_base=Path("output/cyberpunk_heist")
)
```

## Troubleshooting

### Issue: CUDA Out of Memory

**Problem**: `RuntimeError: CUDA out of memory`

**Solutions**:
```python
# 1. Use CPU (slow but works)
manager = StyleConsistencyManager(device="cpu")

# 2. Reduce image resolution
keyframes = manager.generate_with_style(
    prompts, style_name, output_dir,
    width=768, height=768  # Instead of 1024x1024
)

# 3. Clear cache between generations
import torch
for i, prompt in enumerate(prompts):
    # Generate one at a time
    result = manager.generate_with_style(
        [prompt], style_name, output_dir
    )
    torch.cuda.empty_cache()

# 4. Use gradient checkpointing (add to manager init)
# This requires modifying the pipeline
```

### Issue: IP-Adapter Not Loading

**Problem**: IP-Adapter fails to load

**Solution**:
```python
# The system automatically falls back to prompt-based consistency
# To explicitly check:
manager = StyleConsistencyManager(device="cuda")
_ = manager.pipe  # Trigger lazy load

if hasattr(manager, '_has_ip_adapter') and not manager._has_ip_adapter:
    print("Using prompt-based consistency (IP-Adapter unavailable)")
else:
    print("Using IP-Adapter for style consistency")
```

### Issue: Low Consistency Scores

**Problem**: Consistency score below 0.70

**Solutions**:
1. **Strengthen style application**:
   ```python
   profile.ip_adapter_scale = 0.95  # Increase from default 0.8
   ```

2. **Use more specific prompts**:
   ```python
   # Add consistent style keywords to each prompt
   base_style = "cinematic, blue tint, dramatic lighting"
   prompts = [f"{scene}, {base_style}" for scene in base_scenes]
   ```

3. **Reduce scene variation**:
   ```python
   # Keep scenes more similar
   # Instead of drastically different locations/subjects
   ```

### Issue: Slow Generation Speed

**Problem**: Generation takes too long

**Solutions**:
```python
# 1. Reduce inference steps
keyframes = manager.generate_with_style(
    prompts, style_name, output_dir,
    num_inference_steps=25  # Default: 50
)

# 2. Use smaller resolution
keyframes = manager.generate_with_style(
    prompts, style_name, output_dir,
    width=768, height=1366  # Instead of 1080x1920
)

# 3. Enable xformers (if installed)
import torch
# This requires xformers package
# pip install xformers
```

## API Reference

### StyleConsistencyManager

Main class for managing style consistency.

```python
StyleConsistencyManager(
    model_id: str = "stabilityai/stable-diffusion-xl-base-1.0",
    style_library_dir: Optional[Path] = None,
    device: str = "cuda"
)
```

**Methods**:
- `create_style_reference()` - Generate style reference from prompt
- `generate_with_style()` - Generate keyframes with consistent style
- `validate_consistency()` - Validate visual consistency
- `get_style_profiles()` - Get style profiles (optionally filtered)
- `export_style_library()` - Export all styles to JSON
- `import_style_library()` - Import styles from JSON

### StyleProfile

Dataclass representing a style profile.

**Attributes**:
- `name: str` - Style name
- `reference_image_path: str` - Path to reference image
- `style_prompt: str` - Text prompt describing style
- `ip_adapter_scale: float` - Style application strength (0-1)
- `color_palette: List[Tuple[int, int, int]]` - Dominant colors
- `style_tags: List[str]` - Style classification tags
- `created_at: str` - ISO timestamp
- `metadata: Dict` - Additional metadata

### ConsistencyMetrics

Metrics for evaluating visual consistency.

**Attributes**:
- `color_similarity: float` - Color histogram similarity (0-1)
- `structural_similarity: float` - Structural similarity (0-1)
- `style_consistency: float` - Style feature consistency (0-1)
- `overall_score: float` - Weighted average (0-1)
- `frame_scores: List[float]` - Per-frame quality scores

## Examples

See `examples/sdxl_keyframe_example.py` for more usage examples.

## Support

For issues or questions:
- GitHub Issues: [StoryGenerator Issues](https://github.com/Nomoos/StoryGenerator/issues)
- Documentation: [Main README](../README.md)
- Related: [Image Generation Guide](../issues/resolved/phase-3-implementation/group-7-image-generation/)

## License

Same as parent project.
