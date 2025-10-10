using System;
using System.Threading.Tasks;
using StoryGenerator.Core.Interfaces;
using StoryGenerator.Generators;
using StoryGenerator.Models;

namespace StoryGenerator.Examples
{
    /// <summary>
    /// Example demonstrating keyframe generation from simple scene description and subtitles
    /// </summary>
    public class SimpleKeyframeGenerationExample
    {
        /// <summary>
        /// Run the simple keyframe generation example
        /// </summary>
        public static async Task RunAsync()
        {
            Console.WriteLine("=== Simple Keyframe Generation from Scene Description Example ===\n");

            // Note: In a real implementation, you would need to provide an actual
            // IImageGenerationClient implementation that connects to SDXL
            // For this example, we'll create a mock implementation
            var imageClient = CreateMockImageClient();
            var keyframeService = new KeyframeGenerationService(imageClient);

            // Example 1: Generate keyframes from scene description only
            Console.WriteLine("Example 1: Scene description without subtitles");
            Console.WriteLine("-----------------------------------------------");
            await GenerateFromSceneDescription(
                keyframeService,
                sceneDescription: "A peaceful mountain landscape at sunrise with golden light illuminating snow-capped peaks",
                subtitles: null,
                titleId: "mountain_sunrise_001");

            Console.WriteLine("\n\n");

            // Example 2: Generate keyframes from scene description with subtitles
            Console.WriteLine("Example 2: Scene description with subtitles");
            Console.WriteLine("-------------------------------------------");
            await GenerateFromSceneDescription(
                keyframeService,
                sceneDescription: "A cozy coffee shop interior with warm lighting and comfortable seating",
                subtitles: "Welcome to our cafe, where every cup tells a story",
                titleId: "coffee_shop_welcome_002");

            Console.WriteLine("\n\n");

            // Example 3: Generate keyframes for different scene types
            Console.WriteLine("Example 3: Multiple scene types");
            Console.WriteLine("--------------------------------");
            
            var scenes = new[]
            {
                new { Description = "A futuristic city skyline at night with neon lights reflecting off glass buildings", Subtitles = "The year is 2050", TitleId = "future_city_001" },
                new { Description = "An ancient library filled with dusty books and soft candlelight", Subtitles = (string?)null, TitleId = "ancient_library_001" },
                new { Description = "A bustling marketplace with colorful stalls and diverse people shopping", Subtitles = "Fresh produce daily", TitleId = "market_001" }
            };

            foreach (var scene in scenes)
            {
                Console.WriteLine($"\nGenerating: {scene.TitleId}");
                await GenerateFromSceneDescription(
                    keyframeService,
                    scene.Description,
                    scene.Subtitles,
                    scene.TitleId);
            }

            Console.WriteLine("\n\n=== All Examples Complete ===");
        }

        /// <summary>
        /// Generate keyframes from a scene description
        /// </summary>
        private static async Task GenerateFromSceneDescription(
            KeyframeGenerationService service,
            string sceneDescription,
            string? subtitles,
            string titleId)
        {
            // Configure keyframe generation
            var config = new KeyframeGenerationConfig
            {
                VariantsPerShot = 3,  // Generate 3 variants
                TopNPerShot = 2,       // Select top 2
                Width = 1024,
                Height = 1024,
                BaseSteps = 30,
                UseRefiner = false,    // Faster for demo
                AgeSafeContent = true,
                OutputBaseDir = "/tmp/simple_keyframes"
            };

            try
            {
                Console.WriteLine($"  Scene: {sceneDescription.Substring(0, Math.Min(60, sceneDescription.Length))}...");
                if (!string.IsNullOrEmpty(subtitles))
                {
                    Console.WriteLine($"  Subtitles: {subtitles}");
                }

                // Generate keyframes using the new method
                var manifest = await service.GenerateKeyframesFromSceneAsync(
                    sceneDescription,
                    subtitles,
                    titleId,
                    config);

                Console.WriteLine($"  ✓ Generated {manifest.Keyframes.Count} keyframe variants");
                Console.WriteLine($"  ✓ Selected {manifest.SelectedKeyframes[1].Count} top keyframes");
                Console.WriteLine($"  ✓ Generation time: {manifest.TotalGenerationTimeSeconds:F1}s");
                Console.WriteLine($"  ✓ Manifest saved to: images/keyframes_v1/single-scene/all-ages/{titleId}_manifest.json");
            }
            catch (Exception ex)
            {
                Console.WriteLine($"  ✗ Error: {ex.Message}");
            }
        }

        /// <summary>
        /// Create a mock image client for demonstration purposes
        /// In a real implementation, this would be replaced with an actual SDXL client
        /// </summary>
        private static IImageGenerationClient CreateMockImageClient()
        {
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
        private static int _callCount = 0;

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
            _callCount++;
            
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
            _callCount++;
            
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
