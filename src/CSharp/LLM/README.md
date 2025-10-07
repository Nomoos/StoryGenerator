# LLM Content & Shotlist Generation

This module provides C# interfaces and implementations for LLM-based content generation, including script generation, scene breakdown, and detailed shotlist creation with emotions and camera directions.

## Overview

The LLM module enables:
- **Script Generation**: Create engaging short-form video scripts using LLMs
- **Scene Breakdown**: Analyze scripts and break them into individual scenes
- **Shotlist Generation**: Generate detailed, structured shotlists with timing, emotions, camera directions, and visual elements
- **Video Descriptions**: Create detailed visual prompts for AI image/video generation
- **JSON Output**: Structured, parseable shotlist data

## Supported Models

### Recommended Models

1. **Qwen2.5-14B-Instruct** (Primary recommendation)
   - Best for detailed creative descriptions
   - Better scene understanding and emotional nuance
   - HuggingFace: [unsloth/Qwen2.5-14B-Instruct](https://huggingface.co/unsloth/Qwen2.5-14B-Instruct)
   - Ollama model name: `qwen2.5:14b-instruct`

2. **Llama-3.1-8B-Instruct** (Fast alternative)
   - Faster inference (2-3x speed)
   - Good balance of quality and performance
   - HuggingFace: [meta-llama/Llama-3.1-8B-Instruct](https://huggingface.co/meta-llama/Llama-3.1-8B-Instruct)
   - Ollama model name: `llama3.1:8b-instruct`

### Quantized Models (for lower VRAM)

- `qwen2.5:14b-instruct-q4_K_M` - 4-bit quantization (~8GB VRAM)
- `llama3.1:8b-instruct-q4_K_M` - 4-bit quantization (~5GB VRAM)

## Architecture

### Core Interfaces

```
ILLMModelProvider          # Abstraction for LLM providers (Ollama, Transformers, etc.)
  └── OllamaModelProvider   # Ollama CLI implementation

ILLMContentGenerator       # Content generation interface
  └── LLMContentGenerator   # Implementation using model provider

ILLMShotlistGenerator      # Shotlist generation with structured output
  └── LLMShotlistGenerator  # Implementation with JSON parsing
```

### Key Classes

- **PromptTemplates**: Pre-engineered prompts for various generation tasks
- **ShotlistParser**: JSON parsing with validation and error correction
- **StructuredShotlist**: Enhanced shotlist with emotions, camera directions, and metadata
- **ModelInfo**: Model metadata and capabilities

## Installation & Setup

### 1. Install Ollama

```bash
# Linux/macOS
curl -fsSL https://ollama.com/install.sh | sh

# Windows
# Download from https://ollama.com/download/windows
```

### 2. Pull Recommended Models

```bash
# Pull Qwen2.5 14B Instruct (recommended)
ollama pull qwen2.5:14b-instruct

# Or pull Llama 3.1 8B Instruct (faster)
ollama pull llama3.1:8b-instruct

# Or quantized versions for lower VRAM
ollama pull qwen2.5:14b-instruct-q4_K_M
```

### 3. Verify Installation

```bash
# List available models
ollama list

# Test model
ollama run qwen2.5:14b-instruct "Hello, how are you?"
```

## Usage Examples

### Basic Setup

```csharp
using StoryGenerator.Core.Interfaces;
using StoryGenerator.Core.LLM;

// Create Ollama provider
var modelProvider = new OllamaModelProvider(
    defaultModel: RecommendedModels.Qwen25_14B_Instruct
);

// Create content generator
var contentGenerator = new LLMContentGenerator(modelProvider);

// Create shotlist generator
var shotlistGenerator = new LLMShotlistGenerator(contentGenerator);
```

### Generate Script from Story Idea

```csharp
// Assume you have a story idea
var storyIdea = new StoryIdea
{
    Title = "The Last Library",
    Description = "In a world where books are illegal, one librarian protects the last library",
    Tone = "mysterious and hopeful"
};

// Generate script
var script = await contentGenerator.GenerateScriptAsync(
    storyIdea,
    targetLength: 360,  // ~60 seconds
    temperature: 0.7f   // Creative but focused
);

Console.WriteLine(script);
```

### Generate Scene Breakdown

```csharp
var sceneBreakdown = await contentGenerator.GenerateSceneBreakdownAsync(
    scriptText: script,
    temperature: 0.5f  // More deterministic for structure
);

Console.WriteLine(sceneBreakdown);
```

### Generate Structured Shotlist

```csharp
// Generate complete shotlist with JSON structure
var shotlist = await shotlistGenerator.GenerateStructuredShotlistAsync(
    scriptText: script,
    audioDuration: 58.5f,  // Duration in seconds
    temperature: 0.5f
);

// Access structured data
Console.WriteLine($"Story: {shotlist.StoryTitle}");
Console.WriteLine($"Duration: {shotlist.TotalDuration}s");
Console.WriteLine($"Overall Mood: {shotlist.OverallMood}");
Console.WriteLine($"Shots: {shotlist.Shots.Count}");

foreach (var shot in shotlist.Shots)
{
    Console.WriteLine($"\nShot {shot.ShotNumber}: {shot.StartTime:F1}s - {shot.EndTime:F1}s");
    Console.WriteLine($"  Scene: {shot.SceneDescription}");
    Console.WriteLine($"  Emotion: {shot.PrimaryEmotion}");
    Console.WriteLine($"  Camera: {shot.CameraDirection.ShotType}, {shot.CameraDirection.Angle}");
    Console.WriteLine($"  Movement: {shot.CameraDirection.Movement}");
    Console.WriteLine($"  Visual Prompt: {shot.VisualPrompt}");
}
```

### Generate Video Description for Image Generation

```csharp
var videoDescription = await contentGenerator.GenerateVideoDescriptionAsync(
    sceneDescription: "A dusty old library filled with ancient books",
    mood: "mysterious and nostalgic",
    temperature: 0.6f
);

// Use this description with Stable Diffusion, Midjourney, etc.
Console.WriteLine(videoDescription);
```

### Refine Shotlist Details

```csharp
// Enhance shotlist with more detailed camera work and visuals
var refinedShotlist = await shotlistGenerator.RefineShotlistAsync(
    shotlist,
    temperature: 0.4f
);
```

### Generate Camera Direction for Specific Shot

```csharp
var shot = shotlist.Shots[0];
var cameraDirection = await shotlistGenerator.GenerateCameraDirectionAsync(shot);

Console.WriteLine($"Shot Type: {cameraDirection.ShotType}");
Console.WriteLine($"Angle: {cameraDirection.Angle}");
Console.WriteLine($"Movement: {cameraDirection.Movement}");
Console.WriteLine($"Focus: {cameraDirection.FocusPoint}");
Console.WriteLine($"Composition: {cameraDirection.Composition}");
```

### Export Shotlist to JSON

```csharp
using StoryGenerator.Core.LLM;

// Serialize to JSON file
var jsonOutput = ShotlistParser.SerializeToJson(shotlist);
await File.WriteAllTextAsync("shotlist.json", jsonOutput);
```

### Validate and Fix Shotlist Timing

```csharp
// Validate shotlist
var errors = ShotlistParser.ValidateShotlist(shotlist);
if (errors.Count > 0)
{
    Console.WriteLine("Validation errors:");
    errors.ForEach(e => Console.WriteLine($"  - {e}"));
}

// Auto-fix timing issues
shotlist = ShotlistParser.FixShotlistTiming(shotlist, targetDuration: 60.0f);

// Or use built-in validation
shotlist = await shotlistGenerator.ValidateAndCorrectTimingAsync(shotlist, 60.0f);
```

## Model Selection

### Choosing Between Qwen and Llama

| Feature | Qwen2.5-14B-Instruct | Llama-3.1-8B-Instruct |
|---------|---------------------|----------------------|
| Quality | ⭐⭐⭐⭐⭐ Excellent | ⭐⭐⭐⭐ Very Good |
| Speed | ⭐⭐⭐ Moderate | ⭐⭐⭐⭐⭐ Fast |
| VRAM | ~14GB (fp16), ~8GB (q4) | ~8GB (fp16), ~5GB (q4) |
| Creative Detail | Superior | Good |
| JSON Reliability | Excellent | Good |
| Best For | Production quality | Fast iteration |

### Switching Models

```csharp
// Use Qwen for production
var qwenProvider = new OllamaModelProvider(RecommendedModels.Qwen25_14B_Instruct);
var productionGenerator = new LLMContentGenerator(qwenProvider);

// Use Llama for testing/iteration
var llamaProvider = new OllamaModelProvider(RecommendedModels.Llama31_8B_Instruct);
var testGenerator = new LLMContentGenerator(llamaProvider);

// Or use fastest quantized model
var fastProvider = new OllamaModelProvider(RecommendedModels.Fastest);
var rapidGenerator = new LLMContentGenerator(fastProvider);
```

## Prompt Engineering

The module includes optimized prompts in `PromptTemplates`:

- **ScriptGenerationSystem**: System prompt for engaging script writing
- **SceneBreakdownSystem**: For detailed scene analysis
- **ShotlistGenerationSystem**: For structured JSON shotlist output
- **VideoDescriptionSystem**: For image generation prompts
- **CameraDirectionSystem**: For technical cinematography details

### Custom Prompts

```csharp
// Use custom prompts
var customScript = await contentGenerator.GenerateAsync(
    systemPrompt: "You are a horror story writer...",
    userPrompt: "Write a spooky 200-word script about...",
    temperature: 0.8f
);
```

## JSON Output Format

Example structured shotlist JSON:

```json
{
  "story_title": "The Last Library",
  "total_duration": 60.0,
  "overall_mood": "mysterious and hopeful",
  "style": "cinematic",
  "shots": [
    {
      "shot_number": 1,
      "start_time": 0.0,
      "end_time": 5.5,
      "duration": 5.5,
      "scene_description": "Wide shot of abandoned library exterior at dusk",
      "visual_prompt": "Cinematic establishing shot of a grand but weathered library...",
      "primary_emotion": "mystery",
      "secondary_emotions": ["curiosity", "melancholy"],
      "mood": "atmospheric",
      "camera_direction": {
        "shot_type": "wide",
        "angle": "eye-level",
        "movement": "slow-pan-right",
        "focus_point": "library facade",
        "depth_of_field": "deep",
        "composition": "rule-of-thirds"
      },
      "movement_type": "dynamic",
      "transition": "fade",
      "audio_description": "Opening narration begins",
      "character_focus": [],
      "key_elements": ["library", "dusk sky", "overgrown entrance"],
      "lighting": "golden hour, moody",
      "color_palette": "warm oranges, deep blues",
      "importance": 9
    }
  ]
}
```

## Performance Tips

1. **Use Quantized Models**: For faster inference with minimal quality loss
   ```csharp
   var provider = new OllamaModelProvider(RecommendedModels.Llama31_8B_Instruct_Q4);
   ```

2. **Adjust Temperature**: Lower for structure, higher for creativity
   - Scripts: 0.7-0.8 (creative)
   - Shotlists: 0.4-0.5 (structured)
   - Technical: 0.2-0.3 (precise)

3. **Batch Operations**: Generate multiple assets concurrently
   ```csharp
   var tasks = shots.Select(shot => 
       contentGenerator.GenerateVideoDescriptionAsync(shot.SceneDescription, shot.Mood)
   );
   var descriptions = await Task.WhenAll(tasks);
   ```

4. **GPU Acceleration**: Ensure Ollama uses GPU for 5-10x speedup
   ```bash
   # Check if GPU is detected
   ollama list
   # Should show GPU memory if available
   ```

## Testing and Comparison

### Compare Model Quality

```csharp
var qwenGenerator = new LLMContentGenerator(
    new OllamaModelProvider(RecommendedModels.Qwen25_14B_Instruct)
);

var llamaGenerator = new LLMContentGenerator(
    new OllamaModelProvider(RecommendedModels.Llama31_8B_Instruct)
);

var stopwatch = Stopwatch.StartNew();
var qwenResult = await qwenGenerator.GenerateScriptAsync(idea);
var qwenTime = stopwatch.Elapsed;

stopwatch.Restart();
var llamaResult = await llamaGenerator.GenerateScriptAsync(idea);
var llamaTime = stopwatch.Elapsed;

Console.WriteLine($"Qwen: {qwenTime.TotalSeconds:F2}s - Quality: {qwenResult.Length} chars");
Console.WriteLine($"Llama: {llamaTime.TotalSeconds:F2}s - Quality: {llamaResult.Length} chars");
```

## Troubleshooting

### Model Not Found
```bash
# Pull the model first
ollama pull qwen2.5:14b-instruct
```

### Out of Memory
```csharp
// Use quantized model
var provider = new OllamaModelProvider(RecommendedModels.Qwen25_14B_Instruct_Q4);
```

### JSON Parsing Errors
```csharp
// The parser automatically extracts JSON from mixed output
// and fixes common timing issues
try {
    var shotlist = ShotlistParser.ParseShotlist(llmOutput);
    shotlist = ShotlistParser.FixShotlistTiming(shotlist, duration);
} catch (JsonException ex) {
    Console.WriteLine($"Failed to parse: {ex.Message}");
}
```

### Slow Generation
- Use quantized models
- Reduce maxTokens parameter
- Use Llama 3.1 8B instead of Qwen 14B
- Ensure GPU is being used

## Future Enhancements

- [ ] Python transformers API support for direct model loading
- [ ] Fine-tuned models for shotlist generation
- [ ] Multi-modal input (images → descriptions)
- [ ] Batch generation optimization
- [ ] Caching for repeated prompts
- [ ] A/B testing framework for prompt variants

## References

- [Qwen2.5-14B-Instruct](https://huggingface.co/unsloth/Qwen2.5-14B-Instruct)
- [Llama-3.1-8B-Instruct](https://huggingface.co/meta-llama/Llama-3.1-8B-Instruct)
- [Ollama Documentation](https://ollama.com/docs)
- [StoryGenerator Architecture](../ARCHITECTURE.md)

## License

See repository root for license information.
