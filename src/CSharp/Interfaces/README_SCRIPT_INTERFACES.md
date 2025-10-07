# Script Generation, Scoring, and Iteration - C# Interfaces

## Overview

This document describes the C# interfaces designed for the script generation, scoring, and iteration workflow. These interfaces support the complete pipeline from raw script generation using local LLMs through iterative improvements based on scoring feedback.

## Workflow

```
┌────────────────────────────────────────────────────────────────┐
│                 Title Selection & Metadata                      │
│                   (ITitleScorer)                                │
└────────────────────────┬───────────────────────────────────────┘
                         │
                         ▼
┌────────────────────────────────────────────────────────────────┐
│              1. Generate Raw Scripts (v0)                       │
│         Using Local LLM (ILocalScriptGenerator)                │
│    Save: /scripts/raw_local/{segment}/{age}/{title_id}.md     │
└────────────────────────┬───────────────────────────────────────┘
                         │
                         ▼
┌────────────────────────────────────────────────────────────────┐
│              2. Score Raw Scripts (v0)                          │
│     Rubric + Narrative Cohesion (IScriptScorer)               │
│  Save: /scores/{segment}/{age}/{title_id}_script_v0_score.json│
└────────────────────────┬───────────────────────────────────────┘
                         │
                         ▼
┌────────────────────────────────────────────────────────────────┐
│           3. Apply Feedback & Iterate (v1)                      │
│         Improve Script (IScriptIterator)                       │
│  Save: /scripts/iter_local/{segment}/{age}/{title_id}_v1.md   │
└────────────────────────┬───────────────────────────────────────┘
                         │
                         ▼
┌────────────────────────────────────────────────────────────────┐
│              4. Score Iterated Script (v1)                      │
│            Compare Improvements (IScriptScorer)                │
│  Save: /scores/{segment}/{age}/{title_id}_script_v1_score.json│
└────────────────────────────────────────────────────────────────┘
```

## Interface Architecture

### 1. ILocalScriptGenerator

**Purpose:** Generate raw scripts using local LLM models (Qwen2.5-14B-Instruct, Llama-3.1-8B-Instruct).

**Key Methods:**
- `GenerateRawScriptAsync()` - Generate initial v0 script for a title
- `GenerateRawScriptsAsync()` - Batch generate scripts for multiple titles
- `GenerateAndSaveRawScriptAsync()` - Generate and save to proper directory structure
- `IsModelAvailableAsync()` - Check if local model is ready
- `GetModelConfiguration()` - Get model parameters

**Design Decisions:**
- ✅ Extends IGenerator for consistency with existing pipeline
- ✅ Returns ScriptVersion objects with full metadata
- ✅ Supports batch processing for efficiency
- ✅ Integrates with IStoryIdea for context
- ✅ Provides model availability checking

**Usage Example:**
```csharp
var generator = serviceProvider.GetRequiredService<ILocalScriptGenerator>();
var segment = new AudienceSegment("women", "18-23");
var script = await generator.GenerateRawScriptAsync(
    titleId: "001",
    title: "The Secret Nobody Talks About",
    targetAudience: segment
);
// script.Version is "v0"
// script.Content contains the generated script
```

### 2. IScriptScorer

**Purpose:** Score scripts using rubric criteria and narrative cohesion analysis.

**Key Methods:**
- `ScoreScriptAsync()` - Score a script from file path
- `ScoreScriptContentAsync()` - Score script content directly
- `ScoreScriptsInDirectoryAsync()` - Batch score all scripts in a directory
- `ValidateScoringConfiguration()` - Verify scoring setup

**Scoring Criteria:**
- **Hook Quality** (0-100) - Opening engagement
- **Character Development** (0-100) - Character depth
- **Plot Structure** (0-100) - Story pacing and progression
- **Dialogue Quality** (0-100) - Natural conversation
- **Emotional Impact** (0-100) - Emotional resonance
- **Audience Alignment** (0-100) - Demographic fit
- **Clarity** (0-100) - Readability
- **Voice Suitability** (0-100) - TTS compatibility
- **Narrative Cohesion** (0-100) - Story flow and coherence

**Design Decisions:**
- ✅ Rubric-based scoring for objectivity
- ✅ Narrative cohesion as separate dimension
- ✅ Detailed feedback with areas for improvement
- ✅ Batch processing support
- ✅ Configuration validation

**Usage Example:**
```csharp
var scorer = serviceProvider.GetRequiredService<IScriptScorer>();
var segment = new AudienceSegment("women", "18-23");
var result = await scorer.ScoreScriptAsync(
    scriptPath: "/scripts/raw_local/women/18-23/001.md",
    titleId: "001",
    version: "v0",
    targetAudience: segment
);
// result.OverallScore is weighted average
// result.Feedback contains detailed analysis
// result.AreasForImprovement lists specific issues
```

### 3. IScriptIterator

**Purpose:** Improve scripts based on scoring feedback through iterative refinement.

**Key Methods:**
- `IterateScriptAsync()` - Improve script using scoring result
- `IterateScriptWithFeedbackAsync()` - Improve using custom feedback
- `IterateScriptsAsync()` - Batch iterate multiple scripts
- `ApplyImprovementsAsync()` - Apply specific targeted improvements

**Design Decisions:**
- ✅ Uses scoring feedback automatically
- ✅ Supports custom feedback for manual control
- ✅ Preserves version history (v0 → v1 → v2)
- ✅ Batch processing for efficiency
- ✅ Granular improvement application

**Usage Example:**
```csharp
var iterator = serviceProvider.GetRequiredService<IScriptIterator>();
var improvedScript = await iterator.IterateScriptAsync(
    originalScriptPath: "/scripts/raw_local/women/18-23/001.md",
    scoringResult: scoreV0,
    targetVersion: "v1"
);
// improvedScript.Version is "v1"
// improvedScript.PreviousVersion is "v0"
// improvedScript.AppliedFeedback contains the feedback used
```

### 4. IScriptFileManager

**Purpose:** Manage script and score file I/O operations with proper directory structure.

**Key Methods:**
- `SaveRawScriptAsync()` - Save to /scripts/raw_local/
- `SaveIteratedScriptAsync()` - Save to /scripts/iter_local/
- `LoadScriptAsync()` - Load script content
- `SaveScriptScoreAsync()` - Save score JSON to /scores/
- `LoadScriptScoreAsync()` - Load score from JSON
- `FindScriptFilesAsync()` - Find scripts in directory
- `EnsureScriptDirectory()` - Create directory structure
- `GenerateScriptFileName()` - Create proper file names

**Directory Structure:**
```
/scripts/
  raw_local/          # Raw scripts from local LLM (v0)
    {segment}/
      {age}/
        {title_id}.md
  iter_local/         # Iterated/improved scripts (v1+)
    {segment}/
      {age}/
        {title_id}_v1.md
        {title_id}_v2.md

/scores/
  {segment}/
    {age}/
      {title_id}_script_v0_score.json
      {title_id}_script_v1_score.json
```

**Design Decisions:**
- ✅ Consistent directory structure
- ✅ Clear version tracking in file names
- ✅ Automatic directory creation
- ✅ Separation of raw vs. iterated scripts
- ✅ JSON for scores, Markdown for scripts

**Usage Example:**
```csharp
var fileManager = serviceProvider.GetRequiredService<IScriptFileManager>();
var segment = new AudienceSegment("women", "18-23");

// Save raw script
var scriptPath = await fileManager.SaveRawScriptAsync(
    scriptVersion,
    baseScriptsPath: "/scripts"
);
// Returns: /scripts/raw_local/women/18-23/001.md

// Save score
var scorePath = await fileManager.SaveScriptScoreAsync(
    scoringResult,
    baseScoresPath: "/scores"
);
// Returns: /scores/women/18-23/001_script_v0_score.json
```

## Model Classes

### ScriptScoringResult

Represents comprehensive scoring output:
- **RubricScores** - Individual criterion scores (8 criteria)
- **NarrativeCohesion** - Story flow score
- **OverallScore** - Weighted average (0-100)
- **Feedback** - Detailed textual feedback
- **AreasForImprovement** - List of specific issues
- **Strengths** - List of positive aspects
- **Metadata** - Additional scoring information

### ScriptVersion

Tracks script versions and metadata:
- **Version** - Version identifier (v0, v1, v2, etc.)
- **TitleId** - Unique title identifier
- **Content** - The script text
- **FilePath** - Location on disk
- **TargetAudience** - Demographic information
- **PreviousVersion** - Version history tracking
- **Score** - Optional score if evaluated
- **AppliedFeedback** - Feedback used for this iteration
- **GenerationSource** - Origin (local_llm, iteration, etc.)

## Complete Workflow Example

```csharp
// 1. Generate raw scripts for chosen titles
var generator = serviceProvider.GetRequiredService<ILocalScriptGenerator>();
var scorer = serviceProvider.GetRequiredService<IScriptScorer>();
var iterator = serviceProvider.GetRequiredService<IScriptIterator>();
var fileManager = serviceProvider.GetRequiredService<IScriptFileManager>();

var segment = new AudienceSegment("women", "18-23");
var chosenTitles = new[] { "001", "002", "003" };

foreach (var titleId in chosenTitles)
{
    // Step 1: Generate raw script (v0)
    var scriptV0 = await generator.GenerateRawScriptAsync(
        titleId, titleText, segment);
    var scriptPath = await fileManager.SaveRawScriptAsync(
        scriptV0, "/scripts");
    
    // Step 2: Score v0
    var scoreV0 = await scorer.ScoreScriptAsync(
        scriptPath, titleId, "v0", segment);
    await fileManager.SaveScriptScoreAsync(
        scoreV0, "/scores");
    
    // Step 3: Iterate to v1
    var scriptV1 = await iterator.IterateScriptAsync(
        scriptPath, scoreV0, "v1");
    var iterPath = await fileManager.SaveIteratedScriptAsync(
        scriptV1, "/scripts");
    
    // Step 4: Score v1
    var scoreV1 = await scorer.ScoreScriptAsync(
        iterPath, titleId, "v1", segment);
    await fileManager.SaveScriptScoreAsync(
        scoreV1, "/scores");
    
    // Compare scores
    Console.WriteLine($"Title {titleId}:");
    Console.WriteLine($"  v0 Score: {scoreV0.OverallScore:F1}");
    Console.WriteLine($"  v1 Score: {scoreV1.OverallScore:F1}");
    Console.WriteLine($"  Improvement: {scoreV1.OverallScore - scoreV0.OverallScore:+F1}");
}
```

## Integration with Existing Pipeline

### Relationship to Existing Interfaces

```
ITitleScorer ──→ Select top titles
                      │
                      ▼
              ILocalScriptGenerator ──→ Generate scripts
                      │
                      ▼
              IScriptScorer ──→ Evaluate quality
                      │
                      ▼
              IScriptIterator ──→ Improve scripts
                      │
                      ▼
              IScriptGenerator ──→ Final refinement
                      │
                      ▼
              IVoiceGenerator ──→ Text-to-speech
```

### Shared Dependencies

- **AudienceSegment** - Used by title scoring and script generation
- **IStoryIdea** - Provides context for script generation
- **IGenerator** - Base interface for all generators
- **IScoringConfigurationProvider** - Shared configuration system

## Implementation Notes

### Recommended Implementation Order

1. **Models First** ✅ (Complete)
   - ScriptScoringResult
   - ScriptVersion

2. **File Manager** (Foundation)
   - Implement IScriptFileManager
   - Handle directory structure
   - File naming conventions

3. **Local Script Generator** (Content Creation)
   - Implement ILocalScriptGenerator
   - Integrate with local LLM (Ollama, etc.)
   - Generate from titles and story ideas

4. **Script Scorer** (Evaluation)
   - Implement IScriptScorer
   - Define rubric weights
   - Narrative cohesion analysis
   - May use LLM or rule-based

5. **Script Iterator** (Improvement)
   - Implement IScriptIterator
   - Apply feedback intelligently
   - Version management

### Configuration Requirements

**scoring_config.yaml** (extend existing):
```yaml
script_scoring:
  rubric:
    hook_quality: 0.15
    character_development: 0.12
    plot_structure: 0.15
    dialogue_quality: 0.10
    emotional_impact: 0.12
    audience_alignment: 0.10
    clarity: 0.08
    voice_suitability: 0.08
  narrative_cohesion: 0.10  # Total: 1.00
  
  thresholds:
    minimum_score: 60.0
    iteration_threshold: 70.0  # Iterate if below
    excellent_threshold: 85.0
```

**llm_config.yaml**:
```yaml
local_llm:
  model: "qwen2.5:14b-instruct"
  endpoint: "http://localhost:11434"  # Ollama
  parameters:
    temperature: 0.7
    top_p: 0.9
    max_tokens: 1500
    presence_penalty: 0.6
```

### Dependency Injection Setup

```csharp
// Register script-related services
services.AddScoped<ILocalScriptGenerator, LocalScriptGenerator>();
services.AddScoped<IScriptScorer, ScriptScorer>();
services.AddScoped<IScriptIterator, ScriptIterator>();
services.AddScoped<IScriptFileManager, ScriptFileManager>();

// Optional: Use existing IScriptGenerator as fallback
services.AddScoped<IScriptGenerator, GptScriptGenerator>();
```

### Error Handling

Implementations should:
- Throw `ArgumentException` for invalid parameters
- Throw `FileNotFoundException` for missing scripts
- Throw `InvalidOperationException` for model unavailability
- Use nullable return types for optional results
- Log errors with structured logging
- Provide detailed error messages

### Performance Considerations

- **Batch Processing**: Use `*Async` methods for multiple scripts
- **Caching**: Cache scoring configuration and model instances
- **Parallelization**: Score multiple scripts concurrently
- **Streaming**: Stream large script files
- **Model Management**: Keep local LLM loaded between generations

## Testing Strategy

### Unit Tests

```csharp
[Test]
public async Task ScriptScorer_ValidScript_ReturnsScore()
{
    // Arrange
    var scorer = CreateScriptScorer();
    var segment = new AudienceSegment("women", "18-23");
    
    // Act
    var result = await scorer.ScoreScriptContentAsync(
        sampleScript, "001", "v0", segment);
    
    // Assert
    Assert.That(result.OverallScore, Is.InRange(0, 100));
    Assert.That(result.Feedback, Is.Not.Empty);
}
```

### Integration Tests

```csharp
[Test]
public async Task CompleteWorkflow_GenerateScoreIterate_Success()
{
    // Test full pipeline: generate → score → iterate → score
    var generator = CreateGenerator();
    var scorer = CreateScorer();
    var iterator = CreateIterator();
    
    var scriptV0 = await generator.GenerateRawScriptAsync(...);
    var scoreV0 = await scorer.ScoreScriptContentAsync(...);
    var scriptV1 = await iterator.IterateScriptAsync(...);
    var scoreV1 = await scorer.ScoreScriptContentAsync(...);
    
    Assert.That(scoreV1.OverallScore, Is.GreaterThanOrEqualTo(scoreV0.OverallScore));
}
```

## Future Enhancements

### Multi-Version Tracking
```csharp
public interface IScriptVersionTracker
{
    Task<IEnumerable<ScriptVersion>> GetVersionHistoryAsync(string titleId);
    Task<ScriptVersion> GetBestVersionAsync(string titleId);
    Task<VersionComparison> CompareVersionsAsync(string v1, string v2);
}
```

### A/B Testing
```csharp
public interface IScriptABTester
{
    Task<ABTestResult> CompareScriptsAsync(ScriptVersion a, ScriptVersion b);
    Task<ScriptVersion> SelectWinnerAsync(IEnumerable<ScriptVersion> variants);
}
```

### Analytics
```csharp
public interface IScriptAnalytics
{
    Task<ScriptStatistics> GetScriptStatsAsync(AudienceSegment segment);
    Task<IEnumerable<Pattern>> IdentifySuccessPatternsAsync();
}
```

## Conclusion

These interfaces provide a comprehensive foundation for the script generation, scoring, and iteration workflow. The design:

- ✅ Follows SOLID principles
- ✅ Integrates with existing pipeline
- ✅ Supports local LLM generation
- ✅ Provides detailed scoring and feedback
- ✅ Enables iterative improvement
- ✅ Maintains proper file organization
- ✅ Ready for dependency injection and testing

**Status:** ✅ Ready for Implementation
