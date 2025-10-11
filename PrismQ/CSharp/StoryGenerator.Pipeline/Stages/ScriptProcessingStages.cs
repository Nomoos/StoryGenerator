using StoryGenerator.Pipeline.Core;
using StoryGenerator.Pipeline.Interfaces;
using StoryGenerator.Pipeline.Stages.Models;

namespace StoryGenerator.Pipeline.Stages;

/// <summary>
/// Stage 3: Script Scoring
/// Scores improved scripts on multiple quality dimensions.
/// </summary>
public class ScriptScoringStage : BasePipelineStage<ScriptScoringInput, ScriptScoringOutput>
{
    public override string StageName => "ScriptScoring";

    protected override async Task<ScriptScoringOutput> ExecuteCoreAsync(
        ScriptScoringInput input,
        IProgress<PipelineProgress>? progress,
        CancellationToken cancellationToken)
    {
        ReportProgress(progress, 10, "Starting script scoring...");

        var scoredScripts = new List<ScoredScript>();
        int processedCount = 0;
        int totalCount = input.Scripts.Count;

        foreach (var script in input.Scripts)
        {
            cancellationToken.ThrowIfCancellationRequested();

            var scored = ScoreScript(script);
            scoredScripts.Add(scored);

            processedCount++;
            int percentComplete = 10 + (int)((processedCount / (double)totalCount) * 80);
            ReportProgress(progress, percentComplete, $"Scored {processedCount}/{totalCount} scripts");
        }

        ReportProgress(progress, 90, "Script scoring complete");

        return new ScriptScoringOutput
        {
            ScoredScripts = scoredScripts
        };
    }

    private ScoredScript ScoreScript(ImprovedScript script)
    {
        // Calculate scores based on various metrics
        var wordCount = script.Content.Split(' ', StringSplitOptions.RemoveEmptyEntries).Length;
        var improvementCount = script.Improvements.Count;

        // Base scores with improvements factored in
        var clarity = Math.Min(100, 60 + (improvementCount * 8));
        var emotional = Math.Min(100, 55 + (improvementCount * 10));
        var narrative = Math.Min(100, 65 + (improvementCount * 7));

        // Adjust for word count (target is ~360)
        if (wordCount < 300 || wordCount > 420)
        {
            clarity -= 10;
            narrative -= 10;
        }

        var qualityScore = (clarity + emotional + narrative) / 3.0;

        return new ScoredScript
        {
            Script = script,
            QualityScore = qualityScore,
            EmotionalImpact = emotional,
            NarrativeFlow = narrative,
            Clarity = clarity
        };
    }

    public override Task<bool> ValidateInputAsync(ScriptScoringInput input)
    {
        if (input == null)
            return Task.FromResult(false);

        if (input.Scripts == null || input.Scripts.Count == 0)
            return Task.FromResult(false);

        return Task.FromResult(true);
    }
}

/// <summary>
/// Stage 4: Script Selection
/// Selects the best script(s) based on scoring.
/// </summary>
public class ScriptSelectionStage : BasePipelineStage<ScriptSelectionInput, ScriptSelectionOutput>
{
    public override string StageName => "ScriptSelection";

    protected override async Task<ScriptSelectionOutput> ExecuteCoreAsync(
        ScriptSelectionInput input,
        IProgress<PipelineProgress>? progress,
        CancellationToken cancellationToken)
    {
        ReportProgress(progress, 10, "Starting script selection...");

        await Task.Delay(50, cancellationToken);

        var selectedScripts = input.ScoredScripts
            .OrderByDescending(s => s.QualityScore)
            .Take(input.SelectCount)
            .Select(s => s.Script)
            .ToList();

        ReportProgress(progress, 90, $"Selected {selectedScripts.Count} best scripts");

        return new ScriptSelectionOutput
        {
            SelectedScripts = selectedScripts
        };
    }

    public override Task<bool> ValidateInputAsync(ScriptSelectionInput input)
    {
        if (input == null)
            return Task.FromResult(false);

        if (input.ScoredScripts == null || input.ScoredScripts.Count == 0)
            return Task.FromResult(false);

        if (input.SelectCount < 1)
            return Task.FromResult(false);

        return Task.FromResult(true);
    }
}

/// <summary>
/// Stage 5: Script Revision
/// Revises selected scripts for voice clarity and pronunciation.
/// </summary>
public class ScriptRevisionStage : BasePipelineStage<ScriptRevisionInput, ScriptRevisionOutput>
{
    public override string StageName => "ScriptRevision";

    protected override async Task<ScriptRevisionOutput> ExecuteCoreAsync(
        ScriptRevisionInput input,
        IProgress<PipelineProgress>? progress,
        CancellationToken cancellationToken)
    {
        ReportProgress(progress, 10, "Starting script revision...");

        var revisedScripts = new List<RevisedScript>();
        int processedCount = 0;
        int totalCount = input.Scripts.Count;

        foreach (var script in input.Scripts)
        {
            cancellationToken.ThrowIfCancellationRequested();

            var revised = await ReviseScriptAsync(script, cancellationToken);
            revisedScripts.Add(revised);

            processedCount++;
            int percentComplete = 10 + (int)((processedCount / (double)totalCount) * 80);
            ReportProgress(progress, percentComplete, $"Revised {processedCount}/{totalCount} scripts");
        }

        ReportProgress(progress, 90, "Script revision complete");

        return new ScriptRevisionOutput
        {
            RevisedScripts = revisedScripts
        };
    }

    private async Task<RevisedScript> ReviseScriptAsync(ImprovedScript script, CancellationToken cancellationToken)
    {
        await Task.Delay(100, cancellationToken); // Simulate LLM call

        // Simulate voice clarity revisions
        var revisions = new List<string>
        {
            "Simplified complex sentences for voice clarity",
            "Adjusted punctuation for natural speaking pauses",
            "Replaced difficult pronunciations",
            "Optimized rhythm and pacing for narration"
        };

        // Simulate revised content
        var revisedContent = script.Content.Replace("[Version", "[Revised Version");
        revisedContent += "\n\n[Optimized for voice synthesis]";

        return new RevisedScript
        {
            SourceScript = script,
            Content = revisedContent,
            Revisions = revisions
        };
    }

    public override Task<bool> ValidateInputAsync(ScriptRevisionInput input)
    {
        if (input == null)
            return Task.FromResult(false);

        if (input.Scripts == null || input.Scripts.Count == 0)
            return Task.FromResult(false);

        return Task.FromResult(true);
    }
}

/// <summary>
/// Stage 6: Script Enhancement
/// Enhances revised scripts with ElevenLabs voice tags for emotion and pacing.
/// </summary>
public class ScriptEnhancementStage : BasePipelineStage<ScriptEnhancementInput, ScriptEnhancementOutput>
{
    public override string StageName => "ScriptEnhancement";

    protected override async Task<ScriptEnhancementOutput> ExecuteCoreAsync(
        ScriptEnhancementInput input,
        IProgress<PipelineProgress>? progress,
        CancellationToken cancellationToken)
    {
        ReportProgress(progress, 10, "Starting script enhancement...");

        var enhancedScripts = new List<EnhancedScript>();
        int processedCount = 0;
        int totalCount = input.Scripts.Count;

        foreach (var script in input.Scripts)
        {
            cancellationToken.ThrowIfCancellationRequested();

            var enhanced = await EnhanceScriptAsync(script, cancellationToken);
            enhancedScripts.Add(enhanced);

            processedCount++;
            int percentComplete = 10 + (int)((processedCount / (double)totalCount) * 80);
            ReportProgress(progress, percentComplete, $"Enhanced {processedCount}/{totalCount} scripts");
        }

        ReportProgress(progress, 90, "Script enhancement complete");

        return new ScriptEnhancementOutput
        {
            EnhancedScripts = enhancedScripts
        };
    }

    private async Task<EnhancedScript> EnhanceScriptAsync(RevisedScript script, CancellationToken cancellationToken)
    {
        await Task.Delay(80, cancellationToken); // Simulate processing

        // Add ElevenLabs voice tags
        var enhancements = new List<string>
        {
            "Added emotional emphasis tags",
            "Inserted strategic pauses",
            "Applied voice modulation markers",
            "Enhanced dramatic moments"
        };

        // Simulate enhanced content with voice tags
        var enhancedContent = script.Content;
        enhancedContent = enhancedContent.Replace("never expected", "<emphasis level=\"strong\">never expected</emphasis>");
        enhancedContent = enhancedContent.Replace("[Scene", "<break time=\"1s\"/>[Scene");
        enhancedContent += "\n\n[Enhanced with ElevenLabs voice tags]";

        return new EnhancedScript
        {
            SourceScript = script,
            Content = enhancedContent,
            Enhancements = enhancements
        };
    }

    public override Task<bool> ValidateInputAsync(ScriptEnhancementInput input)
    {
        if (input == null)
            return Task.FromResult(false);

        if (input.Scripts == null || input.Scripts.Count == 0)
            return Task.FromResult(false);

        return Task.FromResult(true);
    }
}
