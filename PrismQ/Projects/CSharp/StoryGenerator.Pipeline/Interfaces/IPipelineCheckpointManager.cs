using StoryGenerator.Pipeline.Core;

namespace StoryGenerator.Pipeline.Interfaces;

/// <summary>
/// Manages pipeline checkpoints for resuming interrupted pipelines.
/// Follows Single Responsibility Principle - only handles checkpoint persistence.
/// </summary>
public interface IPipelineCheckpointManager
{
    /// <summary>
    /// Save a checkpoint to persistent storage
    /// </summary>
    /// <param name="checkpoint">Checkpoint data to save</param>
    /// <param name="cancellationToken">Cancellation token</param>
    Task SaveCheckpointAsync(PipelineCheckpoint checkpoint, CancellationToken cancellationToken = default);

    /// <summary>
    /// Load a checkpoint from persistent storage
    /// </summary>
    /// <param name="cancellationToken">Cancellation token</param>
    /// <returns>Checkpoint if exists, otherwise new empty checkpoint</returns>
    Task<PipelineCheckpoint> LoadCheckpointAsync(CancellationToken cancellationToken = default);

    /// <summary>
    /// Check if a checkpoint exists
    /// </summary>
    /// <returns>True if checkpoint exists, false otherwise</returns>
    Task<bool> HasCheckpointAsync();

    /// <summary>
    /// Delete the checkpoint
    /// </summary>
    /// <param name="cancellationToken">Cancellation token</param>
    Task DeleteCheckpointAsync(CancellationToken cancellationToken = default);
}
