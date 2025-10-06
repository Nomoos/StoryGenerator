using System.Threading;
using System.Threading.Tasks;
using StoryGenerator.Models;

namespace StoryGenerator.Interfaces
{
    /// <summary>
    /// Interface for scoring scripts based on rubric criteria and narrative cohesion.
    /// Evaluates script quality and provides detailed feedback for improvement.
    /// </summary>
    public interface IScriptScorer
    {
        /// <summary>
        /// Score a script from file path.
        /// Evaluates the script using rubric criteria and narrative cohesion analysis.
        /// </summary>
        /// <param name="scriptPath">Path to the script file to score</param>
        /// <param name="titleId">The title ID for this script</param>
        /// <param name="version">The version identifier (e.g., "v0", "v1")</param>
        /// <param name="targetAudience">Target audience segment</param>
        /// <param name="cancellationToken">Cancellation token</param>
        /// <returns>Script scoring result with scores and feedback</returns>
        Task<ScriptScoringResult> ScoreScriptAsync(
            string scriptPath,
            string titleId,
            string version,
            AudienceSegment targetAudience,
            CancellationToken cancellationToken = default);

        /// <summary>
        /// Score a script from content string.
        /// </summary>
        /// <param name="scriptContent">The script content to score</param>
        /// <param name="titleId">The title ID for this script</param>
        /// <param name="version">The version identifier</param>
        /// <param name="targetAudience">Target audience segment</param>
        /// <param name="cancellationToken">Cancellation token</param>
        /// <returns>Script scoring result with scores and feedback</returns>
        Task<ScriptScoringResult> ScoreScriptContentAsync(
            string scriptContent,
            string titleId,
            string version,
            AudienceSegment targetAudience,
            CancellationToken cancellationToken = default);

        /// <summary>
        /// Score multiple scripts in a segment directory.
        /// Processes all scripts in /scripts/raw_local/{segment}/{age}/ or similar directories.
        /// </summary>
        /// <param name="scriptsDirectory">Directory containing scripts to score</param>
        /// <param name="targetAudience">Target audience segment</param>
        /// <param name="version">Version identifier for these scripts</param>
        /// <param name="cancellationToken">Cancellation token</param>
        /// <returns>Collection of scoring results</returns>
        Task<System.Collections.Generic.IEnumerable<ScriptScoringResult>> ScoreScriptsInDirectoryAsync(
            string scriptsDirectory,
            AudienceSegment targetAudience,
            string version,
            CancellationToken cancellationToken = default);

        /// <summary>
        /// Validate scoring configuration and rubric.
        /// Ensures all required scoring criteria are properly configured.
        /// </summary>
        /// <returns>True if configuration is valid</returns>
        bool ValidateScoringConfiguration();
    }
}
