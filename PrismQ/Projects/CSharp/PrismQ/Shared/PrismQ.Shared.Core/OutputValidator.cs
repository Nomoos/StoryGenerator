using System;
using System.IO;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.Extensions.Logging;
using PrismQ.Shared.Interfaces;
using PrismQ.Shared.Models;

namespace PrismQ.Shared.Core.Services
{
    /// <summary>
    /// Output quality validation and metrics tracking.
    /// Validates generated files and tracks quality metrics.
    /// Equivalent to Python Tools/Validator.py
    /// </summary>
    public class OutputValidator
    {
        private readonly ILogger<OutputValidator> _logger;
        private readonly IContentFilter? _contentFilter;

        public OutputValidator(ILogger<OutputValidator> logger, IContentFilter? contentFilter = null)
        {
            _logger = logger;
            _contentFilter = contentFilter;
        }

        /// <summary>
        /// Validate an audio file and return metrics.
        /// </summary>
        /// <param name="filePath">Path to audio file</param>
        /// <returns>Tuple of (is_valid, metrics_dict)</returns>
        public (bool IsValid, OutputMetrics Metrics) ValidateAudioFile(string filePath)
        {
            var metrics = new OutputMetrics
            {
                Exists = false,
                SizeBytes = 0,
                SizeMb = 0.0,
                IsValid = false
            };

            if (!File.Exists(filePath))
            {
                _logger.LogWarning("Audio file does not exist: {FilePath}", filePath);
                return (false, metrics);
            }

            metrics.Exists = true;

            try
            {
                var fileInfo = new FileInfo(filePath);
                var sizeBytes = fileInfo.Length;
                metrics.SizeBytes = sizeBytes;
                metrics.SizeMb = Math.Round(sizeBytes / (1024.0 * 1024.0), 2);

                // Basic validation: file should be at least 10KB
                if (sizeBytes < 10240)
                {
                    _logger.LogWarning("Audio file too small ({SizeBytes} bytes): {FilePath}", sizeBytes, filePath);
                    return (false, metrics);
                }

                // Try to get duration and additional metadata using ffprobe if available
                try
                {
                    var duration = GetMediaDuration(filePath);
                    if (duration.HasValue)
                    {
                        metrics.DurationSeconds = Math.Round(duration.Value, 2);

                        // Validate duration (should be at least 5 seconds for a story)
                        if (duration.Value < 5.0)
                        {
                            _logger.LogWarning("Audio too short ({Duration}s): {FilePath}", duration.Value, filePath);
                            return (false, metrics);
                        }
                    }
                }
                catch (Exception ex)
                {
                    _logger.LogWarning("Could not probe audio file: {Message}", ex.Message);
                    // Don't fail validation if probe fails, file might still be valid
                }

                metrics.IsValid = true;
                _logger.LogInformation("✅ Audio file validated: {FilePath} ({SizeMb}MB)", filePath, metrics.SizeMb);
                return (true, metrics);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error validating audio file: {FilePath}", filePath);
                return (false, metrics);
            }
        }

        /// <summary>
        /// Validate a text file (script, subtitles, etc.).
        /// </summary>
        /// <param name="filePath">Path to text file</param>
        /// <param name="minLength">Minimum expected length in characters</param>
        /// <param name="checkDemonetization">Whether to check for demonetized content</param>
        /// <returns>Tuple of (is_valid, metrics_dict)</returns>
        public (bool IsValid, OutputMetrics Metrics) ValidateTextFile(string filePath, int minLength = 100, bool checkDemonetization = false)
        {
            var metrics = new OutputMetrics
            {
                Exists = false,
                SizeBytes = 0,
                CharCount = 0,
                WordCount = 0,
                LineCount = 0,
                IsValid = false
            };

            if (!File.Exists(filePath))
            {
                _logger.LogWarning("Text file does not exist: {FilePath}", filePath);
                return (false, metrics);
            }

            metrics.Exists = true;

            try
            {
                var fileInfo = new FileInfo(filePath);
                metrics.SizeBytes = fileInfo.Length;

                // Read and analyze content
                var content = File.ReadAllText(filePath);
                metrics.CharCount = content.Length;
                metrics.WordCount = content.Split(new[] { ' ', '\n', '\r', '\t' }, StringSplitOptions.RemoveEmptyEntries).Length;
                metrics.LineCount = content.Split('\n').Length;

                // Validate minimum length
                if (metrics.CharCount < minLength)
                {
                    _logger.LogWarning("Text file too short ({CharCount} chars, minimum {MinLength}): {FilePath}",
                        metrics.CharCount, minLength, filePath);
                    return (false, metrics);
                }

                // Check for empty or whitespace-only content
                if (string.IsNullOrWhiteSpace(content))
                {
                    _logger.LogWarning("Text file is empty or whitespace only: {FilePath}", filePath);
                    return (false, metrics);
                }

                // Check for demonetized content if requested and filter is available
                if (checkDemonetization && _contentFilter != null)
                {
                    var filterResult = _contentFilter.CheckContent(content);
                    metrics.ContentFilterResult = filterResult;
                    
                    if (!filterResult.IsClean)
                    {
                        _logger.LogWarning("Content contains {Count} potentially demonetized words/phrases: {FilePath}",
                            filterResult.FlaggedWords.Count, filePath);
                        
                        // Don't fail validation, just warn
                        // This allows the content to proceed but alerts the user
                    }
                }

                metrics.IsValid = true;
                _logger.LogInformation("✅ Text file validated: {FilePath} ({CharCount} chars, {WordCount} words)",
                    filePath, metrics.CharCount, metrics.WordCount);
                return (true, metrics);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error validating text file: {FilePath}", filePath);
                return (false, metrics);
            }
        }

        /// <summary>
        /// Validate a video file.
        /// </summary>
        /// <param name="filePath">Path to video file</param>
        /// <returns>Tuple of (is_valid, metrics_dict)</returns>
        public (bool IsValid, OutputMetrics Metrics) ValidateVideoFile(string filePath)
        {
            var metrics = new OutputMetrics
            {
                Exists = false,
                SizeBytes = 0,
                SizeMb = 0.0,
                IsValid = false
            };

            if (!File.Exists(filePath))
            {
                _logger.LogWarning("Video file does not exist: {FilePath}", filePath);
                return (false, metrics);
            }

            metrics.Exists = true;

            try
            {
                var fileInfo = new FileInfo(filePath);
                var sizeBytes = fileInfo.Length;
                metrics.SizeBytes = sizeBytes;
                metrics.SizeMb = Math.Round(sizeBytes / (1024.0 * 1024.0), 2);

                // Video should be at least 100KB
                if (sizeBytes < 102400)
                {
                    _logger.LogWarning("Video file too small ({SizeBytes} bytes): {FilePath}", sizeBytes, filePath);
                    return (false, metrics);
                }

                // Try to get video metadata
                try
                {
                    var duration = GetMediaDuration(filePath);
                    if (duration.HasValue)
                    {
                        metrics.DurationSeconds = Math.Round(duration.Value, 2);
                    }
                }
                catch (Exception ex)
                {
                    _logger.LogWarning("Could not probe video file: {Message}", ex.Message);
                }

                metrics.IsValid = true;
                _logger.LogInformation("✅ Video file validated: {FilePath} ({SizeMb}MB)", filePath, metrics.SizeMb);
                return (true, metrics);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error validating video file: {FilePath}", filePath);
                return (false, metrics);
            }
        }

        /// <summary>
        /// Validate subtitle sync with audio duration.
        /// </summary>
        /// <param name="audioDuration">Duration of audio in seconds</param>
        /// <param name="subtitleFile">Path to subtitle file</param>
        /// <returns>Tuple of (is_valid, metrics_dict)</returns>
        public (bool IsValid, OutputMetrics Metrics) ValidateSubtitleSync(double audioDuration, string subtitleFile)
        {
            var metrics = new OutputMetrics
            {
                Exists = false,
                IsValid = false
            };

            if (!File.Exists(subtitleFile))
            {
                _logger.LogWarning("Subtitle file does not exist: {FilePath}", subtitleFile);
                return (false, metrics);
            }

            metrics.Exists = true;

            try
            {
                // Read subtitle file
                var content = File.ReadAllText(subtitleFile);

                // Parse last subtitle timing (basic SRT parsing)
                var lines = content.Split('\n');
                double lastEndTime = 0;

                for (int i = 0; i < lines.Length; i++)
                {
                    if (lines[i].Contains("-->"))
                    {
                        var times = lines[i].Split(new[] { "-->" }, StringSplitOptions.None);
                        if (times.Length == 2)
                        {
                            var endTime = ParseSrtTime(times[1].Trim());
                            if (endTime > lastEndTime)
                            {
                                lastEndTime = endTime;
                            }
                        }
                    }
                }

                metrics.DurationSeconds = lastEndTime;

                // Check if subtitle duration is close to audio duration (within 5% tolerance)
                var tolerance = audioDuration * 0.05;
                var diff = Math.Abs(lastEndTime - audioDuration);

                if (diff > tolerance)
                {
                    _logger.LogWarning("Subtitle duration ({SubtitleDuration}s) doesn't match audio duration ({AudioDuration}s)",
                        lastEndTime, audioDuration);
                    return (false, metrics);
                }

                metrics.IsValid = true;
                _logger.LogInformation("✅ Subtitle sync validated: {FilePath}", subtitleFile);
                return (true, metrics);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error validating subtitle sync: {FilePath}", subtitleFile);
                return (false, metrics);
            }
        }

        /// <summary>
        /// Get media duration using ffprobe if available.
        /// </summary>
        private double? GetMediaDuration(string filePath)
        {
            try
            {
                var process = new System.Diagnostics.Process
                {
                    StartInfo = new System.Diagnostics.ProcessStartInfo
                    {
                        FileName = "ffprobe",
                        Arguments = $"-v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 \"{filePath}\"",
                        RedirectStandardOutput = true,
                        RedirectStandardError = true,
                        UseShellExecute = false,
                        CreateNoWindow = true
                    }
                };

                process.Start();
                var output = process.StandardOutput.ReadToEnd();
                process.WaitForExit();

                if (process.ExitCode == 0 && double.TryParse(output.Trim(), out var duration))
                {
                    return duration;
                }
            }
            catch
            {
                // ffprobe not available or failed, return null
            }

            return null;
        }

        /// <summary>
        /// Parse SRT timestamp to seconds.
        /// </summary>
        private double ParseSrtTime(string timeString)
        {
            try
            {
                // Format: HH:MM:SS,mmm
                var parts = timeString.Split(',');
                if (parts.Length != 2) return 0;

                var timeParts = parts[0].Split(':');
                if (timeParts.Length != 3) return 0;

                var hours = int.Parse(timeParts[0]);
                var minutes = int.Parse(timeParts[1]);
                var seconds = int.Parse(timeParts[2]);
                var milliseconds = int.Parse(parts[1]);

                return hours * 3600 + minutes * 60 + seconds + milliseconds / 1000.0;
            }
            catch
            {
                return 0;
            }
        }
    }

    /// <summary>
    /// Metrics for output validation.
    /// </summary>
    public class OutputMetrics
    {
        public bool Exists { get; set; }
        public long SizeBytes { get; set; }
        public double SizeMb { get; set; }
        public int CharCount { get; set; }
        public int WordCount { get; set; }
        public int LineCount { get; set; }
        public double DurationSeconds { get; set; }
        public int Bitrate { get; set; }
        public bool IsValid { get; set; }
        public ContentFilterResult? ContentFilterResult { get; set; }
    }
}
