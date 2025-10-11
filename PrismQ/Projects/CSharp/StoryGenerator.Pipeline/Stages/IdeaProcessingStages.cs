using PrismQ.Shared.Models;
using StoryGenerator.Pipeline.Core;
using StoryGenerator.Pipeline.Interfaces;
using StoryGenerator.Pipeline.Stages.Models;

namespace StoryGenerator.Pipeline.Stages;

/// <summary>
/// Stage 3: Idea Clustering
/// Groups similar ideas together based on themes and content.
/// </summary>
public class IdeaClusteringStage : BasePipelineStage<IdeaClusteringInput, IdeaClusteringOutput>
{
    public override string StageName => "IdeaClustering";

    protected override async Task<IdeaClusteringOutput> ExecuteCoreAsync(
        IdeaClusteringInput input,
        IProgress<PipelineProgress>? progress,
        CancellationToken cancellationToken)
    {
        ReportProgress(progress, 10, "Starting idea clustering...");

        await Task.Delay(100, cancellationToken); // Simulate processing

        // Simple clustering based on themes
        var clusters = new Dictionary<string, IdeaCluster>();

        foreach (var idea in input.Ideas)
        {
            cancellationToken.ThrowIfCancellationRequested();

            var themeKey = idea.Theme ?? "general";
            
            if (!clusters.ContainsKey(themeKey))
            {
                clusters[themeKey] = new IdeaCluster
                {
                    Name = themeKey,
                    Ideas = new List<StoryIdea>()
                };
            }

            clusters[themeKey].Ideas.Add(idea);
        }

        // Calculate average viral scores
        foreach (var cluster in clusters.Values)
        {
            cluster.AverageViralScore = cluster.Ideas
                .Average(i => i.Potential?.Overall ?? 50) / 100.0;
        }

        ReportProgress(progress, 90, $"Created {clusters.Count} clusters");

        return new IdeaClusteringOutput
        {
            Clusters = clusters.Values.ToList()
        };
    }

    public override Task<bool> ValidateInputAsync(IdeaClusteringInput input)
    {
        if (input == null)
            return Task.FromResult(false);

        if (input.Ideas == null || input.Ideas.Count == 0)
            return Task.FromResult(false);

        return Task.FromResult(true);
    }
}

/// <summary>
/// Stage 4: Idea Ranking
/// Ranks ideas within clusters based on viral potential and quality.
/// </summary>
public class IdeaRankingStage : BasePipelineStage<IdeaRankingInput, IdeaRankingOutput>
{
    public override string StageName => "IdeaRanking";

    protected override async Task<IdeaRankingOutput> ExecuteCoreAsync(
        IdeaRankingInput input,
        IProgress<PipelineProgress>? progress,
        CancellationToken cancellationToken)
    {
        ReportProgress(progress, 10, "Starting idea ranking...");

        await Task.Delay(100, cancellationToken); // Simulate processing

        var rankedIdeas = new List<RankedIdea>();
        int currentRank = 1;

        // Rank ideas across all clusters
        var allIdeas = input.Clusters
            .SelectMany(c => c.Ideas.Select(i => (Idea: i, ClusterId: c.Id)))
            .OrderByDescending(item => item.Idea.Potential?.Overall ?? 50)
            .ThenBy(item => item.Idea.StoryTitle);

        foreach (var item in allIdeas)
        {
            cancellationToken.ThrowIfCancellationRequested();

            rankedIdeas.Add(new RankedIdea
            {
                Idea = item.Idea,
                Rank = currentRank++,
                Score = (item.Idea.Potential?.Overall ?? 50) / 100.0,
                ClusterId = item.ClusterId
            });
        }

        ReportProgress(progress, 90, $"Ranked {rankedIdeas.Count} ideas");

        return new IdeaRankingOutput
        {
            RankedIdeas = rankedIdeas
        };
    }

    public override Task<bool> ValidateInputAsync(IdeaRankingInput input)
    {
        if (input == null)
            return Task.FromResult(false);

        if (input.Clusters == null || input.Clusters.Count == 0)
            return Task.FromResult(false);

        return Task.FromResult(true);
    }
}

/// <summary>
/// Stage 5: Idea Selection
/// Selects the top N ideas based on ranking.
/// </summary>
public class IdeaSelectionStage : BasePipelineStage<IdeaSelectionInput, IdeaSelectionOutput>
{
    public override string StageName => "IdeaSelection";

    protected override async Task<IdeaSelectionOutput> ExecuteCoreAsync(
        IdeaSelectionInput input,
        IProgress<PipelineProgress>? progress,
        CancellationToken cancellationToken)
    {
        ReportProgress(progress, 10, "Starting idea selection...");

        await Task.Delay(50, cancellationToken); // Simulate processing

        var selectedIdeas = input.RankedIdeas
            .OrderBy(r => r.Rank)
            .Take(input.SelectCount)
            .Select(r => r.Idea)
            .ToList();

        ReportProgress(progress, 90, $"Selected {selectedIdeas.Count} ideas");

        return new IdeaSelectionOutput
        {
            SelectedIdeas = selectedIdeas
        };
    }

    public override Task<bool> ValidateInputAsync(IdeaSelectionInput input)
    {
        if (input == null)
            return Task.FromResult(false);

        if (input.RankedIdeas == null || input.RankedIdeas.Count == 0)
            return Task.FromResult(false);

        if (input.SelectCount < 1)
            return Task.FromResult(false);

        return Task.FromResult(true);
    }
}
