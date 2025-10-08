namespace StoryGenerator.Core.Configuration;

/// <summary>
/// Configuration options for Python script execution.
/// </summary>
public class PythonOptions
{
    /// <summary>
    /// Path to the Python interpreter executable.
    /// Default: "python3"
    /// </summary>
    public string InterpreterPath { get; set; } = "python3";

    /// <summary>
    /// Path to the Python scripts directory.
    /// Default: "../../scripts"
    /// </summary>
    public string ScriptsPath { get; set; } = "../../scripts";

    /// <summary>
    /// Timeout for Python script execution in seconds.
    /// Default: 300 (5 minutes)
    /// </summary>
    public int TimeoutSeconds { get; set; } = 300;

    /// <summary>
    /// Maximum number of concurrent Python processes.
    /// Default: 4
    /// </summary>
    public int MaxConcurrentProcesses { get; set; } = 4;
}
