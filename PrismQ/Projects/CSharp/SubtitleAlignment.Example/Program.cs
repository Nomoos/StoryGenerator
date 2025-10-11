using System;
using System.Collections.Generic;
using System.IO;
using System.Threading.Tasks;
using PrismQ.Shared.Interfaces;
using PrismQ.Shared.Core.Services;
using PrismQ.Shared.Models;
using StoryGenerator.Research;
using System.Text.Json;

/// <summary>
/// Example demonstrating subtitle alignment and shot mapping functionality.
/// Shows how to:
/// 1. Generate aligned SRT/VTT files from audio using faster-whisper
/// 2. Map subtitle time ranges to shot IDs
/// 3. Save outputs to proper directory structure
/// </summary>
class Program
{
    static async Task Main(string[] args)
        {
            Console.WriteLine("=== Subtitle Alignment and Shot Mapping Example ===\n");

            // Parse command line arguments
            if (args.Length < 1)
            {
                Console.WriteLine("Usage: SubtitleAlignmentExample <audio_path> [segment] [age_bucket] [title_id]");
                Console.WriteLine("\nExample:");
                Console.WriteLine("  SubtitleAlignmentExample audio.mp3 women 18-23 my_story_001");
                return;
            }

            var audioPath = args[0];
            var segment = args.Length > 1 ? args[1] : "women";
            var ageBucket = args.Length > 2 ? args[2] : "18-23";
            var titleId = args.Length > 3 ? args[3] : "example_title_001";

            if (!File.Exists(audioPath))
            {
                Console.WriteLine($"Error: Audio file not found: {audioPath}");
                return;
            }

            Console.WriteLine($"Audio file: {audioPath}");
            Console.WriteLine($"Segment: {segment}");
            Console.WriteLine($"Age bucket: {ageBucket}");
            Console.WriteLine($"Title ID: {titleId}\n");

            try
            {
                // Initialize Whisper client with large-v3 model for best quality
                Console.WriteLine("Initializing faster-whisper client...");
                var whisperClient = new WhisperClient(
                    modelSize: "large-v3",
                    device: "auto",  // Auto-detect GPU or use CPU
                    computeType: "float16"
                );

                // Initialize subtitle aligner service
                var subtitleAligner = new SubtitleAligner(whisperClient);

                // Step 1: Generate aligned SRT file
                Console.WriteLine("\n--- Step 1: Generating Aligned SRT Subtitles ---");
                var srtOutputPath = Path.Combine(
                    "subtitles", "timed", segment, ageBucket, $"{titleId}.srt"
                );
                
                Console.WriteLine($"Generating SRT file: {srtOutputPath}");
                var savedSrtPath = await subtitleAligner.GenerateAndSaveSrtAsync(
                    audioPath,
                    srtOutputPath,
                    language: "en",  // Change to null for auto-detection
                    maxWordsPerLine: 10
                );
                Console.WriteLine($"✓ SRT file saved: {savedSrtPath}");

                // Step 2: Generate aligned VTT file (optional)
                Console.WriteLine("\n--- Step 2: Generating Aligned VTT Subtitles ---");
                var vttOutputPath = Path.Combine(
                    "subtitles", "timed", segment, ageBucket, $"{titleId}.vtt"
                );
                
                Console.WriteLine($"Generating VTT file: {vttOutputPath}");
                var savedVttPath = await subtitleAligner.GenerateAndSaveVttAsync(
                    audioPath,
                    vttOutputPath,
                    language: "en",
                    maxWordsPerLine: 10
                );
                Console.WriteLine($"✓ VTT file saved: {savedVttPath}");

                // Step 3: Create example shotlist
                Console.WriteLine("\n--- Step 3: Creating Example Shotlist ---");
                var shotlist = CreateExampleShotlist();
                Console.WriteLine($"Created shotlist with {shotlist.Shots.Count} shots");
                Console.WriteLine($"Total duration: {shotlist.TotalDuration}s");

                // Step 4: Map subtitles to shots
                Console.WriteLine("\n--- Step 4: Mapping Subtitles to Shots ---");
                var mappingOutputPath = Path.Combine(
                    "scenes", "json", segment, ageBucket, $"{titleId}_subs_to_shots.json"
                );

                Console.WriteLine($"Generating subtitle-to-shot mapping: {mappingOutputPath}");
                var savedMappingPath = await subtitleAligner.MapAndSaveSubtitlesToShotsAsync(
                    audioPath,
                    shotlist,
                    titleId,
                    mappingOutputPath,
                    language: "en",
                    maxWordsPerLine: 10
                );
                Console.WriteLine($"✓ Mapping saved: {savedMappingPath}");

                // Display mapping summary
                Console.WriteLine("\n--- Mapping Summary ---");
                var mappingJson = await File.ReadAllTextAsync(savedMappingPath);
                var mapping = JsonSerializer.Deserialize<SubtitleToShotMapping>(
                    mappingJson,
                    new JsonSerializerOptions { PropertyNameCaseInsensitive = true }
                );

                if (mapping != null)
                {
                    Console.WriteLine($"Total subtitles: {mapping.SubtitleMappings.Count}");
                    Console.WriteLine($"Total duration: {mapping.TotalDuration:F2}s");
                    
                    // Show distribution of subtitles across shots
                    var shotCounts = new Dictionary<int, int>();
                    foreach (var subtitle in mapping.SubtitleMappings)
                    {
                        if (!shotCounts.ContainsKey(subtitle.ShotNumber))
                            shotCounts[subtitle.ShotNumber] = 0;
                        shotCounts[subtitle.ShotNumber]++;
                    }

                    Console.WriteLine("\nSubtitles per shot:");
                    foreach (var kvp in shotCounts)
                    {
                        Console.WriteLine($"  Shot {kvp.Key}: {kvp.Value} subtitle(s)");
                    }
                }

                Console.WriteLine("\n=== Example completed successfully! ===");
                Console.WriteLine("\nGenerated files:");
                Console.WriteLine($"  1. {savedSrtPath}");
                Console.WriteLine($"  2. {savedVttPath}");
                Console.WriteLine($"  3. {savedMappingPath}");
            }
            catch (Exception ex)
            {
                Console.WriteLine($"\nError: {ex.Message}");
                Console.WriteLine($"Stack trace: {ex.StackTrace}");
            }
        }

    /// <summary>
    /// Creates an example shotlist for demonstration purposes.
    /// In a real scenario, this would come from a shotlist generator.
    /// </summary>
    static Shotlist CreateExampleShotlist()
        {
            return new Shotlist
            {
                StoryTitle = "Example Story",
                TotalDuration = 60.0f, // 60 seconds
                Shots = new List<Shot>
                {
                    new Shot
                    {
                        ShotNumber = 1,
                        StartTime = 0.0f,
                        EndTime = 15.0f,
                        Duration = 15.0f,
                        SceneDescription = "Opening scene with narrator introduction",
                        VisualPrompt = "A calm morning landscape with soft lighting",
                        Mood = "Peaceful",
                        CameraAngle = "Wide shot",
                        Lighting = "Soft morning light",
                        ColorPalette = "Warm tones",
                        KeyElements = new List<string> { "landscape", "sunrise", "calm" }
                    },
                    new Shot
                    {
                        ShotNumber = 2,
                        StartTime = 15.0f,
                        EndTime = 30.0f,
                        Duration = 15.0f,
                        SceneDescription = "Main character appears",
                        VisualPrompt = "Close-up of character looking determined",
                        Mood = "Determined",
                        CameraAngle = "Medium close-up",
                        Lighting = "Natural light",
                        ColorPalette = "Neutral tones",
                        KeyElements = new List<string> { "character", "face", "expression" }
                    },
                    new Shot
                    {
                        ShotNumber = 3,
                        StartTime = 30.0f,
                        EndTime = 45.0f,
                        Duration = 15.0f,
                        SceneDescription = "Action sequence",
                        VisualPrompt = "Dynamic movement with energy",
                        Mood = "Energetic",
                        CameraAngle = "Tracking shot",
                        Lighting = "Dynamic lighting",
                        ColorPalette = "Vibrant colors",
                        KeyElements = new List<string> { "movement", "action", "energy" }
                    },
                    new Shot
                    {
                        ShotNumber = 4,
                        StartTime = 45.0f,
                        EndTime = 60.0f,
                        Duration = 15.0f,
                        SceneDescription = "Closing scene with resolution",
                        VisualPrompt = "Wide shot showing the outcome",
                        Mood = "Satisfied",
                        CameraAngle = "Wide shot",
                        Lighting = "Warm sunset light",
                        ColorPalette = "Warm golden tones",
                        KeyElements = new List<string> { "resolution", "sunset", "peace" }
                    }
                }
            };
        }
    }
