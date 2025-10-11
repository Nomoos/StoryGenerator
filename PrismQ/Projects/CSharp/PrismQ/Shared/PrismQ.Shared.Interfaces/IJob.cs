namespace PrismQ.Shared.Interfaces;

/// <summary>
/// Represents a job that can be executed in the pipeline.
/// </summary>
public interface IJob
{
    /// <summary>
    /// Unique identifier for the job.
    /// </summary>
    string Id { get; }

    /// <summary>
    /// Job type or name.
    /// </summary>
    string Type { get; }

    /// <summary>
    /// Current status of the job.
    /// </summary>
    JobStatus Status { get; set; }

    /// <summary>
    /// Timestamp when the job was created.
    /// </summary>
    DateTime CreatedAt { get; }

    /// <summary>
    /// Timestamp when the job was last updated.
    /// </summary>
    DateTime UpdatedAt { get; set; }

    /// <summary>
    /// Error message if the job failed.
    /// </summary>
    string? ErrorMessage { get; set; }
}

/// <summary>
/// Job status enumeration.
/// </summary>
public enum JobStatus
{
    /// <summary>
    /// Job has been created but not started.
    /// </summary>
    Created = 0,

    /// <summary>
    /// Job is currently running.
    /// </summary>
    Running = 1,

    /// <summary>
    /// Job completed successfully.
    /// </summary>
    Succeeded = 2,

    /// <summary>
    /// Job failed with an error.
    /// </summary>
    Failed = 3,

    /// <summary>
    /// Job was cancelled.
    /// </summary>
    Cancelled = 4
}
