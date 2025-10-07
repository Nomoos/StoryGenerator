using System.Collections.Generic;
using System.Threading;
using System.Threading.Tasks;
using StoryGenerator.Models;

namespace StoryGenerator.Core.Interfaces
{
    /// <summary>
    /// Interface for generating raw story ideas for specific audience segments.
    /// Generates ≥20 raw ideas per segment and saves them in markdown format.
    /// </summary>
    /// <remarks>
    /// Ideas are saved to /ideas/{segment}/{age}/YYYYMMDD_ideas.md as a markdown list.
    /// Uses LLM models (GPT-4o-mini, Qwen2.5-14B-Instruct, or similar) for generation.
    /// </remarks>
    public interface IIdeaGenerator : IGenerator
    {
        /// <summary>
        /// Generates raw story ideas for a specific audience segment.
        /// </summary>
        /// <param name="segment">The target audience segment (gender and age range).</param>
        /// <param name="minIdeas">Minimum number of ideas to generate (default: 20).</param>
        /// <param name="cancellationToken">Cancellation token.</param>
        /// <returns>A list of generated raw ideas.</returns>
        Task<List<RawIdea>> GenerateIdeasAsync(
            AudienceSegment segment, 
            int minIdeas = 20, 
            CancellationToken cancellationToken = default);

        /// <summary>
        /// Generates ideas and saves them to a markdown file.
        /// </summary>
        /// <param name="segment">The target audience segment.</param>
        /// <param name="outputDirectory">Base directory for saving ideas (e.g., "/ideas").</param>
        /// <param name="minIdeas">Minimum number of ideas to generate (default: 20).</param>
        /// <param name="cancellationToken">Cancellation token.</param>
        /// <returns>Path to the saved markdown file.</returns>
        /// <remarks>
        /// Output path format: {outputDirectory}/{segment.Gender}/{segment.Age}/YYYYMMDD_ideas.md
        /// </remarks>
        Task<string> GenerateAndSaveIdeasAsync(
            AudienceSegment segment,
            string outputDirectory,
            int minIdeas = 20,
            CancellationToken cancellationToken = default);

        /// <summary>
        /// Generates ideas for all predefined audience segments.
        /// </summary>
        /// <param name="outputDirectory">Base directory for saving ideas.</param>
        /// <param name="minIdeas">Minimum number of ideas per segment (default: 20).</param>
        /// <param name="cancellationToken">Cancellation token.</param>
        /// <returns>Dictionary mapping segments to their generated ideas file paths.</returns>
        Task<Dictionary<AudienceSegment, string>> GenerateIdeasForAllSegmentsAsync(
            string outputDirectory,
            int minIdeas = 20,
            CancellationToken cancellationToken = default);

        /// <summary>
        /// Formats ideas as a markdown list.
        /// </summary>
        /// <param name="ideas">The list of raw ideas to format.</param>
        /// <returns>Markdown-formatted string.</returns>
        string FormatIdeasAsMarkdown(List<RawIdea> ideas);

        /// <summary>
        /// Gets the list of predefined audience segments.
        /// </summary>
        /// <returns>List of standard audience segments (women/men × 10-13, 14-17, 18-23, 24-30).</returns>
        List<AudienceSegment> GetPredefinedSegments();
    }
}
