namespace StoryGenerator.Pipeline.Config;

/// <summary>
/// Pipeline orchestration configuration that can be loaded from YAML/JSON
/// </summary>
public class PipelineOrchestrationConfig
{
    /// <summary>
    /// Pipeline metadata
    /// </summary>
    public PipelineMetadata Metadata { get; set; } = new();

    /// <summary>
    /// Stages to execute in the pipeline
    /// </summary>
    public List<PipelineStageConfig> Stages { get; set; } = new();

    /// <summary>
    /// Global error handling configuration
    /// </summary>
    public ErrorHandlingConfig? ErrorHandling { get; set; }

    /// <summary>
    /// Global retry configuration
    /// </summary>
    public RetryConfig? Retry { get; set; }

    /// <summary>
    /// Logging configuration
    /// </summary>
    public LoggingConfig? Logging { get; set; }

    /// <summary>
    /// Variables that can be referenced in stage parameters
    /// </summary>
    public Dictionary<string, object> Variables { get; set; } = new();
}

/// <summary>
/// Pipeline metadata
/// </summary>
public class PipelineMetadata
{
    /// <summary>
    /// Pipeline name
    /// </summary>
    public string Name { get; set; } = "Unnamed Pipeline";

    /// <summary>
    /// Pipeline version
    /// </summary>
    public string Version { get; set; } = "1.0.0";

    /// <summary>
    /// Pipeline description
    /// </summary>
    public string Description { get; set; } = string.Empty;

    /// <summary>
    /// Pipeline author
    /// </summary>
    public string Author { get; set; } = string.Empty;

    /// <summary>
    /// Tags for categorization
    /// </summary>
    public List<string> Tags { get; set; } = new();
}

/// <summary>
/// Configuration for a stage in the pipeline
/// </summary>
public class PipelineStageConfig
{
    /// <summary>
    /// Stage identifier (must match a registered stage)
    /// </summary>
    public string Id { get; set; } = string.Empty;

    /// <summary>
    /// Display name (optional, defaults to ID)
    /// </summary>
    public string? Name { get; set; }

    /// <summary>
    /// Whether this stage is enabled
    /// </summary>
    public bool Enabled { get; set; } = true;

    /// <summary>
    /// Execution order (lower numbers execute first)
    /// </summary>
    public int Order { get; set; }

    /// <summary>
    /// Condition expression for conditional execution (optional)
    /// Simple expressions like "variables.skip_stage == false"
    /// </summary>
    public string? Condition { get; set; }

    /// <summary>
    /// Whether to continue pipeline if this stage fails
    /// </summary>
    public bool ContinueOnError { get; set; }

    /// <summary>
    /// Maximum retry attempts for this stage
    /// </summary>
    public int? MaxRetries { get; set; }

    /// <summary>
    /// Retry delay in seconds
    /// </summary>
    public int? RetryDelaySeconds { get; set; }

    /// <summary>
    /// Stage-specific parameters
    /// </summary>
    public Dictionary<string, object> Parameters { get; set; } = new();

    /// <summary>
    /// Timeout in seconds (0 = no timeout)
    /// </summary>
    public int TimeoutSeconds { get; set; }
}

/// <summary>
/// Retry configuration
/// </summary>
public class RetryConfig
{
    /// <summary>
    /// Maximum number of retries
    /// </summary>
    public int MaxRetries { get; set; } = 3;

    /// <summary>
    /// Delay between retries in seconds
    /// </summary>
    public int DelaySeconds { get; set; } = 5;

    /// <summary>
    /// Use exponential backoff
    /// </summary>
    public bool ExponentialBackoff { get; set; }

    /// <summary>
    /// Backoff multiplier for exponential backoff
    /// </summary>
    public double BackoffMultiplier { get; set; } = 2.0;
}
