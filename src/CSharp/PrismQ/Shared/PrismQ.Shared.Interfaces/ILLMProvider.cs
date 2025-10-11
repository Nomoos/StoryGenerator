namespace PrismQ.Shared.Interfaces;

using PrismQ.Shared.Models;

/// <summary>
/// Interface for LLM provider implementations.
/// </summary>
public interface ILLMProvider
{
    /// <summary>
    /// Gets the model name being used.
    /// </summary>
    string ModelName { get; }

    /// <summary>
    /// Generates a completion from a prompt.
    /// </summary>
    /// <param name="prompt">The input prompt.</param>
    /// <param name="cancellationToken">Cancellation token.</param>
    /// <returns>The generated completion text.</returns>
    Task<string> GenerateAsync(string prompt, CancellationToken cancellationToken = default);
}
