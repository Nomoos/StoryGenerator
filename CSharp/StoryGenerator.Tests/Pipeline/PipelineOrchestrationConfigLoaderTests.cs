using StoryGenerator.Pipeline.Config;
using Xunit;

namespace StoryGenerator.Tests.Pipeline;

/// <summary>
/// Tests for pipeline orchestration configuration loader
/// </summary>
public class PipelineOrchestrationConfigLoaderTests : IDisposable
{
    private readonly string _testDirectory;

    public PipelineOrchestrationConfigLoaderTests()
    {
        _testDirectory = Path.Combine(Path.GetTempPath(), $"test_config_{Guid.NewGuid():N}");
        Directory.CreateDirectory(_testDirectory);
    }

    public void Dispose()
    {
        if (Directory.Exists(_testDirectory))
        {
            Directory.Delete(_testDirectory, true);
        }
    }

    [Fact]
    [Trait("Category", "Unit")]
    public void LoadFromYaml_WithValidYaml_ShouldDeserialize()
    {
        // Arrange
        var yaml = @"
metadata:
  name: Test Pipeline
  version: 1.0.0
  description: Test description

stages:
  - id: stage_1
    name: Stage 1
    enabled: true
    order: 10
    max_retries: 3
";

        var loader = new PipelineOrchestrationConfigLoader();

        // Act
        var config = loader.LoadFromYaml(yaml);

        // Assert
        Assert.NotNull(config);
        Assert.Equal("Test Pipeline", config.Metadata.Name);
        Assert.Equal("1.0.0", config.Metadata.Version);
        Assert.Single(config.Stages);
        Assert.Equal("stage_1", config.Stages[0].Id);
        Assert.Equal(10, config.Stages[0].Order);
        Assert.Equal(3, config.Stages[0].MaxRetries);
    }

    [Fact]
    [Trait("Category", "Unit")]
    public void LoadFromJson_WithValidJson_ShouldDeserialize()
    {
        // Arrange
        var json = @"{
  ""metadata"": {
    ""name"": ""Test Pipeline"",
    ""version"": ""1.0.0""
  },
  ""stages"": [
    {
      ""id"": ""stage_1"",
      ""name"": ""Stage 1"",
      ""enabled"": true,
      ""order"": 10
    }
  ]
}";

        var loader = new PipelineOrchestrationConfigLoader();

        // Act
        var config = loader.LoadFromJson(json);

        // Assert
        Assert.NotNull(config);
        Assert.Equal("Test Pipeline", config.Metadata.Name);
        Assert.Single(config.Stages);
        Assert.Equal("stage_1", config.Stages[0].Id);
    }

    [Fact]
    [Trait("Category", "Integration")]
    public async Task LoadFromFileAsync_WithYamlFile_ShouldLoad()
    {
        // Arrange
        var yamlPath = Path.Combine(_testDirectory, "test.yaml");
        var yaml = @"
metadata:
  name: File Test Pipeline
  version: 1.0.0

stages:
  - id: stage_1
    name: Stage 1
    order: 10
";
        await File.WriteAllTextAsync(yamlPath, yaml);

        var loader = new PipelineOrchestrationConfigLoader();

        // Act
        var config = await loader.LoadFromFileAsync(yamlPath);

        // Assert
        Assert.NotNull(config);
        Assert.Equal("File Test Pipeline", config.Metadata.Name);
        Assert.Single(config.Stages);
    }

    [Fact]
    [Trait("Category", "Integration")]
    public async Task LoadFromFileAsync_WithJsonFile_ShouldLoad()
    {
        // Arrange
        var jsonPath = Path.Combine(_testDirectory, "test.json");
        var json = @"{
  ""metadata"": {
    ""name"": ""JSON Test Pipeline"",
    ""version"": ""1.0.0""
  },
  ""stages"": [
    {
      ""id"": ""stage_1"",
      ""order"": 10
    }
  ]
}";
        await File.WriteAllTextAsync(jsonPath, json);

        var loader = new PipelineOrchestrationConfigLoader();

        // Act
        var config = await loader.LoadFromFileAsync(jsonPath);

        // Assert
        Assert.NotNull(config);
        Assert.Equal("JSON Test Pipeline", config.Metadata.Name);
        Assert.Single(config.Stages);
    }

    [Fact]
    [Trait("Category", "Integration")]
    public async Task LoadFromFileAsync_WithNonExistentFile_ShouldThrow()
    {
        // Arrange
        var loader = new PipelineOrchestrationConfigLoader();
        var nonExistentPath = Path.Combine(_testDirectory, "nonexistent.yaml");

        // Act & Assert
        await Assert.ThrowsAsync<FileNotFoundException>(
            async () => await loader.LoadFromFileAsync(nonExistentPath));
    }

    [Fact]
    [Trait("Category", "Integration")]
    public async Task LoadFromFileAsync_WithUnsupportedExtension_ShouldThrow()
    {
        // Arrange
        var txtPath = Path.Combine(_testDirectory, "test.txt");
        await File.WriteAllTextAsync(txtPath, "test content");

        var loader = new PipelineOrchestrationConfigLoader();

        // Act & Assert
        await Assert.ThrowsAsync<NotSupportedException>(
            async () => await loader.LoadFromFileAsync(txtPath));
    }

    [Fact]
    [Trait("Category", "Integration")]
    public async Task SaveToFileAsync_WithYaml_ShouldSave()
    {
        // Arrange
        var config = new PipelineOrchestrationConfig
        {
            Metadata = new PipelineMetadata
            {
                Name = "Save Test",
                Version = "1.0.0"
            },
            Stages = new List<PipelineStageConfig>
            {
                new PipelineStageConfig
                {
                    Id = "stage_1",
                    Name = "Stage 1",
                    Order = 10
                }
            }
        };

        var yamlPath = Path.Combine(_testDirectory, "saved.yaml");
        var loader = new PipelineOrchestrationConfigLoader();

        // Act
        await loader.SaveToFileAsync(config, yamlPath);

        // Assert
        Assert.True(File.Exists(yamlPath));
        var loaded = await loader.LoadFromFileAsync(yamlPath);
        Assert.Equal("Save Test", loaded.Metadata.Name);
    }

    [Fact]
    [Trait("Category", "Integration")]
    public async Task SaveToFileAsync_WithJson_ShouldSave()
    {
        // Arrange
        var config = new PipelineOrchestrationConfig
        {
            Metadata = new PipelineMetadata
            {
                Name = "JSON Save Test",
                Version = "1.0.0"
            },
            Stages = new List<PipelineStageConfig>
            {
                new PipelineStageConfig
                {
                    Id = "stage_1",
                    Order = 10
                }
            }
        };

        var jsonPath = Path.Combine(_testDirectory, "saved.json");
        var loader = new PipelineOrchestrationConfigLoader();

        // Act
        await loader.SaveToFileAsync(config, jsonPath);

        // Assert
        Assert.True(File.Exists(jsonPath));
        var loaded = await loader.LoadFromFileAsync(jsonPath);
        Assert.Equal("JSON Save Test", loaded.Metadata.Name);
    }

    [Fact]
    [Trait("Category", "Unit")]
    public void ValidateConfiguration_WithValidConfig_ShouldReturnNoErrors()
    {
        // Arrange
        var config = new PipelineOrchestrationConfig
        {
            Stages = new List<PipelineStageConfig>
            {
                new PipelineStageConfig
                {
                    Id = "stage_1",
                    Order = 10,
                    MaxRetries = 3
                }
            }
        };

        // Act
        var errors = PipelineOrchestrationConfigLoader.ValidateConfiguration(config);

        // Assert
        Assert.Empty(errors);
    }

    [Fact]
    [Trait("Category", "Unit")]
    public void ValidateConfiguration_WithNoStages_ShouldReturnError()
    {
        // Arrange
        var config = new PipelineOrchestrationConfig
        {
            Stages = new List<PipelineStageConfig>()
        };

        // Act
        var errors = PipelineOrchestrationConfigLoader.ValidateConfiguration(config);

        // Assert
        Assert.NotEmpty(errors);
        Assert.Contains(errors, e => e.Contains("at least one stage"));
    }

    [Fact]
    [Trait("Category", "Unit")]
    public void ValidateConfiguration_WithEmptyStageId_ShouldReturnError()
    {
        // Arrange
        var config = new PipelineOrchestrationConfig
        {
            Stages = new List<PipelineStageConfig>
            {
                new PipelineStageConfig
                {
                    Id = "",
                    Order = 10
                }
            }
        };

        // Act
        var errors = PipelineOrchestrationConfigLoader.ValidateConfiguration(config);

        // Assert
        Assert.NotEmpty(errors);
        Assert.Contains(errors, e => e.Contains("cannot be empty"));
    }

    [Fact]
    [Trait("Category", "Unit")]
    public void ValidateConfiguration_WithDuplicateIds_ShouldReturnError()
    {
        // Arrange
        var config = new PipelineOrchestrationConfig
        {
            Stages = new List<PipelineStageConfig>
            {
                new PipelineStageConfig { Id = "stage_1", Order = 10 },
                new PipelineStageConfig { Id = "stage_1", Order = 20 }
            }
        };

        // Act
        var errors = PipelineOrchestrationConfigLoader.ValidateConfiguration(config);

        // Assert
        Assert.NotEmpty(errors);
        Assert.Contains(errors, e => e.Contains("Duplicate stage ID"));
    }

    [Fact]
    [Trait("Category", "Unit")]
    public void ValidateConfiguration_WithNegativeOrder_ShouldReturnError()
    {
        // Arrange
        var config = new PipelineOrchestrationConfig
        {
            Stages = new List<PipelineStageConfig>
            {
                new PipelineStageConfig
                {
                    Id = "stage_1",
                    Order = -1
                }
            }
        };

        // Act
        var errors = PipelineOrchestrationConfigLoader.ValidateConfiguration(config);

        // Assert
        Assert.NotEmpty(errors);
        Assert.Contains(errors, e => e.Contains("invalid order"));
    }

    [Fact]
    [Trait("Category", "Unit")]
    public void ValidateConfiguration_WithNegativeMaxRetries_ShouldReturnError()
    {
        // Arrange
        var config = new PipelineOrchestrationConfig
        {
            Stages = new List<PipelineStageConfig>
            {
                new PipelineStageConfig
                {
                    Id = "stage_1",
                    Order = 10,
                    MaxRetries = -1
                }
            }
        };

        // Act
        var errors = PipelineOrchestrationConfigLoader.ValidateConfiguration(config);

        // Assert
        Assert.NotEmpty(errors);
        Assert.Contains(errors, e => e.Contains("invalid MaxRetries"));
    }

    [Fact]
    [Trait("Category", "Unit")]
    public void SerializeToYaml_ShouldProduceValidYaml()
    {
        // Arrange
        var config = new PipelineOrchestrationConfig
        {
            Metadata = new PipelineMetadata
            {
                Name = "Serialize Test",
                Version = "1.0.0"
            },
            Stages = new List<PipelineStageConfig>
            {
                new PipelineStageConfig
                {
                    Id = "stage_1",
                    Name = "Stage 1",
                    Order = 10
                }
            }
        };

        var loader = new PipelineOrchestrationConfigLoader();

        // Act
        var yaml = loader.SerializeToYaml(config);

        // Assert
        Assert.NotEmpty(yaml);
        Assert.Contains("Serialize Test", yaml);
        Assert.Contains("stage_1", yaml);
    }

    [Fact]
    [Trait("Category", "Unit")]
    public void SerializeToJson_ShouldProduceValidJson()
    {
        // Arrange
        var config = new PipelineOrchestrationConfig
        {
            Metadata = new PipelineMetadata
            {
                Name = "JSON Serialize Test",
                Version = "1.0.0"
            },
            Stages = new List<PipelineStageConfig>
            {
                new PipelineStageConfig
                {
                    Id = "stage_1",
                    Order = 10
                }
            }
        };

        var loader = new PipelineOrchestrationConfigLoader();

        // Act
        var json = loader.SerializeToJson(config);

        // Assert
        Assert.NotEmpty(json);
        Assert.Contains("JSON Serialize Test", json);
        Assert.Contains("stage_1", json);
    }
}
