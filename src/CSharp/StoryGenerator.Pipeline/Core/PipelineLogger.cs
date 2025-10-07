using StoryGenerator.Pipeline.Config;

namespace StoryGenerator.Pipeline.Core;

/// <summary>
/// Pipeline logger with configurable output.
/// Implements IDisposable for proper resource cleanup.
/// </summary>
public class PipelineLogger : IDisposable
{
    private readonly LoggingConfig _config;
    private readonly StreamWriter? _fileWriter;
    private bool _disposed;

    public PipelineLogger(LoggingConfig config)
    {
        _config = config;
        
        if (!string.IsNullOrEmpty(config.File))
        {
            try
            {
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
