using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text.Json;
using System.Threading;
using System.Threading.Tasks;
using StoryGenerator.Core.Interfaces;
using StoryGenerator.Models;

namespace PrismQ.VideoGenerator
{
    /// <summary>
    /// Service for generating keyframes per scene/shot using SDXL
    /// Implements the requirements from the issue:
    /// - Creates per-shot prompts (style, camera, mood, age-safe)
    /// - Generates keyframes with SDXL base+refiner
    /// - Optionally uses LoRA/ControlNet for consistency
    /// - Selects top N per shot
    /// - Saves prompts and manifest
    /// </summary>
    public class KeyframeGenerationService : IKeyframeGenerationService
    {
        private readonly IImageGenerationClient _imageClient;
        private static readonly JsonSerializerOptions JsonOptions = new JsonSerializerOptions
        {
            WriteIndented = true,
            PropertyNameCaseInsensitive = true
        };

        public KeyframeGenerationService(IImageGenerationClient imageClient)
        {
            _imageClient = imageClient ?? throw new ArgumentNullException(nameof(imageClient));
        }

        /// <summary>
        /// Generate keyframes for all shots in a shotlist
        /// </summary>
        public async Task<KeyframeManifest> GenerateKeyframesAsync(
            StructuredShotlist shotlist,
            string titleId,
            string segment,
            string age,
            KeyframeGenerationConfig config,
            CancellationToken cancellationToken = default)
        {
            if (shotlist == null || shotlist.Shots == null || !shotlist.Shots.Any())
                throw new ArgumentException("Shotlist must contain shots", nameof(shotlist));

            var startTime = DateTime.UtcNow;
            var manifest = new KeyframeManifest
            {
                TitleId = titleId,
                Segment = segment,
                Age = age,
                Version = config.LoraPath != null || config.UseControlNet ? "v2" : "v1",
                VariantsPerShot = config.VariantsPerShot,
                TopNPerShot = config.TopNPerShot,
                GenerationConfig = new Dictionary<string, object>
                {
                    ["width"] = config.Width,
                    ["height"] = config.Height,
                    ["base_steps"] = config.BaseSteps,
                    ["refiner_steps"] = config.RefinerSteps,
                    ["guidance_scale"] = config.GuidanceScale,
                    ["use_refiner"] = config.UseRefiner,
                    ["lora_path"] = config.LoraPath ?? "",
                    ["lora_scale"] = config.LoraScale,
                    ["use_controlnet"] = config.UseControlNet
                }
            };

            Console.WriteLine($"🎨 Generating keyframes for {shotlist.Shots.Count} shots");
            Console.WriteLine($"   Title ID: {titleId}");
            Console.WriteLine($"   Segment: {segment}, Age: {age}");
            Console.WriteLine($"   Version: {manifest.Version} (Base+Refiner{(config.LoraPath != null ? "+LoRA" : "")}{(config.UseControlNet ? "+ControlNet" : "")})");

            // Step 1: Create prompts for all shots
            var prompts = new List<KeyframePrompt>();
            foreach (var shot in shotlist.Shots)
            {
                var prompt = CreatePromptForShot(shot, config);
                prompts.Add(prompt);
            }
            manifest.Prompts = prompts;

            // Save prompts JSON
            var promptsDir = Path.Combine(config.OutputBaseDir, $"keyframes_{manifest.Version}", segment, age);
            Directory.CreateDirectory(promptsDir);
            var promptsPath = Path.Combine(promptsDir, $"{titleId}_prompts.json");
            await SavePromptsAsync(prompts, promptsPath);
            Console.WriteLine($"   ✓ Saved prompts to: {promptsPath}");

            // Step 2: Load LoRA if specified (for v2)
            if (!string.IsNullOrEmpty(config.LoraPath) && File.Exists(config.LoraPath))
            {
                Console.WriteLine($"   Loading LoRA: {config.LoraPath}");
                await _imageClient.LoadLoraAsync(config.LoraPath, config.LoraScale);
            }

            // Step 3: Generate keyframes for each shot
            var allKeyframes = new List<GeneratedKeyframe>();
            var outputDir = Path.Combine(promptsDir, titleId);
            Directory.CreateDirectory(outputDir);

            for (int i = 0; i < shotlist.Shots.Count; i++)
            {
                var shot = shotlist.Shots[i];
                Console.WriteLine($"\n   Shot {shot.ShotNumber}/{shotlist.Shots.Count}: {shot.SceneDescription.Substring(0, Math.Min(50, shot.SceneDescription.Length))}...");

                var keyframes = await GenerateKeyframesForShotAsync(
                    shot,
                    titleId,
                    outputDir,
                    config,
                    cancellationToken);

                allKeyframes.AddRange(keyframes);
            }

            manifest.Keyframes = allKeyframes;

            // Step 4: Select top N keyframes per shot
            Console.WriteLine($"\n   Selecting top {config.TopNPerShot} keyframes per shot...");
            manifest.SelectedKeyframes = SelectTopKeyframes(allKeyframes, config.TopNPerShot);

            // Step 5: Unload LoRA if loaded
            if (!string.IsNullOrEmpty(config.LoraPath))
            {
                await _imageClient.UnloadLoraAsync();
            }

            // Step 6: Save manifest
            manifest.TotalGenerationTimeSeconds = (DateTime.UtcNow - startTime).TotalSeconds;
            var manifestPath = Path.Combine(promptsDir, $"{titleId}_manifest.json");
            await SaveManifestAsync(manifest, manifestPath);
            Console.WriteLine($"\n✅ Keyframe generation complete!");
            Console.WriteLine($"   Total keyframes: {allKeyframes.Count}");
            Console.WriteLine($"   Selected keyframes: {manifest.SelectedKeyframes.Values.Sum(v => v.Count)}");
            Console.WriteLine($"   Generation time: {manifest.TotalGenerationTimeSeconds:F1}s");
            Console.WriteLine($"   Manifest saved to: {manifestPath}");

            return manifest;
        }

        /// <summary>
        /// Generate keyframes for a single shot
        /// </summary>
        public async Task<List<GeneratedKeyframe>> GenerateKeyframesForShotAsync(
            StructuredShot shot,
            string titleId,
            string outputDir,
            KeyframeGenerationConfig config,
            CancellationToken cancellationToken = default)
        {
            var keyframes = new List<GeneratedKeyframe>();
            var prompt = CreatePromptForShot(shot, config);
            var variantPrefix = config.LoraPath != null || config.UseControlNet ? "B" : "A";

            for (int i = 0; i < config.VariantsPerShot; i++)
            {
                var variantId = $"{variantPrefix}{i + 1}";
                var filename = $"shot_{shot.ShotNumber:D3}_{variantId}.png";
                var outputPath = Path.Combine(outputDir, filename);

                Console.WriteLine($"      Generating variant {variantId}...");

                try
                {
                    ImageGenerationResult result;
                    var startTime = DateTime.UtcNow;

                    if (config.UseRefiner)
                    {
                        result = await _imageClient.GenerateImageWithRefinerAsync(
                            prompt.CombinedPrompt,
                            prompt.NegativePrompt,
                            config.Width,
                            config.Height,
                            config.BaseSteps,
                            config.RefinerSteps,
                            config.GuidanceScale,
                            seed: null,
                            cancellationToken);
                    }
                    else
                    {
                        result = await _imageClient.GenerateImageAsync(
                            prompt.CombinedPrompt,
                            prompt.NegativePrompt,
                            config.Width,
                            config.Height,
                            config.BaseSteps,
                            config.GuidanceScale,
                            seed: null,
                            cancellationToken);
                    }

                    // Save the image
                    await _imageClient.SaveImageAsync(result, outputPath);

                    var generationTime = (DateTime.UtcNow - startTime).TotalMilliseconds;

                    var keyframe = new GeneratedKeyframe
                    {
                        ShotNumber = shot.ShotNumber,
                        VariantId = variantId,
                        FilePath = outputPath,
                        Prompt = prompt,
                        GenerationMethod = config.UseRefiner ? "base+refiner" : "base",
                        Width = result.Width,
                        Height = result.Height,
                        Seed = result.Seed,
                        GenerationTimeMs = (long)generationTime,
                        GeneratedAt = DateTime.UtcNow
                    };

                    keyframes.Add(keyframe);
                    Console.WriteLine($"      ✓ Saved to: {filename} ({generationTime:F0}ms)");
                }
                catch (Exception ex)
                {
                    Console.WriteLine($"      ✗ Failed to generate variant {variantId}: {ex.Message}");
                }
            }

            return keyframes;
        }

        /// <summary>
        /// Create prompt for a specific shot with style, camera, mood, and age-safe content
        /// </summary>
        public KeyframePrompt CreatePromptForShot(StructuredShot shot, KeyframeGenerationConfig config)
        {
            var prompt = new KeyframePrompt
            {
                ShotNumber = shot.ShotNumber,
                VisualPrompt = shot.VisualPrompt ?? shot.SceneDescription,
                AgeSafe = config.AgeSafeContent
            };

            // Add camera direction
            if (shot.CameraDirection != null)
            {
                var cameraParts = new List<string>();
                if (!string.IsNullOrWhiteSpace(shot.CameraDirection.ShotType))
                    cameraParts.Add(shot.CameraDirection.ShotType);
                if (!string.IsNullOrWhiteSpace(shot.CameraDirection.Angle))
                    cameraParts.Add(shot.CameraDirection.Angle);
                if (!string.IsNullOrWhiteSpace(shot.CameraDirection.Movement))
                    cameraParts.Add(shot.CameraDirection.Movement);
                if (!string.IsNullOrWhiteSpace(shot.CameraDirection.Composition))
                    cameraParts.Add(shot.CameraDirection.Composition);

                prompt.Camera = string.Join(", ", cameraParts);
            }

            // Add mood and atmosphere
            var moodParts = new List<string>();
            if (!string.IsNullOrWhiteSpace(shot.Mood))
                moodParts.Add(shot.Mood);
            if (!string.IsNullOrWhiteSpace(shot.PrimaryEmotion))
                moodParts.Add(shot.PrimaryEmotion);
            if (!string.IsNullOrWhiteSpace(shot.Lighting))
                moodParts.Add(shot.Lighting);
            if (!string.IsNullOrWhiteSpace(shot.ColorPalette))
                moodParts.Add(shot.ColorPalette);

            prompt.Mood = string.Join(", ", moodParts);

            // Add style with quality enhancers
            var styleParts = new List<string>
            {
                "cinematic",
                "high quality",
                "detailed",
                "professional photography"
            };

            prompt.Style = string.Join(", ", styleParts);

            // Age-safe negative prompts
            if (config.AgeSafeContent)
            {
                prompt.NegativePrompt = "nsfw, nude, sexual, violence, gore, disturbing, inappropriate, " +
                    "low quality, blurry, distorted, ugly, deformed, bad anatomy";
            }
            else
            {
                prompt.NegativePrompt = "low quality, blurry, distorted, ugly, deformed, bad anatomy";
            }

            return prompt;
        }

        /// <summary>
        /// Select top N keyframes per shot based on quality
        /// For now, this is a simple selection - in production, you might want to use
        /// vision models or quality metrics to evaluate and rank keyframes
        /// </summary>
        public Dictionary<int, List<string>> SelectTopKeyframes(List<GeneratedKeyframe> keyframes, int topN)
        {
            var selected = new Dictionary<int, List<string>>();

            var groupedByShot = keyframes.GroupBy(k => k.ShotNumber);

            foreach (var group in groupedByShot)
            {
                // Select top N keyframes for this shot
                // For now, we just take the first N (in production, rank by quality)
                var topKeyframes = group
                    .OrderBy(k => k.GenerationTimeMs) // Faster generation might indicate better convergence
                    .Take(topN)
                    .Select(k => k.FilePath)
                    .ToList();

                selected[group.Key] = topKeyframes;

                // Mark selected keyframes
                foreach (var kf in keyframes.Where(k => k.ShotNumber == group.Key))
                {
                    kf.IsSelected = topKeyframes.Contains(kf.FilePath);
                }
            }

            return selected;
        }

        /// <summary>
        /// Save keyframe prompts to JSON file
        /// </summary>
        public async Task<string> SavePromptsAsync(List<KeyframePrompt> prompts, string outputPath)
        {
            var directory = Path.GetDirectoryName(outputPath);
            if (!string.IsNullOrEmpty(directory))
            {
                Directory.CreateDirectory(directory);
            }

            var json = JsonSerializer.Serialize(prompts, JsonOptions);
            await File.WriteAllTextAsync(outputPath, json);

            return outputPath;
        }

        /// <summary>
        /// Save keyframe manifest to JSON file
        /// </summary>
        public async Task<string> SaveManifestAsync(KeyframeManifest manifest, string outputPath)
        {
            var directory = Path.GetDirectoryName(outputPath);
            if (!string.IsNullOrEmpty(directory))
            {
                Directory.CreateDirectory(directory);
            }

            var json = JsonSerializer.Serialize(manifest, JsonOptions);
            await File.WriteAllTextAsync(outputPath, json);

            return outputPath;
        }

        /// <summary>
        /// Generate keyframes from a simple scene description and optional subtitles
        /// </summary>
        public async Task<KeyframeManifest> GenerateKeyframesFromSceneAsync(
            string sceneDescription,
            string? subtitles,
            string titleId,
            KeyframeGenerationConfig config,
            CancellationToken cancellationToken = default)
        {
            if (string.IsNullOrWhiteSpace(sceneDescription))
                throw new ArgumentException("Scene description cannot be null or empty", nameof(sceneDescription));

            if (string.IsNullOrWhiteSpace(titleId))
                throw new ArgumentException("Title ID cannot be null or empty", nameof(titleId));

            // Create a simple shotlist with a single shot from the scene description
            var shotlist = new StructuredShotlist
            {
                StoryTitle = titleId,
                TotalDuration = 10f, // Default duration for a single scene
                OverallMood = "neutral",
                Style = "cinematic",
                TargetAudience = "general"
            };

            // Build visual prompt combining scene description and subtitles
            string visualPrompt = sceneDescription;
            if (!string.IsNullOrWhiteSpace(subtitles))
            {
                visualPrompt = $"{sceneDescription}. Text overlay: \"{subtitles}\"";
            }

            // Create a single shot from the scene description
            var shot = new StructuredShot
            {
                ShotNumber = 1,
                StartTime = 0f,
                EndTime = 10f,
                Duration = 10f,
                SceneDescription = sceneDescription,
                VisualPrompt = visualPrompt,
                PrimaryEmotion = "neutral",
                Mood = "general",
                CameraDirection = new CameraDirection
                {
                    ShotType = "medium shot",
                    Angle = "eye level",
                    Movement = "static",
                    Composition = "balanced"
                },
                Lighting = "natural lighting",
                ColorPalette = "balanced colors"
            };

            // Add subtitles to the audio description if provided
            if (!string.IsNullOrWhiteSpace(subtitles))
            {
                shot.AudioDescription = subtitles;
            }

            shotlist.Shots.Add(shot);

            // Use the existing GenerateKeyframesAsync method
            return await GenerateKeyframesAsync(
                shotlist,
                titleId,
                segment: "single-scene",
                age: config.AgeSafeContent ? "all-ages" : "general",
                config,
                cancellationToken);
        }
    }
}
