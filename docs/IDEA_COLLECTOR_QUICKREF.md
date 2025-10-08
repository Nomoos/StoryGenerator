# IdeaCollector Quick Reference

## Quick Start

```bash
# Run the example
cd src/CSharp/Examples/IdeaCollectorExample
dotnet run

# Run tests
cd src/CSharp
dotnet test StoryGenerator.Tests --filter "IdeaCollectorTests"
```

## Basic Usage

```csharp
// 1. Create a source
var source = new IdeaSource
{
    Title = "Story Title",
    OriginalText = "Source content...",
    SourceType = "reddit"
};

// 2. Transform with collector
var collector = new ManualIdeaCollector();
var ideas = await collector.CollectAndTransformAsync(
    new Dictionary<string, object> { { "sources", new List<IdeaSource> { source } } }
);

// 3. Register in central registry
var registry = new IdeaCollectorRegistry();
registry.RegisterIdeas(ideas);

// 4. Query ideas
var topIdeas = registry.GetTopIdeas(10);
```

## Scoring Quick Reference

```csharp
// Set category scores
idea.ViralPotential.Gender["woman"] = 85;
idea.ViralPotential.AgeGroups["15_20"] = 90;
idea.ViralPotential.Platforms["tiktok"] = 95;
idea.ViralPotential.Regions["US"] = 80;

// Calculate overall (required!)
idea.CalculateOverallScore();
```

## Registry Queries

```csharp
// Top N ideas
registry.GetTopIdeas(10);

// By minimum score
registry.GetIdeasByMinScore(70);

// By collector
registry.GetIdeasByCollector("RedditCollector");

// By category scores
registry.GetIdeasByCategoryScores(new Dictionary<string, int>
{
    { "gender_woman", 75 },
    { "age_15_20", 70 },
    { "platform_tiktok", 80 }
});
```

## Custom Collector Template

```csharp
public class MyCollector : BaseIdeaCollector
{
    public override string Name => "MyCollector";
    public override string Version => "1.0.0";
    public override string SourceType => "my_source";

    public override async Task<List<IdeaSource>> CollectSourcesAsync(
        Dictionary<string, object> parameters,
        CancellationToken cancellationToken = default)
    {
        // Fetch from API/database
        // Return List<IdeaSource>
    }

    public override async Task<List<CollectedIdea>> TransformToIdeasAsync(
        List<IdeaSource> sources,
        CancellationToken cancellationToken = default)
    {
        var ideas = new List<CollectedIdea>();
        foreach (var source in sources)
        {
            var ideaContent = await TransformSourceToOriginal(source);
            if (!IsOriginalContent(ideaContent, source.OriginalText))
                continue;
                
            var idea = CreateCollectedIdea(source, ideaContent);
            idea.ViralPotential = await ScoreIdea(ideaContent);
            idea.CalculateOverallScore();
            ideas.Add(idea);
        }
        return ideas;
    }
}
```

## Important Warnings

### ⚠️ NEVER Copy Source Content Directly

```csharp
// ❌ BAD - Copyright violation
var idea = new CollectedIdea 
{ 
    IdeaContent = source.OriginalText  // NEVER!
};

// ✅ GOOD - Transformed original content
var idea = new CollectedIdea 
{ 
    IdeaContent = await TransformIntoOriginal(source)
};
```

### ⚠️ Always Flag Questionable Sources

```csharp
var source = new IdeaSource
{
    Title = "Copyrighted Material",
    QuestionableAuthorship = true  // Will be filtered out
};
```

### ⚠️ Always Calculate Overall Score

```csharp
// ❌ BAD - Overall score not updated
idea.ViralPotential.Gender["woman"] = 85;

// ✅ GOOD - Overall calculated
idea.ViralPotential.Gender["woman"] = 85;
idea.CalculateOverallScore();
```

## File Locations

```
StoryGenerator.Core/
├── Models/
│   ├── IdeaSource.cs          # Source material
│   ├── CollectedIdea.cs       # Transformed ideas
│   └── StoryIdea.cs           # ViralPotential.CalculateOverall()
├── Interfaces/
│   └── IIdeaCollector.cs      # Collector interface
├── Collectors/
│   ├── BaseIdeaCollector.cs   # Base implementation
│   └── ManualIdeaCollector.cs # Example
└── Services/
    └── IdeaCollectorRegistry.cs # Central registry

StoryGenerator.Tests/
└── Collectors/
    └── IdeaCollectorTests.cs   # Tests

Examples/
└── IdeaCollectorExample/
    └── Program.cs              # Working example
```

## See Also

- **[Full Documentation](../docs/IDEA_COLLECTOR.md)** - Complete guide
- **[Example Application](../src/CSharp/Examples/IdeaCollectorExample)** - Working code
- **[Tests](../src/CSharp/StoryGenerator.Tests/Collectors)** - Test examples
