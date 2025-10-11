using System;
using System.Collections.Generic;
using System.Linq;
using System.Text.Json;
using System.Text.Json.Serialization;
using System.Threading;
using System.Threading.Tasks;
using StoryGenerator.Core.Models;

namespace PrismQ.Shared.Core.Services;

/// <summary>
/// Registry that centralizes idea objects from multiple collectors.
/// Provides a single location to access all collected ideas with their scores.
/// </summary>
public class IdeaCollectorRegistry
{
    private readonly Dictionary<string, CollectedIdea> _ideas = new();
    private readonly object _lock = new();

    /// <summary>
    /// Gets all collected ideas in the registry.
    /// </summary>
    [JsonPropertyName("ideas")]
    public IReadOnlyCollection<CollectedIdea> Ideas
    {
        get
        {
            lock (_lock)
            {
                return _ideas.Values.ToList();
            }
        }
    }

    /// <summary>
    /// Gets the total number of ideas in the registry.
    /// </summary>
    [JsonPropertyName("total_ideas")]
    public int TotalIdeas
    {
        get
        {
            lock (_lock)
            {
                return _ideas.Count;
            }
        }
    }

    /// <summary>
    /// Gets statistics about ideas by collector.
    /// </summary>
    [JsonPropertyName("collector_stats")]
    public Dictionary<string, int> CollectorStats
    {
        get
        {
            lock (_lock)
            {
                return _ideas.Values
                    .GroupBy(i => i.CollectorName)
                    .ToDictionary(g => g.Key, g => g.Count());
            }
        }
    }

    /// <summary>
    /// Registers a single collected idea in the registry.
    /// If an idea with the same ID already exists, it will be updated.
    /// </summary>
    /// <param name="idea">The idea to register.</param>
    public void RegisterIdea(CollectedIdea idea)
    {
        if (idea == null)
        {
            throw new ArgumentNullException(nameof(idea));
        }

        // Ensure overall score is calculated
        idea.CalculateOverallScore();

        lock (_lock)
        {
            _ideas[idea.Id] = idea;
        }
    }

    /// <summary>
    /// Registers multiple collected ideas in the registry.
    /// </summary>
    /// <param name="ideas">The ideas to register.</param>
    public void RegisterIdeas(IEnumerable<CollectedIdea> ideas)
    {
        if (ideas == null)
        {
            throw new ArgumentNullException(nameof(ideas));
        }

        foreach (var idea in ideas)
        {
            RegisterIdea(idea);
        }
    }

    /// <summary>
    /// Registers ideas from a collector asynchronously.
    /// </summary>
    /// <param name="collector">The collector to use.</param>
    /// <param name="parameters">Parameters for the collector.</param>
    /// <param name="cancellationToken">Cancellation token.</param>
    /// <returns>Number of ideas registered.</returns>
    public async Task<int> RegisterFromCollectorAsync(
        Interfaces.IIdeaCollector collector,
        Dictionary<string, object> parameters,
        CancellationToken cancellationToken = default)
    {
        var ideas = await collector.CollectAndTransformAsync(parameters, cancellationToken);
        RegisterIdeas(ideas);
        return ideas.Count;
    }

    /// <summary>
    /// Gets an idea by ID.
    /// </summary>
    /// <param name="id">The idea ID.</param>
    /// <returns>The idea if found, null otherwise.</returns>
    public CollectedIdea? GetIdea(string id)
    {
        lock (_lock)
        {
            return _ideas.TryGetValue(id, out var idea) ? idea : null;
        }
    }

    /// <summary>
    /// Gets ideas filtered by minimum overall score.
    /// </summary>
    /// <param name="minScore">Minimum overall score (0-100).</param>
    /// <returns>Filtered ideas.</returns>
    public IEnumerable<CollectedIdea> GetIdeasByMinScore(int minScore)
    {
        lock (_lock)
        {
            return _ideas.Values
                .Where(i => i.ViralPotential.Overall >= minScore)
                .OrderByDescending(i => i.ViralPotential.Overall)
                .ToList();
        }
    }

    /// <summary>
    /// Gets ideas from a specific collector.
    /// </summary>
    /// <param name="collectorName">The collector name.</param>
    /// <returns>Ideas from the specified collector.</returns>
    public IEnumerable<CollectedIdea> GetIdeasByCollector(string collectorName)
    {
        lock (_lock)
        {
            return _ideas.Values
                .Where(i => i.CollectorName == collectorName)
                .ToList();
        }
    }

    /// <summary>
    /// Gets ideas filtered by category scores.
    /// </summary>
    /// <param name="categoryFilters">Dictionary of category filters (e.g., {"gender_woman": 70, "age_15_20": 60}).</param>
    /// <returns>Filtered ideas.</returns>
    public IEnumerable<CollectedIdea> GetIdeasByCategoryScores(Dictionary<string, int> categoryFilters)
    {
        lock (_lock)
        {
            return _ideas.Values.Where(idea =>
            {
                foreach (var filter in categoryFilters)
                {
                    var parts = filter.Key.Split('_', 2);
                    if (parts.Length != 2) continue;

                    var category = parts[0].ToLower();
                    var key = parts[1];
                    var minScore = filter.Value;

                    switch (category)
                    {
                        case "gender":
                            if (!idea.ViralPotential.Gender.TryGetValue(key, out var genderScore) || genderScore < minScore)
                                return false;
                            break;
                        case "age":
                            if (!idea.ViralPotential.AgeGroups.TryGetValue(key, out var ageScore) || ageScore < minScore)
                                return false;
                            break;
                        case "region":
                            if (!idea.ViralPotential.Regions.TryGetValue(key, out var regionScore) || regionScore < minScore)
                                return false;
                            break;
                        case "platform":
                            if (!idea.ViralPotential.Platforms.TryGetValue(key, out var platformScore) || platformScore < minScore)
                                return false;
                            break;
                    }
                }
                return true;
            }).ToList();
        }
    }

    /// <summary>
    /// Gets the top N ideas by overall score.
    /// </summary>
    /// <param name="count">Number of top ideas to return.</param>
    /// <returns>Top N ideas.</returns>
    public IEnumerable<CollectedIdea> GetTopIdeas(int count)
    {
        lock (_lock)
        {
            return _ideas.Values
                .OrderByDescending(i => i.ViralPotential.Overall)
                .Take(count)
                .ToList();
        }
    }

    /// <summary>
    /// Removes an idea from the registry.
    /// </summary>
    /// <param name="id">The idea ID to remove.</param>
    /// <returns>True if removed, false if not found.</returns>
    public bool RemoveIdea(string id)
    {
        lock (_lock)
        {
            return _ideas.Remove(id);
        }
    }

    /// <summary>
    /// Clears all ideas from the registry.
    /// </summary>
    public void Clear()
    {
        lock (_lock)
        {
            _ideas.Clear();
        }
    }

    /// <summary>
    /// Exports the registry to JSON.
    /// </summary>
    /// <returns>JSON representation of the registry.</returns>
    public string ToJson()
    {
        lock (_lock)
        {
            var options = new JsonSerializerOptions
            {
                WriteIndented = true,
                Encoder = System.Text.Encodings.Web.JavaScriptEncoder.UnsafeRelaxedJsonEscaping
            };

            var export = new
            {
                total_ideas = TotalIdeas,
                collector_stats = CollectorStats,
                ideas = _ideas.Values.OrderByDescending(i => i.ViralPotential.Overall).ToList()
            };

            return JsonSerializer.Serialize(export, options);
        }
    }
}
