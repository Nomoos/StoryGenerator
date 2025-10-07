# Title Scoring System - C# Interfaces

## Overview

This document provides a comprehensive review of the C# interfaces designed for the title scoring system. These interfaces define the contracts for scoring video titles, recommending narrator voices, and managing configuration.

## Architecture

The title scoring system is designed with the following key interfaces:

```
┌─────────────────────────────────────────────────────────────┐
│                     ITitleScorer                            │
│  - ScoreTitleAsync()                                        │
│  - ScoreTitlesAsync()                                       │
│  - ScoreSegmentAsync()                                      │
│  - SelectTopTitles()                                        │
└─────────────────────────────────────────────────────────────┘
                            │
                            │ uses
                            ▼
┌──────────────────────┐  ┌───────────────────┐  ┌──────────────────────┐
│  IVoiceRecommender   │  │ ITitleFileReader  │  │ IScoreOutputWriter   │
│  - RecommendVoiceAsync│ │ - FindTitleFiles  │  │ - SaveScoresAsJson   │
│  - GetVoiceByContent │  │ - ExtractTitle    │  │ - SaveVoiceNotesAsMd │
└──────────────────────┘  └───────────────────┘  └──────────────────────┘
                            │
                            │ configured by
                            ▼
                  ┌─────────────────────────────┐
                  │ IScoringConfigurationProvider│
                  │ - LoadConfiguration         │
                  │ - GetScoringCriteria        │
                  │ - GetVoiceGuidelines        │
                  └─────────────────────────────┘
```

## Interface Descriptions

### 1. ITitleScorer

**Purpose:** Core interface for scoring video titles for viral potential.

**Key Methods:**
- `ScoreTitleAsync()` - Score a single title
- `ScoreTitlesAsync()` - Score multiple titles in batch
- `ScoreSegmentAsync()` - Score all titles in a segment directory
- `SelectTopTitles()` - Select top N titles from results

**Design Decisions:**
- ✅ Async/await pattern for scalability
- ✅ CancellationToken support for long-running operations
- ✅ Strongly-typed return values
- ✅ Separation of concerns (scoring vs. I/O)

**Usage Example:**
```csharp
var scorer = serviceProvider.GetRequiredService<ITitleScorer>();
var result = await scorer.ScoreTitleAsync(
    "5 Secrets You Need to Know", 
    "women", 
    "18-23"
);
Console.WriteLine($"Score: {result.OverallScore}/100");
```

### 2. IScoringConfigurationProvider

**Purpose:** Manages loading and access to scoring configuration.

**Key Methods:**
- `LoadConfigurationAsync()` - Load config from YAML file
- `GetScoringCriteria()` - Get criteria with weights
- `GetVoiceGuidelines()` - Get voice recommendation rules
- `GetTopTitleCount()` - Get top N selection count
- `ValidateConfiguration()` - Validate config integrity

**Design Decisions:**
- ✅ Abstraction over configuration source (file, database, cloud)
- ✅ Validation support for configuration integrity
- ✅ Caching-friendly design
- ✅ Read-only access patterns

**Usage Example:**
```csharp
var configProvider = serviceProvider.GetRequiredService<IScoringConfigurationProvider>();
var config = await configProvider.LoadConfigurationAsync();
var criteria = configProvider.GetScoringCriteria();
foreach (var criterion in criteria)
{
    Console.WriteLine($"{criterion.Name}: {criterion.Weight * 100}%");
}
```

### 3. IVoiceRecommender

**Purpose:** Recommends narrator voice gender based on content and audience.

**Key Methods:**
- `RecommendVoiceAsync()` - Get voice recommendation with reasoning
- `GetVoiceByContentType()` - Map content type to voice gender
- `GenerateReasoning()` - Create explanation for recommendation

**Design Decisions:**
- ✅ Content-aware recommendations (mystery → male, beauty → female)
- ✅ Audience-aligned suggestions
- ✅ Explicit reasoning generation
- ✅ Rule-based and ML-ready design

**Usage Example:**
```csharp
var recommender = serviceProvider.GetRequiredService<IVoiceRecommender>();
var recommendation = await recommender.RecommendVoiceAsync(
    "The Mystery of the Ancient Code",
    "women",
    "18-23"
);
Console.WriteLine($"Voice: {recommendation.Gender.ToShortString()}");
Console.WriteLine($"Reasoning: {recommendation.Reasoning}");
```

### 4. IScoreOutputWriter

**Purpose:** Saves scoring results to various output formats.

**Key Methods:**
- `SaveScoresAsJsonAsync()` - Save as JSON for programmatic use
- `SaveVoiceNotesAsMarkdownAsync()` - Save as Markdown for humans
- `GenerateFileName()` - Create timestamped filenames
- `EnsureOutputDirectory()` - Handle directory creation

**Design Decisions:**
- ✅ Dual output format support (JSON + Markdown)
- ✅ Timestamped filenames (YYYYMMDD format)
- ✅ Directory management
- ✅ Path generation abstraction

**Usage Example:**
```csharp
var writer = serviceProvider.GetRequiredService<IScoreOutputWriter>();
var segment = new AudienceSegment("women", "18-23");
var jsonPath = await writer.SaveScoresAsJsonAsync(
    segment,
    scoringResults,
    "/path/to/scores"
);
var mdPath = await writer.SaveVoiceNotesAsMarkdownAsync(
    segment,
    topTitles,
    "/path/to/voices/choice"
);
```

### 5. ITitleFileReader

**Purpose:** Finds and extracts titles from various file formats.

**Key Methods:**
- `FindTitleFilesAsync()` - Locate title files in directories
- `ExtractTitleFromFileAsync()` - Extract title from single file
- `ExtractTitlesAsync()` - Batch extract from multiple files
- `IsTitleFile()` - Validate file as title source

**Design Decisions:**
- ✅ Multi-format support (JSON, text, nested directories)
- ✅ Batch processing capability
- ✅ Fail-safe extraction (returns null on error)
- ✅ File validation before processing

**Usage Example:**
```csharp
var reader = serviceProvider.GetRequiredService<ITitleFileReader>();
var segment = new AudienceSegment("women", "18-23");
var files = await reader.FindTitleFilesAsync(segment, "/path/to/titles");
var titles = await reader.ExtractTitlesAsync(files);
```

## Model Classes

### TitleScoringResult
Represents a scored title with:
- Individual criterion scores (hook, clarity, relevance, length, viral)
- Overall weighted score (0-100)
- Rationale explanation
- Voice recommendation with reasoning
- Source metadata and timestamp

### AudienceSegment
Represents a target audience:
- Gender (men/women)
- Age range (e.g., "18-23")
- Equality and hashing support

### VoiceRecommendation
Represents voice gender recommendation:
- Gender (Male/Female enum)
- Reasoning text
- Conversion utilities (M/F strings)

### ScoringConfiguration
Complete configuration model:
- Scoring criteria with weights
- Voice recommendation guidelines
- Top selection rules
- LLM prompt template

### TitleItem
Represents an extracted title:
- Title text
- Source file path
- Optional metadata (genre, synopsis, themes)

## Design Principles

### 1. Separation of Concerns
Each interface has a single, well-defined responsibility:
- Scoring logic is separate from I/O operations
- Configuration is abstracted from business logic
- Voice recommendations are independent from scoring

### 2. Async/Await First
All I/O operations are async:
- File reading/writing
- Configuration loading
- Batch processing
- Supports cancellation tokens

### 3. Dependency Injection Ready
All interfaces designed for DI:
- Constructor injection of dependencies
- Interface-based contracts
- Easy to mock for testing
- Supports multiple implementations

### 4. Testability
Design supports comprehensive testing:
- Interface-based mocking
- No static dependencies
- Pure functions where possible
- Validation methods

### 5. Extensibility
Future enhancements supported:
- LLM integration (prompt template ready)
- Multiple scoring strategies
- Custom output formats
- Cloud storage backends

## Implementation Notes

### Recommended Implementation Order

1. **Start with Models** ✅ (Complete)
   - TitleScoringResult
   - AudienceSegment
   - VoiceRecommendation
   - ScoringConfiguration

2. **Configuration Provider**
   - Implement YAML loading
   - Add configuration validation
   - Cache configuration data

3. **File Reader**
   - JSON file parsing
   - Text file reading
   - Directory traversal

4. **Voice Recommender**
   - Content type detection
   - Rule-based recommendations
   - Reasoning generation

5. **Title Scorer** (Core)
   - Implement scoring algorithms
   - Calculate weighted scores
   - Generate rationales

6. **Output Writer**
   - JSON serialization
   - Markdown generation
   - File management

### Dependency Injection Setup

```csharp
services.AddScoped<ITitleScorer, TitleScorer>();
services.AddScoped<IVoiceRecommender, VoiceRecommender>();
services.AddScoped<ITitleFileReader, TitleFileReader>();
services.AddScoped<IScoreOutputWriter, ScoreOutputWriter>();
services.AddSingleton<IScoringConfigurationProvider, YamlConfigurationProvider>();
```

### Error Handling

Implementations should:
- Throw meaningful exceptions for invalid input
- Use nullable return types for optional results
- Log errors appropriately
- Provide detailed error messages

### Performance Considerations

- Cache configuration after first load
- Use parallel processing for batch operations
- Stream large file operations
- Consider memory usage with large datasets

## Testing Strategy

### Unit Tests
- Test each interface implementation independently
- Mock dependencies using test doubles
- Verify scoring algorithms with known inputs
- Test edge cases and error conditions

### Integration Tests
- Test file I/O operations with real files
- Verify configuration loading from YAML
- Test end-to-end scoring pipeline
- Validate output formats

### Performance Tests
- Benchmark batch scoring operations
- Measure file I/O performance
- Test with large datasets
- Profile memory usage

## Future Enhancements

### LLM Integration
The design supports future LLM integration:
```csharp
public interface ILlmScorer : ITitleScorer
{
    Task<TitleScoringResult> ScoreTitleWithLlmAsync(
        string title,
        string targetGender,
        string targetAge,
        string promptTemplate,
        CancellationToken cancellationToken = default
    );
}
```

### Caching
Add caching layer for performance:
```csharp
public interface ICachedTitleScorer : ITitleScorer
{
    Task<TitleScoringResult> GetCachedScoreAsync(string title);
    Task ClearCacheAsync();
}
```

### Analytics
Track scoring patterns over time:
```csharp
public interface IScoringAnalytics
{
    Task<ScoringStatistics> GetStatisticsAsync(AudienceSegment segment);
    Task<IEnumerable<TrendData>> GetTrendingPatternsAsync();
}
```

## Questions for Review

1. **Interface Granularity**: Are the interfaces appropriately sized, or should some be split/merged?

2. **Naming Conventions**: Do the interface and method names clearly convey their purpose?

3. **Async Patterns**: Is the async/await usage appropriate for all methods?

4. **Model Design**: Are the model classes sufficiently rich, or do they need additional properties?

5. **Extensibility**: Does the design support future requirements (LLM integration, cloud storage, etc.)?

6. **Error Handling**: Should interfaces define specific exception types, or rely on standard exceptions?

7. **Validation**: Should validation logic be in interfaces, or left to implementations?

8. **Batch Processing**: Are the batch processing methods sufficient, or do we need more fine-grained control?

## Conclusion

These interfaces provide a solid foundation for implementing the title scoring system in C#. The design follows SOLID principles, supports async operations, and is ready for dependency injection and testing.

**Next Steps:**
1. Review interfaces for completeness and clarity
2. Begin implementation starting with models and configuration
3. Write comprehensive unit tests
4. Implement core scoring logic
5. Add integration tests

**Status:** ✅ Ready for Review
