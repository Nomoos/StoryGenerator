using System.Diagnostics;
using System.Text;
using StoryGenerator.Pipeline.Config;
using StoryGenerator.Pipeline.Core;
using StoryGenerator.Pipeline.Interfaces;

namespace StoryGenerator.Pipeline.Services;

/// <summary>
/// Executes Python scripts and commands.
/// Implements Single Responsibility Principle - only handles Python execution.
/// </summary>
public class PythonExecutor : IPythonExecutor
{
    private readonly PipelineConfig _config;
    private readonly PipelineLogger _logger;
    private readonly string _pythonExecutable;

    public PythonExecutor(PipelineConfig config, PipelineLogger logger)
    {
        _config = config ?? throw new ArgumentNullException(nameof(config));
        _logger = logger ?? throw new ArgumentNullException(nameof(logger));
        _pythonExecutable = FindPythonExecutable();
    }

    /// <inheritdoc/>
    public async Task<string> ExecuteScriptAsync(string scriptPath, string arguments, CancellationToken cancellationToken = default)
    {
        if (string.IsNullOrWhiteSpace(scriptPath))
        {
            throw new ArgumentException("Script path cannot be empty", nameof(scriptPath));
        }

        if (!File.Exists(scriptPath))
        {
            throw new FileNotFoundException($"Python script not found: {scriptPath}");
        }

        var args = $"\"{scriptPath}\" {arguments}";
        return await ExecutePythonAsync(args, cancellationToken);
    }

    /// <inheritdoc/>
    public async Task<string> ExecuteCommandAsync(string command, CancellationToken cancellationToken = default)
    {
        if (string.IsNullOrWhiteSpace(command))
        {
            throw new ArgumentException("Command cannot be empty", nameof(command));
        }

        var args = $"-c \"{command}\"";
        return await ExecutePythonAsync(args, cancellationToken);
    }

    private async Task<string> ExecutePythonAsync(string arguments, CancellationToken cancellationToken)
    {
        var process = new Process
        {
            StartInfo = new ProcessStartInfo
            {
                FileName = _pythonExecutable,
                Arguments = arguments,
                WorkingDirectory = _config.Paths.PythonRoot,
                UseShellExecute = false,
                RedirectStandardOutput = true,
                RedirectStandardError = true,
                CreateNoWindow = true
            }
        };

        var outputBuilder = new StringBuilder();
        var errorBuilder = new StringBuilder();

        process.OutputDataReceived += (sender, e) =>
        {
            if (!string.IsNullOrEmpty(e.Data))
            {
                outputBuilder.AppendLine(e.Data);
                _logger.LogInfo($"  {e.Data}");
            }
        };

        process.ErrorDataReceived += (sender, e) =>
        {
            if (!string.IsNullOrEmpty(e.Data))
            {
                errorBuilder.AppendLine(e.Data);
                _logger.LogWarning($"  {e.Data}");
            }
        };

        _logger.LogDebug($"Executing: {_pythonExecutable} {arguments}");
        
        process.Start();
        process.BeginOutputReadLine();
        process.BeginErrorReadLine();
        
        await process.WaitForExitAsync(cancellationToken);

        if (process.ExitCode != 0 && !_config.Processing.ErrorHandling.ContinueOnError)
        {
            var errorMessage = errorBuilder.ToString();
            throw new InvalidOperationException(
                $"Python execution failed with exit code {process.ExitCode}\n{errorMessage}");
        }

        return outputBuilder.ToString();
    }

    private string FindPythonExecutable()
    {
        var candidates = new[] { "python3", "python", "py" };
        
        foreach (var candidate in candidates)
        {
            try
            {
                var process = Process.Start(new ProcessStartInfo
                {
                    FileName = candidate,
                    Arguments = "--version",
                    UseShellExecute = false,
                    RedirectStandardOutput = true,
                    CreateNoWindow = true
                });

                if (process != null)
                {
                    process.WaitForExit();
                    if (process.ExitCode == 0)
                    {
                        _logger.LogDebug($"Found Python executable: {candidate}");
                        return candidate;
                    }
                }
            }
            catch
            {
                // Try next candidate
            }
        }

        throw new InvalidOperationException(
            "Python executable not found. Please ensure Python is installed and in PATH.");
    }
}
