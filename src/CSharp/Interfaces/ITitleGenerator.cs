using System.Collections.Generic;
using System.Threading;
using System.Threading.Tasks;
using StoryGenerator.Models;

namespace StoryGenerator.Core.Interfaces
{
    /// <summary>
    /// Interface for generating clickable, viral-optimized titles from topic clusters.
    /// Converts topics to ≥10 clickable titles per segment and saves them in JSON format.
    /// </summary>
    /// <remarks>
    /// Titles are saved to /titles/{segment}/{age}/YYYYMMDD_titles.json.
    /// Uses LLM models or title optimization techniques for generating viral-ready titles.
    /// </remarks>
    public interface ITitleGenerator : IGenerator
    {
        /// <summary>
        /// Generates clickable titles from topic clusters for a specific audience segment.
        /// </summary>
        /// <param name="topics">The topic cluster collection to generate titles from.</param>
        /// <param name="segment">The target audience segment.</param>
        /// <param name="minTitles">Minimum number of titles to generate (default: 10).</param>
        /// <param name="cancellationToken">Cancellation token.</param>
        /// <returns>A collection of clickable titles.</returns>
        Task<ClickableTitleCollection> GenerateTitlesFromTopicsAsync(
            TopicClusterCollection topics,
            AudienceSegment segment,
            int minTitles = 10,
            CancellationToken cancellationToken = default);

        /// <summary>
        /// Generates titles from a single topic cluster.
        /// </summary>
        /// <param name="topic">The topic cluster to generate titles from.</param>
        /// <param name="segment">The target audience segment.</param>
        /// <param name="titlesPerTopic">Number of titles to generate per topic (default: 2).</param>
        /// <param name="cancellationToken">Cancellation token.</param>
        /// <returns>A list of clickable titles.</returns>
        Task<List<ClickableTitle>> GenerateTitlesFromTopicAsync(
            TopicCluster topic,
            AudienceSegment segment,
            int titlesPerTopic = 2,
            CancellationToken cancellationToken = default);

        /// <summary>
        /// Generates titles and saves them to a JSON file.
        /// </summary>
        /// <param name="topics">The topic cluster collection to generate titles from.</param>
        /// <param name="segment">The target audience segment.</param>
        /// <param name="outputDirectory">Base directory for saving titles (e.g., "/titles").</param>
        /// <param name="minTitles">Minimum number of titles to generate (default: 10).</param>
        /// <param name="cancellationToken">Cancellation token.</param>
        /// <returns>Path to the saved JSON file.</returns>
        /// <remarks>
        /// Output path format: {outputDirectory}/{segment.Gender}/{segment.Age}/YYYYMMDD_titles.json
        /// </remarks>
        Task<string> GenerateAndSaveTitlesAsync(
            TopicClusterCollection topics,
            AudienceSegment segment,
            string outputDirectory,
            int minTitles = 10,
            CancellationToken cancellationToken = default);

        /// <summary>
        /// Loads topics from a JSON file and generates clickable titles.
        /// </summary>
        /// <param name="topicsFilePath">Path to the JSON file containing topics.</param>
        /// <param name="segment">The target audience segment.</param>
        /// <param name="outputDirectory">Base directory for saving titles.</param>
        /// <param name="minTitles">Minimum number of titles to generate (default: 10).</param>
        /// <param name="cancellationToken">Cancellation token.</param>
        /// <returns>Path to the saved JSON file with titles.</returns>
        Task<string> LoadTopicsAndGenerateTitlesAsync(
            string topicsFilePath,
            AudienceSegment segment,
            string outputDirectory,
            int minTitles = 10,
            CancellationToken cancellationToken = default);

        /// <summary>
        /// Processes all topic files in a directory and generates titles for each segment.
        /// </summary>
        /// <param name="topicsDirectory">Base directory containing topic files.</param>
        /// <param name="outputDirectory">Base directory for saving titles.</param>
        /// <param name="minTitles">Minimum number of titles per segment (default: 10).</param>
        /// <param name="cancellationToken">Cancellation token.</param>
        /// <returns>Dictionary mapping segments to their generated titles file paths.</returns>
        Task<Dictionary<AudienceSegment, string>> GenerateTitlesForAllSegmentsAsync(
            string topicsDirectory,
            string outputDirectory,
            int minTitles = 10,
            CancellationToken cancellationToken = default);

        /// <summary>
        /// Optimizes a title for clickability and viral potential.
        /// </summary>
        /// <param name="title">The title to optimize.</param>
        /// <param name="segment">The target audience segment.</param>
        /// <param name="cancellationToken">Cancellation token.</param>
        /// <returns>An optimized clickable title.</returns>
        Task<ClickableTitle> OptimizeTitleAsync(
            string title,
            AudienceSegment segment,
            CancellationToken cancellationToken = default);

        /// <summary>
        /// Validates that a title meets clickability criteria.
        /// </summary>
        /// <param name="title">The title to validate.</param>
        /// <returns>True if the title meets clickability criteria; otherwise, false.</returns>
        bool ValidateTitleClickability(string title);
    }
}
