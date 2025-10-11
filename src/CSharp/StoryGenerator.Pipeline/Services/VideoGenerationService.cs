using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text.Json;
using System.Threading.Tasks;
using PrismQ.Shared.Interfaces;
using PrismQ.Shared.Models;
using PrismQ.VideoGenerator;
using StoryGenerator.Generators;
using StoryGenerator.Pipeline.Config;

namespace StoryGenerator.Pipeline.Services;

/// <summary>
/// Service for generating video clips from scenes using LTX-Video or keyframe interpolation.
/// </summary>
public class VideoGenerationService
{
    private readonly PathsConfig _paths;
    private readonly VideoConfig _videoConfig;
    private readonly bool _useLTX;

    public VideoGenerationService(PathsConfig paths, VideoConfig videoConfig, bool useLTX = true)
    {
        _paths = paths ?? throw new ArgumentNullException(nameof(paths));
        _videoConfig = videoConfig ?? throw new ArgumentNullException(nameof(videoConfig));
        _useLTX = useLTX;
    }

    /// <summary>
    /// Generate video clips for all scenes in a shotlist.
    /// </summary>
    /// <param name="storyTitle">The story title</param>
    /// <returns>List of generated video clip paths</returns>
    public async Task<List<string>> GenerateVideoClipsAsync(string storyTitle)
    {
        Console.WriteLine($"Generating video clips for: {storyTitle}");
        Console.WriteLine($"  Method: {(_useLTX ? "LTX-Video" : "Keyframe Interpolation")}");

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

        // Create video output directory
        var videoDir = Path.Combine(_paths.StoryRoot, _paths.Videos, storyTitle);
        Directory.CreateDirectory(videoDir);

        // Generate clips for each scene
        var clipPaths = new List<string>();

        if (_useLTX)
        {
            clipPaths = await GenerateWithLTXAsync(shotlist, videoDir);
        }
        else
        {
            clipPaths = await GenerateWithKeyframesAsync(shotlist, videoDir);
        }

        Console.WriteLine($"✅ Generated {clipPaths.Count} video clips");
        return clipPaths;
    }

    private async Task<List<string>> GenerateWithLTXAsync(Shotlist shotlist, string outputDir)
    {
        var synthesizer = new LTXVideoSynthesizer(
            width: _videoConfig.Resolution.Width,
            height: _videoConfig.Resolution.Height,
            fps: _videoConfig.Fps
        );

        var clipPaths = new List<string>();

        for (int i = 0; i < shotlist.Shots.Count; i++)
        {
            var shot = shotlist.Shots[i];
            var outputPath = Path.Combine(outputDir, $"clip_{i:D3}.mp4");

            Console.WriteLine($"  Generating clip {i + 1}/{shotlist.Shots.Count}: {shot.VisualPrompt.Substring(0, Math.Min(50, shot.VisualPrompt.Length))}...");

            try
            {
                var duration = (int)Math.Ceiling(shot.Duration);
                var success = await synthesizer.GenerateVideoAsync(
                    prompt: shot.VisualPrompt,
                    outputPath: outputPath,
                    duration: duration,
                    fps: _videoConfig.Fps
                );

                if (success && File.Exists(outputPath))
                {
                    clipPaths.Add(outputPath);
                }
                else
                {
                    Console.WriteLine($"    ⚠️ Failed to generate clip {i}");
                }
            }
            catch (Exception ex)
            {
                Console.WriteLine($"    ❌ Error generating clip {i}: {ex.Message}");
            }
        }

        return clipPaths;
    }

    private async Task<List<string>> GenerateWithKeyframesAsync(Shotlist shotlist, string outputDir)
    {
        var config = new KeyframeVideoConfig
        {
            TargetFps = _videoConfig.Fps,
            Width = _videoConfig.Resolution.Width,
            Height = _videoConfig.Resolution.Height,
            KeyframesPerScene = 3,
            InferenceSteps = 40,
            GuidanceScale = 7.5
        };

        var synthesizer = new KeyframeVideoSynthesizer(config);
        var clipPaths = new List<string>();

        for (int i = 0; i < shotlist.Shots.Count; i++)
        {
            var shot = shotlist.Shots[i];
            var outputPath = Path.Combine(outputDir, $"clip_{i:D3}.mp4");

            Console.WriteLine($"  Generating clip {i + 1}/{shotlist.Shots.Count}: {shot.VisualPrompt.Substring(0, Math.Min(50, shot.VisualPrompt.Length))}...");

            try
            {
                var success = await synthesizer.GenerateSceneAsync(
                    sceneDescription: shot.VisualPrompt,
                    outputPath: outputPath,
                    duration: shot.Duration
                );

                if (success && File.Exists(outputPath))
                {
                    clipPaths.Add(outputPath);
                }
                else
                {
                    Console.WriteLine($"    ⚠️ Failed to generate clip {i}");
                }
            }
            catch (Exception ex)
            {
                Console.WriteLine($"    ❌ Error generating clip {i}: {ex.Message}");
            }
        }

        return clipPaths;
    }
}
