using System;
using System.Collections.Generic;
using System.IO;
using System.Threading.Tasks;
using StoryGenerator.Core.Interfaces;
using StoryGenerator.Core.LLM;

namespace StoryGenerator.Examples.LLM
{
    /// <summary>
    /// Example demonstrating LLM-based content generation.
    /// Shows how to generate scripts, scene breakdowns, and video descriptions.
    /// </summary>
    public class LLMContentGenerationExample
    {
        /// <summary>
        /// Runs the content generation example.
        /// </summary>
        public static async Task RunAsync()
        {
            Console.WriteLine("=== LLM Content Generation Example ===\n");

            // 1. Setup: Create model provider and content generator
            Console.WriteLine("Setting up LLM provider...");
            var modelProvider = new OllamaModelProvider(
                defaultModel: RecommendedModels.Qwen25_14B_Instruct
            );

            // Check if model is available
            var isAvailable = await modelProvider.IsModelAvailableAsync(RecommendedModels.Qwen25_14B_Instruct);
            if (!isAvailable)
            {
                Console.WriteLine($"Model {RecommendedModels.Qwen25_14B_Instruct} not found.");
                Console.WriteLine("Pulling model (this may take a while)...");
                await modelProvider.PullModelAsync(RecommendedModels.Qwen25_14B_Instruct);
            }

            var contentGenerator = new LLMContentGenerator(modelProvider);
            Console.WriteLine($"Using model: {contentGenerator.ModelName}");
            Console.WriteLine($"Provider: {contentGenerator.Provider}\n");

            // 2. Create a sample story idea
            var storyIdea = new SampleStoryIdea
            {
                Title = "The Last Library",
                Description = "In a world where books are illegal, one librarian protects the last remaining library, preserving humanity's knowledge while evading the authorities.",
                Tone = "mysterious and hopeful"
            };

            Console.WriteLine($"Story Idea: {storyIdea.Title}");
            Console.WriteLine($"Description: {storyIdea.Description}");
            Console.WriteLine($"Tone: {storyIdea.Tone}\n");

            // 3. Generate script
            Console.WriteLine("Generating script (this may take 30-60 seconds)...");
            var script = await contentGenerator.GenerateScriptAsync(
                storyIdea,
                targetLength: 360,  // ~60 seconds of speech
                temperature: 0.7f   // Creative but focused
            );

            Console.WriteLine("\n--- Generated Script ---");
            Console.WriteLine(script);
            Console.WriteLine($"\nScript length: {script.Split(' ').Length} words\n");

            // 4. Generate scene breakdown
            Console.WriteLine("Generating scene breakdown...");
            var sceneBreakdown = await contentGenerator.GenerateSceneBreakdownAsync(
                scriptText: script,
                temperature: 0.5f  // More structured output
            );

            Console.WriteLine("\n--- Scene Breakdown ---");
            Console.WriteLine(sceneBreakdown);
            Console.WriteLine();

            // 5. Generate video description for a specific scene
            Console.WriteLine("Generating video description for opening scene...");
            var videoDescription = await contentGenerator.GenerateVideoDescriptionAsync(
                sceneDescription: "Wide shot of an abandoned library at dusk",
                mood: "mysterious and atmospheric",
                temperature: 0.6f
            );

            Console.WriteLine("\n--- Video Description ---");
            Console.WriteLine(videoDescription);
            Console.WriteLine();

            // 6. Save outputs
            var outputDir = Path.Combine(AppDomain.CurrentDomain.BaseDirectory, "output", "llm-example");
            Directory.CreateDirectory(outputDir);

            var scriptPath = Path.Combine(outputDir, "script.txt");
            await File.WriteAllTextAsync(scriptPath, script);
            Console.WriteLine($"Script saved to: {scriptPath}");

            var scenePath = Path.Combine(outputDir, "scene_breakdown.txt");
            await File.WriteAllTextAsync(scenePath, sceneBreakdown);
            Console.WriteLine($"Scene breakdown saved to: {scenePath}");

            var videoPath = Path.Combine(outputDir, "video_description.txt");
            await File.WriteAllTextAsync(videoPath, videoDescription);
            Console.WriteLine($"Video description saved to: {videoPath}");

            Console.WriteLine("\n=== Example Complete ===");
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
