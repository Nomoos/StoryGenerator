# Scene Beat-Sheet and Subtitle Generators

This document describes the C# implementation for generating scene beat-sheets/shotlists and draft SRT subtitles from scripts.

## Overview

Two new generators have been implemented:

1. **SimpleSceneBeatsGenerator** - Generates structured beat-sheets and shotlists from scripts
2. **SubtitleGenerator** - Generates draft SRT subtitle files from scripts

Both generators follow the repository's folder structure conventions:
- Beat-sheets: `/scenes/json/{segment}/{age}/{title_id}_shots.json`
- Subtitles: `/subtitles/srt/{segment}/{age}/{title_id}_draft.srt`

## SimpleSceneBeatsGenerator

### Purpose
Generates a structured JSON beat-sheet/shotlist from script text without requiring an LLM. This is useful for quick prototyping and when LLM services are not available.

### Features
- Automatically splits scripts into scenes based on sentences
- Calculates timing for each scene based on word count and audio duration
- Generates visual prompts for each scene
- Outputs structured JSON with shot metadata

### Usage

```csharp
using StoryGenerator.Generators;
using StoryGenerator.Models;

// Create generator
var scenesPath = "/path/to/scenes";
var beatsGenerator = new SimpleSceneBeatsGenerator(scenesPath);

// Generate from script text
var shotsPath = await beatsGenerator.GenerateAndSaveBeatsAsync(
    scriptText: "Your script text here...",
    titleId: "story_001",
    segment: "women",
    age: "18-23",
    audioDuration: 58.5f
);

// Or generate from ScriptVersion object
var scriptVersion = new ScriptVersion
{
    TitleId = "story_001",
    Content = "Your script...",
    TargetAudience = new AudienceSegment("women", "18-23")
};

var shotsPath = await beatsGenerator.GenerateFromScriptVersionAsync(
    scriptVersion,
    audioDuration: 58.5f
);
```

### Output Format

The generator produces a JSON file with the following structure:

```json
{
  "titleId": "story_001",
  "totalDuration": 58.5,
  "totalShots": 5,
  "generatedAt": "2025-10-07T06:57:06.7795174Z",
  "shots": [
    {
      "shotNumber": 1,
      "startTime": 0,
      "endTime": 15,
      "duration": 15,
      "sceneDescription": "Scene description text...",
      "visualPrompt": "Visual prompt for image generation...",
      "narration": "Narration text..."
    }
  ]
}
```

## SubtitleGenerator

### Purpose
Generates draft SRT subtitle files from script text with estimated timing. These can be refined later with actual audio timing using ASR (Automatic Speech Recognition).

### Features
- Automatically splits text into subtitle-appropriate segments
- Respects SRT character limits (42 characters per line)
- Calculates timing based on word count and audio duration
- Generates standard SRT format

### Usage

```csharp
using StoryGenerator.Generators;
using StoryGenerator.Models;

// Create generator
var subtitlesPath = "/path/to/subtitles";
var subtitleGenerator = new SubtitleGenerator(subtitlesPath);

// Generate from script text
var srtPath = await subtitleGenerator.GenerateAndSaveSubtitlesAsync(
    scriptText: "Your script text here...",
    titleId: "story_001",
    segment: "women",
    age: "18-23",
    audioDuration: 58.5f  // Optional, improves timing accuracy
);

// Or generate from ScriptVersion object
var scriptVersion = new ScriptVersion
{
    TitleId = "story_001",
    Content = "Your script...",
    TargetAudience = new AudienceSegment("women", "18-23")
};

var srtPath = await subtitleGenerator.GenerateFromScriptVersionAsync(
    scriptVersion,
    audioDuration: 58.5f
);
```

### Output Format

The generator produces an SRT file with standard format:

```srt
1
00:00:00,000 --> 00:00:06,000
In a world where books are banned and

2
00:00:06,000 --> 00:00:10,500
libraries are just distant memories, one

3
00:00:10,500 --> 00:00:15,000
woman refuses to let knowledge die.
```

## Advanced: SceneBeatsGenerator with LLM

For more advanced scene analysis with emotions, camera directions, and detailed metadata, use the `SceneBeatsGenerator` class which leverages the LLM shotlist generator:

```csharp
using StoryGenerator.Core.LLM;
using StoryGenerator.Generators;

// Setup LLM
var modelProvider = new OllamaModelProvider(
    defaultModel: RecommendedModels.Qwen25_14B_Instruct
);
var contentGenerator = new LLMContentGenerator(modelProvider);
var shotlistGenerator = new LLMShotlistGenerator(contentGenerator);

// Create generator
var beatsGenerator = new SceneBeatsGenerator(shotlistGenerator, scenesPath);

// Generate detailed beat-sheet
var shotsPath = await beatsGenerator.GenerateFromScriptVersionAsync(
    scriptVersion,
    audioDuration: 58.5f,
    temperature: 0.5f
);
```

**Note:** This requires Ollama or another LLM service to be running.

## Testing

A test application is provided in `/CSharp/Tests/SceneBeatsTest/` to verify the generators work correctly.

To run the test:

```bash
cd CSharp/Tests/SceneBeatsTest
dotnet run
```

This will:
1. Generate a draft SRT subtitle file
2. Generate a JSON beat-sheet
3. Display the output and save files to the correct directories

## Integration with Pipeline

To integrate these generators into your pipeline:

1. Add the generators to your pipeline orchestrator
2. Call them after script generation and before video synthesis
3. Use the generated files as input for subsequent pipeline stages

Example:

```csharp
// After script generation
var subtitleGenerator = new SubtitleGenerator();
var beatsGenerator = new SimpleSceneBeatsGenerator();

// Generate subtitles and beats
var srtPath = await subtitleGenerator.GenerateFromScriptVersionAsync(
    scriptVersion, audioDuration);
var shotsPath = await beatsGenerator.GenerateFromScriptVersionAsync(
    scriptVersion, audioDuration);

// Continue with video synthesis using shotsPath...
```

## File Naming Convention

Both generators follow the repository's naming convention:

- **Beat-sheets**: `{title_id}_shots.json`
- **Subtitles**: `{title_id}_draft.srt`

The `_draft` suffix on subtitles indicates they are estimated and should be refined with actual audio timing.

## Dependencies

- .NET 9.0
- System.Text.Json (built-in)
- StoryGenerator.Models namespace

No external dependencies required for basic functionality.
