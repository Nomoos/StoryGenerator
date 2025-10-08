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
        public void Constructor_WithDefaultParameters_CreatesInstance()
        {
            // Arrange & Act
            var client = new FFmpegClient();

            // Assert
            Assert.NotNull(client);
        }

        [Fact]
        public void Constructor_WithCustomPaths_CreatesInstance()
        {
            // Arrange & Act
            var client = new FFmpegClient("/usr/bin/ffmpeg", "/usr/bin/ffprobe");

            // Assert
            Assert.NotNull(client);
        }

        [Fact]
        public async Task NormalizeAudioAsync_WithValidAudio_ReturnsNormalizationResult()
        {
            // Arrange
            var client = new FFmpegClient();
            var inputPath = "input_audio.wav";
            var outputPath = "output_audio.wav";

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

        [Fact]
        public async Task NormalizeAudioAsync_WithCustomLUFS_UsesSpecifiedTarget()
        {
            // Arrange
            var client = new FFmpegClient();
            var inputPath = "input.wav";
            var outputPath = "output.wav";

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

        [Fact]
        public async Task NormalizeAudioAsync_WithTwoPass_PerformsTwoPassNormalization()
        {
            // Arrange
            var client = new FFmpegClient();
            var inputPath = "input.wav";
            var outputPath = "output.wav";

            // Act
            var result = await client.NormalizeAudioAsync(
                inputPath,
                outputPath,
                twoPass: true);

            // Assert
            Assert.NotNull(result);
            Assert.True(result.TwoPass);
        }

        [Fact]
        public async Task CropVideoAsync_ToVerticalFormat_ReturnsSuccess()
        {
            // Arrange
            var client = new FFmpegClient();
            var inputPath = "input_video.mp4";
            var outputPath = "output_video.mp4";

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

        [Fact]
        public async Task EncodeVideoAsync_WithH264_CreatesValidVideo()
        {
            // Arrange
            var client = new FFmpegClient();
            var inputPath = "input.mp4";
            var outputPath = "output.mp4";

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

        [Fact]
        public async Task GetMediaInfoAsync_WithValidFile_ReturnsMediaInfo()
        {
            // Arrange
            var client = new FFmpegClient();
            var filePath = "test_video.mp4";

            // Act
            var info = await client.GetMediaInfoAsync(filePath);

            // Assert
            Assert.NotNull(info);
            Assert.True(info.Duration > 0);
        }

        [Fact]
        public async Task ExtractAudioAsync_FromVideo_CreatesAudioFile()
        {
            // Arrange
            var client = new FFmpegClient();
            var videoPath = "video.mp4";
            var audioPath = "audio.wav";

            // Act
            var result = await client.ExtractAudioAsync(
                videoPath,
                audioPath,
                sampleRate: 48000);

            // Assert
            Assert.NotNull(result);
            Assert.True(result.Success);
        }

        [Fact]
        public async Task NormalizeAudioAsync_WithCancellation_ThrowsOperationCanceledException()
        {
            // Arrange
            var client = new FFmpegClient();
            var cts = new CancellationTokenSource();
            cts.Cancel();

            // Act & Assert
            await Assert.ThrowsAnyAsync<OperationCanceledException>(async () =>
            {
                await client.NormalizeAudioAsync(
                    "input.wav",
                    "output.wav",
                    cancellationToken: cts.Token);
            });
        }
    }
}
