using System.Collections.Generic;
using System.Threading;
using System.Threading.Tasks;
using StoryGenerator.Models;

namespace StoryGenerator.Interfaces
{
    /// <summary>
    /// Interface for video post-production operations.
    /// Handles cropping, subtitles, background music, and concatenation.
    /// </summary>
    public interface IVideoPostProducer
    {
        /// <summary>
        /// Perform complete post-production on video segments.
        /// </summary>
        /// <param name="config">Post-production configuration</param>
        /// <param name="cancellationToken">Cancellation token</param>
        /// <returns>Path to the final produced video</returns>
        Task<string> ProduceVideoAsync(
            VideoPostProductionConfig config,
            CancellationToken cancellationToken = default);

        /// <summary>
        /// Crop video to 9:16 aspect ratio (1080x1920).
        /// </summary>
        /// <param name="inputPath">Input video file path</param>
        /// <param name="outputPath">Output video file path</param>
        /// <param name="fps">Target frames per second (default: 30)</param>
        /// <param name="cancellationToken">Cancellation token</param>
        Task CropToVerticalAsync(
            string inputPath,
            string outputPath,
            int fps = 30,
            CancellationToken cancellationToken = default);

        /// <summary>
        /// Add subtitles to video from SRT file.
        /// </summary>
        /// <param name="inputPath">Input video file path</param>
        /// <param name="outputPath">Output video file path</param>
        /// <param name="srtPath">SRT subtitle file path</param>
        /// <param name="burnIn">True to burn in subtitles, false for soft subtitles</param>
        /// <param name="safeMargins">Safe margins for text positioning</param>
        /// <param name="cancellationToken">Cancellation token</param>
        Task AddSubtitlesAsync(
            string inputPath,
            string outputPath,
            string srtPath,
            bool burnIn = true,
            SafeTextMargins? safeMargins = null,
            CancellationToken cancellationToken = default);

        /// <summary>
        /// Mix background music with video audio, applying ducking vs voiceover.
        /// </summary>
        /// <param name="inputPath">Input video file path</param>
        /// <param name="outputPath">Output video file path</param>
        /// <param name="musicPath">Background music file path</param>
        /// <param name="musicVolume">Music volume (0.0-1.0, default: 0.2)</param>
        /// <param name="duckingEnabled">Enable ducking during voiceover (default: true)</param>
        /// <param name="cancellationToken">Cancellation token</param>
        Task AddBackgroundMusicAsync(
            string inputPath,
            string outputPath,
            string musicPath,
            double musicVolume = 0.2,
            bool duckingEnabled = true,
            CancellationToken cancellationToken = default);

        /// <summary>
        /// Concatenate multiple video segments with transitions.
        /// </summary>
        /// <param name="segmentPaths">List of video segment file paths</param>
        /// <param name="outputPath">Output concatenated video file path</param>
        /// <param name="transitionType">Type of transition (fade, xfade, none)</param>
        /// <param name="transitionDuration">Duration of transitions in seconds</param>
        /// <param name="cancellationToken">Cancellation token</param>
        Task ConcatenateVideosAsync(
            List<string> segmentPaths,
            string outputPath,
            string transitionType = "fade",
            double transitionDuration = 0.5,
            CancellationToken cancellationToken = default);
    }
}
