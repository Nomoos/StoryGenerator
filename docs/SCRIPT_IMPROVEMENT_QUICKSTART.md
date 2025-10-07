# Script Improvement - Quick Start Guide

This guide helps you get started with the Script Improvement feature that uses GPT or local LLM to enhance script quality.

## Overview

The Script Improvement tool:
- Scores scripts using an 8-criteria rubric (Hook Quality, Character Development, Plot Structure, etc.)
- Iteratively improves scripts using LLM feedback
- Saves improved versions (v2, v3, v4...) until quality plateaus
- Tracks all versions and scores for analysis

## Quick Start

### 1. Prerequisites

**Option A: Using Local LLM (Recommended)**
```bash
# Install Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# Pull the recommended model
ollama pull qwen2.5:14b-instruct

# Verify Ollama is running
ollama list
```

**Option B: Using OpenAI GPT**
- Set your OpenAI API key in environment variable
- Update the model provider in the code

### 2. Place Your Scripts

Put your scripts in the appropriate directory:
```
data/raw_local/{segment}/{age}/{title_id}.md
```

Example:
```bash
# For men aged 18-23
mkdir -p data/raw_local/men/18-23
echo "# Your Story Title

Your story content here..." > data/raw_local/men/18-23/my_story_001.md
```

### 3. Run the Improvement Process

**Improve a single script:**
```bash
cd CSharp/Examples
dotnet run --project ../StoryGenerator.Pipeline/StoryGenerator.Pipeline.csproj \
  --segment men --age 18-23 --title-id my_story_001
```

**Improve all scripts in a segment:**
```bash
cd CSharp/Examples  
dotnet run --project ../StoryGenerator.Pipeline/StoryGenerator.Pipeline.csproj \
  --segment men --age 18-23
```

**Improve all scripts:**
```bash
cd CSharp/Examples
dotnet run --project ../StoryGenerator.Pipeline/StoryGenerator.Pipeline.csproj --all
```

### 4. Review Results

**Improved scripts are saved to:**
```
data/gpt_improved/{segment}/{age}/{title_id}_v2.md
data/gpt_improved/{segment}/{age}/{title_id}_v3.md
...
```

**Scores are saved to:**
```
scores/{segment}/{age}/{title_id}_script_v1_score.json
scores/{segment}/{age}/{title_id}_script_v2_score.json
...
```

## Sample Output

### Score File Format
```json
{
  "version": "v2",
  "titleId": "my_story_001",
  "targetAudience": {
    "gender": "men",
    "age": "18-23"
  },
  "rubricScores": {
    "hookQuality": 85,
    "characterDevelopment": 70,
    "plotStructure": 80,
    "dialogueQuality": 75,
    "emotionalImpact": 80,
    "audienceAlignment": 85,
    "clarity": 90,
    "voiceSuitability": 85
  },
  "narrativeCohesion": 82,
  "overallScore": 81.5,
  "feedback": "Strong opening and clear structure. Could improve character depth.",
  "areasForImprovement": [
    "Deepen character motivations in the second act",
    "Add more sensory details to enhance immersion"
  ],
  "strengths": [
    "Compelling hook that grabs attention immediately",
    "Clear and easy-to-follow narrative structure",
    "Natural dialogue suitable for voice synthesis"
  ]
}
```

## How It Works

1. **Initial Scoring**: The original script (v1) is scored using the LLM-based rubric
2. **Improvement Generation**: Based on feedback, an improved version (v2) is created
3. **Re-scoring**: The improved version is scored again
4. **Iteration Decision**: 
   - If v2 score > v1 score + 2 points: Create v3
   - If improvement < 2 points: Stop (plateau reached)
   - Maximum 5 iterations (up to v6)
5. **Best Version Selection**: The highest-scoring version is marked as the best

## Configuration

### Model Selection

Edit your configuration to use different models:

```csharp
// Recommended models (in order of quality/speed tradeoff)
"qwen2.5:14b-instruct"        // Best quality, slower
"llama3.1:8b-instruct"        // Good balance
"qwen2.5:14b-instruct-q4_K_M" // Faster, quantized
"llama3.1:8b-instruct-q4_K_M" // Fastest
```

### Scoring Rubric

The 8 criteria evaluated (0-100 each):

1. **Hook Quality**: Opening engagement and attention-grabbing
2. **Character Development**: Character depth and relatability
3. **Plot Structure**: Story pacing and progression
4. **Dialogue Quality**: Natural and effective dialogue
5. **Emotional Impact**: Emotional resonance
6. **Audience Alignment**: Fit with target demographic
7. **Clarity**: Readability and flow
8. **Voice Suitability**: Text-to-speech compatibility

Plus **Narrative Cohesion**: Overall story flow (0-100)

## Troubleshooting

### "Model not found"
```bash
# List available models
ollama list

# Pull the model
ollama pull qwen2.5:14b-instruct
```

### "Connection refused"
```bash
# Check if Ollama is running
systemctl status ollama  # Linux
# or
ps aux | grep ollama

# Restart Ollama
ollama serve
```

### Low quality improvements
- Try a larger model (qwen2.5:14b instead of llama3.1:8b)
- Check if the original script has fundamental structural issues
- Review the feedback in the score files for specific guidance

### Scripts not found
- Verify directory structure: `data/raw_local/{segment}/{age}/`
- Check file extension is `.md`
- Ensure segment is "men" or "women" and age is valid range

## Advanced Usage

### Programmatic Usage

```csharp
using StoryGenerator.Core.LLM;
using StoryGenerator.Tools;
using StoryGenerator.Models;

// Initialize components
var modelProvider = new OllamaModelProvider("qwen2.5:14b-instruct");
var fileManager = new ScriptFileManager();
var scriptScorer = new ScriptScorer(modelProvider, fileManager);
var scriptIterator = new ScriptIterator(modelProvider, fileManager);
var scriptImprover = new ScriptImprover(
    modelProvider, scriptScorer, scriptIterator, fileManager,
    basePath, basePath);

// Improve a script
var audience = new AudienceSegment("men", "18-23");
var bestVersion = await scriptImprover.ImproveScriptAsync(
    scriptPath, titleId, audience);

Console.WriteLine($"Best: {bestVersion.Version} ({bestVersion.Score:F1}/100)");
```

### Custom Scoring

Modify `ScriptScorer.cs` to customize the rubric or adjust scoring weights.

### Batch Processing

Process multiple scripts in parallel:

```csharp
var tasks = scriptPaths.Select(path => 
    scriptImprover.ImproveScriptAsync(path, titleId, audience));
var results = await Task.WhenAll(tasks);
```

## Integration with Pipeline

The script improvement can be integrated into the full video generation pipeline:

1. Generate story ideas
2. Generate initial scripts
3. **→ Improve scripts (this feature)**
4. Score and select best scripts
5. Generate audio/voiceover
6. Create visuals
7. Compose final video

## Performance

Typical processing times (depends on hardware):

- **qwen2.5:14b-instruct**: 30-60 seconds per iteration
- **llama3.1:8b-instruct**: 15-30 seconds per iteration
- **Quantized models**: 10-20 seconds per iteration

A full improvement cycle (original + 3-5 iterations) takes 2-5 minutes per script.

## Next Steps

- Review the [full documentation](CSharp/Tools/SCRIPT_IMPROVEMENT_README.md)
- Check [code quality details](CSharp/CODE_QUALITY_IMPROVEMENTS.md)
- Explore the [example scripts](CSharp/Examples/)
- See the [architecture guide](ARCHITECTURE.md)

## Support

For issues or questions:
1. Check the [troubleshooting section](#troubleshooting)
2. Review error messages in console output
3. Verify directory structure and file permissions
4. Check Ollama logs if using local LLM

---

**Version**: 1.0  
**Last Updated**: 2024  
**Compatibility**: .NET 8.0+, Ollama 0.1.0+
