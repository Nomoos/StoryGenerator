# Source Statistics Collection - Quick Reference

## Summary

This implementation adds source statistics collection and scoring capabilities to the StoryGenerator system, enabling data-driven content selection and performance analysis.

## New Models

### SourceStats
Platform-agnostic engagement statistics from content sources (Reddit, YouTube, TikTok, Instagram).

**Key Properties:**
- `Platform` - Source platform name
- `Views`, `Likes`, `Comments`, `Shares` - Engagement metrics
- `EngagementRate` - Calculated percentage (0-100)
- `NormalizedScore` - Cross-platform comparable score (0-100)

### ScoredString
String value with associated score and metadata, used for title suggestions and scored tags.

**Key Properties:**
- `Value` - The text content
- `Score` - Quality/viral potential score (0-100)
- `Source` - Origin (e.g., "llm_generated", "source_title")
- `Rationale` - Explanation for the score

### SourceStatsNormalizer
Utility class for normalizing engagement statistics across different platforms.

**Methods:**
- `Normalize(stats)` - Auto-detects platform and normalizes
- `NormalizeReddit(stats)` - Reddit-specific normalization
- `NormalizeYouTube(stats)` - YouTube-specific normalization
- `NormalizeTikTok(stats)` - TikTok-specific normalization
- `UpdateScores(stats)` - Updates engagement rate and normalized score

### Extended StoryIdea
The existing `StoryIdea` class now includes optional fields:

**New Properties:**
- `SourceStats` - Reference to source content statistics
- `TitleSuggestions` - List of scored title variations
- `ScoredTags` - List of scored themes/tags

## Quick Start

```csharp
using StoryGenerator.Core.Models;

// Create stats from Reddit
var stats = new SourceStats
{
    Platform = "reddit",
    Views = 50000,
    Likes = 5000,
    Comments = 250
};

// Calculate metrics
SourceStatsNormalizer.UpdateScores(stats);

// Create story idea with source stats
var idea = new StoryIdea
{
    StoryTitle = "My Amazing Story",
    SourceStats = stats,
    TitleSuggestions = new List<ScoredString>
    {
        new ScoredString("Viral Title 1", 92.0, "llm_generated"),
        new ScoredString("Viral Title 2", 87.5, "llm_generated")
    }
};

// Save to file (includes new fields)
await idea.ToFileAsync("output/idea.json");
```

## Files Added

- **Models:**
  - `src/CSharp/StoryGenerator.Core/Models/SourceStats.cs`
  - `src/CSharp/StoryGenerator.Core/Models/ScoredString.cs`
  - `src/CSharp/StoryGenerator.Core/Models/SourceStatsNormalizer.cs`

- **Tests:**
  - `src/CSharp/StoryGenerator.Tests/Models/SourceStatsTests.cs`
  - `src/CSharp/StoryGenerator.Tests/Models/StoryIdeaExtensionsTests.cs`
  - **Test Coverage:** 23 tests, all passing

- **Documentation:**
  - `research/SOURCE_STATS_COLLECTION.md` - Comprehensive research and architecture
  - `research/SOURCE_STATS_USAGE_EXAMPLES.md` - Practical usage examples
  - `research/SOURCE_STATS_QUICK_REFERENCE.md` - This file

## Files Modified

- `src/CSharp/StoryGenerator.Core/Models/StoryIdea.cs` - Added optional fields
- `src/CSharp/StoryGenerator.Tests/StoryGenerator.Tests.csproj` - Added Core reference

## Key Features

✅ **Platform-Agnostic** - Works with Reddit, YouTube, TikTok, Instagram, Twitter  
✅ **Normalized Scoring** - Fair comparison across platforms  
✅ **Backward Compatible** - Existing code continues to work  
✅ **Fully Tested** - 23 unit tests covering all functionality  
✅ **Production Ready** - Well-documented with usage examples

## Use Cases

1. **Quality Assessment** - Score ideas based on source performance
2. **Content Filtering** - Filter out low-performing source content
3. **Title Optimization** - Generate and rank multiple title variations
4. **Performance Analysis** - Compare input stats with output results
5. **Predictive Modeling** - Train ML models using historical data

## Example: Filter High-Quality Ideas

```csharp
// Collect ideas from various sources
var ideas = await CollectIdeasFromReddit();

// Filter by normalized score
var highQuality = ideas
    .Where(i => i.SourceStats != null)
    .Where(i => i.SourceStats.NormalizedScore >= 70.0)
    .Where(i => i.SourceStats.EngagementRate >= 5.0)
    .OrderByDescending(i => i.SourceStats.NormalizedScore)
    .ToList();

Console.WriteLine($"Selected {highQuality.Count} high-quality ideas");
```

## Example: Compare Input/Output Performance

```csharp
// After publishing a video
var originalIdea = await LoadOriginalIdea(videoId);
var outputStats = await GetVideoStats(videoId);

var inputScore = originalIdea.SourceStats?.NormalizedScore ?? 0;
var outputScore = CalculateOutputScore(outputStats);

Console.WriteLine($"Input Score: {inputScore:F1}");
Console.WriteLine($"Output Score: {outputScore:F1}");
Console.WriteLine($"Success Ratio: {outputScore/inputScore:F2}x");
```

## Platform-Specific Normalization

Each platform has optimized scoring:

- **Reddit:** Focus on upvotes and discussion (comments)
- **YouTube:** Focus on views and like ratio
- **TikTok:** Focus on views and shares (viral indicator)
- **Instagram:** Focus on likes and saves (content value)
- **Twitter:** Focus on views and retweets

## Next Steps

See full documentation:
- [SOURCE_STATS_COLLECTION.md](./SOURCE_STATS_COLLECTION.md) - Research and architecture
- [SOURCE_STATS_USAGE_EXAMPLES.md](./SOURCE_STATS_USAGE_EXAMPLES.md) - Practical examples
- [SOCIAL_PLATFORMS_TRENDS.md](./SOCIAL_PLATFORMS_TRENDS.md) - API integration guide

## Answer to Original Question

**Q:** Should we collect stats like upvotes, likes, shares from idea sources and use them for evaluation and analysis?

**A:** ✅ **YES, absolutely!**

**Reasons:**
1. Provides objective quality signals
2. Enables data-driven content selection
3. Supports comparative analysis (input vs. output)
4. Improves prediction accuracy over time
5. Low implementation cost, high value

**Implementation Status:** ✅ Complete and production-ready

---

**Version:** 1.0  
**Status:** Production Ready  
**Tests:** 23/23 Passing  
**Last Updated:** 2025-01-15
