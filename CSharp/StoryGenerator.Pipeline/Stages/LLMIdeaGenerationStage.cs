using StoryGenerator.Pipeline.Core;
using StoryGenerator.Pipeline.Interfaces;
using StoryGenerator.Pipeline.Stages.Models;
using PrismQ.Shared.Models;

namespace StoryGenerator.Pipeline.Stages;

/// <summary>
/// Stage 2: LLM Idea Generation
/// Uses LLM to generate multiple story idea variations from adapted content.
/// </summary>
public class LLMIdeaGenerationStage : BasePipelineStage<LLMIdeaGenerationInput, LLMIdeaGenerationOutput>
{
    public override string StageName => "LLMIdeaGeneration";

    protected override async Task<LLMIdeaGenerationOutput> ExecuteCoreAsync(
        LLMIdeaGenerationInput input,
        IProgress<PipelineProgress>? progress,
        CancellationToken cancellationToken)
    {
        ReportProgress(progress, 10, "Starting LLM idea generation...");

        var generatedIdeas = new List<StoryIdea>();
        int processedCount = 0;
        int totalCount = input.AdaptedIdeas.Count;

        foreach (var adaptedIdea in input.AdaptedIdeas)
        {
            cancellationToken.ThrowIfCancellationRequested();

            // Generate multiple variations
            for (int i = 0; i < input.VariationsPerIdea; i++)
            {
                var storyIdea = await GenerateStoryIdeaAsync(adaptedIdea, i, cancellationToken);
                generatedIdeas.Add(storyIdea);
            }

            processedCount++;
            int percentComplete = 10 + (int)((processedCount / (double)totalCount) * 80);
            ReportProgress(progress, percentComplete, $"Generated {processedCount * input.VariationsPerIdea} ideas");
        }

        ReportProgress(progress, 90, "LLM generation complete");

        return new LLMIdeaGenerationOutput
        {
            GeneratedIdeas = generatedIdeas
        };
    }

    private async Task<StoryIdea> GenerateStoryIdeaAsync(AdaptedIdea adaptedIdea, int variation, CancellationToken cancellationToken)
    {
        await Task.Delay(50, cancellationToken); // Simulate LLM call

        // In production, this would call an LLM API (OpenAI, etc.)
        // For now, create variations based on the adapted content

        var tones = new[] { "emotional, heartwarming", "dramatic, intense", "mysterious, suspenseful" };
        var narrators = new[] { "first-person", "third-person" };
        var timelines = new[] { "present day", "childhood memory", "recent past" };

        return new StoryIdea
        {
            StoryTitle = $"{GetTitleFromContent(adaptedIdea.Content)} - Variation {variation + 1}",
            Tone = tones[variation % tones.Length],
            Theme = string.Join(", ", adaptedIdea.Themes.Take(2)),
            NarratorType = narrators[variation % narrators.Length],
            Timeline = timelines[variation % timelines.Length],
            EmotionalCore = string.Join(", ", adaptedIdea.EmotionalHooks.Take(2)),
            TwistType = variation == 0 ? "unexpected revelation" : "emotional payoff"
        };
    }

    private string GetTitleFromContent(string content)
    {
        // Extract or generate a title from content
        var words = content.Split(' ', StringSplitOptions.RemoveEmptyEntries);
        var titleWords = words.Take(Math.Min(5, words.Length));
        return string.Join(" ", titleWords);
    }

    public override Task<bool> ValidateInputAsync(LLMIdeaGenerationInput input)
    {
        if (input == null)
            return Task.FromResult(false);

        if (input.AdaptedIdeas == null || input.AdaptedIdeas.Count == 0)
            return Task.FromResult(false);

        if (input.VariationsPerIdea < 1 || input.VariationsPerIdea > 10)
            return Task.FromResult(false);

        return Task.FromResult(true);
    }
}
