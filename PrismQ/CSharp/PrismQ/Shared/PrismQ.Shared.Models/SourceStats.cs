using System;
using System.Collections.Generic;
using System.Text.Json.Serialization;

namespace PrismQ.Shared.Models;

/// <summary>
/// Engagement statistics from content source platforms.
/// Provides platform-agnostic structure for tracking viral indicators like views, likes, shares.
/// Used to assess the original performance of content that inspired story ideas.
/// </summary>
public class SourceStats
{
    /// <summary>
    /// Gets or sets the platform where content originated.
    /// Examples: "reddit", "youtube", "tiktok", "instagram", "twitter"
    /// </summary>
    [JsonPropertyName("platform")]
    public string Platform { get; set; } = string.Empty;

    /// <summary>
    /// Gets or sets the URL or ID of the source content.
    /// Enables tracking back to original content for verification.
    /// </summary>
    [JsonPropertyName("source_url")]
    public string SourceUrl { get; set; } = string.Empty;

    /// <summary>
    /// Gets or sets when these statistics were collected.
    /// Important for tracking velocity and temporal changes.
    /// </summary>
    [JsonPropertyName("collected_at")]
    public DateTime CollectedAt { get; set; } = DateTime.UtcNow;

    /// <summary>
    /// Gets or sets the primary engagement metric (views/impressions).
    /// The total number of times content was viewed.
    /// </summary>
    [JsonPropertyName("views")]
    public long Views { get; set; }

    /// <summary>
    /// Gets or sets positive engagement count (upvotes/likes/hearts).
    /// Indicates audience approval and appreciation.
    /// </summary>
    [JsonPropertyName("likes")]
    public long Likes { get; set; }

    /// <summary>
    /// Gets or sets negative engagement count (downvotes/dislikes).
    /// Optional as not all platforms expose this metric.
    /// </summary>
    [JsonPropertyName("dislikes")]
    public long? Dislikes { get; set; }

    /// <summary>
    /// Gets or sets the share/retweet/crosspost count.
    /// Indicates viral spread and content value.
    /// </summary>
    [JsonPropertyName("shares")]
    public long Shares { get; set; }

    /// <summary>
    /// Gets or sets the comment/reply count.
    /// Indicates discussion level and engagement depth.
    /// </summary>
    [JsonPropertyName("comments")]
    public long Comments { get; set; }

    /// <summary>
    /// Gets or sets the save/bookmark count.
    /// Optional metric indicating content value for later consumption.
    /// </summary>
    [JsonPropertyName("saves")]
    public long? Saves { get; set; }

    /// <summary>
    /// Gets or sets the calculated engagement rate (0-100).
    /// Percentage of viewers who engaged (liked, commented, shared).
    /// Formula: (likes + comments + shares + saves) / views * 100
    /// </summary>
    [JsonPropertyName("engagement_rate")]
    public double EngagementRate { get; set; }

    /// <summary>
    /// Gets or sets the normalized score (0-100).
    /// Platform-independent score accounting for different scales.
    /// Allows fair comparison across Reddit, YouTube, TikTok, etc.
    /// </summary>
    [JsonPropertyName("normalized_score")]
    public double NormalizedScore { get; set; }

    /// <summary>
    /// Gets or sets raw metadata from the platform.
    /// Stores platform-specific data that doesn't fit standard fields.
    /// Examples: Reddit awards, YouTube category, TikTok hashtags.
    /// </summary>
    [JsonPropertyName("raw_data")]
    public Dictionary<string, object> RawData { get; set; } = new();

    /// <summary>
    /// Calculates the engagement rate based on current metrics.
    /// Returns percentage of viewers who engaged with content.
    /// </summary>
    /// <returns>Engagement rate as percentage (0-100)</returns>
    public double CalculateEngagementRate()
    {
        if (Views == 0) return 0;

        var totalEngagement = Likes + Comments + Shares + (Saves ?? 0);
        var rate = (totalEngagement / (double)Views) * 100;

        // Update the stored value
        EngagementRate = rate;

        return rate;
    }

    /// <summary>
    /// Returns a string representation of the source stats.
    /// </summary>
    public override string ToString()
    {
        return $"SourceStats(Platform={Platform}, Views={Views:N0}, Likes={Likes:N0}, Score={NormalizedScore:F1})";
    }
}
