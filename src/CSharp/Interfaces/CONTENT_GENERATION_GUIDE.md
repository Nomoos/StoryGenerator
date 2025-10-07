# Content Generation Interfaces

This document describes the C# interfaces for generating ideas, topics, and titles for specific audience segments.

## Overview

The content generation pipeline consists of three main stages:

1. **Idea Generation** - Generate ≥20 raw story ideas per segment
2. **Topic Clustering** - Cluster ideas into ≥8 topic groups per segment
3. **Title Generation** - Convert topics to ≥10 clickable titles per segment

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                      IIdeaGenerator                             │
│  - GenerateIdeasAsync()                                         │
│  - GenerateAndSaveIdeasAsync()                                  │
│  - GenerateIdeasForAllSegmentsAsync()                           │
└─────────────────────────────────────────────────────────────────┘
                            │
                            ▼ Output: /ideas/{segment}/{age}/YYYYMMDD_ideas.md
                            │
┌─────────────────────────────────────────────────────────────────┐
│                      ITopicGenerator                            │
│  - ClusterIdeasIntoTopicsAsync()                                │
│  - ClusterAndSaveTopicsAsync()                                  │
│  - GenerateTopicsForAllSegmentsAsync()                          │
└─────────────────────────────────────────────────────────────────┘
                            │
                            ▼ Output: /topics/{segment}/{age}/YYYYMMDD_topics.json
                            │
┌─────────────────────────────────────────────────────────────────┐
│                      ITitleGenerator                            │
│  - GenerateTitlesFromTopicsAsync()                              │
│  - GenerateAndSaveTitlesAsync()                                 │
│  - GenerateTitlesForAllSegmentsAsync()                          │
└─────────────────────────────────────────────────────────────────┘
                            │
                            ▼ Output: /titles/{segment}/{age}/YYYYMMDD_titles.json
```

## Audience Segments

The system supports the following predefined segments:

- **Gender**: `women`, `men`
- **Age Ranges**: `10-13`, `14-17`, `18-23`, `24-30` (note: issue mentioned 18-23 but folder structure includes 24-30)

This creates 8 total segments: women/men × 4 age ranges.

## Interfaces

### 1. IIdeaGenerator

**Purpose**: Generate raw story ideas for specific audience segments.

**Key Features**:
- Generates minimum 20 ideas per segment
- Saves ideas as markdown lists
- Supports batch generation for all segments
- Uses LLM models (GPT-4o-mini, Qwen2.5-14B-Instruct, etc.)

**Output Format**:
```
/ideas/{gender}/{age}/YYYYMMDD_ideas.md

Example content:
- A teenager discovers a hidden talent that changes their life
- Two best friends face a difficult decision that tests their loyalty
- A mysterious stranger arrives in town with a life-changing secret
...
```

**Key Methods**:
- `GenerateIdeasAsync()` - Generate ideas for a single segment
- `GenerateAndSaveIdeasAsync()` - Generate and save to markdown file
- `GenerateIdeasForAllSegmentsAsync()` - Batch process all segments
- `FormatIdeasAsMarkdown()` - Format ideas as markdown list
- `GetPredefinedSegments()` - Get all standard segments

**Usage Example**:
```csharp
var ideaGenerator = serviceProvider.GetRequiredService<IIdeaGenerator>();
var segment = new AudienceSegment("women", "18-23");

// Generate ideas
var ideas = await ideaGenerator.GenerateIdeasAsync(segment, minIdeas: 20);

// Generate and save
var filePath = await ideaGenerator.GenerateAndSaveIdeasAsync(
    segment, 
    "/ideas", 
    minIdeas: 20
);
Console.WriteLine($"Ideas saved to: {filePath}");

// Batch process all segments
var results = await ideaGenerator.GenerateIdeasForAllSegmentsAsync("/ideas");
```

### 2. ITopicGenerator

**Purpose**: Cluster raw ideas into meaningful topic groups.

**Key Features**:
- Clusters ideas into minimum 8 topics per segment
- Saves topics as JSON with metadata
- Supports loading ideas from markdown files
- Uses clustering algorithms or LLM-based topic extraction

**Output Format**:
```json
{
  "segment": {
    "gender": "women",
    "age": "18-23"
  },
  "topics": [
    {
      "id": "guid",
      "topicName": "Friendship & Loyalty",
      "description": "Stories about testing friendships and making difficult choices",
      "ideaIds": ["id1", "id2", "id3"],
      "keywords": ["friendship", "loyalty", "trust", "betrayal"],
      "viralPotential": 8
    },
    ...
  ],
  "generatedAt": "2025-01-15T10:30:00Z",
  "topicCount": 8
}
```

**Key Methods**:
- `ClusterIdeasIntoTopicsAsync()` - Cluster a list of ideas
- `ClusterAndSaveTopicsAsync()` - Cluster and save to JSON
- `LoadIdeasAndGenerateTopicsAsync()` - Load markdown file and generate topics
- `GenerateTopicsForAllSegmentsAsync()` - Batch process all segments
- `ParseIdeasFromMarkdownAsync()` - Parse ideas from markdown file

**Usage Example**:
```csharp
var topicGenerator = serviceProvider.GetRequiredService<ITopicGenerator>();
var segment = new AudienceSegment("women", "18-23");

// Load ideas from markdown and generate topics
var topicsPath = await topicGenerator.LoadIdeasAndGenerateTopicsAsync(
    "/ideas/women/18-23/20250115_ideas.md",
    segment,
    "/topics",
    minTopics: 8
);

// Or cluster existing ideas
var topics = await topicGenerator.ClusterIdeasIntoTopicsAsync(
    ideas, 
    segment, 
    minTopics: 8
);

// Batch process all segments
var results = await topicGenerator.GenerateTopicsForAllSegmentsAsync(
    "/ideas",
    "/topics",
    minTopics: 8
);
```

### 3. ITitleGenerator

**Purpose**: Generate clickable, viral-optimized titles from topic clusters.

**Key Features**:
- Generates minimum 10 titles per segment
- Optimizes titles for clickability and viral potential
- Saves titles as JSON with metadata
- Supports loading topics from JSON files
- Includes title validation and optimization

**Output Format**:
```json
{
  "segment": {
    "gender": "women",
    "age": "18-23"
  },
  "titles": [
    {
      "id": "guid",
      "title": "The Secret My Best Friend Kept From Me Changed Everything",
      "topicClusterId": "friendship-topic-id",
      "viralPotential": 9,
      "clickabilityScore": 8,
      "keywords": ["secret", "best friend", "betrayal"],
      "emotionalHook": "curiosity",
      "titleFormat": "revelation"
    },
    ...
  ],
  "generatedAt": "2025-01-15T11:00:00Z",
  "titleCount": 10
}
```

**Key Methods**:
- `GenerateTitlesFromTopicsAsync()` - Generate titles from topics
- `GenerateTitlesFromTopicAsync()` - Generate titles from single topic
- `GenerateAndSaveTitlesAsync()` - Generate and save to JSON
- `LoadTopicsAndGenerateTitlesAsync()` - Load JSON file and generate titles
- `GenerateTitlesForAllSegmentsAsync()` - Batch process all segments
- `OptimizeTitleAsync()` - Optimize a single title
- `ValidateTitleClickability()` - Validate title quality

**Usage Example**:
```csharp
var titleGenerator = serviceProvider.GetRequiredService<ITitleGenerator>();
var segment = new AudienceSegment("women", "18-23");

// Load topics from JSON and generate titles
var titlesPath = await titleGenerator.LoadTopicsAndGenerateTitlesAsync(
    "/topics/women/18-23/20250115_topics.json",
    segment,
    "/titles",
    minTitles: 10
);

// Or generate from existing topics
var titles = await titleGenerator.GenerateTitlesFromTopicsAsync(
    topics,
    segment,
    minTitles: 10
);

// Optimize a single title
var optimized = await titleGenerator.OptimizeTitleAsync(
    "My Friend Did Something",
    segment
);

// Validate title
bool isValid = titleGenerator.ValidateTitleClickability(optimized.Title);

// Batch process all segments
var results = await titleGenerator.GenerateTitlesForAllSegmentsAsync(
    "/topics",
    "/titles",
    minTitles: 10
);
```

## Model Classes

### RawIdea

Represents a raw story idea generated for a segment.

**Properties**:
- `Id` - Unique identifier
- `Content` - The idea text/description
- `Segment` - Target audience segment
- `GeneratedAt` - Generation timestamp
- `Tags` - Optional keywords/tags
- `ViralPotential` - Estimated viral score (0-10)

### TopicCluster

Represents a cluster of related ideas grouped by topic.

**Properties**:
- `Id` - Unique identifier
- `TopicName` - Name/title of the topic
- `Description` - Topic description
- `IdeaIds` - List of idea IDs in this cluster
- `Keywords` - Related keywords/themes
- `Segment` - Target audience segment
- `CreatedAt` - Creation timestamp
- `ViralPotential` - Estimated viral score (0-10)
- `IdeaCount` - Number of ideas in cluster

### TopicClusterCollection

Collection of topic clusters for a segment.

**Properties**:
- `Segment` - Target audience segment
- `Topics` - List of topic clusters
- `GeneratedAt` - Generation timestamp
- `Metadata` - Additional metadata
- `TopicCount` - Number of topics

### ClickableTitle

Represents a viral-optimized title derived from a topic.

**Properties**:
- `Id` - Unique identifier
- `Title` - The title text
- `TopicClusterId` - Source topic cluster ID
- `Segment` - Target audience segment
- `GeneratedAt` - Generation timestamp
- `ViralPotential` - Viral score (0-10)
- `ClickabilityScore` - Clickability score (0-10)
- `Keywords` - SEO keywords
- `EmotionalHook` - Emotional appeal type
- `TitleFormat` - Title pattern/format
- `Metadata` - Additional metadata

### ClickableTitleCollection

Collection of clickable titles for a segment.

**Properties**:
- `Segment` - Target audience segment
- `Titles` - List of clickable titles
- `GeneratedAt` - Generation timestamp
- `Metadata` - Additional metadata
- `TitleCount` - Number of titles

## Design Principles

### 1. Separation of Concerns
Each interface has a single, well-defined responsibility:
- IIdeaGenerator: Raw idea generation
- ITopicGenerator: Idea clustering and topic extraction
- ITitleGenerator: Title generation and optimization

### 2. Async/Await Pattern
All I/O and LLM operations are async:
- File reading/writing operations
- LLM API calls for content generation
- Batch processing operations
- Supports cancellation tokens for long-running operations

### 3. Batch Processing Support
All generators support batch operations:
- Process all segments at once
- Efficient pipeline execution
- Progress tracking and error handling

### 4. File Path Conventions
Consistent file naming and directory structure:
- Date-based filenames (YYYYMMDD format)
- Organized by segment (gender/age)
- Clear separation of ideas, topics, and titles

### 5. Extensibility
Design supports future enhancements:
- Multiple LLM providers
- Custom clustering algorithms
- Alternative output formats
- Analytics and tracking

### 6. Dependency Injection Ready
All interfaces designed for DI:
- Constructor injection of dependencies
- Interface-based contracts
- Easy to mock for testing
- Supports multiple implementations

## Implementation Notes

### Recommended Implementation Order

1. **Model Classes** ✅ (Complete)
   - RawIdea
   - TopicCluster & TopicClusterCollection
   - ClickableTitle & ClickableTitleCollection

2. **IIdeaGenerator Implementation**
   - LLM integration for idea generation
   - Markdown file I/O
   - Batch processing logic

3. **ITopicGenerator Implementation**
   - Clustering algorithm (k-means, LLM-based, etc.)
   - Markdown parsing
   - JSON serialization

4. **ITitleGenerator Implementation**
   - Title generation from topics
   - Title optimization logic
   - Validation rules

### Dependency Injection Setup

```csharp
services.AddScoped<IIdeaGenerator, IdeaGenerator>();
services.AddScoped<ITopicGenerator, TopicGenerator>();
services.AddScoped<ITitleGenerator, TitleGenerator>();

// Optional: Add configuration
services.Configure<ContentGenerationOptions>(configuration.GetSection("ContentGeneration"));
```

### Configuration Example

```yaml
# config/content_generation.yaml
content_generation:
  segments:
    - { gender: "women", age: "10-13" }
    - { gender: "women", age: "14-17" }
    - { gender: "women", age: "18-23" }
    - { gender: "women", age: "24-30" }
    - { gender: "men", age: "10-13" }
    - { gender: "men", age: "14-17" }
    - { gender: "men", age: "18-23" }
    - { gender: "men", age: "24-30" }
  
  idea_generation:
    min_ideas: 20
    llm_model: "gpt-4o-mini"
    temperature: 0.8
  
  topic_clustering:
    min_topics: 8
    clustering_method: "llm"  # or "kmeans", "hierarchical"
  
  title_generation:
    min_titles: 10
    titles_per_topic: 2
    optimization_enabled: true
```

### Error Handling

Implementations should:
- Throw meaningful exceptions for invalid input
- Log errors appropriately with context
- Provide detailed error messages
- Support retry logic for LLM calls
- Handle file I/O errors gracefully

### Performance Considerations

- Cache LLM responses when appropriate
- Use parallel processing for batch operations
- Stream large file operations
- Monitor LLM API rate limits
- Consider memory usage with large datasets

## Pipeline Integration

### Full Pipeline Example

```csharp
// Step 1: Generate ideas for all segments
var ideaGenerator = services.GetRequiredService<IIdeaGenerator>();
var ideaPaths = await ideaGenerator.GenerateIdeasForAllSegmentsAsync(
    "/ideas", 
    minIdeas: 20
);

// Step 2: Generate topics from ideas
var topicGenerator = services.GetRequiredService<ITopicGenerator>();
var topicPaths = await topicGenerator.GenerateTopicsForAllSegmentsAsync(
    "/ideas",
    "/topics",
    minTopics: 8
);

// Step 3: Generate titles from topics
var titleGenerator = services.GetRequiredService<ITitleGenerator>();
var titlePaths = await titleGenerator.GenerateTitlesForAllSegmentsAsync(
    "/topics",
    "/titles",
    minTitles: 10
);

// Results
foreach (var segment in ideaGenerator.GetPredefinedSegments())
{
    Console.WriteLine($"Segment: {segment}");
    Console.WriteLine($"  Ideas: {ideaPaths[segment]}");
    Console.WriteLine($"  Topics: {topicPaths[segment]}");
    Console.WriteLine($"  Titles: {titlePaths[segment]}");
}
```

### Integration with Existing Pipeline

These generators can integrate with the existing pipeline:
- Use IStoryIdea as input for script generation
- Feed titles to ITitleScorer for scoring
- Connect with IScriptGenerator for story creation
- Support the existing AudienceSegment model

## Testing Strategy

### Unit Tests
- Test each interface implementation independently
- Mock LLM dependencies
- Verify file I/O operations
- Test edge cases and error conditions
- Validate output formats

### Integration Tests
- Test full pipeline flow
- Verify file generation and structure
- Test batch processing
- Validate JSON/Markdown formats
- Test with real LLM calls (optional)

### Performance Tests
- Benchmark batch operations
- Test with large datasets
- Measure LLM API latency
- Profile memory usage

## Future Enhancements

### Analytics & Tracking
- Track generation metrics
- Monitor viral performance
- A/B testing support
- Trend analysis

### Multi-language Support
- Generate content in multiple languages
- Language-specific optimizations
- Cultural adaptation

### Advanced Clustering
- Semantic clustering with embeddings
- Hierarchical topic structures
- Dynamic topic count optimization

### Title Optimization
- A/B testing of title variations
- Real-time performance feedback
- Machine learning-based optimization
- Sentiment analysis integration

## Status

✅ **Interfaces Designed and Documented**
- IIdeaGenerator
- ITopicGenerator  
- ITitleGenerator

✅ **Models Created**
- RawIdea
- TopicCluster & TopicClusterCollection
- ClickableTitle & ClickableTitleCollection

⏳ **Next Steps**
- Implement concrete classes for each interface
- Add LLM integration
- Create unit tests
- Add configuration support
- Build CLI tools for testing
