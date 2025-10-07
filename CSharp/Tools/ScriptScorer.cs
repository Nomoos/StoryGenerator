using System;
using System.Collections.Generic;
using System.Linq;
using System.Text.Json;
using System.Threading;
using System.Threading.Tasks;
using StoryGenerator.Core.Interfaces;
using StoryGenerator.Interfaces;
using StoryGenerator.Models;

namespace StoryGenerator.Tools
{
    /// <summary>
    /// Scores scripts based on rubric criteria and narrative cohesion.
    /// Uses LLM to evaluate script quality and provide detailed feedback.
    /// Implements the Single Responsibility Principle - only handles script scoring.
    /// </summary>
    public class ScriptScorer : IScriptScorer
    {
        private readonly ILLMModelProvider _modelProvider;
        private readonly IScriptFileManager _fileManager;
        private readonly string _scoringModel;

        /// <summary>
        /// Initializes a new instance of the ScriptScorer class.
        /// </summary>
        /// <param name="modelProvider">The LLM model provider for scoring</param>
        /// <param name="fileManager">The file manager for loading scripts</param>
        /// <param name="scoringModel">Optional model name to use for scoring</param>
        /// <exception cref="ArgumentNullException">Thrown when required dependencies are null</exception>
        public ScriptScorer(ILLMModelProvider modelProvider, IScriptFileManager fileManager, string? scoringModel = null)
        {
            _modelProvider = modelProvider ?? throw new ArgumentNullException(nameof(modelProvider));
            _fileManager = fileManager ?? throw new ArgumentNullException(nameof(fileManager));
            _scoringModel = scoringModel ?? RecommendedModels.Default;
        }

        public async Task<ScriptScoringResult> ScoreScriptAsync(
            string scriptPath,
            string titleId,
            string version,
            AudienceSegment targetAudience,
            CancellationToken cancellationToken = default)
        {
            if (string.IsNullOrWhiteSpace(scriptPath))
                throw new ArgumentException("Script path cannot be null or empty", nameof(scriptPath));
            if (string.IsNullOrWhiteSpace(titleId))
                throw new ArgumentException("Title ID cannot be null or empty", nameof(titleId));
            if (string.IsNullOrWhiteSpace(version))
                throw new ArgumentException("Version cannot be null or empty", nameof(version));
            if (targetAudience == null)
                throw new ArgumentNullException(nameof(targetAudience));

            var content = await _fileManager.LoadScriptAsync(scriptPath, cancellationToken);
            return await ScoreScriptContentAsync(content, titleId, version, targetAudience, cancellationToken);
        }

        public async Task<ScriptScoringResult> ScoreScriptContentAsync(
            string scriptContent,
            string titleId,
            string version,
            AudienceSegment targetAudience,
            CancellationToken cancellationToken = default)
        {
            if (string.IsNullOrWhiteSpace(scriptContent))
                throw new ArgumentException("Script content cannot be null or empty", nameof(scriptContent));
            if (string.IsNullOrWhiteSpace(titleId))
                throw new ArgumentException("Title ID cannot be null or empty", nameof(titleId));
            if (string.IsNullOrWhiteSpace(version))
                throw new ArgumentException("Version cannot be null or empty", nameof(version));
            if (targetAudience == null)
                throw new ArgumentNullException(nameof(targetAudience));
            var systemPrompt = @"You are an expert script evaluator specializing in short-form video content.
You analyze scripts using a detailed rubric and provide constructive feedback for improvement.
Your evaluations are objective, specific, and actionable.

Evaluate scripts on these criteria (0-100 each):
1. Hook Quality: How engaging and attention-grabbing is the opening?
2. Character Development: How well are characters developed and relatable?
3. Plot Structure: Story structure, pacing, and progression quality?
4. Dialogue Quality: Naturalness and effectiveness of dialogue?
5. Emotional Impact: Emotional resonance and engagement?
6. Audience Alignment: How well does it fit the target demographic?
7. Clarity: How clear and easy to follow is the script?
8. Voice Suitability: How well does it work for text-to-speech/voiceover?

Also evaluate Narrative Cohesion (0-100): How well the story flows and maintains coherence.

Provide your response as a JSON object with this exact structure:
{
  ""rubricScores"": {
    ""hookQuality"": 85,
    ""characterDevelopment"": 70,
    ""plotStructure"": 80,
    ""dialogueQuality"": 75,
    ""emotionalImpact"": 80,
    ""audienceAlignment"": 85,
    ""clarity"": 90,
    ""voiceSuitability"": 85
  },
  ""narrativeCohesion"": 82,
  ""overallScore"": 81.5,
  ""feedback"": ""Overall feedback text"",
  ""areasForImprovement"": [""Specific area 1"", ""Specific area 2""],
  ""strengths"": [""Strength 1"", ""Strength 2""]
}";

            var userPrompt = $@"Evaluate this script for the target audience: {targetAudience}

Script:
{scriptContent}

Provide a detailed scoring and constructive feedback in JSON format as specified.";

            try
            {
                var response = await _modelProvider.GenerateAsync(
                    _scoringModel,
                    systemPrompt,
                    userPrompt,
                    temperature: 0.3f,
                    cancellationToken: cancellationToken);

                // Extract JSON from response
                var jsonStart = response.IndexOf('{');
                var jsonEnd = response.LastIndexOf('}');
                
                if (jsonStart < 0 || jsonEnd < 0)
                {
                    throw new InvalidOperationException("No JSON found in LLM response");
                }

                var jsonContent = response.Substring(jsonStart, jsonEnd - jsonStart + 1);
                var scoringData = JsonSerializer.Deserialize<ScoringResponse>(jsonContent, new JsonSerializerOptions
                {
                    PropertyNameCaseInsensitive = true
                });

                if (scoringData == null)
                {
                    throw new InvalidOperationException("Failed to parse scoring response");
                }

                var result = new ScriptScoringResult
                {
                    Version = version,
                    TitleId = titleId,
                    TargetAudience = targetAudience,
                    RubricScores = scoringData.RubricScores,
                    NarrativeCohesion = scoringData.NarrativeCohesion,
                    OverallScore = scoringData.OverallScore,
                    Feedback = scoringData.Feedback,
                    AreasForImprovement = scoringData.AreasForImprovement,
                    Strengths = scoringData.Strengths,
                    ScoredAt = DateTime.UtcNow
                };

                return result;
            }
            catch (Exception ex)
            {
                throw new InvalidOperationException($"Failed to score script: {ex.Message}", ex);
            }
        }

        public async Task<IEnumerable<ScriptScoringResult>> ScoreScriptsInDirectoryAsync(
            string scriptsDirectory,
            AudienceSegment targetAudience,
            string version,
            CancellationToken cancellationToken = default)
        {
            var scriptFiles = await _fileManager.FindScriptFilesAsync(scriptsDirectory, "*.md", cancellationToken);
            var results = new List<ScriptScoringResult>();

            foreach (var scriptPath in scriptFiles)
            {
                var fileName = System.IO.Path.GetFileNameWithoutExtension(scriptPath);
                var titleId = fileName.Replace($"_{version}", "");

                var result = await ScoreScriptAsync(scriptPath, titleId, version, targetAudience, cancellationToken);
                results.Add(result);
            }

            return results;
        }

        public bool ValidateScoringConfiguration()
        {
            return !string.IsNullOrEmpty(_scoringModel);
        }

        private class ScoringResponse
        {
            public ScriptRubricScores RubricScores { get; set; } = new();
            public double NarrativeCohesion { get; set; }
            public double OverallScore { get; set; }
            public string Feedback { get; set; } = string.Empty;
            public List<string> AreasForImprovement { get; set; } = new();
            public List<string> Strengths { get; set; } = new();
        }
    }
}
