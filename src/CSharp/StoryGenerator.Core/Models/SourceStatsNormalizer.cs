using System;

namespace StoryGenerator.Core.Models;

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
        var upvoteScore = Math.Min(Math.Log10(stats.Likes + 1) * 25, 70);

        // Bonus for engagement rate (15% weight)
        var engagementBonus = Math.Min(stats.EngagementRate * 0.15, 15);

        // Bonus for discussion/comments (15% weight)
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
        var viewScore = Math.Min(Math.Log10(stats.Views + 1) * 12, 60);

        // Like ratio bonus (20% weight)
        var likeRatio = 1.0;
        if (stats.Dislikes.HasValue && stats.Dislikes > 0)
        {
            var totalVotes = stats.Likes + stats.Dislikes.Value;
            likeRatio = totalVotes > 0 ? stats.Likes / (double)totalVotes : 1.0;
        }
        var likeBonus = likeRatio * 20;

        // Engagement rate bonus (20% weight)
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
        var viewScore = Math.Min(Math.Log10(stats.Views + 1) * 10, 50);

        // Like rate bonus (25% weight)
        var likeRate = stats.Views > 0 ? (stats.Likes / (double)stats.Views) : 0;
        var likeBonus = Math.Min(likeRate * 250, 25);

        // Share bonus (25% weight) - shares are key viral indicator on TikTok
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
