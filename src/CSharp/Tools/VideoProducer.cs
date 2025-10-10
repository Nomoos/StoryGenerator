using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading;
using System.Threading.Tasks;
using StoryGenerator.Generators;
using StoryGenerator.Interfaces;
using StoryGenerator.Models;

namespace StoryGenerator.Tools
{
    /// <summary>
    /// Complete video production tool that orchestrates video creation from keyframes,
    /// subtitles, script/text, and audio sources. Combines keyframe video synthesis
    /// with post-production processing.
    /// </summary>
    public class VideoProducer : IVideoProducer
    {
        private readonly IKeyframeVideoSynthesizer? _keyframeSynthesizer;
        private readonly IVideoPostProducer _postProducer;

        /// <summary>
        /// Initialize VideoProducer with optional synthesizer and post-producer.
        /// </summary>
        /// <param name="keyframeSynthesizer">Keyframe video synthesizer (optional, will create default if null)</param>
        /// <param name="postProducer">Video post-producer (optional, will create default if null)</param>
        public VideoProducer(
            IKeyframeVideoSynthesizer? keyframeSynthesizer = null,
            IVideoPostProducer? postProducer = null)
        {
            _keyframeSynthesizer = keyframeSynthesizer;
            _postProducer = postProducer ?? new VideoPostProducer();
        }

        /// <summary>
        /// Produce a complete video from keyframes, subtitles, script/text, and audio sources.
        /// </summary>
        public async Task<VideoProductionResult> ProduceVideoAsync(
            VideoProductionConfig config,
            CancellationToken cancellationToken = default)
        {
            var result = new VideoProductionResult();
            var startTime = DateTime.UtcNow;
            var tempFiles = new List<string>();

            try
            {
                // Validate configuration
                ValidateConfig(config);

                Console.WriteLine("🎬 Starting video production pipeline");
                Console.WriteLine($"   Keyframes: {config.KeyframePaths.Count}");
                Console.WriteLine($"   Duration: {config.DurationSeconds}s");
                Console.WriteLine($"   Output: {config.OutputPath}");

                // Step 1: Generate SRT file from script text if needed
                string? srtPath = config.SrtPath;
                if (string.IsNullOrWhiteSpace(srtPath) && 
                    !string.IsNullOrWhiteSpace(config.ScriptText) &&
                    config.GenerateSubtitlesFromScript)
                {
                    Console.WriteLine("\n📝 Generating subtitles from script text...");
                    srtPath = await GenerateSubtitlesFromScriptAsync(
                        config.ScriptText,
                        config.DurationSeconds,
                        config.WordsPerMinute,
                        cancellationToken);
                    
                    if (!string.IsNullOrWhiteSpace(srtPath))
                    {
                        result.GeneratedSrtPath = srtPath;
                        tempFiles.Add(srtPath);
                        Console.WriteLine($"   ✓ Subtitles generated: {srtPath}");
                    }
                }

                // Step 2: Generate video from keyframes
                Console.WriteLine("\n🎥 Generating video from keyframes...");
                string intermediateVideoPath = Path.Combine(
                    Path.GetTempPath(),
                    $"intermediate_{Guid.NewGuid()}.mp4");

                bool videoGenerated = await GenerateVideoFromKeyframesAsync(
                    config.KeyframePaths,
                    intermediateVideoPath,
                    config.DurationSeconds,
                    config.AudioPath,
                    config.InterpolationMethod,
                    config.Fps,
                    cancellationToken);

                if (!videoGenerated)
                {
                    throw new Exception("Failed to generate video from keyframes");
                }

                result.IntermediateVideoPath = intermediateVideoPath;
                tempFiles.Add(intermediateVideoPath);
                Console.WriteLine($"   ✓ Video generated from keyframes");

                // Step 3: Apply post-production (cropping, subtitles, audio mixing)
                Console.WriteLine("\n🎬 Applying post-production...");
                
                // Ensure output directory exists
                var outputDir = Path.GetDirectoryName(config.OutputPath);
                if (!string.IsNullOrEmpty(outputDir) && !Directory.Exists(outputDir))
                {
                    Directory.CreateDirectory(outputDir);
                }

                var postProductionConfig = new VideoPostProductionConfig
                {
                    SegmentPaths = new List<string> { intermediateVideoPath },
                    OutputPath = config.OutputPath,
                    SrtPath = srtPath,
                    BackgroundMusicPath = config.BackgroundMusicPath,
                    SoundEffectsPaths = config.SoundEffectsPaths,
                    Fps = config.Fps,
                    TargetWidth = config.TargetWidth,
                    TargetHeight = config.TargetHeight,
                    BurnInSubtitles = config.BurnInSubtitles,
                    SafeMargins = config.SafeMargins,
                    MusicVolume = config.MusicVolume,
                    EnableDucking = config.EnableDucking,
                    TransitionType = "none", // Single segment, no transitions needed
                    TransitionDuration = 0,
                    VideoBitrate = config.VideoBitrate,
                    AudioBitrate = config.AudioBitrate,
                    Segment = config.Segment,
                    Age = config.Age,
                    Gender = config.Gender,
                    TitleId = config.TitleId
                };

                var finalPath = await _postProducer.ProduceVideoAsync(
                    postProductionConfig,
                    cancellationToken);

                Console.WriteLine($"   ✓ Post-production complete");

                // Step 4: Gather results
                result.Success = true;
                result.OutputPath = finalPath;
                result.ProcessingTimeSeconds = (DateTime.UtcNow - startTime).TotalSeconds;

                if (File.Exists(finalPath))
                {
                    var fileInfo = new FileInfo(finalPath);
                    result.FileSizeBytes = fileInfo.Length;

                    // Get video duration
                    result.VideoDurationSeconds = await GetVideoDurationAsync(finalPath, cancellationToken);

                    Console.WriteLine($"\n✅ Video production completed successfully!");
                    Console.WriteLine($"   Output: {finalPath}");
                    Console.WriteLine($"   Duration: {result.VideoDurationSeconds:F1}s");
                    Console.WriteLine($"   Size: {result.FileSizeMB:F2} MB");
                    Console.WriteLine($"   Processing time: {result.ProcessingTimeSeconds:F1}s");
                }

                return result;
            }
            catch (Exception ex)
            {
                result.Success = false;
                result.ErrorMessage = ex.Message;
                result.ProcessingTimeSeconds = (DateTime.UtcNow - startTime).TotalSeconds;

                Console.WriteLine($"\n❌ Video production failed: {ex.Message}");
                
                return result;
            }
            finally
            {
                // Clean up temporary files
                foreach (var tempFile in tempFiles)
                {
                    try
                    {
                        if (File.Exists(tempFile))
                            File.Delete(tempFile);
                    }
                    catch
                    {
                        // Ignore cleanup errors
                    }
                }
            }
        }

        /// <summary>
        /// Validate video production configuration.
        /// </summary>
        private void ValidateConfig(VideoProductionConfig config)
        {
            if (config == null)
                throw new ArgumentNullException(nameof(config));

            if (config.KeyframePaths == null || config.KeyframePaths.Count < 2)
                throw new ArgumentException("At least 2 keyframes are required", nameof(config));

            if (config.DurationSeconds <= 0)
                throw new ArgumentException("Duration must be greater than 0", nameof(config));

            if (string.IsNullOrWhiteSpace(config.OutputPath))
                throw new ArgumentException("Output path is required", nameof(config));

            // Validate keyframe files exist
            foreach (var keyframe in config.KeyframePaths)
            {
                if (!File.Exists(keyframe))
                    throw new FileNotFoundException($"Keyframe not found: {keyframe}");
            }

            // Validate optional audio files exist
            if (!string.IsNullOrWhiteSpace(config.AudioPath) && !File.Exists(config.AudioPath))
                throw new FileNotFoundException($"Audio file not found: {config.AudioPath}");

            if (!string.IsNullOrWhiteSpace(config.BackgroundMusicPath) && !File.Exists(config.BackgroundMusicPath))
                throw new FileNotFoundException($"Background music file not found: {config.BackgroundMusicPath}");

            if (!string.IsNullOrWhiteSpace(config.SrtPath) && !File.Exists(config.SrtPath))
                throw new FileNotFoundException($"SRT file not found: {config.SrtPath}");
        }

        /// <summary>
        /// Generate video from keyframes using the keyframe synthesizer.
        /// </summary>
        private async Task<bool> GenerateVideoFromKeyframesAsync(
            List<string> keyframePaths,
            string outputPath,
            double duration,
            string? audioPath,
            string interpolationMethod,
            int fps,
            CancellationToken cancellationToken)
        {
            // If we have a keyframe synthesizer, use it
            if (_keyframeSynthesizer != null)
            {
                return await _keyframeSynthesizer.GenerateFromKeyframesAsync(
                    keyframePaths,
                    outputPath,
                    duration,
                    audioPath);
            }

            // Otherwise, create a simple video from keyframes using FFmpeg
            // This is a fallback when no synthesizer is provided
            return await GenerateVideoFromKeyframesUsingFFmpegAsync(
                keyframePaths,
                outputPath,
                duration,
                audioPath,
                fps,
                cancellationToken);
        }

        /// <summary>
        /// Generate video from keyframes using FFmpeg (fallback method).
        /// Creates a simple slideshow-style video with even frame distribution.
        /// </summary>
        private async Task<bool> GenerateVideoFromKeyframesUsingFFmpegAsync(
            List<string> keyframePaths,
            string outputPath,
            double duration,
            string? audioPath,
            int fps,
            CancellationToken cancellationToken)
        {
            try
            {
                // Calculate duration per keyframe
                double durationPerFrame = duration / keyframePaths.Count;

                // Create a concat demuxer file
                var concatFile = Path.Combine(Path.GetTempPath(), $"concat_{Guid.NewGuid()}.txt");
                var sb = new StringBuilder();
                
                foreach (var keyframe in keyframePaths)
                {
                    sb.AppendLine($"file '{keyframe.Replace("\\", "/")}'");
                    sb.AppendLine($"duration {durationPerFrame:F3}");
                }
                // Add last frame again to ensure it displays
                sb.AppendLine($"file '{keyframePaths.Last().Replace("\\", "/")}'");

                await File.WriteAllTextAsync(concatFile, sb.ToString(), cancellationToken);

                // Build FFmpeg command
                var arguments = new StringBuilder();
                arguments.Append($"-f concat -safe 0 -i \"{concatFile}\" ");
                arguments.Append($"-vf \"fps={fps},scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2\" ");
                
                if (!string.IsNullOrWhiteSpace(audioPath) && File.Exists(audioPath))
                {
                    arguments.Append($"-i \"{audioPath}\" -c:a aac -b:a 192k -shortest ");
                }
                
                arguments.Append($"-c:v libx264 -preset medium -crf 23 -pix_fmt yuv420p ");
                arguments.Append($"-y \"{outputPath}\"");

                // Execute FFmpeg
                var processInfo = new ProcessStartInfo
                {
                    FileName = "ffmpeg",
                    Arguments = arguments.ToString(),
                    RedirectStandardOutput = true,
                    RedirectStandardError = true,
                    UseShellExecute = false,
                    CreateNoWindow = true
                };

                using var process = Process.Start(processInfo);
                if (process == null)
                    return false;

                await process.WaitForExitAsync(cancellationToken);

                // Cleanup concat file
                if (File.Exists(concatFile))
                    File.Delete(concatFile);

                return process.ExitCode == 0 && File.Exists(outputPath);
            }
            catch (Exception ex)
            {
                Console.WriteLine($"   ❌ FFmpeg video generation error: {ex.Message}");
                return false;
            }
        }

        /// <summary>
        /// Generate SRT subtitle file from script text.
        /// Splits text into timed subtitle segments.
        /// </summary>
        private async Task<string?> GenerateSubtitlesFromScriptAsync(
            string scriptText,
            double duration,
            int wordsPerMinute,
            CancellationToken cancellationToken)
        {
            try
            {
                // Split script into sentences
                var sentences = SplitIntoSentences(scriptText);
                if (sentences.Count == 0)
                    return null;

                // Calculate timing for each sentence based on word count
                var words = scriptText.Split(new[] { ' ', '\n', '\r', '\t' }, 
                    StringSplitOptions.RemoveEmptyEntries);
                double totalWords = words.Length;
                double wordsPerSecond = wordsPerMinute / 60.0;
                
                // Generate SRT content
                var srtContent = new StringBuilder();
                double currentTime = 0;
                
                for (int i = 0; i < sentences.Count; i++)
                {
                    var sentence = sentences[i].Trim();
                    if (string.IsNullOrWhiteSpace(sentence))
                        continue;

                    // Calculate duration for this sentence
                    var sentenceWords = sentence.Split(new[] { ' ', '\t' }, 
                        StringSplitOptions.RemoveEmptyEntries).Length;
                    double sentenceDuration = sentenceWords / wordsPerSecond;
                    
                    // Ensure we don't exceed total duration
                    if (currentTime + sentenceDuration > duration)
                    {
                        sentenceDuration = duration - currentTime;
                    }

                    // Format timestamps
                    var startTime = FormatSrtTime(currentTime);
                    var endTime = FormatSrtTime(currentTime + sentenceDuration);

                    // Add SRT entry
                    srtContent.AppendLine($"{i + 1}");
                    srtContent.AppendLine($"{startTime} --> {endTime}");
                    srtContent.AppendLine(sentence);
                    srtContent.AppendLine();

                    currentTime += sentenceDuration;
                    
                    // Stop if we've reached the duration
                    if (currentTime >= duration)
                        break;
                }

                // Save SRT file
                var srtPath = Path.Combine(Path.GetTempPath(), $"subtitles_{Guid.NewGuid()}.srt");
                await File.WriteAllTextAsync(srtPath, srtContent.ToString(), cancellationToken);

                return srtPath;
            }
            catch (Exception ex)
            {
                Console.WriteLine($"   ⚠️ Failed to generate subtitles: {ex.Message}");
                return null;
            }
        }

        /// <summary>
        /// Split text into sentences.
        /// </summary>
        private List<string> SplitIntoSentences(string text)
        {
            // Simple sentence splitting by common punctuation
            var sentences = new List<string>();
            var current = new StringBuilder();
            
            for (int i = 0; i < text.Length; i++)
            {
                current.Append(text[i]);
                
                // Check for sentence endings
                if (text[i] == '.' || text[i] == '!' || text[i] == '?')
                {
                    // Look ahead to ensure it's not an abbreviation
                    if (i + 1 >= text.Length || char.IsWhiteSpace(text[i + 1]))
                    {
                        sentences.Add(current.ToString().Trim());
                        current.Clear();
                    }
                }
            }
            
            // Add remaining text
            if (current.Length > 0)
            {
                sentences.Add(current.ToString().Trim());
            }
            
            return sentences;
        }

        /// <summary>
        /// Format time in seconds to SRT timestamp format (HH:MM:SS,mmm).
        /// </summary>
        private string FormatSrtTime(double seconds)
        {
            var timeSpan = TimeSpan.FromSeconds(seconds);
            return $"{(int)timeSpan.TotalHours:D2}:{timeSpan.Minutes:D2}:{timeSpan.Seconds:D2},{timeSpan.Milliseconds:D3}";
        }

        /// <summary>
        /// Get video duration in seconds using FFprobe.
        /// </summary>
        private async Task<double> GetVideoDurationAsync(
            string videoPath,
            CancellationToken cancellationToken)
        {
            try
            {
                var arguments = $"-v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 \"{videoPath}\"";

                var processInfo = new ProcessStartInfo
                {
                    FileName = "ffprobe",
                    Arguments = arguments,
                    RedirectStandardOutput = true,
                    RedirectStandardError = true,
                    UseShellExecute = false,
                    CreateNoWindow = true
                };

                using var process = Process.Start(processInfo);
                if (process == null)
                    return 0;

                var output = await process.StandardOutput.ReadToEndAsync();
                await process.WaitForExitAsync(cancellationToken);

                if (double.TryParse(output.Trim(), out double duration))
                    return duration;

                return 0;
            }
            catch
            {
                return 0;
            }
        }
    }
}
