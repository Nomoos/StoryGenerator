using System.Text.Json;
using StoryGenerator.Pipeline.Config;
using StoryGenerator.Pipeline.Core;
using StoryGenerator.Pipeline.Interfaces;

namespace StoryGenerator.Pipeline.Services;

/// <summary>
/// Manages pipeline checkpoints for resuming interrupted pipelines.
/// Implements Single Responsibility Principle - only handles checkpoint persistence.
/// Provides atomic save operations and validation.
/// </summary>
public class PipelineCheckpointManager : IPipelineCheckpointManager
{
    private readonly PipelineConfig _config;
    private readonly PipelineLogger _logger;
    private readonly string _checkpointFilePath;
    private readonly SemaphoreSlim _semaphore = new(1, 1);

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

        // Validate checkpoint before saving
        if (!ValidateCheckpoint(checkpoint))
        {
            _logger.LogWarning("Checkpoint validation failed - not saving");
            return;
        }

        // Acquire lock for atomic save operation
        await _semaphore.WaitAsync(cancellationToken);
        try
        {
            // Ensure directory exists
            var directory = Path.GetDirectoryName(_checkpointFilePath);
            if (!string.IsNullOrEmpty(directory) && !Directory.Exists(directory))
            {
                Directory.CreateDirectory(directory);
            }

            // Save to temporary file first (atomic write pattern)
            var tempFilePath = _checkpointFilePath + ".tmp";
            var json = JsonSerializer.Serialize(checkpoint, new JsonSerializerOptions 
            { 
                WriteIndented = true 
            });
            
            await File.WriteAllTextAsync(tempFilePath, json, cancellationToken);
            
            // Atomic rename/replace
            if (File.Exists(_checkpointFilePath))
            {
                File.Replace(tempFilePath, _checkpointFilePath, _checkpointFilePath + ".bak");
            }
            else
            {
                File.Move(tempFilePath, _checkpointFilePath);
            }
            
            _logger.LogDebug($"Checkpoint saved atomically to: {_checkpointFilePath}");
        }
        catch (Exception ex)
        {
            _logger.LogWarning($"Failed to save checkpoint: {ex.Message}");
            throw;
        }
        finally
        {
            _semaphore.Release();
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

        await _semaphore.WaitAsync(cancellationToken);
        try
        {
            var json = await File.ReadAllTextAsync(_checkpointFilePath, cancellationToken);
            var checkpoint = JsonSerializer.Deserialize<PipelineCheckpoint>(json);
            
            if (checkpoint == null)
            {
                _logger.LogWarning("Failed to deserialize checkpoint - returning empty checkpoint");
                return new PipelineCheckpoint();
            }

            // Validate loaded checkpoint
            if (!ValidateCheckpoint(checkpoint))
            {
                _logger.LogWarning("Loaded checkpoint failed validation - returning empty checkpoint");
                return new PipelineCheckpoint();
            }

            _logger.LogInfo($"Checkpoint loaded from: {_checkpointFilePath}");
            return checkpoint;
        }
        catch (Exception ex)
        {
            _logger.LogWarning($"Failed to load checkpoint: {ex.Message}");
            return new PipelineCheckpoint();
        }
        finally
        {
            _semaphore.Release();
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

        await _semaphore.WaitAsync(cancellationToken);
        try
        {
            await Task.Run(() => File.Delete(_checkpointFilePath), cancellationToken);
            
            // Also delete backup if it exists
            var backupPath = _checkpointFilePath + ".bak";
            if (File.Exists(backupPath))
            {
                await Task.Run(() => File.Delete(backupPath), cancellationToken);
            }
            
            _logger.LogDebug($"Checkpoint deleted: {_checkpointFilePath}");
        }
        catch (Exception ex)
        {
            _logger.LogWarning($"Failed to delete checkpoint: {ex.Message}");
        }
        finally
        {
            _semaphore.Release();
        }
    }

    /// <summary>
    /// Validate checkpoint data for consistency
    /// </summary>
    private bool ValidateCheckpoint(PipelineCheckpoint checkpoint)
    {
        if (checkpoint == null)
        {
            return false;
        }

        // Check that CompletedSteps and StepData are not null
        if (checkpoint.CompletedSteps == null || checkpoint.StepData == null)
        {
            return false;
        }

        // Validate timestamp is not in the future
        if (checkpoint.LastUpdated > DateTime.Now.AddMinutes(1))
        {
            return false;
        }

        return true;
    }
}
