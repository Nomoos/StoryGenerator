using System.Collections.Generic;
using System.Threading;
using System.Threading.Tasks;
using StoryGenerator.Models;

namespace StoryGenerator.Core.Interfaces
{
    /// <summary>
    /// Interface for clustering raw ideas into topic groups for specific audience segments.
    /// Clusters ideas into ≥8 topics per segment and saves them in JSON format.
    /// </summary>
    /// <remarks>
    /// Topics are saved to /topics/{segment}/{age}/YYYYMMDD_topics.json.
    /// Uses clustering algorithms or LLM models for topic extraction and grouping.
    /// </remarks>
    public interface ITopicGenerator : IGenerator
    {
        /// <summary>
        /// Clusters raw ideas into topic groups for a specific audience segment.
        /// </summary>
        /// <param name="ideas">The list of raw ideas to cluster.</param>
        /// <param name="segment">The target audience segment.</param>
        /// <param name="minTopics">Minimum number of topic clusters to generate (default: 8).</param>
        /// <param name="cancellationToken">Cancellation token.</param>
        /// <returns>A collection of topic clusters.</returns>
        Task<TopicClusterCollection> ClusterIdeasIntoTopicsAsync(
            List<RawIdea> ideas,
            AudienceSegment segment,
            int minTopics = 8,
            CancellationToken cancellationToken = default);

        /// <summary>
        /// Clusters ideas and saves the topics to a JSON file.
        /// </summary>
        /// <param name="ideas">The list of raw ideas to cluster.</param>
        /// <param name="segment">The target audience segment.</param>
        /// <param name="outputDirectory">Base directory for saving topics (e.g., "/topics").</param>
        /// <param name="minTopics">Minimum number of topic clusters to generate (default: 8).</param>
        /// <param name="cancellationToken">Cancellation token.</param>
        /// <returns>Path to the saved JSON file.</returns>
        /// <remarks>
        /// Output path format: {outputDirectory}/{segment.Gender}/{segment.Age}/YYYYMMDD_topics.json
        /// </remarks>
        Task<string> ClusterAndSaveTopicsAsync(
            List<RawIdea> ideas,
            AudienceSegment segment,
            string outputDirectory,
            int minTopics = 8,
            CancellationToken cancellationToken = default);

        /// <summary>
        /// Loads raw ideas from a markdown file and clusters them into topics.
        /// </summary>
        /// <param name="ideasFilePath">Path to the markdown file containing ideas.</param>
        /// <param name="segment">The target audience segment.</param>
        /// <param name="outputDirectory">Base directory for saving topics.</param>
        /// <param name="minTopics">Minimum number of topic clusters to generate (default: 8).</param>
        /// <param name="cancellationToken">Cancellation token.</param>
        /// <returns>Path to the saved JSON file with topics.</returns>
        Task<string> LoadIdeasAndGenerateTopicsAsync(
            string ideasFilePath,
            AudienceSegment segment,
            string outputDirectory,
            int minTopics = 8,
            CancellationToken cancellationToken = default);

        /// <summary>
        /// Processes all idea files in a directory and generates topics for each segment.
        /// </summary>
        /// <param name="ideasDirectory">Base directory containing idea files.</param>
        /// <param name="outputDirectory">Base directory for saving topics.</param>
        /// <param name="minTopics">Minimum number of topic clusters per segment (default: 8).</param>
        /// <param name="cancellationToken">Cancellation token.</param>
        /// <returns>Dictionary mapping segments to their generated topics file paths.</returns>
        Task<Dictionary<AudienceSegment, string>> GenerateTopicsForAllSegmentsAsync(
            string ideasDirectory,
            string outputDirectory,
            int minTopics = 8,
            CancellationToken cancellationToken = default);

        /// <summary>
        /// Parses raw ideas from a markdown file.
        /// </summary>
        /// <param name="markdownFilePath">Path to the markdown file.</param>
        /// <param name="segment">The target audience segment.</param>
        /// <param name="cancellationToken">Cancellation token.</param>
        /// <returns>List of raw ideas parsed from the file.</returns>
        Task<List<RawIdea>> ParseIdeasFromMarkdownAsync(
            string markdownFilePath,
            AudienceSegment segment,
            CancellationToken cancellationToken = default);
    }
}
