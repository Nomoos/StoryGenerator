using System.Threading;
using System.Threading.Tasks;

namespace StoryGenerator.Interfaces
{
    /// <summary>
    /// Interface for FFmpeg media processing client.
    /// Defines operations for audio/video manipulation and format conversion.
    /// </summary>
    public interface IFFmpegClient
    {
        /// <summary>
        /// Normalize audio to target LUFS using loudnorm filter.
        /// </summary>
        /// <param name="inputPath">Input audio file path</param>
        /// <param name="outputPath">Output audio file path</param>
        /// <param name="targetLufs">Target integrated loudness in LUFS (typically -14 to -16)</param>
        /// <param name="targetLra">Target loudness range in LU</param>
        /// <param name="targetTp">Target true peak in dBTP</param>
        /// <param name="twoPass">Use two-pass normalization for better accuracy</param>
        /// <param name="sampleRate">Output sample rate in Hz</param>
        /// <param name="cancellationToken">Cancellation token</param>
        /// <returns>Normalization result with metrics</returns>
        Task<NormalizationResult> NormalizeAudioAsync(
            string inputPath,
            string outputPath,
            double targetLufs = -14.0,
            double targetLra = 7.0,
            double targetTp = -1.0,
            bool twoPass = true,
            int sampleRate = 48000,
            CancellationToken cancellationToken = default);

        /// <summary>
        /// Get audio file information using FFprobe.
        /// </summary>
        /// <param name="audioPath">Path to audio file</param>
        /// <param name="cancellationToken">Cancellation token</param>
        /// <returns>Audio file information</returns>
        Task<AudioInfo> GetAudioInfoAsync(
            string audioPath,
            CancellationToken cancellationToken = default);

        /// <summary>
        /// Extract audio from video file.
        /// </summary>
        /// <param name="videoPath">Input video file path</param>
        /// <param name="audioPath">Output audio file path</param>
        /// <param name="codec">Audio codec (e.g., "mp3", "aac", "wav")</param>
        /// <param name="bitrate">Audio bitrate (e.g., "192k")</param>
        /// <param name="cancellationToken">Cancellation token</param>
        Task ExtractAudioAsync(
            string videoPath,
            string audioPath,
            string codec = "mp3",
            string bitrate = "192k",
            CancellationToken cancellationToken = default);

        /// <summary>
        /// Convert video to different format.
        /// </summary>
        /// <param name="inputPath">Input video file path</param>
        /// <param name="outputPath">Output video file path</param>
        /// <param name="codec">Video codec (e.g., "libx264", "libx265")</param>
        /// <param name="preset">Encoding preset (e.g., "medium", "fast")</param>
        /// <param name="crf">Constant Rate Factor (0-51, lower = better quality)</param>
        /// <param name="cancellationToken">Cancellation token</param>
        Task ConvertVideoAsync(
            string inputPath,
            string outputPath,
            string codec = "libx264",
            string preset = "medium",
            int crf = 23,
            CancellationToken cancellationToken = default);
    }
}
