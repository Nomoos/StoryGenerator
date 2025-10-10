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
        [Fact(Skip = "Requires whisper_subprocess.py script")]
        [Trait("Category", "Integration")]
        public void Constructor_WithDefaultParameters_CreatesInstance()
        {
            // Skip if whisper script not available
            if (!TestHelpers.IsWhisperAvailable())
            {
                return;
            }

            // Arrange & Act
            var client = new WhisperClient();

            // Assert
            Assert.NotNull(client);
        }

        [Fact(Skip = "Requires whisper_subprocess.py script")]
        [Trait("Category", "Integration")]
        public void Constructor_WithCustomModelPath_CreatesInstance()
        {
            // Skip if whisper script not available
            if (!TestHelpers.IsWhisperAvailable())
            {
                return;
            }

            // Arrange & Act
            var client = new WhisperClient("/path/to/model", "large-v3");

            // Assert
            Assert.NotNull(client);
        }

        [Fact(Skip = "Requires whisper_subprocess.py script and faster-whisper")]
        [Trait("Category", "Integration")]
        public async Task TranscribeAsync_WithValidAudioFile_ReturnsTranscription()
        {
            // Skip if whisper script not available
            if (!TestHelpers.IsWhisperAvailable())
            {
                return;
            }

            // Arrange
            var client = new WhisperClient();
            var audioPath = TestHelpers.CreateDummyAudioFile();

            try
            {
                // Act
                var result = await client.TranscribeAsync(audioPath);

                // Assert
                Assert.NotNull(result);
                Assert.NotNull(result.Text);
            }
            finally
            {
                TestHelpers.CleanupFile(audioPath);
            }
        }

        [Fact(Skip = "Requires whisper_subprocess.py script and faster-whisper")]
        [Trait("Category", "Integration")]
        public async Task TranscribeAsync_WithWordTimestamps_ReturnsTimedWords()
        {
            // Skip if whisper script not available
            if (!TestHelpers.IsWhisperAvailable())
            {
                return;
            }

            // Arrange
            var client = new WhisperClient();
            var audioPath = TestHelpers.CreateDummyAudioFile();

            try
            {
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
            finally
            {
                TestHelpers.CleanupFile(audioPath);
            }
        }

        [Fact(Skip = "Requires whisper_subprocess.py script and faster-whisper")]
        [Trait("Category", "Integration")]
        public async Task TranscribeAsync_WithLanguage_UsesSpecifiedLanguage()
        {
            // Skip if whisper script not available
            if (!TestHelpers.IsWhisperAvailable())
            {
                return;
            }

            // Arrange
            var client = new WhisperClient();
            var audioPath = TestHelpers.CreateDummyAudioFile();

            try
            {
                // Act
                var result = await client.TranscribeAsync(
                    audioPath,
                    language: "es",
                    wordTimestamps: false);

                // Assert
                Assert.NotNull(result);
                Assert.Equal("es", result.Language);
            }
            finally
            {
                TestHelpers.CleanupFile(audioPath);
            }
        }

        [Fact(Skip = "Requires whisper_subprocess.py script and faster-whisper")]
        [Trait("Category", "Integration")]
        public async Task TranscribeAsync_WithVADFilter_EnablesVAD()
        {
            // Skip if whisper script not available
            if (!TestHelpers.IsWhisperAvailable())
            {
                return;
            }

            // Arrange
            var client = new WhisperClient();
            var audioPath = TestHelpers.CreateDummyAudioFile();

            try
            {
                // Act
                var result = await client.TranscribeAsync(
                    audioPath,
                    vadFilter: true,
                    wordTimestamps: true);

                // Assert
                Assert.NotNull(result);
            }
            finally
            {
                TestHelpers.CleanupFile(audioPath);
            }
        }

        [Fact(Skip = "Requires whisper_subprocess.py script")]
        [Trait("Category", "Integration")]
        public async Task TranscribeAsync_WithCancellation_ThrowsOperationCanceledException()
        {
            // Skip if whisper script not available
            if (!TestHelpers.IsWhisperAvailable())
            {
                return;
            }

            // Arrange
            var client = new WhisperClient();
            var cts = new CancellationTokenSource();
            cts.Cancel();
            var audioPath = TestHelpers.CreateDummyAudioFile();

            try
            {
                // Act & Assert
                await Assert.ThrowsAnyAsync<OperationCanceledException>(async () =>
                {
                    await client.TranscribeAsync(audioPath, cancellationToken: cts.Token);
                });
            }
            finally
            {
                TestHelpers.CleanupFile(audioPath);
            }
        }

        [Fact(Skip = "Requires whisper_subprocess.py script")]
        [Trait("Category", "Integration")]
        public async Task GetAvailableModelsAsync_ReturnsModelList()
        {
            // Skip if whisper script not available
            if (!TestHelpers.IsWhisperAvailable())
            {
                return;
            }

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
