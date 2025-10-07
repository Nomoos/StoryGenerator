using System.Text.Json;
using StoryGenerator.Pipeline.Config;
using StoryGenerator.Pipeline.Core;
using StoryGenerator.Pipeline.Interfaces;

namespace StoryGenerator.Pipeline.Services;

/// <summary>
/// Manages pipeline checkpoints for resuming interrupted pipelines.
/// Implements Single Responsibility Principle - only handles checkpoint persistence.
/// </summary>
public class PipelineCheckpointManager : IPipelineCheckpointManager
{
    private readonly PipelineConfig _config;
    private readonly PipelineLogger _logger;
    private readonly string _checkpointFilePath;

    public PipelineCheckpointManager(PipelineConfig config, PipelineLogger logger)
    {
        _config = config ?? throw new ArgumentNullException(nameof(config));
        _logger = logger ?? throw new ArgumentNullException(nameof(logger));
        _checkpointFilePath = Path.Combine(_config.Paths.StoryRoot, "pipeline_checkpoint.json");
    }

    /// <inheritdoc/>
    public async Task SaveCheckpointAsync(PipelineCheckpoint checkpoint, CancellationToken cancellationToken = default)
    {
        if (checkpoint == null)
        {
            throw new ArgumentNullException(nameof(checkpoint));
        }

        if (!_config.Processing.Checkpointing.Enabled)
        {
            return;
        }

        try
        {
            var json = JsonSerializer.Serialize(checkpoint, new JsonSerializerOptions 
            { 
                WriteIndented = true 
            });
            await File.WriteAllTextAsync(_checkpointFilePath, json, cancellationToken);
            _logger.LogDebug($"Checkpoint saved to: {_checkpointFilePath}");
        }
        catch (Exception ex)
        {
            _logger.LogWarning($"Failed to save checkpoint: {ex.Message}");
        }
    }

    /// <inheritdoc/>
    public async Task<PipelineCheckpoint> LoadCheckpointAsync(CancellationToken cancellationToken = default)
    {
        if (!_config.Processing.Checkpointing.Enabled || 
            !_config.Processing.Checkpointing.ResumeFromCheckpoint)
        {
            return new PipelineCheckpoint();
        }

        if (!File.Exists(_checkpointFilePath))
        {
            return new PipelineCheckpoint();
        }

        try
        {
            var json = await File.ReadAllTextAsync(_checkpointFilePath, cancellationToken);
            var checkpoint = JsonSerializer.Deserialize<PipelineCheckpoint>(json);
            _logger.LogInfo($"Checkpoint loaded from: {_checkpointFilePath}");
            return checkpoint ?? new PipelineCheckpoint();
        }
        catch (Exception ex)
        {
            _logger.LogWarning($"Failed to load checkpoint: {ex.Message}");
            return new PipelineCheckpoint();
        }
    }

    /// <inheritdoc/>
    public Task<bool> HasCheckpointAsync()
    {
        return Task.FromResult(File.Exists(_checkpointFilePath));
    }

    /// <inheritdoc/>
    public async Task DeleteCheckpointAsync(CancellationToken cancellationToken = default)
    {
        if (!File.Exists(_checkpointFilePath))
        {
            return;
        }

        try
        {
            await Task.Run(() => File.Delete(_checkpointFilePath), cancellationToken);
            _logger.LogDebug($"Checkpoint deleted: {_checkpointFilePath}");
        }
        catch (Exception ex)
        {
            _logger.LogWarning($"Failed to delete checkpoint: {ex.Message}");
        }
    }
}
