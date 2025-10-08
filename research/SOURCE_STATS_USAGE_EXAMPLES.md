# Source Statistics Collection - Usage Examples

This document provides practical examples for using the source statistics collection features in the StoryGenerator system.

## Overview

The source statistics collection system enables you to:
1. **Capture engagement metrics** from content sources (Reddit, YouTube, TikTok, etc.)
2. **Score and rank content** using platform-specific normalization
3. **Track title variations** with scores for A/B testing
4. **Analyze input vs. output performance** for better predictions

## Table of Contents

- [Quick Start](#quick-start)
- [Use Case 1: Reddit Post as Source](#use-case-1-reddit-post-as-source)
- [Use Case 2: YouTube Video as Source](#use-case-2-youtube-video-as-source)
- [Use Case 3: Generating Multiple Title Variations](#use-case-3-generating-multiple-title-variations)
- [Use Case 4: Comparing Input and Output Performance](#use-case-4-comparing-input-and-output-performance)
- [Use Case 5: Filtering Low-Quality Ideas](#use-case-5-filtering-low-quality-ideas)
- [Integration Patterns](#integration-patterns)

---

## Quick Start

### Basic SourceStats Creation

```csharp
using StoryGenerator.Core.Models;

// Create stats from a Reddit post
var stats = new SourceStats
{
    Platform = "reddit",
    SourceUrl = "https://reddit.com/r/AmItheAsshole/comments/abc123",
    Views = 50000,
    Likes = 5000,      // Upvotes
    Comments = 250,
    Shares = 100       // Crossposts
};

// Calculate engagement rate and normalized score
SourceStatsNormalizer.UpdateScores(stats);

Console.WriteLine($"Engagement Rate: {stats.EngagementRate:F2}%");
Console.WriteLine($"Normalized Score: {stats.NormalizedScore:F1}/100");
```

### Creating ScoredStrings

```csharp
// Create a scored title suggestion
var titleSuggestion = new ScoredString(
    value: "I Found Out My Best Friend's Dark Secret",
    score: 87.5,
    source: "llm_generated",
    rationale: "Strong emotional hook, mystery element, first-person perspective"
);

// Create scored tags
var tags = new List<ScoredString>
{
    new ScoredString("friendship", 85.0, "ai_extracted"),
    new ScoredString("betrayal", 82.0, "ai_extracted"),
    new ScoredString("trust", 78.5, "ai_extracted")
};
```

---

## Use Case 1: Reddit Post as Source

**Scenario:** You found a popular Reddit post that you want to adapt into a story.

```csharp
using StoryGenerator.Core.Models;

public async Task<StoryIdea> CreateIdeaFromRedditPost(string postId)
{
    // Step 1: Fetch Reddit post data (using your Reddit client)
    var redditPost = await _redditClient.GetPostAsync(postId);
    
    // Step 2: Create SourceStats
    var sourceStats = new SourceStats
    {
        Platform = "reddit",
        SourceUrl = $"https://reddit.com{redditPost.Permalink}",
        Views = redditPost.NumViews ?? 0,
        Likes = redditPost.Ups,
        Dislikes = redditPost.Downs,
        Comments = redditPost.NumComments,
        Shares = redditPost.NumCrossposts,
        CollectedAt = DateTime.UtcNow
    };
    
    // Store raw metadata for later reference
    sourceStats.RawData["subreddit"] = redditPost.Subreddit;
    sourceStats.RawData["author"] = redditPost.Author;
    sourceStats.RawData["created_utc"] = redditPost.CreatedUtc;
    sourceStats.RawData["awards_count"] = redditPost.TotalAwardsReceived;
    
    // Step 3: Calculate metrics
    SourceStatsNormalizer.UpdateScores(sourceStats);
    
    // Step 4: Create StoryIdea
    var storyIdea = new StoryIdea
    {
        StoryTitle = redditPost.Title,
        SourceStats = sourceStats,
        Theme = ExtractTheme(redditPost.Text),
        EmotionalCore = ExtractEmotionalCore(redditPost.Text)
    };
    
    // Step 5: Generate title variations
    storyIdea.TitleSuggestions = await GenerateTitleVariations(redditPost.Title);
    
    // Step 6: Extract and score tags
    storyIdea.ScoredTags = ExtractScoredTags(redditPost.Text);
    
    return storyIdea;
}

private List<ScoredString> ExtractScoredTags(string text)
{
    var tags = new List<ScoredString>();
    
    // Simple keyword extraction (replace with NLP in production)
    var keywords = new[] 
    {
        ("friendship", 85.0),
        ("betrayal", 82.0),
        ("family", 78.0),
        ("trust", 75.0),
        ("relationship", 72.0)
    };
    
    foreach (var (keyword, score) in keywords)
    {
        if (text.ToLower().Contains(keyword))
        {
            tags.Add(new ScoredString(keyword, score, "keyword_extraction"));
        }
    }
    
    return tags;
}
```

**Output Example:**

```json
{
  "story_title": "AITA for telling my sister's secret to our parents?",
  "source_stats": {
    "platform": "reddit",
    "source_url": "https://reddit.com/r/AmItheAsshole/comments/abc123",
    "views": 85000,
    "likes": 12500,
    "comments": 450,
    "shares": 125,
    "engagement_rate": 15.29,
    "normalized_score": 87.3,
    "raw_data": {
      "subreddit": "AmItheAsshole",
      "awards_count": 15
    }
  },
  "title_suggestions": [
    {
      "value": "I Exposed My Sister's Dark Secret",
      "score": 92.0,
      "source": "llm_generated"
    }
  ]
}
```

---

## Use Case 2: YouTube Video as Source

**Scenario:** You found a trending YouTube video to inspire a story.

```csharp
using StoryGenerator.Core.Models;

public async Task<StoryIdea> CreateIdeaFromYouTubeVideo(string videoId)
{
    // Step 1: Fetch video data from YouTube API
    var video = await _youtubeClient.GetVideoAsync(videoId);
    
    // Step 2: Create SourceStats
    var sourceStats = new SourceStats
    {
        Platform = "youtube",
        SourceUrl = $"https://youtube.com/watch?v={videoId}",
        Views = long.Parse(video.Statistics.ViewCount),
        Likes = long.Parse(video.Statistics.LikeCount ?? "0"),
        Dislikes = long.Parse(video.Statistics.DislikeCount ?? "0"),
        Comments = long.Parse(video.Statistics.CommentCount ?? "0"),
        CollectedAt = DateTime.UtcNow
    };
    
    // Store video metadata
    sourceStats.RawData["video_id"] = videoId;
    sourceStats.RawData["channel"] = video.Snippet.ChannelTitle;
    sourceStats.RawData["category"] = video.Snippet.CategoryId;
    sourceStats.RawData["duration"] = video.ContentDetails.Duration;
    sourceStats.RawData["tags"] = video.Snippet.Tags;
    
    // Step 3: Calculate metrics
    SourceStatsNormalizer.UpdateScores(sourceStats);
    
    // Step 4: Create StoryIdea
    var storyIdea = new StoryIdea
    {
        StoryTitle = video.Snippet.Title,
        SourceStats = sourceStats
    };
    
    // Step 5: Extract best tags from video
    if (video.Snippet.Tags != null && video.Snippet.Tags.Any())
    {
        storyIdea.ScoredTags = video.Snippet.Tags
            .Take(5)
            .Select((tag, index) => new ScoredString(
                tag,
                90.0 - (index * 5), // Descending scores
                "youtube_tags"
            ))
            .ToList();
    }
    
    return storyIdea;
}
```

---

## Use Case 3: Generating Multiple Title Variations

**Scenario:** Generate and score multiple title variations for A/B testing.

```csharp
using StoryGenerator.Core.Models;

public async Task<List<ScoredString>> GenerateTitleVariations(
    string originalTitle,
    string content)
{
    var variations = new List<ScoredString>();
    
    // Add original title
    var originalScore = await _titleScorer.ScoreAsync(originalTitle);
    variations.Add(new ScoredString(
        originalTitle,
        originalScore.Total,
        "source_title",
        originalScore.Rationale
    ));
    
    // Generate LLM variations
    var llmPrompt = $@"
        Generate 3 viral-worthy title variations for this story:
        Original: {originalTitle}
        Content Summary: {content.Substring(0, Math.Min(500, content.Length))}
        
        Requirements:
        - Emotional hook
        - Clear conflict
        - First-person perspective preferred
        - 8-15 words
    ";
    
    var llmTitles = await _llmClient.GenerateAsync(llmPrompt);
    
    foreach (var title in ParseTitles(llmTitles))
    {
        var score = await _titleScorer.ScoreAsync(title);
        variations.Add(new ScoredString(
            title,
            score.Total,
            "llm_generated",
            score.Rationale
        ));
    }
    
    // Sort by score (descending)
    return variations.OrderByDescending(v => v.Score).ToList();
}

// Example usage
var storyIdea = new StoryIdea
{
    StoryTitle = "Original Title",
    TitleSuggestions = await GenerateTitleVariations(
        "AITA for not inviting my sister to my wedding?",
        fullStoryText
    )
};

// Access best title
var bestTitle = storyIdea.TitleSuggestions?.First();
Console.WriteLine($"Best Title: {bestTitle?.Value} (Score: {bestTitle?.Score})");
```

---

## Use Case 4: Comparing Input and Output Performance

**Scenario:** After publishing, compare source stats with your video's performance.

```csharp
using StoryGenerator.Core.Models;

public class PerformanceAnalyzer
{
    public async Task<PerformanceComparison> CompareInputOutput(
        StoryIdea sourceIdea,
        string publishedVideoId)
    {
        // Get output stats from your platform
        var outputStats = await _youtubeClient.GetVideoStatsAsync(publishedVideoId);
        
        // Calculate correlation
        var inputScore = sourceIdea.SourceStats?.NormalizedScore ?? 0;
        var outputScore = CalculateOutputScore(outputStats);
        
        return new PerformanceComparison
        {
            InputPlatform = sourceIdea.SourceStats?.Platform ?? "unknown",
            InputScore = inputScore,
            InputViews = sourceIdea.SourceStats?.Views ?? 0,
            InputEngagementRate = sourceIdea.SourceStats?.EngagementRate ?? 0,
            
            OutputPlatform = "youtube",
            OutputScore = outputScore,
            OutputViews = outputStats.Views,
            OutputEngagementRate = CalculateEngagementRate(outputStats),
            
            Correlation = CalculateCorrelation(inputScore, outputScore),
            SuccessRatio = outputScore / Math.Max(inputScore, 1)
        };
    }
    
    private double CalculateOutputScore(VideoStats stats)
    {
        // Similar to SourceStatsNormalizer but for output
        
        // View score (60% weight): Uses logarithmic scale
        // Multiplier 12 gives: 100K views ≈ 60, 1M views ≈ 72, 10M views ≈ 96
        // This rewards exponential growth while capping at 60 to leave room for other factors
        var viewScore = Math.Min(Math.Log10(stats.Views + 1) * 12, 60);
        
        // Like ratio bonus (20% weight)
        var likeRatio = stats.Dislikes > 0 
            ? stats.Likes / (double)(stats.Likes + stats.Dislikes) 
            : 1.0;
        var likeBonus = likeRatio * 20; // Perfect ratio (1.0) = 20 points
        
        // Engagement bonus (20% weight)
        // Multiplier 0.2 means: 10% engagement rate = 2 points, 50% rate = 10 points
        // Capped at 20 to ensure balanced scoring across all factors
        var engagementBonus = Math.Min(
            CalculateEngagementRate(stats) * 0.2, 
            20
        );
        
        return Math.Min(viewScore + likeBonus + engagementBonus, 100);
    }
}

public class PerformanceComparison
{
    public string InputPlatform { get; set; }
    public double InputScore { get; set; }
    public long InputViews { get; set; }
    public double InputEngagementRate { get; set; }
    
    public string OutputPlatform { get; set; }
    public double OutputScore { get; set; }
    public long OutputViews { get; set; }
    public double OutputEngagementRate { get; set; }
    
    public double Correlation { get; set; }
    public double SuccessRatio { get; set; }
    
    public string GetAnalysis()
    {
        return SuccessRatio switch
        {
            >= 1.5 => "🎉 Outstanding! Output significantly exceeded input performance",
            >= 1.0 => "✅ Success! Output matched or exceeded input performance",
            >= 0.7 => "⚠️ Moderate performance, room for improvement",
            _ => "❌ Underperformed compared to source"
        };
    }
}
```

---

## Use Case 5: Filtering Low-Quality Ideas

**Scenario:** Filter out low-performing source content before investing in production.

```csharp
using StoryGenerator.Core.Models;

public class IdeaFilter
{
    private readonly double _minimumScore;
    
    public IdeaFilter(double minimumScore = 60.0)
    {
        _minimumScore = minimumScore;
    }
    
    public async Task<List<StoryIdea>> FilterHighQualityIdeas(
        List<StoryIdea> allIdeas)
    {
        var filtered = new List<StoryIdea>();
        
        foreach (var idea in allIdeas)
        {
            // Skip if no source stats
            if (idea.SourceStats == null)
            {
                Console.WriteLine($"⚠️ Skipping '{idea.StoryTitle}' - no source stats");
                continue;
            }
            
            // Check normalized score
            if (idea.SourceStats.NormalizedScore < _minimumScore)
            {
                Console.WriteLine(
                    $"❌ Rejected '{idea.StoryTitle}' - " +
                    $"score {idea.SourceStats.NormalizedScore:F1} < {_minimumScore}"
                );
                continue;
            }
            
            // Check minimum engagement
            if (idea.SourceStats.EngagementRate < 5.0)
            {
                Console.WriteLine(
                    $"❌ Rejected '{idea.StoryTitle}' - " +
                    $"engagement {idea.SourceStats.EngagementRate:F1}% < 5%"
                );
                continue;
            }
            
            // Check platform-specific minimums
            if (!MeetsPlatformMinimums(idea.SourceStats))
            {
                Console.WriteLine(
                    $"❌ Rejected '{idea.StoryTitle}' - " +
                    $"doesn't meet {idea.SourceStats.Platform} minimums"
                );
                continue;
            }
            
            Console.WriteLine(
                $"✅ Accepted '{idea.StoryTitle}' - " +
                $"score {idea.SourceStats.NormalizedScore:F1}, " +
                $"engagement {idea.SourceStats.EngagementRate:F1}%"
            );
            
            filtered.Add(idea);
        }
        
        // Sort by normalized score (best first)
        return filtered
            .OrderByDescending(i => i.SourceStats!.NormalizedScore)
            .ToList();
    }
    
    private bool MeetsPlatformMinimums(SourceStats stats)
    {
        return stats.Platform.ToLower() switch
        {
            "reddit" => stats.Likes >= 1000 && stats.Comments >= 50,
            "youtube" => stats.Views >= 100000 && stats.Likes >= 5000,
            "tiktok" => stats.Views >= 500000 && stats.Likes >= 50000,
            "instagram" => stats.Likes >= 10000 && stats.Comments >= 100,
            _ => true // Unknown platforms pass through
        };
    }
}

// Usage
var filter = new IdeaFilter(minimumScore: 70.0);
var highQualityIdeas = await filter.FilterHighQualityIdeas(allIdeas);

Console.WriteLine($"\n📊 Filtered {highQualityIdeas.Count} high-quality ideas from {allIdeas.Count} total");
```

---

## Integration Patterns

### Pattern 1: Idea Collection Pipeline

```csharp
public class IdeaCollectionPipeline
{
    public async Task<List<StoryIdea>> CollectAndScoreIdeas()
    {
        var ideas = new List<StoryIdea>();
        
        // Collect from Reddit
        var redditIdeas = await CollectFromReddit();
        ideas.AddRange(redditIdeas);
        
        // Collect from YouTube
        var youtubeIdeas = await CollectFromYouTube();
        ideas.AddRange(youtubeIdeas);
        
        // Update all scores
        foreach (var idea in ideas)
        {
            if (idea.SourceStats != null)
            {
                SourceStatsNormalizer.UpdateScores(idea.SourceStats);
            }
        }
        
        // Filter and sort
        var filter = new IdeaFilter(minimumScore: 65.0);
        var filtered = await filter.FilterHighQualityIdeas(ideas);
        
        // Save to database or file
        await SaveIdeas(filtered);
        
        return filtered;
    }
}
```

### Pattern 2: Batch Analysis

```csharp
public async Task AnalyzeBatchPerformance(List<string> videoIds)
{
    var results = new List<PerformanceComparison>();
    
    foreach (var videoId in videoIds)
    {
        // Load original idea
        var idea = await LoadOriginalIdea(videoId);
        
        // Compare performance
        var analyzer = new PerformanceAnalyzer();
        var comparison = await analyzer.CompareInputOutput(idea, videoId);
        
        results.Add(comparison);
    }
    
    // Generate report
    var avgSuccessRatio = results.Average(r => r.SuccessRatio);
    var correlationByPlatform = results
        .GroupBy(r => r.InputPlatform)
        .ToDictionary(
            g => g.Key,
            g => g.Average(r => r.Correlation)
        );
    
    Console.WriteLine($"Average Success Ratio: {avgSuccessRatio:F2}x");
    foreach (var (platform, correlation) in correlationByPlatform)
    {
        Console.WriteLine($"{platform} Correlation: {correlation:F2}");
    }
}
```

### Pattern 3: Real-time Scoring Dashboard

```csharp
public class ScoringDashboard
{
    public async Task<DashboardData> GetDashboardData()
    {
        var recentIdeas = await _database.GetRecentIdeas(limit: 50);
        
        return new DashboardData
        {
            TotalIdeas = recentIdeas.Count,
            AverageScore = recentIdeas
                .Where(i => i.SourceStats != null)
                .Average(i => i.SourceStats!.NormalizedScore),
            TopIdeas = recentIdeas
                .Where(i => i.SourceStats != null)
                .OrderByDescending(i => i.SourceStats!.NormalizedScore)
                .Take(10)
                .ToList(),
            ScoreDistribution = CalculateDistribution(recentIdeas),
            PlatformBreakdown = recentIdeas
                .Where(i => i.SourceStats != null)
                .GroupBy(i => i.SourceStats!.Platform)
                .ToDictionary(
                    g => g.Key,
                    g => new PlatformStats
                    {
                        Count = g.Count(),
                        AvgScore = g.Average(i => i.SourceStats!.NormalizedScore),
                        AvgEngagement = g.Average(i => i.SourceStats!.EngagementRate)
                    }
                )
        };
    }
}
```

---

## Best Practices

### 1. Always Validate Input Data

```csharp
public bool ValidateSourceStats(SourceStats stats)
{
    if (string.IsNullOrEmpty(stats.Platform))
        return false;
    
    if (stats.Views < 0 || stats.Likes < 0)
        return false;
    
    if (stats.Views > 0 && stats.Likes > stats.Views)
        return false; // Impossible: more likes than views
    
    return true;
}
```

### 2. Cache Normalized Scores

```csharp
// Calculate once and store
SourceStatsNormalizer.UpdateScores(stats);
await SaveToDatabase(stats); // Stores calculated values
```

### 3. Track Collection Timestamps

```csharp
// Stats change over time - track when collected
stats.CollectedAt = DateTime.UtcNow;

// Later: check if stats are stale
var isStale = (DateTime.UtcNow - stats.CollectedAt).TotalHours > 24;
if (isStale)
{
    // Refresh stats
    stats = await RefreshStats(stats.SourceUrl);
}
```

### 4. Use Raw Data for Platform-Specific Features

```csharp
// Store platform-specific data for later analysis
stats.RawData["reddit_awards"] = post.TotalAwardsReceived;
stats.RawData["youtube_category"] = video.CategoryId;
stats.RawData["tiktok_sounds"] = video.MusicInfo;
```

---

## Conclusion

These patterns and examples demonstrate how to effectively use the source statistics collection system to:
- **Collect** quality metrics from various platforms
- **Score** and **rank** ideas objectively
- **Filter** low-quality content early
- **Analyze** performance for continuous improvement

For more information, see:
- [SOURCE_STATS_COLLECTION.md](./SOURCE_STATS_COLLECTION.md) - Full research and architecture
- [SOCIAL_PLATFORMS_TRENDS.md](./SOCIAL_PLATFORMS_TRENDS.md) - Platform API integration details

---

**Last Updated:** 2025-01-15  
**Version:** 1.0  
**Status:** Production Ready
