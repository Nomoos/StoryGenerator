# Vision Guidance Module

Vision guidance utilities for image captioning, quality assessment, and consistency validation using LLaVA-OneVision or Phi-3.5-vision models.

## Overview

This module provides tools to:
- Generate descriptive captions for images
- Assess image quality (composition, lighting, clarity, etc.)
- Check visual consistency between consecutive frames
- Validate entire storyboard sequences
- Detect visual errors and artifacts

## Features

### Supported Models

| Model | Size | VRAM | Quality | Speed | Use Case |
|-------|------|------|---------|-------|----------|
| **Phi-3.5-vision** | ~4B | ~8GB | Good | Faster | Recommended for most use cases |
| **LLaVA-OneVision** | ~7B | ~14GB | Higher | Slower | Best quality, needs more resources |
| **LLaVA-v1.5-7b** | ~7B | ~14GB | High | Moderate | Alternative option |

### Core Capabilities

1. **Image Captioning**: Generate detailed descriptions of images
2. **Quality Assessment**: Score images on multiple quality metrics (0-10 scale)
3. **Consistency Validation**: Compare consecutive images for visual continuity
4. **Storyboard Validation**: Validate entire image sequences for quality and consistency
5. **Error Detection**: Identify visual artifacts and anomalies

## Installation

### Basic Installation

```bash
# Install core dependencies
pip install -r requirements.txt
```

### Vision Model Support

```bash
# Install transformers for vision model support
pip install transformers>=4.40.0
pip install accelerate>=0.20.0
```

## Quick Start

### 1. Basic Initialization

```python
from Python.Generators.GVision import GVision

# Initialize without loading model
generator = GVision(model_name="phi-3.5-vision", load_model=False)

# Model will be loaded automatically on first use
```

### 2. Generate Image Caption

```python
# Load model and generate caption
generator = GVision(model_name="phi-3.5-vision", load_model=True)

caption = generator.generate_caption("path/to/image.jpg")
print(f"Caption: {caption.caption}")
print(f"Confidence: {caption.confidence}")
```

### 3. Assess Image Quality

```python
quality = generator.assess_quality("path/to/image.jpg")

print(f"Overall Quality: {quality.overall_quality}/10")
print(f"Composition: {quality.composition}/10")
print(f"Lighting: {quality.lighting}/10")
print(f"Average: {quality.average_score():.1f}/10")
print(f"Artifacts: {quality.artifacts_detected}")
print(f"Reasoning: {quality.reasoning}")
```

### 4. Check Consistency Between Frames

```python
consistency = generator.check_consistency(
    "scene1.jpg",
    "scene2.jpg"
)

print(f"Character Consistency: {consistency.character_consistency}/10")
print(f"Style Consistency: {consistency.style_consistency}/10")
print(f"Visual Continuity: {consistency.visual_continuity}/10")
print(f"Average: {consistency.average_score():.1f}/10")

if consistency.inconsistencies:
    print("Issues found:")
    for issue in consistency.inconsistencies:
        print(f"  - {issue}")
```

### 5. Validate Complete Storyboard

```python
from Python.Tools.VisionUtils import find_keyframe_images

# Find all keyframes in story folder
image_paths = find_keyframe_images("path/to/story_folder")

# Validate entire sequence
validation = generator.validate_storyboard(
    image_paths,
    check_consistency=True,
    quality_threshold=6.0,
    consistency_threshold=6.0
)

print(f"Story: {validation.story_name}")
print(f"Scenes: {validation.scene_count}")
print(f"Avg Quality: {validation.overall_quality_avg:.1f}/10")
print(f"Avg Consistency: {validation.overall_consistency_avg:.1f}/10")
print(f"Passed: {validation.validation_passed}")

# Save results
import json
with open("validation_results.json", "w") as f:
    json.dump(validation.to_dict(), f, indent=2)
```

### 6. Integration with Pipeline

```python
from Python.Generators.GVision import GVision
from Python.Generators.GKeyframeGenerator import KeyframeGenerator

# Initialize generators
vision = GVision(model_name="phi-3.5-vision", load_model=True)
keyframe_gen = KeyframeGenerator()

# Generate and validate keyframe
keyframe_path = "keyframe.jpg"
keyframe_gen.generate_scene_keyframe(scene, output_path=keyframe_path)

# Check quality
result = vision.validate_image(keyframe_path, quality_threshold=7.0)

if result.quality_score.average_score() < 7.0:
    print("Quality too low, regenerating with better parameters...")
    keyframe_gen.generate_scene_keyframe(
        scene,
        output_path=keyframe_path,
        num_inference_steps=50  # Higher quality
    )

# Cleanup
vision.cleanup()
```

## Module Structure

```
Python/
├── Generators/
│   └── GVision.py                 # Main vision guidance generator
├── Models/
│   └── VisionAnalysis.py          # Data models for results
└── Tools/
    └── VisionUtils.py             # Utility functions

config/
└── vision_prompts.py              # Validation prompts

tests/
└── test_vision.py                 # Unit tests

examples/
└── vision_guidance_example.py     # Usage examples
```

## Data Models

### QualityScore

Stores quality assessment metrics:
- `overall_quality`: Overall image quality (0-10)
- `sharpness`: Image sharpness (0-10)
- `clarity`: Visual clarity (0-10)
- `composition`: Composition quality (0-10)
- `lighting`: Lighting quality (0-10)
- `subject_clarity`: Main subject clarity (0-10)
- `artifacts_detected`: Boolean flag for artifacts
- `reasoning`: Textual explanation

### ConsistencyScore

Stores consistency metrics between images:
- `character_consistency`: Character appearance consistency (0-10)
- `style_consistency`: Visual style consistency (0-10)
- `lighting_consistency`: Lighting consistency (0-10)
- `visual_continuity`: Overall visual flow (0-10)
- `inconsistencies`: List of detected issues
- `reasoning`: Textual explanation

### VisionAnalysisResult

Complete analysis for a single image:
- `image_path`: Path to analyzed image
- `caption`: Generated caption (ImageCaption object)
- `quality_score`: Quality metrics (QualityScore object)
- `consistency_score`: Consistency metrics (ConsistencyScore object)
- `validation_passed`: Boolean validation result
- `errors`: List of errors
- `warnings`: List of warnings

### StoryboardValidation

Validation results for image sequence:
- `story_name`: Name of the story
- `scene_count`: Number of scenes
- `scene_analyses`: List of VisionAnalysisResult objects
- `overall_quality_avg`: Average quality score
- `overall_consistency_avg`: Average consistency score
- `validation_passed`: Overall validation result
- `recommendations`: List of improvement suggestions

## Utility Functions

### Image Operations

```python
from Python.Tools.VisionUtils import (
    load_image,
    validate_image_dimensions,
    resize_image_for_vision_model,
    calculate_image_quality_heuristics
)

# Load image
image = load_image("path/to/image.jpg")

# Validate dimensions
is_valid, msg = validate_image_dimensions(image, min_width=512, min_height=512)

# Resize for model
resized = resize_image_for_vision_model(image, max_size=1024)

# Calculate basic quality metrics
metrics = calculate_image_quality_heuristics(image)
print(f"Brightness: {metrics['brightness']}")
print(f"Contrast: {metrics['contrast']}")
```

### Response Parsing

```python
from Python.Tools.VisionUtils import (
    parse_quality_scores,
    parse_consistency_scores,
    validate_caption_alignment
)

# Parse model responses
quality_data = parse_quality_scores(model_response)
consistency_data = parse_consistency_scores(model_response)

# Validate captions
is_valid, matched, missing = validate_caption_alignment(
    caption="A young girl walking down a hallway",
    expected_keywords=["girl", "hallway", "walking"],
    min_keyword_matches=2
)
```

### System Checks

```python
from Python.Tools.VisionUtils import check_gpu_available, estimate_vram_usage

# Check GPU
gpu_available, device = check_gpu_available()
print(f"GPU Available: {gpu_available}")
print(f"Device: {device}")

# Check VRAM requirements
vram = estimate_vram_usage("phi-3.5-vision")
print(f"Estimated VRAM: {vram}")
```

## Configuration

### Vision Prompts

Prompts are defined in `config/vision_prompts.py`:

```python
from config.vision_prompts import get_prompt

# Get specific prompt
quality_prompt = get_prompt("quality")
consistency_prompt = get_prompt("consistency")
caption_prompt = get_prompt("caption")

# Available prompt types:
# - quality: Image quality assessment
# - consistency: Frame-to-frame consistency
# - caption: Image captioning
# - descriptive: Detailed description
# - reference: Reference image analysis
# - sequence: Multi-image sequence validation
# - error_detection: Visual error detection
# - composition: Composition scoring
# - prompt_alignment: Prompt-to-image alignment
```

## Testing

Run the test suite:

```bash
# Run all vision tests
python tests/test_vision.py

# Run specific test
python -m pytest tests/test_vision.py::test_data_models -v
```

## Performance Considerations

### Model Selection

- **Phi-3.5-vision**: Recommended for most use cases (8GB VRAM, faster)
- **LLaVA-OneVision**: Best quality but slower (14GB VRAM)

### Memory Management

```python
# Clean up after use to free memory
generator.cleanup()

# For batch processing, process in chunks
for i in range(0, len(images), batch_size):
    batch = images[i:i+batch_size]
    # Process batch
    generator.cleanup()  # Free memory between batches
```

### Inference Speed

- CPU inference: ~10-30 seconds per image
- GPU inference: ~2-5 seconds per image
- Quality threshold tuning can reduce re-generation overhead

## Troubleshooting

### Common Issues

1. **Module not found errors**:
   ```bash
   pip install transformers accelerate scipy
   ```

2. **CUDA out of memory**:
   - Use smaller model (phi-3.5-vision)
   - Reduce batch size
   - Process images sequentially
   - Call `generator.cleanup()` regularly

3. **Slow inference on CPU**:
   - Expected behavior
   - Consider using GPU if available
   - Reduce number of validation checks

## References

- [LLaVA-OneVision Documentation](https://huggingface.co/docs/transformers/en/model_doc/llava_onevision)
- [Phi-3.5-vision Model](https://huggingface.co/microsoft/Phi-3.5-vision-instruct)
- [PIPELINE.md - Section 4: Vision Guidance](../PIPELINE.md)
- [docs/CHILD_ISSUES.md - Vision Guidance Integration](../docs/CHILD_ISSUES.md)

## License

This module is part of the StoryGenerator project.
