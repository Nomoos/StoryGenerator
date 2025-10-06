using System.Collections.Generic;
using System.Threading;
using System.Threading.Tasks;

namespace StoryGenerator.Research
{
    /// <summary>
    /// Interface for Ollama local LLM client.
    /// Defines operations for interacting with local language models via Ollama.
    /// </summary>
    public interface IOllamaClient
    {
        /// <summary>
        /// Generate text using Ollama model.
        /// </summary>
        /// <param name="prompt">Input prompt</param>
        /// <param name="system">Optional system message</param>
        /// <param name="temperature">Sampling temperature (0.0-1.0)</param>
        /// <param name="maxTokens">Maximum tokens to generate</param>
        /// <param name="cancellationToken">Cancellation token</param>
        /// <returns>Generated text</returns>
        Task<string> GenerateAsync(
            string prompt,
            string system = null,
            float temperature = 0.7f,
            int? maxTokens = null,
            CancellationToken cancellationToken = default);

        /// <summary>
        /// Chat completion using Ollama API format.
        /// </summary>
        /// <param name="messages">List of chat messages</param>
        /// <param name="temperature">Sampling temperature</param>
        /// <param name="maxTokens">Maximum tokens to generate</param>
        /// <param name="cancellationToken">Cancellation token</param>
        /// <returns>Assistant's response</returns>
        Task<string> ChatAsync(
            List<ChatMessage> messages,
            float temperature = 0.7f,
            int? maxTokens = null,
            CancellationToken cancellationToken = default);

        /// <summary>
        /// List available Ollama models.
        /// </summary>
        /// <returns>List of model names</returns>
        Task<List<string>> ListModelsAsync();

        /// <summary>
        /// Download an Ollama model.
        /// </summary>
        /// <param name="modelName">Name of the model to download</param>
        /// <returns>True if successful</returns>
        Task<bool> PullModelAsync(string modelName);
    }
}
