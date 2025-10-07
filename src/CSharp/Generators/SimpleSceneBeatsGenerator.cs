using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text;
using System.Text.Json;
using System.Text.Json.Serialization;
using System.Threading;
using System.Threading.Tasks;
using StoryGenerator.Models;

namespace StoryGenerator.Generators
{
    /// <summary>
    /// Generates simple beat-sheets and shotlists from scripts without requiring LLM.
    /// Creates a basic structure based on script sentences and estimated timing.
    /// </summary>
    public class SimpleSceneBeatsGenerator
    {
        private readonly string _scenesRootPath;
        private const int AverageWordsPerMinute = 150; // Average speaking rate

        /// <summary>
        /// Creates a new simple scene beats generator.
        /// </summary>
        /// <param name="scenesRootPath">Root path for scenes output (defaults to ./scenes)</param>
        public SimpleSceneBeatsGenerator(string? scenesRootPath = null)
        {
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
        /// <param name="cancellationToken">Cancellation token</param>
        /// <returns>Path to the saved JSON file</returns>
        public async Task<string> GenerateAndSaveBeatsAsync(
            string scriptText,
            string titleId,
            string segment,
            string age,
            float audioDuration,
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

            // Generate simple shotlist structure
            var shotlist = GenerateShotlistFromScript(scriptText, titleId, audioDuration);

            // Build output path: /scenes/json/{segment}/{age}/{title_id}_shots.json
            var outputDir = Path.Combine(_scenesRootPath, "json", segment, age);
            Directory.CreateDirectory(outputDir);

            var outputPath = Path.Combine(outputDir, $"{titleId}_shots.json");

            // Serialize to JSON and save
            var jsonOptions = new JsonSerializerOptions
            {
                WriteIndented = true,
                PropertyNamingPolicy = JsonNamingPolicy.CamelCase,
                DefaultIgnoreCondition = JsonIgnoreCondition.WhenWritingNull
            };

            var jsonOutput = JsonSerializer.Serialize(shotlist, jsonOptions);
            await File.WriteAllTextAsync(outputPath, jsonOutput, cancellationToken);

            return outputPath;
        }

        /// <summary>
        /// Generates beat-sheet from script version.
        /// </summary>
        /// <param name="scriptVersion">The script version containing all metadata</param>
        /// <param name="audioDuration">Duration of the audio in seconds</param>
        /// <param name="cancellationToken">Cancellation token</param>
        /// <returns>Path to the saved JSON file</returns>
        public async Task<string> GenerateFromScriptVersionAsync(
            ScriptVersion scriptVersion,
            float audioDuration,
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
                cancellationToken
            );
        }

        /// <summary>
        /// Generates a simple shotlist structure from script text.
        /// </summary>
        private SimpleShotlist GenerateShotlistFromScript(string scriptText, string titleId, float totalDuration)
        {
            // Split script into sentences
            var sentences = SplitIntoSentences(scriptText);
            if (!sentences.Any())
                return new SimpleShotlist { TitleId = titleId, TotalDuration = totalDuration };

            // Calculate timing
            var totalWords = sentences.Sum(s => CountWords(s));
            var wordsPerSecond = totalWords / totalDuration;

            var shotlist = new SimpleShotlist
            {
                TitleId = titleId,
                TotalDuration = totalDuration,
                TotalShots = sentences.Count,
                GeneratedAt = DateTime.UtcNow,
                Shots = new List<SimpleShot>()
            };

            var currentTime = 0.0f;
            var shotNumber = 1;

            foreach (var sentence in sentences)
            {
                var words = CountWords(sentence);
                if (words == 0)
                    continue;

                var duration = words / wordsPerSecond;
                
                var shot = new SimpleShot
                {
                    ShotNumber = shotNumber,
                    StartTime = currentTime,
                    EndTime = currentTime + duration,
                    Duration = duration,
                    SceneDescription = sentence.Trim(),
                    VisualPrompt = GenerateVisualPrompt(sentence),
                    Narration = sentence.Trim()
                };

                shotlist.Shots.Add(shot);
                currentTime += duration;
                shotNumber++;
            }

            return shotlist;
        }

        /// <summary>
        /// Generates a simple visual prompt from scene text.
        /// </summary>
        private string GenerateVisualPrompt(string sceneText)
        {
            // Simple extraction - just clean up the text for a visual description
            var prompt = sceneText.Trim();
            
            // Remove quotes if present
            prompt = prompt.Trim('"', '\'');
            
            // Limit length
            if (prompt.Length > 200)
                prompt = prompt.Substring(0, 197) + "...";
            
            return prompt;
        }

        /// <summary>
        /// Splits text into sentences.
        /// </summary>
        private List<string> SplitIntoSentences(string text)
        {
            if (string.IsNullOrWhiteSpace(text))
                return new List<string>();

            // Clean and normalize text
            text = text.Replace("\r\n", " ").Replace("\n", " ").Replace("\r", " ");
            text = System.Text.RegularExpressions.Regex.Replace(text, @"\s+", " ").Trim();

            // Split by sentence-ending punctuation
            var sentences = System.Text.RegularExpressions.Regex.Split(text, @"(?<=[.!?])\s+");
            return sentences.Where(s => !string.IsNullOrWhiteSpace(s)).ToList();
        }

        /// <summary>
        /// Counts words in a text string.
        /// </summary>
        private int CountWords(string text)
        {
            if (string.IsNullOrWhiteSpace(text))
                return 0;

            return text.Split(new[] { ' ', '\t', '\n', '\r' }, StringSplitOptions.RemoveEmptyEntries).Length;
        }
    }

    /// <summary>
    /// Simple shotlist structure for JSON serialization.
    /// </summary>
    public class SimpleShotlist
    {
        public string TitleId { get; set; } = string.Empty;
        public float TotalDuration { get; set; }
        public int TotalShots { get; set; }
        public DateTime GeneratedAt { get; set; }
        public List<SimpleShot> Shots { get; set; } = new();
    }

    /// <summary>
    /// Simple shot structure.
    /// </summary>
    public class SimpleShot
    {
        public int ShotNumber { get; set; }
        public float StartTime { get; set; }
        public float EndTime { get; set; }
        public float Duration { get; set; }
        public string SceneDescription { get; set; } = string.Empty;
        public string VisualPrompt { get; set; } = string.Empty;
        public string Narration { get; set; } = string.Empty;
    }
}
