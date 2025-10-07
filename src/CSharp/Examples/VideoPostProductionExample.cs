using System;
using System.Collections.Generic;
using System.IO;
using System.Threading.Tasks;
using StoryGenerator.Models;
using StoryGenerator.Tools;

namespace StoryGenerator.Examples
{
    /// <summary>
    /// Example demonstrating video post-production workflow.
    /// Shows how to crop, add subtitles, mix audio, and concatenate videos.
    /// </summary>
    public class VideoPostProductionExample
    {
        /// <summary>
        /// Main example entry point.
        /// </summary>
        public static async Task Main(string[] args)
        {
            Console.WriteLine("Video Post-Production Example");
            Console.WriteLine("==============================\n");

            try
            {
                await RunCompletePostProductionExample();
                await RunIndividualOperationsExample();
            }
            catch (Exception ex)
            {
                Console.WriteLine($"Error: {ex.Message}");
                Console.WriteLine($"Stack trace: {ex.StackTrace}");
            }

            Console.WriteLine("\nExample completed. Press any key to exit...");
            Console.ReadKey();
        }

        /// <summary>
        /// Example of complete post-production pipeline.
        /// </summary>
        private static async Task RunCompletePostProductionExample()
        {
            Console.WriteLine("Example 1: Complete Post-Production Pipeline");
            Console.WriteLine("---------------------------------------------\n");

            var producer = new VideoPostProducer();

            // Configure post-production
            var config = new VideoPostProductionConfig
            {
                // Input segments to process
                SegmentPaths = new List<string>
                {
                    "videos/segment_1.mp4",
                    "videos/segment_2.mp4",
                    "videos/segment_3.mp4"
                },

                // Output path following the required format
                // /final/{segment}/{age}/{title_id}_draft.mp4
                Segment = "tech",
                Age = "18-23",
                Gender = "men",
                TitleId = "ai_revolution_2024",
                OutputPath = "final/tech/18-23/ai_revolution_2024_draft.mp4",

                // Subtitle configuration
                SrtPath = "subtitles/ai_revolution_2024.srt",
                BurnInSubtitles = true,
                SafeMargins = new SafeTextMargins
                {
                    Top = 100,
                    Bottom = 150,
                    Left = 50,
                    Right = 50
                },

                // Audio configuration
                BackgroundMusicPath = "audio/bgm/tech_ambient.mp3",
                MusicVolume = 0.2,
                EnableDucking = true,

                // Video specifications
                Fps = 30,
                TargetWidth = 1080,
                TargetHeight = 1920,
                VideoBitrate = "8M",
                AudioBitrate = "192k",

                // Transition configuration
                TransitionType = "fade",
                TransitionDuration = 0.5
            };

            Console.WriteLine($"Processing {config.SegmentPaths.Count} video segments...");
            Console.WriteLine($"Output: {config.OutputPath}");
            Console.WriteLine($"Target: {config.TargetWidth}x{config.TargetHeight} @ {config.Fps}fps");
            Console.WriteLine($"Subtitles: {(string.IsNullOrEmpty(config.SrtPath) ? "None" : "Yes (burn-in)")}");
            Console.WriteLine($"Background Music: {(string.IsNullOrEmpty(config.BackgroundMusicPath) ? "None" : "Yes (with ducking)")}");
            Console.WriteLine();

            var startTime = DateTime.UtcNow;

            try
            {
                var outputPath = await producer.ProduceVideoAsync(config);
                var processingTime = (DateTime.UtcNow - startTime).TotalSeconds;

                Console.WriteLine($"✓ Post-production completed successfully!");
                Console.WriteLine($"  Output: {outputPath}");
                Console.WriteLine($"  Processing time: {processingTime:F1} seconds");
                
                if (File.Exists(outputPath))
                {
                    var fileInfo = new FileInfo(outputPath);
                    Console.WriteLine($"  File size: {fileInfo.Length / (1024.0 * 1024.0):F2} MB");
                }
                Console.WriteLine();
            }
            catch (Exception ex)
            {
                Console.WriteLine($"✗ Post-production failed: {ex.Message}");
                Console.WriteLine();
            }
        }

        /// <summary>
        /// Example of individual post-production operations.
        /// </summary>
        private static async Task RunIndividualOperationsExample()
        {
            Console.WriteLine("Example 2: Individual Post-Production Operations");
            Console.WriteLine("------------------------------------------------\n");

            var producer = new VideoPostProducer();

            // Example 2.1: Crop video to vertical format
            Console.WriteLine("2.1. Cropping video to 9:16 aspect ratio...");
            try
            {
                var inputVideo = "videos/raw_video.mp4";
                var outputVideo = "videos/vertical_video.mp4";

                await producer.CropToVerticalAsync(inputVideo, outputVideo, fps: 30);
                Console.WriteLine($"  ✓ Video cropped: {outputVideo}");
            }
            catch (Exception ex)
            {
                Console.WriteLine($"  ✗ Crop failed: {ex.Message}");
            }
            Console.WriteLine();

            // Example 2.2: Add subtitles
            Console.WriteLine("2.2. Adding subtitles to video...");
            try
            {
                var inputVideo = "videos/vertical_video.mp4";
                var outputVideo = "videos/subtitled_video.mp4";
                var srtFile = "subtitles/video.srt";

                var safeMargins = new SafeTextMargins
                {
                    Top = 100,
                    Bottom = 150,
                    Left = 50,
                    Right = 50
                };

                await producer.AddSubtitlesAsync(
                    inputVideo,
                    outputVideo,
                    srtFile,
                    burnIn: true,
                    safeMargins: safeMargins);

                Console.WriteLine($"  ✓ Subtitles added: {outputVideo}");
            }
            catch (Exception ex)
            {
                Console.WriteLine($"  ✗ Subtitle addition failed: {ex.Message}");
            }
            Console.WriteLine();

            // Example 2.3: Add background music with ducking
            Console.WriteLine("2.3. Adding background music with ducking...");
            try
            {
                var inputVideo = "videos/subtitled_video.mp4";
                var outputVideo = "videos/final_video.mp4";
                var musicFile = "audio/bgm/background_music.mp3";

                await producer.AddBackgroundMusicAsync(
                    inputVideo,
                    outputVideo,
                    musicFile,
                    musicVolume: 0.2,
                    duckingEnabled: true);

                Console.WriteLine($"  ✓ Background music added: {outputVideo}");
            }
            catch (Exception ex)
            {
                Console.WriteLine($"  ✗ Music addition failed: {ex.Message}");
            }
            Console.WriteLine();

            // Example 2.4: Concatenate multiple videos
            Console.WriteLine("2.4. Concatenating video segments...");
            try
            {
                var segments = new List<string>
                {
                    "videos/intro.mp4",
                    "videos/main.mp4",
                    "videos/outro.mp4"
                };
                var outputVideo = "videos/concatenated.mp4";

                await producer.ConcatenateVideosAsync(
                    segments,
                    outputVideo,
                    transitionType: "fade",
                    transitionDuration: 0.5);

                Console.WriteLine($"  ✓ Videos concatenated: {outputVideo}");
            }
            catch (Exception ex)
            {
                Console.WriteLine($"  ✗ Concatenation failed: {ex.Message}");
            }
            Console.WriteLine();
        }

        /// <summary>
        /// Example configuration for different age groups and segments.
        /// </summary>
        private static void ShowConfigurationExamples()
        {
            Console.WriteLine("Configuration Examples for Different Demographics");
            Console.WriteLine("------------------------------------------------\n");

            // Example 1: Teen girls (10-13)
            var teenGirlsConfig = new VideoPostProductionConfig
            {
                Segment = "lifestyle",
                Age = "10-13",
                Gender = "women",
                TitleId = "morning_routine_tips",
                OutputPath = "final/lifestyle/10-13/morning_routine_tips_draft.mp4",
                Fps = 30,
                BurnInSubtitles = true,
                MusicVolume = 0.25,
                TransitionType = "fade"
            };
            Console.WriteLine("Teen Girls (10-13) - Lifestyle Content:");
            Console.WriteLine($"  Output: {teenGirlsConfig.OutputPath}");
            Console.WriteLine($"  Music Volume: {teenGirlsConfig.MusicVolume * 100}%");
            Console.WriteLine();

            // Example 2: Young adult men (18-23)
            var youngMenConfig = new VideoPostProductionConfig
            {
                Segment = "gaming",
                Age = "18-23",
                Gender = "men",
                TitleId = "top_gaming_strategies",
                OutputPath = "final/gaming/18-23/top_gaming_strategies_draft.mp4",
                Fps = 30,
                BurnInSubtitles = true,
                MusicVolume = 0.15,
                TransitionType = "xfade"
            };
            Console.WriteLine("Young Adult Men (18-23) - Gaming Content:");
            Console.WriteLine($"  Output: {youngMenConfig.OutputPath}");
            Console.WriteLine($"  Transition: {youngMenConfig.TransitionType}");
            Console.WriteLine();

            // Example 3: Adult women (24-30)
            var adultWomenConfig = new VideoPostProductionConfig
            {
                Segment = "wellness",
                Age = "24-30",
                Gender = "women",
                TitleId = "mindfulness_practices",
                OutputPath = "final/wellness/24-30/mindfulness_practices_draft.mp4",
                Fps = 30,
                BurnInSubtitles = true,
                MusicVolume = 0.2,
                EnableDucking = true
            };
            Console.WriteLine("Adult Women (24-30) - Wellness Content:");
            Console.WriteLine($"  Output: {adultWomenConfig.OutputPath}");
            Console.WriteLine($"  Audio Ducking: {(adultWomenConfig.EnableDucking ? "Enabled" : "Disabled")}");
            Console.WriteLine();
        }
    }
}
