using System;
using System.Collections.Generic;
using System.Threading.Tasks;
using StoryGenerator.Generators;
using StoryGenerator.Tools;

namespace StoryGenerator.Examples
{
    /// <summary>
    /// Example program demonstrating video synthesis approaches
    /// </summary>
    class VideoSynthesisExample
    {
        static async Task Main(string[] args)
        {
            Console.WriteLine("═══════════════════════════════════════════════════════════════");
            Console.WriteLine("    StoryGenerator - Video Synthesis Examples");
            Console.WriteLine("═══════════════════════════════════════════════════════════════");
            Console.WriteLine();
            
            // Example 1: LTX-Video Generation
            await Example1_LTXVideoBasic();
            
            // Example 2: SDXL + Frame Interpolation
            await Example2_KeyframeVideo();
            
            // Example 3: Scene with Motion Control
            await Example3_SceneWithMotion();
            
            // Example 4: Compare Approaches
            await Example4_CompareApproaches();
            
            Console.WriteLine("\n✅ All examples completed!");
        }
        
        /// <summary>
        /// Example 1: Basic LTX-Video generation
        /// </summary>
        static async Task Example1_LTXVideoBasic()
        {
            Console.WriteLine("\n" + new string('═', 70));
            Console.WriteLine("EXAMPLE 1: LTX-Video Basic Generation");
            Console.WriteLine(new string('═', 70));
            
            var synthesizer = new LTXVideoSynthesizer(
                width: 1080,
                height: 1920,
                fps: 30
            );
            
            string prompt = "A serene lake at sunset with mountains in the background, " +
                          "camera slowly panning right, cinematic, beautiful lighting";
            
            string outputPath = "output/example1_ltx_video.mp4";
            
            Console.WriteLine($"\nPrompt: {prompt}");
            Console.WriteLine($"Output: {outputPath}");
            
            bool success = await synthesizer.GenerateVideoAsync(
                prompt: prompt,
                outputPath: outputPath,
                duration: 10,
                fps: 30
            );
            
            if (success)
                Console.WriteLine("✅ Video generated successfully!");
            else
                Console.WriteLine("❌ Video generation failed");
        }
        
        /// <summary>
        /// Example 2: SDXL keyframes with frame interpolation
        /// </summary>
        static async Task Example2_KeyframeVideo()
        {
            Console.WriteLine("\n" + new string('═', 70));
            Console.WriteLine("EXAMPLE 2: SDXL + Frame Interpolation");
            Console.WriteLine(new string('═', 70));
            
            var config = new KeyframeVideoConfig
            {
                TargetFps = 30,
                Method = InterpolationMethod.RIFE,
                Width = 1080,
                Height = 1920,
                KeyframesPerScene = 3
            };
            
            var synthesizer = new KeyframeVideoSynthesizer(config);
            
            string sceneDescription = "A mystical forest path with sunlight filtering " +
                                    "through trees, magical atmosphere";
            
            var stylePrompts = new List<string>
            {
                "cinematic lighting",
                "depth of field",
                "photorealistic"
            };
            
            string outputPath = "output/example2_keyframe_video.mp4";
            
            Console.WriteLine($"\nScene: {sceneDescription}");
            Console.WriteLine($"Style: {string.Join(", ", stylePrompts)}");
            Console.WriteLine($"Output: {outputPath}");
            
            bool success = await synthesizer.GenerateSceneAsync(
                sceneDescription: sceneDescription,
                outputPath: outputPath,
                duration: 8.0,
                stylePrompts: stylePrompts
            );
            
            if (success)
                Console.WriteLine("✅ Video generated successfully!");
            else
                Console.WriteLine("❌ Video generation failed");
        }
        
        /// <summary>
        /// Example 3: Scene generation with motion control
        /// </summary>
        static async Task Example3_SceneWithMotion()
        {
            Console.WriteLine("\n" + new string('═', 70));
            Console.WriteLine("EXAMPLE 3: Scene with Motion Control");
            Console.WriteLine(new string('═', 70));
            
            var synthesizer = new LTXVideoSynthesizer();
            
            var scenes = new List<(string description, string motion, double duration)>
            {
                (
                    "City skyline at night with twinkling lights",
                    "camera slowly panning right across the skyline",
                    5.0
                ),
                (
                    "Close-up of a person's face with contemplative expression",
                    "slight zoom in, focus on eyes",
                    4.0
                ),
                (
                    "Busy street with people walking",
                    "camera moving forward through the crowd",
                    6.0
                )
            };
            
            for (int i = 0; i < scenes.Count; i++)
            {
                var scene = scenes[i];
                string outputPath = $"output/example3_scene_{i + 1}.mp4";
                
                Console.WriteLine($"\nScene {i + 1}:");
                Console.WriteLine($"  Description: {scene.description}");
                Console.WriteLine($"  Motion: {scene.motion}");
                Console.WriteLine($"  Duration: {scene.duration}s");
                
                bool success = await synthesizer.GenerateSceneClipAsync(
                    sceneDescription: scene.description,
                    motionHint: scene.motion,
                    outputPath: outputPath,
                    duration: scene.duration
                );
                
                if (success)
                    Console.WriteLine($"  ✅ Scene {i + 1} generated");
                else
                    Console.WriteLine($"  ❌ Scene {i + 1} failed");
            }
        }
        
        /// <summary>
        /// Example 4: Compare different approaches
        /// </summary>
        static async Task Example4_CompareApproaches()
        {
            Console.WriteLine("\n" + new string('═', 70));
            Console.WriteLine("EXAMPLE 4: Compare Video Synthesis Approaches");
            Console.WriteLine(new string('═', 70));
            
            var comparator = new VideoSynthesisComparator();
            
            string testPrompt = "A beautiful sunset over ocean waves, " +
                              "camera slowly pulling back, cinematic";
            
            Console.WriteLine($"\nTest Prompt: {testPrompt}");
            Console.WriteLine("Testing all approaches...\n");
            
            var results = await comparator.CompareApproachesAsync(
                testPrompt: testPrompt,
                duration: 10.0,
                outputDir: "output/comparison"
            );
            
            Console.WriteLine($"\n✅ Comparison complete! Results saved to output/comparison/");
        }
        
        /// <summary>
        /// Example 5: Using predefined motion presets
        /// </summary>
        static async Task Example5_MotionPresets()
        {
            Console.WriteLine("\n" + new string('═', 70));
            Console.WriteLine("EXAMPLE 5: Using Motion Presets");
            Console.WriteLine(new string('═', 70));
            
            var synthesizer = new LTXVideoSynthesizer();
            
            // Motion presets from configuration
            var motionPresets = new Dictionary<string, string>
            {
                { "pan_right", "camera slowly panning right, smooth lateral movement" },
                { "zoom_in", "camera slowly zooming in, forward movement" },
                { "dolly_forward", "camera moving forward, approaching subject" },
                { "orbit", "camera orbiting around subject, circular movement" }
            };
            
            Console.WriteLine("\nAvailable motion presets:");
            foreach (var preset in motionPresets)
            {
                Console.WriteLine($"  - {preset.Key}: {preset.Value}");
            }
            
            // Example using a preset
            string selectedMotion = motionPresets["zoom_in"];
            string description = "A mystical crystal glowing in a dark cave";
            
            Console.WriteLine($"\nGenerating scene with '{selectedMotion}' motion...");
            
            bool success = await synthesizer.GenerateSceneClipAsync(
                sceneDescription: description,
                motionHint: selectedMotion,
                outputPath: "output/example5_motion_preset.mp4",
                duration: 5.0
            );
            
            if (success)
                Console.WriteLine("✅ Scene with motion preset generated!");
        }
        
        /// <summary>
        /// Example 6: Batch scene generation
        /// </summary>
        static async Task Example6_BatchGeneration()
        {
            Console.WriteLine("\n" + new string('═', 70));
            Console.WriteLine("EXAMPLE 6: Batch Scene Generation");
            Console.WriteLine(new string('═', 70));
            
            var synthesizer = new LTXVideoSynthesizer();
            
            var scenes = new List<(string description, double duration)>
            {
                ("Opening scene: sunrise over mountains", 5.0),
                ("Character walking through forest path", 7.0),
                ("Discovery of ancient ruins", 6.0),
                ("Mysterious artifact glowing", 5.0),
                ("Closing scene: sunset over valley", 5.0)
            };
            
            Console.WriteLine($"\nGenerating {scenes.Count} scenes...\n");
            
            int successCount = 0;
            for (int i = 0; i < scenes.Count; i++)
            {
                var scene = scenes[i];
                string outputPath = $"output/batch/scene_{i + 1:D2}.mp4";
                
                Console.WriteLine($"Scene {i + 1}/{scenes.Count}: {scene.description}");
                
                bool success = await synthesizer.GenerateVideoAsync(
                    prompt: scene.description,
                    outputPath: outputPath,
                    duration: (int)scene.duration
                );
                
                if (success)
                {
                    successCount++;
                    Console.WriteLine("  ✅ Success");
                }
                else
                {
                    Console.WriteLine("  ❌ Failed");
                }
            }
            
            Console.WriteLine($"\n✅ Batch generation complete: {successCount}/{scenes.Count} successful");
        }
    }
}
