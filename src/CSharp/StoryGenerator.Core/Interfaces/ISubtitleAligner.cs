using System.Threading;
using System.Threading.Tasks;

namespace StoryGenerator.Core.Interfaces
{
    /// <summary>
    /// Interface for aligning subtitles to audio and mapping them to shots/scenes.
    /// Uses faster-whisper for forced alignment with word-level timestamps.
    /// </summary>
    public interface ISubtitleAligner
    {
        /// <summary>
        /// Generates aligned subtitles from audio file using forced alignment.
        /// </summary>
        /// <param name="audioPath">Path to the audio file.</param>
        /// <param name="language">Language code (e.g., "en", "es") or null for auto-detection.</param>
        /// <param name="maxWordsPerLine">Maximum words per subtitle line.</param>
        /// <param name="cancellationToken">Cancellation token.</param>
        /// <returns>Subtitle content in SRT format with word-level alignment.</returns>
        Task<string> GenerateAlignedSubtitlesAsync(
            string audioPath,
            string? language = null,
            int maxWordsPerLine = 10,
            CancellationToken cancellationToken = default);

        /// <summary>
        /// Generates aligned SRT file and saves it to the specified path.
        /// </summary>
        /// <param name="audioPath">Path to the audio file.</param>
        /// <param name="outputPath">Path to save the SRT file.</param>
        /// <param name="language">Language code or null for auto-detection.</param>
        /// <param name="maxWordsPerLine">Maximum words per subtitle line.</param>
        /// <param name="cancellationToken">Cancellation token.</param>
        /// <returns>Path to the saved SRT file.</returns>
        Task<string> GenerateAndSaveSrtAsync(
            string audioPath,
            string outputPath,
            string? language = null,
            int maxWordsPerLine = 10,
            CancellationToken cancellationToken = default);

        /// <summary>
        /// Generates aligned VTT file and saves it to the specified path.
        /// </summary>
        /// <param name="audioPath">Path to the audio file.</param>
        /// <param name="outputPath">Path to save the VTT file.</param>
        /// <param name="language">Language code or null for auto-detection.</param>
        /// <param name="maxWordsPerLine">Maximum words per subtitle line.</param>
        /// <param name="cancellationToken">Cancellation token.</param>
        /// <returns>Path to the saved VTT file.</returns>
        Task<string> GenerateAndSaveVttAsync(
            string audioPath,
            string outputPath,
            string? language = null,
            int maxWordsPerLine = 10,
            CancellationToken cancellationToken = default);

        /// <summary>
        /// Maps subtitle time ranges to shot IDs from a shotlist.
        /// </summary>
        /// <param name="audioPath">Path to the audio file.</param>
        /// <param name="shotlist">The shotlist containing shot timing information.</param>
        /// <param name="titleId">The title/story ID for the mapping.</param>
        /// <param name="language">Language code or null for auto-detection.</param>
        /// <param name="maxWordsPerLine">Maximum words per subtitle line.</param>
        /// <param name="cancellationToken">Cancellation token.</param>
        /// <returns>Mapping of subtitles to shot IDs.</returns>
        Task<Models.SubtitleToShotMapping> MapSubtitlesToShotsAsync(
            string audioPath,
            Shotlist shotlist,
            string titleId,
            string? language = null,
            int maxWordsPerLine = 10,
            CancellationToken cancellationToken = default);

        /// <summary>
        /// Maps subtitle time ranges to shot IDs and saves the mapping as JSON.
        /// </summary>
        /// <param name="audioPath">Path to the audio file.</param>
        /// <param name="shotlist">The shotlist containing shot timing information.</param>
        /// <param name="titleId">The title/story ID for the mapping.</param>
        /// <param name="outputPath">Path to save the JSON mapping file.</param>
        /// <param name="language">Language code or null for auto-detection.</param>
        /// <param name="maxWordsPerLine">Maximum words per subtitle line.</param>
        /// <param name="cancellationToken">Cancellation token.</param>
        /// <returns>Path to the saved JSON file.</returns>
        Task<string> MapAndSaveSubtitlesToShotsAsync(
            string audioPath,
            Shotlist shotlist,
            string titleId,
            string outputPath,
            string? language = null,
            int maxWordsPerLine = 10,
            CancellationToken cancellationToken = default);
    }
}
