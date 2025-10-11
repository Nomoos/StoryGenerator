using System;
using System.Collections.Generic;
using System.IO;
using System.Threading.Tasks;
using StoryGenerator.Models;
using StoryGenerator.Tools;

namespace StoryGenerator.Examples
{
    /// <summary>
    /// Example demonstrating complete video production from keyframes, subtitles, 
    /// script/text, and audio sources.
    /// </summary>
    public class VideoProductionExample
    {
        /// <summary>
        /// Main example entry point.
        /// </summary>
        public static async Task Main(string[] args)
        {
            Console.WriteLine("Video Production from Keyframes, Subtitles, and Script Example");
            Console.WriteLine("===============================================================\n");

            try
            {
                await RunCompleteVideoProductionExample();
                await RunVideoProductionWithScriptExample();
                await RunVideoProductionWithMinimalConfigExample();
                await RunCameraMotionExamples();
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
        /// Example 1: Complete video production with all features.
        /// </summary>
        private static async Task RunCompleteVideoProductionExample()
        {
            Console.WriteLine("Example 1: Complete Video Production Pipeline");
            Console.WriteLine("----------------------------------------------\n");

            var producer = new VideoProducer();

            // Configure video production
            var config = new VideoProductionConfig
            {
                // Input keyframes (at least 2 required)
                KeyframePaths = new List<string>
                {
                    "keyframes/frame_001.png",
                    "keyframes/frame_002.png",
                    "keyframes/frame_003.png",
                    "keyframes/frame_004.png",
                    "keyframes/frame_005.png"
                },

                // Video duration
                DurationSeconds = 60.0,

                // Output path following the required format
                // /final/{segment}/{age}/{title_id}_draft.mp4
                Segment = "tech",
                Age = "18-23",
                Gender = "men",
                TitleId = "ai_future_2024",
                OutputPath = "final/tech/18-23/ai_future_2024_draft.mp4",

                // Subtitle configuration
                SrtPath = "subtitles/ai_future_2024.srt",
                BurnInSubtitles = true,
                SafeMargins = new SafeTextMargins
                {
                    Top = 100,
                    Bottom = 150,
                    Left = 50,
                    Right = 50
                },

                // Audio configuration
                AudioPath = "audio/voiceover/ai_future_narration.mp3",
                BackgroundMusicPath = "audio/bgm/tech_ambient.mp3",
                MusicVolume = 0.2,
                EnableDucking = true,

                // Video specifications
                Fps = 30,
                TargetWidth = 1080,
                TargetHeight = 1920,
                VideoBitrate = "8M",
                AudioBitrate = "192k",

                // Frame interpolation
                InterpolationMethod = "RIFE",

                // Cinematic camera motion
                EnableCameraMotion = true,
                CameraMotion = CameraMotionType.Dynamic,
                CameraMotionIntensity = 0.3
            };

            Console.WriteLine($"Producing video from {config.KeyframePaths.Count} keyframes...");
            Console.WriteLine($"Duration: {config.DurationSeconds}s");
            Console.WriteLine($"Output: {config.OutputPath}");
            Console.WriteLine($"Target: {config.TargetWidth}x{config.TargetHeight} @ {config.Fps}fps");
            Console.WriteLine();

            var result = await producer.ProduceVideoAsync(config);

            if (result.Success)
            {
                Console.WriteLine($"\n✅ Video production successful!");
                Console.WriteLine($"   Output: {result.OutputPath}");
                Console.WriteLine($"   Duration: {result.VideoDurationSeconds:F1}s");
                Console.WriteLine($"   Size: {result.FileSizeMB:F2} MB");
                Console.WriteLine($"   Processing time: {result.ProcessingTimeSeconds:F1}s");
            }
            else
            {
                Console.WriteLine($"\n❌ Video production failed: {result.ErrorMessage}");
            }
            Console.WriteLine();
        }

        /// <summary>
        /// Example 2: Video production with script text (auto-generate subtitles).
        /// </summary>
        private static async Task RunVideoProductionWithScriptExample()
        {
            Console.WriteLine("Example 2: Video Production with Script Text");
            Console.WriteLine("--------------------------------------------\n");

            var producer = new VideoProducer();

            // Sample script text
            var scriptText = @"
                Artificial intelligence is transforming our world. 
                From healthcare to transportation, AI is making a difference. 
                Machine learning algorithms analyze vast amounts of data. 
                They help doctors diagnose diseases more accurately. 
                Self-driving cars use AI to navigate safely. 
                Natural language models like GPT understand human language. 
                The future of AI holds incredible possibilities. 
                But we must develop it responsibly and ethically.
            ";

            var config = new VideoProductionConfig
            {
                KeyframePaths = new List<string>
                {
                    "keyframes/ai/frame_001.png",
                    "keyframes/ai/frame_002.png",
                    "keyframes/ai/frame_003.png"
                },

                DurationSeconds = 45.0,

                // Use script text instead of SRT file
                ScriptText = scriptText,
                GenerateSubtitlesFromScript = true,
                WordsPerMinute = 150,

                Segment = "education",
                Age = "14-17",
                TitleId = "ai_introduction",
                OutputPath = "final/education/14-17/ai_introduction_draft.mp4",

                AudioPath = "audio/voiceover/ai_intro.mp3",
                BackgroundMusicPath = "audio/bgm/educational.mp3",
                MusicVolume = 0.15,
                EnableDucking = true,

                BurnInSubtitles = true,
                Fps = 30
            };

            Console.WriteLine("Producing video with auto-generated subtitles from script...");
            Console.WriteLine($"Script length: {scriptText.Length} characters");
            Console.WriteLine();

            var result = await producer.ProduceVideoAsync(config);

            if (result.Success)
            {
                Console.WriteLine($"\n✅ Video production successful!");
                Console.WriteLine($"   Output: {result.OutputPath}");
                Console.WriteLine($"   Generated SRT: {result.GeneratedSrtPath}");
                Console.WriteLine($"   Duration: {result.VideoDurationSeconds:F1}s");
                Console.WriteLine($"   Processing time: {result.ProcessingTimeSeconds:F1}s");
            }
            else
            {
                Console.WriteLine($"\n❌ Video production failed: {result.ErrorMessage}");
            }
            Console.WriteLine();
        }

        /// <summary>
        /// Example 3: Minimal video production (keyframes only).
        /// </summary>
        private static async Task RunVideoProductionWithMinimalConfigExample()
        {
            Console.WriteLine("Example 3: Minimal Video Production");
            Console.WriteLine("-----------------------------------\n");

            var producer = new VideoProducer();

            var config = new VideoProductionConfig
            {
                // Minimal configuration - just keyframes and output
                KeyframePaths = new List<string>
                {
                    "keyframes/simple/frame_001.png",
                    "keyframes/simple/frame_002.png"
                },

                DurationSeconds = 10.0,
                OutputPath = "output/simple_video.mp4"
            };

            Console.WriteLine("Producing simple video from keyframes only...");
            Console.WriteLine($"Keyframes: {config.KeyframePaths.Count}");
            Console.WriteLine();

            var result = await producer.ProduceVideoAsync(config);

            if (result.Success)
            {
                Console.WriteLine($"\n✅ Video production successful!");
                Console.WriteLine($"   Output: {result.OutputPath}");
                Console.WriteLine($"   Processing time: {result.ProcessingTimeSeconds:F1}s");
            }
            else
            {
                Console.WriteLine($"\n❌ Video production failed: {result.ErrorMessage}");
            }
            Console.WriteLine();
        }

        /// <summary>
        /// Example 4: Cinematic camera motion demonstrations.
        /// </summary>
        private static async Task RunCameraMotionExamples()
        {
            Console.WriteLine("Example 4: Cinematic Camera Motion");
            Console.WriteLine("-----------------------------------\n");

            var producer = new VideoProducer();

            // Example 4.1: Ken Burns effect (zoom and pan)
            Console.WriteLine("4.1. Ken Burns Effect (Zoom and Pan)");
            try
            {
                var config = new VideoProductionConfig
                {
                    KeyframePaths = new List<string>
                    {
                        "keyframes/landscape_001.png",
                        "keyframes/landscape_002.png",
                        "keyframes/landscape_003.png"
                    },
                    DurationSeconds = 20.0,
                    OutputPath = "output/ken_burns_effect.mp4",
                    
                    // Ken Burns style motion
                    EnableCameraMotion = true,
                    CameraMotion = CameraMotionType.ZoomAndPan,
                    CameraMotionIntensity = 0.4
                };

                var result = await producer.ProduceVideoAsync(config);
                if (result.Success)
                    Console.WriteLine($"  ✓ Ken Burns video: {result.OutputPath}");
                else
                    Console.WriteLine($"  ✗ Failed: {result.ErrorMessage}");
            }
            catch (Exception ex)
            {
                Console.WriteLine($"  ✗ Error: {ex.Message}");
            }
            Console.WriteLine();

            // Example 4.2: Slow zoom in
            Console.WriteLine("4.2. Slow Zoom In Effect");
            try
            {
                var config = new VideoProductionConfig
                {
                    KeyframePaths = new List<string>
                    {
                        "keyframes/portrait_001.png",
                        "keyframes/portrait_002.png"
                    },
                    DurationSeconds = 15.0,
                    OutputPath = "output/zoom_in_effect.mp4",
                    
                    EnableCameraMotion = true,
                    CameraMotion = CameraMotionType.ZoomIn,
                    CameraMotionIntensity = 0.3
                };

                var result = await producer.ProduceVideoAsync(config);
                if (result.Success)
                    Console.WriteLine($"  ✓ Zoom in video: {result.OutputPath}");
                else
                    Console.WriteLine($"  ✗ Failed: {result.ErrorMessage}");
            }
            catch (Exception ex)
            {
                Console.WriteLine($"  ✗ Error: {ex.Message}");
            }
            Console.WriteLine();

            // Example 4.3: Dynamic motion (varies per keyframe)
            Console.WriteLine("4.3. Dynamic Motion (Alternating Effects)");
            try
            {
                var config = new VideoProductionConfig
                {
                    KeyframePaths = new List<string>
                    {
                        "keyframes/story/intro.png",
                        "keyframes/story/scene1.png",
                        "keyframes/story/scene2.png",
                        "keyframes/story/scene3.png",
                        "keyframes/story/outro.png"
                    },
                    DurationSeconds = 30.0,
                    OutputPath = "output/dynamic_motion.mp4",
                    
                    // Dynamic motion automatically varies effects
                    EnableCameraMotion = true,
                    CameraMotion = CameraMotionType.Dynamic,
                    CameraMotionIntensity = 0.35
                };

                var result = await producer.ProduceVideoAsync(config);
                if (result.Success)
                    Console.WriteLine($"  ✓ Dynamic motion video: {result.OutputPath}");
                else
                    Console.WriteLine($"  ✗ Failed: {result.ErrorMessage}");
            }
            catch (Exception ex)
            {
                Console.WriteLine($"  ✗ Error: {ex.Message}");
            }
            Console.WriteLine();

            // Example 4.4: Pan right with subtle zoom
            Console.WriteLine("4.4. Pan Right Effect");
            try
            {
                var config = new VideoProductionConfig
                {
                    KeyframePaths = new List<string>
                    {
                        "keyframes/wide_001.png",
                        "keyframes/wide_002.png"
                    },
                    DurationSeconds = 12.0,
                    OutputPath = "output/pan_right_effect.mp4",
                    
                    EnableCameraMotion = true,
                    CameraMotion = CameraMotionType.PanRight,
                    CameraMotionIntensity = 0.25
                };

                var result = await producer.ProduceVideoAsync(config);
                if (result.Success)
                    Console.WriteLine($"  ✓ Pan right video: {result.OutputPath}");
                else
                    Console.WriteLine($"  ✗ Failed: {result.ErrorMessage}");
            }
            catch (Exception ex)
            {
                Console.WriteLine($"  ✗ Error: {ex.Message}");
            }
            Console.WriteLine();

            // Example 4.5: No camera motion (static slideshow)
            Console.WriteLine("4.5. Static Slideshow (No Motion)");
            try
            {
                var config = new VideoProductionConfig
                {
                    KeyframePaths = new List<string>
                    {
                        "keyframes/presentation_001.png",
                        "keyframes/presentation_002.png",
                        "keyframes/presentation_003.png"
                    },
                    DurationSeconds = 18.0,
                    OutputPath = "output/static_slideshow.mp4",
                    
                    // Disable camera motion for static presentation
                    EnableCameraMotion = false
                };

                var result = await producer.ProduceVideoAsync(config);
                if (result.Success)
                    Console.WriteLine($"  ✓ Static slideshow: {result.OutputPath}");
                else
                    Console.WriteLine($"  ✗ Failed: {result.ErrorMessage}");
            }
            catch (Exception ex)
            {
                Console.WriteLine($"  ✗ Error: {ex.Message}");
            }
            Console.WriteLine();
        }

        /// <summary>
        /// Example configurations for different use cases.
        /// </summary>
        private static void ShowConfigurationExamples()
        {
            Console.WriteLine("Configuration Examples for Different Use Cases");
            Console.WriteLine("----------------------------------------------\n");

            // Story-driven content
            var storyConfig = new VideoProductionConfig
            {
                KeyframePaths = new List<string>
                {
                    "keyframes/story/beginning.png",
                    "keyframes/story/middle.png",
                    "keyframes/story/end.png"
                },
                DurationSeconds = 90.0,
                ScriptText = "Once upon a time...",
                GenerateSubtitlesFromScript = true,
                AudioPath = "voiceover/story_narration.mp3",
                BackgroundMusicPath = "bgm/gentle_piano.mp3",
                MusicVolume = 0.15,
                EnableDucking = true,
                OutputPath = "final/stories/kids/fairytale_draft.mp4"
            };
            Console.WriteLine("Story-Driven Content:");
            Console.WriteLine($"  Keyframes: {storyConfig.KeyframePaths.Count}");
            Console.WriteLine($"  Duration: {storyConfig.DurationSeconds}s");
            Console.WriteLine($"  Auto-subtitles: {storyConfig.GenerateSubtitlesFromScript}");
            Console.WriteLine();

            // Educational content
            var eduConfig = new VideoProductionConfig
            {
                KeyframePaths = new List<string>
                {
                    "keyframes/lesson/concept1.png",
                    "keyframes/lesson/concept2.png",
                    "keyframes/lesson/concept3.png",
                    "keyframes/lesson/summary.png"
                },
                DurationSeconds = 120.0,
                SrtPath = "subtitles/lesson_chapter1.srt",
                AudioPath = "voiceover/lesson_audio.mp3",
                BurnInSubtitles = true,
                OutputPath = "final/education/math/chapter1_draft.mp4"
            };
            Console.WriteLine("Educational Content:");
            Console.WriteLine($"  Keyframes: {eduConfig.KeyframePaths.Count}");
            Console.WriteLine($"  Duration: {eduConfig.DurationSeconds}s");
            Console.WriteLine($"  Burn-in subtitles: {eduConfig.BurnInSubtitles}");
            Console.WriteLine();

            // Social media content
            var socialConfig = new VideoProductionConfig
            {
                KeyframePaths = new List<string>
                {
                    "keyframes/social/hook.png",
                    "keyframes/social/content.png",
                    "keyframes/social/cta.png"
                },
                DurationSeconds = 15.0,
                ScriptText = "Quick tip: Did you know that...",
                GenerateSubtitlesFromScript = true,
                WordsPerMinute = 180, // Faster pacing for social media
                BackgroundMusicPath = "bgm/upbeat.mp3",
                MusicVolume = 0.3,
                Fps = 30,
                OutputPath = "final/social/tips/tip001_draft.mp4"
            };
            Console.WriteLine("Social Media Content:");
            Console.WriteLine($"  Duration: {socialConfig.DurationSeconds}s (short-form)");
            Console.WriteLine($"  Fast pacing: {socialConfig.WordsPerMinute} WPM");
            Console.WriteLine($"  Music volume: {socialConfig.MusicVolume * 100}%");
            Console.WriteLine();
        }
    }
}
