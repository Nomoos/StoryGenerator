# Content Generation Pipeline - Quick Reference

## Overview

This document provides a quick reference for the content generation interfaces that generate ideas, topics, and titles per audience segment.

## Pipeline Flow

```
Step 1: Idea Generation
├── Input: Audience Segment (gender + age)
├── Process: IIdeaGenerator
└── Output: /ideas/{gender}/{age}/YYYYMMDD_ideas.md (≥20 ideas)

Step 2: Topic Clustering
├── Input: Ideas from markdown file
├── Process: ITopicGenerator
└── Output: /topics/{gender}/{age}/YYYYMMDD_topics.json (≥8 topics)

Step 3: Title Generation
├── Input: Topics from JSON file
├── Process: ITitleGenerator
└── Output: /titles/{gender}/{age}/YYYYMMDD_titles.json (≥10 titles)
```

## Audience Segments

| Gender | Age Ranges |
|--------|------------|
| women  | 10-13, 14-17, 18-23, 24-30 |
| men    | 10-13, 14-17, 18-23, 24-30 |

**Total: 8 segments**

## Quick Start Example

```csharp
// 1. Generate ideas
var ideaGenerator = services.GetRequiredService<IIdeaGenerator>();
var segment = new AudienceSegment("women", "18-23");
var ideasPath = await ideaGenerator.GenerateAndSaveIdeasAsync(
    segment, 
    "/ideas", 
    minIdeas: 20
);
// Output: /ideas/women/18-23/20250115_ideas.md

// 2. Generate topics from ideas
var topicGenerator = services.GetRequiredService<ITopicGenerator>();
var topicsPath = await topicGenerator.LoadIdeasAndGenerateTopicsAsync(
    ideasPath,
    segment,
    "/topics",
    minTopics: 8
);
// Output: /topics/women/18-23/20250115_topics.json

// 3. Generate titles from topics
var titleGenerator = services.GetRequiredService<ITitleGenerator>();
var titlesPath = await titleGenerator.LoadTopicsAndGenerateTitlesAsync(
    topicsPath,
    segment,
    "/titles",
    minTitles: 10
);
// Output: /titles/women/18-23/20250115_titles.json
```

## Batch Processing

```csharp
// Process all segments at once
var ideaPaths = await ideaGenerator.GenerateIdeasForAllSegmentsAsync("/ideas");
var topicPaths = await topicGenerator.GenerateTopicsForAllSegmentsAsync("/ideas", "/topics");
var titlePaths = await titleGenerator.GenerateTitlesForAllSegmentsAsync("/topics", "/titles");
```

## File Formats

### Ideas File (Markdown)
```markdown
- A teenager discovers a hidden talent that changes their life
- Two best friends face a difficult decision that tests their loyalty
- A mysterious stranger arrives in town with a life-changing secret
...
```

### Topics File (JSON)
```json
{
  "segment": {"gender": "women", "age": "18-23"},
  "topics": [
    {
      "id": "guid",
      "topicName": "Friendship & Loyalty",
      "description": "Stories about testing friendships",
      "ideaIds": ["id1", "id2"],
      "keywords": ["friendship", "loyalty"],
      "viralPotential": 8
    }
  ],
  "topicCount": 8
}
```

### Titles File (JSON)
```json
{
  "segment": {"gender": "women", "age": "18-23"},
  "titles": [
    {
      "id": "guid",
      "title": "The Secret My Best Friend Kept Changed Everything",
      "topicClusterId": "topic-id",
      "viralPotential": 9,
      "clickabilityScore": 8,
      "emotionalHook": "curiosity"
    }
  ],
  "titleCount": 10
}
```

## Integration with Existing Pipeline

These interfaces integrate seamlessly with the existing StoryGenerator pipeline:

1. **Use generated titles** → Feed to `ITitleScorer` for scoring
2. **Pick top titles** → Create `IStoryIdea` instances
3. **Generate scripts** → Use `IScriptGenerator`
4. **Create videos** → Continue with existing pipeline

## Interfaces Reference

| Interface | Purpose | Min Output |
|-----------|---------|------------|
| `IIdeaGenerator` | Generate raw ideas | ≥20 ideas/segment |
| `ITopicGenerator` | Cluster ideas into topics | ≥8 topics/segment |
| `ITitleGenerator` | Generate clickable titles | ≥10 titles/segment |

## Models Reference

| Model | Description |
|-------|-------------|
| `RawIdea` | A raw story idea with metadata |
| `TopicCluster` | A cluster of related ideas |
| `TopicClusterCollection` | Collection of topics for a segment |
| `ClickableTitle` | A viral-optimized title |
| `ClickableTitleCollection` | Collection of titles for a segment |
| `AudienceSegment` | Gender + age range identifier |

## Documentation

For detailed documentation, see:
- [CONTENT_GENERATION_GUIDE.md](./CONTENT_GENERATION_GUIDE.md) - Comprehensive guide with examples
- [IGenerators.cs](./IGenerators.cs) - Existing generator interfaces
- [IStoryIdea.cs](./IStoryIdea.cs) - Story idea model

## Implementation Status

✅ **Completed**:
- Interface definitions (IIdeaGenerator, ITopicGenerator, ITitleGenerator)
- Model classes (RawIdea, TopicCluster, ClickableTitle)
- Comprehensive documentation
- Build verification

⏳ **Future Work**:
- Concrete implementations of interfaces
- LLM integration for content generation
- Unit tests
- CLI tools for testing

## Design Principles

1. **Async/Await** - All I/O operations are async
2. **Batch Processing** - Process all segments efficiently
3. **File Conventions** - Consistent naming (YYYYMMDD format)
4. **Dependency Injection** - Ready for DI frameworks
5. **Extensibility** - Support for multiple LLM providers
6. **Documentation** - Comprehensive XML comments

## Configuration Example

```yaml
content_generation:
  idea_generation:
    min_ideas: 20
    llm_model: "gpt-4o-mini"
    temperature: 0.8
  
  topic_clustering:
    min_topics: 8
    clustering_method: "llm"
  
  title_generation:
    min_titles: 10
    titles_per_topic: 2
```

## Requirements

- .NET 8.0+
- LLM API access (GPT-4o-mini, Qwen2.5-14B-Instruct, or similar)
- File system access for reading/writing

## Next Steps

To implement these interfaces:

1. Create concrete classes implementing each interface
2. Add LLM client integration
3. Implement clustering algorithms
4. Add configuration support
5. Create unit tests
6. Build CLI tools for testing

For questions or contributions, see the main [README.md](../../README.md).
