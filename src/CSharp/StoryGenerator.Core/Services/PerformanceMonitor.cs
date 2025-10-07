using System.Diagnostics;
using System.Text.Json;
using Microsoft.Extensions.Logging;

namespace StoryGenerator.Core.Services;

/// <summary>
/// Performance monitoring and metrics tracking service.
/// Ported from Python Tools/Monitor.py with C# enhancements.
/// </summary>
public class PerformanceMonitor
{
    private readonly ILogger<PerformanceMonitor> _logger;
    private readonly string _metricsFilePath;

    public PerformanceMonitor(ILogger<PerformanceMonitor> logger, string? metricsDirectory = null)
    {
        _logger = logger;
        var metricsDir = metricsDirectory ?? Path.Combine(Directory.GetCurrentDirectory(), "logs");
        Directory.CreateDirectory(metricsDir);
        _metricsFilePath = Path.Combine(metricsDir, "metrics.json");
    }

    /// <summary>
    /// Logs a completed operation with metrics.
    /// </summary>
    /// <param name="operation">Operation name.</param>
    /// <param name="storyTitle">Story title.</param>
    /// <param name="duration">Duration in seconds.</param>
    /// <param name="success">Whether the operation succeeded.</param>
    /// <param name="error">Error message if operation failed.</param>
    /// <param name="metrics">Additional metrics.</param>
    public async Task LogOperationAsync(
        string operation,
        string storyTitle,
        double duration,
        bool success,
        string? error = null,
        Dictionary<string, object>? metrics = null)
    {
        var entry = new OperationEntry
        {
            Timestamp = DateTime.UtcNow,
            Operation = operation,
            StoryTitle = storyTitle,
            DurationSeconds = Math.Round(duration, 2),
            Success = success,
            Error = error,
            Metrics = metrics ?? new Dictionary<string, object>()
        };

        // Load existing metrics
        var allMetrics = await LoadMetricsAsync();
        allMetrics.Sessions.Add(entry);

        // Keep only last 1000 entries
        if (allMetrics.Sessions.Count > 1000)
        {
            allMetrics.Sessions = allMetrics.Sessions.Skip(allMetrics.Sessions.Count - 1000).ToList();
        }

        await SaveMetricsAsync(allMetrics);

        // Log to console/file
        var status = success ? "✅" : "❌";
        var message = $"{status} {operation} for '{storyTitle}' completed in {duration:F2}s";

        if (success)
        {
            _logger.LogInformation(message);
            if (metrics != null && metrics.Count > 0)
            {
                _logger.LogInformation("   Metrics: {Metrics}", JsonSerializer.Serialize(metrics));
            }
        }
        else
        {
            _logger.LogError("{Message} - Error: {Error}", message, error);
        }
    }

    /// <summary>
    /// Measures the execution time of an operation.
    /// </summary>
    /// <typeparam name="T">Return type of the operation.</typeparam>
    /// <param name="operationName">Name of the operation.</param>
    /// <param name="storyTitle">Story title.</param>
    /// <param name="operation">The operation to execute.</param>
    /// <param name="metrics">Optional metrics dictionary to populate.</param>
    /// <returns>Result of the operation.</returns>
    public async Task<T> MeasureAsync<T>(
        string operationName,
        string storyTitle,
        Func<Task<T>> operation,
        Dictionary<string, object>? metrics = null)
    {
        var stopwatch = Stopwatch.StartNew();
        var success = true;
        string? error = null;

        try
        {
            return await operation();
        }
        catch (Exception ex)
        {
            success = false;
            error = ex.Message;
            throw;
        }
        finally
        {
            stopwatch.Stop();
            await LogOperationAsync(
                operationName,
                storyTitle,
                stopwatch.Elapsed.TotalSeconds,
                success,
                error,
                metrics);
        }
    }

    /// <summary>
    /// Loads metrics from the JSON file.
    /// </summary>
    private async Task<MetricsData> LoadMetricsAsync()
    {
        if (!File.Exists(_metricsFilePath))
        {
            return new MetricsData();
        }

        try
        {
            var json = await File.ReadAllTextAsync(_metricsFilePath);
            return JsonSerializer.Deserialize<MetricsData>(json) ?? new MetricsData();
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Failed to load metrics from {FilePath}", _metricsFilePath);
            return new MetricsData();
        }
    }

    /// <summary>
    /// Saves metrics to the JSON file.
    /// </summary>
    private async Task SaveMetricsAsync(MetricsData metrics)
    {
        try
        {
            var options = new JsonSerializerOptions { WriteIndented = true };
            var json = JsonSerializer.Serialize(metrics, options);
            await File.WriteAllTextAsync(_metricsFilePath, json);
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Failed to save metrics to {FilePath}", _metricsFilePath);
        }
    }

    /// <summary>
    /// Gets a summary of recent performance metrics.
    /// </summary>
    public async Task<PerformanceSummary> GetPerformanceSummaryAsync()
    {
        var metrics = await LoadMetricsAsync();
        var sessions = metrics.Sessions;

        if (sessions.Count == 0)
        {
            return new PerformanceSummary { Message = "No metrics available" };
        }

        var totalOperations = sessions.Count;
        var successful = sessions.Count(s => s.Success);
        var failed = totalOperations - successful;

        var operationTypes = sessions
            .GroupBy(s => s.Operation)
            .ToDictionary(
                g => g.Key,
                g => new OperationStatistics
                {
                    Count = g.Count(),
                    TotalTime = g.Sum(s => s.DurationSeconds),
                    AverageTime = Math.Round(g.Average(s => s.DurationSeconds), 2),
                    Failures = g.Count(s => !s.Success)
                });

        return new PerformanceSummary
        {
            TotalOperations = totalOperations,
            Successful = successful,
            Failed = failed,
            SuccessRate = totalOperations > 0 ? Math.Round((double)successful / totalOperations * 100, 1) : 0,
            ByOperation = operationTypes
        };
    }
}

/// <summary>
/// Represents a single operation entry in the metrics log.
/// </summary>
public class OperationEntry
{
    public DateTime Timestamp { get; set; }
    public string Operation { get; set; } = string.Empty;
    public string StoryTitle { get; set; } = string.Empty;
    public double DurationSeconds { get; set; }
    public bool Success { get; set; }
    public string? Error { get; set; }
    public Dictionary<string, object> Metrics { get; set; } = new();
}

/// <summary>
/// Container for all metrics data.
/// </summary>
public class MetricsData
{
    public List<OperationEntry> Sessions { get; set; } = new();
}

/// <summary>
/// Summary of performance metrics.
/// </summary>
public class PerformanceSummary
{
    public string? Message { get; set; }
    public int TotalOperations { get; set; }
    public int Successful { get; set; }
    public int Failed { get; set; }
    public double SuccessRate { get; set; }
    public Dictionary<string, OperationStatistics> ByOperation { get; set; } = new();
}

/// <summary>
/// Statistics for a specific operation type.
/// </summary>
public class OperationStatistics
{
    public int Count { get; set; }
    public double TotalTime { get; set; }
    public double AverageTime { get; set; }
    public int Failures { get; set; }
}
