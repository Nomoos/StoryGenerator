using Microsoft.Data.Sqlite;
using Microsoft.Extensions.Options;
using PrismQ.Shared.Core;
using PrismQ.Shared.Core.Configuration;
using PrismQ.Shared.Interfaces;
using PrismQ.Shared.Models;

namespace StoryGenerator.Data;

/// <summary>
/// SQLite database implementation.
/// </summary>
public class SqliteDatabase : IDatabase
{
    private readonly DatabaseOptions _options;
    private readonly string _connectionString;

    /// <summary>
    /// Initializes a new instance of the <see cref="SqliteDatabase"/> class.
    /// </summary>
    /// <param name="options">Database options.</param>
    public SqliteDatabase(IOptions<DatabaseOptions> options)
    {
        _options = options.Value;
        _connectionString = _options.ConnectionString;
    }

    /// <inheritdoc/>
    public async Task<Result<bool>> InitializeAsync(CancellationToken cancellationToken = default)
    {
        try
        {
            using var connection = new SqliteConnection(_connectionString);
            await connection.OpenAsync(cancellationToken);

            if (_options.EnableMigrations)
            {
                await RunMigrationsAsync(connection, cancellationToken);
            }

            return Result<bool>.Success(true);
        }
        catch (Exception ex)
        {
            return Result<bool>.Failure($"Failed to initialize database: {ex.Message}");
        }
    }

    /// <inheritdoc/>
    public async Task<Result<IEnumerable<T>>> QueryAsync<T>(
        string sql,
        object? parameters = null,
        CancellationToken cancellationToken = default)
        where T : class
    {
        try
        {
            using var connection = new SqliteConnection(_connectionString);
            await connection.OpenAsync(cancellationToken);

            using var command = connection.CreateCommand();
            command.CommandText = sql;
            command.CommandTimeout = _options.CommandTimeoutSeconds;

            AddParameters(command, parameters);

            var results = new List<T>();
            using var reader = await command.ExecuteReaderAsync(cancellationToken);

            while (await reader.ReadAsync(cancellationToken))
            {
                var item = MapFromReader<T>(reader);
                results.Add(item);
            }

            return Result<IEnumerable<T>>.Success(results);
        }
        catch (Exception ex)
        {
            return Result<IEnumerable<T>>.Failure($"Query failed: {ex.Message}", ex);
        }
    }

    /// <inheritdoc/>
    public async Task<Result<int>> ExecuteAsync(
        string sql,
        object? parameters = null,
        CancellationToken cancellationToken = default)
    {
        try
        {
            using var connection = new SqliteConnection(_connectionString);
            await connection.OpenAsync(cancellationToken);

            using var command = connection.CreateCommand();
            command.CommandText = sql;
            command.CommandTimeout = _options.CommandTimeoutSeconds;

            AddParameters(command, parameters);

            var rowsAffected = await command.ExecuteNonQueryAsync(cancellationToken);
            return Result<int>.Success(rowsAffected);
        }
        catch (Exception ex)
        {
            return Result<int>.Failure($"Execute failed: {ex.Message}", ex);
        }
    }

    /// <inheritdoc/>
    public async Task<bool> HealthCheckAsync()
    {
        try
        {
            using var connection = new SqliteConnection(_connectionString);
            await connection.OpenAsync();
            return true;
        }
        catch
        {
            return false;
        }
    }

    private async Task RunMigrationsAsync(SqliteConnection connection, CancellationToken cancellationToken)
    {
        // Create version table
        var createVersionTable = @"
            CREATE TABLE IF NOT EXISTS schema_version (
                version INTEGER PRIMARY KEY,
                applied_at TEXT NOT NULL
            )";

        using var versionCmd = connection.CreateCommand();
        versionCmd.CommandText = createVersionTable;
        await versionCmd.ExecuteNonQueryAsync(cancellationToken);

        // Get current version
        using var getCurrentCmd = connection.CreateCommand();
        getCurrentCmd.CommandText = "SELECT COALESCE(MAX(version), 0) FROM schema_version";
        var currentVersion = Convert.ToInt32(await getCurrentCmd.ExecuteScalarAsync(cancellationToken));

        // Run migrations
        var migrations = GetMigrations();
        foreach (var (version, sql) in migrations.Where(m => m.version > currentVersion))
        {
            using var transaction = connection.BeginTransaction();
            try
            {
                using var migrationCmd = connection.CreateCommand();
                migrationCmd.CommandText = sql;
                await migrationCmd.ExecuteNonQueryAsync(cancellationToken);

                using var updateVersionCmd = connection.CreateCommand();
                updateVersionCmd.CommandText = "INSERT INTO schema_version (version, applied_at) VALUES ($version, $applied_at)";
                updateVersionCmd.Parameters.AddWithValue("$version", version);
                updateVersionCmd.Parameters.AddWithValue("$applied_at", DateTime.UtcNow.ToString("O"));
                await updateVersionCmd.ExecuteNonQueryAsync(cancellationToken);

                transaction.Commit();
            }
            catch
            {
                transaction.Rollback();
                throw;
            }
        }
    }

    private List<(int version, string sql)> GetMigrations()
    {
        return new List<(int, string)>
        {
            (1, @"
                CREATE TABLE IF NOT EXISTS jobs (
                    id TEXT PRIMARY KEY,
                    type TEXT NOT NULL,
                    status INTEGER NOT NULL,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL,
                    error_message TEXT,
                    metadata TEXT
                )
            ")
        };
    }

    private void AddParameters(SqliteCommand command, object? parameters)
    {
        if (parameters == null)
        {
            return;
        }

        foreach (var prop in parameters.GetType().GetProperties())
        {
            var value = prop.GetValue(parameters);
            command.Parameters.AddWithValue($"${prop.Name}", value ?? DBNull.Value);
        }
    }

    private T MapFromReader<T>(SqliteDataReader reader)
        where T : class
    {
        // Simple mapping for Job type
        if (typeof(T) == typeof(Models.Job))
        {
            var job = new Models.Job
            {
                Id = reader.GetString(reader.GetOrdinal("id")),
                Type = reader.GetString(reader.GetOrdinal("type")),
                Status = (JobStatus)reader.GetInt32(reader.GetOrdinal("status")),
                CreatedAt = DateTime.Parse(reader.GetString(reader.GetOrdinal("created_at"))),
                UpdatedAt = DateTime.Parse(reader.GetString(reader.GetOrdinal("updated_at"))),
                ErrorMessage = reader.IsDBNull(reader.GetOrdinal("error_message")) ? null : reader.GetString(reader.GetOrdinal("error_message")),
                Metadata = reader.IsDBNull(reader.GetOrdinal("metadata")) ? null : reader.GetString(reader.GetOrdinal("metadata"))
            };
            return (job as T)!;
        }

        throw new NotSupportedException($"Mapping for type {typeof(T).Name} is not supported");
    }
}
