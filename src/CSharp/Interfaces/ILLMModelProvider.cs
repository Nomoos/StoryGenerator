using System.Collections.Generic;
using System.Threading;
using System.Threading.Tasks;

namespace StoryGenerator.Core.Interfaces
{
    /// <summary>
    /// Interface for LLM model providers (Ollama, Transformers, etc.).
    /// Abstracts the underlying implementation for model interactions.
    /// </summary>
    public interface ILLMModelProvider
    {
        /// <summary>
        /// Gets the provider name (e.g., "Ollama", "Transformers", "OpenAI").
        /// </summary>
        string ProviderName { get; }

        /// <summary>
        /// Gets the current model name.
        /// </summary>
        string CurrentModel { get; }

        /// <summary>
        /// Gets or sets the base URL for API access (if applicable).
        /// </summary>
        string? BaseUrl { get; set; }

        /// <summary>
        /// Lists available models from the provider.
        /// </summary>
        /// <param name="cancellationToken">Cancellation token.</param>
        /// <returns>List of available model names.</returns>
        Task<List<string>> ListAvailableModelsAsync(CancellationToken cancellationToken = default);

        /// <summary>
        /// Checks if a specific model is available.
        /// </summary>
        /// <param name="modelName">The model name to check.</param>
        /// <param name="cancellationToken">Cancellation token.</param>
        /// <returns>True if the model is available.</returns>
        Task<bool> IsModelAvailableAsync(string modelName, CancellationToken cancellationToken = default);

        /// <summary>
        /// Downloads/pulls a model (if supported by provider).
        /// </summary>
        /// <param name="modelName">The model name to download.</param>
        /// <param name="cancellationToken">Cancellation token.</param>
        /// <returns>True if successful.</returns>
        Task<bool> PullModelAsync(string modelName, CancellationToken cancellationToken = default);

        /// <summary>
        /// Generates text using the specified model.
        /// </summary>
        /// <param name="modelName">The model to use.</param>
        /// <param name="systemPrompt">System instructions.</param>
        /// <param name="userPrompt">User prompt.</param>
        /// <param name="temperature">Sampling temperature (0.0-1.0).</param>
        /// <param name="maxTokens">Maximum tokens to generate (optional).</param>
        /// <param name="cancellationToken">Cancellation token.</param>
        /// <returns>Generated text.</returns>
        Task<string> GenerateAsync(
            string modelName,
            string systemPrompt,
            string userPrompt,
            float temperature = 0.7f,
            int? maxTokens = null,
            CancellationToken cancellationToken = default);

        /// <summary>
        /// Generates text with chat history context.
        /// </summary>
        /// <param name="modelName">The model to use.</param>
        /// <param name="messages">List of chat messages.</param>
        /// <param name="temperature">Sampling temperature (0.0-1.0).</param>
        /// <param name="maxTokens">Maximum tokens to generate (optional).</param>
        /// <param name="cancellationToken">Cancellation token.</param>
        /// <returns>Generated text.</returns>
        Task<string> ChatAsync(
            string modelName,
            List<ChatMessage> messages,
            float temperature = 0.7f,
            int? maxTokens = null,
            CancellationToken cancellationToken = default);

        /// <summary>
        /// Gets model information/metadata.
        /// </summary>
        /// <param name="modelName">The model name.</param>
        /// <param name="cancellationToken">Cancellation token.</param>
        /// <returns>Model information.</returns>
        Task<ModelInfo> GetModelInfoAsync(string modelName, CancellationToken cancellationToken = default);
    }

    /// <summary>
    /// Represents a chat message for conversation context.
    /// </summary>
    public class ChatMessage
    {
        /// <summary>
        /// Gets or sets the role (system, user, assistant).
        /// </summary>
        public string Role { get; set; } = string.Empty;

        /// <summary>
        /// Gets or sets the message content.
        /// </summary>
        public string Content { get; set; } = string.Empty;

        /// <summary>
        /// Initializes a new instance of the ChatMessage class.
        /// </summary>
        public ChatMessage() { }

        /// <summary>
        /// Initializes a new instance of the ChatMessage class.
        /// </summary>
        /// <param name="role">The role (system, user, assistant).</param>
        /// <param name="content">The message content.</param>
        public ChatMessage(string role, string content)
        {
            Role = role;
            Content = content;
        }
    }

    /// <summary>
    /// Represents information about an LLM model.
    /// </summary>
    public class ModelInfo
    {
        /// <summary>
        /// Gets or sets the model name.
        /// </summary>
        public string Name { get; set; } = string.Empty;

        /// <summary>
        /// Gets or sets the model family (e.g., "Qwen2.5", "Llama3.1").
        /// </summary>
        public string Family { get; set; } = string.Empty;

        /// <summary>
        /// Gets or sets the parameter size (e.g., "14B", "8B").
        /// </summary>
        public string ParameterSize { get; set; } = string.Empty;

        /// <summary>
        /// Gets or sets the quantization level (e.g., "Q4_K_M", "fp16").
        /// </summary>
        public string Quantization { get; set; } = string.Empty;

        /// <summary>
        /// Gets or sets whether the model is instruction-tuned.
        /// </summary>
        public bool IsInstructionTuned { get; set; }

        /// <summary>
        /// Gets or sets the context length (max tokens).
        /// </summary>
        public int ContextLength { get; set; }

        /// <summary>
        /// Gets or sets the model size in bytes.
        /// </summary>
        public long SizeBytes { get; set; }

        /// <summary>
        /// Gets or sets additional metadata.
        /// </summary>
        public Dictionary<string, object> Metadata { get; set; } = new();
    }

    /// <summary>
    /// Recommended LLM models for story generation tasks.
    /// </summary>
    public static class RecommendedModels
    {
        /// <summary>
        /// Qwen2.5-14B-Instruct - Recommended for detailed creative content.
        /// </summary>
        public const string Qwen25_14B_Instruct = "qwen2.5:14b-instruct";

        /// <summary>
        /// Llama-3.1-8B-Instruct - Good balance of speed and quality.
        /// </summary>
        public const string Llama31_8B_Instruct = "llama3.1:8b-instruct";

        /// <summary>
        /// Qwen2.5-14B-Instruct (Q4 quantized) - Faster, less VRAM.
        /// </summary>
        public const string Qwen25_14B_Instruct_Q4 = "qwen2.5:14b-instruct-q4_K_M";

        /// <summary>
        /// Llama-3.1-8B-Instruct (Q4 quantized) - Fastest inference.
        /// </summary>
        public const string Llama31_8B_Instruct_Q4 = "llama3.1:8b-instruct-q4_K_M";

        /// <summary>
        /// Gets all recommended models.
        /// </summary>
        public static readonly string[] All = new[]
        {
            Qwen25_14B_Instruct,
            Llama31_8B_Instruct,
            Qwen25_14B_Instruct_Q4,
            Llama31_8B_Instruct_Q4
        };

        /// <summary>
        /// Gets the default model for content generation.
        /// </summary>
        public static string Default => Qwen25_14B_Instruct;

        /// <summary>
        /// Gets the fastest model for quick iterations.
        /// </summary>
        public static string Fastest => Llama31_8B_Instruct_Q4;
    }
}
