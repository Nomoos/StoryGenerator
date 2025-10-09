using System.Text.Json;
using StoryGenerator.Pipeline.Core;
using StoryGenerator.Pipeline.Interfaces;
using StoryGenerator.Pipeline.Stages.Models;

namespace StoryGenerator.Pipeline.Stages;

/// <summary>
/// Stage 6: Idea Validation
/// Validates selected ideas for completeness and quality.
/// </summary>
public class IdeaValidationStage : BasePipelineStage<IdeaValidationInput, IdeaValidationOutput>
{
    public override string StageName => "IdeaValidation";

    protected override async Task<IdeaValidationOutput> ExecuteCoreAsync(
        IdeaValidationInput input,
        IProgress<PipelineProgress>? progress,
        CancellationToken cancellationToken)
    {
        ReportProgress(progress, 10, "Starting idea validation...");

        var validatedIdeas = new List<ValidatedIdea>();
        int processedCount = 0;
        int totalCount = input.Ideas.Count;

        foreach (var idea in input.Ideas)
        {
            cancellationToken.ThrowIfCancellationRequested();

            var validated = ValidateIdea(idea);
            validatedIdeas.Add(validated);

            processedCount++;
            int percentComplete = 10 + (int)((processedCount / (double)totalCount) * 80);
            ReportProgress(progress, percentComplete, $"Validated {processedCount}/{totalCount} ideas");
        }

        ReportProgress(progress, 90, "Validation complete");

        return new IdeaValidationOutput
        {
            ValidatedIdeas = validatedIdeas
        };
    }

    private ValidatedIdea ValidateIdea(StoryGenerator.Core.Models.StoryIdea idea)
    {
        var validated = new ValidatedIdea
        {
            Idea = idea,
            IsValid = true,
            ValidationMessages = new List<string>()
        };

        // Check required fields
        if (string.IsNullOrWhiteSpace(idea.StoryTitle))
        {
            validated.IsValid = false;
            validated.ValidationMessages.Add("Story title is required");
        }

        if (string.IsNullOrWhiteSpace(idea.Tone))
        {
            validated.ValidationMessages.Add("Warning: Tone is not specified");
        }

        if (string.IsNullOrWhiteSpace(idea.Theme))
        {
            validated.ValidationMessages.Add("Warning: Theme is not specified");
        }

        if (idea.Potential == null)
        {
            validated.ValidationMessages.Add("Warning: Viral potential not calculated");
        }
        else if (idea.Potential.Overall < 30)
        {
            validated.ValidationMessages.Add("Warning: Low viral potential score");
        }

        return validated;
    }

    public override Task<bool> ValidateInputAsync(IdeaValidationInput input)
    {
        if (input == null)
            return Task.FromResult(false);

        if (input.Ideas == null || input.Ideas.Count == 0)
            return Task.FromResult(false);

        return Task.FromResult(true);
    }
}

/// <summary>
/// Stage 7: Idea Registry Update
/// Saves validated ideas to the idea registry for future use.
/// </summary>
public class IdeaRegistryUpdateStage : BasePipelineStage<IdeaRegistryUpdateInput, IdeaRegistryUpdateOutput>
{
    private readonly string _registryPath;

    public IdeaRegistryUpdateStage(string? registryPath = null)
    {
        _registryPath = registryPath ?? Path.Combine(
            Environment.GetFolderPath(Environment.SpecialFolder.UserProfile),
            ".storygenerator",
            "idea_registry.json");
    }

    public override string StageName => "IdeaRegistryUpdate";

    protected override async Task<IdeaRegistryUpdateOutput> ExecuteCoreAsync(
        IdeaRegistryUpdateInput input,
        IProgress<PipelineProgress>? progress,
        CancellationToken cancellationToken)
    {
        ReportProgress(progress, 10, "Starting registry update...");

        // Filter valid ideas
        var validIdeas = input.ValidatedIdeas
            .Where(v => v.IsValid)
            .Select(v => v.Idea)
            .ToList();

        ReportProgress(progress, 30, $"Saving {validIdeas.Count} valid ideas...");

        // Ensure directory exists
        var directory = Path.GetDirectoryName(_registryPath);
        if (!string.IsNullOrEmpty(directory) && !Directory.Exists(directory))
        {
            Directory.CreateDirectory(directory);
        }

        // Load existing registry if it exists
        var registry = new List<StoryGenerator.Core.Models.StoryIdea>();
        if (File.Exists(_registryPath))
        {
            var existingJson = await File.ReadAllTextAsync(_registryPath, cancellationToken);
            var existing = JsonSerializer.Deserialize<List<StoryGenerator.Core.Models.StoryIdea>>(existingJson);
            if (existing != null)
            {
                registry.AddRange(existing);
            }
        }

        ReportProgress(progress, 50, "Merging with existing registry...");

        // Add new ideas (avoid duplicates by title)
        var existingTitles = new HashSet<string>(
            registry.Select(i => i.StoryTitle),
            StringComparer.OrdinalIgnoreCase);

        int addedCount = 0;
        foreach (var idea in validIdeas)
        {
            if (!existingTitles.Contains(idea.StoryTitle))
            {
                registry.Add(idea);
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

        ReportProgress(progress, 90, $"Registry updated with {addedCount} new ideas");

        return new IdeaRegistryUpdateOutput
        {
            RegisteredCount = addedCount,
            RegistryPath = _registryPath
        };
    }

    public override Task<bool> ValidateInputAsync(IdeaRegistryUpdateInput input)
    {
        if (input == null)
            return Task.FromResult(false);

        if (input.ValidatedIdeas == null || input.ValidatedIdeas.Count == 0)
            return Task.FromResult(false);

        return Task.FromResult(true);
    }
}
