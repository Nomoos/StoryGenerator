using System;
using System.Diagnostics;
using System.IO;
using System.Threading.Tasks;
using StoryGenerator.Core.Interfaces;
using StoryGenerator.Core.LLM;

namespace StoryGenerator.Examples.LLM
{
    /// <summary>
    /// Example demonstrating LLM-based shotlist generation.
    /// Shows how to generate structured shotlists with emotions, camera directions, and timing.
    /// </summary>
    public class LLMShotlistGenerationExample
    {
        /// <summary>
        /// Runs the shotlist generation example.
        /// </summary>
        public static async Task RunAsync()
        {
            Console.WriteLine("=== LLM Shotlist Generation Example ===\n");

            // 1. Setup: Create model provider and generators
            Console.WriteLine("Setting up LLM provider...");
            var modelProvider = new OllamaModelProvider(
                defaultModel: RecommendedModels.Qwen25_14B_Instruct
            );

            var contentGenerator = new LLMContentGenerator(modelProvider);
            var shotlistGenerator = new LLMShotlistGenerator(contentGenerator);

            Console.WriteLine($"Using model: {contentGenerator.ModelName}");
            Console.WriteLine($"Provider: {contentGenerator.Provider}\n");

            // 2. Sample script
            var script = @"In a world where books are banned and libraries are just distant memories, one woman refuses to let knowledge die. 
Sarah, the last librarian, guards an underground library hidden beneath an abandoned subway station. 
Every night, she risks everything to preserve humanity's greatest treasure—our stories, our history, our truth. 
The authorities are closing in, but Sarah knows that as long as one person remembers, hope survives. 
Tonight, she makes her final stand, not with weapons, but with words.";

            Console.WriteLine("Script:");
            Console.WriteLine(script);
            Console.WriteLine($"\nScript length: {script.Split(' ').Length} words\n");

            // 3. Generate structured shotlist
            Console.WriteLine("Generating structured shotlist (this may take 60-90 seconds)...");
            var stopwatch = Stopwatch.StartNew();

            var shotlist = await shotlistGenerator.GenerateStructuredShotlistAsync(
                scriptText: script,
                audioDuration: 58.5f,  // Audio duration in seconds
                temperature: 0.5f      // More structured output
            );

            stopwatch.Stop();
            Console.WriteLine($"Generation completed in {stopwatch.Elapsed.TotalSeconds:F2} seconds\n");

            // 4. Display shotlist information
            Console.WriteLine("--- Shotlist Overview ---");
            Console.WriteLine($"Title: {shotlist.StoryTitle}");
            Console.WriteLine($"Total Duration: {shotlist.TotalDuration}s");
            Console.WriteLine($"Overall Mood: {shotlist.OverallMood}");
            Console.WriteLine($"Style: {shotlist.Style}");
            Console.WriteLine($"Number of Shots: {shotlist.Shots.Count}");
            Console.WriteLine($"Model: {shotlist.Metadata.ModelUsed}");
            Console.WriteLine($"Generation Time: {shotlist.Metadata.GenerationTimeSeconds:F2}s\n");

            // 5. Display each shot in detail
            Console.WriteLine("--- Shot Breakdown ---\n");
            foreach (var shot in shotlist.Shots)
            {
                Console.WriteLine($"SHOT {shot.ShotNumber}:");
                Console.WriteLine($"  Time: {shot.StartTime:F1}s - {shot.EndTime:F1}s ({shot.Duration:F1}s)");
                Console.WriteLine($"  Scene: {shot.SceneDescription}");
                Console.WriteLine($"  Emotion: {shot.PrimaryEmotion}");
                if (shot.SecondaryEmotions.Count > 0)
                {
                    Console.WriteLine($"  Secondary Emotions: {string.Join(", ", shot.SecondaryEmotions)}");
                }
                Console.WriteLine($"  Mood: {shot.Mood}");
                Console.WriteLine($"  Camera:");
                Console.WriteLine($"    - Type: {shot.CameraDirection.ShotType}");
                Console.WriteLine($"    - Angle: {shot.CameraDirection.Angle}");
                Console.WriteLine($"    - Movement: {shot.CameraDirection.Movement}");
                Console.WriteLine($"    - Focus: {shot.CameraDirection.FocusPoint}");
                Console.WriteLine($"    - Composition: {shot.CameraDirection.Composition}");
                Console.WriteLine($"  Movement: {shot.MovementType}");
                Console.WriteLine($"  Transition: {shot.Transition}");
                Console.WriteLine($"  Lighting: {shot.Lighting}");
                Console.WriteLine($"  Color Palette: {shot.ColorPalette}");
                Console.WriteLine($"  Importance: {shot.Importance}/10");
                Console.WriteLine($"  Visual Prompt: {shot.VisualPrompt}");
                if (shot.KeyElements.Count > 0)
                {
                    Console.WriteLine($"  Key Elements: {string.Join(", ", shot.KeyElements)}");
                }
                Console.WriteLine();
            }

            // 6. Validate shotlist
            Console.WriteLine("--- Validation ---");
            var errors = ShotlistParser.ValidateShotlist(shotlist);
            if (errors.Count == 0)
            {
                Console.WriteLine("✓ Shotlist is valid!");
            }
            else
            {
                Console.WriteLine("⚠ Validation warnings:");
                foreach (var error in errors)
                {
                    Console.WriteLine($"  - {error}");
                }
            }
            Console.WriteLine();

            // 7. Save shotlist as JSON
            var outputDir = Path.Combine(AppDomain.CurrentDomain.BaseDirectory, "output", "llm-example");
            Directory.CreateDirectory(outputDir);

            var jsonPath = Path.Combine(outputDir, "shotlist.json");
            var jsonOutput = ShotlistParser.SerializeToJson(shotlist);
            await File.WriteAllTextAsync(jsonPath, jsonOutput);
            Console.WriteLine($"Shotlist saved to: {jsonPath}");

            // 8. Demonstrate refining a shot
            Console.WriteLine("\n--- Refining Shot Details ---");
            Console.WriteLine("Generating enhanced camera direction for shot 1...");
            var refinedDirection = await shotlistGenerator.GenerateCameraDirectionAsync(shotlist.Shots[0]);
            Console.WriteLine($"Shot Type: {refinedDirection.ShotType}");
            Console.WriteLine($"Angle: {refinedDirection.Angle}");
            Console.WriteLine($"Movement: {refinedDirection.Movement}");
            Console.WriteLine($"Notes: {refinedDirection.Notes}");

            Console.WriteLine("\n=== Example Complete ===");
        }
    }
}
