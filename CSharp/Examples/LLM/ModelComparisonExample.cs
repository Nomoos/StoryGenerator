using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Threading.Tasks;
using StoryGenerator.Core.Interfaces;
using StoryGenerator.Core.LLM;

namespace StoryGenerator.Examples.LLM
{
    /// <summary>
    /// Example comparing Qwen2.5-14B-Instruct vs Llama-3.1-8B-Instruct.
    /// Tests quality and speed differences between models.
    /// </summary>
    public class ModelComparisonExample
    {
        /// <summary>
        /// Runs the model comparison example.
        /// </summary>
        public static async Task RunAsync()
        {
            Console.WriteLine("=== LLM Model Comparison: Qwen vs Llama ===\n");

            // Sample story idea for testing
            var storyIdea = new SampleStoryIdea
            {
                Title = "The Last Library",
                Description = "In a world where books are illegal, one librarian protects the last library",
                Tone = "mysterious and hopeful"
            };

            Console.WriteLine($"Test Story: {storyIdea.Title}");
            Console.WriteLine($"Description: {storyIdea.Description}\n");

            // Test Qwen2.5-14B-Instruct
            Console.WriteLine("=== Testing Qwen2.5-14B-Instruct ===");
            await TestModel(
                RecommendedModels.Qwen25_14B_Instruct,
                "Qwen2.5 14B",
                storyIdea
            );

            Console.WriteLine("\n" + new string('-', 80) + "\n");

            // Test Llama-3.1-8B-Instruct
            Console.WriteLine("=== Testing Llama-3.1-8B-Instruct ===");
            await TestModel(
                RecommendedModels.Llama31_8B_Instruct,
                "Llama 3.1 8B",
                storyIdea
            );

            Console.WriteLine("\n=== Comparison Summary ===");
            Console.WriteLine("Qwen2.5-14B-Instruct:");
            Console.WriteLine("  Pros: Superior quality, better creative detail, excellent JSON output");
            Console.WriteLine("  Cons: Slower inference, higher VRAM usage (~14GB)");
            Console.WriteLine("  Best for: Production quality content");
            Console.WriteLine();
            Console.WriteLine("Llama-3.1-8B-Instruct:");
            Console.WriteLine("  Pros: 2-3x faster, lower VRAM (~8GB), good quality");
            Console.WriteLine("  Cons: Less creative detail, occasional JSON formatting issues");
            Console.WriteLine("  Best for: Fast iteration, testing, prototyping");
            Console.WriteLine();
            Console.WriteLine("Recommendation: Use Qwen for final production, Llama for development/testing");
        }

        private static async Task TestModel(string modelName, string displayName, SampleStoryIdea storyIdea)
        {
            Console.WriteLine($"Model: {modelName}");

            // Setup
            var modelProvider = new OllamaModelProvider(modelName);

            // Check availability
            var isAvailable = await modelProvider.IsModelAvailableAsync(modelName);
            if (!isAvailable)
            {
                Console.WriteLine($"⚠ Model {modelName} not available. Run: ollama pull {modelName}");
                return;
            }

            var contentGenerator = new LLMContentGenerator(modelProvider);
            var shotlistGenerator = new LLMShotlistGenerator(contentGenerator);

            // Test 1: Script Generation Speed
            Console.WriteLine("\nTest 1: Script Generation");
            var scriptStopwatch = Stopwatch.StartNew();
            var script = await contentGenerator.GenerateScriptAsync(
                storyIdea,
                targetLength: 200,  // Shorter for faster testing
                temperature: 0.7f
            );
            scriptStopwatch.Stop();

            Console.WriteLine($"  Time: {scriptStopwatch.Elapsed.TotalSeconds:F2}s");
            Console.WriteLine($"  Length: {script.Split(' ').Length} words");
            Console.WriteLine($"  Quality Sample: {script.Substring(0, Math.Min(150, script.Length))}...");

            // Test 2: Scene Breakdown Speed
            Console.WriteLine("\nTest 2: Scene Breakdown");
            var sceneStopwatch = Stopwatch.StartNew();
            var sceneBreakdown = await contentGenerator.GenerateSceneBreakdownAsync(
                script,
                temperature: 0.5f
            );
            sceneStopwatch.Stop();

            Console.WriteLine($"  Time: {sceneStopwatch.Elapsed.TotalSeconds:F2}s");
            Console.WriteLine($"  Length: {sceneBreakdown.Length} characters");

            // Test 3: Shotlist Generation Speed and Quality
            Console.WriteLine("\nTest 3: Structured Shotlist Generation");
            var shotlistStopwatch = Stopwatch.StartNew();
            
            StructuredShotlist shotlist;
            bool parseSuccess = true;
            try
            {
                shotlist = await shotlistGenerator.GenerateStructuredShotlistAsync(
                    script,
                    audioDuration: 40.0f,  // Shorter for testing
                    temperature: 0.5f
                );
                shotlistStopwatch.Stop();

                Console.WriteLine($"  Time: {shotlistStopwatch.Elapsed.TotalSeconds:F2}s");
                Console.WriteLine($"  Shots: {shotlist.Shots.Count}");
                Console.WriteLine($"  Duration: {shotlist.TotalDuration}s");
                Console.WriteLine($"  Overall Mood: {shotlist.OverallMood}");

                // Validate
                var errors = ShotlistParser.ValidateShotlist(shotlist);
                Console.WriteLine($"  Validation: {(errors.Count == 0 ? "✓ Pass" : $"⚠ {errors.Count} issues")}");

                // Quality metrics
                int detailedShots = 0;
                foreach (var shot in shotlist.Shots)
                {
                    if (!string.IsNullOrWhiteSpace(shot.CameraDirection.ShotType) &&
                        !string.IsNullOrWhiteSpace(shot.PrimaryEmotion) &&
                        shot.VisualPrompt.Length > 50)
                    {
                        detailedShots++;
                    }
                }
                Console.WriteLine($"  Quality: {detailedShots}/{shotlist.Shots.Count} shots with complete details");
            }
            catch (Exception ex)
            {
                shotlistStopwatch.Stop();
                parseSuccess = false;
                Console.WriteLine($"  Time: {shotlistStopwatch.Elapsed.TotalSeconds:F2}s");
                Console.WriteLine($"  Status: ✗ Failed to parse JSON");
                Console.WriteLine($"  Error: {ex.Message}");
            }

            // Performance Summary
            Console.WriteLine("\nPerformance Summary:");
            Console.WriteLine($"  Total Time: {(scriptStopwatch.Elapsed + sceneStopwatch.Elapsed + shotlistStopwatch.Elapsed).TotalSeconds:F2}s");
            Console.WriteLine($"  Script: {scriptStopwatch.Elapsed.TotalSeconds:F2}s");
            Console.WriteLine($"  Scene: {sceneStopwatch.Elapsed.TotalSeconds:F2}s");
            Console.WriteLine($"  Shotlist: {shotlistStopwatch.Elapsed.TotalSeconds:F2}s");
            Console.WriteLine($"  JSON Parsing: {(parseSuccess ? "✓" : "✗")}");
        }

        /// <summary>
        /// Sample story idea implementation for demonstration.
        /// </summary>
        private class SampleStoryIdea : IStoryIdea
        {
            public string StoryTitle { get; set; } = string.Empty;
            public string NarratorGender { get; set; } = "female";
            public string? Tone { get; set; }
            public string? Theme { get; set; }
            public string? NarratorType { get; set; } = "third-person";
            public string? OtherCharacter { get; set; }
            public string? Outcome { get; set; }
            public string? EmotionalCore { get; set; }
            public string? PowerDynamic { get; set; }
            public string? Timeline { get; set; }
            public string? TwistType { get; set; }
            public string? CharacterArc { get; set; }
            public string? VoiceStyle { get; set; }
            public string? TargetMoral { get; set; }
            public string? Locations { get; set; }
            public string? MentionedBrands { get; set; }
            public string? Goal { get; set; }
            public string Language { get; set; } = "en";
            public Dictionary<string, string> Personalization { get; set; } = new();
            public string VideoStyle { get; set; } = "cinematic";
            public float VoiceStability { get; set; } = 0.5f;
            public float VoiceSimilarityBoost { get; set; } = 0.75f;
            public float VoiceStyleExaggeration { get; set; } = 0.0f;
            public ViralPotential Potential { get; set; } = new();

            // Helper properties for convenience
            public string Title
            {
                get => StoryTitle;
                set => StoryTitle = value;
            }

            public string Description { get; set; } = string.Empty;
        }
    }
}
