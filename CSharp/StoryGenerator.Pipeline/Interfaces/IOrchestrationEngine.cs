namespace StoryGenerator.Pipeline.Interfaces;

/// <summary>
/// Represents lifecycle hook arguments for stage events
/// </summary>
public class StageLifecycleEventArgs
{
    /// <summary>
    /// Name of the stage
    /// </summary>
    public string StageName { get; set; } = string.Empty;

    /// <summary>
    /// Timestamp of the event
    /// </summary>
    public DateTime Timestamp { get; set; } = DateTime.Now;

    /// <summary>
    /// Additional context data
    /// </summary>
    public Dictionary<string, object> Context { get; set; } = new();
}

/// <summary>
/// Represents error information for stage failure events
/// </summary>
public class StageErrorEventArgs : StageLifecycleEventArgs
{
    /// <summary>
    /// The exception that occurred
    /// </summary>
    public Exception? Exception { get; set; }

    /// <summary>
    /// Whether the stage will be retried
    /// </summary>
    public bool WillRetry { get; set; }

    /// <summary>
    /// Retry attempt number (0 for first attempt)
    /// </summary>
    public int RetryAttempt { get; set; }
}

/// <summary>
/// Core orchestration engine interface for coordinating pipeline stages.
/// Provides lifecycle hooks and manages stage execution flow.
/// </summary>
public interface IOrchestrationEngine
{
    /// <summary>
    /// Event fired when a stage is about to start
    /// </summary>
    event EventHandler<StageLifecycleEventArgs>? OnStageStart;

    /// <summary>
    /// Event fired when a stage completes successfully
    /// </summary>
    event EventHandler<StageLifecycleEventArgs>? OnStageComplete;

    /// <summary>
    /// Event fired when a stage encounters an error
    /// </summary>
    event EventHandler<StageErrorEventArgs>? OnStageError;

    /// <summary>
    /// Register a stage for execution
    /// </summary>
    /// <param name="stageDefinition">The stage definition to register</param>
    void RegisterStage(StageDefinition stageDefinition);

    /// <summary>
    /// Execute all registered stages in order
    /// </summary>
    /// <param name="context">Execution context</param>
    /// <param name="cancellationToken">Cancellation token</param>
    /// <returns>Execution results</returns>
    Task<OrchestrationResult> ExecuteAsync(
        OrchestrationContext context,
        CancellationToken cancellationToken = default);

    /// <summary>
    /// Get the execution plan (stages in order)
    /// </summary>
    /// <returns>List of stage names in execution order</returns>
    IReadOnlyList<string> GetExecutionPlan();
}

/// <summary>
/// Defines a stage to be executed by the orchestration engine
/// </summary>
public class StageDefinition
{
    /// <summary>
    /// Unique identifier for the stage
    /// </summary>
    public string Id { get; set; } = string.Empty;

    /// <summary>
    /// Display name for the stage
    /// </summary>
    public string Name { get; set; } = string.Empty;

    /// <summary>
    /// Order in which the stage should execute (lower numbers execute first)
    /// </summary>
    public int Order { get; set; }

    /// <summary>
    /// Whether this stage is enabled
    /// </summary>
    public bool Enabled { get; set; } = true;

    /// <summary>
    /// Condition that must be true for the stage to execute
    /// </summary>
    public Func<OrchestrationContext, bool>? Condition { get; set; }

    /// <summary>
    /// The actual stage execution function
    /// </summary>
    public Func<OrchestrationContext, CancellationToken, Task>? ExecuteFunc { get; set; }

    /// <summary>
    /// Whether to continue pipeline execution if this stage fails
    /// </summary>
    public bool ContinueOnError { get; set; }

    /// <summary>
    /// Maximum number of retry attempts (0 = no retries)
    /// </summary>
    public int MaxRetries { get; set; }

    /// <summary>
    /// Delay between retry attempts in seconds
    /// </summary>
    public int RetryDelaySeconds { get; set; } = 5;
}

/// <summary>
/// Context passed to stages during orchestration
/// </summary>
public class OrchestrationContext
{
    /// <summary>
    /// Shared data between stages
    /// </summary>
    public Dictionary<string, object> Data { get; set; } = new();

    /// <summary>
    /// Configuration for the pipeline
    /// </summary>
    public object? Configuration { get; set; }

    /// <summary>
    /// Get data from context
    /// </summary>
    public T? GetData<T>(string key)
    {
        if (Data.TryGetValue(key, out var value) && value is T typedValue)
        {
            return typedValue;
        }
        return default;
    }

    /// <summary>
    /// Set data in context
    /// </summary>
    public void SetData<T>(string key, T value)
    {
        if (value != null)
        {
            Data[key] = value;
        }
    }
}

/// <summary>
/// Result of orchestration execution
/// </summary>
public class OrchestrationResult
{
    /// <summary>
    /// Whether the orchestration completed successfully
    /// </summary>
    public bool Success { get; set; }

    /// <summary>
    /// Stages that were executed
    /// </summary>
    public List<string> ExecutedStages { get; set; } = new();

    /// <summary>
    /// Stages that were skipped
    /// </summary>
    public List<string> SkippedStages { get; set; } = new();

    /// <summary>
    /// Stages that failed
    /// </summary>
    public List<string> FailedStages { get; set; } = new();

    /// <summary>
    /// Total execution time
    /// </summary>
    public TimeSpan TotalDuration { get; set; }

    /// <summary>
    /// Error message if orchestration failed
    /// </summary>
    public string? ErrorMessage { get; set; }

    /// <summary>
    /// Exception if orchestration failed
    /// </summary>
    public Exception? Exception { get; set; }
}
