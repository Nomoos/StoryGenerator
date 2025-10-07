# LLM Examples

This directory contains example code demonstrating how to use the LLM content and shotlist generation interfaces.

## Examples

### 1. LLMContentGenerationExample

Demonstrates basic LLM content generation:
- Script generation from story ideas
- Scene breakdown from scripts
- Video description generation for AI image/video models
- Saving outputs to files

**Usage:**
```csharp
await LLMContentGenerationExample.RunAsync();
```

**What it shows:**
- Setting up Ollama model provider
- Checking and pulling models
- Generating creative content with different temperature settings
- Saving generated content to files

### 2. LLMShotlistGenerationExample

Demonstrates structured shotlist generation:
- Complete shotlist with timing, emotions, and camera directions
- JSON output format
- Validation and error checking
- Refining shot details

**Usage:**
```csharp
await LLMShotlistGenerationExample.RunAsync();
```

**What it shows:**
- Generating structured JSON shotlists
- Accessing shot metadata (emotions, camera work, timing)
- Validating shotlist correctness
- Enhancing individual shots with more detail
- Exporting to JSON files

### 3. ModelComparisonExample

Compares Qwen2.5-14B-Instruct vs Llama-3.1-8B-Instruct:
- Performance benchmarking
- Quality comparison
- JSON parsing reliability
- Speed vs quality trade-offs

**Usage:**
```csharp
await ModelComparisonExample.RunAsync();
```

**What it shows:**
- Side-by-side model comparison
- Timing benchmarks for different generation tasks
- Quality metrics (detail level, completeness)
- Recommendations for model selection

## Prerequisites

### Install Ollama

```bash
# Linux/macOS
curl -fsSL https://ollama.com/install.sh | sh

# Windows
# Download from https://ollama.com/download/windows
```

### Pull Models

Before running the examples, pull at least one model:

```bash
# Qwen (recommended for quality)
ollama pull qwen2.5:14b-instruct

# Llama (recommended for speed)
ollama pull llama3.1:8b-instruct
```

## Running the Examples

### Option 1: From your code

```csharp
using StoryGenerator.Examples.LLM;

// Run content generation example
await LLMContentGenerationExample.RunAsync();

// Run shotlist generation example
await LLMShotlistGenerationExample.RunAsync();

// Run model comparison
await ModelComparisonExample.RunAsync();
```

### Option 2: Create a simple console app

```csharp
using System;
using System.Threading.Tasks;
using StoryGenerator.Examples.LLM;

class Program
{
    static async Task Main(string[] args)
    {
        Console.WriteLine("Select example to run:");
        Console.WriteLine("1. Content Generation");
        Console.WriteLine("2. Shotlist Generation");
        Console.WriteLine("3. Model Comparison");
        Console.Write("\nEnter choice (1-3): ");
        
        var choice = Console.ReadLine();
        
        try
        {
            switch (choice)
            {
                case "1":
                    await LLMContentGenerationExample.RunAsync();
                    break;
                case "2":
                    await LLMShotlistGenerationExample.RunAsync();
                    break;
                case "3":
                    await ModelComparisonExample.RunAsync();
                    break;
                default:
                    Console.WriteLine("Invalid choice");
                    break;
            }
        }
        catch (Exception ex)
        {
            Console.WriteLine($"Error: {ex.Message}");
            Console.WriteLine($"Stack trace: {ex.StackTrace}");
        }
    }
}
```

## Expected Output

### Content Generation Example

```
=== LLM Content Generation Example ===

Setting up LLM provider...
Using model: qwen2.5:14b-instruct
Provider: Ollama

Story Idea: The Last Library
Description: In a world where books are illegal, one librarian protects...
Tone: mysterious and hopeful

Generating script (this may take 30-60 seconds)...

--- Generated Script ---
[Generated script content here]

Script length: 365 words

Generating scene breakdown...

--- Scene Breakdown ---
[Scene breakdown content here]

...
```

### Shotlist Generation Example

```
=== LLM Shotlist Generation Example ===

...

--- Shotlist Overview ---
Title: The Last Library
Total Duration: 58.5s
Overall Mood: mysterious and hopeful
Style: cinematic
Number of Shots: 8
Model: qwen2.5:14b-instruct
Generation Time: 45.32s

--- Shot Breakdown ---

SHOT 1:
  Time: 0.0s - 5.5s (5.5s)
  Scene: Wide shot of abandoned library exterior at dusk
  Emotion: mystery
  Secondary Emotions: curiosity, melancholy
  Mood: atmospheric
  Camera:
    - Type: wide
    - Angle: eye-level
    - Movement: slow-pan-right
    - Focus: library facade
    - Composition: rule-of-thirds
  ...
```

### Model Comparison Example

```
=== LLM Model Comparison: Qwen vs Llama ===

=== Testing Qwen2.5-14B-Instruct ===
Model: qwen2.5:14b-instruct

Test 1: Script Generation
  Time: 32.45s
  Length: 203 words
  Quality Sample: In a world where books are banned...

Test 2: Scene Breakdown
  Time: 28.12s
  Length: 1245 characters

Test 3: Structured Shotlist Generation
  Time: 45.67s
  Shots: 6
  Duration: 40.0s
  Overall Mood: mysterious and hopeful
  Validation: ✓ Pass
  Quality: 6/6 shots with complete details

Performance Summary:
  Total Time: 106.24s
  Script: 32.45s
  Scene: 28.12s
  Shotlist: 45.67s
  JSON Parsing: ✓

=== Testing Llama-3.1-8B-Instruct ===
[Similar output, typically 2-3x faster but with lower quality scores]
```

## Output Files

Examples save generated content to:
```
output/llm-example/
  ├── script.txt
  ├── scene_breakdown.txt
  ├── video_description.txt
  └── shotlist.json
```

## Troubleshooting

### Model not found
```bash
# Pull the required model
ollama pull qwen2.5:14b-instruct
```

### Out of memory
```csharp
// Use quantized models (requires less VRAM)
var provider = new OllamaModelProvider(RecommendedModels.Qwen25_14B_Instruct_Q4);
```

### Slow generation
- Use Llama 3.1 8B instead of Qwen 14B
- Use quantized models
- Ensure GPU is being used (check with `nvidia-smi`)

### JSON parsing errors
- Try using Qwen (more reliable JSON output)
- Lower the temperature (0.3-0.5 for structured output)
- The parser has built-in error recovery for common issues

## Tips

1. **Start with Llama 3.1 8B** for fast iteration during development
2. **Switch to Qwen 2.5 14B** for production-quality content
3. **Use lower temperatures** (0.4-0.5) for structured output like shotlists
4. **Use higher temperatures** (0.7-0.8) for creative script writing
5. **Enable GPU acceleration** in Ollama for 5-10x speedup

## Next Steps

After running these examples:

1. Integrate into your own story generation pipeline
2. Customize prompt templates in `PromptTemplates.cs`
3. Fine-tune temperature and parameters for your use case
4. Build automated testing with model comparison
5. Create custom model providers (e.g., for Transformers API)

## Related Documentation

- [LLM Module README](../LLM/README.md) - Complete API documentation
- [Interfaces Guide](../INTERFACES_GUIDE.md) - Interface overview
- [Architecture](../../ARCHITECTURE.md) - System architecture

## Support

For issues or questions:
1. Check the main LLM README for detailed documentation
2. Verify Ollama is running (`ollama list`)
3. Check model availability
4. Review error messages and stack traces
