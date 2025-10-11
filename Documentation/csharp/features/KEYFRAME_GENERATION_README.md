# Keyframe Generation Per Scene (SDXL)

This feature implements per-shot keyframe generation using Stable Diffusion XL (SDXL) as specified in the issue requirements.

## Overview

The keyframe generation system creates high-quality images for each shot in a story, with the following capabilities:

- **Per-shot prompts**: Generates detailed prompts including style, camera angles, mood, and age-safe content filtering
- **SDXL Base + Refiner**: Uses SDXL base model with optional refiner for enhanced quality
- **LoRA/ControlNet support**: Optional v2 generation with LoRA or ControlNet for character/style consistency
- **Top-N selection**: Generates multiple variants per shot and selects the best ones
- **Organized file structure**: Saves outputs to organized directories by segment, age rating, and version

## File Structure

Generated keyframes are organized as follows:

```
images/
├── keyframes_v1/              # Base + Refiner generations
│   └── {segment}/             # e.g., "shorts", "long-form"
│       └── {age}/             # e.g., "all-ages", "13+", "18+"
│           ├── {title_id}_prompts.json
│           ├── {title_id}_manifest.json
│           └── {title_id}/
│               ├── shot_001_A1.png
│               ├── shot_001_A2.png
│               ├── shot_002_A1.png
│               └── ...
│
└── keyframes_v2/              # LoRA/ControlNet generations
    └── {segment}/
        └── {age}/
            ├── {title_id}_prompts.json
            ├── {title_id}_manifest.json
            └── {title_id}/
                ├── shot_001_B1.png
                ├── shot_001_B2.png
                └── ...
```

## Components

### Models

**KeyframeModels.cs** contains:
- `KeyframePrompt`: Structured prompt with visual description, style, camera, mood, and age-safe filtering
- `GeneratedKeyframe`: Metadata for each generated image including path, settings, and quality metrics
- `KeyframeManifest`: Complete record of all generated keyframes with selection information
- `KeyframeGenerationConfig`: Configuration for the generation process

### Service Interface

**IKeyframeGenerationService.cs** defines:
- `GenerateKeyframesAsync()`: Generate keyframes for all shots in a shotlist
- `GenerateKeyframesForShotAsync()`: Generate keyframes for a single shot
- `CreatePromptForShot()`: Create a detailed prompt from shot information
- `SelectTopKeyframes()`: Select the best N keyframes per shot
- `SavePromptsAsync()`: Save prompts to JSON
- `SaveManifestAsync()`: Save manifest to JSON

### Implementation

**KeyframeGenerationService.cs** implements the interface with:
- Integration with `IImageGenerationClient` for SDXL
- Prompt engineering with style, camera, mood, and safety filters
- Batch generation with progress tracking
- Quality-based selection (extensible for vision-based ranking)
- Structured JSON output

## Usage

### Basic Usage

```csharp
using StoryGenerator.Core.Interfaces;
using StoryGenerator.Generators;
using StoryGenerator.Models;

// Create the service with an SDXL image client
var imageClient = new YourSDXLImageClient(); // Implement IImageGenerationClient
var keyframeService = new KeyframeGenerationService(imageClient);

// Configure generation
var config = new KeyframeGenerationConfig
{
    VariantsPerShot = 4,      // Generate 4 variants per shot
    TopNPerShot = 2,          // Select top 2 per shot
    Width = 1024,
    Height = 1024,
    BaseSteps = 40,           // SDXL base steps
    RefinerSteps = 20,        // Refiner steps
    UseRefiner = true,
    AgeSafeContent = true,
    OutputBaseDir = "images"
};

// Generate keyframes for a shotlist
var manifest = await keyframeService.GenerateKeyframesAsync(
    shotlist,                 // StructuredShotlist from LLM
    titleId: "story_123",
    segment: "shorts",
    age: "all-ages",
    config: config
);

Console.WriteLine($"Generated {manifest.Keyframes.Count} keyframes");
Console.WriteLine($"Selected {manifest.SelectedKeyframes.Values.Sum(v => v.Count)} top keyframes");
```

### V2 Generation with LoRA

```csharp
var configV2 = new KeyframeGenerationConfig
{
    VariantsPerShot = 4,
    TopNPerShot = 2,
    Width = 1024,
    Height = 1024,
    BaseSteps = 40,
    RefinerSteps = 20,
    UseRefiner = true,
    LoraPath = "/path/to/character_lora.safetensors",
    LoraScale = 0.75,
    AgeSafeContent = true,
    OutputBaseDir = "images"
};

var manifestV2 = await keyframeService.GenerateKeyframesAsync(
    shotlist,
    titleId: "story_123",
    segment: "shorts",
    age: "all-ages",
    config: configV2
);

// This will save to images/keyframes_v2/ with variant IDs like B1, B2, etc.
```

### Prompt Structure

The service automatically creates structured prompts from shot information:

```json
{
  "shot_number": 1,
  "visual_prompt": "Beautiful mountain peaks with golden sunrise light, misty valleys below",
  "camera": "wide shot, eye level, static, rule of thirds",
  "mood": "serene, peaceful, golden hour, warm oranges and blues",
  "style": "cinematic, high quality, detailed, professional photography",
  "age_safe": true,
  "negative_prompt": "nsfw, nude, sexual, violence, gore, disturbing, inappropriate, low quality, blurry, distorted, ugly, deformed, bad anatomy",
  "combined_prompt": "Beautiful mountain peaks with golden sunrise light, misty valleys below, wide shot, eye level, static, rule of thirds, serene, peaceful, golden hour, warm oranges and blues, cinematic, high quality, detailed, professional photography"
}
```

### Manifest Output

The manifest JSON contains complete generation information:

```json
{
  "title_id": "story_123",
  "segment": "shorts",
  "age": "all-ages",
  "version": "v1",
  "variants_per_shot": 4,
  "top_n_per_shot": 2,
  "prompts": [...],
  "keyframes": [
    {
      "shot_number": 1,
      "variant_id": "A1",
      "file_path": "images/keyframes_v1/shorts/all-ages/story_123/shot_001_A1.png",
      "generation_method": "base+refiner",
      "width": 1024,
      "height": 1024,
      "seed": 42,
      "generation_time_ms": 2350,
      "is_selected": true
    }
  ],
  "selected_keyframes": {
    "1": ["shot_001_A1.png", "shot_001_A3.png"],
    "2": ["shot_002_A2.png", "shot_002_A4.png"]
  },
  "generation_config": {...},
  "total_generation_time_seconds": 45.6
}
```

## Integration with Pipeline

To integrate with the existing pipeline:

1. **After shotlist generation**: Call the keyframe service with the generated `StructuredShotlist`
2. **Use generated keyframes**: Feed keyframes to video synthesis (LTX-Video, RIFE interpolation, etc.)
3. **Track progress**: Use the manifest to track which keyframes were generated and selected

Example pipeline integration:

```csharp
// Step 1: Generate shotlist
var shotlist = await shotlistGenerator.GenerateStructuredShotlistAsync(script, audioDuration);

// Step 2: Generate keyframes
var keyframeManifest = await keyframeService.GenerateKeyframesAsync(
    shotlist, titleId, segment, age, keyframeConfig);

// Step 3: Use keyframes for video synthesis
var videoClips = await videoSynthesizer.GenerateFromKeyframesAsync(
    keyframeManifest.SelectedKeyframes, shotlist);
```

## Example

See `CSharp/Examples/KeyframeGenerationExample.cs` for a complete working example with:
- Sample shotlist creation
- Keyframe generation configuration
- Mock SDXL client for demonstration

Run the example:

```bash
cd CSharp/StoryGenerator.Pipeline
dotnet run
```

## Requirements

### SDXL Implementation

You need to implement `IImageGenerationClient` to connect to SDXL. Options include:

1. **Hugging Face Diffusers** (Python interop):
   - Use the existing Python bridge in the codebase
   - Call Diffusers pipeline from C#

2. **Stability AI API**:
   - Implement HTTP client for Stability AI REST API
   - Handle authentication and image download

3. **Local ONNX Runtime**:
   - Convert SDXL to ONNX format
   - Use Microsoft.ML.OnnxRuntime for inference

4. **ComfyUI/Automatic1111**:
   - Integrate with existing UI servers via HTTP API
   - Send prompts and receive generated images

### Dependencies

The keyframe generation service requires:
- .NET 9.0 or later
- System.Text.Json for JSON serialization
- An implementation of `IImageGenerationClient`

## Configuration Options

### KeyframeGenerationConfig Properties

| Property | Default | Description |
|----------|---------|-------------|
| `VariantsPerShot` | 4 | Number of image variants to generate per shot |
| `TopNPerShot` | 2 | Number of best variants to select per shot |
| `Width` | 1024 | Generated image width in pixels |
| `Height` | 1024 | Generated image height in pixels |
| `BaseSteps` | 40 | Inference steps for SDXL base model |
| `RefinerSteps` | 20 | Inference steps for SDXL refiner |
| `GuidanceScale` | 7.5 | Classifier-free guidance scale |
| `UseRefiner` | true | Whether to use the refiner for enhanced quality |
| `LoraPath` | null | Path to LoRA weights (optional, for v2) |
| `LoraScale` | 0.75 | LoRA strength (0.0-1.0) |
| `UseControlNet` | false | Whether to use ControlNet (optional, for v2) |
| `AgeSafeContent` | true | Enable age-safe content filtering |
| `OutputBaseDir` | "images" | Base directory for output files |

## Future Enhancements

Potential improvements:
1. **Quality ranking**: Use vision models (CLIP, aesthetic predictor) to rank generated keyframes
2. **Character consistency**: Implement face detection and matching across shots
3. **Style transfer**: Support custom style LoRAs for consistent artistic look
4. **Batch optimization**: Parallel generation for faster processing
5. **Caching**: Cache prompts and reuse for similar shots
6. **A/B testing**: Generate variations with different prompts/settings for comparison

## License

This code is part of the StoryGenerator project and follows the same license terms.
