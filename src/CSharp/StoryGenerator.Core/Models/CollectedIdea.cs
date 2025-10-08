using System;
using System.Text.Json.Serialization;

namespace StoryGenerator.Core.Models;

/// <summary>
/// Represents a collected idea with source information and viral potential scoring.
/// This is the centralized idea object that gets produced by IdeaCollectors.
/// </summary>
public class CollectedIdea
{
    /// <summary>
    /// Gets or sets the unique identifier for the collected idea.
    /// </summary>
    [JsonPropertyName("id")]
    public string Id { get; set; } = Guid.NewGuid().ToString();

    /// <summary>
    /// Gets or sets the source that inspired this idea.
    /// This tracks the original material for reference only.
    /// </summary>
    [JsonPropertyName("source")]
    public IdeaSource? Source { get; set; }

    /// <summary>
    /// Gets or sets the transformed/interpreted idea content.
    /// This should be original content inspired by the source, not a copy.
    /// </summary>
    [JsonPropertyName("idea_content")]
    public string IdeaContent { get; set; } = string.Empty;

    /// <summary>
    /// Gets or sets the viral potential scores for this idea.
    /// Includes scoring for platforms, regions, age groups, and gender.
    /// </summary>
    [JsonPropertyName("viral_potential")]
    public ViralPotential ViralPotential { get; set; } = new();

    /// <summary>
    /// Gets or sets the timestamp when this idea was created.
    /// </summary>
    [JsonPropertyName("created_at")]
    public DateTime CreatedAt { get; set; } = DateTime.UtcNow;

    /// <summary>
    /// Gets or sets the name of the collector that produced this idea.
    /// </summary>
    [JsonPropertyName("collector_name")]
    public string CollectorName { get; set; } = string.Empty;

    /// <summary>
    /// Gets or sets notes about how the source was transformed into the idea.
    /// Useful for understanding the creative process.
    /// </summary>
    [JsonPropertyName("transformation_notes")]
    public string? TransformationNotes { get; set; }

    /// <summary>
    /// Calculates and updates the overall viral potential score.
    /// This is calculated from the individual category scores.
    /// </summary>
    public void CalculateOverallScore()
    {
        ViralPotential.Overall = ViralPotential.CalculateOverall();
    }

    /// <summary>
    /// Returns a string representation of the collected idea.
    /// </summary>
    public override string ToString()
    {
        return $"CollectedIdea(Id='{Id}', Overall={ViralPotential.Overall}, Collector='{CollectorName}')";
    }
}
