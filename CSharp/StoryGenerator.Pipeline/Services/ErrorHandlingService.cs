using StoryGenerator.Pipeline.Config;
using StoryGenerator.Pipeline.Core;

namespace StoryGenerator.Pipeline.Services;

/// <summary>
/// Provides error handling and retry logic for pipeline operations.
/// Implements retry policies with exponential backoff and circuit breaker pattern.
/// </summary>
public class ErrorHandlingService
{
    private readonly ProcessingConfig _config;
    private readonly PipelineLogger _logger;
    private readonly Dictionary<string, CircuitBreakerState> _circuitBreakers = new();
    private readonly SemaphoreSlim _lock = new(1, 1);

    public ErrorHandlingService(ProcessingConfig config, PipelineLogger logger)
    {
        _config = config ?? throw new ArgumentNullException(nameof(config));
        _logger = logger ?? throw new ArgumentNullException(nameof(logger));
    }

    /// <summary>
    /// Execute an operation with retry logic
    /// </summary>
    public async Task<T> ExecuteWithRetryAsync<T>(
        string operationName,
        Func<Task<T>> operation,
        CancellationToken cancellationToken = default)
    {
        if (operation == null)
        {
            throw new ArgumentNullException(nameof(operation));
        }

        // Check circuit breaker
        if (IsCircuitOpen(operationName))
        {
            throw new InvalidOperationException($"Circuit breaker is open for operation: {operationName}");
        }

        int attempts = 0;
        int maxAttempts = _config.ErrorHandling.RetryCount + 1; // +1 for initial attempt
        Exception? lastException = null;

        while (attempts < maxAttempts)
        {
            attempts++;
            try
            {
                _logger.LogDebug($"Attempting operation '{operationName}' (attempt {attempts}/{maxAttempts})");
                var result = await operation();
                
                // Success - reset circuit breaker
                RecordSuccess(operationName);
                return result;
            }
            catch (Exception ex) when (IsRetriableException(ex))
            {
                lastException = ex;
                _logger.LogWarning($"Operation '{operationName}' failed (attempt {attempts}/{maxAttempts}): {ex.Message}");

                if (attempts < maxAttempts)
                {
                    // Calculate delay with exponential backoff
                    var delay = CalculateRetryDelay(attempts);
                    _logger.LogDebug($"Retrying in {delay.TotalSeconds:F1}s...");
                    await Task.Delay(delay, cancellationToken);
                }
                else
                {
                    // Max attempts reached - record failure
                    RecordFailure(operationName);
                }
            }
            catch (Exception ex)
            {
                // Non-retriable exception
                _logger.LogError($"Operation '{operationName}' failed with non-retriable error: {ex.Message}");
                RecordFailure(operationName);
                throw;
            }
        }

        // All retries exhausted
        throw new InvalidOperationException(
            $"Operation '{operationName}' failed after {attempts} attempts",
            lastException);
    }

    /// <summary>
    /// Execute an operation without retry (fire-and-forget style)
    /// </summary>
    public async Task ExecuteWithoutRetryAsync(
        string operationName,
        Func<Task> operation)
    {
        if (operation == null)
        {
            throw new ArgumentNullException(nameof(operation));
        }

        try
        {
            _logger.LogDebug($"Executing operation '{operationName}' (no retry)");
            await operation();
            RecordSuccess(operationName);
        }
        catch (Exception ex)
        {
            _logger.LogError($"Operation '{operationName}' failed: {ex.Message}");
            RecordFailure(operationName);
            throw;
        }
    }

    /// <summary>
    /// Check if an exception is retriable
    /// </summary>
    private bool IsRetriableException(Exception ex)
    {
        // Network-related exceptions are typically retriable
        if (ex is HttpRequestException || ex is TaskCanceledException || ex is TimeoutException)
        {
            return true;
        }

        // IO exceptions might be retriable
        if (ex is IOException)
        {
            return true;
        }

        // Check inner exception
        if (ex.InnerException != null)
        {
            return IsRetriableException(ex.InnerException);
        }

        return false;
    }

    /// <summary>
    /// Calculate retry delay with exponential backoff
    /// </summary>
    private TimeSpan CalculateRetryDelay(int attemptNumber)
    {
        var baseDelay = TimeSpan.FromSeconds(_config.ErrorHandling.RetryDelay);
        
        // Exponential backoff: delay * 2^(attempt-1)
        var exponentialDelay = baseDelay * Math.Pow(2, attemptNumber - 1);
        
        // Cap at maximum delay
        var maxDelay = TimeSpan.FromSeconds(_config.ErrorHandling.RetryDelay * 10);
        return exponentialDelay > maxDelay ? maxDelay : exponentialDelay;
    }

    /// <summary>
    /// Record a successful operation
    /// </summary>
    private void RecordSuccess(string operationName)
    {
        _lock.Wait();
        try
        {
            if (_circuitBreakers.ContainsKey(operationName))
            {
                var state = _circuitBreakers[operationName];
                state.FailureCount = 0;
                state.LastFailureTime = null;
                
                if (state.IsOpen)
                {
                    _logger.LogInfo($"Circuit breaker closed for operation: {operationName}");
                    state.IsOpen = false;
                }
            }
        }
        finally
        {
            _lock.Release();
        }
    }

    /// <summary>
    /// Record a failed operation
    /// </summary>
    private void RecordFailure(string operationName)
    {
        _lock.Wait();
        try
        {
            if (!_circuitBreakers.ContainsKey(operationName))
            {
                _circuitBreakers[operationName] = new CircuitBreakerState();
            }

            var state = _circuitBreakers[operationName];
            state.FailureCount++;
            state.LastFailureTime = DateTime.Now;

            // Open circuit if threshold reached
            if (state.FailureCount >= 5 && !state.IsOpen)
            {
                _logger.LogWarning($"Circuit breaker opened for operation: {operationName}");
                state.IsOpen = true;
            }
        }
        finally
        {
            _lock.Release();
        }
    }

    /// <summary>
    /// Check if circuit breaker is open
    /// </summary>
    private bool IsCircuitOpen(string operationName)
    {
        _lock.Wait();
        try
        {
            if (!_circuitBreakers.ContainsKey(operationName))
            {
                return false;
            }

            var state = _circuitBreakers[operationName];
            
            // If circuit is open, check if enough time has passed to try again
            if (state.IsOpen && state.LastFailureTime.HasValue)
            {
                var timeSinceFailure = DateTime.Now - state.LastFailureTime.Value;
                if (timeSinceFailure > TimeSpan.FromMinutes(5))
                {
                    _logger.LogInfo($"Circuit breaker half-open for operation: {operationName}");
                    state.IsOpen = false;
                    state.FailureCount = 0;
                    return false;
                }
            }

            return state.IsOpen;
        }
        finally
        {
            _lock.Release();
        }
    }

    /// <summary>
    /// Circuit breaker state for an operation
    /// </summary>
    private class CircuitBreakerState
    {
        public int FailureCount { get; set; }
        public DateTime? LastFailureTime { get; set; }
        public bool IsOpen { get; set; }
    }
}
