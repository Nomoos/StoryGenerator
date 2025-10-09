using StoryGenerator.Pipeline.Core;
using StoryGenerator.Pipeline.Interfaces;
using StoryGenerator.Pipeline.Stages.Models;

namespace StoryGenerator.Pipeline.Stages;

/// <summary>
/// Stage 1: Script Generation
/// Generates initial ~360 word scripts from story ideas.
/// </summary>
public class ScriptGenerationStage : BasePipelineStage<ScriptGenerationInput, ScriptGenerationOutput>
{
    public override string StageName => "ScriptGeneration";

    protected override async Task<ScriptGenerationOutput> ExecuteCoreAsync(
        ScriptGenerationInput input,
        IProgress<PipelineProgress>? progress,
        CancellationToken cancellationToken)
    {
        ReportProgress(progress, 10, "Starting script generation...");

        var generatedScripts = new List<GeneratedScript>();
        int processedCount = 0;
        int totalCount = input.StoryIdeas.Count;

        foreach (var idea in input.StoryIdeas)
        {
            cancellationToken.ThrowIfCancellationRequested();

            var script = await GenerateScriptAsync(idea, cancellationToken);
            generatedScripts.Add(script);

            processedCount++;
            int percentComplete = 10 + (int)((processedCount / (double)totalCount) * 80);
            ReportProgress(progress, percentComplete, $"Generated {processedCount}/{totalCount} scripts");
        }

        ReportProgress(progress, 90, "Script generation complete");

        return new ScriptGenerationOutput
        {
            GeneratedScripts = generatedScripts
        };
    }

    private async Task<GeneratedScript> GenerateScriptAsync(StoryGenerator.Core.Models.StoryIdea idea, CancellationToken cancellationToken)
    {
        await Task.Delay(100, cancellationToken); // Simulate LLM call

        // In production, this would call an LLM API (OpenAI, etc.)
        // Generate a script based on the story idea
        var scriptContent = GenerateScriptContent(idea);

        return new GeneratedScript
        {
            SourceIdea = idea,
            Title = idea.StoryTitle,
            Content = scriptContent,
            WordCount = scriptContent.Split(' ', StringSplitOptions.RemoveEmptyEntries).Length
        };
    }

    private string GenerateScriptContent(StoryGenerator.Core.Models.StoryIdea idea)
    {
        // Simulate script generation with template
        var template = $@"[Scene opens with a {idea.Tone ?? "contemplative"} mood]

I never expected that {idea.Outcome ?? "things would turn out this way"}. Looking back, {idea.Timeline ?? "it all started last year"}.

{idea.EmotionalCore ?? "There was something special about that moment"}.

[The story unfolds with {idea.PowerDynamic ?? "unexpected dynamics"}]

What I learned was that {idea.TargetMoral ?? "life has a way of teaching us lessons"}. The {idea.OtherCharacter ?? "person"} changed everything.

[Scene closes with {idea.TwistType ?? "a meaningful revelation"}]";

        // Expand to approximately 360 words
        var words = template.Split(' ', StringSplitOptions.RemoveEmptyEntries);
        while (words.Length < 350)
        {
            template += $" {idea.Theme ?? "This experience"}. ";
            words = template.Split(' ', StringSplitOptions.RemoveEmptyEntries);
        }

        return template;
    }

    public override Task<bool> ValidateInputAsync(ScriptGenerationInput input)
    {
        if (input == null)
            return Task.FromResult(false);

        if (input.StoryIdeas == null || input.StoryIdeas.Count == 0)
            return Task.FromResult(false);

        return Task.FromResult(true);
    }
}

/// <summary>
/// Stage 2: Script Improvement
/// Creates multiple improved versions of each script (v2, v3, v4).
/// </summary>
public class ScriptImprovementStage : BasePipelineStage<ScriptImprovementInput, ScriptImprovementOutput>
{
    public override string StageName => "ScriptImprovement";

    protected override async Task<ScriptImprovementOutput> ExecuteCoreAsync(
        ScriptImprovementInput input,
        IProgress<PipelineProgress>? progress,
        CancellationToken cancellationToken)
    {
        ReportProgress(progress, 10, "Starting script improvements...");

        var improvedScripts = new List<ImprovedScript>();
        int processedCount = 0;
        int totalOperations = input.Scripts.Count * input.ImprovementIterations;

        foreach (var script in input.Scripts)
        {
            var currentContent = script.Content;

            for (int i = 1; i <= input.ImprovementIterations; i++)
            {
                cancellationToken.ThrowIfCancellationRequested();

                var improved = await ImproveScriptAsync(script, currentContent, i, cancellationToken);
                improvedScripts.Add(improved);
                currentContent = improved.Content; // Use improved version for next iteration

                processedCount++;
                int percentComplete = 10 + (int)((processedCount / (double)totalOperations) * 80);
                ReportProgress(progress, percentComplete, $"Improved {processedCount}/{totalOperations} versions");
            }
        }

        ReportProgress(progress, 90, "Script improvements complete");

        return new ScriptImprovementOutput
        {
            ImprovedScripts = improvedScripts
        };
    }

    private async Task<ImprovedScript> ImproveScriptAsync(GeneratedScript original, string currentContent, int iteration, CancellationToken cancellationToken)
    {
        await Task.Delay(80, cancellationToken); // Simulate LLM call

        // Simulate improvements
        var improvements = new List<string>
        {
            $"Enhanced emotional depth in version {iteration}",
            $"Improved narrative pacing",
            $"Refined character voice"
        };

        // Simulate content improvement
        var improvedContent = currentContent + $"\n\n[Version {iteration} enhancement: More vivid imagery and emotional resonance]";

        return new ImprovedScript
        {
            OriginalScript = original,
            Version = $"v{iteration}",
            Content = improvedContent,
            Improvements = improvements
        };
    }

    public override Task<bool> ValidateInputAsync(ScriptImprovementInput input)
    {
        if (input == null)
            return Task.FromResult(false);

        if (input.Scripts == null || input.Scripts.Count == 0)
            return Task.FromResult(false);

        if (input.ImprovementIterations < 1 || input.ImprovementIterations > 5)
            return Task.FromResult(false);

        return Task.FromResult(true);
    }
}
