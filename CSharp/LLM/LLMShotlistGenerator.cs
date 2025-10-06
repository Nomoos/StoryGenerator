using System;
using System.Diagnostics;
using System.Linq;
using System.Threading;
using System.Threading.Tasks;
using StoryGenerator.Core.Interfaces;

namespace StoryGenerator.Core.LLM
{
    /// <summary>
    /// LLM-based shotlist generator implementation.
    /// Generates detailed structured shotlists with emotions, camera directions, and timing.
    /// </summary>
    public class LLMShotlistGenerator : ILLMShotlistGenerator
    {
        private readonly ILLMContentGenerator _contentGenerator;

        /// <inheritdoc/>
        public string Name => "LLM Shotlist Generator";

        /// <inheritdoc/>
        public string Version => "1.0.0";

        /// <inheritdoc/>
        public ILLMContentGenerator ContentGenerator => _contentGenerator;

        /// <summary>
        /// Initializes a new instance of the LLMShotlistGenerator class.
        /// </summary>
        /// <param name="contentGenerator">The LLM content generator to use.</param>
        public LLMShotlistGenerator(ILLMContentGenerator contentGenerator)
        {
            _contentGenerator = contentGenerator ?? throw new ArgumentNullException(nameof(contentGenerator));
        }

        /// <inheritdoc/>
        public async Task<Shotlist> GenerateShotlistAsync(
            string scriptText,
            float audioDuration,
            CancellationToken cancellationToken = default)
        {
            var structuredShotlist = await GenerateStructuredShotlistAsync(
                scriptText,
                audioDuration,
                temperature: 0.5f,
                cancellationToken
            );

            // Convert to base Shotlist type
            return structuredShotlist;
        }

        /// <inheritdoc/>
        public async Task<StructuredShotlist> GenerateStructuredShotlistAsync(
            string scriptText,
            float audioDuration,
            float temperature = 0.5f,
            CancellationToken cancellationToken = default)
        {
            if (string.IsNullOrWhiteSpace(scriptText))
            {
                throw new ArgumentException("Script text cannot be empty", nameof(scriptText));
            }

            if (audioDuration <= 0)
            {
                throw new ArgumentException("Audio duration must be positive", nameof(audioDuration));
            }

            var stopwatch = Stopwatch.StartNew();

            try
            {
                var systemPrompt = PromptTemplates.ShotlistGenerationSystem;
                var userPrompt = PromptTemplates.FormatShotlistPrompt(scriptText, audioDuration);

                var llmOutput = await _contentGenerator.GenerateAsync(
                    systemPrompt,
                    userPrompt,
                    temperature,
                    maxTokens: 4000, // Large enough for detailed shotlist
                    cancellationToken
                );

                // Parse the LLM output into structured shotlist
                var shotlist = ShotlistParser.ParseShotlist(llmOutput);

                // Validate and fix timing if needed
                shotlist = ShotlistParser.FixShotlistTiming(shotlist, audioDuration);

                // Add metadata
                shotlist.Metadata = new GenerationMetadata
                {
                    ModelUsed = _contentGenerator.ModelName,
                    Provider = _contentGenerator.Provider,
                    Temperature = temperature,
                    GenerationTimeSeconds = (float)stopwatch.Elapsed.TotalSeconds,
                    GeneratedAt = DateTime.UtcNow
                };

                return shotlist;
            }
            catch (Exception ex)
            {
                throw new Exception($"Failed to generate shotlist: {ex.Message}", ex);
            }
            finally
            {
                stopwatch.Stop();
            }
        }

        /// <inheritdoc/>
        public async Task<StructuredShotlist> RefineShotlistAsync(
            StructuredShotlist shotlist,
            float temperature = 0.4f,
            CancellationToken cancellationToken = default)
        {
            if (shotlist == null)
            {
                throw new ArgumentNullException(nameof(shotlist));
            }

            // For each shot that needs refinement, generate enhanced details
            for (int i = 0; i < shotlist.Shots.Count; i++)
            {
                var shot = shotlist.Shots[i];

                // If camera direction is not detailed enough, enhance it
                if (string.IsNullOrWhiteSpace(shot.CameraDirection.ShotType) ||
                    string.IsNullOrWhiteSpace(shot.CameraDirection.Movement))
                {
                    shot.CameraDirection = await GenerateCameraDirectionAsync(shot, cancellationToken);
                }

                // If visual prompt is too short, enhance it
                if (shot.VisualPrompt.Length < 50)
                {
                    shot.VisualPrompt = await _contentGenerator.GenerateVideoDescriptionAsync(
                        shot.SceneDescription,
                        shot.PrimaryEmotion,
                        temperature,
                        cancellationToken
                    );
                }
            }

            return shotlist;
        }

        /// <inheritdoc/>
        public async Task<CameraDirection> GenerateCameraDirectionAsync(
            StructuredShot shot,
            CancellationToken cancellationToken = default)
        {
            if (shot == null)
            {
                throw new ArgumentNullException(nameof(shot));
            }

            var systemPrompt = PromptTemplates.CameraDirectionSystem;
            var userPrompt = PromptTemplates.FormatCameraDirectionPrompt(
                shot.SceneDescription,
                shot.PrimaryEmotion
            );

            var llmOutput = await _contentGenerator.GenerateAsync(
                systemPrompt,
                userPrompt,
                temperature: 0.4f,
                cancellationToken: cancellationToken
            );

            // Parse the output into camera direction
            return ParseCameraDirection(llmOutput);
        }

        /// <inheritdoc/>
        public async Task<StructuredShotlist> ValidateAndCorrectTimingAsync(
            StructuredShotlist shotlist,
            float audioDuration,
            CancellationToken cancellationToken = default)
        {
            if (shotlist == null)
            {
                throw new ArgumentNullException(nameof(shotlist));
            }

            // Validate the shotlist
            var errors = ShotlistParser.ValidateShotlist(shotlist);

            if (errors.Count > 0)
            {
                // Attempt to fix timing issues
                shotlist = ShotlistParser.FixShotlistTiming(shotlist, audioDuration);

                // Re-validate
                errors = ShotlistParser.ValidateShotlist(shotlist);

                if (errors.Count > 0)
                {
                    // Log validation errors but don't fail
                    Console.WriteLine($"Warning: Shotlist validation found {errors.Count} issues:");
                    foreach (var error in errors)
                    {
                        Console.WriteLine($"  - {error}");
                    }
                }
            }

            return await Task.FromResult(shotlist);
        }

        private static CameraDirection ParseCameraDirection(string llmOutput)
        {
            var direction = new CameraDirection();

            // Parse common camera direction elements from text
            var lines = llmOutput.Split('\n', StringSplitOptions.RemoveEmptyEntries);

            foreach (var line in lines)
            {
                var lowerLine = line.ToLower();

                if (lowerLine.Contains("shot type:") || lowerLine.Contains("shot:"))
                {
                    direction.ShotType = ExtractValue(line);
                }
                else if (lowerLine.Contains("angle:") || lowerLine.Contains("camera angle:"))
                {
                    direction.Angle = ExtractValue(line);
                }
                else if (lowerLine.Contains("movement:") || lowerLine.Contains("camera movement:"))
                {
                    direction.Movement = ExtractValue(line);
                }
                else if (lowerLine.Contains("focus:") || lowerLine.Contains("focus point:"))
                {
                    direction.FocusPoint = ExtractValue(line);
                }
                else if (lowerLine.Contains("depth of field:") || lowerLine.Contains("dof:"))
                {
                    direction.DepthOfField = ExtractValue(line);
                }
                else if (lowerLine.Contains("composition:"))
                {
                    direction.Composition = ExtractValue(line);
                }
            }

            // Use entire output as notes if not already parsed
            if (string.IsNullOrWhiteSpace(direction.ShotType))
            {
                direction.Notes = llmOutput;
            }

            return direction;
        }

        private static string ExtractValue(string line)
        {
            var parts = line.Split(':', 2);
            return parts.Length > 1 ? parts[1].Trim().TrimStart('-', '*', '•').Trim() : line.Trim();
        }
    }
}
