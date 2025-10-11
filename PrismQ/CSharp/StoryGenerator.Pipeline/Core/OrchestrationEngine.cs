using StoryGenerator.Pipeline.Config;
using StoryGenerator.Pipeline.Interfaces;
using System.Diagnostics;

namespace StoryGenerator.Pipeline.Core;

/// <summary>
/// Core orchestration engine that coordinates pipeline stages with lifecycle hooks,
/// error handling, and retry logic.
/// </summary>
public class OrchestrationEngine : IOrchestrationEngine
{
    private readonly List<StageDefinition> _stages = new();
    private readonly PipelineLogger _logger;
    private readonly ErrorHandlingConfig _errorHandlingConfig;

    /// <inheritdoc/>
    public event EventHandler<StageLifecycleEventArgs>? OnStageStart;

    /// <inheritdoc/>
    public event EventHandler<StageLifecycleEventArgs>? OnStageComplete;

    /// <inheritdoc/>
    public event EventHandler<StageErrorEventArgs>? OnStageError;

    public OrchestrationEngine(
        PipelineLogger logger,
        ErrorHandlingConfig? errorHandlingConfig = null)
    {
        _logger = logger ?? throw new ArgumentNullException(nameof(logger));
        _errorHandlingConfig = errorHandlingConfig ?? new ErrorHandlingConfig
        {
            ContinueOnError = false,
            RetryCount = 3,
            RetryDelay = 5
        };
    }

    /// <inheritdoc/>
    public void RegisterStage(StageDefinition stageDefinition)
    {
        if (stageDefinition == null)
        {
            throw new ArgumentNullException(nameof(stageDefinition));
        }

        if (string.IsNullOrWhiteSpace(stageDefinition.Id))
        {
            throw new ArgumentException("Stage ID cannot be empty", nameof(stageDefinition));
        }

        if (stageDefinition.ExecuteFunc == null)
        {
            throw new ArgumentException("Stage ExecuteFunc cannot be null", nameof(stageDefinition));
        }

        if (_stages.Any(s => s.Id == stageDefinition.Id))
        {
            throw new InvalidOperationException($"Stage with ID '{stageDefinition.Id}' is already registered");
        }

        _stages.Add(stageDefinition);
        _logger.LogDebug($"Registered stage: {stageDefinition.Id} (Order: {stageDefinition.Order})");
    }

    /// <inheritdoc/>
    public IReadOnlyList<string> GetExecutionPlan()
    {
        return _stages
            .Where(s => s.Enabled)
            .OrderBy(s => s.Order)
            .Select(s => s.Id)
            .ToList();
    }

    /// <inheritdoc/>
    public async Task<OrchestrationResult> ExecuteAsync(
        OrchestrationContext context,
        CancellationToken cancellationToken = default)
    {
        var result = new OrchestrationResult { Success = true };
        var overallStopwatch = Stopwatch.StartNew();

        _logger.LogInfo("=== Starting Pipeline Orchestration ===");
        _logger.LogInfo($"Registered stages: {_stages.Count}");

        var orderedStages = _stages
            .Where(s => s.Enabled)
            .OrderBy(s => s.Order)
            .ToList();

        _logger.LogInfo($"Enabled stages: {orderedStages.Count}");
        _logger.LogInfo(new string('=', 80));

        foreach (var stage in orderedStages)
        {
            if (cancellationToken.IsCancellationRequested)
            {
                _logger.LogWarning("Pipeline execution cancelled");
                result.Success = false;
                result.ErrorMessage = "Pipeline execution was cancelled";
                break;
            }

            // Check condition
            if (stage.Condition != null && !stage.Condition(context))
            {
                _logger.LogInfo($"⏭️  Skipping stage: {stage.Name} (condition not met)");
                result.SkippedStages.Add(stage.Id);
                continue;
            }

            // Execute stage with retry logic
            var stageExecuted = await ExecuteStageWithRetryAsync(
                stage,
                context,
                result,
                cancellationToken);

            if (!stageExecuted && !stage.ContinueOnError && !_errorHandlingConfig.ContinueOnError)
            {
                // Stage failed and we should not continue
                result.Success = false;
                result.ErrorMessage = $"Stage '{stage.Name}' failed and ContinueOnError is false";
                _logger.LogError($"Pipeline halted due to stage failure: {stage.Name}");
                break;
            }
        }

        overallStopwatch.Stop();
        result.TotalDuration = overallStopwatch.Elapsed;

        _logger.LogInfo(new string('=', 80));
        _logger.LogInfo("=== Pipeline Orchestration Complete ===");
        _logger.LogInfo($"Success: {result.Success}");
        _logger.LogInfo($"Executed: {result.ExecutedStages.Count}, Skipped: {result.SkippedStages.Count}, Failed: {result.FailedStages.Count}");
        _logger.LogInfo($"Total Duration: {result.TotalDuration.TotalSeconds:F2}s");
        
        if (!string.IsNullOrEmpty(result.ErrorMessage))
        {
            _logger.LogError($"Error: {result.ErrorMessage}");
        }

        return result;
    }

    private async Task<bool> ExecuteStageWithRetryAsync(
        StageDefinition stage,
        OrchestrationContext context,
        OrchestrationResult result,
        CancellationToken cancellationToken)
    {
        // Use stage-specific retries if set (even if 0), otherwise use global config
        var maxRetries = stage.MaxRetries >= 0 ? stage.MaxRetries : _errorHandlingConfig.RetryCount;
        var retryDelay = stage.RetryDelaySeconds > 0 ? stage.RetryDelaySeconds : _errorHandlingConfig.RetryDelay;

        // Fire OnStageStart event once at the beginning
        var startEventArgs = new StageLifecycleEventArgs
        {
            StageName = stage.Name,
            Timestamp = DateTime.Now,
            Context = new Dictionary<string, object>
            {
                ["Id"] = stage.Id,
                ["Order"] = stage.Order
            }
        };
        OnStageStart?.Invoke(this, startEventArgs);

        for (int attempt = 0; attempt <= maxRetries; attempt++)
        {
            try
            {
                _logger.StartTimer(stage.Id);
                _logger.LogInfo($"\n▶️  Executing stage: {stage.Name}");
                if (attempt > 0)
                {
                    _logger.LogInfo($"   (Retry attempt {attempt} of {maxRetries})");
                }

                // Execute the stage
                await stage.ExecuteFunc!(context, cancellationToken);

                var elapsed = _logger.StopTimer(stage.Id);

                // Fire OnStageComplete event
                var completeEventArgs = new StageLifecycleEventArgs
                {
                    StageName = stage.Name,
                    Timestamp = DateTime.Now,
                    Context = new Dictionary<string, object>
                    {
                        ["Id"] = stage.Id,
                        ["Duration"] = elapsed,
                        ["Attempt"] = attempt
                    }
                };
                OnStageComplete?.Invoke(this, completeEventArgs);

                _logger.LogInfo($"✅ Stage completed: {stage.Name} ({elapsed.TotalSeconds:F2}s)");
                result.ExecutedStages.Add(stage.Id);
                return true;
            }
            catch (Exception ex)
            {
                _logger.StopTimer(stage.Id);

                var willRetry = attempt < maxRetries;
                
                // Fire OnStageError event
                var errorEventArgs = new StageErrorEventArgs
                {
                    StageName = stage.Name,
                    Timestamp = DateTime.Now,
                    Exception = ex,
                    WillRetry = willRetry,
                    RetryAttempt = attempt,
                    Context = new Dictionary<string, object>
                    {
                        ["Id"] = stage.Id,
                        ["MaxRetries"] = maxRetries
                    }
                };
                OnStageError?.Invoke(this, errorEventArgs);

                if (willRetry)
                {
                    _logger.LogWarning($"⚠️  Stage failed: {stage.Name} - {ex.Message}");
                    _logger.LogWarning($"   Retrying in {retryDelay}s... (Attempt {attempt + 1}/{maxRetries})");
                    await Task.Delay(TimeSpan.FromSeconds(retryDelay), cancellationToken);
                }
                else
                {
                    _logger.LogError($"❌ Stage failed: {stage.Name} - {ex.Message}");
                    _logger.LogDebug($"   Stack trace: {ex.StackTrace}");
                    result.FailedStages.Add(stage.Id);
                    
                    if (result.Exception == null)
                    {
                        result.Exception = ex;
                    }
                    
                    return false;
                }
            }
        }

        return false;
    }
}
