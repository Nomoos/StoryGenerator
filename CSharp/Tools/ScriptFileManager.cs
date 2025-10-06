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
    /// </summary>
    public class ScriptFileManager : IScriptFileManager
    {
        private readonly JsonSerializerOptions _jsonOptions;

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
            if (!Directory.Exists(directory))
            {
                return Task.FromResult(Enumerable.Empty<string>());
            }

            var files = Directory.GetFiles(directory, pattern, SearchOption.TopDirectoryOnly);
            return Task.FromResult(files.AsEnumerable());
        }

        public string EnsureScriptDirectory(string basePath, AudienceSegment segment, string scriptType)
        {
            var directory = Path.Combine(basePath, "scripts", scriptType, segment.Gender, segment.Age);
            
            if (!Directory.Exists(directory))
            {
                Directory.CreateDirectory(directory);
            }

            return directory;
        }

        public string EnsureScoreDirectory(string basePath, AudienceSegment segment)
        {
            var directory = Path.Combine(basePath, "scores", segment.Gender, segment.Age);
            
            if (!Directory.Exists(directory))
            {
                Directory.CreateDirectory(directory);
            }

            return directory;
        }

        public string GenerateScriptFileName(string titleId, string? version = null)
        {
            if (string.IsNullOrEmpty(version))
            {
                return $"{titleId}.md";
            }

            return $"{titleId}_{version}.md";
        }

        public string GenerateScoreFileName(string titleId, string version)
        {
            return $"{titleId}_script_{version}_score.json";
        }
    }
}
