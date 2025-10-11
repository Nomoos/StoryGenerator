using PrismQ.Shared.Interfaces;

namespace StoryGenerator.Data.Models;

/// <summary>
/// Represents a job in the database.
/// </summary>
public class Job : IJob
{
    /// <inheritdoc/>
    public string Id { get; set; } = string.Empty;

    /// <inheritdoc/>
    public string Type { get; set; } = string.Empty;

    /// <inheritdoc/>
    public JobStatus Status { get; set; }

    /// <inheritdoc/>
    public DateTime CreatedAt { get; set; }

    /// <inheritdoc/>
    public DateTime UpdatedAt { get; set; }

    /// <inheritdoc/>
    public string? ErrorMessage { get; set; }

    /// <summary>
    /// Additional metadata as JSON.
    /// </summary>
    public string? Metadata { get; set; }
}
