using System;
using System.IO;
using System.Threading.Tasks;
using StoryGenerator.Generators;
using StoryGenerator.Models;

namespace SceneBeatsTest
{
    class Program
    {
        static async Task Main(string[] args)
        {
            Console.WriteLine("=== Scene Beats and Subtitles Test ===\n");

            // Setup paths - use repository root
            var repoRoot = Path.GetFullPath(Path.Combine(AppDomain.CurrentDomain.BaseDirectory, "..", "..", "..", "..", "..", ".."));
            var scenesPath = Path.Combine(repoRoot, "scenes");
            var subtitlesPath = Path.Combine(repoRoot, "subtitles");

            Console.WriteLine($"Repository root: {repoRoot}");
            Console.WriteLine($"Scenes path: {scenesPath}");
            Console.WriteLine($"Subtitles path: {subtitlesPath}\n");

            // Sample script
            var scriptText = @"In a world where books are banned and libraries are just distant memories, one woman refuses to let knowledge die. 
Sarah, the last librarian, guards an underground library hidden beneath an abandoned subway station. 
Every night, she risks everything to preserve humanity's greatest treasure—our stories, our history, our truth. 
The authorities are closing in, but Sarah knows that as long as one person remembers, hope survives. 
Tonight, she makes her final stand, not with weapons, but with words.";

            // Create test script version
            var scriptVersion = new ScriptVersion
            {
                TitleId = "test_story_001",
                Title = "The Last Librarian",
                Content = scriptText,
                TargetAudience = new AudienceSegment("women", "18-23"),
                Version = "v1"
            };

            var audioDuration = 58.5f; // Estimated duration in seconds

            Console.WriteLine("Script Information:");
            Console.WriteLine($"  Title: {scriptVersion.Title}");
            Console.WriteLine($"  Title ID: {scriptVersion.TitleId}");
            Console.WriteLine($"  Audience: {scriptVersion.TargetAudience}");
            Console.WriteLine($"  Audio Duration: {audioDuration}s");
            Console.WriteLine($"  Word Count: {scriptText.Split(' ').Length} words\n");

            // ===== PART 1: Generate Subtitles =====
            Console.WriteLine("--- Generating Draft Subtitles ---");
            try
            {
                var subtitleGenerator = new SubtitleGenerator(subtitlesPath);
                var srtPath = await subtitleGenerator.GenerateFromScriptVersionAsync(
                    scriptVersion,
                    audioDuration
                );

                Console.WriteLine($"✓ Subtitles saved to: {srtPath}");
                
                // Display first few lines of SRT
                if (File.Exists(srtPath))
                {
                    var srtContent = await File.ReadAllTextAsync(srtPath);
                    var lines = srtContent.Split('\n').Take(20);
                    Console.WriteLine("\nFirst subtitle entries:");
                    Console.WriteLine(new string('-', 60));
                    foreach (var line in lines)
                    {
                        Console.WriteLine(line);
                    }
                    Console.WriteLine(new string('-', 60));
                }
            }
            catch (Exception ex)
            {
                Console.WriteLine($"✗ Subtitle generation failed: {ex.Message}");
                Console.WriteLine(ex.StackTrace);
            }
            Console.WriteLine();

            // ===== PART 2: Generate Scene Beats =====
            Console.WriteLine("--- Generating Scene Beat-Sheet ---");
            try
            {
                var beatsGenerator = new SimpleSceneBeatsGenerator(scenesPath);
                var shotsPath = await beatsGenerator.GenerateFromScriptVersionAsync(
                    scriptVersion,
                    audioDuration
                );

                Console.WriteLine($"✓ Beat-sheet saved to: {shotsPath}");
                
                // Display JSON content
                if (File.Exists(shotsPath))
                {
                    var jsonContent = await File.ReadAllTextAsync(shotsPath);
                    Console.WriteLine("\nGenerated JSON:");
                    Console.WriteLine(new string('-', 60));
                    Console.WriteLine(jsonContent);
                    Console.WriteLine(new string('-', 60));
                }
            }
            catch (Exception ex)
            {
                Console.WriteLine($"✗ Scene beats generation failed: {ex.Message}");
                Console.WriteLine(ex.StackTrace);
            }

            Console.WriteLine("\n=== Test Complete ===");
        }
    }
}
