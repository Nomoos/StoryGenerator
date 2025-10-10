# Simple Keyframe Generation from Scene Description

This document describes the new feature that allows generating keyframes directly from simple scene descriptions and optional subtitles, without requiring a full `StructuredShotlist`.

## Overview

The `GenerateKeyframesFromSceneAsync` method provides a simplified API for generating keyframes when you have:
- A simple text description of a scene
- Optional subtitle text to include in the scene

**Important Note**: Subtitle text is incorporated into the image generation prompt (influencing the visual style and content), not rendered as actual text overlay on the image. For actual text rendering, use post-processing tools.

This is useful for:
- Quick prototyping and testing
- Single-scene generation
- Scenarios where you don't need complex shot planning
- Direct integration from user input or simple scripts

## Usage

### Basic Example - Scene Description Only

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
    VariantsPerShot = 3,      // Generate 3 variants
    TopNPerShot = 2,          // Select top 2
    Width = 1024,
    Height = 1024,
    BaseSteps = 30,
    UseRefiner = false,
    AgeSafeContent = true,
    OutputBaseDir = "images"
};

// Generate keyframes from scene description
var manifest = await keyframeService.GenerateKeyframesFromSceneAsync(
    sceneDescription: "A peaceful mountain landscape at sunrise with golden light",
    subtitles: null,
    titleId: "mountain_scene_001",
    config: config
);

Console.WriteLine($"Generated {manifest.Keyframes.Count} keyframes");
```

### Example with Subtitles

```csharp
// Generate keyframes with subtitle text overlay
var manifest = await keyframeService.GenerateKeyframesFromSceneAsync(
    sceneDescription: "A cozy coffee shop interior with warm lighting",
    subtitles: "Welcome to our cafe, where every cup tells a story",
    titleId: "coffee_shop_welcome",
    config: config
);
```

## Method Signature

```csharp
Task<KeyframeManifest> GenerateKeyframesFromSceneAsync(
    string sceneDescription,
    string? subtitles,
    string titleId,
    KeyframeGenerationConfig config,
    CancellationToken cancellationToken = default)
```

### Parameters

- **sceneDescription** (required): Text description of the scene to visualize
- **subtitles** (optional): Subtitle text to include in the scene. When provided, it's added to the visual prompt as "Text overlay: {subtitles}"
- **titleId** (required): Unique identifier for this scene/title
- **config** (required): Configuration for keyframe generation (variants, size, quality, etc.)
- **cancellationToken** (optional): Token for cancellation support

### Returns

`KeyframeManifest` containing:
- All generated keyframe variants
- Selected top N keyframes
- Generation metadata
- File paths to saved images
- Prompts used for generation

## How It Works

The method internally:

1. Creates a simple `StructuredShotlist` with a single shot
2. Sets default camera settings (medium shot, eye level, static, balanced composition)
3. Combines scene description and subtitles into the visual prompt
4. Calls the existing `GenerateKeyframesAsync` method
5. Returns the complete manifest

### Generated File Structure

Keyframes are saved to:
```
{OutputBaseDir}/keyframes_{version}/single-scene/{age}/{titleId}/
├── shot_001_A1.png
├── shot_001_A2.png
├── shot_001_A3.png
└── ...
```

Metadata files:
```
{OutputBaseDir}/keyframes_{version}/single-scene/{age}/
├── {titleId}_prompts.json
└── {titleId}_manifest.json
```

## Differences from Full Shotlist Generation

| Feature | GenerateKeyframesFromSceneAsync | GenerateKeyframesAsync |
|---------|--------------------------------|------------------------|
| Input | Simple scene description + subtitles | Full StructuredShotlist with multiple shots |
| Shots | Single shot | Multiple shots with timing |
| Camera Control | Default settings (medium shot, eye level) | Full control per shot |
| Timing | Fixed 10s duration | Custom timing per shot |
| Use Case | Quick single scenes, prototyping | Full story production |
| Segment | Always "single-scene" | Configurable (shorts, long-form, etc.) |

## Example Scenarios

### 1. Product Visualization

```csharp
await service.GenerateKeyframesFromSceneAsync(
    "A sleek smartphone on a minimalist desk with soft natural lighting",
    "Introducing the new XPhone Pro",
    "product_xphone_001",
    config
);
```

### 2. Location Showcase

```csharp
await service.GenerateKeyframesFromSceneAsync(
    "A pristine beach with turquoise water and white sand under blue sky",
    null,  // No subtitles
    "beach_paradise_001",
    config
);
```

### 3. Mood/Atmosphere

```csharp
await service.GenerateKeyframesFromSceneAsync(
    "A dark rainy street with neon signs reflecting in puddles, cyberpunk aesthetic",
    "Neo Tokyo - 2077",
    "cyberpunk_street_001",
    config
);
```

### 4. Character Introduction

```csharp
await service.GenerateKeyframesFromSceneAsync(
    "A mysterious figure in a long coat standing in fog, silhouette visible",
    "Detective Morgan arrives at the scene",
    "detective_intro_001",
    config
);
```

## Prompt Construction

The method automatically constructs prompts with:

1. **Visual Description**: Your scene description
2. **Subtitle Integration**: When provided, added as `"Text overlay: {subtitles}"`
3. **Camera Details**: Default medium shot, eye level, static, balanced composition
4. **Mood**: Default "neutral" and "general"
5. **Style**: Cinematic style with quality enhancers
6. **Age-Safe Content**: Based on config.AgeSafeContent setting

Example generated prompt:
```
"A peaceful mountain landscape at sunrise with golden light, 
medium shot, eye level, static, balanced, neutral, general, 
cinematic, high quality, detailed, professional photography"
```

With subtitles:
```
"A cozy coffee shop interior with warm lighting. 
Text overlay: "Welcome to our cafe", 
medium shot, eye level, static, balanced, neutral, general, 
cinematic, high quality, detailed, professional photography"
```

## Full Example Application

See `CSharp/Examples/SimpleKeyframeGenerationExample.cs` for a complete working example that demonstrates:
- Scene description without subtitles
- Scene description with subtitles  
- Multiple scene types
- Mock SDXL client for testing

**Note**: The example file is provided as a reference. To use it, you would need to integrate it into an executable project (such as the CLI or Pipeline project) that can run the example code.

## Configuration Tips

### For Quick Prototyping
```csharp
var config = new KeyframeGenerationConfig
{
    VariantsPerShot = 2,
    TopNPerShot = 1,
    Width = 512,
    Height = 512,
    BaseSteps = 20,
    UseRefiner = false,  // Faster
    AgeSafeContent = true
};
```

### For High Quality
```csharp
var config = new KeyframeGenerationConfig
{
    VariantsPerShot = 4,
    TopNPerShot = 2,
    Width = 1024,
    Height = 1024,
    BaseSteps = 40,
    RefinerSteps = 20,
    UseRefiner = true,   // Better quality
    AgeSafeContent = true
};
```

### For Vertical Video (TikTok, Reels)
```csharp
var config = new KeyframeGenerationConfig
{
    VariantsPerShot = 3,
    TopNPerShot = 2,
    Width = 1080,
    Height = 1920,  // 9:16 aspect ratio
    BaseSteps = 30,
    UseRefiner = false,
    AgeSafeContent = true
};
```

## Error Handling

The method validates inputs and throws `ArgumentException` if:
- Scene description is null or whitespace
- Title ID is null or whitespace

```csharp
try
{
    var manifest = await service.GenerateKeyframesFromSceneAsync(
        sceneDescription,
        subtitles,
        titleId,
        config
    );
}
catch (ArgumentException ex)
{
    Console.WriteLine($"Invalid input: {ex.Message}");
}
catch (Exception ex)
{
    Console.WriteLine($"Generation failed: {ex.Message}");
}
```

## Integration with Existing Pipeline

This method is designed to work seamlessly with existing components:

```csharp
// Step 1: Generate keyframes from simple description
var keyframeManifest = await keyframeService.GenerateKeyframesFromSceneAsync(
    sceneDescription, subtitles, titleId, keyframeConfig);

// Step 2: Use selected keyframes for video synthesis
var selectedKeyframes = keyframeManifest.SelectedKeyframes[1]; // Shot 1
var videoClips = await videoSynthesizer.GenerateFromKeyframesAsync(
    selectedKeyframes, outputPath);

// Step 3: Add audio/music
await audioMixer.AddBackgroundMusicAsync(videoClips, musicPath);
```

## Limitations

- Only generates a single shot (for multiple shots, use `GenerateKeyframesAsync` with a full shotlist)
- Default camera settings (for custom camera work, use full shotlist)
- Fixed 10-second duration
- Subtitle text is embedded in the prompt, not as actual text overlay (use post-processing for actual text rendering)

## Future Enhancements

Potential improvements:
1. Support for multiple scenes in a single call
2. Custom camera settings parameter
3. Duration parameter
4. Automatic text overlay rendering (not just prompt-based)
5. Style presets (cinematic, cartoon, realistic, etc.)
6. Aspect ratio presets (16:9, 9:16, 1:1, etc.)

## License

This feature is part of the StoryGenerator project and follows the same license terms.
