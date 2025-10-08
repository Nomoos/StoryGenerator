using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading;
using System.Threading.Tasks;
using StoryGenerator.Core.Models;

namespace StoryGenerator.Core.Collectors;

/// <summary>
/// A simple manual idea collector for testing and demonstration purposes.
/// Allows manual creation of idea sources and their transformation.
/// </summary>
public class ManualIdeaCollector : BaseIdeaCollector
{
    /// <summary>
    /// Gets the name of the collector.
    /// </summary>
    public override string Name => "ManualIdeaCollector";

    /// <summary>
    /// Gets the version of the collector.
    /// </summary>
    public override string Version => "1.0.0";

    /// <summary>
    /// Gets the type of source this collector works with.
    /// </summary>
    public override string SourceType => "manual";

    /// <summary>
    /// Collects source material from manually provided sources.
    /// </summary>
    /// <param name="parameters">
    /// Expected parameters:
    /// - "sources": List&lt;IdeaSource&gt; - The manually created sources
    /// </param>
    public override Task<List<IdeaSource>> CollectSourcesAsync(
        Dictionary<string, object> parameters,
        CancellationToken cancellationToken = default)
    {
        if (parameters.TryGetValue("sources", out var sourcesObj) && sourcesObj is List<IdeaSource> sources)
        {
            return Task.FromResult(sources);
        }

        return Task.FromResult(new List<IdeaSource>());
    }

    /// <summary>
    /// Transforms collected sources into scored idea objects.
    /// Uses basic content analysis to estimate viral potential.
    /// </summary>
    public override Task<List<CollectedIdea>> TransformToIdeasAsync(
        List<IdeaSource> sources,
        CancellationToken cancellationToken = default)
    {
        var ideas = new List<CollectedIdea>();

        foreach (var source in sources)
        {
            cancellationToken.ThrowIfCancellationRequested();

            // Create a transformed idea that's inspired by but not copied from the source
            var ideaContent = TransformSourceToIdea(source);

            // Ensure the content is original
            if (!IsOriginalContent(ideaContent, source.OriginalText))
            {
                // If too similar, skip or modify further
                continue;
            }

            var idea = CreateCollectedIdea(
                source,
                ideaContent,
                $"Manually transformed from {source.SourceType} source"
            );

            // Estimate viral potential
            idea.ViralPotential = EstimateViralPotential(ideaContent, source);
            idea.CalculateOverallScore();

            ideas.Add(idea);
        }

        return Task.FromResult(ideas);
    }

    /// <summary>
    /// Transforms a source into an original idea.
    /// This is a simple implementation - real collectors should use more sophisticated methods.
    /// </summary>
    private string TransformSourceToIdea(IdeaSource source)
    {
        // In a real implementation, this would use NLP, LLMs, or other techniques
        // to create truly original content inspired by the source
        
        var parts = new List<string>();

        if (!string.IsNullOrWhiteSpace(source.Title))
        {
            parts.Add($"Story inspired by: {source.Title}");
        }

        if (!string.IsNullOrWhiteSpace(source.OriginalText))
        {
            // Extract key themes but don't copy directly
            var themes = ExtractThemes(source.OriginalText);
            if (themes.Any())
            {
                parts.Add($"Key themes: {string.Join(", ", themes)}");
            }
        }

        if (source.Tags.Any())
        {
            parts.Add($"Categories: {string.Join(", ", source.Tags)}");
        }

        return string.Join(" | ", parts);
    }

    /// <summary>
    /// Extracts themes from text using simple keyword analysis.
    /// Real implementations should use more sophisticated NLP.
    /// </summary>
    private List<string> ExtractThemes(string text)
    {
        var themes = new List<string>();
        var textLower = text.ToLower();

        // Simple theme detection based on keywords
        var themeKeywords = new Dictionary<string, string[]>
        {
            { "friendship", new[] { "friend", "friendship", "buddy", "companion" } },
            { "family", new[] { "family", "parent", "sibling", "mother", "father" } },
            { "romance", new[] { "love", "romance", "relationship", "dating" } },
            { "betrayal", new[] { "betray", "betrayal", "backstab", "deceive" } },
            { "success", new[] { "success", "achieve", "accomplish", "win" } },
            { "struggle", new[] { "struggle", "challenge", "difficult", "hardship" } },
            { "transformation", new[] { "change", "transform", "evolve", "growth" } }
        };

        foreach (var theme in themeKeywords)
        {
            if (theme.Value.Any(keyword => textLower.Contains(keyword)))
            {
                themes.Add(theme.Key);
            }
        }

        return themes.Take(3).ToList(); // Return up to 3 themes
    }
}
