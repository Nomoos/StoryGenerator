using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text.Json;
using System.Threading;
using System.Threading.Tasks;
using StoryGenerator.Interfaces;
using StoryGenerator.Models;

namespace StoryGenerator.Tools
{
    /// <summary>
    /// Manages script file I/O operations.
    /// Handles reading, writing, and organizing scripts in the proper directory structure.
    /// Implements the Single Responsibility Principle - only handles file operations.
    /// </summary>
    public class ScriptFileManager : IScriptFileManager
    {
        private readonly JsonSerializerOptions _jsonOptions;

        /// <summary>
        /// Initializes a new instance of the ScriptFileManager class.
        /// </summary>
        public ScriptFileManager()
        {
            _jsonOptions = new JsonSerializerOptions
            {
                WriteIndented = true,
                PropertyNamingPolicy = JsonNamingPolicy.CamelCase
            };
        }

        public async Task<string> SaveRawScriptAsync(
            ScriptVersion scriptVersion,
            string baseScriptsPath,
            CancellationToken cancellationToken = default)
        {
            if (scriptVersion == null)
                throw new ArgumentNullException(nameof(scriptVersion));
            if (string.IsNullOrWhiteSpace(baseScriptsPath))
                throw new ArgumentException("Base scripts path cannot be null or empty", nameof(baseScriptsPath));
            var directory = EnsureScriptDirectory(baseScriptsPath, scriptVersion.TargetAudience, "raw_local");
            var fileName = GenerateScriptFileName(scriptVersion.TitleId);
            var filePath = Path.Combine(directory, fileName);

            await File.WriteAllTextAsync(filePath, scriptVersion.Content, cancellationToken);

            scriptVersion.FilePath = filePath;
            return filePath;
        }

        public async Task<string> SaveIteratedScriptAsync(
            ScriptVersion scriptVersion,
            string baseScriptsPath,
            CancellationToken cancellationToken = default)
        {
            if (scriptVersion == null)
                throw new ArgumentNullException(nameof(scriptVersion));
            if (string.IsNullOrWhiteSpace(baseScriptsPath))
                throw new ArgumentException("Base scripts path cannot be null or empty", nameof(baseScriptsPath));
            // Save to gpt_improved directory instead of iter_local
            var directory = EnsureScriptDirectory(baseScriptsPath, scriptVersion.TargetAudience, "gpt_improved");
            var fileName = GenerateScriptFileName(scriptVersion.TitleId, scriptVersion.Version);
            var filePath = Path.Combine(directory, fileName);

            await File.WriteAllTextAsync(filePath, scriptVersion.Content, cancellationToken);

            scriptVersion.FilePath = filePath;
            return filePath;
        }

        public async Task<string> LoadScriptAsync(
            string scriptPath,
            CancellationToken cancellationToken = default)
        {
            if (string.IsNullOrWhiteSpace(scriptPath))
                throw new ArgumentException("Script path cannot be null or empty", nameof(scriptPath));
            if (!File.Exists(scriptPath))
            {
                throw new FileNotFoundException($"Script file not found: {scriptPath}");
            }

            return await File.ReadAllTextAsync(scriptPath, cancellationToken);
        }

        public async Task<string> SaveScriptScoreAsync(
            ScriptScoringResult scoringResult,
            string baseScoresPath,
            CancellationToken cancellationToken = default)
        {
            if (scoringResult == null)
                throw new ArgumentNullException(nameof(scoringResult));
            if (string.IsNullOrWhiteSpace(baseScoresPath))
                throw new ArgumentException("Base scores path cannot be null or empty", nameof(baseScoresPath));
            var directory = EnsureScoreDirectory(baseScoresPath, scoringResult.TargetAudience);
            var fileName = GenerateScoreFileName(scoringResult.TitleId, scoringResult.Version);
            var filePath = Path.Combine(directory, fileName);

            var json = JsonSerializer.Serialize(scoringResult, _jsonOptions);
            await File.WriteAllTextAsync(filePath, json, cancellationToken);

            return filePath;
        }

        public async Task<ScriptScoringResult> LoadScriptScoreAsync(
            string scorePath,
            CancellationToken cancellationToken = default)
        {
            if (string.IsNullOrWhiteSpace(scorePath))
                throw new ArgumentException("Score path cannot be null or empty", nameof(scorePath));
            if (!File.Exists(scorePath))
            {
                throw new FileNotFoundException($"Score file not found: {scorePath}");
            }

            var json = await File.ReadAllTextAsync(scorePath, cancellationToken);
            var result = JsonSerializer.Deserialize<ScriptScoringResult>(json, _jsonOptions);

            if (result == null)
            {
                throw new InvalidOperationException($"Failed to deserialize score file: {scorePath}");
            }

            return result;
        }

        public Task<IEnumerable<string>> FindScriptFilesAsync(
            string directory,
            string pattern = "*.md",
            CancellationToken cancellationToken = default)
        {
            if (string.IsNullOrWhiteSpace(directory))
                throw new ArgumentException("Directory cannot be null or empty", nameof(directory));
            if (string.IsNullOrWhiteSpace(pattern))
                throw new ArgumentException("Pattern cannot be null or empty", nameof(pattern));
            if (!Directory.Exists(directory))
            {
                return Task.FromResult(Enumerable.Empty<string>());
            }

            var files = Directory.GetFiles(directory, pattern, SearchOption.TopDirectoryOnly);
            return Task.FromResult(files.AsEnumerable());
        }

        public string EnsureScriptDirectory(string basePath, AudienceSegment segment, string scriptType)
        {
            if (string.IsNullOrWhiteSpace(basePath))
                throw new ArgumentException("Base path cannot be null or empty", nameof(basePath));
            if (segment == null)
                throw new ArgumentNullException(nameof(segment));
            if (string.IsNullOrWhiteSpace(scriptType))
                throw new ArgumentException("Script type cannot be null or empty", nameof(scriptType));
            var directory = Path.Combine(basePath, "scripts", scriptType, segment.Gender, segment.Age);
            
            if (!Directory.Exists(directory))
            {
                Directory.CreateDirectory(directory);
            }

            return directory;
        }

        public string EnsureScoreDirectory(string basePath, AudienceSegment segment)
        {
            if (string.IsNullOrWhiteSpace(basePath))
                throw new ArgumentException("Base path cannot be null or empty", nameof(basePath));
            if (segment == null)
                throw new ArgumentNullException(nameof(segment));
            var directory = Path.Combine(basePath, "scores", segment.Gender, segment.Age);
            
            if (!Directory.Exists(directory))
            {
                Directory.CreateDirectory(directory);
            }

            return directory;
        }

        public string GenerateScriptFileName(string titleId, string? version = null)
        {
            if (string.IsNullOrWhiteSpace(titleId))
                throw new ArgumentException("Title ID cannot be null or empty", nameof(titleId));
            if (string.IsNullOrEmpty(version))
            {
                return $"{titleId}.md";
            }

            return $"{titleId}_{version}.md";
        }

        public string GenerateScoreFileName(string titleId, string version)
        {
            if (string.IsNullOrWhiteSpace(titleId))
                throw new ArgumentException("Title ID cannot be null or empty", nameof(titleId));
            if (string.IsNullOrWhiteSpace(version))
                throw new ArgumentException("Version cannot be null or empty", nameof(version));
            return $"{titleId}_script_{version}_score.json";
        }
    }
}
