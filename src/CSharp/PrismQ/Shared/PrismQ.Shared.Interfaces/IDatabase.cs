using PrismQ.Shared.Models;

namespace PrismQ.Shared.Interfaces;

/// <summary>
/// Database abstraction for managing connections and operations.
/// </summary>
public interface IDatabase
{
    /// <summary>
    /// Initializes the database and runs migrations if enabled.
    /// </summary>
    /// <param name="cancellationToken">Cancellation token.</param>
    /// <returns>Result of initialization.</returns>
    Task<Result<bool>> InitializeAsync(CancellationToken cancellationToken = default);

    /// <summary>
    /// Executes a SQL query and returns a list of results.
    /// </summary>
    /// <typeparam name="T">Result type.</typeparam>
    /// <param name="sql">SQL query.</param>
    /// <param name="parameters">Query parameters.</param>
    /// <param name="cancellationToken">Cancellation token.</param>
    /// <returns>List of results.</returns>
    Task<Result<IEnumerable<T>>> QueryAsync<T>(
        string sql,
        object? parameters = null,
        CancellationToken cancellationToken = default)
        where T : class;

    /// <summary>
    /// Executes a SQL command that doesn't return results.
    /// </summary>
    /// <param name="sql">SQL command.</param>
    /// <param name="parameters">Command parameters.</param>
    /// <param name="cancellationToken">Cancellation token.</param>
    /// <returns>Number of rows affected.</returns>
    Task<Result<int>> ExecuteAsync(
        string sql,
        object? parameters = null,
        CancellationToken cancellationToken = default);

    /// <summary>
    /// Checks if the database connection is healthy.
    /// </summary>
    /// <returns>True if connection is healthy.</returns>
    Task<bool> HealthCheckAsync();
}
