namespace PrismQ.SubtitleGenerator;

/// <summary>
/// Subtitle generation result containing the SRT file path and metadata.
/// </summary>
public class SubtitleGenerationResult
{
    /// <summary>
    /// Path to the generated SRT subtitle file.
    /// </summary>
    public string SrtFilePath { get; set; } = string.Empty;

    /// <summary>
    /// Number of words in the subtitle file.
    /// </summary>
    public int WordCount { get; set; }

    /// <summary>
    /// Accuracy percentage of alignment (0-100).
    /// </summary>
    public double AlignmentAccuracy { get; set; }

    /// <summary>
    /// Duration of the audio in seconds.
    /// </summary>
    public double AudioDuration { get; set; }
}

/// <summary>
/// Interface for generating subtitles from audio and script.
/// Ported from Python Generators/GTitles.py.
/// </summary>
public interface ISubtitleGenerator : IGenerator
{
    /// <summary>
    /// Generates word-level SRT subtitles by aligning a script with audio.
    /// Uses speech recognition to transcribe audio and aligns it with the provided script.
    /// </summary>
    /// <param name="audioPath">Path to the audio file (MP3, WAV, etc.).</param>
    /// <param name="scriptPath">Path to the text script file.</param>
    /// <param name="outputSrtPath">Path where the SRT file should be saved.</param>
    /// <param name="cancellationToken">Cancellation token.</param>
    /// <returns>Subtitle generation result with metadata.</returns>
    Task<SubtitleGenerationResult> GenerateSubtitlesAsync(
        string audioPath,
        string scriptPath,
        string outputSrtPath,
        CancellationToken cancellationToken = default);

    /// <summary>
    /// Processes a story folder by generating subtitles from voiceover and revised script.
    /// Expects folder to contain "voiceover_normalized.mp3" and "Revised.txt".
    /// </summary>
    /// <param name="storyFolderPath">Path to the story folder.</param>
    /// <param name="storyTitle">Title of the story for logging.</param>
    /// <param name="cancellationToken">Cancellation token.</param>
    /// <returns>Subtitle generation result with metadata.</returns>
    Task<SubtitleGenerationResult> GenerateSubtitlesForStoryAsync(
        string storyFolderPath,
        string storyTitle,
        CancellationToken cancellationToken = default);
}
