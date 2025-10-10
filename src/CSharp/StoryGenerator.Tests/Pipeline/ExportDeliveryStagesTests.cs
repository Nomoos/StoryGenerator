using System.Text.Json;
using StoryGenerator.Pipeline.Stages;
using StoryGenerator.Pipeline.Stages.Models;
using Xunit;

namespace StoryGenerator.Tests.Pipeline;

/// <summary>
/// Tests for Phase 3 Group 11: Export & Delivery Stages
/// </summary>
public class ExportDeliveryStagesTests
{
    #region Final Encode Tests

    [Fact]
    public async Task FinalEncodeStage_WithValidInput_EncodesVideo()
    {
        // Arrange
        var stage = new FinalEncodeStage();
        var testVideoPath = CreateTestVideoFile();
        var input = new FinalEncodeInput
        {
            InputVideoPath = testVideoPath,
            TitleId = "test_001",
            Gender = "male",
            AgeGroup = "18-24",
            Platform = "youtube",
            Codec = "h264",
            Bitrate = "8M",
            Resolution = "1080x1920"
        };

        try
        {
            // Act
            var output = await stage.ExecuteAsync(input, null, CancellationToken.None);

            // Assert
            Assert.NotNull(output);
            Assert.NotEmpty(output.FinalVideoPath);
            Assert.True(output.FileSizeBytes > 0);
            Assert.True(output.DurationSeconds > 0);
            Assert.Equal("h264", output.Codec);
            Assert.Equal("8M", output.Bitrate);
            Assert.Equal("1080x1920", output.Resolution);
        }
        finally
        {
            // Cleanup
            CleanupTestFile(testVideoPath);
        }
    }

    [Fact]
    public async Task FinalEncodeStage_InvalidVideoPath_ThrowsException()
    {
        // Arrange
        var stage = new FinalEncodeStage();
        var input = new FinalEncodeInput
        {
            InputVideoPath = "nonexistent.mp4",
            TitleId = "test_002",
            Gender = "male",
            AgeGroup = "18-24"
        };

        // Act & Assert
        await Assert.ThrowsAsync<FileNotFoundException>(
            async () => await stage.ExecuteAsync(input, null, CancellationToken.None));
    }

    [Fact]
    public async Task FinalEncodeStage_DifferentPlatforms_EncodesCorrectly()
    {
        // Arrange
        var stage = new FinalEncodeStage();
        var platforms = new[] { "youtube", "tiktok", "instagram" };
        var outputs = new List<FinalEncodeOutput>();

        // Act
        foreach (var platform in platforms)
        {
            var testVideoPath = CreateTestVideoFile();
            try
            {
                var input = new FinalEncodeInput
                {
                    InputVideoPath = testVideoPath,
                    TitleId = $"test_003_{platform}",
                    Gender = "female",
                    AgeGroup = "25-34",
                    Platform = platform
                };
                var output = await stage.ExecuteAsync(input, null, CancellationToken.None);
                outputs.Add(output);
            }
            finally
            {
                CleanupTestFile(testVideoPath);
            }
        }

        // Assert
        Assert.Equal(3, outputs.Count);
        Assert.All(outputs, o => Assert.NotEmpty(o.FinalVideoPath));
        Assert.All(outputs, o => Assert.True(o.FileSizeBytes > 0));
    }

    #endregion

    #region Thumbnail Generation Tests

    [Fact]
    public async Task ThumbnailGenerationStage_WithValidVideo_GeneratesThumbnail()
    {
        // Arrange
        var stage = new ThumbnailGenerationStage();
        var testVideoPath = CreateTestVideoFile();
        var input = new ThumbnailGenerationInput
        {
            VideoPath = testVideoPath,
            TitleId = "test_004",
            Gender = "male",
            AgeGroup = "18-24",
            Width = 1920,
            Height = 1080,
            Quality = 90
        };

        try
        {
            // Act
            var output = await stage.ExecuteAsync(input, null, CancellationToken.None);

            // Assert
            Assert.NotNull(output);
            Assert.NotEmpty(output.ThumbnailPath);
            Assert.Equal(1920, output.Width);
            Assert.Equal(1080, output.Height);
            Assert.True(output.FileSizeBytes > 0);
            Assert.True(output.TimestampSeconds >= 0);
        }
        finally
        {
            // Cleanup
            CleanupTestFile(testVideoPath);
        }
    }

    [Fact]
    public async Task ThumbnailGenerationStage_InvalidVideoPath_ThrowsException()
    {
        // Arrange
        var stage = new ThumbnailGenerationStage();
        var input = new ThumbnailGenerationInput
        {
            VideoPath = "nonexistent.mp4",
            TitleId = "test_005",
            Gender = "male",
            AgeGroup = "18-24"
        };

        // Act & Assert
        await Assert.ThrowsAsync<FileNotFoundException>(
            async () => await stage.ExecuteAsync(input, null, CancellationToken.None));
    }

    [Fact]
    public async Task ThumbnailGenerationStage_WithCustomTimestamp_UsesSpecifiedTime()
    {
        // Arrange
        var stage = new ThumbnailGenerationStage();
        var testVideoPath = CreateTestVideoFile();
        var customTimestamp = 15.5;
        var input = new ThumbnailGenerationInput
        {
            VideoPath = testVideoPath,
            TitleId = "test_006",
            Gender = "female",
            AgeGroup = "25-34",
            TimestampSeconds = customTimestamp
        };

        try
        {
            // Act
            var output = await stage.ExecuteAsync(input, null, CancellationToken.None);

            // Assert
            Assert.Equal(customTimestamp, output.TimestampSeconds);
        }
        finally
        {
            // Cleanup
            CleanupTestFile(testVideoPath);
        }
    }

    [Fact]
    public async Task ThumbnailGenerationStage_CustomDimensions_GeneratesCorrectSize()
    {
        // Arrange
        var stage = new ThumbnailGenerationStage();
        var testVideoPath = CreateTestVideoFile();
        var input = new ThumbnailGenerationInput
        {
            VideoPath = testVideoPath,
            TitleId = "test_007",
            Gender = "male",
            AgeGroup = "18-24",
            Width = 1280,
            Height = 720,
            Quality = 85
        };

        try
        {
            // Act
            var output = await stage.ExecuteAsync(input, null, CancellationToken.None);

            // Assert
            Assert.Equal(1280, output.Width);
            Assert.Equal(720, output.Height);
        }
        finally
        {
            // Cleanup
            CleanupTestFile(testVideoPath);
        }
    }

    #endregion

    #region Metadata Creation Tests

    [Fact]
    public async Task MetadataCreationStage_WithValidInputs_CreatesMetadata()
    {
        // Arrange
        var stage = new MetadataCreationStage();
        var testVideoPath = CreateTestVideoFile();
        var testThumbnailPath = CreateTestThumbnailFile();
        var input = new MetadataCreationInput
        {
            VideoPath = testVideoPath,
            ThumbnailPath = testThumbnailPath,
            TitleId = "test_008",
            Title = "Test Video Title",
            Description = "Test video description for unit testing",
            Gender = "male",
            AgeGroup = "18-24",
            Tags = new List<string> { "test", "video", "demo" },
            Platform = "youtube"
        };

        try
        {
            // Act
            var output = await stage.ExecuteAsync(input, null, CancellationToken.None);

            // Assert
            Assert.NotNull(output);
            Assert.NotEmpty(output.MetadataPath);
            Assert.NotNull(output.Metadata);
            Assert.Equal("test_008", output.Metadata.TitleId);
            Assert.Equal("Test Video Title", output.Metadata.Title);
            Assert.Equal("Test video description for unit testing", output.Metadata.Description);
            Assert.Equal("youtube", output.Metadata.Platform);
            Assert.Equal(3, output.Metadata.Tags.Count);
            Assert.True(File.Exists(output.MetadataPath));
        }
        finally
        {
            // Cleanup
            CleanupTestFile(testVideoPath);
            CleanupTestFile(testThumbnailPath);
        }
    }

    [Fact]
    public async Task MetadataCreationStage_InvalidVideoPath_ThrowsException()
    {
        // Arrange
        var stage = new MetadataCreationStage();
        var testThumbnailPath = CreateTestThumbnailFile();
        var input = new MetadataCreationInput
        {
            VideoPath = "nonexistent.mp4",
            ThumbnailPath = testThumbnailPath,
            TitleId = "test_009",
            Title = "Test",
            Gender = "male",
            AgeGroup = "18-24"
        };

        try
        {
            // Act & Assert
            await Assert.ThrowsAsync<FileNotFoundException>(
                async () => await stage.ExecuteAsync(input, null, CancellationToken.None));
        }
        finally
        {
            CleanupTestFile(testThumbnailPath);
        }
    }

    [Fact]
    public async Task MetadataCreationStage_InvalidThumbnailPath_ThrowsException()
    {
        // Arrange
        var stage = new MetadataCreationStage();
        var testVideoPath = CreateTestVideoFile();
        var input = new MetadataCreationInput
        {
            VideoPath = testVideoPath,
            ThumbnailPath = "nonexistent.jpg",
            TitleId = "test_010",
            Title = "Test",
            Gender = "male",
            AgeGroup = "18-24"
        };

        try
        {
            // Act & Assert
            await Assert.ThrowsAsync<FileNotFoundException>(
                async () => await stage.ExecuteAsync(input, null, CancellationToken.None));
        }
        finally
        {
            CleanupTestFile(testVideoPath);
        }
    }

    [Fact]
    public async Task MetadataCreationStage_WithQualityReport_IncludesQualityStatus()
    {
        // Arrange
        var stage = new MetadataCreationStage();
        var testVideoPath = CreateTestVideoFile();
        var testThumbnailPath = CreateTestThumbnailFile();
        var testQualityReportPath = CreateTestQualityReportFile("PASS");
        var input = new MetadataCreationInput
        {
            VideoPath = testVideoPath,
            ThumbnailPath = testThumbnailPath,
            TitleId = "test_011",
            Title = "Test Video with QC",
            Description = "Test",
            Gender = "female",
            AgeGroup = "25-34",
            Platform = "tiktok",
            QualityReportPath = testQualityReportPath
        };

        try
        {
            // Act
            var output = await stage.ExecuteAsync(input, null, CancellationToken.None);

            // Assert
            Assert.NotNull(output.Metadata.QualityStatus);
            Assert.Equal("PASS", output.Metadata.QualityStatus);
        }
        finally
        {
            // Cleanup
            CleanupTestFile(testVideoPath);
            CleanupTestFile(testThumbnailPath);
            CleanupTestFile(testQualityReportPath);
        }
    }

    [Fact]
    public async Task MetadataCreationStage_MetadataJsonFormat_IsValid()
    {
        // Arrange
        var stage = new MetadataCreationStage();
        var testVideoPath = CreateTestVideoFile();
        var testThumbnailPath = CreateTestThumbnailFile();
        var input = new MetadataCreationInput
        {
            VideoPath = testVideoPath,
            ThumbnailPath = testThumbnailPath,
            TitleId = "test_012",
            Title = "JSON Format Test",
            Description = "Testing JSON output",
            Gender = "male",
            AgeGroup = "35-44",
            Tags = new List<string> { "json", "test" },
            Platform = "instagram"
        };

        try
        {
            // Act
            var output = await stage.ExecuteAsync(input, null, CancellationToken.None);

            // Assert - Verify JSON is valid by deserializing it
            var jsonContent = await File.ReadAllTextAsync(output.MetadataPath);
            var deserializedMetadata = JsonSerializer.Deserialize<VideoMetadata>(jsonContent, new JsonSerializerOptions
            {
                PropertyNameCaseInsensitive = true
            });

            Assert.NotNull(deserializedMetadata);
            Assert.Equal("test_012", deserializedMetadata.TitleId);
            Assert.Equal("JSON Format Test", deserializedMetadata.Title);
        }
        finally
        {
            // Cleanup
            CleanupTestFile(testVideoPath);
            CleanupTestFile(testThumbnailPath);
        }
    }

    #endregion

    #region Integration Tests

    [Fact]
    public async Task ExportPipeline_FullWorkflow_ProducesAllArtifacts()
    {
        // Arrange
        var encodeStage = new FinalEncodeStage();
        var thumbnailStage = new ThumbnailGenerationStage();
        var metadataStage = new MetadataCreationStage();

        var testVideoPath = CreateTestVideoFile();

        // Act
        // Step 1: Encode video
        var encodeInput = new FinalEncodeInput
        {
            InputVideoPath = testVideoPath,
            TitleId = "test_013",
            Gender = "male",
            AgeGroup = "18-24",
            Platform = "youtube"
        };
        var encodeOutput = await encodeStage.ExecuteAsync(encodeInput, null, CancellationToken.None);

        // Step 2: Generate thumbnail
        var thumbnailInput = new ThumbnailGenerationInput
        {
            VideoPath = encodeOutput.FinalVideoPath,
            TitleId = "test_013",
            Gender = "male",
            AgeGroup = "18-24"
        };
        var thumbnailOutput = await thumbnailStage.ExecuteAsync(thumbnailInput, null, CancellationToken.None);

        // Step 3: Create metadata
        var metadataInput = new MetadataCreationInput
        {
            VideoPath = encodeOutput.FinalVideoPath,
            ThumbnailPath = thumbnailOutput.ThumbnailPath,
            TitleId = "test_013",
            Title = "Integration Test Video",
            Description = "Full pipeline test",
            Gender = "male",
            AgeGroup = "18-24",
            Tags = new List<string> { "integration", "test" },
            Platform = "youtube"
        };
        var metadataOutput = await metadataStage.ExecuteAsync(metadataInput, null, CancellationToken.None);

        // Assert
        Assert.NotEmpty(encodeOutput.FinalVideoPath);
        Assert.NotEmpty(thumbnailOutput.ThumbnailPath);
        Assert.NotEmpty(metadataOutput.MetadataPath);
        Assert.Equal("test_013", metadataOutput.Metadata.TitleId);
        Assert.Equal("Integration Test Video", metadataOutput.Metadata.Title);

        // Cleanup
        CleanupTestFile(testVideoPath);
    }

    #endregion

    #region Helper Methods

    private string CreateTestVideoFile()
    {
        var tempFile = Path.Combine(Path.GetTempPath(), $"test_video_{Guid.NewGuid()}.mp4");
        File.WriteAllText(tempFile, "test video content");
        return tempFile;
    }

    private string CreateTestThumbnailFile()
    {
        var tempFile = Path.Combine(Path.GetTempPath(), $"test_thumbnail_{Guid.NewGuid()}.jpg");
        File.WriteAllText(tempFile, "test thumbnail content");
        return tempFile;
    }

    private string CreateTestQualityReportFile(string status)
    {
        var tempFile = Path.Combine(Path.GetTempPath(), $"test_qc_report_{Guid.NewGuid()}.json");
        var report = new { overallStatus = status };
        var json = JsonSerializer.Serialize(report);
        File.WriteAllText(tempFile, json);
        return tempFile;
    }

    private void CleanupTestFile(string filePath)
    {
        if (File.Exists(filePath))
        {
            try
            {
                File.Delete(filePath);
            }
            catch
            {
                // Ignore cleanup errors
            }
        }
    }

    #endregion
}
