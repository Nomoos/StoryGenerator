using System;

namespace PrismQ.Shared.Models;

/// <summary>
/// Utility class for normalizing engagement statistics across different platforms.
/// Converts platform-specific metrics into standardized 0-100 scores for comparison.
/// </summary>
public static class SourceStatsNormalizer
{
    /// <summary>
    /// Normalizes stats from any platform using platform-specific logic.
    /// </summary>
    /// <param name="stats">The source stats to normalize</param>
    /// <returns>Normalized score (0-100)</returns>
    public static double Normalize(SourceStats stats)
    {
        return stats.Platform.ToLower() switch
        {
            "reddit" => NormalizeReddit(stats),
            "youtube" => NormalizeYouTube(stats),
            "tiktok" => NormalizeTikTok(stats),
            "instagram" => NormalizeInstagram(stats),
            "twitter" or "x" => NormalizeTwitter(stats),
            _ => NormalizeGeneric(stats)
        };
    }

    /// <summary>
    /// Normalizes Reddit statistics.
    /// Primary metric: Upvotes. Secondary: Comments, engagement rate.
    /// Scale: 10K+ upvotes = 100 score, 1K upvotes = 50 score, 100 upvotes = 25 score.
    /// </summary>
    public static double NormalizeReddit(SourceStats stats)
    {
        // Base score from upvotes (70% weight)
        // Using logarithmic scale: score = log10(upvotes + 1) * 25
        // Examples: 100 upvotes ≈ 50 points, 1K ≈ 75 points, 10K ≈ 100 points
        // The +1 prevents log10(0) errors, multiplier 25 calibrates the scale
        var upvoteScore = Math.Min(Math.Log10(stats.Likes + 1) * 25, 70);

        // Bonus for engagement rate (15% weight)
        // Multiplier 0.15 means: 10% engagement = 1.5 points, 50% = 7.5 points
        var engagementBonus = Math.Min(stats.EngagementRate * 0.15, 15);

        // Bonus for discussion/comments (15% weight)
        // High comment-to-view ratio indicates valuable discussion
        // Multiplier 1500 calibrated for typical Reddit ratios (0.01 = 15 points)
        var commentRatio = stats.Views > 0 ? (stats.Comments / (double)stats.Views) : 0;
        var commentBonus = Math.Min(commentRatio * 1500, 15);

        var total = upvoteScore + engagementBonus + commentBonus;
        return Math.Min(Math.Max(total, 0), 100);
    }

    /// <summary>
    /// Normalizes YouTube statistics.
    /// Primary metric: Views. Secondary: Like ratio, engagement rate.
    /// Scale: 10M+ views = 100 score, 1M views = 50 score, 100K views = 25 score.
    /// </summary>
    public static double NormalizeYouTube(SourceStats stats)
    {
        // Base score from views (60% weight)
        // Using logarithmic scale: score = log10(views + 1) * 12
        // Examples: 100K views ≈ 60 points, 1M ≈ 72 points, 10M ≈ 96 points
        // Multiplier 12 calibrated to reach ~60 points at 100K views (typical viral threshold)
        var viewScore = Math.Min(Math.Log10(stats.Views + 1) * 12, 60);

        // Like ratio bonus (20% weight)
        // Perfect ratio (100% likes, 0% dislikes) = 20 points
        // If no dislikes reported, assume perfect ratio
        var likeRatio = 1.0;
        if (stats.Dislikes.HasValue && stats.Dislikes > 0)
        {
            var totalVotes = stats.Likes + stats.Dislikes.Value;
            likeRatio = totalVotes > 0 ? stats.Likes / (double)totalVotes : 1.0;
        }
        var likeBonus = likeRatio * 20;

        // Engagement rate bonus (20% weight)
        // Multiplier 0.2 means: 10% engagement = 2 points, 50% = 10 points
        // Capped at 20 to ensure balanced scoring
        var engagementBonus = Math.Min(stats.EngagementRate * 0.2, 20);

        var total = viewScore + likeBonus + engagementBonus;
        return Math.Min(Math.Max(total, 0), 100);
    }

    /// <summary>
    /// Normalizes TikTok statistics.
    /// Primary metric: Views. Secondary: Likes, shares (viral indicator).
    /// Scale: 50M+ views = 100 score, 5M views = 50 score, 500K views = 25 score.
    /// </summary>
    public static double NormalizeTikTok(SourceStats stats)
    {
        // Base score from views (50% weight)
        // TikTok has higher view counts, adjusted logarithmic scale
        // Multiplier 10 gives: 500K views ≈ 57 points, 5M ≈ 67 points, 50M ≈ 77 points
        // Lower base to emphasize engagement (TikTok is more engagement-driven)
        var viewScore = Math.Min(Math.Log10(stats.Views + 1) * 10, 50);

        // Like rate bonus (25% weight)
        // TikTok typically has higher like rates than other platforms
        // Multiplier 250 means: 10% like rate = 25 points (maximum for this factor)
        var likeRate = stats.Views > 0 ? (stats.Likes / (double)stats.Views) : 0;
        var likeBonus = Math.Min(likeRate * 250, 25);

        // Share bonus (25% weight) - shares are key viral indicator on TikTok
        // Multiplier 500 means: 5% share rate = 25 points (shares indicate strong virality)
        // TikTok shares are crucial for algorithm boosting
        var shareRate = stats.Views > 0 ? (stats.Shares / (double)stats.Views) : 0;
        var shareBonus = Math.Min(shareRate * 500, 25);

        var total = viewScore + likeBonus + shareBonus;
        return Math.Min(Math.Max(total, 0), 100);
    }

    /// <summary>
    /// Normalizes Instagram statistics.
    /// Primary metric: Likes. Secondary: Comments, saves, engagement rate.
    /// Scale: 1M+ likes = 100 score, 100K likes = 50 score, 10K likes = 25 score.
    /// </summary>
    public static double NormalizeInstagram(SourceStats stats)
    {
        // Base score from likes (60% weight)
        var likeScore = Math.Min(Math.Log10(stats.Likes + 1) * 15, 60);

        // Engagement rate bonus (25% weight)
        var engagementBonus = Math.Min(stats.EngagementRate * 0.25, 25);

        // Save rate bonus (15% weight) - saves indicate high-value content
        var saveRate = stats.Views > 0 && stats.Saves.HasValue
            ? (stats.Saves.Value / (double)stats.Views)
            : 0;
        var saveBonus = Math.Min(saveRate * 300, 15);

        var total = likeScore + engagementBonus + saveBonus;
        return Math.Min(Math.Max(total, 0), 100);
    }

    /// <summary>
    /// Normalizes Twitter/X statistics.
    /// Primary metric: Views/Impressions. Secondary: Retweets (shares), likes.
    /// Scale: 10M+ views = 100 score, 1M views = 50 score, 100K views = 25 score.
    /// </summary>
    public static double NormalizeTwitter(SourceStats stats)
    {
        // Base score from views (50% weight)
        var viewScore = Math.Min(Math.Log10(stats.Views + 1) * 10, 50);

        // Retweet bonus (30% weight) - retweets are primary viral indicator
        var retweetRate = stats.Views > 0 ? (stats.Shares / (double)stats.Views) : 0;
        var retweetBonus = Math.Min(retweetRate * 300, 30);

        // Engagement rate bonus (20% weight)
        var engagementBonus = Math.Min(stats.EngagementRate * 0.2, 20);

        var total = viewScore + retweetBonus + engagementBonus;
        return Math.Min(Math.Max(total, 0), 100);
    }

    /// <summary>
    /// Generic normalization for unknown platforms.
    /// Uses basic engagement metrics without platform-specific optimizations.
    /// </summary>
    public static double NormalizeGeneric(SourceStats stats)
    {
        // View-based score (50% weight)
        var viewScore = Math.Min(Math.Log10(stats.Views + 1) * 10, 50);

        // Like-based score (30% weight)
        var likeScore = Math.Min(Math.Log10(stats.Likes + 1) * 7.5, 30);

        // Engagement rate bonus (20% weight)
        var engagementBonus = Math.Min(stats.EngagementRate * 0.2, 20);

        var total = viewScore + likeScore + engagementBonus;
        return Math.Min(Math.Max(total, 0), 100);
    }

    /// <summary>
    /// Updates the source stats with calculated engagement rate and normalized score.
    /// Modifies the stats object in place.
    /// </summary>
    /// <param name="stats">The source stats to update</param>
    public static void UpdateScores(SourceStats stats)
    {
        stats.CalculateEngagementRate();
        stats.NormalizedScore = Normalize(stats);
    }
}
