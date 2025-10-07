using System.Threading;
using System.Threading.Tasks;
using StoryGenerator.Models;

namespace StoryGenerator.Interfaces
{
    /// <summary>
    /// Interface for iterating and improving scripts based on feedback.
    /// Takes scored scripts and produces improved versions.
    /// </summary>
    public interface IScriptIterator
    {
        /// <summary>
        /// Iterate and improve a script based on scoring feedback.
        /// Creates a new version with improvements addressing identified weaknesses.
        /// </summary>
        /// <param name="originalScriptPath">Path to the original script file</param>
        /// <param name="scoringResult">The scoring result with feedback</param>
        /// <param name="targetVersion">Target version identifier (e.g., "v1", "v2")</param>
        /// <param name="cancellationToken">Cancellation token</param>
        /// <returns>The improved script version</returns>
        Task<ScriptVersion> IterateScriptAsync(
            string originalScriptPath,
            ScriptScoringResult scoringResult,
            string targetVersion,
            CancellationToken cancellationToken = default);

        /// <summary>
        /// Iterate a script based on custom feedback.
        /// Allows for manual feedback instead of using a scoring result.
        /// </summary>
        /// <param name="originalScriptPath">Path to the original script</param>
        /// <param name="feedback">Custom feedback for improvement</param>
        /// <param name="titleId">The title ID</param>
        /// <param name="targetVersion">Target version identifier</param>
        /// <param name="targetAudience">Target audience segment</param>
        /// <param name="cancellationToken">Cancellation token</param>
        /// <returns>The improved script version</returns>
        Task<ScriptVersion> IterateScriptWithFeedbackAsync(
            string originalScriptPath,
            string feedback,
            string titleId,
            string targetVersion,
            AudienceSegment targetAudience,
            CancellationToken cancellationToken = default);

        /// <summary>
        /// Iterate multiple scripts in a directory based on their scoring results.
        /// Processes all scripts and creates improved versions.
        /// </summary>
        /// <param name="scriptsDirectory">Directory containing original scripts</param>
        /// <param name="scoringResults">Collection of scoring results with feedback</param>
        /// <param name="targetVersion">Target version identifier</param>
        /// <param name="cancellationToken">Cancellation token</param>
        /// <returns>Collection of improved script versions</returns>
        Task<System.Collections.Generic.IEnumerable<ScriptVersion>> IterateScriptsAsync(
            string scriptsDirectory,
            System.Collections.Generic.IEnumerable<ScriptScoringResult> scoringResults,
            string targetVersion,
            CancellationToken cancellationToken = default);

        /// <summary>
        /// Apply specific improvements to a script.
        /// Allows for targeted improvements in specific areas.
        /// </summary>
        /// <param name="scriptContent">Original script content</param>
        /// <param name="improvements">List of specific improvements to apply</param>
        /// <param name="cancellationToken">Cancellation token</param>
        /// <returns>Improved script content</returns>
        Task<string> ApplyImprovementsAsync(
            string scriptContent,
            System.Collections.Generic.IEnumerable<string> improvements,
            CancellationToken cancellationToken = default);
    }
}
