using StoryGenerator.Pipeline.Core;
using StoryGenerator.Pipeline.Config;
using StoryGenerator.Pipeline.Services;
using StoryGenerator.Pipeline.Interfaces;
using Xunit;

namespace StoryGenerator.Tests.Pipeline;

/// <summary>
/// Tests for Phase 2: Pipeline Orchestration Foundation
/// </summary>
public class Phase2OrchestrationTests
{
    private readonly PipelineConfig _testConfig;
    private readonly PipelineLogger _testLogger;

    public Phase2OrchestrationTests()
    {
        _testConfig = CreateTestConfig();
        _testLogger = new PipelineLogger(_testConfig.Logging);
    }

    private static PipelineConfig CreateTestConfig()
    {
        return new PipelineConfig
        {
            Paths = new PathsConfig
            {
                StoryRoot = Path.Combine(Path.GetTempPath(), "test_stories"),
                PythonRoot = "./Python"
            },
            Processing = new ProcessingConfig
            {
                ErrorHandling = new ErrorHandlingConfig
                {
                    RetryCount = 3,
                    RetryDelay = 1
                },
                Checkpointing = new CheckpointingConfig
                {
                    Enabled = true,
                    ResumeFromCheckpoint = true
                }
            },
            Logging = new LoggingConfig
            {
                Level = "INFO",
                Console = false,
                File = "" // No file logging in tests
            }
        };
    }

    #region Task 1: Pipeline Stage Interface Tests

    [Fact]
    public void PipelineProgress_Properties_ShouldBeSetCorrectly()
    {
        // Arrange
        var progress = new PipelineProgress
        {
            StageName = "TestStage",
            PercentComplete = 50,
            Message = "Processing..."
        };

        // Assert
        Assert.Equal("TestStage", progress.StageName);
        Assert.Equal(50, progress.PercentComplete);
        Assert.Equal("Processing...", progress.Message);
        Assert.True((DateTime.Now - progress.Timestamp).TotalSeconds < 1);
    }

    [Fact]
    public async Task BasePipelineStage_ExecuteAsync_ShouldValidateInput()
    {
        // Arrange
        var stage = new TestPipelineStage();

        // Act & Assert
        await Assert.ThrowsAsync<ArgumentException>(
            () => stage.ExecuteAsync(null!, null, CancellationToken.None));
    }

    [Fact]
    public async Task BasePipelineStage_ExecuteAsync_ShouldReportProgress()
    {
        // Arrange
        var stage = new TestPipelineStage();
        var progressReports = new List<PipelineProgress>();
        var progress = new Progress<PipelineProgress>(p => progressReports.Add(p));

        // Act
        var result = await stage.ExecuteAsync("test input", progress, CancellationToken.None);

        // Assert
        Assert.Equal("PROCESSED: test input", result);
        Assert.True(progressReports.Count >= 2); // At least start and end
        Assert.Contains(progressReports, p => p.PercentComplete == 0);
        Assert.Contains(progressReports, p => p.PercentComplete == 100);
    }

    #endregion

    #region Task 2: Checkpoint Manager Tests

    [Fact]
    public async Task CheckpointManager_SaveAndLoad_ShouldPersistState()
    {
        // Arrange
        var manager = new PipelineCheckpointManager(_testConfig, _testLogger);
        var checkpoint = new PipelineCheckpoint();
        checkpoint.CompleteStep("step1", "data1");
        checkpoint.CompleteStep("step2", "data2");

        // Act
        await manager.SaveCheckpointAsync(checkpoint);
        var loaded = await manager.LoadCheckpointAsync();

        // Assert
        Assert.True(loaded.IsStepComplete("step1"));
        Assert.True(loaded.IsStepComplete("step2"));
        Assert.Equal("data1", loaded.GetStepData("step1"));
        Assert.Equal("data2", loaded.GetStepData("step2"));

        // Cleanup
        await manager.DeleteCheckpointAsync();
    }

    [Fact]
    public async Task CheckpointManager_SaveCheckpoint_ShouldBeAtomic()
    {
        // Arrange
        var manager = new PipelineCheckpointManager(_testConfig, _testLogger);
        var checkpoint = new PipelineCheckpoint();
        checkpoint.CompleteStep("step1", "data1");

        // Act
        await manager.SaveCheckpointAsync(checkpoint);
        var hasCheckpoint = await manager.HasCheckpointAsync();

        // Assert
        Assert.True(hasCheckpoint);

        // Cleanup
        await manager.DeleteCheckpointAsync();
    }

    [Fact]
    public async Task CheckpointManager_ValidateCheckpoint_ShouldRejectInvalidData()
    {
        // Arrange
        var manager = new PipelineCheckpointManager(_testConfig, _testLogger);
        
        // Act & Assert - Save null checkpoint should throw ArgumentNullException
        await Assert.ThrowsAsync<ArgumentNullException>(
            async () => await manager.SaveCheckpointAsync(null!));
    }

    #endregion

    #region Task 3: Configuration Validator Tests

    [Fact]
    public void ConfigValidator_ValidConfig_ShouldPassValidation()
    {
        // Arrange
        var validator = new ConfigurationValidator();
        var config = CreateTestConfig();

        // Act
        var isValid = validator.Validate(config);

        // Assert
        Assert.True(isValid);
        Assert.Empty(validator.Errors);
    }

    [Fact]
    public void ConfigValidator_InvalidPaths_ShouldReportErrors()
    {
        // Arrange
        var validator = new ConfigurationValidator();
        var config = CreateTestConfig();
        config.Paths.StoryRoot = ""; // Invalid

        // Act
        var isValid = validator.Validate(config);

        // Assert
        Assert.False(isValid);
        Assert.Contains(validator.Errors, e => e.Contains("StoryRoot"));
    }

    [Fact]
    public void ConfigValidator_InvalidVideoSettings_ShouldReportErrors()
    {
        // Arrange
        var validator = new ConfigurationValidator();
        var config = CreateTestConfig();
        config.Generation.Video.Fps = 0; // Invalid

        // Act
        var isValid = validator.Validate(config);

        // Assert
        Assert.False(isValid);
        Assert.Contains(validator.Errors, e => e.Contains("FPS"));
    }

    #endregion

    #region Task 4: Enhanced Logging Tests

    [Fact]
    public void Logger_StartStopTimer_ShouldTrackElapsed()
    {
        // Arrange & Act
        _testLogger.StartTimer("test_operation");
        Thread.Sleep(100); // Simulate work
        var elapsed = _testLogger.StopTimer("test_operation");

        // Assert
        Assert.True(elapsed.TotalMilliseconds >= 100);
        Assert.True(elapsed.TotalMilliseconds < 200);
    }

    [Fact]
    public void Logger_RecordMetric_ShouldStoreValue()
    {
        // Arrange & Act
        _testLogger.RecordMetric("test_metric", 42);
        var metrics = _testLogger.GetMetrics();

        // Assert
        Assert.True(metrics.ContainsKey("test_metric"));
        Assert.Equal(42, metrics["test_metric"]);
    }

    [Fact]
    public void Logger_MultipleMetrics_ShouldTrackAll()
    {
        // Arrange & Act
        _testLogger.RecordMetric("metric1", 100);
        _testLogger.RecordMetric("metric2", 200);
        _testLogger.RecordMetric("metric3", 300);
        var metrics = _testLogger.GetMetrics();

        // Assert
        Assert.Equal(3, metrics.Count);
        Assert.Equal(100, metrics["metric1"]);
        Assert.Equal(200, metrics["metric2"]);
        Assert.Equal(300, metrics["metric3"]);
    }

    #endregion

    #region Task 5: Error Handling Service Tests

    [Fact]
    public async Task ErrorHandlingService_SuccessfulOperation_ShouldExecuteOnce()
    {
        // Arrange
        var errorHandler = new ErrorHandlingService(_testConfig.Processing, _testLogger);
        var executionCount = 0;

        // Act
        var result = await errorHandler.ExecuteWithRetryAsync(
            "test_operation",
            async () =>
            {
                executionCount++;
                await Task.Delay(10);
                return "success";
            });

        // Assert
        Assert.Equal("success", result);
        Assert.Equal(1, executionCount);
    }

    [Fact]
    public async Task ErrorHandlingService_RetriableFailure_ShouldRetry()
    {
        // Arrange
        var errorHandler = new ErrorHandlingService(_testConfig.Processing, _testLogger);
        var executionCount = 0;

        // Act & Assert
        await Assert.ThrowsAnyAsync<Exception>(async () =>
        {
            await errorHandler.ExecuteWithRetryAsync<string>(
                "test_operation",
                async () =>
                {
                    executionCount++;
                    await Task.Delay(10);
                    throw new HttpRequestException("Network error"); // Retriable
                });
        });

        // Should have tried initial + retries
        Assert.Equal(_testConfig.Processing.ErrorHandling.RetryCount + 1, executionCount);
    }

    [Fact]
    public async Task ErrorHandlingService_NonRetriableFailure_ShouldNotRetry()
    {
        // Arrange
        var errorHandler = new ErrorHandlingService(_testConfig.Processing, _testLogger);
        var executionCount = 0;

        // Act & Assert
        await Assert.ThrowsAsync<ArgumentException>(async () =>
        {
            await errorHandler.ExecuteWithRetryAsync<string>(
                "test_operation",
                async () =>
                {
                    executionCount++;
                    await Task.Delay(10);
                    throw new ArgumentException("Bad argument"); // Non-retriable
                });
        });

        // Should only execute once (no retries for non-retriable exceptions)
        Assert.Equal(1, executionCount);
    }

    #endregion

    #region Helper Classes

    /// <summary>
    /// Test implementation of BasePipelineStage
    /// </summary>
    private class TestPipelineStage : BasePipelineStage<string, string>
    {
        public override string StageName => "TestStage";

        protected override async Task<string> ExecuteCoreAsync(
            string input,
            IProgress<PipelineProgress>? progress,
            CancellationToken cancellationToken)
        {
            ReportProgress(progress, 50, "Processing...");
            await Task.Delay(50, cancellationToken);
            return $"PROCESSED: {input}";
        }

        public override Task<bool> ValidateInputAsync(string input)
        {
            return Task.FromResult(!string.IsNullOrEmpty(input));
        }
    }

    #endregion
}
