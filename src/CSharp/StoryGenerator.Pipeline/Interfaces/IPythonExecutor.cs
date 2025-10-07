namespace StoryGenerator.Pipeline.Interfaces;

/// <summary>
/// Executes Python scripts and commands.
/// Follows Single Responsibility Principle - only handles Python execution.
/// Abstracts away Python execution details from the pipeline logic.
/// </summary>
public interface IPythonExecutor
{
    /// <summary>
    /// Execute a Python script file
    /// </summary>
    /// <param name="scriptPath">Path to the Python script</param>
    /// <param name="arguments">Command-line arguments to pass to the script</param>
    /// <param name="cancellationToken">Cancellation token</param>
    /// <returns>Output from the script</returns>
    Task<string> ExecuteScriptAsync(string scriptPath, string arguments, CancellationToken cancellationToken = default);

    /// <summary>
    /// Execute a Python command (using -c flag)
    /// </summary>
    /// <param name="command">Python code to execute</param>
    /// <param name="cancellationToken">Cancellation token</param>
    /// <returns>Output from the command</returns>
    Task<string> ExecuteCommandAsync(string command, CancellationToken cancellationToken = default);
}
