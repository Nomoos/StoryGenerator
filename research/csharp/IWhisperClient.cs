using System.Threading;
using System.Threading.Tasks;

namespace StoryGenerator.Research
{
    /// <summary>
    /// Interface for Whisper ASR (Automatic Speech Recognition) client.
    /// Defines operations for speech-to-text transcription and subtitle generation.
    /// </summary>
    public interface IWhisperClient
    {
        /// <summary>
        /// Transcribe audio file.
        /// </summary>
        /// <param name="audioPath">Path to audio file</param>
        /// <param name="language">Language code (e.g., "en", "es") or null for auto-detection</param>
        /// <param name="task">Task type ("transcribe" or "translate")</param>
        /// <param name="wordTimestamps">Include word-level timestamps</param>
        /// <param name="vadFilter">Apply voice activity detection filter</param>
        /// <param name="cancellationToken">Cancellation token</param>
        /// <returns>Transcription result</returns>
        Task<TranscriptionResult> TranscribeAsync(
            string audioPath,
            string language = null,
            string task = "transcribe",
            bool wordTimestamps = true,
            bool vadFilter = true,
            CancellationToken cancellationToken = default);

        /// <summary>
        /// Transcribe audio and generate SRT subtitle file.
        /// </summary>
        /// <param name="audioPath">Path to audio file</param>
        /// <param name="outputPath">Path to save SRT file</param>
        /// <param name="language">Language code or null for auto-detection</param>
        /// <param name="maxWordsPerLine">Maximum words per subtitle line</param>
        /// <param name="cancellationToken">Cancellation token</param>
        /// <returns>SRT content as string</returns>
        Task<string> TranscribeToSrtAsync(
            string audioPath,
            string outputPath = null,
            string language = null,
            int maxWordsPerLine = 10,
            CancellationToken cancellationToken = default);

        /// <summary>
        /// Detect the language of an audio file.
        /// </summary>
        /// <param name="audioPath">Path to audio file</param>
        /// <param name="cancellationToken">Cancellation token</param>
        /// <returns>Tuple of language code and confidence</returns>
        Task<(string Language, double Confidence)> DetectLanguageAsync(
            string audioPath,
            CancellationToken cancellationToken = default);
    }
}
