using System;
using System.IO;
using System.Threading;
using System.Threading.Tasks;
using StoryGenerator.Core.Interfaces;
using StoryGenerator.Core.LLM;
using StoryGenerator.Models;

namespace PrismQ.SceneDescriptions
{
    /// <summary>
    /// Generates scene beat-sheets and shotlists from final scripts.
    /// Uses LLM-based shotlist generation and saves as JSON in /scenes/json/{segment}/{age}/{title_id}_shots.json
    /// </summary>
    public class SceneBeatsGenerator
    {
        private readonly ILLMShotlistGenerator _shotlistGenerator;
        private readonly string _scenesRootPath;

        /// <summary>
        /// Creates a new scene beats generator.
        /// </summary>
        /// <param name="shotlistGenerator">The LLM shotlist generator to use</param>
        /// <param name="scenesRootPath">Root path for scenes output (defaults to ./scenes)</param>
        public SceneBeatsGenerator(ILLMShotlistGenerator shotlistGenerator, string? scenesRootPath = null)
        {
            _shotlistGenerator = shotlistGenerator ?? throw new ArgumentNullException(nameof(shotlistGenerator));
            _scenesRootPath = scenesRootPath ?? Path.Combine(Directory.GetCurrentDirectory(), "scenes");
        }

        /// <summary>
        /// Generates beat-sheet and shotlist from a script and saves to JSON.
        /// </summary>
        /// <param name="scriptText">The script text to analyze</param>
        /// <param name="titleId">The title ID for the story</param>
        /// <param name="segment">Audience segment (gender)</param>
        /// <param name="age">Age range</param>
        /// <param name="audioDuration">Duration of the audio in seconds</param>
        /// <param name="temperature">LLM temperature (default: 0.5)</param>
        /// <param name="cancellationToken">Cancellation token</param>
        /// <returns>Path to the saved JSON file</returns>
        public async Task<string> GenerateAndSaveBeatsAsync(
            string scriptText,
            string titleId,
            string segment,
            string age,
            float audioDuration,
            float temperature = 0.5f,
            CancellationToken cancellationToken = default)
        {
            if (string.IsNullOrWhiteSpace(scriptText))
                throw new ArgumentException("Script text cannot be empty", nameof(scriptText));
            if (string.IsNullOrWhiteSpace(titleId))
                throw new ArgumentException("Title ID cannot be empty", nameof(titleId));
            if (string.IsNullOrWhiteSpace(segment))
                throw new ArgumentException("Segment cannot be empty", nameof(segment));
            if (string.IsNullOrWhiteSpace(age))
                throw new ArgumentException("Age cannot be empty", nameof(age));
            if (audioDuration <= 0)
                throw new ArgumentException("Audio duration must be positive", nameof(audioDuration));

            // Generate structured shotlist using LLM
            var shotlist = await _shotlistGenerator.GenerateStructuredShotlistAsync(
                scriptText,
                audioDuration,
                temperature,
                cancellationToken
            );

            // Validate and correct timing if needed
            shotlist = await _shotlistGenerator.ValidateAndCorrectTimingAsync(
                shotlist,
                audioDuration,
                cancellationToken
            );

            // Build output path: /scenes/json/{segment}/{age}/{title_id}_shots.json
            var outputDir = Path.Combine(_scenesRootPath, "json", segment, age);
            Directory.CreateDirectory(outputDir);

            var outputPath = Path.Combine(outputDir, $"{titleId}_shots.json");

            // Serialize to JSON and save
            var jsonOutput = ShotlistParser.SerializeToJson(shotlist);
            await File.WriteAllTextAsync(outputPath, jsonOutput, cancellationToken);

            return outputPath;
        }

        /// <summary>
        /// Generates beat-sheet from script version.
        /// </summary>
        /// <param name="scriptVersion">The script version containing all metadata</param>
        /// <param name="audioDuration">Duration of the audio in seconds</param>
        /// <param name="temperature">LLM temperature (default: 0.5)</param>
        /// <param name="cancellationToken">Cancellation token</param>
        /// <returns>Path to the saved JSON file</returns>
        public async Task<string> GenerateFromScriptVersionAsync(
            ScriptVersion scriptVersion,
            float audioDuration,
            float temperature = 0.5f,
            CancellationToken cancellationToken = default)
        {
            if (scriptVersion == null)
                throw new ArgumentNullException(nameof(scriptVersion));

            return await GenerateAndSaveBeatsAsync(
                scriptVersion.Content,
                scriptVersion.TitleId,
                scriptVersion.TargetAudience.Gender,
                scriptVersion.TargetAudience.Age,
                audioDuration,
                temperature,
                cancellationToken
            );
        }
    }
}
