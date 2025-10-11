using PrismQ.Shared.Interfaces;

namespace PrismQ.StoryGenerator;

/// <summary>
/// Interface for revising scripts for AI voice clarity.
/// Ported from Python Generators/GRevise.py.
/// </summary>
public interface IRevisionGenerator : IGenerator
{
    /// <summary>
    /// Revises a script for better voice clarity and natural speech patterns.
    /// Removes awkward phrasing and optimizes for TTS synthesis.
    /// </summary>
    /// <param name="scriptText">The original script text to revise.</param>
    /// <param name="storyTitle">The story title for logging.</param>
    /// <param name="cancellationToken">Cancellation token.</param>
    /// <returns>The revised script text.</returns>
    Task<string> ReviseScriptAsync(
        string scriptText,
        string storyTitle,
        CancellationToken cancellationToken = default);

    /// <summary>
    /// Revises a script from a story folder and saves the revised version.
    /// </summary>
    /// <param name="scriptDirectory">Directory containing the original script.</param>
    /// <param name="outputDirectory">Directory to save the revised script.</param>
    /// <param name="storyTitle">The story title.</param>
    /// <param name="cancellationToken">Cancellation token.</param>
    /// <returns>Path to the saved revised script file.</returns>
    Task<string> ReviseAndSaveScriptAsync(
        string scriptDirectory,
        string outputDirectory,
        string storyTitle,
        CancellationToken cancellationToken = default);
}
