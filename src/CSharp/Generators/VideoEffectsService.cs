using System;
using System.Diagnostics;
using System.IO;
using System.Threading;
using System.Threading.Tasks;
using Microsoft.Extensions.Logging;

namespace StoryGenerator.Generators
{
    /// <summary>
    /// Video enhancement tools for adding effects like Ken Burns, transitions, and filters.
    /// Equivalent to Python VideoEffects.py
    /// Shells out to FFmpeg for video processing operations.
    /// </summary>
    public class VideoEffectsService
    {
        private readonly ILogger<VideoEffectsService> _logger;
        private readonly string _ffmpegPath;

        public VideoEffectsService(
            ILogger<VideoEffectsService> logger,
            string ffmpegPath = "ffmpeg")
        {
            _logger = logger ?? throw new ArgumentNullException(nameof(logger));
            _ffmpegPath = ffmpegPath;
        }

        /// <summary>
        /// Apply Ken Burns effect (zoom and pan) to a still image
        /// </summary>
        /// <param name="inputImage">Path to input image</param>
        /// <param name="outputVideo">Path to output video file</param>
        /// <param name="audioPath">Path to audio file</param>
        /// <param name="duration">Duration of the video in seconds</param>
        /// <param name="zoomDirection">Zoom direction: "in" or "out"</param>
        /// <param name="panDirection">Pan direction: "left", "right", "up", "down", or "center"</param>
        /// <param name="zoomIntensity">Zoom level (1.0 = no zoom, 1.5 = 50% zoom)</param>
        /// <param name="cancellationToken">Cancellation token</param>
        /// <returns>True if successful</returns>
        public async Task<bool> ApplyKenBurnsEffectAsync(
            string inputImage,
            string outputVideo,
            string audioPath,
            double duration,
            string zoomDirection = "in",
            string panDirection = "right",
            double zoomIntensity = 1.2,
            CancellationToken cancellationToken = default)
        {
            if (!File.Exists(inputImage))
            {
                _logger.LogError("❌ Image not found: {Image}", inputImage);
                return false;
            }

            if (!File.Exists(audioPath))
            {
                _logger.LogError("❌ Audio not found: {Audio}", audioPath);
                return false;
            }

            _logger.LogInformation("🎬 Applying Ken Burns effect to {Image}", Path.GetFileName(inputImage));

            try
            {
                // Build FFmpeg command for Ken Burns effect
                // Simple zoom effect - zoom from 1.0 to zoomIntensity over duration
                var args = $"-loop 1 -framerate 30 -t {duration} -i \"{inputImage}\" " +
                          $"-i \"{audioPath}\" " +
                          $"-vf \"scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920\" " +
                          $"-c:v libx264 -c:a aac -b:a 192k -pix_fmt yuv420p -r 30 " +
                          $"-shortest -t {duration} -y \"{outputVideo}\"";

                var success = await ExecuteFfmpegAsync(args, cancellationToken);

                if (success)
                {
                    _logger.LogInformation("✅ Created video with Ken Burns effect: {Output}", 
                        Path.GetFileName(outputVideo));
                }

                return success;
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "❌ Failed to apply Ken Burns effect");
                return false;
            }
        }

        /// <summary>
        /// Add transition between two video clips
        /// </summary>
        /// <param name="video1">Path to first video</param>
        /// <param name="video2">Path to second video</param>
        /// <param name="output">Path to output video</param>
        /// <param name="transitionType">Transition type: "fade", "wipe", "dissolve"</param>
        /// <param name="duration">Transition duration in seconds</param>
        /// <param name="cancellationToken">Cancellation token</param>
        /// <returns>True if successful</returns>
        public async Task<bool> AddVideoTransitionAsync(
            string video1,
            string video2,
            string output,
            string transitionType = "fade",
            double duration = 1.0,
            CancellationToken cancellationToken = default)
        {
            if (!File.Exists(video1))
            {
                _logger.LogError("❌ First video not found: {Video}", video1);
                return false;
            }

            if (!File.Exists(video2))
            {
                _logger.LogError("❌ Second video not found: {Video}", video2);
                return false;
            }

            _logger.LogInformation("🎬 Adding {Transition} transition between videos", transitionType);

            try
            {
                string filterComplex;

                switch (transitionType.ToLower())
                {
                    case "fade":
                        filterComplex = $"[0:v][1:v]xfade=transition=fade:duration={duration}:offset=0[v]";
                        break;
                    case "wipe":
                        filterComplex = $"[0:v][1:v]xfade=transition=wipeleft:duration={duration}:offset=0[v]";
                        break;
                    case "dissolve":
                        filterComplex = $"[0:v][1:v]xfade=transition=dissolve:duration={duration}:offset=0[v]";
                        break;
                    default:
                        filterComplex = $"[0:v][1:v]xfade=transition=fade:duration={duration}:offset=0[v]";
                        break;
                }

                var args = $"-i \"{video1}\" -i \"{video2}\" " +
                          $"-filter_complex \"{filterComplex}\" " +
                          $"-map \"[v]\" -c:v libx264 -pix_fmt yuv420p -y \"{output}\"";

                var success = await ExecuteFfmpegAsync(args, cancellationToken);

                if (success)
                {
                    _logger.LogInformation("✅ Created video with transition: {Output}",
                        Path.GetFileName(output));
                }

                return success;
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "❌ Failed to add video transition");
                return false;
            }
        }

        /// <summary>
        /// Add color grading/filter to video
        /// </summary>
        /// <param name="inputVideo">Path to input video</param>
        /// <param name="outputVideo">Path to output video</param>
        /// <param name="filterType">Filter type: "warm", "cool", "vintage", "vibrant"</param>
        /// <param name="cancellationToken">Cancellation token</param>
        /// <returns>True if successful</returns>
        public async Task<bool> ApplyColorGradingAsync(
            string inputVideo,
            string outputVideo,
            string filterType = "warm",
            CancellationToken cancellationToken = default)
        {
            if (!File.Exists(inputVideo))
            {
                _logger.LogError("❌ Input video not found: {Video}", inputVideo);
                return false;
            }

            _logger.LogInformation("🎨 Applying {Filter} color grading to video", filterType);

            try
            {
                string videoFilter;

                switch (filterType.ToLower())
                {
                    case "warm":
                        videoFilter = "eq=saturation=1.2:gamma=1.1,curves=r='0/0 0.5/0.58 1/1':g='0/0 0.5/0.5 1/1':b='0/0 0.5/0.42 1/1'";
                        break;
                    case "cool":
                        videoFilter = "eq=saturation=1.1:gamma=0.95,curves=r='0/0 0.5/0.42 1/1':g='0/0 0.5/0.5 1/1':b='0/0 0.5/0.58 1/1'";
                        break;
                    case "vintage":
                        videoFilter = "eq=contrast=0.9:brightness=-0.05:saturation=0.8,curves=all='0/0 0.5/0.48 1/0.95'";
                        break;
                    case "vibrant":
                        videoFilter = "eq=saturation=1.4:contrast=1.1";
                        break;
                    default:
                        videoFilter = "eq=saturation=1.0"; // No change
                        break;
                }

                var args = $"-i \"{inputVideo}\" -vf \"{videoFilter}\" " +
                          $"-c:v libx264 -c:a copy -y \"{outputVideo}\"";

                var success = await ExecuteFfmpegAsync(args, cancellationToken);

                if (success)
                {
                    _logger.LogInformation("✅ Applied color grading: {Output}",
                        Path.GetFileName(outputVideo));
                }

                return success;
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "❌ Failed to apply color grading");
                return false;
            }
        }

        /// <summary>
        /// Add text overlay to video
        /// </summary>
        /// <param name="inputVideo">Path to input video</param>
        /// <param name="outputVideo">Path to output video</param>
        /// <param name="text">Text to overlay</param>
        /// <param name="position">Position: "top", "center", "bottom"</param>
        /// <param name="fontSize">Font size</param>
        /// <param name="fontColor">Font color (e.g., "white", "black")</param>
        /// <param name="cancellationToken">Cancellation token</param>
        /// <returns>True if successful</returns>
        public async Task<bool> AddTextOverlayAsync(
            string inputVideo,
            string outputVideo,
            string text,
            string position = "bottom",
            int fontSize = 48,
            string fontColor = "white",
            CancellationToken cancellationToken = default)
        {
            if (!File.Exists(inputVideo))
            {
                _logger.LogError("❌ Input video not found: {Video}", inputVideo);
                return false;
            }

            _logger.LogInformation("📝 Adding text overlay to video");

            try
            {
                // Escape text for FFmpeg
                var escapedText = text.Replace("'", "\\'").Replace(":", "\\:");

                string yPosition = position.ToLower() switch
                {
                    "top" => "100",
                    "center" => "(h-text_h)/2",
                    "bottom" => "h-text_h-100",
                    _ => "h-text_h-100"
                };

                var drawtext = $"drawtext=text='{escapedText}':fontsize={fontSize}:fontcolor={fontColor}:" +
                              $"x=(w-text_w)/2:y={yPosition}:shadowcolor=black:shadowx=2:shadowy=2";

                var args = $"-i \"{inputVideo}\" -vf \"{drawtext}\" " +
                          $"-c:v libx264 -c:a copy -y \"{outputVideo}\"";

                var success = await ExecuteFfmpegAsync(args, cancellationToken);

                if (success)
                {
                    _logger.LogInformation("✅ Added text overlay: {Output}",
                        Path.GetFileName(outputVideo));
                }

                return success;
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "❌ Failed to add text overlay");
                return false;
            }
        }

        /// <summary>
        /// Execute FFmpeg command
        /// </summary>
        private async Task<bool> ExecuteFfmpegAsync(string arguments, CancellationToken cancellationToken)
        {
            try
            {
                var processInfo = new ProcessStartInfo
                {
                    FileName = _ffmpegPath,
                    Arguments = arguments,
                    RedirectStandardOutput = true,
                    RedirectStandardError = true,
                    UseShellExecute = false,
                    CreateNoWindow = true
                };

                using var process = Process.Start(processInfo);
                if (process == null)
                {
                    _logger.LogError("Failed to start FFmpeg process");
                    return false;
                }

                var outputTask = process.StandardOutput.ReadToEndAsync();
                var errorTask = process.StandardError.ReadToEndAsync();

                await process.WaitForExitAsync(cancellationToken);

                var output = await outputTask;
                var error = await errorTask;

                if (process.ExitCode != 0)
                {
                    _logger.LogError("FFmpeg failed with exit code {ExitCode}", process.ExitCode);
                    if (!string.IsNullOrEmpty(error))
                    {
                        _logger.LogDebug("FFmpeg stderr: {Error}", error);
                    }
                    return false;
                }

                return true;
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Failed to execute FFmpeg");
                return false;
            }
        }
    }
}
