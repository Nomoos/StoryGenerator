using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading;
using System.Threading.Tasks;
using StoryGenerator.Core.Interfaces;
using StoryGenerator.Interfaces;
using StoryGenerator.Models;

namespace StoryGenerator.Tools
{
    /// <summary>
    /// Iterates and improves scripts based on feedback.
    /// Takes scored scripts and produces improved versions using LLM.
    /// Implements the Single Responsibility Principle - only handles script iteration.
    /// </summary>
    public class ScriptIterator : IScriptIterator
    {
        private readonly ILLMModelProvider _modelProvider;
        private readonly IScriptFileManager _fileManager;
        private readonly string _iterationModel;

        /// <summary>
        /// Initializes a new instance of the ScriptIterator class.
        /// </summary>
        /// <param name="modelProvider">The LLM model provider for generating improvements</param>
        /// <param name="fileManager">The file manager for loading scripts</param>
        /// <param name="iterationModel">Optional model name to use for iteration</param>
        /// <exception cref="ArgumentNullException">Thrown when required dependencies are null</exception>
        public ScriptIterator(ILLMModelProvider modelProvider, IScriptFileManager fileManager, string? iterationModel = null)
        {
            _modelProvider = modelProvider ?? throw new ArgumentNullException(nameof(modelProvider));
            _fileManager = fileManager ?? throw new ArgumentNullException(nameof(fileManager));
            _iterationModel = iterationModel ?? RecommendedModels.Default;
        }

        public async Task<ScriptVersion> IterateScriptAsync(
            string originalScriptPath,
            ScriptScoringResult scoringResult,
            string targetVersion,
            CancellationToken cancellationToken = default)
        {
            if (string.IsNullOrWhiteSpace(originalScriptPath))
                throw new ArgumentException("Script path cannot be null or empty", nameof(originalScriptPath));
            if (scoringResult == null)
                throw new ArgumentNullException(nameof(scoringResult));
            if (string.IsNullOrWhiteSpace(targetVersion))
                throw new ArgumentException("Target version cannot be null or empty", nameof(targetVersion));

            var originalContent = await _fileManager.LoadScriptAsync(originalScriptPath, cancellationToken);
            
            var feedback = BuildIterationFeedback(scoringResult);
            
            return await IterateScriptWithFeedbackAsync(
                originalScriptPath,
                feedback,
                scoringResult.TitleId,
                targetVersion,
                scoringResult.TargetAudience,
                cancellationToken);
        }

        public async Task<ScriptVersion> IterateScriptWithFeedbackAsync(
            string originalScriptPath,
            string feedback,
            string titleId,
            string targetVersion,
            AudienceSegment targetAudience,
            CancellationToken cancellationToken = default)
        {
            if (string.IsNullOrWhiteSpace(originalScriptPath))
                throw new ArgumentException("Script path cannot be null or empty", nameof(originalScriptPath));
            if (string.IsNullOrWhiteSpace(feedback))
                throw new ArgumentException("Feedback cannot be null or empty", nameof(feedback));
            if (string.IsNullOrWhiteSpace(titleId))
                throw new ArgumentException("Title ID cannot be null or empty", nameof(titleId));
            if (string.IsNullOrWhiteSpace(targetVersion))
                throw new ArgumentException("Target version cannot be null or empty", nameof(targetVersion));
            if (targetAudience == null)
                throw new ArgumentNullException(nameof(targetAudience));
            var originalContent = await _fileManager.LoadScriptAsync(originalScriptPath, cancellationToken);
            
            var improvedContent = await ApplyImprovementsAsync(
                originalContent,
                new[] { feedback },
                cancellationToken);

            var scriptVersion = new ScriptVersion
            {
                TitleId = titleId,
                Version = targetVersion,
                Content = improvedContent,
                TargetAudience = targetAudience,
                CreatedAt = DateTime.UtcNow,
                AppliedFeedback = feedback,
                GenerationSource = "iteration",
                PreviousVersion = ExtractVersionFromPath(originalScriptPath)
            };

            return scriptVersion;
        }

        public async Task<IEnumerable<ScriptVersion>> IterateScriptsAsync(
            string scriptsDirectory,
            IEnumerable<ScriptScoringResult> scoringResults,
            string targetVersion,
            CancellationToken cancellationToken = default)
        {
            var results = new List<ScriptVersion>();
            var resultsDict = scoringResults.ToDictionary(r => r.TitleId, r => r);

            var scriptFiles = await _fileManager.FindScriptFilesAsync(scriptsDirectory, "*.md", cancellationToken);

            foreach (var scriptPath in scriptFiles)
            {
                var fileName = System.IO.Path.GetFileNameWithoutExtension(scriptPath);
                var titleId = ExtractTitleIdFromFileName(fileName);

                if (resultsDict.TryGetValue(titleId, out var scoringResult))
                {
                    var iteratedScript = await IterateScriptAsync(
                        scriptPath,
                        scoringResult,
                        targetVersion,
                        cancellationToken);

                    results.Add(iteratedScript);
                }
            }

            return results;
        }

        public async Task<string> ApplyImprovementsAsync(
            string scriptContent,
            IEnumerable<string> improvements,
            CancellationToken cancellationToken = default)
        {
            var systemPrompt = @"You are an expert script editor specializing in improving short-form video content.
Your task is to enhance scripts based on specific feedback while preserving the core narrative and tone.
Focus on making targeted improvements that address the identified issues.

Guidelines:
- Maintain the original story structure and key plot points
- Enhance clarity, pacing, and hooks where needed
- Improve dialogue to be more natural and engaging
- Ensure the script remains suitable for text-to-speech synthesis
- Keep the word count similar to the original
- Make the opening more compelling if feedback suggests it
- Strengthen emotional impact where appropriate";

            var feedbackText = string.Join("\n", improvements.Select((f, i) => $"{i + 1}. {f}"));

            var userPrompt = $@"Improve the following script based on this feedback:

FEEDBACK:
{feedbackText}

ORIGINAL SCRIPT:
{scriptContent}

Provide the improved script only, without any explanations or additional text.
The improved script should directly address the feedback while maintaining the core narrative.";

            try
            {
                var response = await _modelProvider.GenerateAsync(
                    _iterationModel,
                    systemPrompt,
                    userPrompt,
                    temperature: 0.7f,
                    cancellationToken: cancellationToken);

                return response.Trim();
            }
            catch (Exception ex)
            {
                throw new InvalidOperationException($"Failed to apply improvements: {ex.Message}", ex);
            }
        }

        private string BuildIterationFeedback(ScriptScoringResult scoringResult)
        {
            var feedback = new StringBuilder();
            
            feedback.AppendLine($"Overall Score: {scoringResult.OverallScore:F1}/100");
            feedback.AppendLine();
            feedback.AppendLine("Areas for Improvement:");
            
            foreach (var area in scoringResult.AreasForImprovement)
            {
                feedback.AppendLine($"- {area}");
            }
            
            feedback.AppendLine();
            feedback.AppendLine("Specific Rubric Scores:");
            
            var rubric = scoringResult.RubricScores;
            if (rubric.HookQuality < 80)
                feedback.AppendLine($"- Hook Quality: {rubric.HookQuality}/100 - Improve the opening to better grab attention");
            
            if (rubric.Clarity < 80)
                feedback.AppendLine($"- Clarity: {rubric.Clarity}/100 - Enhance readability and flow");
            
            if (rubric.DialogueQuality < 80)
                feedback.AppendLine($"- Dialogue Quality: {rubric.DialogueQuality}/100 - Make dialogue more natural");
            
            if (rubric.EmotionalImpact < 80)
                feedback.AppendLine($"- Emotional Impact: {rubric.EmotionalImpact}/100 - Strengthen emotional resonance");
            
            if (rubric.PlotStructure < 80)
                feedback.AppendLine($"- Plot Structure: {rubric.PlotStructure}/100 - Improve pacing and structure");
            
            if (scoringResult.NarrativeCohesion < 80)
                feedback.AppendLine($"- Narrative Cohesion: {scoringResult.NarrativeCohesion}/100 - Improve story flow");
            
            feedback.AppendLine();
            feedback.AppendLine("Strengths to Maintain:");
            foreach (var strength in scoringResult.Strengths)
            {
                feedback.AppendLine($"- {strength}");
            }

            return feedback.ToString();
        }

        private string ExtractVersionFromPath(string path)
        {
            var fileName = System.IO.Path.GetFileNameWithoutExtension(path);
            
            if (fileName.Contains("_v"))
            {
                var parts = fileName.Split("_v");
                if (parts.Length > 1)
                {
                    return $"v{parts[1]}";
                }
            }
            
            return "v0";
        }

        private string ExtractTitleIdFromFileName(string fileName)
        {
            if (fileName.Contains("_v"))
            {
                var parts = fileName.Split("_v");
                return parts[0];
            }
            
            return fileName;
        }
    }
}
