using Microsoft.Extensions.Options;
using StoryGenerator.Core.Configuration;
using StoryGenerator.Core.Interfaces;
using StoryGenerator.Data;
using StoryGenerator.Data.Models;
using StoryGenerator.Data.Repositories;
using Xunit;

namespace StoryGenerator.Tests.Data;

/// <summary>
/// Tests for JobRepository CRUD operations.
/// </summary>
public class JobRepositoryTests : IDisposable
{
    private readonly IDatabase _database;
    private readonly JobRepository _repository;
    private readonly string _testDbPath;

    public JobRepositoryTests()
    {
        _testDbPath = Path.Combine(Path.GetTempPath(), $"test_{Guid.NewGuid()}.db");
        var options = Options.Create(new DatabaseOptions
        {
            ConnectionString = $"Data Source={_testDbPath}",
            EnableMigrations = true
        });

        _database = new SqliteDatabase(options);
        _database.InitializeAsync().Wait();
        _repository = new JobRepository(_database);
    }

    public void Dispose()
    {
        if (File.Exists(_testDbPath))
        {
            File.Delete(_testDbPath);
        }
    }

    [Fact]
    public async Task CreateAsync_ShouldCreateJob()
    {
        // Arrange
        var job = new Job
        {
            Id = Guid.NewGuid().ToString(),
            Type = "TestJob",
            Status = JobStatus.Created
        };

        // Act
        var result = await _repository.CreateAsync(job);

        // Assert
        Assert.True(result.IsSuccess);
        Assert.NotNull(result.Value);
        Assert.Equal(job.Id, result.Value.Id);
        Assert.Equal(job.Type, result.Value.Type);
        Assert.Equal(JobStatus.Created, result.Value.Status);
    }

    [Fact]
    public async Task GetByIdAsync_ShouldReturnJob_WhenExists()
    {
        // Arrange
        var job = new Job
        {
            Id = Guid.NewGuid().ToString(),
            Type = "TestJob",
            Status = JobStatus.Created
        };
        await _repository.CreateAsync(job);

        // Act
        var result = await _repository.GetByIdAsync(job.Id);

        // Assert
        Assert.True(result.IsSuccess);
        Assert.NotNull(result.Value);
        Assert.Equal(job.Id, result.Value.Id);
    }

    [Fact]
    public async Task GetByIdAsync_ShouldReturnNull_WhenNotExists()
    {
        // Act
        var result = await _repository.GetByIdAsync("nonexistent-id");

        // Assert
        Assert.True(result.IsSuccess);
        Assert.Null(result.Value);
    }

    [Fact]
    public async Task UpdateAsync_ShouldUpdateJob()
    {
        // Arrange
        var job = new Job
        {
            Id = Guid.NewGuid().ToString(),
            Type = "TestJob",
            Status = JobStatus.Created
        };
        await _repository.CreateAsync(job);

        // Act
        job.Status = JobStatus.Running;
        job.ErrorMessage = "Test error";
        var result = await _repository.UpdateAsync(job);

        // Assert
        Assert.True(result.IsSuccess);
        
        var retrieved = await _repository.GetByIdAsync(job.Id);
        Assert.Equal(JobStatus.Running, retrieved.Value!.Status);
        Assert.Equal("Test error", retrieved.Value.ErrorMessage);
    }

    [Fact]
    public async Task DeleteAsync_ShouldDeleteJob()
    {
        // Arrange
        var job = new Job
        {
            Id = Guid.NewGuid().ToString(),
            Type = "TestJob",
            Status = JobStatus.Created
        };
        await _repository.CreateAsync(job);

        // Act
        var deleteResult = await _repository.DeleteAsync(job.Id);

        // Assert
        Assert.True(deleteResult.IsSuccess);
        Assert.True(deleteResult.Value);

        var getResult = await _repository.GetByIdAsync(job.Id);
        Assert.Null(getResult.Value);
    }

    [Fact]
    public async Task GetAllAsync_ShouldReturnAllJobs()
    {
        // Arrange
        var job1 = new Job { Id = Guid.NewGuid().ToString(), Type = "Job1", Status = JobStatus.Created };
        var job2 = new Job { Id = Guid.NewGuid().ToString(), Type = "Job2", Status = JobStatus.Running };
        await _repository.CreateAsync(job1);
        await _repository.CreateAsync(job2);

        // Act
        var result = await _repository.GetAllAsync();

        // Assert
        Assert.True(result.IsSuccess);
        Assert.Equal(2, result.Value!.Count());
    }

    [Fact]
    public async Task GetByStatusAsync_ShouldFilterByStatus()
    {
        // Arrange
        var job1 = new Job { Id = Guid.NewGuid().ToString(), Type = "Job1", Status = JobStatus.Created };
        var job2 = new Job { Id = Guid.NewGuid().ToString(), Type = "Job2", Status = JobStatus.Running };
        var job3 = new Job { Id = Guid.NewGuid().ToString(), Type = "Job3", Status = JobStatus.Created };
        await _repository.CreateAsync(job1);
        await _repository.CreateAsync(job2);
        await _repository.CreateAsync(job3);

        // Act
        var result = await _repository.GetByStatusAsync(JobStatus.Created);

        // Assert
        Assert.True(result.IsSuccess);
        Assert.Equal(2, result.Value!.Count());
        Assert.All(result.Value, job => Assert.Equal(JobStatus.Created, job.Status));
    }
}
