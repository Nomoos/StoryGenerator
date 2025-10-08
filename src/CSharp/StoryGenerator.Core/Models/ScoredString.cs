using System;
using System.Collections.Generic;
using System.Text.Json.Serialization;

namespace StoryGenerator.Core.Models;

/// <summary>
/// A string value with an associated score and optional metadata.
/// Used for title suggestions, tag rankings, and other scored text content.
/// Enables tracking and comparing multiple variations of text with their quality scores.
/// </summary>
public class ScoredString
{
    /// <summary>
    /// Gets or sets the string content/value.
    /// The actual text being scored (e.g., a title, tag, or description).
    /// </summary>
    [JsonPropertyName("value")]
    public string Value { get; set; } = string.Empty;

    /// <summary>
    /// Gets or sets the score for this string (0-100 scale).
    /// Higher scores indicate better quality, viral potential, or relevance.
    /// </summary>
    [JsonPropertyName("score")]
    public double Score { get; set; }

    /// <summary>
    /// Gets or sets the optional rationale explaining the score.
    /// Provides human-readable explanation for why this score was assigned.
    /// Useful for debugging and understanding scoring decisions.
    /// </summary>
    [JsonPropertyName("rationale")]
    public string? Rationale { get; set; }

    /// <summary>
    /// Gets or sets the source of this string.
    /// Examples: "llm_generated", "source_title", "manual", "ai_variation", "trend_based"
    /// Helps track provenance and compare different generation methods.
    /// </summary>
    [JsonPropertyName("source")]
    public string Source { get; set; } = "unknown";

    /// <summary>
    /// Gets or sets additional metadata for this scored string.
    /// Can store custom attributes like platform preferences, A/B test results, etc.
    /// Flexible structure for future extensions.
    /// </summary>
    [JsonPropertyName("metadata")]
    public Dictionary<string, object> Metadata { get; set; } = new();

    /// <summary>
    /// Gets or sets when this string was scored.
    /// Enables tracking score changes over time and versioning.
    /// </summary>
    [JsonPropertyName("scored_at")]
    public DateTime ScoredAt { get; set; } = DateTime.UtcNow;

    /// <summary>
    /// Creates a new scored string with default values.
    /// </summary>
    public ScoredString()
    {
    }

    /// <summary>
    /// Creates a new scored string with specified value and score.
    /// </summary>
    /// <param name="value">The string content</param>
    /// <param name="score">The score (0-100)</param>
    public ScoredString(string value, double score)
    {
        Value = value ?? throw new ArgumentNullException(nameof(value));
        Score = score;
    }

    /// <summary>
    /// Creates a new scored string with value, score, and source.
    /// </summary>
    /// <param name="value">The string content</param>
    /// <param name="score">The score (0-100)</param>
    /// <param name="source">The source identifier</param>
    public ScoredString(string value, double score, string source)
    {
        Value = value ?? throw new ArgumentNullException(nameof(value));
        Score = score;
        Source = source ?? "unknown";
    }

    /// <summary>
    /// Creates a new scored string with all primary fields.
    /// </summary>
    /// <param name="value">The string content</param>
    /// <param name="score">The score (0-100)</param>
    /// <param name="source">The source identifier</param>
    /// <param name="rationale">Explanation for the score</param>
    public ScoredString(string value, double score, string source, string? rationale)
    {
        Value = value ?? throw new ArgumentNullException(nameof(value));
        Score = score;
        Source = source ?? "unknown";
        Rationale = rationale;
    }

    /// <summary>
    /// Returns a string representation of the scored string.
    /// </summary>
    public override string ToString()
    {
        return $"ScoredString(Value=\"{Value}\", Score={Score:F1}, Source={Source})";
    }

    /// <summary>
    /// Compares this scored string with another for sorting by score (descending).
    /// Used for ranking lists of scored strings from highest to lowest score.
    /// </summary>
    /// <param name="other">The other scored string to compare with</param>
    /// <returns>Comparison result for sorting</returns>
    public int CompareTo(ScoredString? other)
    {
        if (other == null) return 1;
        // Sort descending by score (higher scores first)
        return other.Score.CompareTo(Score);
    }
}
