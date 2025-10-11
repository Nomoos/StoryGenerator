using StoryGenerator.Pipeline.Stages;
using StoryGenerator.Pipeline.Stages.Models;
using Xunit;

namespace StoryGenerator.Tests.Pipeline;

/// <summary>
/// Tests for Phase 3 Group 10: Quality Control Stages
/// </summary>
public class QualityControlStagesTests
{
    #region Device Preview Tests

    [Fact]
    public async Task DevicePreviewStage_WithDefaultProfiles_GeneratesPreviews()
    {
        // Arrange
        var stage = new DevicePreviewStage();
        var testVideoPath = CreateTestVideoFile();
        var input = new DevicePreviewInput
        {
            VideoPath = testVideoPath,
            TitleId = "test_001",
            Gender = "male",
            AgeGroup = "18-24",
            DeviceProfiles = new List<DeviceProfile>() // Empty list will use defaults
        };

        try
        {
            // Act
            var output = await stage.ExecuteAsync(input, null, CancellationToken.None);

            // Assert
            Assert.NotNull(output);
            Assert.NotEmpty(output.Previews);
            Assert.NotEmpty(output.OutputPath);
            Assert.True(output.Previews.Count >= 3); // Default profiles
        }
        finally
        {
            // Cleanup
            CleanupTestFile(testVideoPath);
        }
    }

    [Fact]
    public async Task DevicePreviewStage_WithCustomProfile_GeneratesPreview()
    {
        // Arrange
        var stage = new DevicePreviewStage();
        var testVideoPath = CreateTestVideoFile();
        var customProfile = new DeviceProfile
        {
            Name = "Custom Device",
            Width = 1920,
            Height = 1080,
            AspectRatio = "16:9",
            SafeZonePercentage = 0.9
        };
        var input = new DevicePreviewInput
        {
            VideoPath = testVideoPath,
            TitleId = "test_002",
            Gender = "female",
            AgeGroup = "25-34",
            DeviceProfiles = new List<DeviceProfile> { customProfile }
        };

        try
        {
            // Act
            var output = await stage.ExecuteAsync(input, null, CancellationToken.None);

            // Assert
            Assert.NotNull(output);
            Assert.Single(output.Previews);
            Assert.Equal("Custom Device", output.Previews[0].Profile.Name);
            Assert.InRange(output.Previews[0].ReadabilityScore, 0, 100);
        }
        finally
        {
            // Cleanup
            CleanupTestFile(testVideoPath);
        }
    }

    [Fact]
    public async Task DevicePreviewStage_InvalidVideoPath_ThrowsException()
    {
        // Arrange
        var stage = new DevicePreviewStage();
        var input = new DevicePreviewInput
        {
            VideoPath = "nonexistent.mp4",
            TitleId = "test_003",
            Gender = "male",
            AgeGroup = "18-24"
        };

        // Act & Assert
        await Assert.ThrowsAsync<FileNotFoundException>(
            async () => await stage.ExecuteAsync(input, null, CancellationToken.None));
    }

    [Fact]
    public async Task DevicePreviewStage_CalculatesReadabilityScore()
    {
        // Arrange
        var stage = new DevicePreviewStage();
        var testVideoPath = CreateTestVideoFile();
        var input = new DevicePreviewInput
        {
            VideoPath = testVideoPath,
            TitleId = "test_004",
            Gender = "male",
            AgeGroup = "18-24",
            DeviceProfiles = new List<DeviceProfile>
            {
                new DeviceProfile
                {
                    Name = "Test Device",
                    Width = 1080,
                    Height = 1920,
                    AspectRatio = "9:16",
                    SafeZonePercentage = 0.9
                }
            }
        };

        try
        {
            // Act
            var output = await stage.ExecuteAsync(input, null, CancellationToken.None);

            // Assert
            Assert.Single(output.Previews);
            var preview = output.Previews[0];
            Assert.InRange(preview.ReadabilityScore, 0, 100);
        }
        finally
        {
            // Cleanup
            CleanupTestFile(testVideoPath);
        }
    }

    #endregion

    #region Sync Check Tests

    [Fact]
    public async Task SyncCheckStage_WithValidFiles_PerformsSyncCheck()
    {
        // Arrange
        var stage = new SyncCheckStage();
        var testVideoPath = CreateTestVideoFile();
        var testSubtitlePath = CreateTestSubtitleFile();
        var input = new SyncCheckInput
        {
            VideoPath = testVideoPath,
            SubtitlePath = testSubtitlePath,
            TitleId = "test_005",
            Gender = "male",
            AgeGroup = "18-24",
            MaxDriftMs = 50
        };

        try
        {
            // Act
            var output = await stage.ExecuteAsync(input, null, CancellationToken.None);

            // Assert
            Assert.NotNull(output);
            Assert.NotNull(output.Result);
            Assert.NotEmpty(output.ReportPath);
            Assert.True(output.Result.SubtitleCount > 0);
        }
        finally
        {
            // Cleanup
            CleanupTestFile(testVideoPath);
            CleanupTestFile(testSubtitlePath);
        }
    }

    [Fact]
    public async Task SyncCheckStage_InvalidVideoPath_ThrowsException()
    {
        // Arrange
        var stage = new SyncCheckStage();
        var testSubtitlePath = CreateTestSubtitleFile();
        var input = new SyncCheckInput
        {
            VideoPath = "nonexistent.mp4",
            SubtitlePath = testSubtitlePath,
            TitleId = "test_006",
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
            // Cleanup
            CleanupTestFile(testSubtitlePath);
        }
    }

    [Fact]
    public async Task SyncCheckStage_InvalidSubtitlePath_ThrowsException()
    {
        // Arrange
        var stage = new SyncCheckStage();
        var testVideoPath = CreateTestVideoFile();
        var input = new SyncCheckInput
        {
            VideoPath = testVideoPath,
            SubtitlePath = "nonexistent.srt",
            TitleId = "test_007",
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
            // Cleanup
            CleanupTestFile(testVideoPath);
        }
    }

    [Fact]
    public async Task SyncCheckStage_CalculatesSyncMetrics()
    {
        // Arrange
        var stage = new SyncCheckStage();
        var testVideoPath = CreateTestVideoFile();
        var testSubtitlePath = CreateTestSubtitleFile();
        var input = new SyncCheckInput
        {
            VideoPath = testVideoPath,
            SubtitlePath = testSubtitlePath,
            TitleId = "test_008",
            Gender = "female",
            AgeGroup = "25-34",
            MaxDriftMs = 50
        };

        try
        {
            // Act
            var output = await stage.ExecuteAsync(input, null, CancellationToken.None);

            // Assert
            Assert.NotNull(output.Result);
            Assert.True(output.Result.MaxDriftMs >= 0);
            Assert.True(output.Result.AverageDriftMs >= 0);
            Assert.True(output.Result.SubtitleCount > 0);
        }
        finally
        {
            // Cleanup
            CleanupTestFile(testVideoPath);
            CleanupTestFile(testSubtitlePath);
        }
    }

    #endregion

    #region Quality Report Tests

    [Fact]
    public async Task QualityReportStage_WithValidInput_GeneratesReport()
    {
        // Arrange
        var stage = new QualityReportStage();
        var testVideoPath = CreateTestVideoFile();
        var input = new QualityReportInput
        {
            VideoPath = testVideoPath,
            TitleId = "test_009",
            Gender = "male",
            AgeGroup = "18-24"
        };

        try
        {
            // Act
            var output = await stage.ExecuteAsync(input, null, CancellationToken.None);

            // Assert
            Assert.NotNull(output);
            Assert.NotNull(output.Report);
            Assert.NotEmpty(output.ReportPath);
            Assert.Equal("test_009", output.Report.TitleId);
            Assert.Contains(output.Report.OverallStatus, new[] { "PASS", "FAIL", "WARNING" });
        }
        finally
        {
            // Cleanup
            CleanupTestFile(testVideoPath);
        }
    }

    [Fact]
    public async Task QualityReportStage_InvalidVideoPath_ThrowsException()
    {
        // Arrange
        var stage = new QualityReportStage();
        var input = new QualityReportInput
        {
            VideoPath = "nonexistent.mp4",
            TitleId = "test_010",
            Gender = "male",
            AgeGroup = "18-24"
        };

        // Act & Assert
        await Assert.ThrowsAsync<FileNotFoundException>(
            async () => await stage.ExecuteAsync(input, null, CancellationToken.None));
    }

    [Fact]
    public async Task QualityReportStage_WithSyncCheckResults_IncludesSyncMetrics()
    {
        // Arrange
        var stage = new QualityReportStage();
        var testVideoPath = CreateTestVideoFile();
        var syncCheckOutput = new SyncCheckOutput
        {
            Result = new SyncCheckResult
            {
                IsSynced = true,
                MaxDriftMs = 35,
                AverageDriftMs = 20.5,
                SubtitleCount = 10
            },
            ReportPath = "test_sync_report.json"
        };
        var input = new QualityReportInput
        {
            VideoPath = testVideoPath,
            TitleId = "test_011",
            Gender = "male",
            AgeGroup = "18-24",
            SyncCheckResults = syncCheckOutput
        };

        try
        {
            // Act
            var output = await stage.ExecuteAsync(input, null, CancellationToken.None);

            // Assert
            Assert.NotNull(output.Report.AvSync);
            Assert.Equal(35, output.Report.AvSync.MaxDrift);
            Assert.Equal("PASS", output.Report.AvSync.Status);
        }
        finally
        {
            // Cleanup
            CleanupTestFile(testVideoPath);
        }
    }

    [Fact]
    public async Task QualityReportStage_WithDevicePreviewResults_IncludesDeviceMetrics()
    {
        // Arrange
        var stage = new QualityReportStage();
        var testVideoPath = CreateTestVideoFile();
        var devicePreviewOutput = new DevicePreviewOutput
        {
            Previews = new List<DevicePreview>
            {
                new DevicePreview
                {
                    Profile = new DeviceProfile { Name = "iPhone 14" },
                    ReadabilityScore = 85,
                    SafeZoneCompliant = true
                },
                new DevicePreview
                {
                    Profile = new DeviceProfile { Name = "Samsung Galaxy S23" },
                    ReadabilityScore = 80,
                    SafeZoneCompliant = true
                }
            },
            OutputPath = "test_previews"
        };
        var input = new QualityReportInput
        {
            VideoPath = testVideoPath,
            TitleId = "test_012",
            Gender = "female",
            AgeGroup = "25-34",
            DevicePreviewResults = devicePreviewOutput
        };

        try
        {
            // Act
            var output = await stage.ExecuteAsync(input, null, CancellationToken.None);

            // Assert
            Assert.NotNull(output.Report.Subtitles);
            Assert.True(output.Report.Subtitles.Readability > 0);
            Assert.NotNull(output.Report.Devices);
            Assert.Equal("PASS", output.Report.Devices.Ios);
            Assert.Equal("PASS", output.Report.Devices.Android);
        }
        finally
        {
            // Cleanup
            CleanupTestFile(testVideoPath);
        }
    }

    [Fact]
    public async Task QualityReportStage_FailedChecks_SetsOverallStatusToFail()
    {
        // Arrange
        var stage = new QualityReportStage();
        var testVideoPath = CreateTestVideoFile();
        var syncCheckOutput = new SyncCheckOutput
        {
            Result = new SyncCheckResult
            {
                IsSynced = false,
                MaxDriftMs = 75, // Exceeds tolerance
                AverageDriftMs = 60.0,
                SubtitleCount = 10
            },
            ReportPath = "test_sync_report.json"
        };
        var input = new QualityReportInput
        {
            VideoPath = testVideoPath,
            TitleId = "test_013",
            Gender = "male",
            AgeGroup = "18-24",
            SyncCheckResults = syncCheckOutput
        };

        try
        {
            // Act
            var output = await stage.ExecuteAsync(input, null, CancellationToken.None);

            // Assert
            Assert.Equal("FAIL", output.Report.AvSync.Status);
            Assert.Equal("FAIL", output.Report.OverallStatus);
            Assert.NotEmpty(output.Report.Issues);
            Assert.NotEmpty(output.Report.Recommendations);
        }
        finally
        {
            // Cleanup
            CleanupTestFile(testVideoPath);
        }
    }

    #endregion

    #region Helper Methods

    private string CreateTestVideoFile()
    {
        var tempFile = Path.Combine(Path.GetTempPath(), $"test_video_{Guid.NewGuid()}.mp4");
        File.WriteAllText(tempFile, "test video content");
        return tempFile;
    }

    private string CreateTestSubtitleFile()
    {
        var tempFile = Path.Combine(Path.GetTempPath(), $"test_subtitle_{Guid.NewGuid()}.srt");
        var srtContent = @"1
00:00:00,000 --> 00:00:02,000
First subtitle

2
00:00:02,500 --> 00:00:05,000
Second subtitle

3
00:00:05,500 --> 00:00:08,000
Third subtitle
";
        File.WriteAllText(tempFile, srtContent);
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
