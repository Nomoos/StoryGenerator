using System;
using System.Threading.Tasks;
using StoryGenerator.Generators;
using StoryGenerator.Models;

namespace StoryGenerator.Examples
{
    /// <summary>
    /// Example program demonstrating the content generation pipeline.
    /// </summary>
    public class ContentGenerationExample
    {
        public static async Task Main(string[] args)
        {
            Console.WriteLine("=== StoryGenerator Content Generation Example ===\n");

            // Define output directories (use absolute paths in production)
            var baseDir = args.Length > 0 ? args[0] : "/tmp/storygen_test";
            var ideasDir = $"{baseDir}/ideas";
            var topicsDir = $"{baseDir}/topics";
            var titlesDir = $"{baseDir}/titles";

            // Create generators
            var ideaGenerator = new IdeaGenerator();
            var topicGenerator = new TopicGenerator();
            var titleGenerator = new TitleGenerator();

            Console.WriteLine($"Output directory: {baseDir}\n");

            // Example 1: Generate content for a single segment
            await GenerateSingleSegmentExample(
                ideaGenerator,
                topicGenerator,
                titleGenerator,
                ideasDir,
                topicsDir,
                titlesDir);

            Console.WriteLine("\n" + new string('-', 60) + "\n");

            // Example 2: Generate content for all segments
            await GenerateAllSegmentsExample(
                ideaGenerator,
                topicGenerator,
                titleGenerator,
                ideasDir,
                topicsDir,
                titlesDir);

            Console.WriteLine("\n=== Content Generation Complete ===");
        }

        private static async Task GenerateSingleSegmentExample(
            IdeaGenerator ideaGenerator,
            TopicGenerator topicGenerator,
            TitleGenerator titleGenerator,
            string ideasDir,
            string topicsDir,
            string titlesDir)
        {
            Console.WriteLine("Example 1: Generate content for a single segment (women, 18-23)");
            Console.WriteLine();

            var segment = new AudienceSegment("women", "18-23");

            // Step 1: Generate ideas
            Console.WriteLine($"Step 1: Generating ideas for {segment}...");
            var ideasPath = await ideaGenerator.GenerateAndSaveIdeasAsync(
                segment,
                ideasDir,
                minIdeas: 20);
            Console.WriteLine($"✓ Ideas saved to: {ideasPath}");

            // Step 2: Generate topics from ideas
            Console.WriteLine($"\nStep 2: Clustering ideas into topics...");
            var topicsPath = await topicGenerator.LoadIdeasAndGenerateTopicsAsync(
                ideasPath,
                segment,
                topicsDir,
                minTopics: 8);
            Console.WriteLine($"✓ Topics saved to: {topicsPath}");

            // Step 3: Generate titles from topics
            Console.WriteLine($"\nStep 3: Generating clickable titles...");
            var titlesPath = await titleGenerator.LoadTopicsAndGenerateTitlesAsync(
                topicsPath,
                segment,
                titlesDir,
                minTitles: 10);
            Console.WriteLine($"✓ Titles saved to: {titlesPath}");
        }

        private static async Task GenerateAllSegmentsExample(
            IdeaGenerator ideaGenerator,
            TopicGenerator topicGenerator,
            TitleGenerator titleGenerator,
            string ideasDir,
            string topicsDir,
            string titlesDir)
        {
            Console.WriteLine("Example 2: Generate content for all segments (batch processing)");
            Console.WriteLine();

            // Step 1: Generate ideas for all segments
            Console.WriteLine("Step 1: Generating ideas for all segments...");
            var ideaPaths = await ideaGenerator.GenerateIdeasForAllSegmentsAsync(
                ideasDir,
                minIdeas: 20);
            Console.WriteLine($"✓ Generated ideas for {ideaPaths.Count} segments");

            // Step 2: Generate topics for all segments
            Console.WriteLine("\nStep 2: Clustering ideas for all segments...");
            var topicPaths = await topicGenerator.GenerateTopicsForAllSegmentsAsync(
                ideasDir,
                topicsDir,
                minTopics: 8);
            Console.WriteLine($"✓ Generated topics for {topicPaths.Count} segments");

            // Step 3: Generate titles for all segments
            Console.WriteLine("\nStep 3: Generating titles for all segments...");
            var titlePaths = await titleGenerator.GenerateTitlesForAllSegmentsAsync(
                topicsDir,
                titlesDir,
                minTitles: 10);
            Console.WriteLine($"✓ Generated titles for {titlePaths.Count} segments");

            // Summary
            Console.WriteLine("\nSummary:");
            foreach (var segment in ideaGenerator.GetPredefinedSegments())
            {
                if (ideaPaths.ContainsKey(segment))
                {
                    Console.WriteLine($"  {segment}:");
                    Console.WriteLine($"    Ideas:  {ideaPaths[segment]}");
                    if (topicPaths.ContainsKey(segment))
                        Console.WriteLine($"    Topics: {topicPaths[segment]}");
                    if (titlePaths.ContainsKey(segment))
                        Console.WriteLine($"    Titles: {titlePaths[segment]}");
                }
            }
        }
    }
}
