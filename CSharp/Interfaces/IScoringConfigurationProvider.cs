using System.Threading;
using System.Threading.Tasks;

namespace StoryGenerator.Interfaces
{
    /// <summary>
    /// Interface for loading and managing scoring configuration.
    /// Provides access to scoring rubrics, criteria weights, and guidelines.
    /// </summary>
    public interface IScoringConfigurationProvider
    {
        /// <summary>
        /// Load the scoring configuration from file or storage.
        /// </summary>
        /// <param name="cancellationToken">Cancellation token</param>
        /// <returns>Scoring configuration</returns>
        Task<ScoringConfiguration> LoadConfigurationAsync(CancellationToken cancellationToken = default);

        /// <summary>
        /// Get the scoring criteria with their weights.
        /// </summary>
        /// <returns>Collection of scoring criteria</returns>
        IEnumerable<ScoringCriterion> GetScoringCriteria();

        /// <summary>
        /// Get voice recommendation guidelines.
        /// </summary>
        /// <returns>Voice recommendation guidelines</returns>
        VoiceRecommendationGuidelines GetVoiceGuidelines();

        /// <summary>
        /// Get the number of top titles to select per segment.
        /// </summary>
        /// <returns>Count of top titles to select</returns>
        int GetTopTitleCount();

        /// <summary>
        /// Validate the configuration for completeness and correctness.
        /// </summary>
        /// <returns>True if configuration is valid, false otherwise</returns>
        bool ValidateConfiguration();
    }
}
