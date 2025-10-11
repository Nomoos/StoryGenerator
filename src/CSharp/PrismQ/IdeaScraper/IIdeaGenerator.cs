using PrismQ.Shared.Models;

namespace PrismQ.IdeaScraper;

/// <summary>
/// Interface for generating story ideas with viral potential scoring.
/// Ported from Python Generators/GStoryIdeas.py.
/// </summary>
public interface IIdeaGenerator : IGenerator
{
    /// <summary>
    /// Generates story ideas based on a topic.
    /// </summary>
    /// <param name="topic">The topic to generate ideas for.</param>
    /// <param name="count">Number of ideas to generate (default: 5).</param>
    /// <param name="tone">Optional tone for the stories.</param>
    /// <param name="theme">Optional theme for the stories.</param>
    /// <param name="cancellationToken">Cancellation token.</param>
    /// <returns>List of generated story ideas.</returns>
    Task<List<StoryIdea>> GenerateIdeasAsync(
        string topic,
        int count = 5,
        string? tone = null,
        string? theme = null,
        CancellationToken cancellationToken = default);

    /// <summary>
    /// Generates story ideas and saves them to files.
    /// </summary>
    /// <param name="topic">The topic to generate ideas for.</param>
    /// <param name="outputDirectory">Directory to save the ideas.</param>
    /// <param name="count">Number of ideas to generate (default: 5).</param>
    /// <param name="tone">Optional tone for the stories.</param>
    /// <param name="theme">Optional theme for the stories.</param>
    /// <param name="cancellationToken">Cancellation token.</param>
    /// <returns>Paths to the saved idea files.</returns>
    Task<List<string>> GenerateAndSaveIdeasAsync(
        string topic,
        string outputDirectory,
        int count = 5,
        string? tone = null,
        string? theme = null,
        CancellationToken cancellationToken = default);
}
