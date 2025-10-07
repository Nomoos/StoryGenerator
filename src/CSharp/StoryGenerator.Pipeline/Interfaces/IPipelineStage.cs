namespace StoryGenerator.Pipeline.Interfaces;

/// <summary>
/// Represents a single stage in the pipeline.
/// Each stage is independently testable and replaceable.
/// Follows Single Responsibility Principle - each stage does one thing.
/// </summary>
/// <typeparam name="TInput">Input type for the stage</typeparam>
/// <typeparam name="TOutput">Output type for the stage</typeparam>
public interface IPipelineStage<TInput, TOutput>
{
    /// <summary>
    /// Name of the pipeline stage for logging and tracking
    /// </summary>
    string StageName { get; }

    /// <summary>
    /// Execute the pipeline stage
    /// </summary>
    /// <param name="input">Input data for the stage</param>
    /// <param name="cancellationToken">Cancellation token</param>
    /// <returns>Output data from the stage</returns>
    Task<TOutput> ExecuteAsync(TInput input, CancellationToken cancellationToken = default);

    /// <summary>
    /// Validate input before execution
    /// </summary>
    /// <param name="input">Input to validate</param>
    /// <returns>True if input is valid, false otherwise</returns>
    Task<bool> ValidateInputAsync(TInput input);
}
