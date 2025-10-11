using PrismQ.Shared.Core;
using PrismQ.Shared.Interfaces;
using PrismQ.Shared.Models;
using StoryGenerator.Data.Models;

namespace StoryGenerator.Data.Repositories;

/// <summary>
/// Repository for Job CRUD operations.
/// </summary>
public class JobRepository
{
    private readonly IDatabase _database;

    /// <summary>
    /// Initializes a new instance of the <see cref="JobRepository"/> class.
    /// </summary>
    /// <param name="database">Database instance.</param>
    public JobRepository(IDatabase database)
    {
        _database = database;
    }

    /// <summary>
    /// Creates a new job in the database.
    /// </summary>
    /// <param name="job">Job to create.</param>
    /// <param name="cancellationToken">Cancellation token.</param>
    /// <returns>Result of the create operation.</returns>
    public async Task<Result<Job>> CreateAsync(Job job, CancellationToken cancellationToken = default)
    {
        job.CreatedAt = DateTime.UtcNow;
        job.UpdatedAt = DateTime.UtcNow;

        var sql = @"
            INSERT INTO jobs (id, type, status, created_at, updated_at, error_message, metadata)
            VALUES ($Id, $Type, $Status, $CreatedAt, $UpdatedAt, $ErrorMessage, $Metadata)";

        var result = await _database.ExecuteAsync(sql, new
        {
            job.Id,
            job.Type,
            Status = (int)job.Status,
            CreatedAt = job.CreatedAt.ToString("O"),
            UpdatedAt = job.UpdatedAt.ToString("O"),
            job.ErrorMessage,
            job.Metadata
        }, cancellationToken);

        return result.IsSuccess
            ? Result<Job>.Success(job)
            : Result<Job>.Failure(result.Error ?? "Failed to create job");
    }

    /// <summary>
    /// Gets a job by ID.
    /// </summary>
    /// <param name="id">Job ID.</param>
    /// <param name="cancellationToken">Cancellation token.</param>
    /// <returns>Result containing the job if found.</returns>
    public async Task<Result<Job?>> GetByIdAsync(string id, CancellationToken cancellationToken = default)
    {
        var sql = "SELECT * FROM jobs WHERE id = $Id";
        var result = await _database.QueryAsync<Job>(sql, new { Id = id }, cancellationToken);

        if (!result.IsSuccess)
        {
            return Result<Job?>.Failure(result.Error ?? "Failed to get job");
        }

        var job = result.Value?.FirstOrDefault();
        return Result<Job?>.Success(job);
    }

    /// <summary>
    /// Gets all jobs.
    /// </summary>
    /// <param name="cancellationToken">Cancellation token.</param>
    /// <returns>Result containing all jobs.</returns>
    public async Task<Result<IEnumerable<Job>>> GetAllAsync(CancellationToken cancellationToken = default)
    {
        var sql = "SELECT * FROM jobs ORDER BY created_at DESC";
        return await _database.QueryAsync<Job>(sql, null, cancellationToken);
    }

    /// <summary>
    /// Updates a job.
    /// </summary>
    /// <param name="job">Job to update.</param>
    /// <param name="cancellationToken">Cancellation token.</param>
    /// <returns>Result of the update operation.</returns>
    public async Task<Result<Job>> UpdateAsync(Job job, CancellationToken cancellationToken = default)
    {
        job.UpdatedAt = DateTime.UtcNow;

        var sql = @"
            UPDATE jobs
            SET type = $Type,
                status = $Status,
                updated_at = $UpdatedAt,
                error_message = $ErrorMessage,
                metadata = $Metadata
            WHERE id = $Id";

        var result = await _database.ExecuteAsync(sql, new
        {
            job.Id,
            job.Type,
            Status = (int)job.Status,
            UpdatedAt = job.UpdatedAt.ToString("O"),
            job.ErrorMessage,
            job.Metadata
        }, cancellationToken);

        return result.IsSuccess && result.Value > 0
            ? Result<Job>.Success(job)
            : Result<Job>.Failure("Job not found or update failed");
    }

    /// <summary>
    /// Deletes a job by ID.
    /// </summary>
    /// <param name="id">Job ID.</param>
    /// <param name="cancellationToken">Cancellation token.</param>
    /// <returns>Result indicating if the delete was successful.</returns>
    public async Task<Result<bool>> DeleteAsync(string id, CancellationToken cancellationToken = default)
    {
        var sql = "DELETE FROM jobs WHERE id = $Id";
        var result = await _database.ExecuteAsync(sql, new { Id = id }, cancellationToken);

        return result.IsSuccess && result.Value > 0
            ? Result<bool>.Success(true)
            : Result<bool>.Failure("Job not found or delete failed");
    }

    /// <summary>
    /// Gets jobs by status.
    /// </summary>
    /// <param name="status">Job status to filter by.</param>
    /// <param name="cancellationToken">Cancellation token.</param>
    /// <returns>Result containing jobs with the specified status.</returns>
    public async Task<Result<IEnumerable<Job>>> GetByStatusAsync(JobStatus status, CancellationToken cancellationToken = default)
    {
        var sql = "SELECT * FROM jobs WHERE status = $Status ORDER BY created_at DESC";
        return await _database.QueryAsync<Job>(sql, new { Status = (int)status }, cancellationToken);
    }
}
