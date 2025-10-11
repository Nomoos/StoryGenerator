using System.Collections.Generic;
using System.Threading;
using System.Threading.Tasks;
using StoryGenerator.Core.Models;

namespace PrismQ.Shared.Interfaces;

/// <summary>
/// Interface for collecting ideas from various sources (Reddit, Instagram, TikTok, etc.).
/// Collectors gather source material and transform it into scored idea objects.
/// </summary>
/// <remarks>
/// IMPORTANT: All collectors must ensure that source material is used ONLY as inspiration.
/// Original content, images, and text from sources should NEVER appear directly in final products.
/// This is critical for avoiding copyright issues and questionable authorship concerns.
/// </remarks>
public interface IIdeaCollector
{
    /// <summary>
    /// Gets the name of the collector (e.g., "RedditCollector", "InstagramCollector").
    /// </summary>
    string Name { get; }

    /// <summary>
    /// Gets the version of the collector.
    /// </summary>
    string Version { get; }

    /// <summary>
    /// Gets the type of source this collector works with (e.g., "reddit", "instagram", "tiktok").
    /// </summary>
    string SourceType { get; }

    /// <summary>
    /// Collects source material from the specified source.
    /// </summary>
    /// <param name="parameters">Parameters for collection (URLs, keywords, filters, etc.).</param>
    /// <param name="cancellationToken">Cancellation token.</param>
    /// <returns>List of idea sources collected.</returns>
    Task<List<IdeaSource>> CollectSourcesAsync(
        Dictionary<string, object> parameters,
        CancellationToken cancellationToken = default);

    /// <summary>
    /// Transforms collected sources into scored idea objects.
    /// This is where the creative interpretation happens - sources are used as inspiration only.
    /// </summary>
    /// <param name="sources">The sources to transform.</param>
    /// <param name="cancellationToken">Cancellation token.</param>
    /// <returns>List of collected ideas with viral potential scoring.</returns>
    Task<List<CollectedIdea>> TransformToIdeasAsync(
        List<IdeaSource> sources,
        CancellationToken cancellationToken = default);

    /// <summary>
    /// Collects sources and transforms them into ideas in one operation.
    /// </summary>
    /// <param name="parameters">Parameters for collection.</param>
    /// <param name="cancellationToken">Cancellation token.</param>
    /// <returns>List of collected ideas.</returns>
    Task<List<CollectedIdea>> CollectAndTransformAsync(
        Dictionary<string, object> parameters,
        CancellationToken cancellationToken = default);

    /// <summary>
    /// Validates that a source is appropriate to use (not copyrighted, has clear authorship, etc.).
    /// </summary>
    /// <param name="source">The source to validate.</param>
    /// <returns>True if the source is safe to use as inspiration, false otherwise.</returns>
    bool ValidateSource(IdeaSource source);
}
