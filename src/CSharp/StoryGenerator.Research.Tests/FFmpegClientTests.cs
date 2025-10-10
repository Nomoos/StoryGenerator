using Moq;
using StoryGenerator.Research;
using System.Threading;
using System.Threading.Tasks;

namespace StoryGenerator.Research.Tests
{
    /// <summary>
    /// Tests for FFmpegClient - Audio/Video processing integration.
    /// </summary>
    public class FFmpegClientTests
    {
        [Fact]
        [Trait("Category", "Unit")]
        public void Constructor_WithDefaultParameters_CreatesInstance()
        {
            // Arrange & Act
            var client = new FFmpegClient();

            // Assert
            Assert.NotNull(client);
        }

        [Fact]
        [Trait("Category", "Unit")]
        public void Constructor_WithCustomPaths_CreatesInstance()
        {
            // Arrange & Act
            var client = new FFmpegClient("/usr/bin/ffmpeg", "/usr/bin/ffprobe");

            // Assert
            Assert.NotNull(client);
        }

        [Fact(Skip = "Requires FFmpeg to be installed")]
        [Trait("Category", "Integration")]
        public async Task NormalizeAudioAsync_WithValidAudio_ReturnsNormalizationResult()
        {
            // Skip if FFmpeg not available
            if (!TestHelpers.IsFFmpegAvailable())
            {
                return;
            }

            // Arrange
            var client = new FFmpegClient();
            var inputPath = TestHelpers.CreateDummyAudioFile("input_audio.wav");
            var outputPath = Path.Combine(Path.GetTempPath(), "output_audio.wav");

            try
            {
                // Act
                // Note: This requires FFmpeg to be installed
                // In a real test, we would mock the process execution
                var result = await client.NormalizeAudioAsync(
                    inputPath,
                    outputPath,
                    targetLufs: -14.0);

                // Assert
                Assert.NotNull(result);
            }
            finally
            {
                TestHelpers.CleanupFile(inputPath);
                TestHelpers.CleanupFile(outputPath);
            }
        }

        [Fact(Skip = "Requires FFmpeg to be installed")]
        [Trait("Category", "Integration")]
        public async Task NormalizeAudioAsync_WithCustomLUFS_UsesSpecifiedTarget()
        {
            // Skip if FFmpeg not available
            if (!TestHelpers.IsFFmpegAvailable())
            {
                return;
            }

            // Arrange
            var client = new FFmpegClient();
            var inputPath = TestHelpers.CreateDummyAudioFile("input.wav");
            var outputPath = Path.Combine(Path.GetTempPath(), "output.wav");

            try
            {
                // Act
                var result = await client.NormalizeAudioAsync(
                    inputPath,
                    outputPath,
                    targetLufs: -16.0,
                    targetLra: 11.0,
                    targetTp: -2.0);

                // Assert
                Assert.NotNull(result);
                Assert.Equal(-16.0, result.TargetLufs);
            }
            finally
            {
                TestHelpers.CleanupFile(inputPath);
                TestHelpers.CleanupFile(outputPath);
            }
        }

        [Fact(Skip = "Requires FFmpeg to be installed")]
        [Trait("Category", "Integration")]
        public async Task NormalizeAudioAsync_WithTwoPass_PerformsTwoPassNormalization()
        {
            // Skip if FFmpeg not available
            if (!TestHelpers.IsFFmpegAvailable())
            {
                return;
            }

            // Arrange
            var client = new FFmpegClient();
            var inputPath = TestHelpers.CreateDummyAudioFile("input.wav");
            var outputPath = Path.Combine(Path.GetTempPath(), "output.wav");

            try
            {
                // Act
                var result = await client.NormalizeAudioAsync(
                    inputPath,
                    outputPath,
                    twoPass: true);

                // Assert
                Assert.NotNull(result);
                Assert.True(result.TwoPass);
            }
            finally
            {
                TestHelpers.CleanupFile(inputPath);
                TestHelpers.CleanupFile(outputPath);
            }
        }

        [Fact(Skip = "Requires FFmpeg to be installed")]
        [Trait("Category", "Integration")]
        public async Task CropVideoAsync_ToVerticalFormat_ReturnsSuccess()
        {
            // Skip if FFmpeg not available
            if (!TestHelpers.IsFFmpegAvailable())
            {
                return;
            }

            // Arrange
            var client = new FFmpegClient();
            var inputPath = TestHelpers.CreateDummyVideoFile("input_video.mp4");
            var outputPath = Path.Combine(Path.GetTempPath(), "output_video.mp4");

            try
            {
                // Act
                var result = await client.CropVideoAsync(
                    inputPath,
                    outputPath,
                    width: 1080,
                    height: 1920);

                // Assert
                Assert.NotNull(result);
                Assert.True(result.Success);
                Assert.Equal(1080, result.Width);
                Assert.Equal(1920, result.Height);
            }
            finally
            {
                TestHelpers.CleanupFile(inputPath);
                TestHelpers.CleanupFile(outputPath);
            }
        }

        [Fact(Skip = "Requires FFmpeg to be installed")]
        [Trait("Category", "Integration")]
        public async Task EncodeVideoAsync_WithH264_CreatesValidVideo()
        {
            // Skip if FFmpeg not available
            if (!TestHelpers.IsFFmpegAvailable())
            {
                return;
            }

            // Arrange
            var client = new FFmpegClient();
            var inputPath = TestHelpers.CreateDummyVideoFile("input.mp4");
            var outputPath = Path.Combine(Path.GetTempPath(), "output.mp4");

            try
            {
                // Act
                var result = await client.EncodeVideoAsync(
                    inputPath,
                    outputPath,
                    codec: "libx264",
                    preset: "medium",
                    crf: 23);

                // Assert
                Assert.NotNull(result);
                Assert.True(result.Success);
            }
            finally
            {
                TestHelpers.CleanupFile(inputPath);
                TestHelpers.CleanupFile(outputPath);
            }
        }

        [Fact(Skip = "Requires FFmpeg to be installed")]
        [Trait("Category", "Integration")]
        public async Task GetMediaInfoAsync_WithValidFile_ReturnsMediaInfo()
        {
            // Skip if FFmpeg not available
            if (!TestHelpers.IsFFmpegAvailable())
            {
                return;
            }

            // Arrange
            var client = new FFmpegClient();
            var filePath = TestHelpers.CreateDummyVideoFile("test_video.mp4");

            try
            {
                // Act
                var info = await client.GetMediaInfoAsync(filePath);

                // Assert
                Assert.NotNull(info);
                Assert.True(info.Duration > 0);
            }
            finally
            {
                TestHelpers.CleanupFile(filePath);
            }
        }

        [Fact(Skip = "Requires FFmpeg to be installed")]
        [Trait("Category", "Integration")]
        public async Task ExtractAudioAsync_FromVideo_CreatesAudioFile()
        {
            // Skip if FFmpeg not available
            if (!TestHelpers.IsFFmpegAvailable())
            {
                return;
            }

            // Arrange
            var client = new FFmpegClient();
            var videoPath = TestHelpers.CreateDummyVideoFile("video.mp4");
            var audioPath = Path.Combine(Path.GetTempPath(), "audio.wav");

            try
            {
                // Act
                var result = await client.ExtractAudioAsync(
                    videoPath,
                    audioPath,
                    sampleRate: 48000);

                // Assert
                Assert.NotNull(result);
                Assert.True(result.Success);
            }
            finally
            {
                TestHelpers.CleanupFile(videoPath);
                TestHelpers.CleanupFile(audioPath);
            }
        }

        [Fact(Skip = "Requires FFmpeg to be installed")]
        [Trait("Category", "Integration")]
        public async Task NormalizeAudioAsync_WithCancellation_ThrowsOperationCanceledException()
        {
            // Skip if FFmpeg not available
            if (!TestHelpers.IsFFmpegAvailable())
            {
                return;
            }

            // Arrange
            var client = new FFmpegClient();
            var inputPath = TestHelpers.CreateDummyAudioFile("input.wav");
            var outputPath = Path.Combine(Path.GetTempPath(), "output.wav");
            var cts = new CancellationTokenSource();
            cts.Cancel();

            try
            {
                // Act & Assert
                await Assert.ThrowsAnyAsync<OperationCanceledException>(async () =>
                {
                    await client.NormalizeAudioAsync(
                        inputPath,
                        outputPath,
                        cancellationToken: cts.Token);
                });
            }
            finally
            {
                TestHelpers.CleanupFile(inputPath);
                TestHelpers.CleanupFile(outputPath);
            }
        }
    }
}
