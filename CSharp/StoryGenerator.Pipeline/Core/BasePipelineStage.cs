using StoryGenerator.Pipeline.Interfaces;

namespace StoryGenerator.Pipeline.Core;

/// <summary>
/// Base implementation for pipeline stages with common functionality.
/// Provides default implementations for validation and progress reporting.
/// </summary>
/// <typeparam name="TInput">Input type for the stage</typeparam>
/// <typeparam name="TOutput">Output type for the stage</typeparam>
public abstract class BasePipelineStage<TInput, TOutput> : IPipelineStage<TInput, TOutput>
{
    /// <inheritdoc/>
    public abstract string StageName { get; }

    /// <inheritdoc/>
    public async Task<TOutput> ExecuteAsync(
        TInput input,
        IProgress<PipelineProgress>? progress = null,
        CancellationToken cancellationToken = default)
    {
        // Validate input
        if (!await ValidateInputAsync(input))
        {
            throw new ArgumentException($"Invalid input for stage: {StageName}", nameof(input));
        }

        // Report start
        ReportProgress(progress, 0, $"Starting {StageName}");

        try
        {
            // Execute the stage-specific logic
            var result = await ExecuteCoreAsync(input, progress, cancellationToken);

            // Report completion
            ReportProgress(progress, 100, $"Completed {StageName}");

            return result;
        }
        catch (Exception ex)
        {
            // Report error
            ReportProgress(progress, -1, $"Error in {StageName}: {ex.Message}");
            throw;
        }
    }

    /// <summary>
    /// Core execution logic to be implemented by derived classes.
    /// </summary>
    protected abstract Task<TOutput> ExecuteCoreAsync(
        TInput input,
        IProgress<PipelineProgress>? progress,
        CancellationToken cancellationToken);

    /// <inheritdoc/>
    public virtual Task<bool> ValidateInputAsync(TInput input)
    {
        // Default implementation - check for null
        return Task.FromResult(input != null);
    }

    /// <summary>
    /// Helper method to report progress.
    /// </summary>
    protected void ReportProgress(IProgress<PipelineProgress>? progress, int percentComplete, string message)
    {
        progress?.Report(new PipelineProgress
        {
            StageName = StageName,
            PercentComplete = percentComplete,
            Message = message,
            Timestamp = DateTime.Now
        });
    }
}
