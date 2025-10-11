using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text.Json;
using System.Text.Json.Serialization;

namespace PrismQ.Shared.Models;

/// <summary>
/// Represents a story idea with metadata and viral potential scoring.
/// Ported from Python Models/StoryIdea.py with C# enhancements.
/// </summary>
public class StoryIdea
{
    /// <summary>
    /// Gets or sets the title of the story.
    /// </summary>
    [JsonPropertyName("story_title")]
    public string StoryTitle { get; set; } = string.Empty;

    /// <summary>
    /// Gets or sets the narrator's gender (e.g., "male", "female").
    /// </summary>
    [JsonPropertyName("narrator_gender")]
    public string NarratorGender { get; set; } = string.Empty;

    /// <summary>
    /// Gets or sets the tone of the story (e.g., "emotional, heartwarming").
    /// </summary>
    [JsonPropertyName("tone")]
    public string? Tone { get; set; }

    /// <summary>
    /// Gets or sets the theme of the story (e.g., "friendship, acceptance").
    /// </summary>
    [JsonPropertyName("theme")]
    public string? Theme { get; set; }

    /// <summary>
    /// Gets or sets the narrator type (e.g., "first-person", "third-person").
    /// </summary>
    [JsonPropertyName("narrator_type")]
    public string? NarratorType { get; set; }

    /// <summary>
    /// Gets or sets the other main character in the story.
    /// </summary>
    [JsonPropertyName("other_character")]
    public string? OtherCharacter { get; set; }

    /// <summary>
    /// Gets or sets the key plot outcome.
    /// </summary>
    [JsonPropertyName("outcome")]
    public string? Outcome { get; set; }

    /// <summary>
    /// Gets or sets the emotional core of the story.
    /// </summary>
    [JsonPropertyName("emotional_core")]
    public string? EmotionalCore { get; set; }

    /// <summary>
    /// Gets or sets the power dynamic between characters.
    /// </summary>
    [JsonPropertyName("power_dynamic")]
    public string? PowerDynamic { get; set; }

    /// <summary>
    /// Gets or sets the timeline of the story.
    /// </summary>
    [JsonPropertyName("timeline")]
    public string? Timeline { get; set; }

    /// <summary>
    /// Gets or sets the type of twist in the story.
    /// </summary>
    [JsonPropertyName("twist_type")]
    public string? TwistType { get; set; }

    /// <summary>
    /// Gets or sets the character arc.
    /// </summary>
    [JsonPropertyName("character_arc")]
    public string? CharacterArc { get; set; }

    /// <summary>
    /// Gets or sets the voice style for narration.
    /// </summary>
    [JsonPropertyName("voice_style")]
    public string? VoiceStyle { get; set; }

    /// <summary>
    /// Gets or sets the target moral or message.
    /// </summary>
    [JsonPropertyName("target_moral")]
    public string? TargetMoral { get; set; }

    /// <summary>
    /// Gets or sets the locations featured in the story.
    /// </summary>
    [JsonPropertyName("locations")]
    public string? Locations { get; set; }

    /// <summary>
    /// Gets or sets any brands mentioned in the story.
    /// </summary>
    [JsonPropertyName("mentioned_brands")]
    public string? MentionedBrands { get; set; }

    /// <summary>
    /// Gets or sets the goal or purpose of the story.
    /// </summary>
    [JsonPropertyName("goal")]
    public string? Goal { get; set; }

    /// <summary>
    /// Gets or sets the language code (e.g., "en", "es", "fr").
    /// Default is "en" for English.
    /// </summary>
    [JsonPropertyName("language")]
    public string Language { get; set; } = "en";

    /// <summary>
    /// Gets or sets personalization replacements for the story.
    /// Key-value pairs where keys are placeholders and values are replacement text.
    /// </summary>
    [JsonPropertyName("personalization")]
    public Dictionary<string, string> Personalization { get; set; } = new();

    /// <summary>
    /// Gets or sets the video style (e.g., "cinematic", "documentary").
    /// Default is "cinematic".
    /// </summary>
    [JsonPropertyName("video_style")]
    public string VideoStyle { get; set; } = "cinematic";

    /// <summary>
    /// Gets or sets the voice stability parameter (0.0 to 1.0).
    /// Default is 0.5.
    /// </summary>
    [JsonPropertyName("voice_stability")]
    public float VoiceStability { get; set; } = 0.5f;

    /// <summary>
    /// Gets or sets the voice similarity boost parameter (0.0 to 1.0).
    /// Default is 0.75.
    /// </summary>
    [JsonPropertyName("voice_similarity_boost")]
    public float VoiceSimilarityBoost { get; set; } = 0.75f;

    /// <summary>
    /// Gets or sets the voice style exaggeration parameter (0.0 to 1.0).
    /// Default is 0.0.
    /// </summary>
    [JsonPropertyName("voice_style_exaggeration")]
    public float VoiceStyleExaggeration { get; set; } = 0.0f;

    /// <summary>
    /// Gets or sets the viral potential scores across platforms, regions, age groups, and gender.
    /// </summary>
    [JsonPropertyName("potencial")]
    public ViralPotential Potential { get; set; } = new();

    /// <summary>
    /// Gets or sets optional reference to source content statistics.
    /// Used when the story idea originated from specific platform content (Reddit, YouTube, etc.).
    /// Enables tracking input quality and comparing with output performance.
    /// </summary>
    [JsonPropertyName("source_stats")]
    public SourceStats? SourceStats { get; set; }

    /// <summary>
    /// Gets or sets title suggestions with scores.
    /// List of alternative titles ranked by viral potential.
    /// Allows A/B testing and selection of the best performing title.
    /// </summary>
    [JsonPropertyName("title_suggestions")]
    public List<ScoredString>? TitleSuggestions { get; set; }

    /// <summary>
    /// Gets or sets scored tags/themes for the story.
    /// Helps with categorization, trend alignment, and SEO optimization.
    /// Tags ranked by relevance and viral potential.
    /// </summary>
    [JsonPropertyName("scored_tags")]
    public List<ScoredString>? ScoredTags { get; set; }

    /// <summary>
    /// Calculates the overall viral potential score based on key metrics.
    /// </summary>
    public int CalculateOverallPotential()
    {
        var scores = new List<int>
        {
            Potential.AgeGroups.GetValueOrDefault("10_15", 0),
            Potential.AgeGroups.GetValueOrDefault("15_20", 0),
            Potential.Regions.GetValueOrDefault("US", 0),
            Potential.Platforms.GetValueOrDefault("youtube", 0),
            Potential.Gender.GetValueOrDefault("woman", 0)
        };

        return scores.Count > 0 ? (int)Math.Round(scores.Average()) : 0;
    }

    /// <summary>
    /// Loads a StoryIdea from a JSON file.
    /// </summary>
    /// <param name="filepath">Path to the JSON file.</param>
    /// <returns>The deserialized StoryIdea object.</returns>
    public static async Task<StoryIdea> FromFileAsync(string filepath)
    {
        var json = await File.ReadAllTextAsync(filepath);
        var idea = JsonSerializer.Deserialize<StoryIdea>(json, new JsonSerializerOptions
        {
            PropertyNameCaseInsensitive = true
        }) ?? throw new InvalidOperationException($"Failed to deserialize StoryIdea from {filepath}");

        // Calculate overall potential after loading
        idea.Potential.Overall = idea.CalculateOverallPotential();
        return idea;
    }

    /// <summary>
    /// Saves the StoryIdea to a JSON file.
    /// </summary>
    /// <param name="outputPath">Path to save the JSON file.</param>
    public async Task ToFileAsync(string outputPath)
    {
        // Ensure overall potential is calculated
        Potential.Overall = CalculateOverallPotential();

        var directory = Path.GetDirectoryName(outputPath);
        if (!string.IsNullOrEmpty(directory))
        {
            Directory.CreateDirectory(directory);
        }

        var options = new JsonSerializerOptions
        {
            WriteIndented = true,
            Encoder = System.Text.Encodings.Web.JavaScriptEncoder.UnsafeRelaxedJsonEscaping
        };

        var json = JsonSerializer.Serialize(this, options);
        await File.WriteAllTextAsync(outputPath, json);
    }

    /// <summary>
    /// Returns a string representation of the StoryIdea.
    /// </summary>
    public override string ToString()
    {
        return $"StoryIdea(StoryTitle='{StoryTitle}', OverallPotential={Potential.Overall})";
    }
}

/// <summary>
/// Represents viral potential scoring across different dimensions.
/// </summary>
public class ViralPotential
{
    /// <summary>
    /// Gets or sets the overall viral potential score (0-100).
    /// </summary>
    [JsonPropertyName("overall")]
    public int Overall { get; set; }

    /// <summary>
    /// Gets or sets platform-specific scores.
    /// </summary>
    [JsonPropertyName("platforms")]
    public Dictionary<string, int> Platforms { get; set; } = new()
    {
        { "youtube", 0 },
        { "tiktok", 0 },
        { "instagram", 0 }
    };

    /// <summary>
    /// Gets or sets region-specific scores.
    /// </summary>
    [JsonPropertyName("regions")]
    public Dictionary<string, int> Regions { get; set; } = new()
    {
        { "US", 0 },
        { "AU", 0 },
        { "GB", 0 }
    };

    /// <summary>
    /// Gets or sets age group scores.
    /// </summary>
    [JsonPropertyName("age_groups")]
    public Dictionary<string, int> AgeGroups { get; set; } = new()
    {
        { "10_15", 0 },
        { "15_20", 0 },
        { "20_25", 0 },
        { "25_30", 0 },
        { "30_50", 0 },
        { "50_70", 0 }
    };

    /// <summary>
    /// Gets or sets gender-specific scores.
    /// </summary>
    [JsonPropertyName("gender")]
    public Dictionary<string, int> Gender { get; set; } = new()
    {
        { "woman", 0 },
        { "man", 0 }
    };

    /// <summary>
    /// Calculates the overall viral potential score from all category scores.
    /// Takes the average of all non-zero scores across platforms, regions, age groups, and gender.
    /// </summary>
    /// <returns>The calculated overall score (0-100).</returns>
    public int CalculateOverall()
    {
        var allScores = new List<int>();

        // Add all platform scores
        allScores.AddRange(Platforms.Values.Where(v => v > 0));

        // Add all region scores
        allScores.AddRange(Regions.Values.Where(v => v > 0));

        // Add all age group scores
        allScores.AddRange(AgeGroups.Values.Where(v => v > 0));

        // Add all gender scores
        allScores.AddRange(Gender.Values.Where(v => v > 0));

        // Return average if we have scores, otherwise 0
        return allScores.Count > 0 ? (int)Math.Round(allScores.Average()) : 0;
    }
}
