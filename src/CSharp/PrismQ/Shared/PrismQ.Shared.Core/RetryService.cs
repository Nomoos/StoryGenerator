using Microsoft.Extensions.Logging;
using Polly;
using Polly.Retry;

namespace PrismQ.Shared.Core.Services;

/// <summary>
/// Retry service with exponential backoff and circuit breaker patterns.
/// Ported from Python Tools/Retry.py with Polly integration.
/// </summary>
public class RetryService
{
    private readonly ILogger<RetryService> _logger;
    private readonly Dictionary<string, ResiliencePipeline> _circuitBreakers = new();

    public RetryService(ILogger<RetryService> logger)
    {
        _logger = logger;
    }

    /// <summary>
    /// Creates a retry policy with exponential backoff.
    /// </summary>
    /// <param name="maxRetries">Maximum number of retry attempts.</param>
    /// <param name="baseDelay">Base delay in seconds.</param>
    /// <param name="maxDelay">Maximum delay in seconds.</param>
    /// <returns>Retry policy.</returns>
    public ResiliencePipeline<T> CreateRetryPolicy<T>(
        int maxRetries = 3,
        double baseDelay = 2.0,
        double maxDelay = 30.0)
    {
        return new ResiliencePipelineBuilder<T>()
            .AddRetry(new RetryStrategyOptions<T>
            {
                MaxRetryAttempts = maxRetries,
                Delay = TimeSpan.FromSeconds(baseDelay),
                BackoffType = DelayBackoffType.Exponential,
                MaxDelay = TimeSpan.FromSeconds(maxDelay),
                OnRetry = args =>
                {
                    _logger.LogWarning(
                        "Retry attempt {AttemptNumber} after {Delay}ms due to: {Exception}",
                        args.AttemptNumber,
                        args.RetryDelay.TotalMilliseconds,
                        args.Outcome.Exception?.Message);
                    return ValueTask.CompletedTask;
                }
            })
            .Build();
    }

    /// <summary>
    /// Executes an operation with retry logic.
    /// </summary>
    /// <typeparam name="T">Return type.</typeparam>
    /// <param name="operation">Operation to execute.</param>
    /// <param name="maxRetries">Maximum number of retry attempts.</param>
    /// <param name="baseDelay">Base delay in seconds.</param>
    /// <param name="maxDelay">Maximum delay in seconds.</param>
    /// <returns>Result of the operation.</returns>
    public async Task<T> ExecuteWithRetryAsync<T>(
        Func<Task<T>> operation,
        int maxRetries = 3,
        double baseDelay = 2.0,
        double maxDelay = 30.0)
    {
        var policy = CreateRetryPolicy<T>(maxRetries, baseDelay, maxDelay);
        return await policy.ExecuteAsync(async _ => await operation(), CancellationToken.None);
    }

    /// <summary>
    /// Executes an operation with circuit breaker pattern.
    /// </summary>
    /// <typeparam name="T">Return type.</typeparam>
    /// <param name="circuitBreakerName">Name of the circuit breaker (e.g., "openai", "elevenlabs").</param>
    /// <param name="operation">Operation to execute.</param>
    /// <returns>Result of the operation.</returns>
    public async Task<T> ExecuteWithCircuitBreakerAsync<T>(
        string circuitBreakerName,
        Func<Task<T>> operation)
    {
        if (!_circuitBreakers.TryGetValue(circuitBreakerName, out var pipeline))
        {
            pipeline = CreateCircuitBreakerPipeline(circuitBreakerName);
            _circuitBreakers[circuitBreakerName] = pipeline;
        }

        return await pipeline.ExecuteAsync<T>(async _ => await operation(), CancellationToken.None);
    }

    /// <summary>
    /// Creates a circuit breaker pipeline for a specific service.
    /// </summary>
    private ResiliencePipeline CreateCircuitBreakerPipeline(string serviceName)
    {
        return new ResiliencePipelineBuilder()
            .AddCircuitBreaker(new Polly.CircuitBreaker.CircuitBreakerStrategyOptions
            {
                FailureRatio = 0.5,
                SamplingDuration = TimeSpan.FromSeconds(30),
                MinimumThroughput = 3,
                BreakDuration = TimeSpan.FromSeconds(60),
                OnOpened = args =>
                {
                    _logger.LogError(
                        "Circuit breaker '{ServiceName}' opened due to failures",
                        serviceName);
                    return ValueTask.CompletedTask;
                },
                OnClosed = args =>
                {
                    _logger.LogInformation(
                        "Circuit breaker '{ServiceName}' closed - service recovered",
                        serviceName);
                    return ValueTask.CompletedTask;
                },
                OnHalfOpened = args =>
                {
                    _logger.LogInformation(
                        "Circuit breaker '{ServiceName}' half-opened - testing service",
                        serviceName);
                    return ValueTask.CompletedTask;
                }
            })
            .Build();
    }

    /// <summary>
    /// Executes an operation with both retry and circuit breaker patterns.
    /// </summary>
    /// <typeparam name="T">Return type.</typeparam>
    /// <param name="circuitBreakerName">Name of the circuit breaker.</param>
    /// <param name="operation">Operation to execute.</param>
    /// <param name="maxRetries">Maximum number of retry attempts.</param>
    /// <param name="baseDelay">Base delay in seconds.</param>
    /// <param name="maxDelay">Maximum delay in seconds.</param>
    /// <returns>Result of the operation.</returns>
    public async Task<T> ExecuteWithRetryAndCircuitBreakerAsync<T>(
        string circuitBreakerName,
        Func<Task<T>> operation,
        int maxRetries = 3,
        double baseDelay = 2.0,
        double maxDelay = 30.0)
    {
        return await ExecuteWithCircuitBreakerAsync(
            circuitBreakerName,
            () => ExecuteWithRetryAsync(operation, maxRetries, baseDelay, maxDelay));
    }
}
