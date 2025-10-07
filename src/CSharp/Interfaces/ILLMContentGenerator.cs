using System.Threading;
using System.Threading.Tasks;

namespace StoryGenerator.Core.Interfaces
{
    /// <summary>
    /// Interface for generating content using Large Language Models.
    /// Supports script generation, scene breakdowns, and video descriptions.
    /// </summary>
    /// <remarks>
    /// Recommended models:
    /// - Qwen2.5-14B-Instruct: https://huggingface.co/unsloth/Qwen2.5-14B-Instruct
    /// - Llama-3.1-8B-Instruct: https://huggingface.co/meta-llama/Llama-3.1-8B-Instruct
    /// Implementation options: Ollama CLI or Python transformers API
    /// </remarks>
    public interface ILLMContentGenerator : IGenerator
    {
        /// <summary>
        /// Gets the model name being used (e.g., "qwen2.5:14b-instruct", "llama3.1:8b-instruct").
        /// </summary>
        string ModelName { get; }

        /// <summary>
        /// Gets the model provider (e.g., "Ollama", "Transformers").
        /// </summary>
        string Provider { get; }

        /// <summary>
        /// Generates a script from a story idea using LLM.
        /// </summary>
        /// <param name="storyIdea">The story idea to generate a script from.</param>
        /// <param name="targetLength">Target script length in words (default: 360 for ~60 seconds).</param>
        /// <param name="temperature">Sampling temperature for creativity (0.0-1.0, default: 0.7).</param>
        /// <param name="cancellationToken">Cancellation token.</param>
        /// <returns>The generated script text.</returns>
        Task<string> GenerateScriptAsync(
            IStoryIdea storyIdea,
            int targetLength = 360,
            float temperature = 0.7f,
            CancellationToken cancellationToken = default);

        /// <summary>
        /// Generates scene breakdown from a script.
        /// Analyzes the script and breaks it down into individual scenes with descriptions.
        /// </summary>
        /// <param name="scriptText">The script text to analyze.</param>
        /// <param name="temperature">Sampling temperature (0.0-1.0, default: 0.5 for more focused output).</param>
        /// <param name="cancellationToken">Cancellation token.</param>
        /// <returns>Scene breakdown as structured text.</returns>
        Task<string> GenerateSceneBreakdownAsync(
            string scriptText,
            float temperature = 0.5f,
            CancellationToken cancellationToken = default);

        /// <summary>
        /// Generates video description for a scene.
        /// Creates detailed visual descriptions suitable for video generation prompts.
        /// </summary>
        /// <param name="sceneDescription">The scene description to expand.</param>
        /// <param name="mood">The desired mood/emotion for the scene.</param>
        /// <param name="temperature">Sampling temperature (0.0-1.0, default: 0.6).</param>
        /// <param name="cancellationToken">Cancellation token.</param>
        /// <returns>Detailed video description/prompt.</returns>
        Task<string> GenerateVideoDescriptionAsync(
            string sceneDescription,
            string mood,
            float temperature = 0.6f,
            CancellationToken cancellationToken = default);

        /// <summary>
        /// Generates content with custom prompt.
        /// Allows flexible content generation with user-defined prompts.
        /// </summary>
        /// <param name="systemPrompt">System instructions for the LLM.</param>
        /// <param name="userPrompt">User prompt/query.</param>
        /// <param name="temperature">Sampling temperature (0.0-1.0).</param>
        /// <param name="maxTokens">Maximum tokens to generate (optional).</param>
        /// <param name="cancellationToken">Cancellation token.</param>
        /// <returns>Generated content.</returns>
        Task<string> GenerateAsync(
            string systemPrompt,
            string userPrompt,
            float temperature = 0.7f,
            int? maxTokens = null,
            CancellationToken cancellationToken = default);
    }
}
