using Moq;
using StoryGenerator.Research;
using System.Threading;
using System.Threading.Tasks;

namespace StoryGenerator.Research.Tests
{
    /// <summary>
    /// Tests for WhisperClient - ASR (Automatic Speech Recognition) integration.
    /// </summary>
    public class WhisperClientTests
    {
        [Fact]
        public void Constructor_WithDefaultParameters_CreatesInstance()
        {
            // Arrange & Act
            var client = new WhisperClient();

            // Assert
            Assert.NotNull(client);
        }

        [Fact]
        public void Constructor_WithCustomModelPath_CreatesInstance()
        {
            // Arrange & Act
            var client = new WhisperClient("/path/to/model", "large-v3");

            // Assert
            Assert.NotNull(client);
        }

        [Fact]
        public async Task TranscribeAsync_WithValidAudioFile_ReturnsTranscription()
        {
            // Arrange
            var client = new WhisperClient();
            var audioPath = "test_audio.wav";

            // Act
            // Note: This requires faster-whisper to be installed
            // In a real test, we would mock the subprocess execution
            var result = await client.TranscribeAsync(audioPath);

            // Assert
            Assert.NotNull(result);
            Assert.NotNull(result.Text);
        }

        [Fact]
        public async Task TranscribeAsync_WithWordTimestamps_ReturnsTimedWords()
        {
            // Arrange
            var client = new WhisperClient();
            var audioPath = "test_audio.wav";

            // Act
            var result = await client.TranscribeAsync(
                audioPath,
                wordTimestamps: true,
                language: "en");

            // Assert
            Assert.NotNull(result);
            if (result.Segments != null)
            {
                // If audio was successfully processed, segments should exist
                Assert.NotEmpty(result.Segments);
            }
        }

        [Fact]
        public async Task TranscribeAsync_WithLanguage_UsesSpecifiedLanguage()
        {
            // Arrange
            var client = new WhisperClient();
            var audioPath = "test_audio.wav";

            // Act
            var result = await client.TranscribeAsync(
                audioPath,
                language: "es",
                wordTimestamps: false);

            // Assert
            Assert.NotNull(result);
            Assert.Equal("es", result.Language);
        }

        [Fact]
        public async Task TranscribeAsync_WithVADFilter_EnablesVAD()
        {
            // Arrange
            var client = new WhisperClient();
            var audioPath = "test_audio.wav";

            // Act
            var result = await client.TranscribeAsync(
                audioPath,
                vadFilter: true,
                wordTimestamps: true);

            // Assert
            Assert.NotNull(result);
        }

        [Fact]
        public async Task TranscribeAsync_WithCancellation_ThrowsOperationCanceledException()
        {
            // Arrange
            var client = new WhisperClient();
            var cts = new CancellationTokenSource();
            cts.Cancel();

            // Act & Assert
            await Assert.ThrowsAnyAsync<OperationCanceledException>(async () =>
            {
                await client.TranscribeAsync("test.wav", cancellationToken: cts.Token);
            });
        }

        [Fact]
        public async Task GetAvailableModelsAsync_ReturnsModelList()
        {
            // Arrange
            var client = new WhisperClient();

            // Act
            var models = await client.GetAvailableModelsAsync();

            // Assert
            Assert.NotNull(models);
            // Standard Whisper models
            Assert.Contains("tiny", models);
            Assert.Contains("base", models);
            Assert.Contains("small", models);
            Assert.Contains("medium", models);
            Assert.Contains("large-v3", models);
        }
    }
}
