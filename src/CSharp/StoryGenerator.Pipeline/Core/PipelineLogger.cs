using StoryGenerator.Pipeline.Config;
using System.Diagnostics;

namespace StoryGenerator.Pipeline.Core;

/// <summary>
/// Pipeline logger with configurable output and performance metrics.
/// Implements IDisposable for proper resource cleanup.
/// </summary>
public class PipelineLogger : IDisposable
{
    private readonly LoggingConfig _config;
    private readonly StreamWriter? _fileWriter;
    private readonly Dictionary<string, Stopwatch> _timers = new();
    private readonly Dictionary<string, long> _metrics = new();
    private bool _disposed;

    public PipelineLogger(LoggingConfig config)
    {
        _config = config ?? throw new ArgumentNullException(nameof(config));
        
        if (!string.IsNullOrEmpty(config.File))
        {
            try
            {
                // Ensure directory exists
                var directory = Path.GetDirectoryName(config.File);
                if (!string.IsNullOrEmpty(directory) && !Directory.Exists(directory))
                {
                    Directory.CreateDirectory(directory);
                }

                _fileWriter = new StreamWriter(config.File, append: true)
                {
                    AutoFlush = true
                };
            }
            catch (Exception ex)
            {
                Console.WriteLine($"Warning: Failed to open log file: {ex.Message}");
            }
        }
    }

    public void LogInfo(string message)
    {
        Log("INFO", message);
    }

    public void LogWarning(string message)
    {
        Log("WARNING", message);
    }

    public void LogError(string message)
    {
        Log("ERROR", message);
    }

    public void LogDebug(string message)
    {
        if (_config.Level == "DEBUG")
        {
            Log("DEBUG", message);
        }
    }

    /// <summary>
    /// Start a performance timer for a named operation
    /// </summary>
    public void StartTimer(string name)
    {
        if (!_timers.ContainsKey(name))
        {
            _timers[name] = new Stopwatch();
        }
        _timers[name].Restart();
        LogDebug($"Timer started: {name}");
    }

    /// <summary>
    /// Stop a performance timer and log the elapsed time
    /// </summary>
    public TimeSpan StopTimer(string name)
    {
        if (!_timers.ContainsKey(name))
        {
            LogWarning($"Timer '{name}' was never started");
            return TimeSpan.Zero;
        }

        _timers[name].Stop();
        var elapsed = _timers[name].Elapsed;
        LogInfo($"Timer stopped: {name} - Elapsed: {elapsed.TotalSeconds:F2}s");
        
        // Store metric
        RecordMetric($"{name}_duration_ms", (long)elapsed.TotalMilliseconds);
        
        return elapsed;
    }

    /// <summary>
    /// Get elapsed time for a running timer
    /// </summary>
    public TimeSpan GetElapsedTime(string name)
    {
        if (!_timers.ContainsKey(name))
        {
            return TimeSpan.Zero;
        }
        return _timers[name].Elapsed;
    }

    /// <summary>
    /// Record a numeric metric
    /// </summary>
    public void RecordMetric(string name, long value)
    {
        _metrics[name] = value;
        LogDebug($"Metric recorded: {name} = {value}");
    }

    /// <summary>
    /// Get all recorded metrics
    /// </summary>
    public IReadOnlyDictionary<string, long> GetMetrics()
    {
        return _metrics;
    }

    /// <summary>
    /// Log performance summary with all metrics
    /// </summary>
    public void LogPerformanceSummary()
    {
        if (_metrics.Count == 0)
        {
            LogInfo("No performance metrics recorded");
            return;
        }

        LogInfo("=== Performance Summary ===");
        foreach (var metric in _metrics.OrderBy(m => m.Key))
        {
            LogInfo($"  {metric.Key}: {metric.Value}");
        }
        LogInfo("=========================");
    }

    private void Log(string level, string message)
    {
        var timestamp = DateTime.Now.ToString("yyyy-MM-dd HH:mm:ss");
        var formattedMessage = _config.Format
            .Replace("{timestamp}", timestamp)
            .Replace("{level}", level)
            .Replace("{message}", message);

        if (_config.Console)
        {
            // Add color for console output
            var originalColor = Console.ForegroundColor;
            Console.ForegroundColor = level switch
            {
                "ERROR" => ConsoleColor.Red,
                "WARNING" => ConsoleColor.Yellow,
                "INFO" => ConsoleColor.White,
                "DEBUG" => ConsoleColor.Gray,
                _ => ConsoleColor.White
            };
            Console.WriteLine(formattedMessage);
            Console.ForegroundColor = originalColor;
        }

        _fileWriter?.WriteLine(formattedMessage);
    }

    public void Dispose()
    {
        Dispose(true);
        GC.SuppressFinalize(this);
    }

    protected virtual void Dispose(bool disposing)
    {
        if (_disposed)
        {
            return;
        }

        if (disposing)
        {
            _fileWriter?.Dispose();
        }

        _disposed = true;
    }
}
