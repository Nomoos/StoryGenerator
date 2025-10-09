using StoryGenerator.Pipeline.Core;
using StoryGenerator.Pipeline.Interfaces;
using StoryGenerator.Pipeline.Stages.Models;

namespace StoryGenerator.Pipeline.Stages;

/// <summary>
/// Stage 1: Reddit Adaptation
/// Adapts collected Reddit ideas into story seeds ready for LLM generation.
/// </summary>
public class RedditAdaptationStage : BasePipelineStage<RedditAdaptationInput, RedditAdaptationOutput>
{
    public override string StageName => "RedditAdaptation";

    protected override async Task<RedditAdaptationOutput> ExecuteCoreAsync(
        RedditAdaptationInput input,
        IProgress<PipelineProgress>? progress,
        CancellationToken cancellationToken)
    {
        ReportProgress(progress, 10, "Starting Reddit adaptation...");

        var adaptedIdeas = new List<AdaptedIdea>();
        int processedCount = 0;
        int totalCount = input.CollectedIdeas.Count;

        foreach (var collectedIdea in input.CollectedIdeas)
        {
            cancellationToken.ThrowIfCancellationRequested();

            var adapted = await AdaptIdeaAsync(collectedIdea, cancellationToken);
            adaptedIdeas.Add(adapted);

            processedCount++;
            int percentComplete = 10 + (int)((processedCount / (double)totalCount) * 80);
            ReportProgress(progress, percentComplete, $"Adapted {processedCount}/{totalCount} ideas");
        }

        ReportProgress(progress, 90, "Adaptation complete");

        return new RedditAdaptationOutput
        {
            AdaptedIdeas = adaptedIdeas
        };
    }

    private async Task<AdaptedIdea> AdaptIdeaAsync(StoryGenerator.Core.Models.CollectedIdea collectedIdea, CancellationToken cancellationToken)
    {
        await Task.Delay(10, cancellationToken); // Simulate processing

        var adapted = new AdaptedIdea
        {
            SourceIdea = collectedIdea,
            Content = AdaptContent(collectedIdea.IdeaContent),
            Themes = ExtractThemes(collectedIdea.IdeaContent),
            EmotionalHooks = ExtractEmotionalHooks(collectedIdea.IdeaContent)
        };

        return adapted;
    }

    private string AdaptContent(string content)
    {
        // Transform the content into a story-friendly format
        // Remove Reddit-specific formatting, extract core narrative
        var adapted = content.Trim();
        
        // Remove common Reddit patterns
        adapted = System.Text.RegularExpressions.Regex.Replace(adapted, @"TL;?DR:.*", "", System.Text.RegularExpressions.RegexOptions.IgnoreCase);
        adapted = System.Text.RegularExpressions.Regex.Replace(adapted, @"Edit:.*", "", System.Text.RegularExpressions.RegexOptions.IgnoreCase);
        adapted = adapted.Replace("[removed]", "").Replace("[deleted]", "");
        
        return adapted.Trim();
    }

    private List<string> ExtractThemes(string content)
    {
        var themes = new List<string>();
        var lowerContent = content.ToLowerInvariant();

        // Simple keyword-based theme extraction
        if (lowerContent.Contains("friend") || lowerContent.Contains("friendship"))
            themes.Add("friendship");
        if (lowerContent.Contains("love") || lowerContent.Contains("romance"))
            themes.Add("romance");
        if (lowerContent.Contains("family") || lowerContent.Contains("parent"))
            themes.Add("family");
        if (lowerContent.Contains("betray") || lowerContent.Contains("trust"))
            themes.Add("betrayal");
        if (lowerContent.Contains("overcome") || lowerContent.Contains("struggle"))
            themes.Add("perseverance");
        if (lowerContent.Contains("loss") || lowerContent.Contains("grief"))
            themes.Add("loss");
        if (lowerContent.Contains("surprise") || lowerContent.Contains("unexpected"))
            themes.Add("unexpected");

        return themes.Distinct().ToList();
    }

    private List<string> ExtractEmotionalHooks(string content)
    {
        var hooks = new List<string>();
        var lowerContent = content.ToLowerInvariant();

        // Identify emotional elements
        if (lowerContent.Contains("happy") || lowerContent.Contains("joy"))
            hooks.Add("joy");
        if (lowerContent.Contains("sad") || lowerContent.Contains("cry"))
            hooks.Add("sadness");
        if (lowerContent.Contains("angry") || lowerContent.Contains("mad"))
            hooks.Add("anger");
        if (lowerContent.Contains("surprise") || lowerContent.Contains("shock"))
            hooks.Add("surprise");
        if (lowerContent.Contains("scare") || lowerContent.Contains("fear"))
            hooks.Add("fear");
        if (lowerContent.Contains("disgust") || lowerContent.Contains("gross"))
            hooks.Add("disgust");

        return hooks.Distinct().ToList();
    }

    public override Task<bool> ValidateInputAsync(RedditAdaptationInput input)
    {
        if (input == null)
            return Task.FromResult(false);

        if (input.CollectedIdeas == null || input.CollectedIdeas.Count == 0)
            return Task.FromResult(false);

        return Task.FromResult(true);
    }
}
