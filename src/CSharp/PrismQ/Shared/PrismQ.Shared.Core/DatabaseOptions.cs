namespace PrismQ.Shared.Core.Configuration;

/// <summary>
/// Configuration options for database access.
/// </summary>
public class DatabaseOptions
{
    /// <summary>
    /// Database provider type.
    /// Supported values: "SQLite", "PostgreSQL"
    /// Default: "SQLite"
    /// </summary>
    public string Provider { get; set; } = "SQLite";

    /// <summary>
    /// Database connection string.
    /// Default: "Data Source=storygenerator.db"
    /// </summary>
    public string ConnectionString { get; set; } = "Data Source=storygenerator.db";

    /// <summary>
    /// Whether to automatically run migrations on startup.
    /// Default: true
    /// </summary>
    public bool EnableMigrations { get; set; } = true;

    /// <summary>
    /// Command timeout in seconds.
    /// Default: 30
    /// </summary>
    public int CommandTimeoutSeconds { get; set; } = 30;
}
