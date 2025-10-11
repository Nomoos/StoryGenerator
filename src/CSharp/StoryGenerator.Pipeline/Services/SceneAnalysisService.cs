using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Threading.Tasks;
using PrismQ.Shared.Interfaces;
using PrismQ.Shared.Models;
using StoryGenerator.Pipeline.Config;

namespace StoryGenerator.Pipeline.Services;

/// <summary>
/// Service for analyzing scripts and generating scene breakdowns based on subtitles.
/// </summary>
public class SceneAnalysisService
{
    private readonly PathsConfig _paths;

    public SceneAnalysisService(PathsConfig paths)
    {
        _paths = paths ?? throw new ArgumentNullException(nameof(paths));
    }

    /// <summary>
    /// Analyze a story and generate scene breakdown.
    /// </summary>
    /// <param name="storyTitle">The story title</param>
    /// <returns>Shotlist with scene timing and descriptions</returns>
    public async Task<Shotlist> AnalyzeScenesAsync(string storyTitle)
    {
        Console.WriteLine($"Analyzing scenes for: {storyTitle}");

        // Load subtitle file (SRT format)
        var srtPath = Path.Combine(_paths.StoryRoot, _paths.Titles, $"{storyTitle}.srt");
        if (!File.Exists(srtPath))
        {
            throw new FileNotFoundException($"Subtitle file not found: {srtPath}");
        }

        // Load audio file to get total duration
        var audioPath = Path.Combine(_paths.StoryRoot, _paths.Voiceover, $"{storyTitle}.mp3");
        var duration = await GetAudioDurationAsync(audioPath);

        // Parse subtitles
        var subtitles = await ParseSubtitlesAsync(srtPath);
        
        // Segment into scenes (basic implementation: ~10-15 second scenes)
        var shots = SegmentIntoScenes(subtitles, duration);

        var shotlist = new Shotlist
        {
            StoryTitle = storyTitle,
            TotalDuration = duration,
            Shots = shots
        };

        // Save shotlist
        var outputPath = Path.Combine(_paths.StoryRoot, _paths.Scenes, $"{storyTitle}_scenes.json");
        await SaveShotlistAsync(shotlist, outputPath);

        Console.WriteLine($"✅ Scene analysis complete: {shots.Count} scenes");
        return shotlist;
    }

    private async Task<float> GetAudioDurationAsync(string audioPath)
    {
        if (!File.Exists(audioPath))
        {
            throw new FileNotFoundException($"Audio file not found: {audioPath}");
        }

        // For now, estimate from file size (rough approximation)
        // In production, use FFprobe or similar tool
        var fileInfo = new FileInfo(audioPath);
        var estimatedDuration = (float)(fileInfo.Length / 16000.0); // Rough estimate for MP3

        return await Task.FromResult(estimatedDuration);
    }

    private async Task<List<SubtitleEntry>> ParseSubtitlesAsync(string srtPath)
    {
        var entries = new List<SubtitleEntry>();
        var lines = await File.ReadAllLinesAsync(srtPath);

        SubtitleEntry? current = null;
        for (int i = 0; i < lines.Length; i++)
        {
            var line = lines[i].Trim();

            if (string.IsNullOrEmpty(line))
            {
                if (current != null)
                {
                    entries.Add(current);
                    current = null;
                }
                continue;
            }

            if (int.TryParse(line, out _))
            {
                current = new SubtitleEntry();
                continue;
            }

            if (line.Contains("-->") && current != null)
            {
                var parts = line.Split(new[] { "-->" }, StringSplitOptions.None);
                if (parts.Length == 2)
                {
                    current.StartTime = ParseTimestamp(parts[0].Trim());
                    current.EndTime = ParseTimestamp(parts[1].Trim());
                }
                continue;
            }

            if (current != null && current.StartTime > 0)
            {
                if (string.IsNullOrEmpty(current.Text))
                    current.Text = line;
                else
                    current.Text += " " + line;
            }
        }

        if (current != null)
        {
            entries.Add(current);
        }

        return entries;
    }

    private float ParseTimestamp(string timestamp)
    {
        // Format: 00:00:10,500 (hours:minutes:seconds,milliseconds)
        timestamp = timestamp.Replace(',', '.');
        var parts = timestamp.Split(':');
        
        if (parts.Length == 3)
        {
            var hours = float.Parse(parts[0]);
            var minutes = float.Parse(parts[1]);
            var seconds = float.Parse(parts[2]);
            return hours * 3600 + minutes * 60 + seconds;
        }

        return 0;
    }

    private List<Shot> SegmentIntoScenes(List<SubtitleEntry> subtitles, float totalDuration)
    {
        var shots = new List<Shot>();
        var targetSceneDuration = 10.0f; // Target ~10 seconds per scene
        
        int sceneNumber = 0;
        float currentSceneStart = 0;
        var currentSceneText = new List<string>();

        foreach (var subtitle in subtitles)
        {
            currentSceneText.Add(subtitle.Text);

            // Check if we should create a new scene
            var currentDuration = subtitle.EndTime - currentSceneStart;
            if (currentDuration >= targetSceneDuration || subtitle == subtitles.Last())
            {
                var shot = new Shot
                {
                    ShotNumber = sceneNumber++,
                    StartTime = currentSceneStart,
                    EndTime = subtitle.EndTime,
                    Duration = subtitle.EndTime - currentSceneStart,
                    SceneDescription = string.Join(" ", currentSceneText)
                };

                shots.Add(shot);

                currentSceneStart = subtitle.EndTime;
                currentSceneText.Clear();
            }
        }

        return shots;
    }

    private async Task SaveShotlistAsync(Shotlist shotlist, string outputPath)
    {
        var directory = Path.GetDirectoryName(outputPath);
        if (!string.IsNullOrEmpty(directory) && !Directory.Exists(directory))
        {
            Directory.CreateDirectory(directory);
        }

        var json = System.Text.Json.JsonSerializer.Serialize(shotlist, new System.Text.Json.JsonSerializerOptions
        {
            WriteIndented = true
        });

        await File.WriteAllTextAsync(outputPath, json);
    }

    private class SubtitleEntry
    {
        public float StartTime { get; set; }
        public float EndTime { get; set; }
        public string Text { get; set; } = string.Empty;
    }
}
