namespace StoryGenerator.Core.Interfaces;

/// <summary>
/// Represents a step in the processing pipeline.
/// </summary>
/// <typeparam name="TInput">Input type for the step.</typeparam>
/// <typeparam name="TOutput">Output type for the step.</typeparam>
public interface IPipelineStep<TInput, TOutput>
{
    /// <summary>
    /// Name of the pipeline step.
    /// </summary>
    string Name { get; }

    /// <summary>
    /// Executes the pipeline step.
    /// </summary>
    /// <param name="input">Input data for the step.</param>
    /// <param name="cancellationToken">Cancellation token.</param>
    /// <returns>Result of the step execution.</returns>
    Task<Result<TOutput>> ExecuteAsync(TInput input, CancellationToken cancellationToken = default);
}
