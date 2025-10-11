using System.Collections.Generic;
using System.Threading;
using System.Threading.Tasks;
using PrismQ.Shared.Models;

namespace PrismQ.Shared.Interfaces
{
    /// <summary>
    /// Interface for generating keyframes per scene/shot using SDXL
    /// </summary>
    public interface IKeyframeGenerationService
    {
        /// <summary>
        /// Generate keyframes for all shots in a shotlist
        /// </summary>
        /// <param name="shotlist">Structured shotlist with shots</param>
        /// <param name="titleId">Title identifier for file organization</param>
        /// <param name="segment">Segment type (e.g., "shorts", "long-form")</param>
        /// <param name="age">Age rating (e.g., "all-ages", "13+", "18+")</param>
        /// <param name="config">Generation configuration</param>
        /// <param name="cancellationToken">Cancellation token</param>
        /// <returns>Keyframe manifest with all generated keyframes</returns>
        Task<KeyframeManifest> GenerateKeyframesAsync(
            StructuredShotlist shotlist,
            string titleId,
            string segment,
            string age,
            KeyframeGenerationConfig config,
            CancellationToken cancellationToken = default);

        /// <summary>
        /// Generate keyframes for a single shot
        /// </summary>
        /// <param name="shot">Shot to generate keyframes for</param>
        /// <param name="titleId">Title identifier</param>
        /// <param name="outputDir">Output directory for keyframes</param>
        /// <param name="config">Generation configuration</param>
        /// <param name="cancellationToken">Cancellation token</param>
        /// <returns>List of generated keyframes</returns>
        Task<List<GeneratedKeyframe>> GenerateKeyframesForShotAsync(
            StructuredShot shot,
            string titleId,
            string outputDir,
            KeyframeGenerationConfig config,
            CancellationToken cancellationToken = default);

        /// <summary>
        /// Create prompt for a specific shot
        /// </summary>
        /// <param name="shot">Shot to create prompt for</param>
        /// <param name="config">Generation configuration</param>
        /// <returns>Keyframe prompt with style, camera, mood, and age-safe content</returns>
        KeyframePrompt CreatePromptForShot(StructuredShot shot, KeyframeGenerationConfig config);

        /// <summary>
        /// Select top N keyframes per shot based on quality
        /// </summary>
        /// <param name="keyframes">All generated keyframes</param>
        /// <param name="topN">Number of top keyframes to select per shot</param>
        /// <returns>Dictionary mapping shot number to selected keyframe paths</returns>
        Dictionary<int, List<string>> SelectTopKeyframes(List<GeneratedKeyframe> keyframes, int topN);

        /// <summary>
        /// Save keyframe prompts to JSON file
        /// </summary>
        /// <param name="prompts">List of keyframe prompts</param>
        /// <param name="outputPath">Path to save JSON file</param>
        /// <returns>Path to saved file</returns>
        Task<string> SavePromptsAsync(List<KeyframePrompt> prompts, string outputPath);

        /// <summary>
        /// Save keyframe manifest to JSON file
        /// </summary>
        /// <param name="manifest">Keyframe manifest</param>
        /// <param name="outputPath">Path to save JSON file</param>
        /// <returns>Path to saved file</returns>
        Task<string> SaveManifestAsync(KeyframeManifest manifest, string outputPath);

        /// <summary>
        /// Generate keyframes from a simple scene description and optional subtitles
        /// </summary>
        /// <param name="sceneDescription">Description of the scene to generate</param>
        /// <param name="subtitles">Optional subtitle text to include in the scene</param>
        /// <param name="titleId">Title identifier for file organization</param>
        /// <param name="config">Generation configuration</param>
        /// <param name="cancellationToken">Cancellation token</param>
        /// <returns>Keyframe manifest with generated keyframes</returns>
        Task<KeyframeManifest> GenerateKeyframesFromSceneAsync(
            string sceneDescription,
            string? subtitles,
            string titleId,
            KeyframeGenerationConfig config,
            CancellationToken cancellationToken = default);
    }
}
