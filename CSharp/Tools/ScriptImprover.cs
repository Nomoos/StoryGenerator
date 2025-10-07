using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Threading;
using System.Threading.Tasks;
using StoryGenerator.Core.Interfaces;
using StoryGenerator.Interfaces;
using StoryGenerator.Models;

namespace StoryGenerator.Tools
{
    /// <summary>
    /// Orchestrates the script improvement process.
    /// Improves scripts using GPT or local LLM, scores them, and iterates until improvement plateaus.
    /// Implements the Facade pattern to provide a simple interface for complex script improvement operations.
    /// Follows SOLID principles with dependency injection and single responsibility.
    /// </summary>
    public class ScriptImprover
    {
        private readonly ILLMModelProvider _modelProvider;
        private readonly IScriptScorer _scriptScorer;
        private readonly IScriptIterator _scriptIterator;
        private readonly IScriptFileManager _fileManager;
        private readonly string _baseScriptsPath;
        private readonly string _baseScoresPath;
        
        /// <summary>
        /// Minimum improvement threshold (in points) required to continue iterating.
        /// </summary>
        private const double ImprovementThreshold = 2.0;
        
        /// <summary>
        /// Maximum number of iterations (v2, v3, v4, v5, v6).
        /// </summary>
        private const int MaxIterations = 5;

        /// <summary>
        /// Initializes a new instance of the ScriptImprover class.
        /// </summary>
        /// <param name="modelProvider">The LLM model provider</param>
        /// <param name="scriptScorer">The script scorer for evaluation</param>
        /// <param name="scriptIterator">The script iterator for improvements</param>
        /// <param name="fileManager">The file manager for I/O operations</param>
        /// <param name="baseScriptsPath">Base path for scripts directory</param>
        /// <param name="baseScoresPath">Base path for scores directory</param>
        /// <exception cref="ArgumentNullException">Thrown when required dependencies are null</exception>
        public ScriptImprover(
            ILLMModelProvider modelProvider,
            IScriptScorer scriptScorer,
            IScriptIterator scriptIterator,
            IScriptFileManager fileManager,
            string baseScriptsPath,
            string baseScoresPath)
        {
            _modelProvider = modelProvider ?? throw new ArgumentNullException(nameof(modelProvider));
            _scriptScorer = scriptScorer ?? throw new ArgumentNullException(nameof(scriptScorer));
            _scriptIterator = scriptIterator ?? throw new ArgumentNullException(nameof(scriptIterator));
            _fileManager = fileManager ?? throw new ArgumentNullException(nameof(fileManager));
            _baseScriptsPath = baseScriptsPath ?? throw new ArgumentNullException(nameof(baseScriptsPath));
            _baseScoresPath = baseScoresPath ?? throw new ArgumentNullException(nameof(baseScoresPath));
        }

        /// <summary>
        /// Improves a single script iteratively until improvement plateaus.
        /// </summary>
        /// <param name="originalScriptPath">Path to the original script (v0 or v1)</param>
        /// <param name="titleId">The title ID</param>
        /// <param name="targetAudience">Target audience segment</param>
        /// <param name="cancellationToken">Cancellation token</param>
        /// <returns>The best script version achieved</returns>
        /// <exception cref="ArgumentException">Thrown when parameters are invalid</exception>
        /// <exception cref="ArgumentNullException">Thrown when required parameters are null</exception>
        public async Task<ScriptVersion> ImproveScriptAsync(
            string originalScriptPath,
            string titleId,
            AudienceSegment targetAudience,
            CancellationToken cancellationToken = default)
        {
            if (string.IsNullOrWhiteSpace(originalScriptPath))
                throw new ArgumentException("Script path cannot be null or empty", nameof(originalScriptPath));
            if (string.IsNullOrWhiteSpace(titleId))
                throw new ArgumentException("Title ID cannot be null or empty", nameof(titleId));
            if (targetAudience == null)
                throw new ArgumentNullException(nameof(targetAudience));
        /// <returns>The best script version achieved</returns>
        public async Task<ScriptVersion> ImproveScriptAsync(
            string originalScriptPath,
            string titleId,
            AudienceSegment targetAudience,
            CancellationToken cancellationToken = default)
        {
            Console.WriteLine($"\n{'=',-60}");
            Console.WriteLine($"Improving script: {titleId}");
            Console.WriteLine($"Target audience: {targetAudience}");
            Console.WriteLine($"{'=',-60}\n");

            // Determine starting version
            var originalVersion = ExtractVersionFromPath(originalScriptPath);
            var startingVersionNum = ParseVersionNumber(originalVersion);

            // Score the original script
            Console.WriteLine($"Scoring original script ({originalVersion})...");
            var currentScore = await _scriptScorer.ScoreScriptAsync(
                originalScriptPath,
                titleId,
                originalVersion,
                targetAudience,
                cancellationToken);

            Console.WriteLine($"Original score: {currentScore.OverallScore:F1}/100");
            
            // Save original score
            await _fileManager.SaveScriptScoreAsync(currentScore, _baseScoresPath, cancellationToken);

            var currentScriptPath = originalScriptPath;
            var currentVersionNum = startingVersionNum;
            var bestScore = currentScore.OverallScore;
            var bestVersion = new ScriptVersion
            {
                TitleId = titleId,
                Version = originalVersion,
                Content = await _fileManager.LoadScriptAsync(originalScriptPath, cancellationToken),
                FilePath = originalScriptPath,
                TargetAudience = targetAudience,
                Score = bestScore
            };

            // Iterate to improve
            for (int i = 0; i < MaxIterations; i++)
            {
                var nextVersionNum = currentVersionNum + 1;
                var nextVersion = $"v{nextVersionNum}";

                Console.WriteLine($"\nCreating improved version: {nextVersion}...");

                // Generate improved script
                var improvedScript = await _scriptIterator.IterateScriptAsync(
                    currentScriptPath,
                    currentScore,
                    nextVersion,
                    cancellationToken);

                // Save improved script
                var improvedScriptPath = await _fileManager.SaveIteratedScriptAsync(
                    improvedScript,
                    _baseScriptsPath,
                    cancellationToken);

                Console.WriteLine($"Saved improved script to: {improvedScriptPath}");

                // Score improved script
                Console.WriteLine($"Scoring {nextVersion}...");
                var improvedScore = await _scriptScorer.ScoreScriptAsync(
                    improvedScriptPath,
                    titleId,
                    nextVersion,
                    targetAudience,
                    cancellationToken);

                Console.WriteLine($"{nextVersion} score: {improvedScore.OverallScore:F1}/100");

                // Save score
                await _fileManager.SaveScriptScoreAsync(improvedScore, _baseScoresPath, cancellationToken);

                // Calculate improvement
                var improvement = improvedScore.OverallScore - currentScore.OverallScore;
                Console.WriteLine($"Improvement: {improvement:+0.0;-0.0}/100");

                // Check if this is the best version so far
                if (improvedScore.OverallScore > bestScore)
                {
                    bestScore = improvedScore.OverallScore;
                    bestVersion = improvedScript;
                    bestVersion.Score = bestScore;
                    bestVersion.FilePath = improvedScriptPath;
                    Console.WriteLine($"✓ New best score: {bestScore:F1}/100");
                }

                // Check if improvement has plateaued
                if (improvement < ImprovementThreshold)
                {
                    Console.WriteLine($"\nImprovement plateaued (< {ImprovementThreshold} points). Stopping iteration.");
                    break;
                }

                // Update for next iteration
                currentScriptPath = improvedScriptPath;
                currentScore = improvedScore;
                currentVersionNum = nextVersionNum;
            }

            Console.WriteLine($"\n{'=',-60}");
            Console.WriteLine($"Best version: {bestVersion.Version} with score {bestScore:F1}/100");
            Console.WriteLine($"{'=',-60}\n");

            return bestVersion;
        }

        /// <summary>
        /// Improves all scripts in a directory for a specific audience segment.
        /// </summary>
        /// <param name="segment">Audience segment (e.g., "men", "women")</param>
        /// <param name="age">Age range (e.g., "18-23")</param>
        /// <param name="sourceDirectory">Source directory type (e.g., "raw_local", "iter_local")</param>
        /// <param name="cancellationToken">Cancellation token</param>
        /// <returns>Collection of best script versions</returns>
        public async Task<IEnumerable<ScriptVersion>> ImproveScriptsInSegmentAsync(
            string segment,
            string age,
            string sourceDirectory = "raw_local",
            CancellationToken cancellationToken = default)
        {
            var targetAudience = new AudienceSegment(segment, age);
            var scriptsDir = Path.Combine(_baseScriptsPath, "scripts", sourceDirectory, segment, age);

            if (!Directory.Exists(scriptsDir))
            {
                Console.WriteLine($"Warning: Scripts directory not found: {scriptsDir}");
                return Enumerable.Empty<ScriptVersion>();
            }

            var scriptFiles = await _fileManager.FindScriptFilesAsync(scriptsDir, "*.md", cancellationToken);
            var results = new List<ScriptVersion>();

            Console.WriteLine($"\nFound {scriptFiles.Count()} scripts to improve in {segment}/{age}");

            foreach (var scriptPath in scriptFiles)
            {
                var fileName = Path.GetFileNameWithoutExtension(scriptPath);
                var titleId = ExtractTitleIdFromFileName(fileName);

                try
                {
                    var bestVersion = await ImproveScriptAsync(
                        scriptPath,
                        titleId,
                        targetAudience,
                        cancellationToken);

                    results.Add(bestVersion);
                }
                catch (Exception ex)
                {
                    Console.WriteLine($"Error improving script {titleId}: {ex.Message}");
                }
            }

            return results;
        }

        /// <summary>
        /// Improves all scripts across all segments and age groups.
        /// </summary>
        /// <param name="cancellationToken">Cancellation token</param>
        /// <returns>Collection of all improved script versions</returns>
        public async Task<IEnumerable<ScriptVersion>> ImproveAllScriptsAsync(
            CancellationToken cancellationToken = default)
        {
            var segments = new[] { "men", "women" };
            var ageRanges = new[] { "10-13", "14-17", "18-23", "24-30" };
            var allResults = new List<ScriptVersion>();

            foreach (var segment in segments)
            {
                foreach (var age in ageRanges)
                {
                    Console.WriteLine($"\n{'=',80}");
                    Console.WriteLine($"Processing segment: {segment}/{age}");
                    Console.WriteLine($"{'=',80}");

                    var results = await ImproveScriptsInSegmentAsync(
                        segment,
                        age,
                        "raw_local",
                        cancellationToken);

                    allResults.AddRange(results);
                }
            }

            return allResults;
        }

        private string ExtractVersionFromPath(string path)
        {
            var fileName = Path.GetFileNameWithoutExtension(path);
            
            if (fileName.Contains("_v"))
            {
                var parts = fileName.Split("_v");
                if (parts.Length > 1 && int.TryParse(parts[1], out _))
                {
                    return $"v{parts[1]}";
                }
            }
            
            return "v1"; // Default to v1 for raw scripts
        }

        private int ParseVersionNumber(string version)
        {
            if (version.StartsWith("v") && int.TryParse(version.Substring(1), out var num))
            {
                return num;
            }
            return 0;
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
