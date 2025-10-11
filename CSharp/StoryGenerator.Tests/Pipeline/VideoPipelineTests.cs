using System;
using System.IO;
using System.Threading.Tasks;
using StoryGenerator.Pipeline.Config;
using StoryGenerator.Pipeline.Services;
using Xunit;

namespace StoryGenerator.Tests.Pipeline;

public class VideoPipelineTests
{
    [Fact]
    public void SceneAnalysisService_Constructor_InitializesSuccessfully()
    {
        // Arrange
        var paths = new PathsConfig
        {
            StoryRoot = "./test_stories",
            Titles = "titles",
            Scenes = "scenes",
            Voiceover = "voiceover"
        };

        // Act
        var service = new SceneAnalysisService(paths);

        // Assert
        Assert.NotNull(service);
    }

    [Fact]
    public void SceneDescriptionService_Constructor_InitializesSuccessfully()
    {
        // Arrange
        var paths = new PathsConfig
        {
            StoryRoot = "./test_stories",
            Scenes = "scenes"
        };

        // Act
        var service = new SceneDescriptionService(paths);

        // Assert
        Assert.NotNull(service);
    }

    [Fact]
    public void VideoGenerationService_Constructor_LTXMode_InitializesSuccessfully()
    {
        // Arrange
        var paths = new PathsConfig
        {
            StoryRoot = "./test_stories",
            Videos = "videos",
            Scenes = "scenes"
        };
        var videoConfig = new VideoConfig
        {
            Resolution = new Resolution { Width = 1080, Height = 1920 },
            Fps = 30
        };

        // Act
        var service = new VideoGenerationService(paths, videoConfig, useLTX: true);

        // Assert
        Assert.NotNull(service);
    }

    [Fact]
    public void VideoGenerationService_Constructor_KeyframeMode_InitializesSuccessfully()
    {
        // Arrange
        var paths = new PathsConfig
        {
            StoryRoot = "./test_stories",
            Videos = "videos",
            Scenes = "scenes"
        };
        var videoConfig = new VideoConfig
        {
            Resolution = new Resolution { Width = 1080, Height = 1920 },
            Fps = 30
        };

        // Act
        var service = new VideoGenerationService(paths, videoConfig, useLTX: false);

        // Assert
        Assert.NotNull(service);
    }

    [Fact]
    public void VideoCompositionService_Constructor_InitializesSuccessfully()
    {
        // Arrange
        var paths = new PathsConfig
        {
            StoryRoot = "./test_stories",
            Final = "final",
            Voiceover = "voiceover",
            Titles = "titles"
        };
        var videoConfig = new VideoConfig
        {
            Codec = "libx264",
            AudioCodec = "aac"
        };

        // Act
        var service = new VideoCompositionService(paths, videoConfig);

        // Assert
        Assert.NotNull(service);
    }

    [Fact]
    public async Task SceneAnalysisService_AnalyzeScenesAsync_MissingFile_ThrowsException()
    {
        // Arrange
        var paths = new PathsConfig
        {
            StoryRoot = "./test_stories",
            Titles = "titles",
            Scenes = "scenes",
            Voiceover = "voiceover"
        };
        var service = new SceneAnalysisService(paths);

        // Act & Assert
        await Assert.ThrowsAsync<FileNotFoundException>(
            async () => await service.AnalyzeScenesAsync("nonexistent_story"));
    }

    [Fact]
    public async Task SceneDescriptionService_DescribeScenesAsync_MissingFile_ThrowsException()
    {
        // Arrange
        var paths = new PathsConfig
        {
            StoryRoot = "./test_stories",
            Scenes = "scenes"
        };
        var service = new SceneDescriptionService(paths);

        // Act & Assert
        await Assert.ThrowsAsync<FileNotFoundException>(
            async () => await service.DescribeScenesAsync("nonexistent_story"));
    }

    [Fact]
    public async Task VideoGenerationService_GenerateVideoClipsAsync_MissingFile_ThrowsException()
    {
        // Arrange
        var paths = new PathsConfig
        {
            StoryRoot = "./test_stories",
            Videos = "videos",
            Scenes = "scenes"
        };
        var videoConfig = new VideoConfig();
        var service = new VideoGenerationService(paths, videoConfig, useLTX: true);

        // Act & Assert
        await Assert.ThrowsAsync<FileNotFoundException>(
            async () => await service.GenerateVideoClipsAsync("nonexistent_story"));
    }
}
