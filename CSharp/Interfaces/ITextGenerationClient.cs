using System;
using System.Collections.Generic;
using System.Threading;
using System.Threading.Tasks;

namespace StoryGenerator.Core.Interfaces
{
    /// <summary>
    /// Interface for text generation using large language models.
    /// Supports both local models (Qwen2.5-14B, Llama-3.1-8B) and API-based models.
    /// </summary>
    /// <remarks>
    /// Recommended models:
    /// - Qwen/Qwen2.5-14B-Instruct: https://huggingface.co/Qwen/Qwen2.5-14B-Instruct
    /// - meta-llama/Llama-3.1-8B-Instruct: https://huggingface.co/meta-llama/Llama-3.1-8B-Instruct
    /// Both support long context (32K-128K tokens) and instruction following.
    /// </remarks>
    public interface ITextGenerationClient
    {
        /// <summary>
        /// Generate text completion from a prompt.
        /// </summary>
        /// <param name="prompt">Input prompt text</param>
        /// <param name="maxTokens">Maximum tokens to generate (default: 1024)</param>
        /// <param name="temperature">Sampling temperature 0.0-2.0 (default: 0.7)</param>
        /// <param name="topP">Nucleus sampling parameter (default: 0.9)</param>
        /// <param name="stopSequences">Optional stop sequences</param>
        /// <param name="cancellationToken">Cancellation token</param>
        /// <returns>Generated text</returns>
        Task<TextGenerationResult> GenerateAsync(
            string prompt,
            int maxTokens = 1024,
            double temperature = 0.7,
            double topP = 0.9,
            List<string>? stopSequences = null,
            CancellationToken cancellationToken = default);

        /// <summary>
        /// Generate text using chat format with system and user messages.
        /// </summary>
        /// <param name="messages">List of chat messages</param>
        /// <param name="maxTokens">Maximum tokens to generate</param>
        /// <param name="temperature">Sampling temperature</param>
        /// <param name="topP">Nucleus sampling parameter</param>
        /// <param name="cancellationToken">Cancellation token</param>
        /// <returns>Assistant's response</returns>
        Task<TextGenerationResult> ChatAsync(
            List<ChatMessage> messages,
            int maxTokens = 1024,
            double temperature = 0.7,
            double topP = 0.9,
            CancellationToken cancellationToken = default);

        /// <summary>
        /// Generate text with streaming output.
        /// </summary>
        /// <param name="prompt">Input prompt text</param>
        /// <param name="maxTokens">Maximum tokens to generate</param>
        /// <param name="temperature">Sampling temperature</param>
        /// <param name="cancellationToken">Cancellation token</param>
        /// <returns>Async enumerable of text chunks</returns>
        IAsyncEnumerable<string> GenerateStreamAsync(
            string prompt,
            int maxTokens = 1024,
            double temperature = 0.7,
            CancellationToken cancellationToken = default);

        /// <summary>
        /// Get information about the loaded model.
        /// </summary>
        /// <returns>Model information</returns>
        ModelInfo GetModelInfo();

        /// <summary>
        /// Check if the model is ready for inference.
        /// </summary>
        /// <returns>True if model is loaded and ready</returns>
        Task<bool> IsReadyAsync();
    }

    /// <summary>
    /// Result of text generation.
    /// </summary>
    public class TextGenerationResult
    {
        /// <summary>
        /// Generated text.
        /// </summary>
        public string Text { get; set; } = string.Empty;

        /// <summary>
        /// Number of tokens generated.
        /// </summary>
        public int TokensGenerated { get; set; }

        /// <summary>
        /// Generation time in milliseconds.
        /// </summary>
        public long GenerationTimeMs { get; set; }

        /// <summary>
        /// Tokens per second.
        /// </summary>
        public double TokensPerSecond => TokensGenerated > 0 && GenerationTimeMs > 0
            ? (TokensGenerated / (GenerationTimeMs / 1000.0))
            : 0;

        /// <summary>
        /// Finish reason (e.g., "stop", "length", "error").
        /// </summary>
        public string FinishReason { get; set; } = string.Empty;

        /// <summary>
        /// Model used for generation.
        /// </summary>
        public string Model { get; set; } = string.Empty;
    }

    /// <summary>
    /// Chat message for conversation-style generation.
    /// </summary>
    public class ChatMessage
    {
        /// <summary>
        /// Role of the message sender (system, user, assistant).
        /// </summary>
        public string Role { get; set; } = string.Empty;

        /// <summary>
        /// Content of the message.
        /// </summary>
        public string Content { get; set; } = string.Empty;

        /// <summary>
        /// Optional name of the message sender.
        /// </summary>
        public string? Name { get; set; }

        /// <summary>
        /// Create a system message.
        /// </summary>
        public static ChatMessage System(string content) =>
            new() { Role = "system", Content = content };

        /// <summary>
        /// Create a user message.
        /// </summary>
        public static ChatMessage User(string content) =>
            new() { Role = "user", Content = content };

        /// <summary>
        /// Create an assistant message.
        /// </summary>
        public static ChatMessage Assistant(string content) =>
            new() { Role = "assistant", Content = content };
    }
}
