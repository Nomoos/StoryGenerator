using System;
using System.Collections.Generic;
using System.Text.Json.Serialization;

namespace StoryGenerator.Core.Models;

/// <summary>
/// Represents a source of inspiration for story ideas.
/// Contains metadata like title, original text, image links, etc.
/// This content is used ONLY as inspiration and should NEVER appear directly in the final product.
/// </summary>
public class IdeaSource
{
    /// <summary>
    /// Gets or sets the unique identifier for the source.
    /// </summary>
    [JsonPropertyName("id")]
    public string Id { get; set; } = Guid.NewGuid().ToString();

    /// <summary>
    /// Gets or sets the title of the source material.
    /// </summary>
    [JsonPropertyName("title")]
    public string Title { get; set; } = string.Empty;

    /// <summary>
    /// Gets or sets the original text from the source.
    /// WARNING: This is for inspiration only - never use directly in final product.
    /// </summary>
    [JsonPropertyName("original_text")]
    public string OriginalText { get; set; } = string.Empty;

    /// <summary>
    /// Gets or sets the URL or source location.
    /// </summary>
    [JsonPropertyName("source_url")]
    public string? SourceUrl { get; set; }

    /// <summary>
    /// Gets or sets the type of source (e.g., "reddit", "instagram", "tiktok", "manual").
    /// </summary>
    [JsonPropertyName("source_type")]
    public string SourceType { get; set; } = "manual";

    /// <summary>
    /// Gets or sets the author/creator of the original content (if known).
    /// </summary>
    [JsonPropertyName("author")]
    public string? Author { get; set; }

    /// <summary>
    /// Gets or sets image links associated with the source.
    /// </summary>
    [JsonPropertyName("image_links")]
    public List<string> ImageLinks { get; set; } = new();

    /// <summary>
    /// Gets or sets video links associated with the source.
    /// </summary>
    [JsonPropertyName("video_links")]
    public List<string> VideoLinks { get; set; } = new();

    /// <summary>
    /// Gets or sets additional metadata about the source.
    /// </summary>
    [JsonPropertyName("metadata")]
    public Dictionary<string, object> Metadata { get; set; } = new();

    /// <summary>
    /// Gets or sets the timestamp when this source was collected.
    /// </summary>
    [JsonPropertyName("collected_at")]
    public DateTime CollectedAt { get; set; } = DateTime.UtcNow;

    /// <summary>
    /// Gets or sets whether this source has questionable authorship or copyright concerns.
    /// If true, extra caution should be taken to ensure only inspiration is derived.
    /// </summary>
    [JsonPropertyName("questionable_authorship")]
    public bool QuestionableAuthorship { get; set; } = false;

    /// <summary>
    /// Gets or sets tags or categories for this source.
    /// </summary>
    [JsonPropertyName("tags")]
    public List<string> Tags { get; set; } = new();

    /// <summary>
    /// Returns a string representation of the idea source.
    /// </summary>
    public override string ToString()
    {
        return $"IdeaSource(Id='{Id}', Title='{Title}', SourceType='{SourceType}')";
    }
}
