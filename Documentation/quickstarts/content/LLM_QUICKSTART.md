# LLM Content & Shotlist Generation - Quick Start Guide

This guide provides a quick overview of the LLM-based content and shotlist generation capabilities added to the StoryGenerator project.

## What's New

C# interfaces and implementations for:
- **Script Generation**: Create engaging scripts from story ideas using LLMs
- **Scene Breakdown**: Analyze scripts and break them into scenes with visual details
- **Shotlist Generation**: Generate structured shotlists with emotions, camera directions, and timing
- **Model Support**: Qwen2.5-14B-Instruct and Llama-3.1-8B-Instruct via Ollama

## Key Features

✅ **Structured JSON Output**: Parse LLM output into structured `StructuredShotlist` objects  
✅ **Emotions & Camera Directions**: Each shot includes primary/secondary emotions, camera type, angle, movement  
✅ **Timing Validation**: Automatic validation and correction of shot timing  
✅ **Prompt Engineering**: Pre-engineered templates optimized for story generation  
✅ **Model Comparison**: Built-in tools to compare Qwen vs Llama for quality/speed  
✅ **Extensible Design**: Clean interfaces support multiple LLM providers  

## Quick Start

### 1. Install Ollama

```bash
# Linux/macOS
curl -fsSL https://ollama.com/install.sh | sh

# Windows - download from https://ollama.com/download/windows
```

### 2. Pull a Model

```bash
# Qwen (best quality)
ollama pull qwen2.5:14b-instruct

# OR Llama (best speed)
ollama pull llama3.1:8b-instruct
```

### 3. Use in Your Code

```csharp
using StoryGenerator.Core.Interfaces;
using StoryGenerator.Core.LLM;

// Setup
var modelProvider = new OllamaModelProvider(RecommendedModels.Qwen25_14B_Instruct);
var contentGenerator = new LLMContentGenerator(modelProvider);
var shotlistGenerator = new LLMShotlistGenerator(contentGenerator);

// Generate shotlist
var shotlist = await shotlistGenerator.GenerateStructuredShotlistAsync(
    scriptText: "Your script here...",
    audioDuration: 60.0f
);

// Access structured data
foreach (var shot in shotlist.Shots)
{
    Console.WriteLine($"Shot {shot.ShotNumber}: {shot.SceneDescription}");
    Console.WriteLine($"  Emotion: {shot.PrimaryEmotion}");
    Console.WriteLine($"  Camera: {shot.CameraDirection.ShotType}, {shot.CameraDirection.Angle}");
    Console.WriteLine($"  Time: {shot.StartTime}s - {shot.EndTime}s");
}

// Export to JSON
var json = ShotlistParser.SerializeToJson(shotlist);
await File.WriteAllTextAsync("shotlist.json", json);
```

## Documentation

- **Complete API Documentation**: [CSharp/LLM/README.md](CSharp/LLM/README.md)
- **Implementation Details**: [CSharp/LLM/IMPLEMENTATION_SUMMARY.md](CSharp/LLM/IMPLEMENTATION_SUMMARY.md)
- **Usage Examples**: [CSharp/Examples/LLM/README.md](CSharp/Examples/LLM/README.md)

## Examples

Three complete examples are provided:

1. **LLMContentGenerationExample** - Basic content generation (scripts, scenes, descriptions)
2. **LLMShotlistGenerationExample** - Structured shotlist generation with full metadata
3. **ModelComparisonExample** - Compare Qwen vs Llama for quality and speed

Run examples:
```csharp
await LLMContentGenerationExample.RunAsync();
await LLMShotlistGenerationExample.RunAsync();
await ModelComparisonExample.RunAsync();
```

## Architecture

```
CSharp/
├── Interfaces/                    # Core interfaces
│   ├── ILLMContentGenerator.cs   # Content generation
│   ├── ILLMModelProvider.cs      # Model provider abstraction
│   └── ILLMShotlistGenerator.cs  # Shotlist generation
│
├── LLM/                           # Implementations
│   ├── LLMContentGenerator.cs    # Content generator
│   ├── LLMShotlistGenerator.cs   # Shotlist generator
│   ├── OllamaModelProvider.cs    # Ollama CLI provider
│   ├── PromptTemplates.cs        # Pre-engineered prompts
│   ├── ShotlistParser.cs         # JSON parsing utilities
│   └── README.md                 # Complete documentation
│
└── Examples/LLM/                  # Usage examples
    ├── LLMContentGenerationExample.cs
    ├── LLMShotlistGenerationExample.cs
    ├── ModelComparisonExample.cs
    └── README.md
```

## Model Recommendations

| Model | Best For | Speed | Quality | VRAM |
|-------|----------|-------|---------|------|
| Qwen2.5-14B-Instruct | Production | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | 14GB |
| Llama-3.1-8B-Instruct | Testing/Dev | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | 8GB |
| Qwen 14B Q4 | Balanced | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | 8GB |
| Llama 8B Q4 | Fast | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | 5GB |

**Recommendation**: Use Qwen for final production content, Llama for rapid iteration during development.

## Structured Shotlist Output

Each shotlist includes:

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
      "scene_description": "Wide shot of abandoned library at dusk",
      "visual_prompt": "Cinematic establishing shot...",
      "primary_emotion": "mystery",
      "secondary_emotions": ["curiosity", "melancholy"],
      "camera_direction": {
        "shot_type": "wide",
        "angle": "eye-level",
        "movement": "slow-pan-right",
        "focus_point": "library facade",
        "depth_of_field": "deep",
        "composition": "rule-of-thirds"
      },
      "lighting": "golden hour, moody",
      "color_palette": "warm oranges, deep blues",
      "importance": 9
    }
  ]
}
```

## Key Classes

### Interfaces
- `ILLMModelProvider` - Abstraction for LLM providers (Ollama, Transformers, etc.)
- `ILLMContentGenerator` - Script and content generation
- `ILLMShotlistGenerator` - Structured shotlist generation

### Models
- `StructuredShotlist` - Complete shotlist with metadata
- `StructuredShot` - Individual shot with emotions, camera work, timing
- `CameraDirection` - Detailed camera specifications
- `GenerationMetadata` - Generation statistics

### Utilities
- `PromptTemplates` - Pre-engineered prompts for various tasks
- `ShotlistParser` - JSON parsing with validation and error correction
- `RecommendedModels` - Recommended model names and configurations

## Troubleshooting

### Model not found
```bash
ollama pull qwen2.5:14b-instruct
```

### Out of memory
Use quantized models:
```csharp
var provider = new OllamaModelProvider(RecommendedModels.Qwen25_14B_Instruct_Q4);
```

### Slow generation
- Use Llama instead of Qwen
- Use quantized models
- Verify GPU usage with `nvidia-smi`

### JSON parsing errors
- Use Qwen (more reliable JSON)
- Lower temperature (0.4-0.5)
- Parser has automatic error recovery

## Performance Tips

1. **Temperature Settings**:
   - 0.7-0.8 for creative script writing
   - 0.5-0.6 for scene breakdowns
   - 0.4-0.5 for structured shotlists

2. **Model Selection**:
   - Development/Testing: Llama 3.1 8B Q4 (fastest)
   - Production: Qwen 2.5 14B (best quality)

3. **GPU Acceleration**: Ensure Ollama detects your GPU for 5-10x speedup

4. **Batch Processing**: Generate multiple shots concurrently when possible

## References

- **Qwen2.5-14B-Instruct**: https://huggingface.co/unsloth/Qwen2.5-14B-Instruct
- **Llama-3.1-8B-Instruct**: https://huggingface.co/meta-llama/Llama-3.1-8B-Instruct
- **Ollama**: https://ollama.com/docs

## Next Steps

1. Run the examples to see the interfaces in action
2. Read the complete documentation in `CSharp/LLM/README.md`
3. Integrate into your story generation pipeline
4. Customize prompts in `PromptTemplates.cs` for your use case
5. Compare models using `ModelComparisonExample`

## Support

For detailed information, see:
- [Complete API Documentation](CSharp/LLM/README.md)
- [Implementation Summary](CSharp/LLM/IMPLEMENTATION_SUMMARY.md)
- [Example Usage](CSharp/Examples/LLM/README.md)

---

**Status**: ✅ Complete and ready for use  
**Models Tested**: Qwen2.5-14B-Instruct, Llama-3.1-8B-Instruct  
**Implementation**: Ollama CLI (Python transformers support can be added)
