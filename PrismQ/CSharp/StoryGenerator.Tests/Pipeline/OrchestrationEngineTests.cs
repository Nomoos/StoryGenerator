using StoryGenerator.Pipeline.Config;
using StoryGenerator.Pipeline.Core;
using StoryGenerator.Pipeline.Interfaces;
using Xunit;

namespace StoryGenerator.Tests.Pipeline;

/// <summary>
/// Tests for the orchestration engine
/// </summary>
public class OrchestrationEngineTests : IDisposable
{
    private readonly string _testDirectory;
    private readonly PipelineLogger _logger;
    private readonly OrchestrationEngine _engine;

    public OrchestrationEngineTests()
    {
        _testDirectory = Path.Combine(Path.GetTempPath(), $"test_orchestration_{Guid.NewGuid():N}");
        Directory.CreateDirectory(_testDirectory);

        var loggingConfig = new LoggingConfig
        {
            Level = "DEBUG",
            Console = false,
            File = ""
        };

        _logger = new PipelineLogger(loggingConfig);
        _engine = new OrchestrationEngine(_logger);
    }

    public void Dispose()
    {
        _logger?.Dispose();
        if (Directory.Exists(_testDirectory))
        {
            Directory.Delete(_testDirectory, true);
        }
    }

    [Fact]
    [Trait("Category", "Unit")]
    public void RegisterStage_WithValidStage_ShouldSucceed()
    {
        // Arrange
        var stage = new StageDefinition
        {
            Id = "test_stage",
            Name = "Test Stage",
            Order = 10,
            ExecuteFunc = async (ctx, ct) => await Task.CompletedTask
        };

        // Act
        _engine.RegisterStage(stage);

        // Assert
        var plan = _engine.GetExecutionPlan();
        Assert.Single(plan);
        Assert.Equal("test_stage", plan[0]);
    }

    [Fact]
    [Trait("Category", "Unit")]
    public void RegisterStage_WithDuplicateId_ShouldThrow()
    {
        // Arrange
        var stage1 = new StageDefinition
        {
            Id = "test_stage",
            Name = "Test Stage 1",
            Order = 10,
            ExecuteFunc = async (ctx, ct) => await Task.CompletedTask
        };

        var stage2 = new StageDefinition
        {
            Id = "test_stage",
            Name = "Test Stage 2",
            Order = 20,
            ExecuteFunc = async (ctx, ct) => await Task.CompletedTask
        };

        // Act & Assert
        _engine.RegisterStage(stage1);
        Assert.Throws<InvalidOperationException>(() => _engine.RegisterStage(stage2));
    }

    [Fact]
    [Trait("Category", "Unit")]
    public void RegisterStage_WithNullStage_ShouldThrow()
    {
        // Act & Assert
        Assert.Throws<ArgumentNullException>(() => _engine.RegisterStage(null!));
    }

    [Fact]
    [Trait("Category", "Unit")]
    public void RegisterStage_WithEmptyId_ShouldThrow()
    {
        // Arrange
        var stage = new StageDefinition
        {
            Id = "",
            Name = "Test Stage",
            ExecuteFunc = async (ctx, ct) => await Task.CompletedTask
        };

        // Act & Assert
        Assert.Throws<ArgumentException>(() => _engine.RegisterStage(stage));
    }

    [Fact]
    [Trait("Category", "Unit")]
    public void RegisterStage_WithNullExecuteFunc_ShouldThrow()
    {
        // Arrange
        var stage = new StageDefinition
        {
            Id = "test_stage",
            Name = "Test Stage",
            ExecuteFunc = null
        };

        // Act & Assert
        Assert.Throws<ArgumentException>(() => _engine.RegisterStage(stage));
    }

    [Fact]
    [Trait("Category", "Unit")]
    public void GetExecutionPlan_WithMultipleStages_ShouldReturnOrderedList()
    {
        // Arrange
        var stage1 = new StageDefinition
        {
            Id = "stage_3",
            Name = "Stage 3",
            Order = 30,
            ExecuteFunc = async (ctx, ct) => await Task.CompletedTask
        };

        var stage2 = new StageDefinition
        {
            Id = "stage_1",
            Name = "Stage 1",
            Order = 10,
            ExecuteFunc = async (ctx, ct) => await Task.CompletedTask
        };

        var stage3 = new StageDefinition
        {
            Id = "stage_2",
            Name = "Stage 2",
            Order = 20,
            ExecuteFunc = async (ctx, ct) => await Task.CompletedTask
        };

        // Act
        _engine.RegisterStage(stage1);
        _engine.RegisterStage(stage2);
        _engine.RegisterStage(stage3);

        var plan = _engine.GetExecutionPlan();

        // Assert
        Assert.Equal(3, plan.Count);
        Assert.Equal("stage_1", plan[0]);
        Assert.Equal("stage_2", plan[1]);
        Assert.Equal("stage_3", plan[2]);
    }

    [Fact]
    [Trait("Category", "Unit")]
    public void GetExecutionPlan_WithDisabledStages_ShouldExcludeDisabled()
    {
        // Arrange
        var stage1 = new StageDefinition
        {
            Id = "enabled_stage",
            Name = "Enabled Stage",
            Order = 10,
            Enabled = true,
            ExecuteFunc = async (ctx, ct) => await Task.CompletedTask
        };

        var stage2 = new StageDefinition
        {
            Id = "disabled_stage",
            Name = "Disabled Stage",
            Order = 20,
            Enabled = false,
            ExecuteFunc = async (ctx, ct) => await Task.CompletedTask
        };

        // Act
        _engine.RegisterStage(stage1);
        _engine.RegisterStage(stage2);

        var plan = _engine.GetExecutionPlan();

        // Assert
        Assert.Single(plan);
        Assert.Equal("enabled_stage", plan[0]);
    }

    [Fact]
    [Trait("Category", "Integration")]
    public async Task ExecuteAsync_WithSuccessfulStages_ShouldCompleteSuccessfully()
    {
        // Arrange
        var executionOrder = new List<string>();

        var stage1 = new StageDefinition
        {
            Id = "stage_1",
            Name = "Stage 1",
            Order = 10,
            ExecuteFunc = async (ctx, ct) =>
            {
                executionOrder.Add("stage_1");
                await Task.CompletedTask;
            }
        };

        var stage2 = new StageDefinition
        {
            Id = "stage_2",
            Name = "Stage 2",
            Order = 20,
            ExecuteFunc = async (ctx, ct) =>
            {
                executionOrder.Add("stage_2");
                await Task.CompletedTask;
            }
        };

        _engine.RegisterStage(stage1);
        _engine.RegisterStage(stage2);

        var context = new OrchestrationContext();

        // Act
        var result = await _engine.ExecuteAsync(context);

        // Assert
        Assert.True(result.Success);
        Assert.Equal(2, result.ExecutedStages.Count);
        Assert.Empty(result.FailedStages);
        Assert.Empty(result.SkippedStages);
        Assert.Equal(new[] { "stage_1", "stage_2" }, executionOrder);
    }

    [Fact]
    [Trait("Category", "Integration")]
    public async Task ExecuteAsync_WithFailingStage_ShouldReportFailure()
    {
        // Arrange
        var stage1 = new StageDefinition
        {
            Id = "success_stage",
            Name = "Success Stage",
            Order = 10,
            ExecuteFunc = async (ctx, ct) => await Task.CompletedTask
        };

        var stage2 = new StageDefinition
        {
            Id = "failing_stage",
            Name = "Failing Stage",
            Order = 20,
            MaxRetries = 0,
            ExecuteFunc = async (ctx, ct) =>
            {
                await Task.CompletedTask;
                throw new InvalidOperationException("Test failure");
            }
        };

        _engine.RegisterStage(stage1);
        _engine.RegisterStage(stage2);

        var context = new OrchestrationContext();

        // Act
        var result = await _engine.ExecuteAsync(context);

        // Assert
        Assert.False(result.Success);
        Assert.Single(result.ExecutedStages);
        Assert.Single(result.FailedStages);
        Assert.Equal("failing_stage", result.FailedStages[0]);
        Assert.NotNull(result.Exception);
    }

    [Fact]
    [Trait("Category", "Integration")]
    public async Task ExecuteAsync_WithContinueOnError_ShouldContinueAfterFailure()
    {
        // Arrange
        var executionOrder = new List<string>();

        var stage1 = new StageDefinition
        {
            Id = "stage_1",
            Name = "Stage 1",
            Order = 10,
            ContinueOnError = true,
            MaxRetries = 0,
            ExecuteFunc = async (ctx, ct) =>
            {
                executionOrder.Add("stage_1");
                await Task.CompletedTask;
                throw new InvalidOperationException("Stage 1 failed");
            }
        };

        var stage2 = new StageDefinition
        {
            Id = "stage_2",
            Name = "Stage 2",
            Order = 20,
            ExecuteFunc = async (ctx, ct) =>
            {
                executionOrder.Add("stage_2");
                await Task.CompletedTask;
            }
        };

        _engine.RegisterStage(stage1);
        _engine.RegisterStage(stage2);

        var context = new OrchestrationContext();

        // Act
        var result = await _engine.ExecuteAsync(context);

        // Assert
        Assert.True(result.Success); // Pipeline continues despite failure
        Assert.Single(result.ExecutedStages);
        Assert.Single(result.FailedStages);
        Assert.Equal(new[] { "stage_1", "stage_2" }, executionOrder);
    }

    [Fact]
    [Trait("Category", "Integration")]
    public async Task ExecuteAsync_WithCondition_ShouldSkipWhenConditionFalse()
    {
        // Arrange
        var executionOrder = new List<string>();

        var stage1 = new StageDefinition
        {
            Id = "stage_1",
            Name = "Stage 1",
            Order = 10,
            ExecuteFunc = async (ctx, ct) =>
            {
                executionOrder.Add("stage_1");
                await Task.CompletedTask;
            }
        };

        var stage2 = new StageDefinition
        {
            Id = "stage_2",
            Name = "Stage 2",
            Order = 20,
            Condition = ctx => false, // Always skip
            ExecuteFunc = async (ctx, ct) =>
            {
                executionOrder.Add("stage_2");
                await Task.CompletedTask;
            }
        };

        _engine.RegisterStage(stage1);
        _engine.RegisterStage(stage2);

        var context = new OrchestrationContext();

        // Act
        var result = await _engine.ExecuteAsync(context);

        // Assert
        Assert.True(result.Success);
        Assert.Single(result.ExecutedStages);
        Assert.Single(result.SkippedStages);
        Assert.Equal("stage_2", result.SkippedStages[0]);
        Assert.Equal(new[] { "stage_1" }, executionOrder);
    }

    [Fact]
    [Trait("Category", "Integration")]
    public async Task ExecuteAsync_WithRetry_ShouldRetryOnFailure()
    {
        // Arrange
        var attemptCount = 0;

        var stage = new StageDefinition
        {
            Id = "retry_stage",
            Name = "Retry Stage",
            Order = 10,
            MaxRetries = 2,
            RetryDelaySeconds = 0, // No delay for testing
            ExecuteFunc = async (ctx, ct) =>
            {
                attemptCount++;
                await Task.CompletedTask;
                if (attemptCount < 3)
                {
                    throw new InvalidOperationException("Retry test");
                }
            }
        };

        _engine.RegisterStage(stage);

        var context = new OrchestrationContext();

        // Act
        var result = await _engine.ExecuteAsync(context);

        // Assert
        Assert.True(result.Success);
        Assert.Equal(3, attemptCount); // Initial attempt + 2 retries
        Assert.Single(result.ExecutedStages);
    }

    [Fact]
    [Trait("Category", "Integration")]
    public async Task ExecuteAsync_WithLifecycleHooks_ShouldTriggerEvents()
    {
        // Arrange
        var startEvents = new List<string>();
        var completeEvents = new List<string>();
        var errorEvents = new List<string>();

        _engine.OnStageStart += (sender, args) => startEvents.Add(args.StageName);
        _engine.OnStageComplete += (sender, args) => completeEvents.Add(args.StageName);
        _engine.OnStageError += (sender, args) => errorEvents.Add(args.StageName);

        var stage1 = new StageDefinition
        {
            Id = "success_stage",
            Name = "Success Stage",
            Order = 10,
            ExecuteFunc = async (ctx, ct) => await Task.CompletedTask
        };

        var stage2 = new StageDefinition
        {
            Id = "error_stage",
            Name = "Error Stage",
            Order = 20,
            MaxRetries = 0,
            ContinueOnError = true,
            ExecuteFunc = async (ctx, ct) =>
            {
                await Task.CompletedTask;
                throw new InvalidOperationException("Test error");
            }
        };

        _engine.RegisterStage(stage1);
        _engine.RegisterStage(stage2);

        var context = new OrchestrationContext();

        // Act
        await _engine.ExecuteAsync(context);

        // Assert
        Assert.Equal(2, startEvents.Count);
        Assert.Single(completeEvents);
        Assert.Single(errorEvents);
        Assert.Equal("Success Stage", completeEvents[0]);
        Assert.Equal("Error Stage", errorEvents[0]);
    }

    [Fact]
    [Trait("Category", "Integration")]
    public async Task ExecuteAsync_WithCancellation_ShouldStopExecution()
    {
        // Arrange
        var executionOrder = new List<string>();
        var cts = new CancellationTokenSource();

        var stage1 = new StageDefinition
        {
            Id = "stage_1",
            Name = "Stage 1",
            Order = 10,
            ExecuteFunc = async (ctx, ct) =>
            {
                executionOrder.Add("stage_1");
                cts.Cancel(); // Cancel after first stage
                await Task.CompletedTask;
            }
        };

        var stage2 = new StageDefinition
        {
            Id = "stage_2",
            Name = "Stage 2",
            Order = 20,
            ExecuteFunc = async (ctx, ct) =>
            {
                executionOrder.Add("stage_2");
                await Task.CompletedTask;
            }
        };

        _engine.RegisterStage(stage1);
        _engine.RegisterStage(stage2);

        var context = new OrchestrationContext();

        // Act
        var result = await _engine.ExecuteAsync(context, cts.Token);

        // Assert
        Assert.False(result.Success);
        Assert.Single(executionOrder);
        Assert.Equal("stage_1", executionOrder[0]);
        Assert.Contains("cancelled", result.ErrorMessage?.ToLower());
    }
}
