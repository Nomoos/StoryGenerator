namespace StoryGenerator.Generators;

/// <summary>
/// Interface for enhancing scripts with ElevenLabs voice tags.
/// Ported from Python Generators/GEnhanceScript.py.
/// </summary>
public interface IEnhancementGenerator : IGenerator
{
    /// <summary>
    /// Enhances a revised script by adding ElevenLabs v3 audio tags.
    /// Tags include emotion markers, pacing cues, and performance directions.
    /// </summary>
    /// <param name="revisedScript">The revised script text to enhance.</param>
    /// <param name="storyTitle">The story title for logging.</param>
    /// <param name="cancellationToken">Cancellation token.</param>
    /// <returns>The enhanced script with audio tags.</returns>
    Task<string> EnhanceScriptAsync(
        string revisedScript,
        string storyTitle,
        CancellationToken cancellationToken = default);

    /// <summary>
    /// Enhances a script from a story folder and saves the enhanced version.
    /// </summary>
    /// <param name="revisedDirectory">Directory containing the revised script.</param>
    /// <param name="storyTitle">The story title.</param>
    /// <param name="cancellationToken">Cancellation token.</param>
    /// <returns>Path to the saved enhanced script file.</returns>
    Task<string> EnhanceAndSaveScriptAsync(
        string revisedDirectory,
        string storyTitle,
        CancellationToken cancellationToken = default);
}
