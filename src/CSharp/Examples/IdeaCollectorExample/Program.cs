using System;
using System.Collections.Generic;
using System.IO;
using System.Threading.Tasks;
using StoryGenerator.Core.Collectors;
using StoryGenerator.Core.Models;
using StoryGenerator.Core.Services;

namespace StoryGenerator.Examples;

/// <summary>
/// Example demonstrating the Idea Collector system.
/// Shows how to collect sources, transform them into ideas, score them, and query the registry.
/// </summary>
public class IdeaCollectorExample
{
    public static async Task Main(string[] args)
    {
        Console.WriteLine("=== Idea Collector System Example ===\n");

        // Step 1: Create example sources (normally these would come from APIs)
        Console.WriteLine("Step 1: Creating example sources...");
        var sources = CreateExampleSources();
        Console.WriteLine($"Created {sources.Count} source(s)\n");

        // Step 2: Initialize collector
        Console.WriteLine("Step 2: Initializing ManualIdeaCollector...");
        var collector = new ManualIdeaCollector();
        Console.WriteLine($"Collector: {collector.Name} v{collector.Version}");
        Console.WriteLine($"Source Type: {collector.SourceType}\n");

        // Step 3: Transform sources into ideas
        Console.WriteLine("Step 3: Transforming sources into original ideas...");
        var parameters = new Dictionary<string, object>
        {
            { "sources", sources }
        };
        var ideas = await collector.CollectAndTransformAsync(parameters);
        Console.WriteLine($"Generated {ideas.Count} idea(s)\n");

        // Step 4: Display generated ideas
        Console.WriteLine("Step 4: Displaying generated ideas...");
        foreach (var idea in ideas)
        {
            DisplayIdea(idea);
        }

        // Step 5: Register ideas in central registry
        Console.WriteLine("\nStep 5: Registering ideas in central registry...");
        var registry = new IdeaCollectorRegistry();
        registry.RegisterIdeas(ideas);
        Console.WriteLine($"Registry now contains {registry.TotalIdeas} idea(s)");
        Console.WriteLine("\nCollector Statistics:");
        foreach (var stat in registry.CollectorStats)
        {
            Console.WriteLine($"  {stat.Key}: {stat.Value} ideas");
        }

        // Step 6: Query and filter ideas
        Console.WriteLine("\n=== Querying Ideas ===\n");

        // Top ideas
        Console.WriteLine("Top 3 Ideas by Overall Score:");
        var topIdeas = registry.GetTopIdeas(3);
        foreach (var idea in topIdeas)
        {
            Console.WriteLine($"  - Overall: {idea.ViralPotential.Overall} | {idea.IdeaContent}");
        }

        // High scoring ideas
        Console.WriteLine("\nIdeas with Overall Score >= 50:");
        var highScoring = registry.GetIdeasByMinScore(50);
        foreach (var idea in highScoring)
        {
            Console.WriteLine($"  - Overall: {idea.ViralPotential.Overall} | {idea.IdeaContent}");
        }

        // Category filtering
        Console.WriteLine("\nIdeas scoring high with women aged 15-20:");
        var categoryFilters = new Dictionary<string, int>
        {
            { "gender_woman", 60 },
            { "age_15_20", 60 }
        };
        var filteredIdeas = registry.GetIdeasByCategoryScores(categoryFilters);
        foreach (var idea in filteredIdeas)
        {
            Console.WriteLine($"  - Women: {idea.ViralPotential.Gender["woman"]}, " +
                            $"Age 15-20: {idea.ViralPotential.AgeGroups["15_20"]} | {idea.IdeaContent}");
        }

        // Step 7: Export to JSON
        Console.WriteLine("\n=== Exporting Registry ===\n");
        var json = registry.ToJson();
        var outputPath = Path.Combine(Path.GetTempPath(), "idea_registry_example.json");
        await File.WriteAllTextAsync(outputPath, json);
        Console.WriteLine($"Registry exported to: {outputPath}");
        Console.WriteLine($"File size: {new FileInfo(outputPath).Length} bytes");

        Console.WriteLine("\n=== Example Complete ===");
    }

    /// <summary>
    /// Creates example sources that simulate data from various sources.
    /// In a real application, these would be fetched from APIs or scraping.
    /// </summary>
    private static List<IdeaSource> CreateExampleSources()
    {
        return new List<IdeaSource>
        {
            new IdeaSource
            {
                Title = "Best Friend Betrayed Me at My Wedding",
                OriginalText = "My best friend of 10 years told everyone my biggest secret right before I walked down the aisle. " +
                              "I had to continue with the wedding but everyone kept staring at me. " +
                              "I don't know if I can ever forgive her.",
                SourceType = "reddit",
                SourceUrl = "https://reddit.com/r/relationships/example1",
                Author = "throwaway_bride123",
                Tags = new List<string> { "betrayal", "friendship", "wedding", "secrets" },
                QuestionableAuthorship = false
            },
            new IdeaSource
            {
                Title = "Discovered My Parents Lied About My Adoption",
                OriginalText = "I found out at age 25 that I was adopted, but my parents never told me. " +
                              "They had the chance to tell me thousands of times but chose not to. " +
                              "Now I don't know who I really am and I feel betrayed by the people I trusted most.",
                SourceType = "reddit",
                SourceUrl = "https://reddit.com/r/TrueOffMyChest/example2",
                Author = "confused_adoptee",
                Tags = new List<string> { "adoption", "family", "identity", "betrayal" },
                QuestionableAuthorship = false
            },
            new IdeaSource
            {
                Title = "My Teacher Changed My Life with One Sentence",
                OriginalText = "I was about to drop out of school when my teacher pulled me aside and said something " +
                              "that completely changed my perspective. It's been 5 years and I still think about " +
                              "that moment every day.",
                SourceType = "instagram",
                SourceUrl = "https://instagram.com/stories/example",
                Author = "inspirational_stories",
                Tags = new List<string> { "inspiration", "education", "transformation", "gratitude" },
                QuestionableAuthorship = false
            },
            new IdeaSource
            {
                Title = "This Content Has Questionable Origins",
                OriginalText = "Some story content that we're not sure about the copyright status...",
                SourceType = "unknown",
                Tags = new List<string> { "questionable" },
                QuestionableAuthorship = true  // This will be filtered out
            }
        };
    }

    /// <summary>
    /// Displays detailed information about a collected idea.
    /// </summary>
    private static void DisplayIdea(CollectedIdea idea)
    {
        Console.WriteLine("─────────────────────────────────────────────────────");
        Console.WriteLine($"Idea ID: {idea.Id}");
        Console.WriteLine($"Collector: {idea.CollectorName}");
        Console.WriteLine($"Created: {idea.CreatedAt:yyyy-MM-dd HH:mm:ss}");
        
        if (idea.Source != null)
        {
            Console.WriteLine($"\nSource Information:");
            Console.WriteLine($"  Title: {idea.Source.Title}");
            Console.WriteLine($"  Type: {idea.Source.SourceType}");
            Console.WriteLine($"  URL: {idea.Source.SourceUrl ?? "N/A"}");
            Console.WriteLine($"  Tags: {string.Join(", ", idea.Source.Tags)}");
        }

        Console.WriteLine($"\nTransformed Idea:");
        Console.WriteLine($"  {idea.IdeaContent}");

        if (!string.IsNullOrWhiteSpace(idea.TransformationNotes))
        {
            Console.WriteLine($"\nTransformation Notes:");
            Console.WriteLine($"  {idea.TransformationNotes}");
        }

        Console.WriteLine($"\nViral Potential Scores:");
        Console.WriteLine($"  Overall: {idea.ViralPotential.Overall}");
        
        Console.WriteLine($"\n  Gender:");
        foreach (var kvp in idea.ViralPotential.Gender)
        {
            if (kvp.Value > 0)
                Console.WriteLine($"    {kvp.Key}: {kvp.Value}");
        }

        Console.WriteLine($"\n  Age Groups:");
        foreach (var kvp in idea.ViralPotential.AgeGroups)
        {
            if (kvp.Value > 0)
                Console.WriteLine($"    {kvp.Key}: {kvp.Value}");
        }

        Console.WriteLine($"\n  Platforms:");
        foreach (var kvp in idea.ViralPotential.Platforms)
        {
            if (kvp.Value > 0)
                Console.WriteLine($"    {kvp.Key}: {kvp.Value}");
        }

        Console.WriteLine($"\n  Regions:");
        foreach (var kvp in idea.ViralPotential.Regions)
        {
            if (kvp.Value > 0)
                Console.WriteLine($"    {kvp.Key}: {kvp.Value}");
        }

        Console.WriteLine();
    }
}
