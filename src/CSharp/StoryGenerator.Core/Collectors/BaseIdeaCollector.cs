using System;
using System.Collections.Generic;
using System.Threading;
using System.Threading.Tasks;
using StoryGenerator.Core.Interfaces;
using StoryGenerator.Core.Models;

namespace StoryGenerator.Core.Collectors;

/// <summary>
/// Base abstract class for IdeaCollectors that provides common functionality.
/// </summary>
public abstract class BaseIdeaCollector : IIdeaCollector
{
    /// <summary>
    /// Gets the name of the collector.
    /// </summary>
    public abstract string Name { get; }

    /// <summary>
    /// Gets the version of the collector.
    /// </summary>
    public abstract string Version { get; }

    /// <summary>
    /// Gets the type of source this collector works with.
    /// </summary>
    public abstract string SourceType { get; }

    /// <summary>
    /// Collects source material from the specified source.
    /// </summary>
    public abstract Task<List<IdeaSource>> CollectSourcesAsync(
        Dictionary<string, object> parameters,
        CancellationToken cancellationToken = default);

    /// <summary>
    /// Transforms collected sources into scored idea objects.
    /// </summary>
    public abstract Task<List<CollectedIdea>> TransformToIdeasAsync(
        List<IdeaSource> sources,
        CancellationToken cancellationToken = default);

    /// <summary>
    /// Collects sources and transforms them into ideas in one operation.
    /// </summary>
    public virtual async Task<List<CollectedIdea>> CollectAndTransformAsync(
        Dictionary<string, object> parameters,
        CancellationToken cancellationToken = default)
    {
        var sources = await CollectSourcesAsync(parameters, cancellationToken);
        
        // Filter out invalid sources
        var validSources = sources.FindAll(ValidateSource);
        
        return await TransformToIdeasAsync(validSources, cancellationToken);
    }

    /// <summary>
    /// Validates that a source is appropriate to use.
    /// Default implementation checks for questionable authorship flag.
    /// Override to add custom validation logic.
    /// </summary>
    public virtual bool ValidateSource(IdeaSource source)
    {
        if (source == null)
        {
            return false;
        }

        // Reject sources flagged with questionable authorship
        if (source.QuestionableAuthorship)
        {
            return false;
        }

        // Ensure we have some content to work with
        if (string.IsNullOrWhiteSpace(source.Title) && string.IsNullOrWhiteSpace(source.OriginalText))
        {
            return false;
        }

        return true;
    }

    /// <summary>
    /// Creates a CollectedIdea from an IdeaSource with default scoring.
    /// Helper method for derived classes.
    /// </summary>
    protected CollectedIdea CreateCollectedIdea(IdeaSource source, string ideaContent, string? transformationNotes = null)
    {
        return new CollectedIdea
        {
            Source = source,
            IdeaContent = ideaContent,
            CollectorName = Name,
            TransformationNotes = transformationNotes,
            ViralPotential = new ViralPotential()
        };
    }

    /// <summary>
    /// Estimates viral potential scores based on content analysis.
    /// This is a basic implementation that derived classes should override for more sophisticated scoring.
    /// </summary>
    protected virtual ViralPotential EstimateViralPotential(string content, IdeaSource source)
    {
        var potential = new ViralPotential();
        var contentLower = content.ToLower();

        // Basic scoring logic - should be overridden by derived classes
        // This is just a placeholder to demonstrate the concept

        // Age group scoring
        if (contentLower.Contains("teen") || contentLower.Contains("school"))
        {
            potential.AgeGroups["15_20"] = 70;
            potential.AgeGroups["10_15"] = 60;
        }
        else if (contentLower.Contains("college") || contentLower.Contains("university"))
        {
            potential.AgeGroups["20_25"] = 75;
            potential.AgeGroups["15_20"] = 65;
        }
        else
        {
            // Default moderate scores
            potential.AgeGroups["15_20"] = 50;
            potential.AgeGroups["20_25"] = 50;
            potential.AgeGroups["25_30"] = 45;
        }

        // Gender scoring - default balanced
        potential.Gender["woman"] = 50;
        potential.Gender["man"] = 50;

        // Platform scoring - default focus on youth platforms
        potential.Platforms["tiktok"] = 60;
        potential.Platforms["youtube"] = 55;
        potential.Platforms["instagram"] = 55;

        // Region scoring - default US focus
        potential.Regions["US"] = 60;
        potential.Regions["AU"] = 45;
        potential.Regions["GB"] = 45;

        // Calculate overall
        potential.Overall = potential.CalculateOverall();

        return potential;
    }

    /// <summary>
    /// Ensures that the idea content is original and not a direct copy of the source.
    /// This is a safety check to prevent copyright issues.
    /// </summary>
    protected bool IsOriginalContent(string ideaContent, string originalText)
    {
        if (string.IsNullOrWhiteSpace(ideaContent) || string.IsNullOrWhiteSpace(originalText))
        {
            return true;
        }

        // Check if idea is too similar to original (>80% overlap)
        var ideaWords = new HashSet<string>(ideaContent.ToLower().Split(' ', StringSplitOptions.RemoveEmptyEntries));
        var originalWords = new HashSet<string>(originalText.ToLower().Split(' ', StringSplitOptions.RemoveEmptyEntries));

        if (ideaWords.Count == 0)
        {
            return false;
        }

        var overlap = ideaWords.Intersect(originalWords).Count();
        var similarity = (double)overlap / ideaWords.Count;

        return similarity < 0.8; // Less than 80% similarity
    }
}
