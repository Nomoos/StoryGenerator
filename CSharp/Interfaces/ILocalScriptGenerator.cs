using System.Threading;
using System.Threading.Tasks;
using StoryGenerator.Core.Interfaces;
using StoryGenerator.Models;

namespace StoryGenerator.Interfaces
{
    /// <summary>
    /// Interface for generating scripts using local LLM models.
    /// Extends IScriptGenerator with local model-specific functionality.
    /// </summary>
    /// <remarks>
    /// Supports local models like Qwen2.5-14B-Instruct, Llama-3.1-8B-Instruct.
    /// Generates raw scripts for specific audience segments and title IDs.
    /// Integrates with script scoring and iteration workflow.
    /// </remarks>
    public interface ILocalScriptGenerator : IGenerator
    {
        /// <summary>
        /// Generate a raw script using local LLM for a specific title and audience.
        /// Creates initial v0 version of the script.
        /// </summary>
        /// <param name="titleId">The title ID to generate a script for</param>
        /// <param name="title">The title text</param>
        /// <param name="targetAudience">Target audience segment</param>
        /// <param name="storyIdea">Optional story idea with additional context</param>
        /// <param name="cancellationToken">Cancellation token</param>
        /// <returns>Generated script version (v0)</returns>
        Task<ScriptVersion> GenerateRawScriptAsync(
            string titleId,
            string title,
            AudienceSegment targetAudience,
            IStoryIdea? storyIdea = null,
            CancellationToken cancellationToken = default);

        /// <summary>
        /// Generate raw scripts for multiple titles in a segment.
        /// Batch processing for all chosen titles in a segment/age group.
        /// </summary>
        /// <param name="titles">Collection of title items to generate scripts for</param>
        /// <param name="targetAudience">Target audience segment</param>
        /// <param name="cancellationToken">Cancellation token</param>
        /// <returns>Collection of generated script versions</returns>
        Task<System.Collections.Generic.IEnumerable<ScriptVersion>> GenerateRawScriptsAsync(
            System.Collections.Generic.IEnumerable<TitleItem> titles,
            AudienceSegment targetAudience,
            CancellationToken cancellationToken = default);

        /// <summary>
        /// Generate a script from a story idea using local LLM.
        /// Standard script generation from story metadata.
        /// </summary>
        /// <param name="storyIdea">Story idea with metadata</param>
        /// <param name="cancellationToken">Cancellation token</param>
        /// <returns>Generated script text</returns>
        Task<string> GenerateScriptAsync(
            IStoryIdea storyIdea,
            CancellationToken cancellationToken = default);

        /// <summary>
        /// Generate and save a raw script to the proper directory structure.
        /// Saves to /scripts/raw_local/{segment}/{age}/{title_id}.md
        /// </summary>
        /// <param name="titleId">The title ID</param>
        /// <param name="title">The title text</param>
        /// <param name="targetAudience">Target audience segment</param>
        /// <param name="baseScriptsPath">Base path to scripts directory</param>
        /// <param name="storyIdea">Optional story idea</param>
        /// <param name="cancellationToken">Cancellation token</param>
        /// <returns>Path to the saved script file</returns>
        Task<string> GenerateAndSaveRawScriptAsync(
            string titleId,
            string title,
            AudienceSegment targetAudience,
            string baseScriptsPath,
            IStoryIdea? storyIdea = null,
            CancellationToken cancellationToken = default);

        /// <summary>
        /// Get the local model name being used.
        /// </summary>
        /// <returns>Model name (e.g., "Qwen2.5-14B-Instruct")</returns>
        string GetModelName();

        /// <summary>
        /// Check if the local model is available and loaded.
        /// </summary>
        /// <returns>True if model is ready to use</returns>
        Task<bool> IsModelAvailableAsync();

        /// <summary>
        /// Get model configuration and parameters.
        /// </summary>
        /// <returns>Dictionary of model configuration</returns>
        System.Collections.Generic.Dictionary<string, object> GetModelConfiguration();
    }
}
