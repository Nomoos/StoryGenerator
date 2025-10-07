using System;
using System.Threading.Tasks;
using StoryGenerator.Core.Interfaces;
using StoryGenerator.Generators;
using StoryGenerator.Models;

namespace StoryGenerator.Examples
{
    /// <summary>
    /// Example demonstrating keyframe generation per scene using SDXL
    /// </summary>
    public class KeyframeGenerationExample
    {
        /// <summary>
        /// Run the keyframe generation example
        /// </summary>
        public static async Task RunAsync()
        {
            Console.WriteLine("=== Keyframe Generation Example ===\n");

            // Note: In a real implementation, you would need to provide an actual
            // IImageGenerationClient implementation that connects to SDXL
            // For this example, we'll create a mock implementation

            var imageClient = CreateMockImageClient();
            var keyframeService = new KeyframeGenerationService(imageClient);

            // Create a sample shotlist
            var shotlist = CreateSampleShotlist();

            // Configure keyframe generation
            var config = new KeyframeGenerationConfig
            {
                VariantsPerShot = 4,  // Generate 4 variants per shot
                TopNPerShot = 2,       // Select top 2 per shot
                Width = 1024,
                Height = 1024,
                BaseSteps = 40,
                RefinerSteps = 20,
                GuidanceScale = 7.5,
                UseRefiner = true,
                AgeSafeContent = true,
                OutputBaseDir = "images"
            };

            try
            {
                // Generate keyframes
                var manifest = await keyframeService.GenerateKeyframesAsync(
                    shotlist,
                    titleId: "example_story_001",
                    segment: "shorts",
                    age: "all-ages",
                    config: config);

                Console.WriteLine("\n=== Generation Complete ===");
                Console.WriteLine($"Total Keyframes: {manifest.Keyframes.Count}");
                Console.WriteLine($"Selected Keyframes: {manifest.SelectedKeyframes.Values.Sum(v => v.Count)}");
                Console.WriteLine($"Generation Time: {manifest.TotalGenerationTimeSeconds:F1}s");
                Console.WriteLine($"\nFiles saved to:");
                Console.WriteLine($"  - Prompts: images/keyframes_v1/shorts/all-ages/example_story_001_prompts.json");
                Console.WriteLine($"  - Manifest: images/keyframes_v1/shorts/all-ages/example_story_001_manifest.json");
                Console.WriteLine($"  - Keyframes: images/keyframes_v1/shorts/all-ages/example_story_001/shot_*.png");
            }
            catch (Exception ex)
            {
                Console.WriteLine($"\n❌ Error: {ex.Message}");
            }
        }

        /// <summary>
        /// Create a sample shotlist for demonstration
        /// </summary>
        private static StructuredShotlist CreateSampleShotlist()
        {
            var shotlist = new StructuredShotlist
            {
                StoryTitle = "Example Story",
                TotalDuration = 30f,
                OverallMood = "uplifting",
                Style = "cinematic",
                TargetAudience = "general"
            };

            // Shot 1: Opening establishing shot
            shotlist.Shots.Add(new StructuredShot
            {
                ShotNumber = 1,
                StartTime = 0f,
                EndTime = 5f,
                Duration = 5f,
                SceneDescription = "A peaceful mountain landscape at sunrise",
                VisualPrompt = "Beautiful mountain peaks with golden sunrise light, misty valleys below",
                PrimaryEmotion = "peaceful",
                Mood = "serene",
                CameraDirection = new CameraDirection
                {
                    ShotType = "wide shot",
                    Angle = "eye level",
                    Movement = "static",
                    Composition = "rule of thirds"
                },
                Lighting = "golden hour",
                ColorPalette = "warm oranges and blues"
            });

            // Shot 2: Character introduction
            shotlist.Shots.Add(new StructuredShot
            {
                ShotNumber = 2,
                StartTime = 5f,
                EndTime = 15f,
                Duration = 10f,
                SceneDescription = "A young adventurer looking at a map",
                VisualPrompt = "Person in hiking gear studying an old map, backpack beside them, determined expression",
                PrimaryEmotion = "determined",
                Mood = "adventurous",
                CameraDirection = new CameraDirection
                {
                    ShotType = "medium close-up",
                    Angle = "slightly high angle",
                    Movement = "slow push in",
                    Composition = "centered"
                },
                Lighting = "natural daylight",
                ColorPalette = "earthy tones"
            });

            // Shot 3: Action/journey
            shotlist.Shots.Add(new StructuredShot
            {
                ShotNumber = 3,
                StartTime = 15f,
                EndTime = 25f,
                Duration = 10f,
                SceneDescription = "Hiking through a dense forest trail",
                VisualPrompt = "Winding forest path with dappled sunlight, tall trees, adventure atmosphere",
                PrimaryEmotion = "curious",
                Mood = "mysterious",
                CameraDirection = new CameraDirection
                {
                    ShotType = "tracking shot",
                    Angle = "following behind",
                    Movement = "smooth dolly",
                    Composition = "leading lines"
                },
                Lighting = "dappled forest light",
                ColorPalette = "rich greens and browns"
            });

            // Shot 4: Conclusion
            shotlist.Shots.Add(new StructuredShot
            {
                ShotNumber = 4,
                StartTime = 25f,
                EndTime = 30f,
                Duration = 5f,
                SceneDescription = "Reaching the summit with a breathtaking view",
                VisualPrompt = "Standing on mountain summit with arms raised, epic vista behind, triumph",
                PrimaryEmotion = "triumphant",
                Mood = "inspiring",
                CameraDirection = new CameraDirection
                {
                    ShotType = "wide shot",
                    Angle = "low angle",
                    Movement = "crane up",
                    Composition = "hero composition"
                },
                Lighting = "bright daylight",
                ColorPalette = "vibrant blues and whites"
            });

            return shotlist;
        }

        /// <summary>
        /// Create a mock image client for demonstration purposes
        /// In a real implementation, this would be replaced with an actual SDXL client
        /// </summary>
        private static IImageGenerationClient CreateMockImageClient()
        {
            // This is a placeholder - in real usage, you would implement or use
            // an actual IImageGenerationClient that connects to SDXL
            // For example, using the Hugging Face Diffusers library or Stability AI API
            
            Console.WriteLine("Note: Using mock image client for demonstration.");
            Console.WriteLine("In production, replace with actual SDXL implementation.\n");
            
            return new MockImageGenerationClient();
        }
    }

    /// <summary>
    /// Mock implementation of IImageGenerationClient for demonstration
    /// Replace with actual SDXL client in production
    /// </summary>
    internal class MockImageGenerationClient : IImageGenerationClient
    {
        public async Task<ImageGenerationResult> GenerateImageAsync(
            string prompt,
            string? negativePrompt = null,
            int width = 1024,
            int height = 1024,
            int numInferenceSteps = 30,
            double guidanceScale = 7.5,
            int? seed = null,
            System.Threading.CancellationToken cancellationToken = default)
        {
            await Task.Delay(100, cancellationToken); // Simulate generation time
            
            return new ImageGenerationResult
            {
                ImageData = new byte[1024], // Mock image data
                Width = width,
                Height = height,
                Prompt = prompt,
                NegativePrompt = negativePrompt,
                Seed = seed ?? new Random().Next(),
                InferenceSteps = numInferenceSteps,
                GuidanceScale = guidanceScale,
                GenerationTimeMs = 100,
                Model = "mock-sdxl-base",
                UsedRefiner = false
            };
        }

        public async Task<ImageGenerationResult> GenerateImageWithRefinerAsync(
            string prompt,
            string? negativePrompt = null,
            int width = 1024,
            int height = 1024,
            int baseSteps = 40,
            int refinerSteps = 20,
            double guidanceScale = 7.5,
            int? seed = null,
            System.Threading.CancellationToken cancellationToken = default)
        {
            await Task.Delay(200, cancellationToken); // Simulate longer generation time
            
            return new ImageGenerationResult
            {
                ImageData = new byte[1024], // Mock image data
                Width = width,
                Height = height,
                Prompt = prompt,
                NegativePrompt = negativePrompt,
                Seed = seed ?? new Random().Next(),
                InferenceSteps = baseSteps + refinerSteps,
                GuidanceScale = guidanceScale,
                GenerationTimeMs = 200,
                Model = "mock-sdxl-base+refiner",
                UsedRefiner = true
            };
        }

        public Task<System.Collections.Generic.List<ImageGenerationResult>> GenerateImageBatchAsync(
            string prompt,
            string? negativePrompt = null,
            int count = 4,
            int width = 1024,
            int height = 1024,
            int numInferenceSteps = 30,
            double guidanceScale = 7.5,
            System.Threading.CancellationToken cancellationToken = default)
        {
            throw new NotImplementedException("Mock client - batch generation not implemented");
        }

        public Task<bool> LoadLoraAsync(string loraPath, double scale = 0.75)
        {
            Console.WriteLine($"   [Mock] Loading LoRA: {loraPath} (scale: {scale})");
            return Task.FromResult(true);
        }

        public Task<bool> UnloadLoraAsync()
        {
            Console.WriteLine($"   [Mock] Unloading LoRA");
            return Task.FromResult(true);
        }

        public Task<string> SaveImageAsync(ImageGenerationResult result, string outputPath)
        {
            // Create a mock image file
            var directory = System.IO.Path.GetDirectoryName(outputPath);
            if (!string.IsNullOrEmpty(directory))
            {
                System.IO.Directory.CreateDirectory(directory);
            }
            
            System.IO.File.WriteAllBytes(outputPath, result.ImageData);
            return Task.FromResult(outputPath);
        }

        public ModelInfo GetModelInfo()
        {
            return new ModelInfo
            {
                ModelName = "mock-sdxl-base-1.0",
                ModelType = "stable-diffusion-xl",
                IsLoaded = true
            };
        }

        public Task<bool> IsReadyAsync()
        {
            return Task.FromResult(true);
        }
    }

    /// <summary>
    /// Model information
    /// </summary>
    public class ModelInfo
    {
        public string ModelName { get; set; } = string.Empty;
        public string ModelType { get; set; } = string.Empty;
        public bool IsLoaded { get; set; }
    }
}
