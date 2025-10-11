using StoryGenerator.Core.Models;

namespace PrismQ.StoryGenerator;

/// <summary>
/// Interface for generating scripts from story ideas.
/// Ported from Python Generators/GScript.py.
/// </summary>
public interface IScriptGenerator : IGenerator
{
    /// <summary>
    /// Generates a script from a story idea.
    /// Target length: ~360 words (~60 seconds of speech).
    /// </summary>
    /// <param name="storyIdea">The story idea to generate a script from.</param>
    /// <param name="cancellationToken">Cancellation token.</param>
    /// <returns>The generated script text.</returns>
    Task<string> GenerateScriptAsync(StoryIdea storyIdea, CancellationToken cancellationToken = default);

    /// <summary>
    /// Generates a script and saves it along with the idea file.
    /// </summary>
    /// <param name="storyIdea">The story idea to generate a script from.</param>
    /// <param name="outputDirectory">Base directory for scripts (will create story subfolder).</param>
    /// <param name="cancellationToken">Cancellation token.</param>
    /// <returns>Path to the saved script file.</returns>
    Task<string> GenerateAndSaveScriptAsync(
        StoryIdea storyIdea,
        string outputDirectory,
        CancellationToken cancellationToken = default);
}
