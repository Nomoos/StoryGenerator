# Idea Collector System

## Overview

The Idea Collector system provides a framework for gathering story ideas from multiple sources (Reddit, Instagram, TikTok, etc.), transforming them into original content, and scoring them based on viral potential across different demographics.

## ⚠️ Critical Guidelines

**IMPORTANT**: All source material collected by idea collectors is used **ONLY as inspiration**. 

- ❌ **NEVER** use original content, images, or text directly in final products
- ❌ **NEVER** use content with questionable authorship
- ✅ **ALWAYS** transform sources into original ideas
- ✅ **ALWAYS** ensure copyright compliance

This is critical for avoiding copyright issues and maintaining ethical content creation practices.

## Architecture

### Key Components

1. **IdeaSource** - Represents source material (title, text, images) collected for inspiration
2. **CollectedIdea** - A transformed, original idea with viral potential scoring
3. **IIdeaCollector** - Interface for implementing collectors for different sources
4. **IdeaCollectorRegistry** - Centralized registry for all collected ideas
5. **ViralPotential** - Scoring model for different demographics and platforms

### Class Diagram

```
┌─────────────────┐
│   IdeaSource    │
│  (inspiration)  │
└────────┬────────┘
         │
         │ transforms into
         ▼
┌─────────────────┐     ┌──────────────────┐
│ CollectedIdea   │────▶│ ViralPotential   │
│  (original)     │     │  - Age groups    │
└────────┬────────┘     │  - Gender        │
         │              │  - Platforms     │
         │              │  - Regions       │
         │              │  - Overall score │
         │              └──────────────────┘
         │
         │ registered in
         ▼
┌─────────────────────────┐
│ IdeaCollectorRegistry   │
│  (centralized storage)  │
└─────────────────────────┘
```

## Models

### IdeaSource

Represents source material collected for inspiration:

```csharp
public class IdeaSource
{
    public string Id { get; set; }
    public string Title { get; set; }
    public string OriginalText { get; set; }  // For inspiration only!
    public string? SourceUrl { get; set; }
    public string SourceType { get; set; }  // "reddit", "instagram", etc.
    public string? Author { get; set; }
    public List<string> ImageLinks { get; set; }
    public List<string> VideoLinks { get; set; }
    public bool QuestionableAuthorship { get; set; }
    public List<string> Tags { get; set; }
}
```

### CollectedIdea

The transformed, original idea with scoring:

```csharp
public class CollectedIdea
{
    public string Id { get; set; }
    public IdeaSource? Source { get; set; }  // Reference to inspiration
    public string IdeaContent { get; set; }  // ORIGINAL transformed content
    public ViralPotential ViralPotential { get; set; }
    public string CollectorName { get; set; }
    public string? TransformationNotes { get; set; }
    
    public void CalculateOverallScore();  // Updates overall score
}
```

### ViralPotential

Demographic and platform scoring:

```csharp
public class ViralPotential
{
    public int Overall { get; set; }  // 0-100
    public Dictionary<string, int> Platforms { get; set; }  // youtube, tiktok, instagram
    public Dictionary<string, int> Regions { get; set; }    // US, AU, GB
    public Dictionary<string, int> AgeGroups { get; set; }  // 10_15, 15_20, 20_25, etc.
    public Dictionary<string, int> Gender { get; set; }     // woman, man
    
    public int CalculateOverall();  // Averages all non-zero scores
}
```

## Usage

### Basic Example

```csharp
using StoryGenerator.Core.Collectors;
using StoryGenerator.Core.Models;
using StoryGenerator.Core.Services;

// 1. Create sources (from API, scraping, etc.)
var source = new IdeaSource
{
    Title = "Friend betrayed me at my wedding",
    OriginalText = "My best friend told everyone my secret...",
    SourceType = "reddit",
    SourceUrl = "https://reddit.com/r/relationships/...",
    Tags = new List<string> { "betrayal", "friendship", "wedding" }
};

// 2. Use a collector to transform sources into ideas
var collector = new ManualIdeaCollector();
var parameters = new Dictionary<string, object>
{
    { "sources", new List<IdeaSource> { source } }
};

var ideas = await collector.CollectAndTransformAsync(parameters);

// 3. Register ideas in central registry
var registry = new IdeaCollectorRegistry();
registry.RegisterIdeas(ideas);

// 4. Query ideas by score
var topIdeas = registry.GetTopIdeas(10);
var highWomenScore = registry.GetIdeasByCategoryScores(new Dictionary<string, int>
{
    { "gender_woman", 70 },
    { "age_15_20", 65 }
});

// 5. Export to JSON
var json = registry.ToJson();
File.WriteAllText("ideas_registry.json", json);
```

### Implementing a Custom Collector

```csharp
public class RedditCollector : BaseIdeaCollector
{
    public override string Name => "RedditCollector";
    public override string Version => "1.0.0";
    public override string SourceType => "reddit";

    public override async Task<List<IdeaSource>> CollectSourcesAsync(
        Dictionary<string, object> parameters,
        CancellationToken cancellationToken = default)
    {
        // 1. Extract parameters
        var subreddit = parameters["subreddit"] as string;
        var limit = (int)parameters.GetValueOrDefault("limit", 20);
        
        // 2. Call Reddit API
        var posts = await _redditClient.GetTopPostsAsync(subreddit, limit);
        
        // 3. Convert to IdeaSource
        return posts.Select(post => new IdeaSource
        {
            Title = post.Title,
            OriginalText = post.SelfText,
            SourceUrl = post.Url,
            SourceType = "reddit",
            Author = post.Author,
            Tags = post.Flair != null ? new List<string> { post.Flair } : new()
        }).ToList();
    }

    public override async Task<List<CollectedIdea>> TransformToIdeasAsync(
        List<IdeaSource> sources,
        CancellationToken cancellationToken = default)
    {
        var ideas = new List<CollectedIdea>();
        
        foreach (var source in sources)
        {
            // Use LLM to transform source into original idea
            var ideaContent = await TransformWithLLM(source);
            
            // Ensure originality
            if (!IsOriginalContent(ideaContent, source.OriginalText))
            {
                continue;  // Skip if too similar
            }
            
            var idea = CreateCollectedIdea(source, ideaContent);
            
            // Score the idea
            idea.ViralPotential = await ScoreIdea(ideaContent, source);
            idea.CalculateOverallScore();
            
            ideas.Add(idea);
        }
        
        return ideas;
    }
    
    private async Task<string> TransformWithLLM(IdeaSource source)
    {
        var prompt = $@"Transform this story idea into an original concept.
        
Original Title: {source.Title}
Original Content: {source.OriginalText}

Create a NEW story that is INSPIRED by this but is completely original.
Focus on the emotional core and key themes, but change specific details, characters, and plot.";

        return await _llmClient.GenerateAsync(prompt);
    }
}
```

### Registry Queries

```csharp
var registry = new IdeaCollectorRegistry();

// Get all ideas
var allIdeas = registry.Ideas;

// Get top N ideas
var top10 = registry.GetTopIdeas(10);

// Filter by minimum score
var highScoring = registry.GetIdeasByMinScore(70);

// Filter by collector
var redditIdeas = registry.GetIdeasByCollector("RedditCollector");

// Complex category filtering
var filters = new Dictionary<string, int>
{
    { "gender_woman", 75 },      // Women score >= 75
    { "age_15_20", 70 },          // Age 15-20 score >= 70
    { "region_US", 65 },          // US region score >= 65
    { "platform_tiktok", 80 }     // TikTok platform score >= 80
};
var filteredIdeas = registry.GetIdeasByCategoryScores(filters);

// Statistics
Console.WriteLine($"Total ideas: {registry.TotalIdeas}");
foreach (var stat in registry.CollectorStats)
{
    Console.WriteLine($"{stat.Key}: {stat.Value} ideas");
}
```

## Scoring System

### Category Scores

Each idea receives scores (0-100) across multiple dimensions:

1. **Gender**: `woman`, `man`
2. **Age Groups**: `10_15`, `15_20`, `20_25`, `25_30`, `30_50`, `50_70`
3. **Platforms**: `youtube`, `tiktok`, `instagram`
4. **Regions**: `US`, `AU`, `GB`

### Overall Score Calculation

The overall score is calculated by averaging all non-zero category scores:

```csharp
// Example scores
var potential = new ViralPotential();
potential.Gender["woman"] = 85;
potential.Gender["man"] = 0;      // Not counted (zero)
potential.AgeGroups["15_20"] = 90;
potential.AgeGroups["20_25"] = 75;
potential.Platforms["tiktok"] = 95;
potential.Regions["US"] = 80;

// Calculate: (85 + 90 + 75 + 95 + 80) / 5 = 85
int overall = potential.CalculateOverall();
```

### Scoring Guidelines

- **80-100**: Exceptional viral potential
- **60-79**: High viral potential
- **40-59**: Moderate viral potential
- **20-39**: Low viral potential
- **0-19**: Very low viral potential

## Source Validation

All collectors validate sources before transformation:

```csharp
public bool ValidateSource(IdeaSource source)
{
    // Reject null sources
    if (source == null) return false;
    
    // Reject questionable authorship
    if (source.QuestionableAuthorship) return false;
    
    // Ensure we have content
    if (string.IsNullOrWhiteSpace(source.Title) && 
        string.IsNullOrWhiteSpace(source.OriginalText))
        return false;
    
    return true;
}
```

### Originality Check

The base collector includes a similarity check:

```csharp
protected bool IsOriginalContent(string ideaContent, string originalText)
{
    // Returns false if >80% word overlap
    // This ensures transformed ideas are sufficiently different
}
```

## Best Practices

### 1. Always Transform Content

```csharp
// ❌ BAD: Direct copy
var idea = new CollectedIdea
{
    IdeaContent = source.OriginalText  // NEVER do this!
};

// ✅ GOOD: Transformed content
var idea = new CollectedIdea
{
    IdeaContent = await TransformIntoOriginal(source)
};
```

### 2. Flag Questionable Sources

```csharp
var source = new IdeaSource
{
    Title = "Copyrighted material",
    QuestionableAuthorship = true  // Will be filtered out
};
```

### 3. Document Transformations

```csharp
var idea = new CollectedIdea
{
    Source = source,
    IdeaContent = transformedContent,
    TransformationNotes = "Used LLM to extract themes of betrayal and friendship, " +
                         "created new characters and setting, changed plot details"
};
```

### 4. Score Consistently

```csharp
// Always calculate overall score after setting category scores
idea.ViralPotential.Gender["woman"] = 85;
idea.ViralPotential.AgeGroups["15_20"] = 90;
idea.CalculateOverallScore();  // Must call this!
```

## Integration with Pipeline

The Idea Collector system fits into the content pipeline:

```
┌──────────────────────┐
│  Source Collection   │  ← Reddit, Instagram, TikTok APIs
│  (IdeaCollectors)    │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│   Transformation     │  ← LLM transforms into original ideas
│   & Validation       │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│  Viral Scoring       │  ← Score across demographics
│  (ViralPotential)    │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│  Registry Storage    │  ← Centralized idea repository
│  (Registry)          │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│  Idea Selection      │  ← Query, filter, rank ideas
│  & Filtering         │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│  Script Generation   │  ← Existing pipeline continues
└──────────────────────┘
```

## File Structure

```
StoryGenerator.Core/
├── Models/
│   ├── IdeaSource.cs          # Source material model
│   ├── CollectedIdea.cs       # Transformed idea model
│   └── StoryIdea.cs           # Extended with ViralPotential.CalculateOverall()
├── Interfaces/
│   └── IIdeaCollector.cs      # Collector interface
├── Collectors/
│   ├── BaseIdeaCollector.cs   # Abstract base class
│   └── ManualIdeaCollector.cs # Example implementation
└── Services/
    └── IdeaCollectorRegistry.cs # Central registry

StoryGenerator.Tests/
└── Collectors/
    └── IdeaCollectorTests.cs   # Comprehensive tests
```

## Testing

Run the tests:

```bash
cd src/CSharp
dotnet test StoryGenerator.Tests/StoryGenerator.Tests.csproj \
    --filter "FullyQualifiedName~IdeaCollectorTests"
```

All tests validate:
- ✅ Model creation and defaults
- ✅ Overall score calculation
- ✅ Zero score handling
- ✅ Collector collection and transformation
- ✅ Source validation
- ✅ Registry operations
- ✅ Filtering and querying
- ✅ Originality checks
- ✅ JSON serialization

## Future Enhancements

1. **Reddit Collector** - Scrape r/relationships, r/AmITheAsshole, etc.
2. **Instagram Collector** - Collect trending story posts
3. **TikTok Collector** - Extract viral video concepts
4. **LLM Integration** - Use GPT-4/Claude for better transformation
5. **Advanced Scoring** - ML models for viral prediction
6. **Deduplication** - Detect and merge similar ideas
7. **A/B Testing** - Track actual performance vs. predicted scores
8. **Trend Analysis** - Incorporate current viral trends

## License

Part of the StoryGenerator project.
