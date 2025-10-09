using System.Text.Json;
using StoryGenerator.Pipeline.Core;
using StoryGenerator.Pipeline.Interfaces;
using StoryGenerator.Pipeline.Stages.Models;

namespace StoryGenerator.Pipeline.Stages;

/// <summary>
/// Stage 7: Script Validation
/// Validates enhanced scripts for completeness and quality.
/// </summary>
public class ScriptValidationStage : BasePipelineStage<ScriptValidationInput, ScriptValidationOutput>
{
    public override string StageName => "ScriptValidation";

    protected override async Task<ScriptValidationOutput> ExecuteCoreAsync(
        ScriptValidationInput input,
        IProgress<PipelineProgress>? progress,
        CancellationToken cancellationToken)
    {
        ReportProgress(progress, 10, "Starting script validation...");

        var validatedScripts = new List<ValidatedScript>();
        int processedCount = 0;
        int totalCount = input.Scripts.Count;

        foreach (var script in input.Scripts)
        {
            cancellationToken.ThrowIfCancellationRequested();

            var validated = ValidateScript(script);
            validatedScripts.Add(validated);

            processedCount++;
            int percentComplete = 10 + (int)((processedCount / (double)totalCount) * 80);
            ReportProgress(progress, percentComplete, $"Validated {processedCount}/{totalCount} scripts");
        }

        ReportProgress(progress, 90, "Script validation complete");

        return new ScriptValidationOutput
        {
            ValidatedScripts = validatedScripts
        };
    }

    private ValidatedScript ValidateScript(EnhancedScript script)
    {
        var validated = new ValidatedScript
        {
            Script = script,
            IsValid = true,
            ValidationMessages = new List<string>()
        };

        // Check content exists
        if (string.IsNullOrWhiteSpace(script.Content))
        {
            validated.IsValid = false;
            validated.ValidationMessages.Add("Script content is empty");
            return validated;
        }

        // Check word count (target ~360 words)
        var wordCount = script.Content.Split(' ', StringSplitOptions.RemoveEmptyEntries).Length;
        if (wordCount < 200)
        {
            validated.ValidationMessages.Add($"Warning: Script is short ({wordCount} words)");
        }
        else if (wordCount > 500)
        {
            validated.ValidationMessages.Add($"Warning: Script is long ({wordCount} words)");
        }

        // Check for enhancements
        if (script.Enhancements == null || script.Enhancements.Count == 0)
        {
            validated.ValidationMessages.Add("Warning: No enhancements recorded");
        }

        // Check for source script
        if (script.SourceScript == null)
        {
            validated.ValidationMessages.Add("Warning: No source script reference");
        }

        return validated;
    }

    public override Task<bool> ValidateInputAsync(ScriptValidationInput input)
    {
        if (input == null)
            return Task.FromResult(false);

        if (input.Scripts == null || input.Scripts.Count == 0)
            return Task.FromResult(false);

        return Task.FromResult(true);
    }
}

/// <summary>
/// Stage 8: Script Registry Update
/// Saves validated scripts to the script registry.
/// </summary>
public class ScriptRegistryUpdateStage : BasePipelineStage<ScriptRegistryUpdateInput, ScriptRegistryUpdateOutput>
{
    private readonly string _registryPath;

    public ScriptRegistryUpdateStage(string? registryPath = null)
    {
        _registryPath = registryPath ?? Path.Combine(
            Environment.GetFolderPath(Environment.SpecialFolder.UserProfile),
            ".storygenerator",
            "script_registry.json");
    }

    public override string StageName => "ScriptRegistryUpdate";

    protected override async Task<ScriptRegistryUpdateOutput> ExecuteCoreAsync(
        ScriptRegistryUpdateInput input,
        IProgress<PipelineProgress>? progress,
        CancellationToken cancellationToken)
    {
        ReportProgress(progress, 10, "Starting registry update...");

        // Filter valid scripts
        var validScripts = input.ValidatedScripts
            .Where(v => v.IsValid)
            .Select(v => v.Script)
            .ToList();

        ReportProgress(progress, 30, $"Saving {validScripts.Count} valid scripts...");

        // Ensure directory exists
        var directory = Path.GetDirectoryName(_registryPath);
        if (!string.IsNullOrEmpty(directory) && !Directory.Exists(directory))
        {
            Directory.CreateDirectory(directory);
        }

        // Load existing registry if it exists
        var registry = new List<ScriptRegistryEntry>();
        if (File.Exists(_registryPath))
        {
            var existingJson = await File.ReadAllTextAsync(_registryPath, cancellationToken);
            var existing = JsonSerializer.Deserialize<List<ScriptRegistryEntry>>(existingJson);
            if (existing != null)
            {
                registry.AddRange(existing);
            }
        }

        ReportProgress(progress, 50, "Merging with existing registry...");

        // Add new scripts (avoid duplicates by content hash)
        var existingHashes = new HashSet<int>(registry.Select(e => e.ContentHash));

        int addedCount = 0;
        foreach (var script in validScripts)
        {
            var contentHash = script.Content.GetHashCode();
            if (!existingHashes.Contains(contentHash))
            {
                registry.Add(new ScriptRegistryEntry
                {
                    Id = Guid.NewGuid().ToString(),
                    Content = script.Content,
                    ContentHash = contentHash,
                    EnhancementCount = script.Enhancements?.Count ?? 0,
                    RegisteredAt = DateTime.UtcNow
                });
                addedCount++;
            }
        }

        ReportProgress(progress, 70, "Saving updated registry...");

        // Save updated registry
        var options = new JsonSerializerOptions
        {
            WriteIndented = true
        };
        var json = JsonSerializer.Serialize(registry, options);
        await File.WriteAllTextAsync(_registryPath, json, cancellationToken);

        ReportProgress(progress, 90, $"Registry updated with {addedCount} new scripts");

        return new ScriptRegistryUpdateOutput
        {
            RegisteredCount = addedCount,
            RegistryPath = _registryPath
        };
    }

    public override Task<bool> ValidateInputAsync(ScriptRegistryUpdateInput input)
    {
        if (input == null)
            return Task.FromResult(false);

        if (input.ValidatedScripts == null || input.ValidatedScripts.Count == 0)
            return Task.FromResult(false);

        return Task.FromResult(true);
    }
}

/// <summary>
/// Entry in the script registry
/// </summary>
public class ScriptRegistryEntry
{
    public string Id { get; set; } = string.Empty;
    public string Content { get; set; } = string.Empty;
    public int ContentHash { get; set; }
    public int EnhancementCount { get; set; }
    public DateTime RegisteredAt { get; set; }
}
