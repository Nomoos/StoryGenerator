namespace PrismQ.Shared.Models;

/// <summary>
/// Represents audience demographic information.
/// </summary>
public record AudienceSegment
{
    /// <summary>
    /// Gets or initializes the target gender (e.g., "women", "men", "all").
    /// </summary>
    public required string Gender { get; init; }

    /// <summary>
    /// Gets or initializes the target age bucket (e.g., "18-23", "24-30").
    /// </summary>
    public required string AgeBucket { get; init; }
}
