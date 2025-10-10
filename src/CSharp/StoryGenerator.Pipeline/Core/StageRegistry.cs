using StoryGenerator.Pipeline.Interfaces;

namespace StoryGenerator.Pipeline.Core;

/// <summary>
/// Registry for managing pipeline stages and their metadata.
/// Supports dynamic stage registration and discovery.
/// </summary>
public interface IStageRegistry
{
    /// <summary>
    /// Register a stage with the registry
    /// </summary>
    void Register(string id, StageMetadata metadata);

    /// <summary>
    /// Get metadata for a stage
    /// </summary>
    StageMetadata? GetMetadata(string id);

    /// <summary>
    /// Get all registered stages
    /// </summary>
    IReadOnlyList<StageMetadata> GetAllStages();

    /// <summary>
    /// Check if a stage is registered
    /// </summary>
    bool IsRegistered(string id);

    /// <summary>
    /// Unregister a stage
    /// </summary>
    void Unregister(string id);
}

/// <summary>
/// Metadata about a registered stage
/// </summary>
public class StageMetadata
{
    /// <summary>
    /// Unique identifier for the stage
    /// </summary>
    public string Id { get; set; } = string.Empty;

    /// <summary>
    /// Display name
    /// </summary>
    public string Name { get; set; } = string.Empty;

    /// <summary>
    /// Description of what the stage does
    /// </summary>
    public string Description { get; set; } = string.Empty;

    /// <summary>
    /// Stage category (e.g., "generation", "processing", "export")
    /// </summary>
    public string Category { get; set; } = string.Empty;

    /// <summary>
    /// Factory function to create stage definition
    /// </summary>
    public Func<StageConfiguration, StageDefinition>? CreateDefinition { get; set; }

    /// <summary>
    /// Default configuration for the stage
    /// </summary>
    public StageConfiguration DefaultConfiguration { get; set; } = new();

    /// <summary>
    /// Dependencies (stage IDs that must execute before this stage)
    /// </summary>
    public List<string> Dependencies { get; set; } = new();

    /// <summary>
    /// Whether this stage is optional
    /// </summary>
    public bool IsOptional { get; set; }
}

/// <summary>
/// Configuration for a stage instance
/// </summary>
public class StageConfiguration
{
    /// <summary>
    /// Stage ID
    /// </summary>
    public string Id { get; set; } = string.Empty;

    /// <summary>
    /// Whether the stage is enabled
    /// </summary>
    public bool Enabled { get; set; } = true;

    /// <summary>
    /// Execution order
    /// </summary>
    public int Order { get; set; }

    /// <summary>
    /// Continue pipeline on error
    /// </summary>
    public bool ContinueOnError { get; set; }

    /// <summary>
    /// Maximum retry attempts
    /// </summary>
    public int MaxRetries { get; set; }

    /// <summary>
    /// Retry delay in seconds
    /// </summary>
    public int RetryDelaySeconds { get; set; } = 5;

    /// <summary>
    /// Custom parameters for the stage
    /// </summary>
    public Dictionary<string, object> Parameters { get; set; } = new();
}

/// <summary>
/// Default implementation of stage registry
/// </summary>
public class StageRegistry : IStageRegistry
{
    private readonly Dictionary<string, StageMetadata> _stages = new();
    private readonly object _lock = new();

    /// <inheritdoc/>
    public void Register(string id, StageMetadata metadata)
    {
        if (string.IsNullOrWhiteSpace(id))
        {
            throw new ArgumentException("Stage ID cannot be empty", nameof(id));
        }

        if (metadata == null)
        {
            throw new ArgumentNullException(nameof(metadata));
        }

        lock (_lock)
        {
            if (_stages.ContainsKey(id))
            {
                throw new InvalidOperationException($"Stage '{id}' is already registered");
            }

            _stages[id] = metadata;
        }
    }

    /// <inheritdoc/>
    public StageMetadata? GetMetadata(string id)
    {
        lock (_lock)
        {
            return _stages.TryGetValue(id, out var metadata) ? metadata : null;
        }
    }

    /// <inheritdoc/>
    public IReadOnlyList<StageMetadata> GetAllStages()
    {
        lock (_lock)
        {
            return _stages.Values.ToList();
        }
    }

    /// <inheritdoc/>
    public bool IsRegistered(string id)
    {
        lock (_lock)
        {
            return _stages.ContainsKey(id);
        }
    }

    /// <inheritdoc/>
    public void Unregister(string id)
    {
        lock (_lock)
        {
            _stages.Remove(id);
        }
    }
}
