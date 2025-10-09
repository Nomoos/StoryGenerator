# Script Improvement Tool

This tool improves scripts using GPT or local LLM (qwen2.5_14b) with iterative improvements until quality plateaus.

## Overview

The script improvement process:
1. Loads original scripts from `/data/raw_local/{segment}/{age}/`
2. Scores the script using an LLM-based rubric evaluation
3. Generates improved versions (v2, v3, v4, etc.)
4. Saves improved scripts to `/data/gpt_improved/{segment}/{age}/`
5. Saves scores to `/scores/{segment}/{age}/`
6. Continues iterating until improvement plateaus (< 2 points improvement)

## Architecture

### Components

1. **ScriptFileManager** - Handles file I/O operations
   - Reads/writes scripts from/to the correct directories
   - Manages score file storage
   - Generates proper file names

2. **ScriptScorer** - Evaluates script quality
   - Uses LLM to score scripts on 8 rubric criteria (0-100 each):
     - Hook Quality
     - Character Development
     - Plot Structure
     - Dialogue Quality
     - Emotional Impact
     - Audience Alignment
     - Clarity
     - Voice Suitability
   - Also evaluates Narrative Cohesion
   - Provides overall score and detailed feedback

3. **ScriptIterator** - Improves scripts based on feedback
   - Takes scoring feedback and generates improved versions
   - Uses LLM to apply targeted improvements
   - Maintains core narrative while enhancing weak areas

4. **ScriptImprover** - Orchestrates the improvement process
   - Manages iterative improvement loop
   - Tracks best version across iterations
   - Stops when improvement plateaus
   - Saves all versions and scores

## Usage

### Using the Example Application

```bash
cd /home/runner/work/StoryGenerator/StoryGenerator/CSharp/Examples
dotnet run --project ScriptImprovementExample.cs -- [options]
```

### Command Line Options

- `--base-path <path>` - Base project path (default: /home/runner/work/StoryGenerator/StoryGenerator)
- `--model <name>` - Model name (default: qwen2.5:14b-instruct)
- `--segment <segment>` - Audience segment: "men" or "women"
- `--age <range>` - Age range: "10-13", "14-17", "18-23", or "24-30"
- `--title-id <id>` - Specific title ID to improve
- `--all` - Improve all scripts across all segments

### Examples

**Improve all scripts in a specific segment:**
```bash
dotnet run --project ScriptImprovementExample.cs -- --segment men --age 18-23
```

**Improve a specific script:**
```bash
dotnet run --project ScriptImprovementExample.cs -- --segment men --age 18-23 --title-id test_story_001
```

**Improve all scripts across all segments:**
```bash
dotnet run --project ScriptImprovementExample.cs -- --all
```

**Use a different model:**
```bash
dotnet run --project ScriptImprovementExample.cs -- --model llama3.1:8b-instruct --segment women --age 24-30
```

### Using the API Programmatically

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
    modelProvider,
    scriptScorer,
    scriptIterator,
    fileManager,
    "/path/to/project",
    "/path/to/project"
);

// Improve a single script
var audience = new AudienceSegment("men", "18-23");
var bestVersion = await scriptImprover.ImproveScriptAsync(
    "/path/to/script.md",
    "story_001",
    audience
);

Console.WriteLine($"Best version: {bestVersion.Version}");
Console.WriteLine($"Score: {bestVersion.Score:F1}/100");

// Improve all scripts in a segment
var results = await scriptImprover.ImproveScriptsInSegmentAsync("men", "18-23");

// Improve all scripts across all segments
var allResults = await scriptImprover.ImproveAllScriptsAsync();
```

## Output Structure

### Improved Scripts
Saved to: `/data/gpt_improved/{segment}/{age}/{title_id}_{version}.md`

Example: `/data/gpt_improved/men/18-23/test_story_001_v2.md`

### Score Files
Saved to: `/scores/{segment}/{age}/{title_id}_script_{version}_score.json`

Example: `/scores/men/18-23/test_story_001_script_v2_score.json`

### Score File Format
```json
{
  "version": "v2",
  "titleId": "test_story_001",
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
  "feedback": "Overall feedback text",
  "areasForImprovement": [
    "Specific area 1",
    "Specific area 2"
  ],
  "strengths": [
    "Strength 1",
    "Strength 2"
  ]
}
```

## Configuration

### Model Selection

The tool supports any Ollama model. Recommended models:

- `qwen2.5:14b-instruct` - Best quality (default)
- `llama3.1:8b-instruct` - Good balance of speed and quality
- `qwen2.5:14b-instruct-q4_K_M` - Faster, less VRAM
- `llama3.1:8b-instruct-q4_K_M` - Fastest inference

### Iteration Settings

- **Improvement Threshold**: 2.0 points (minimum improvement to continue)
- **Max Iterations**: 5 (v2 through v6)

These can be adjusted in the `ScriptImprover` class constructor.

## Requirements

- .NET 9.0 or later
- Ollama installed and running (for local models)
- OR OpenAI API key (for GPT models)

### Installing Ollama

1. Visit [ollama.ai](https://ollama.ai)
2. Download and install for your platform
3. Pull a model: `ollama pull qwen2.5:14b-instruct`

## Troubleshooting

### Model not found
If you get "Model not found" error, ensure:
1. Ollama is installed and running
2. The model is pulled: `ollama pull qwen2.5:14b-instruct`
3. The model name matches exactly

### Connection errors
If you get connection errors:
1. Check if Ollama is running: `ollama list`
2. Verify the base URL (default: http://localhost:11434)
3. Try restarting Ollama

### Low quality improvements
If improvements aren't significant:
1. Try a larger model (e.g., qwen2.5:14b instead of llama3.1:8b)
2. Check if the original script has fundamental issues
3. Review the scoring feedback for specific areas to address

## Performance

- **qwen2.5:14b-instruct**: ~30-60 seconds per iteration
- **llama3.1:8b-instruct**: ~15-30 seconds per iteration

Processing times depend on:
- Model size and quantization
- Hardware (GPU/CPU)
- Script length
- System load

## Future Enhancements

- Support for GPT-4 via OpenAI API
- Parallel processing of multiple scripts
- Custom rubric criteria
- A/B testing of improved vs original scripts
- Integration with video generation pipeline
