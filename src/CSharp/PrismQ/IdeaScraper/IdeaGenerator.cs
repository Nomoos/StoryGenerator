using System.Text.Json;
using Microsoft.Extensions.Logging;
using PrismQ.Shared.Models;
using PrismQ.Shared.Core.Services;
using PrismQ.Shared.Core;
using StoryGenerator.Providers.OpenAI;

namespace PrismQ.IdeaScraper;

/// <summary>
/// Generates story ideas with viral potential scoring.
/// Ported from Python Generators/GStoryIdeas.py with C# enhancements.
/// </summary>
public class IdeaGenerator : IIdeaGenerator
{
    private readonly OpenAIClient _openAIClient;
    private readonly ILogger<IdeaGenerator> _logger;
    private readonly PerformanceMonitor _performanceMonitor;
    private readonly PathConfiguration _pathConfiguration;

    public string Name => "IdeaGenerator";
    public string Version => "1.0.0";

    public IdeaGenerator(
        OpenAIClient openAIClient,
        ILogger<IdeaGenerator> logger,
        PerformanceMonitor performanceMonitor,
        PathConfiguration pathConfiguration)
    {
        _openAIClient = openAIClient;
        _logger = logger;
        _performanceMonitor = performanceMonitor;
        _pathConfiguration = pathConfiguration;
    }

    /// <summary>
    /// Generates story ideas based on a topic.
    /// </summary>
    public async Task<List<StoryIdea>> GenerateIdeasAsync(
        string topic,
        int count = 5,
        string? tone = null,
        string? theme = null,
        CancellationToken cancellationToken = default)
    {
        return await _performanceMonitor.MeasureAsync(
            "Idea_Generation",
            topic,
            async () => await GenerateIdeasInternalAsync(topic, count, tone, theme, cancellationToken),
            new Dictionary<string, object> { { "count", count } });
    }

    private async Task<List<StoryIdea>> GenerateIdeasInternalAsync(
        string topic,
        int count,
        string? tone,
        string? theme,
        CancellationToken cancellationToken)
    {
        var prompt = BuildPrompt(topic, count, tone, theme);
        var messages = new List<ChatMessage>
        {
            ChatMessage.User(prompt)
        };

        _logger.LogInformation("Generating {Count} story ideas for topic: {Topic}", count, topic);

        var response = await _openAIClient.CreateChatCompletionAsync(
            messages,
            temperature: 0.9f,
            cancellationToken: cancellationToken);

        var content = response.Choices.FirstOrDefault()?.Message.Content
            ?? throw new InvalidOperationException("No response from OpenAI");

        // Parse JSON response
        var ideas = ParseIdeasFromResponse(content);

        _logger.LogInformation("✅ Generated {Count} story ideas for topic '{Topic}'", ideas.Count, topic);

        return ideas;
    }

    /// <summary>
    /// Generates story ideas and saves them to files.
    /// </summary>
    public async Task<List<string>> GenerateAndSaveIdeasAsync(
        string topic,
        string outputDirectory,
        int count = 5,
        string? tone = null,
        string? theme = null,
        CancellationToken cancellationToken = default)
    {
        var ideas = await GenerateIdeasAsync(topic, count, tone, theme, cancellationToken);
        var savedPaths = new List<string>();

        foreach (var idea in ideas)
        {
            var sanitizedTitle = FileHelper.SanitizeFilename(idea.StoryTitle);
            var filePath = Path.Combine(outputDirectory, $"{sanitizedTitle}.json");
            
            await idea.ToFileAsync(filePath);
            savedPaths.Add(filePath);
            
            _logger.LogInformation("Saved idea: {FilePath}", filePath);
        }

        return savedPaths;
    }

    /// <summary>
    /// Builds the prompt for story idea generation.
    /// </summary>
    private string BuildPrompt(string topic, int count, string? tone, string? theme)
    {
        return $@"You are a viral story idea generator for short vertical video scripts (TikTok, Reels, Shorts).

Your task is to generate exactly {count} unique, dramatic story ideas inspired by this topic: ""{topic}"".

Each idea must be a JSON object with the following structure:

- story_title: string (REQUIRED)  
  – should be longer than a short phrase (ideally 70–100 characters)  
  – must follow YouTube title standards: emotionally engaging, curiosity-driven, yet clear and natural  
  – avoid clickbait, all caps, emojis, or excessive punctuation
- tone: string (optional)
- theme: string (optional)
- narrator_type: string (optional)
- narrator_gender: string (REQUIRED, male or female)
- other_character: string (optional)
- outcome: string (optional)
- emotional_core: string (optional)
- power_dynamic: string (optional)
- timeline: string (optional)
- twist_type: string (optional)
- character_arc: string (optional)
- voice_style: string (optional)
- target_moral: string (optional)
- locations: string (optional)
- mentioned_brands: string (optional)
- goal: string (optional)
- potencial: object (REQUIRED) – pessimistic virality estimate with the following structure:

   ""potencial"": {{
            ""platforms"": {{
              ""youtube"": integer (0–100),
              ""tiktok"": integer (0–100),
              ""instagram"": integer (0–100)
            }},
            ""regions"": {{
              ""US"": integer (0–100),
              ""AU"": integer (0–100),
              ""GB"": integer (0–100)
            }},
            ""age_groups"": {{
              ""10_15"": integer (0–100),
              ""15_20"": integer (0–100),
              ""20_25"": integer (0–100),
              ""25_30"": integer (0–100),
              ""30_50"": integer (0–100),
              ""50_70"": integer (0–100)
            }},
            ""gender"": {{
              ""man"": integer (0–100),
              ""woman"": integer (0–100)
            }}
          }}

All numbers represent pessimistic estimates of how viral the idea could be in that segment.

Respond with a JSON array containing exactly {count} story idea objects, and nothing else. Do not explain the list.

Optional context:
Tone: {tone ?? "any"}
Theme: {theme ?? "any"}".Trim();
    }

    /// <summary>
    /// Parses story ideas from the OpenAI response.
    /// </summary>
    private List<StoryIdea> ParseIdeasFromResponse(string response)
    {
        // Clean up the response - remove markdown code blocks if present
        var cleaned = response.Trim()
            .Replace("```json", "")
            .Replace("```", "")
            .Trim();

        try
        {
            var ideas = JsonSerializer.Deserialize<List<StoryIdea>>(cleaned, new JsonSerializerOptions
            {
                PropertyNameCaseInsensitive = true
            });

            if (ideas == null || ideas.Count == 0)
            {
                throw new InvalidOperationException("No ideas were parsed from the response");
            }

            // Calculate overall potential for each idea
            foreach (var idea in ideas)
            {
                idea.Potential.Overall = idea.CalculateOverallPotential();
            }

            return ideas;
        }
        catch (JsonException ex)
        {
            _logger.LogError(ex, "Failed to parse ideas from response: {Response}", cleaned);
            throw new InvalidOperationException($"Invalid JSON from OpenAI: {cleaned}", ex);
        }
    }
}
