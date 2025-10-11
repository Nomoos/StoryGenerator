namespace StoryGenerator.Pipeline.Interfaces;

/// <summary>
/// Represents progress information for a pipeline stage
/// </summary>
public class PipelineProgress
{
    /// <summary>
    /// Stage name
    /// </summary>
    public string StageName { get; set; } = string.Empty;

    /// <summary>
    /// Progress percentage (0-100)
    /// </summary>
    public int PercentComplete { get; set; }

    /// <summary>
    /// Current status message
    /// </summary>
    public string Message { get; set; } = string.Empty;

    /// <summary>
    /// Timestamp of the progress update
    /// </summary>
    public DateTime Timestamp { get; set; } = DateTime.Now;
}

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
    /// Execute the pipeline stage with progress reporting
    /// </summary>
    /// <param name="input">Input data for the stage</param>
    /// <param name="progress">Progress reporter for status updates</param>
    /// <param name="cancellationToken">Cancellation token</param>
    /// <returns>Output data from the stage</returns>
    Task<TOutput> ExecuteAsync(
        TInput input,
        IProgress<PipelineProgress>? progress = null,
        CancellationToken cancellationToken = default);

    /// <summary>
    /// Validate input before execution
    /// </summary>
    /// <param name="input">Input to validate</param>
    /// <returns>True if input is valid, false otherwise</returns>
    Task<bool> ValidateInputAsync(TInput input);
}
