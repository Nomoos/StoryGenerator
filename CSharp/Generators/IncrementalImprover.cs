using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text.Json;
using System.Threading;
using System.Threading.Tasks;
using Microsoft.Extensions.Logging;
using StoryGenerator.Core.Models;
using StoryGenerator.Providers.OpenAI;

namespace StoryGenerator.Generators
{
    /// <summary>
    /// Implements iterative improvement system for video generation.
    /// Equivalent to Python GIncrementalImprover.py
    /// 
    /// Features:
    /// - Analyzes generated outputs for quality issues
    /// - Suggests improvements based on feedback
    /// - Tracks improvement history
    /// - Learns from successful iterations
    /// </summary>
    public class IncrementalImprover
    {
        private readonly OpenAIClient _openAIClient;
        private readonly ILogger<IncrementalImprover> _logger;
        private readonly string _model;

        public IncrementalImprover(
            OpenAIClient openAIClient,
            ILogger<IncrementalImprover> logger,
            string model = "gpt-4o-mini")
        {
            _openAIClient = openAIClient ?? throw new ArgumentNullException(nameof(openAIClient));
            _logger = logger ?? throw new ArgumentNullException(nameof(logger));
            _model = model;
        }

        /// <summary>
        /// Analyze video quality and suggest improvements
        /// </summary>
        /// <param name="storyIdea">Story idea object</param>
        /// <param name="scenes">List of scene information</param>
        /// <param name="userFeedback">Optional user feedback on the video</param>
        /// <param name="cancellationToken">Cancellation token</param>
        /// <returns>Analysis result with issues and suggestions</returns>
        public async Task<VideoQualityAnalysis> AnalyzeVideoQualityAsync(
            StoryIdea storyIdea,
            List<SceneInfo> scenes,
            string? userFeedback = null,
            CancellationToken cancellationToken = default)
        {
            if (storyIdea == null)
                throw new ArgumentNullException(nameof(storyIdea));
            if (scenes == null)
                throw new ArgumentNullException(nameof(scenes));

            _logger.LogInformation("🔍 Analyzing video quality for '{Title}'...", storyIdea.StoryTitle);

            var analysis = new VideoQualityAnalysis
            {
                StoryTitle = storyIdea.StoryTitle,
                Timestamp = DateTime.UtcNow,
                SceneCount = scenes.Count,
                Issues = new List<string>(),
                Suggestions = new List<string>(),
                Scores = new Dictionary<string, double>()
            };

            // Check 1: Scene duration consistency
            if (scenes.Any())
            {
                var durations = scenes.Select(s => s.Duration).ToList();
                var avgDuration = durations.Average();

                if (durations.Any(d => d < 2))
                {
                    analysis.Issues.Add("Some scenes are too short (< 2 seconds)");
                    analysis.Suggestions.Add("Consider merging very short scenes or adjusting segmentation");
                }

                if (durations.Any(d => d > 15))
                {
                    analysis.Issues.Add("Some scenes are too long (> 15 seconds)");
                    analysis.Suggestions.Add("Split long scenes into multiple segments for better pacing");
                }

                analysis.Scores["scene_duration"] = Math.Min(1.0, 1 - (Math.Abs(avgDuration - 7) / 10));
            }

            // Check 2: Visual description quality
            var descriptionLengths = scenes
                .Where(s => !string.IsNullOrEmpty(s.Description))
                .Select(s => s.Description.Split(' ', StringSplitOptions.RemoveEmptyEntries).Length)
                .ToList();

            if (descriptionLengths.Any())
            {
                var avgDescLength = descriptionLengths.Average();

                if (avgDescLength < 20)
                {
                    analysis.Issues.Add("Scene descriptions are too brief");
                    analysis.Suggestions.Add("Regenerate scene descriptions with more visual detail");
                }

                if (avgDescLength > 100)
                {
                    analysis.Issues.Add("Scene descriptions are too verbose");
                    analysis.Suggestions.Add("Simplify scene descriptions for better image generation");
                }

                analysis.Scores["description_quality"] = Math.Min(1.0, avgDescLength / 50);
            }

            // Check 3: Keyframe coverage
            var scenesWithKeyframes = scenes.Count(s => s.HasKeyframes);
            var keyframeCoverage = scenes.Count > 0 ? (double)scenesWithKeyframes / scenes.Count : 0;

            if (keyframeCoverage < 1.0)
            {
                var missing = scenes.Count - scenesWithKeyframes;
                analysis.Issues.Add($"{missing} scenes missing keyframes");
                analysis.Suggestions.Add("Regenerate keyframes for all scenes");
            }

            analysis.Scores["keyframe_coverage"] = keyframeCoverage;

            // Check 4: Get GPT-based quality assessment if user feedback provided
            if (!string.IsNullOrEmpty(userFeedback))
            {
                try
                {
                    var gptAnalysis = await GetGptQualityAnalysisAsync(
                        storyIdea, scenes, userFeedback, cancellationToken);

                    if (gptAnalysis != null)
                    {
                        analysis.GptAnalysis = gptAnalysis;
                        if (gptAnalysis.Issues != null)
                            analysis.Issues.AddRange(gptAnalysis.Issues);
                        if (gptAnalysis.Suggestions != null)
                            analysis.Suggestions.AddRange(gptAnalysis.Suggestions);
                    }
                }
                catch (Exception ex)
                {
                    _logger.LogWarning(ex, "Failed to get GPT quality analysis");
                }
            }

            // Calculate overall quality score
            if (analysis.Scores.Any())
            {
                analysis.OverallScore = analysis.Scores.Values.Average();
            }

            _logger.LogInformation("✅ Quality analysis complete. Overall score: {Score:F2}", analysis.OverallScore);

            return analysis;
        }

        /// <summary>
        /// Use GPT to analyze quality based on user feedback
        /// </summary>
        private async Task<GptQualityAnalysis?> GetGptQualityAnalysisAsync(
            StoryIdea storyIdea,
            List<SceneInfo> scenes,
            string userFeedback,
            CancellationToken cancellationToken)
        {
            var scenesSummary = string.Join("\n", scenes.Take(5).Select(s =>
                $"Scene {s.SceneId}: {(s.Text.Length > 100 ? s.Text.Substring(0, 100) + "..." : s.Text)} (duration: {s.Duration:F1}s)"));

            var prompt = $@"Analyze this short-form vertical video and provide quality assessment.

Story: {storyIdea.StoryTitle}
Total Scenes: {scenes.Count}

Sample Scenes:
{scenesSummary}

User Feedback:
{userFeedback}

Please provide:
1. Key issues identified (be specific)
2. Concrete improvement suggestions
3. Priority areas to focus on

Format your response as JSON with keys: ""issues"" (list), ""suggestions"" (list), ""priorities"" (list)";

            var messages = new List<ChatMessage>
            {
                ChatMessage.System("You are a video quality analyst specializing in short-form vertical content."),
                ChatMessage.User(prompt)
            };

            var response = await _openAIClient.CreateChatCompletionAsync(
                messages,
                model: _model,
                temperature: 0.7f,
                cancellationToken: cancellationToken);

            var content = response.Choices.FirstOrDefault()?.Message.Content;
            if (string.IsNullOrEmpty(content))
                return null;

            try
            {
                // Try to extract JSON from response
                var jsonStart = content.IndexOf('{');
                var jsonEnd = content.LastIndexOf('}');
                if (jsonStart >= 0 && jsonEnd > jsonStart)
                {
                    var jsonContent = content.Substring(jsonStart, jsonEnd - jsonStart + 1);
                    return JsonSerializer.Deserialize<GptQualityAnalysis>(jsonContent);
                }
            }
            catch (Exception ex)
            {
                _logger.LogWarning(ex, "Failed to parse GPT quality analysis JSON");
            }

            return null;
        }

        /// <summary>
        /// Save improvement history to file
        /// </summary>
        public async Task SaveImprovementHistoryAsync(
            string outputDirectory,
            VideoQualityAnalysis analysis,
            CancellationToken cancellationToken = default)
        {
            if (string.IsNullOrEmpty(outputDirectory))
                throw new ArgumentException("Output directory cannot be empty", nameof(outputDirectory));

            Directory.CreateDirectory(outputDirectory);

            var historyFile = Path.Combine(outputDirectory, "improvement_history.json");
            var history = new List<VideoQualityAnalysis>();

            // Load existing history
            if (File.Exists(historyFile))
            {
                try
                {
                    var json = await File.ReadAllTextAsync(historyFile, cancellationToken);
                    var existingHistory = JsonSerializer.Deserialize<List<VideoQualityAnalysis>>(json);
                    if (existingHistory != null)
                        history = existingHistory;
                }
                catch (Exception ex)
                {
                    _logger.LogWarning(ex, "Failed to load existing improvement history");
                }
            }

            // Add new analysis
            analysis.Iteration = history.Count + 1;
            history.Add(analysis);

            // Save updated history
            var options = new JsonSerializerOptions { WriteIndented = true };
            var updatedJson = JsonSerializer.Serialize(history, options);
            await File.WriteAllTextAsync(historyFile, updatedJson, cancellationToken);

            _logger.LogInformation("💾 Saved improvement history to {File}", historyFile);
        }
    }

    /// <summary>
    /// Scene information for quality analysis
    /// </summary>
    public class SceneInfo
    {
        public int SceneId { get; set; }
        public string Text { get; set; } = string.Empty;
        public string Description { get; set; } = string.Empty;
        public double Duration { get; set; }
        public bool HasKeyframes { get; set; }
    }

    /// <summary>
    /// Video quality analysis result
    /// </summary>
    public class VideoQualityAnalysis
    {
        public string StoryTitle { get; set; } = string.Empty;
        public DateTime Timestamp { get; set; }
        public int Iteration { get; set; }
        public int SceneCount { get; set; }
        public List<string> Issues { get; set; } = new();
        public List<string> Suggestions { get; set; } = new();
        public Dictionary<string, double> Scores { get; set; } = new();
        public double OverallScore { get; set; }
        public GptQualityAnalysis? GptAnalysis { get; set; }
    }

    /// <summary>
    /// GPT-based quality analysis result
    /// </summary>
    public class GptQualityAnalysis
    {
        public List<string>? Issues { get; set; }
        public List<string>? Suggestions { get; set; }
        public List<string>? Priorities { get; set; }
    }
}
