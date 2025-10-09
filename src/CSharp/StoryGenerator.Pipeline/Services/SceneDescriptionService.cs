using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text.Json;
using System.Threading.Tasks;
using StoryGenerator.Core.Interfaces;
using StoryGenerator.Pipeline.Config;

namespace StoryGenerator.Pipeline.Services;

/// <summary>
/// Service for generating visual descriptions and prompts for scenes.
/// </summary>
public class SceneDescriptionService
{
    private readonly PathsConfig _paths;

    public SceneDescriptionService(PathsConfig paths)
    {
        _paths = paths ?? throw new ArgumentNullException(nameof(paths));
    }

    /// <summary>
    /// Generate visual descriptions for scenes in a shotlist.
    /// </summary>
    /// <param name="storyTitle">The story title</param>
    /// <returns>Updated shotlist with visual prompts</returns>
    public async Task<Shotlist> DescribeScenesAsync(string storyTitle)
    {
        Console.WriteLine($"Generating scene descriptions for: {storyTitle}");

        // Load shotlist
        var shotlistPath = Path.Combine(_paths.StoryRoot, _paths.Scenes, $"{storyTitle}_scenes.json");
        if (!File.Exists(shotlistPath))
        {
            throw new FileNotFoundException($"Shotlist not found: {shotlistPath}");
        }

        var json = await File.ReadAllTextAsync(shotlistPath);
        var shotlist = JsonSerializer.Deserialize<Shotlist>(json);
        
        if (shotlist == null || shotlist.Shots == null)
        {
            throw new InvalidOperationException("Failed to parse shotlist");
        }

        // Generate visual prompts for each scene
        foreach (var shot in shotlist.Shots)
        {
            shot.VisualPrompt = GenerateVisualPrompt(shot);
            shot.Mood = DetermineMood(shot.SceneDescription);
            shot.CameraAngle = DetermineCameraAngle(shot.ShotNumber, shotlist.Shots.Count);
            shot.Lighting = DetermineLighting(shot.Mood);
        }

        // Save updated shotlist
        await SaveShotlistAsync(shotlist, shotlistPath);

        Console.WriteLine($"✅ Scene descriptions generated for {shotlist.Shots.Count} scenes");
        return shotlist;
    }

    private string GenerateVisualPrompt(Shot shot)
    {
        // Generate a visual prompt based on the scene description
        // This is a simplified version - in production, you'd use an LLM
        var basePrompt = shot.SceneDescription;
        
        // Add cinematic qualities
        var visualElements = new List<string>
        {
            "cinematic lighting",
            "professional cinematography",
            "high detail",
            "vertical video format 9:16",
            "4k quality"
        };

        return $"{basePrompt}, {string.Join(", ", visualElements)}";
    }

    private string DetermineMood(string description)
    {
        // Simple keyword-based mood detection
        var lowerDesc = description.ToLower();

        if (lowerDesc.Contains("happy") || lowerDesc.Contains("joy") || lowerDesc.Contains("celebration"))
            return "joyful";
        if (lowerDesc.Contains("sad") || lowerDesc.Contains("cry") || lowerDesc.Contains("tears"))
            return "melancholic";
        if (lowerDesc.Contains("tense") || lowerDesc.Contains("danger") || lowerDesc.Contains("threat"))
            return "tense";
        if (lowerDesc.Contains("peaceful") || lowerDesc.Contains("calm") || lowerDesc.Contains("serene"))
            return "peaceful";
        if (lowerDesc.Contains("mysterious") || lowerDesc.Contains("unknown") || lowerDesc.Contains("secret"))
            return "mysterious";

        return "neutral";
    }

    private string DetermineCameraAngle(int shotNumber, int totalShots)
    {
        // Vary camera angles for visual interest
        var angles = new[]
        {
            "wide angle establishing shot",
            "medium shot",
            "close-up",
            "over the shoulder",
            "bird's eye view",
            "low angle"
        };

        // First and last shots are typically wide establishing shots
        if (shotNumber == 0)
            return angles[0];
        if (shotNumber == totalShots - 1)
            return "wide angle concluding shot";

        // Cycle through other angles for middle shots
        return angles[1 + (shotNumber % (angles.Length - 1))];
    }

    private string DetermineLighting(string mood)
    {
        return mood switch
        {
            "joyful" => "bright, warm lighting, golden hour",
            "melancholic" => "soft, diffused lighting, blue tones",
            "tense" => "dramatic shadows, high contrast",
            "peaceful" => "soft, natural lighting",
            "mysterious" => "dim lighting with dramatic shadows",
            _ => "natural, balanced lighting"
        };
    }

    private async Task SaveShotlistAsync(Shotlist shotlist, string outputPath)
    {
        var directory = Path.GetDirectoryName(outputPath);
        if (!string.IsNullOrEmpty(directory) && !Directory.Exists(directory))
        {
            Directory.CreateDirectory(directory);
        }

        var json = JsonSerializer.Serialize(shotlist, new JsonSerializerOptions
        {
            WriteIndented = true
        });

        await File.WriteAllTextAsync(outputPath, json);
    }
}
