using PrismQ.Shared.Models;

namespace StoryGenerator.Pipeline.Stages.Models;

/// <summary>
/// Input for Reddit Adaptation Stage
/// </summary>
public class RedditAdaptationInput
{
    /// <summary>
    /// Reddit posts or ideas to adapt
    /// </summary>
    public List<CollectedIdea> CollectedIdeas { get; set; } = new();
}

/// <summary>
/// Output from Reddit Adaptation Stage
/// </summary>
public class RedditAdaptationOutput
{
    /// <summary>
    /// Adapted ideas ready for LLM generation
    /// </summary>
    public List<AdaptedIdea> AdaptedIdeas { get; set; } = new();
}

/// <summary>
/// Represents an idea adapted from source material
/// </summary>
public class AdaptedIdea
{
    /// <summary>
    /// Unique identifier
    /// </summary>
    public string Id { get; set; } = Guid.NewGuid().ToString();

    /// <summary>
    /// Source idea that was adapted
    /// </summary>
    public CollectedIdea? SourceIdea { get; set; }

    /// <summary>
    /// Adapted content
    /// </summary>
    public string Content { get; set; } = string.Empty;

    /// <summary>
    /// Key themes extracted
    /// </summary>
    public List<string> Themes { get; set; } = new();

    /// <summary>
    /// Emotional hooks identified
    /// </summary>
    public List<string> EmotionalHooks { get; set; } = new();

    /// <summary>
    /// Timestamp of adaptation
    /// </summary>
    public DateTime AdaptedAt { get; set; } = DateTime.UtcNow;
}

/// <summary>
/// Input for LLM Idea Generation Stage
/// </summary>
public class LLMIdeaGenerationInput
{
    /// <summary>
    /// Adapted ideas to expand
    /// </summary>
    public List<AdaptedIdea> AdaptedIdeas { get; set; } = new();

    /// <summary>
    /// Number of variations per idea
    /// </summary>
    public int VariationsPerIdea { get; set; } = 3;
}

/// <summary>
/// Output from LLM Idea Generation Stage
/// </summary>
public class LLMIdeaGenerationOutput
{
    /// <summary>
    /// Generated story ideas
    /// </summary>
    public List<StoryIdea> GeneratedIdeas { get; set; } = new();
}

/// <summary>
/// Input for Idea Clustering Stage
/// </summary>
public class IdeaClusteringInput
{
    /// <summary>
    /// Ideas to cluster
    /// </summary>
    public List<StoryIdea> Ideas { get; set; } = new();
}

/// <summary>
/// Output from Idea Clustering Stage
/// </summary>
public class IdeaClusteringOutput
{
    /// <summary>
    /// Clustered ideas
    /// </summary>
    public List<IdeaCluster> Clusters { get; set; } = new();
}

/// <summary>
/// Represents a cluster of similar ideas
/// </summary>
public class IdeaCluster
{
    /// <summary>
    /// Cluster identifier
    /// </summary>
    public string Id { get; set; } = Guid.NewGuid().ToString();

    /// <summary>
    /// Name/theme of the cluster
    /// </summary>
    public string Name { get; set; } = string.Empty;

    /// <summary>
    /// Ideas in this cluster
    /// </summary>
    public List<StoryIdea> Ideas { get; set; } = new();

    /// <summary>
    /// Average viral potential of cluster
    /// </summary>
    public double AverageViralScore { get; set; }
}

/// <summary>
/// Input for Idea Ranking Stage
/// </summary>
public class IdeaRankingInput
{
    /// <summary>
    /// Clusters to rank
    /// </summary>
    public List<IdeaCluster> Clusters { get; set; } = new();
}

/// <summary>
/// Output from Idea Ranking Stage
/// </summary>
public class IdeaRankingOutput
{
    /// <summary>
    /// Ranked ideas
    /// </summary>
    public List<RankedIdea> RankedIdeas { get; set; } = new();
}

/// <summary>
/// Represents an idea with ranking information
/// </summary>
public class RankedIdea
{
    /// <summary>
    /// The story idea
    /// </summary>
    public StoryIdea Idea { get; set; } = new();

    /// <summary>
    /// Rank (1 is best)
    /// </summary>
    public int Rank { get; set; }

    /// <summary>
    /// Overall score
    /// </summary>
    public double Score { get; set; }

    /// <summary>
    /// Cluster this idea belongs to
    /// </summary>
    public string ClusterId { get; set; } = string.Empty;
}

/// <summary>
/// Input for Idea Selection Stage
/// </summary>
public class IdeaSelectionInput
{
    /// <summary>
    /// Ranked ideas to select from
    /// </summary>
    public List<RankedIdea> RankedIdeas { get; set; } = new();

    /// <summary>
    /// Number of ideas to select
    /// </summary>
    public int SelectCount { get; set; } = 5;
}

/// <summary>
/// Output from Idea Selection Stage
/// </summary>
public class IdeaSelectionOutput
{
    /// <summary>
    /// Selected ideas
    /// </summary>
    public List<StoryIdea> SelectedIdeas { get; set; } = new();
}

/// <summary>
/// Input for Idea Validation Stage
/// </summary>
public class IdeaValidationInput
{
    /// <summary>
    /// Ideas to validate
    /// </summary>
    public List<StoryIdea> Ideas { get; set; } = new();
}

/// <summary>
/// Output from Idea Validation Stage
/// </summary>
public class IdeaValidationOutput
{
    /// <summary>
    /// Validated ideas
    /// </summary>
    public List<ValidatedIdea> ValidatedIdeas { get; set; } = new();
}

/// <summary>
/// Represents a validated idea
/// </summary>
public class ValidatedIdea
{
    /// <summary>
    /// The story idea
    /// </summary>
    public StoryIdea Idea { get; set; } = new();

    /// <summary>
    /// Whether the idea is valid
    /// </summary>
    public bool IsValid { get; set; }

    /// <summary>
    /// Validation messages
    /// </summary>
    public List<string> ValidationMessages { get; set; } = new();
}

/// <summary>
/// Input for Idea Registry Update Stage
/// </summary>
public class IdeaRegistryUpdateInput
{
    /// <summary>
    /// Validated ideas to register
    /// </summary>
    public List<ValidatedIdea> ValidatedIdeas { get; set; } = new();
}

/// <summary>
/// Output from Idea Registry Update Stage
/// </summary>
public class IdeaRegistryUpdateOutput
{
    /// <summary>
    /// Number of ideas registered
    /// </summary>
    public int RegisteredCount { get; set; }

    /// <summary>
    /// Registry file path
    /// </summary>
    public string RegistryPath { get; set; } = string.Empty;
}
