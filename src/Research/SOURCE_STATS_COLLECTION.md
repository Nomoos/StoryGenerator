# Source Statistics Collection - Research & Implementation Guide

## Overview

This document researches the value and implementation approach for collecting engagement statistics (upvotes, likes, shares, views) from idea sources and using them to improve content generation and viral potential prediction.

## Problem Statement

**Question:** Should the idea collector gather statistics from content sources (Reddit, YouTube, TikTok, Instagram) and use them for:
1. **Input Evaluation** - Score ideas based on their source performance
2. **Comparative Analysis** - Compare input stats with output performance
3. **Predictive Modeling** - Train better viral potential scoring models

## Value Proposition

### ✅ Benefits of Collecting Source Stats

1. **Quality Signal**: High-performing source content indicates proven viral potential
   - Reddit posts with 10K+ upvotes have demonstrated appeal
   - YouTube videos with high like ratios show audience resonance
   - TikTok videos with strong engagement indicate trend alignment

2. **Training Data**: Enable machine learning for better predictions
   - Input: Source stats (views, likes, shares, comments)
   - Output: Our video performance (views, engagement, revenue)
   - Model: Learn what source characteristics predict our success

3. **Trend Validation**: Verify trending topics are actually trending
   - Google Trends might say "X is trending"
   - Source stats confirm real engagement exists
   - Reduces false positives from trend data

4. **Content Filtering**: Prioritize high-potential ideas
   - Skip low-engagement source content (likely not viral)
   - Focus resources on proven winners
   - Improve ROI on content production

5. **Platform Insights**: Understand platform-specific patterns
   - Reddit: What upvote counts correlate with our success?
   - YouTube: Do high-view videos translate to our platform?
   - TikTok: Which engagement patterns work for our niche?

### ⚠️ Challenges & Considerations

1. **Data Collection Complexity**
   - Multiple platforms with different APIs
   - Rate limits and API costs (see SOCIAL_PLATFORMS_TRENDS.md)
   - Data freshness (stats change over time)

2. **Normalization Issues**
   - 10K upvotes on Reddit ≠ 10K likes on TikTok
   - Different platforms have different scales
   - Need platform-specific normalization

3. **Context Matters**
   - Niche subreddits vs. mainstream subreddits
   - Different video lengths on YouTube
   - Geographic differences in engagement

4. **Temporal Decay**
   - Older content may have high stats but be outdated
   - Recent content may not have accumulated stats yet
   - Need to consider velocity (rate of engagement growth)

## Recommended Architecture

### Phase 1: Foundation (Weeks 1-2)

**Goal:** Enable basic stats collection and storage

```
┌─────────────────────────────────────────────────────────────┐
│                    Idea Collection Flow                      │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Source (Reddit/YouTube/TikTok/Instagram)                   │
│         │                                                     │
│         ├─> Content (title, description, text)              │
│         └─> SourceStats (views, likes, shares, etc.)        │
│                    │                                         │
│                    ▼                                         │
│             RawIdea + SourceStats                           │
│                    │                                         │
│                    ▼                                         │
│         Viral Potential Estimation                          │
│         (considers source stats)                            │
│                    │                                         │
│                    ▼                                         │
│             StoryIdea (enhanced)                            │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

**Core Models:**

1. **SourceStats** - Platform-agnostic engagement metrics
2. **ScoredString** - String with associated score (for titles, tags, etc.)
3. **Enhanced StoryIdea** - Include source reference and stats

### Phase 2: Analysis (Weeks 3-4)

**Goal:** Enable comparative analysis of input vs. output

```
Input Stats              Our Performance          Analysis
─────────────────────   ────────────────────    ──────────────
Reddit: 15K upvotes  →  YouTube: 50K views   →  Correlation: 0.75
Score: 85/100           Engagement: 12%          Pattern: Reddit→YT strong

TikTok: 2M views     →  YouTube: 20K views   →  Correlation: 0.45
Score: 90/100           Engagement: 8%           Pattern: TikTok→YT weak

Instagram: 50K likes →  YouTube: 100K views  →  Correlation: 0.82
Score: 75/100           Engagement: 15%          Pattern: IG→YT very strong
```

**Features:**
- Store our output performance alongside input stats
- Calculate correlation coefficients
- Identify platform-specific patterns
- Generate reports on what works

### Phase 3: Predictive Modeling (Months 2-3)

**Goal:** Use historical data to predict success

```
┌────────────────────────────────────────────────────────┐
│              Predictive Model Training                 │
├────────────────────────────────────────────────────────┤
│                                                        │
│  Input Features:                                       │
│  ✓ Source platform                                     │
│  ✓ Source engagement (views, likes, shares)           │
│  ✓ Source velocity (growth rate)                      │
│  ✓ Content category                                    │
│  ✓ Target audience                                     │
│  ✓ Time of day/week                                    │
│                                                        │
│  Output (to predict):                                  │
│  ✓ Our video views                                     │
│  ✓ Our engagement rate                                 │
│  ✓ Our viral potential score                          │
│                                                        │
│  Model Types:                                          │
│  • Linear Regression (baseline)                        │
│  • Random Forest (feature importance)                  │
│  • Neural Network (complex patterns)                   │
│                                                        │
└────────────────────────────────────────────────────────┘
```

## Data Models

### 1. SourceStats

```csharp
/// <summary>
/// Engagement statistics from content source platforms.
/// Platform-agnostic structure for tracking viral indicators.
/// </summary>
public class SourceStats
{
    /// Platform where content originated (reddit, youtube, tiktok, instagram)
    public string Platform { get; set; } = string.Empty;
    
    /// URL or ID of source content
    public string SourceUrl { get; set; } = string.Empty;
    
    /// When these stats were collected
    public DateTime CollectedAt { get; set; } = DateTime.UtcNow;
    
    /// Primary engagement metric (views/impressions)
    public long Views { get; set; }
    
    /// Positive engagement (upvotes/likes)
    public long Likes { get; set; }
    
    /// Negative engagement (downvotes/dislikes) - optional
    public long? Dislikes { get; set; }
    
    /// Shares/retweets/crossposts
    public long Shares { get; set; }
    
    /// Comments/replies
    public long Comments { get; set; }
    
    /// Saves/bookmarks
    public long? Saves { get; set; }
    
    /// Calculated engagement rate (0-100)
    public double EngagementRate { get; set; }
    
    /// Normalized score (0-100) accounting for platform differences
    public double NormalizedScore { get; set; }
    
    /// Raw metadata from platform
    public Dictionary<string, object> RawData { get; set; } = new();
}
```

### 2. ScoredString

```csharp
/// <summary>
/// A string value with an associated score and optional metadata.
/// Used for title suggestions, tag rankings, and other scored content.
/// </summary>
public class ScoredString
{
    /// The string content
    public string Value { get; set; } = string.Empty;
    
    /// Score (0-100 scale)
    public double Score { get; set; }
    
    /// Optional rationale for the score
    public string? Rationale { get; set; }
    
    /// Source of this string (e.g., "llm_generated", "source_title", "manual")
    public string Source { get; set; } = "unknown";
    
    /// Additional metadata
    public Dictionary<string, object> Metadata { get; set; } = new();
    
    /// When this was scored
    public DateTime ScoredAt { get; set; } = DateTime.UtcNow;
}
```

### 3. Enhanced StoryIdea

Extend existing `StoryIdea` class with optional fields:

```csharp
public class StoryIdea
{
    // ... existing fields ...
    
    /// <summary>
    /// Optional reference to source content stats.
    /// Used when idea originated from specific platform content.
    /// </summary>
    [JsonPropertyName("source_stats")]
    public SourceStats? SourceStats { get; set; }
    
    /// <summary>
    /// Title suggestions with scores.
    /// Alternative titles ranked by viral potential.
    /// </summary>
    [JsonPropertyName("title_suggestions")]
    public List<ScoredString>? TitleSuggestions { get; set; }
    
    /// <summary>
    /// Scored tags/themes for the story.
    /// Helps with categorization and trend alignment.
    /// </summary>
    [JsonPropertyName("scored_tags")]
    public List<ScoredString>? ScoredTags { get; set; }
}
```

## Implementation Recommendations

### Immediate Actions (Week 1)

1. ✅ **Create Models**
   - Add `SourceStats.cs` to `src/CSharp/StoryGenerator.Core/Models/`
   - Add `ScoredString.cs` to `src/CSharp/StoryGenerator.Core/Models/`
   - Extend `StoryIdea.cs` with optional fields

2. ✅ **Documentation**
   - Create this research document
   - Add code examples
   - Document best practices

3. ✅ **Testing**
   - Unit tests for model serialization
   - Test backward compatibility
   - Validate JSON structure

### Near-term (Weeks 2-4)

4. **Reddit Integration** (if using Reddit as source)
   - Collect upvotes, comments, awards
   - Calculate engagement rate
   - Store in SourceStats

5. **Normalization Service**
   - Create `IStatsNormalizer` interface
   - Implement platform-specific normalization
   - Convert raw stats to 0-100 scale

6. **Basic Analysis**
   - Simple correlation calculations
   - Export to CSV for analysis
   - Generate basic reports

### Future Enhancements (Months 2-3)

7. **YouTube API Integration** (see SOCIAL_PLATFORMS_TRENDS.md)
   - Collect view counts, like counts
   - Track video performance
   - Compare with source stats

8. **TikTok Integration** (budget permitting)
   - Via RapidAPI ($10-20/month)
   - Track trending content
   - Validate trend predictions

9. **Machine Learning Pipeline**
   - Feature engineering from source stats
   - Train predictive models
   - A/B test predictions vs. manual selection

## Scoring Formulas

### Engagement Rate Calculation

```csharp
public static double CalculateEngagementRate(SourceStats stats)
{
    if (stats.Views == 0) return 0;
    
    var totalEngagement = stats.Likes + 
                         stats.Comments + 
                         stats.Shares + 
                         (stats.Saves ?? 0);
    
    return (totalEngagement / (double)stats.Views) * 100;
}
```

### Platform Normalization (Reddit Example)

```csharp
public static double NormalizeRedditScore(SourceStats stats)
{
    // Reddit scoring: upvotes are primary metric
    // 10K+ upvotes = 100 score
    // 1K upvotes = 50 score
    // 100 upvotes = 25 score
    
    var upvoteScore = Math.Min(stats.Likes / 100.0, 100);
    
    // Bonus for engagement rate
    var engagementBonus = stats.EngagementRate * 0.5;
    
    // Bonus for comments (shows discussion)
    var commentBonus = Math.Min(stats.Comments / 50.0, 10);
    
    var total = upvoteScore + engagementBonus + commentBonus;
    return Math.Min(total, 100);
}
```

### Platform Normalization (YouTube Example)

```csharp
public static double NormalizeYouTubeScore(SourceStats stats)
{
    // YouTube scoring: views are primary, likes are secondary
    // 10M views = 100 score
    // 1M views = 50 score
    // 100K views = 25 score
    
    var viewScore = Math.Min(stats.Views / 100_000.0, 100);
    
    // Like ratio matters
    var likeRatio = stats.Dislikes.HasValue && stats.Dislikes > 0
        ? stats.Likes / (double)(stats.Likes + stats.Dislikes.Value)
        : 1.0;
    var likeBonus = likeRatio * 10;
    
    // Engagement rate bonus
    var engagementBonus = stats.EngagementRate * 0.5;
    
    var total = viewScore * 0.7 + likeBonus + engagementBonus;
    return Math.Min(total, 100);
}
```

## Usage Examples

### Example 1: Collecting Reddit Stats

```csharp
// Collect idea from Reddit post
var redditPost = await redditClient.GetPostAsync(postId);

var sourceStats = new SourceStats
{
    Platform = "reddit",
    SourceUrl = $"https://reddit.com{redditPost.Permalink}",
    Views = redditPost.Views,
    Likes = redditPost.Upvotes,
    Dislikes = redditPost.Downvotes,
    Comments = redditPost.CommentCount,
    Shares = redditPost.CrosspostCount,
    EngagementRate = CalculateEngagementRate(redditPost),
    NormalizedScore = NormalizeRedditScore(redditPost)
};

var storyIdea = new StoryIdea
{
    StoryTitle = redditPost.Title,
    SourceStats = sourceStats,
    // ... other fields ...
};
```

### Example 2: Generating Title Suggestions

```csharp
// Generate multiple title variations with scores
var titleSuggestions = new List<ScoredString>
{
    new ScoredString
    {
        Value = "I Found Out My Best Friend's Secret",
        Score = 87.5,
        Source = "llm_generated",
        Rationale = "Strong hook, emotional appeal, clear mystery"
    },
    new ScoredString
    {
        Value = "The Secret That Changed Everything",
        Score = 82.0,
        Source = "llm_generated",
        Rationale = "Good intrigue, but less specific"
    },
    new ScoredString
    {
        Value = originalTitle,
        Score = 75.0,
        Source = "source_title",
        Rationale = "Original title from source"
    }
};

storyIdea.TitleSuggestions = titleSuggestions;
```

### Example 3: Comparative Analysis

```csharp
// After video is published, compare performance
var inputScore = storyIdea.SourceStats?.NormalizedScore ?? 0;
var outputViews = await youtubeClient.GetVideoStatsAsync(videoId);

var correlation = CalculateCorrelation(
    inputScore,
    outputViews.Views,
    storyIdea.SourceStats?.Platform ?? "unknown"
);

Console.WriteLine($"Input Score: {inputScore}");
Console.WriteLine($"Output Views: {outputViews.Views}");
Console.WriteLine($"Correlation: {correlation:F2}");
```

## Decision Matrix

| Scenario | Collect Stats? | Priority | Notes |
|----------|---------------|----------|-------|
| Reddit-sourced ideas | ✅ YES | HIGH | Easy to collect, strong signal |
| YouTube trend research | ✅ YES | HIGH | Official API, free quota |
| TikTok trends | ⚠️ MAYBE | MEDIUM | Costs $10-20/month, good ROI if budget allows |
| Instagram content | ❌ NO | LOW | No easy API access, expensive |
| AI-generated ideas | ❌ NO | N/A | No source to collect from |
| Manual ideas | ❌ NO | N/A | No source stats available |

## Best Practices

1. **Always Normalize**: Don't compare raw stats across platforms
2. **Consider Velocity**: Recent high-growth content may be more valuable than older high-stat content
3. **Context Matters**: Store niche/subreddit/category information
4. **Privacy First**: Don't store personal information from sources
5. **Cache Appropriately**: Stats change over time, store collection timestamp
6. **Graceful Degradation**: Code should work with or without source stats

## Conclusion

**Recommendation:** ✅ **YES, collect source stats**

**Reasoning:**
1. High value for quality assessment and filtering
2. Enables data-driven content selection
3. Supports future ML/AI improvements
4. Relatively low implementation cost
5. Existing infrastructure (SOCIAL_PLATFORMS_TRENDS.md) provides blueprint

**Next Steps:**
1. Implement core models (Phase 1)
2. Add Reddit stats collection (if using Reddit)
3. Build normalization service
4. Enable basic analysis and reporting
5. Expand to YouTube/TikTok as budget allows

## References

- [Social Platforms Trends Research](./SOCIAL_PLATFORMS_TRENDS.md)
- [Viral Video Requirements](./VIRAL_VIDEO_REQUIREMENTS.md)
- [Analytics Group Tasks](../issues/p2-medium/analytics/README.md)
- [Reddit API Documentation](https://www.reddit.com/dev/api/)
- [YouTube Data API v3](https://developers.google.com/youtube/v3)

---

**Document Status:** ✅ Complete  
**Last Updated:** 2025-01-15  
**Author:** Research Team  
**Reviewers:** Architecture Team
