using StoryGenerator.Pipeline.Core;
using StoryGenerator.Pipeline.Interfaces;
using Xunit;

namespace StoryGenerator.Tests.Pipeline;

/// <summary>
/// Tests for the stage registry
/// </summary>
public class StageRegistryTests
{
    [Fact]
    [Trait("Category", "Unit")]
    public void Register_WithValidMetadata_ShouldSucceed()
    {
        // Arrange
        var registry = new StageRegistry();
        var metadata = new StageMetadata
        {
            Id = "test_stage",
            Name = "Test Stage",
            Description = "Test stage description",
            Category = "test"
        };

        // Act
        registry.Register("test_stage", metadata);

        // Assert
        Assert.True(registry.IsRegistered("test_stage"));
        var retrieved = registry.GetMetadata("test_stage");
        Assert.NotNull(retrieved);
        Assert.Equal("Test Stage", retrieved.Name);
    }

    [Fact]
    [Trait("Category", "Unit")]
    public void Register_WithEmptyId_ShouldThrow()
    {
        // Arrange
        var registry = new StageRegistry();
        var metadata = new StageMetadata
        {
            Id = "test_stage",
            Name = "Test Stage"
        };

        // Act & Assert
        Assert.Throws<ArgumentException>(() => registry.Register("", metadata));
    }

    [Fact]
    [Trait("Category", "Unit")]
    public void Register_WithNullMetadata_ShouldThrow()
    {
        // Arrange
        var registry = new StageRegistry();

        // Act & Assert
        Assert.Throws<ArgumentNullException>(() => registry.Register("test_stage", null!));
    }

    [Fact]
    [Trait("Category", "Unit")]
    public void Register_WithDuplicateId_ShouldThrow()
    {
        // Arrange
        var registry = new StageRegistry();
        var metadata1 = new StageMetadata
        {
            Id = "test_stage",
            Name = "Test Stage 1"
        };
        var metadata2 = new StageMetadata
        {
            Id = "test_stage",
            Name = "Test Stage 2"
        };

        // Act
        registry.Register("test_stage", metadata1);

        // Assert
        Assert.Throws<InvalidOperationException>(() => registry.Register("test_stage", metadata2));
    }

    [Fact]
    [Trait("Category", "Unit")]
    public void GetMetadata_WithNonExistentId_ShouldReturnNull()
    {
        // Arrange
        var registry = new StageRegistry();

        // Act
        var metadata = registry.GetMetadata("nonexistent");

        // Assert
        Assert.Null(metadata);
    }

    [Fact]
    [Trait("Category", "Unit")]
    public void IsRegistered_WithRegisteredStage_ShouldReturnTrue()
    {
        // Arrange
        var registry = new StageRegistry();
        var metadata = new StageMetadata
        {
            Id = "test_stage",
            Name = "Test Stage"
        };
        registry.Register("test_stage", metadata);

        // Act
        var isRegistered = registry.IsRegistered("test_stage");

        // Assert
        Assert.True(isRegistered);
    }

    [Fact]
    [Trait("Category", "Unit")]
    public void IsRegistered_WithUnregisteredStage_ShouldReturnFalse()
    {
        // Arrange
        var registry = new StageRegistry();

        // Act
        var isRegistered = registry.IsRegistered("nonexistent");

        // Assert
        Assert.False(isRegistered);
    }

    [Fact]
    [Trait("Category", "Unit")]
    public void GetAllStages_WithMultipleStages_ShouldReturnAll()
    {
        // Arrange
        var registry = new StageRegistry();
        var metadata1 = new StageMetadata { Id = "stage_1", Name = "Stage 1" };
        var metadata2 = new StageMetadata { Id = "stage_2", Name = "Stage 2" };
        var metadata3 = new StageMetadata { Id = "stage_3", Name = "Stage 3" };

        registry.Register("stage_1", metadata1);
        registry.Register("stage_2", metadata2);
        registry.Register("stage_3", metadata3);

        // Act
        var allStages = registry.GetAllStages();

        // Assert
        Assert.Equal(3, allStages.Count);
        Assert.Contains(allStages, s => s.Id == "stage_1");
        Assert.Contains(allStages, s => s.Id == "stage_2");
        Assert.Contains(allStages, s => s.Id == "stage_3");
    }

    [Fact]
    [Trait("Category", "Unit")]
    public void Unregister_WithExistingStage_ShouldRemoveStage()
    {
        // Arrange
        var registry = new StageRegistry();
        var metadata = new StageMetadata
        {
            Id = "test_stage",
            Name = "Test Stage"
        };
        registry.Register("test_stage", metadata);

        // Act
        registry.Unregister("test_stage");

        // Assert
        Assert.False(registry.IsRegistered("test_stage"));
        Assert.Null(registry.GetMetadata("test_stage"));
    }

    [Fact]
    [Trait("Category", "Unit")]
    public void Unregister_WithNonExistentStage_ShouldNotThrow()
    {
        // Arrange
        var registry = new StageRegistry();

        // Act & Assert - should not throw
        registry.Unregister("nonexistent");
    }

    [Fact]
    [Trait("Category", "Unit")]
    public void StageMetadata_WithDependencies_ShouldStoreDependencies()
    {
        // Arrange
        var metadata = new StageMetadata
        {
            Id = "stage_with_deps",
            Name = "Stage With Dependencies",
            Dependencies = new List<string> { "dep_1", "dep_2" }
        };

        // Assert
        Assert.Equal(2, metadata.Dependencies.Count);
        Assert.Contains("dep_1", metadata.Dependencies);
        Assert.Contains("dep_2", metadata.Dependencies);
    }

    [Fact]
    [Trait("Category", "Unit")]
    public void StageConfiguration_WithParameters_ShouldStoreParameters()
    {
        // Arrange
        var config = new StageConfiguration
        {
            Id = "test_stage",
            Enabled = true,
            Order = 10,
            Parameters = new Dictionary<string, object>
            {
                ["param1"] = "value1",
                ["param2"] = 42
            }
        };

        // Assert
        Assert.Equal(2, config.Parameters.Count);
        Assert.Equal("value1", config.Parameters["param1"]);
        Assert.Equal(42, config.Parameters["param2"]);
    }
}
