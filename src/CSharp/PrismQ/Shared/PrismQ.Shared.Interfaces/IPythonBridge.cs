namespace PrismQ.Shared.Interfaces;

/// <summary>
/// Bridge for communicating with Python scripts via subprocess.
/// </summary>
public interface IPythonBridge
{
    /// <summary>
    /// Executes a Python operation via JSONL protocol.
    /// </summary>
    /// <typeparam name="TRequest">Request type.</typeparam>
    /// <typeparam name="TResponse">Response type.</typeparam>
    /// <param name="scriptName">Name of the Python script (e.g., "whisper_asr.py").</param>
    /// <param name="operation">Operation name (e.g., "asr.transcribe").</param>
    /// <param name="args">Operation arguments.</param>
    /// <param name="cancellationToken">Cancellation token.</param>
    /// <returns>Result containing the response data.</returns>
    Task<Result<TResponse>> ExecuteAsync<TRequest, TResponse>(
        string scriptName,
        string operation,
        TRequest args,
        CancellationToken cancellationToken = default)
        where TRequest : class
        where TResponse : class;

    /// <summary>
    /// Checks if the Python environment is properly configured.
    /// </summary>
    /// <returns>True if Python is available and configured.</returns>
    Task<bool> IsAvailableAsync();
}
