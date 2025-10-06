using System.Threading;
using System.Threading.Tasks;

namespace StoryGenerator.Interfaces
{
    /// <summary>
    /// Interface for saving title scoring results to various output formats.
    /// Supports JSON scores and Markdown voice notes.
    /// </summary>
    public interface IScoreOutputWriter
    {
        /// <summary>
        /// Save scoring results to JSON format.
        /// </summary>
        /// <param name="segment">Audience segment</param>
        /// <param name="results">Collection of scoring results</param>
        /// <param name="outputPath">Output directory path</param>
        /// <param name="cancellationToken">Cancellation token</param>
        /// <returns>Path to the created file</returns>
        Task<string> SaveScoresAsJsonAsync(
            AudienceSegment segment,
            IEnumerable<TitleScoringResult> results,
            string outputPath,
            CancellationToken cancellationToken = default);

        /// <summary>
        /// Save top titles as Markdown voice notes.
        /// </summary>
        /// <param name="segment">Audience segment</param>
        /// <param name="topTitles">Top scoring titles</param>
        /// <param name="outputPath">Output directory path</param>
        /// <param name="cancellationToken">Cancellation token</param>
        /// <returns>Path to the created file</returns>
        Task<string> SaveVoiceNotesAsMarkdownAsync(
            AudienceSegment segment,
            IEnumerable<TitleScoringResult> topTitles,
            string outputPath,
            CancellationToken cancellationToken = default);

        /// <summary>
        /// Generate the filename for score output files.
        /// </summary>
        /// <param name="segment">Audience segment</param>
        /// <param name="fileType">File type (json, md)</param>
        /// <returns>Generated filename</returns>
        string GenerateFileName(AudienceSegment segment, string fileType);

        /// <summary>
        /// Ensure output directory exists, creating it if necessary.
        /// </summary>
        /// <param name="basePath">Base output path</param>
        /// <param name="segment">Audience segment</param>
        /// <returns>Full path to the output directory</returns>
        string EnsureOutputDirectory(string basePath, AudienceSegment segment);
    }
}
