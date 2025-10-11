using StoryGenerator.Pipeline.Core;
using StoryGenerator.Pipeline.Config;
using StoryGenerator.Pipeline.Services;
using Xunit;

namespace StoryGenerator.Tests.Pipeline;

/// <summary>
/// Integration tests for Phase 4: Pipeline Orchestration
/// Tests checkpoint management, resume functionality, and error recovery
/// </summary>
public class Phase4IntegrationTests : IDisposable
{
    private readonly string _testDirectory;
    private readonly PipelineConfig _testConfig;
    private readonly PipelineLogger _testLogger;
    private readonly PipelineCheckpointManager _checkpointManager;

    public Phase4IntegrationTests()
    {
        // Create a unique test directory for each test
        _testDirectory = Path.Combine(Path.GetTempPath(), $"test_phase4_{Guid.NewGuid():N}");
        Directory.CreateDirectory(_testDirectory);

        _testConfig = CreateTestConfig(_testDirectory);
        _testLogger = new PipelineLogger(_testConfig.Logging);
        _checkpointManager = new PipelineCheckpointManager(_testConfig, _testLogger);
    }

    public void Dispose()
    {
        // Clean up test directory
        if (Directory.Exists(_testDirectory))
        {
            Directory.Delete(_testDirectory, true);
        }
    }

    private static PipelineConfig CreateTestConfig(string testDirectory)
    {
        return new PipelineConfig
        {
            Paths = new PathsConfig
            {
                StoryRoot = testDirectory,
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

    #region Checkpoint Management Tests

    [Fact]
    [Trait("Category", "Integration")]
    public async Task CheckpointManager_SaveAndLoad_ShouldPersistCheckpoint()
    {
        // Arrange
        var checkpoint = new PipelineCheckpoint();
        checkpoint.CompleteStep("story_idea", "TestStory");
        checkpoint.CompleteStep("script_generation", "TestStory");

        // Act - Save checkpoint
        await _checkpointManager.SaveCheckpointAsync(checkpoint);

        // Assert - Checkpoint file exists
        var checkpointPath = Path.Combine(_testDirectory, "pipeline_checkpoint.json");
        Assert.True(File.Exists(checkpointPath), "Checkpoint file should exist after save");

        // Act - Load checkpoint
        var loadedCheckpoint = await _checkpointManager.LoadCheckpointAsync();

        // Assert - Loaded checkpoint matches saved checkpoint
        Assert.True(loadedCheckpoint.IsStepComplete("story_idea"));
        Assert.True(loadedCheckpoint.IsStepComplete("script_generation"));
        Assert.Equal("TestStory", loadedCheckpoint.GetStepData("story_idea"));
        Assert.Equal("TestStory", loadedCheckpoint.GetStepData("script_generation"));
    }

    [Fact]
    [Trait("Category", "Integration")]
    public async Task CheckpointManager_SaveMultipleTimes_ShouldUpdateCheckpoint()
    {
        // Arrange
        var checkpoint1 = new PipelineCheckpoint();
        checkpoint1.CompleteStep("story_idea", "TestStory");

        // Act - Save first checkpoint
        await _checkpointManager.SaveCheckpointAsync(checkpoint1);
        var firstSaveTime = checkpoint1.LastUpdated;

        // Wait a bit to ensure different timestamp
        await Task.Delay(100);

        // Update checkpoint with another step
        checkpoint1.CompleteStep("script_generation", "TestStory");

        // Act - Save updated checkpoint
        await _checkpointManager.SaveCheckpointAsync(checkpoint1);

        // Act - Load checkpoint
        var loadedCheckpoint = await _checkpointManager.LoadCheckpointAsync();

        // Assert - Both steps are present
        Assert.True(loadedCheckpoint.IsStepComplete("story_idea"));
        Assert.True(loadedCheckpoint.IsStepComplete("script_generation"));
        Assert.True(loadedCheckpoint.LastUpdated > firstSaveTime);
    }

    [Fact]
    [Trait("Category", "Integration")]
    public async Task CheckpointManager_DeleteCheckpoint_ShouldRemoveFile()
    {
        // Arrange
        var checkpoint = new PipelineCheckpoint();
        checkpoint.CompleteStep("story_idea", "TestStory");
        await _checkpointManager.SaveCheckpointAsync(checkpoint);

        var checkpointPath = Path.Combine(_testDirectory, "pipeline_checkpoint.json");
        Assert.True(File.Exists(checkpointPath), "Checkpoint file should exist before delete");

        // Act
        await _checkpointManager.DeleteCheckpointAsync();

        // Assert
        Assert.False(File.Exists(checkpointPath), "Checkpoint file should not exist after delete");
    }

    [Fact]
    [Trait("Category", "Integration")]
    public async Task CheckpointManager_LoadNonExistentCheckpoint_ShouldReturnEmpty()
    {
        // Act - Try to load checkpoint when none exists
        var checkpoint = await _checkpointManager.LoadCheckpointAsync();

        // Assert - Should return empty checkpoint, not throw
        Assert.NotNull(checkpoint);
        Assert.Empty(checkpoint.CompletedSteps);
        Assert.Empty(checkpoint.StepData);
    }

    [Fact]
    [Trait("Category", "Integration")]
    public async Task CheckpointManager_HasCheckpoint_ShouldDetectCheckpoint()
    {
        // Arrange - No checkpoint initially
        var hasCheckpointBefore = await _checkpointManager.HasCheckpointAsync();
        Assert.False(hasCheckpointBefore);

        // Act - Create checkpoint
        var checkpoint = new PipelineCheckpoint();
        checkpoint.CompleteStep("story_idea", "TestStory");
        await _checkpointManager.SaveCheckpointAsync(checkpoint);

        // Assert - Checkpoint exists now
        var hasCheckpointAfter = await _checkpointManager.HasCheckpointAsync();
        Assert.True(hasCheckpointAfter);
    }

    #endregion

    #region PipelineCheckpoint Logic Tests

    [Fact]
    [Trait("Category", "Unit")]
    public void PipelineCheckpoint_CompleteStep_ShouldMarkStepComplete()
    {
        // Arrange
        var checkpoint = new PipelineCheckpoint();

        // Act
        checkpoint.CompleteStep("test_stage", "test_data");

        // Assert
        Assert.True(checkpoint.IsStepComplete("test_stage"));
        Assert.Equal("test_data", checkpoint.GetStepData("test_stage"));
    }

    [Fact]
    [Trait("Category", "Unit")]
    public void PipelineCheckpoint_IsStepComplete_ReturnsFalseForUncompletedStep()
    {
        // Arrange
        var checkpoint = new PipelineCheckpoint();

        // Act & Assert
        Assert.False(checkpoint.IsStepComplete("uncompleted_stage"));
    }

    [Fact]
    [Trait("Category", "Unit")]
    public void PipelineCheckpoint_GetStepData_ReturnsNullForNonExistentStep()
    {
        // Arrange
        var checkpoint = new PipelineCheckpoint();

        // Act
        var data = checkpoint.GetStepData("nonexistent_step");

        // Assert
        Assert.Null(data);
    }

    [Fact]
    [Trait("Category", "Unit")]
    public void PipelineCheckpoint_CompleteStep_WithEmptyStepName_ThrowsException()
    {
        // Arrange
        var checkpoint = new PipelineCheckpoint();

        // Act & Assert
        Assert.Throws<ArgumentException>(() => checkpoint.CompleteStep("", "data"));
        Assert.Throws<ArgumentException>(() => checkpoint.CompleteStep("   ", "data"));
    }

    [Fact]
    [Trait("Category", "Unit")]
    public void PipelineCheckpoint_CompleteStep_UpdatesLastUpdatedTime()
    {
        // Arrange
        var checkpoint = new PipelineCheckpoint();
        var timeBefore = DateTime.Now;

        // Act
        checkpoint.CompleteStep("test_stage", "test_data");

        // Assert
        Assert.True(checkpoint.LastUpdated >= timeBefore);
        Assert.True(checkpoint.LastUpdated <= DateTime.Now);
    }

    #endregion

    #region Resume Workflow Simulation Tests

    [Fact]
    [Trait("Category", "Integration")]
    public async Task PipelineResume_SimulateInterruption_ShouldResumeFromCheckpoint()
    {
        // Simulate a pipeline that gets interrupted

        // Phase 1: Initial pipeline execution
        var checkpoint = new PipelineCheckpoint();
        
        // Complete some stages
        checkpoint.CompleteStep("story_idea", "MyStory");
        checkpoint.CompleteStep("script_generation", "MyStory");
        await _checkpointManager.SaveCheckpointAsync(checkpoint);

        // Simulate interruption (pipeline stops here)

        // Phase 2: Resume pipeline
        var resumedCheckpoint = await _checkpointManager.LoadCheckpointAsync();

        // Assert - Previously completed stages are marked as complete
        Assert.True(resumedCheckpoint.IsStepComplete("story_idea"));
        Assert.True(resumedCheckpoint.IsStepComplete("script_generation"));
        
        // Assert - Later stages are not complete
        Assert.False(resumedCheckpoint.IsStepComplete("script_revision"));
        Assert.False(resumedCheckpoint.IsStepComplete("voice_synthesis"));

        // Continue pipeline from where it left off
        resumedCheckpoint.CompleteStep("script_revision", "MyStory");
        await _checkpointManager.SaveCheckpointAsync(resumedCheckpoint);

        // Verify the checkpoint was updated
        var finalCheckpoint = await _checkpointManager.LoadCheckpointAsync();
        Assert.True(finalCheckpoint.IsStepComplete("story_idea"));
        Assert.True(finalCheckpoint.IsStepComplete("script_generation"));
        Assert.True(finalCheckpoint.IsStepComplete("script_revision"));
    }

    [Fact]
    [Trait("Category", "Integration")]
    public async Task PipelineResume_MultipleInterruptions_ShouldTrackAllProgress()
    {
        // Simulate multiple interruptions and resumes

        // Interruption 1
        var checkpoint = new PipelineCheckpoint();
        checkpoint.CompleteStep("story_idea", "MyStory");
        await _checkpointManager.SaveCheckpointAsync(checkpoint);

        // Resume 1
        checkpoint = await _checkpointManager.LoadCheckpointAsync();
        checkpoint.CompleteStep("script_generation", "MyStory");
        await _checkpointManager.SaveCheckpointAsync(checkpoint);

        // Interruption 2
        // Resume 2
        checkpoint = await _checkpointManager.LoadCheckpointAsync();
        checkpoint.CompleteStep("script_revision", "MyStory");
        checkpoint.CompleteStep("script_enhancement", "MyStory");
        await _checkpointManager.SaveCheckpointAsync(checkpoint);

        // Final verification
        var finalCheckpoint = await _checkpointManager.LoadCheckpointAsync();
        Assert.True(finalCheckpoint.IsStepComplete("story_idea"));
        Assert.True(finalCheckpoint.IsStepComplete("script_generation"));
        Assert.True(finalCheckpoint.IsStepComplete("script_revision"));
        Assert.True(finalCheckpoint.IsStepComplete("script_enhancement"));
    }

    #endregion
}
