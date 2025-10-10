using Moq;
using StoryGenerator.Research;
using System.Threading;
using System.Threading.Tasks;

namespace StoryGenerator.Research.Tests
{
    /// <summary>
    /// Tests for Orchestrator - Coordinates all research prototype clients.
    /// </summary>
    public class OrchestratorTests
    {
        [Fact]
        [Trait("Category", "Unit")]
        public void Constructor_WithClients_CreatesInstance()
        {
            // Arrange
            var ollamaClient = new Mock<IOllamaClient>();
            var whisperClient = new Mock<IWhisperClient>();
            var ffmpegClient = new Mock<IFFmpegClient>();

            // Act
            var orchestrator = new Orchestrator(
                ollamaClient.Object,
                whisperClient.Object,
                ffmpegClient.Object);

            // Assert
            Assert.NotNull(orchestrator);
        }

        [Fact(Skip = "Requires whisper_subprocess.py script")]
        [Trait("Category", "Integration")]
        public void Constructor_WithoutClients_CreatesDefaultInstances()
        {
            // Skip if dependencies not available
            if (!TestHelpers.IsWhisperAvailable())
            {
                return;
            }

            // Arrange & Act
            var orchestrator = new Orchestrator();

            // Assert
            Assert.NotNull(orchestrator);
        }

        [Fact]
        [Trait("Category", "Unit")]
        public async Task GenerateScriptAsync_WithTitleAndPrompt_ReturnsScript()
        {
            // Arrange
            var ollamaClientMock = new Mock<IOllamaClient>();
            ollamaClientMock
                .Setup(x => x.GenerateAsync(
                    It.IsAny<string>(),
                    It.IsAny<string>(),
                    It.IsAny<float>(),
                    It.IsAny<int?>(),
                    It.IsAny<CancellationToken>()))
                .ReturnsAsync("Generated script content.");

            var orchestrator = new Orchestrator(
                ollamaClientMock.Object,
                new Mock<IWhisperClient>().Object,
                new Mock<IFFmpegClient>().Object);

            // Act
            var script = await orchestrator.GenerateScriptAsync(
                "Story Title",
                "Generate a story about...");

            // Assert
            Assert.NotNull(script);
            // The method currently returns a placeholder
            Assert.Contains("Story Title", script);
            Assert.Contains("Generate a story about...", script);
        }

        [Fact]
        [Trait("Category", "Unit")]
        public async Task TranscribeAndNormalizeAsync_WithAudioFile_ReturnsResult()
        {
            // Arrange
            var whisperClientMock = new Mock<IWhisperClient>();
            whisperClientMock
                .Setup(x => x.TranscribeAsync(
                    It.IsAny<string>(),
                    It.IsAny<string>(),
                    It.IsAny<string>(),
                    It.IsAny<bool>(),
                    It.IsAny<bool>(),
                    It.IsAny<CancellationToken>()))
                .ReturnsAsync(new TranscriptionResult
                {
                    Text = "Transcribed text",
                    Language = "en"
                });

            whisperClientMock
                .Setup(x => x.TranscribeToSrtAsync(
                    It.IsAny<string>(),
                    It.IsAny<string>(),
                    It.IsAny<string>(),
                    It.IsAny<int>(),
                    It.IsAny<CancellationToken>()))
                .ReturnsAsync("1\n00:00:00,000 --> 00:00:01,000\nTranscribed text\n");

            var ffmpegClientMock = new Mock<IFFmpegClient>();
            ffmpegClientMock
                .Setup(x => x.NormalizeAudioAsync(
                    It.IsAny<string>(),
                    It.IsAny<string>(),
                    It.IsAny<double>(),
                    It.IsAny<double>(),
                    It.IsAny<double>(),
                    It.IsAny<bool>(),
                    It.IsAny<int>(),
                    It.IsAny<CancellationToken>()))
                .ReturnsAsync(new NormalizationResult
                {
                    Success = true,
                    OutputPath = "normalized.wav"
                });

            ffmpegClientMock
                .Setup(x => x.GetAudioInfoAsync(
                    It.IsAny<string>(),
                    It.IsAny<CancellationToken>()))
                .ReturnsAsync(new AudioInfo
                {
                    Duration = 10.0,
                    SampleRate = 48000,
                    Channels = 2,
                    Codec = "pcm_s16le"
                });

            var orchestrator = new Orchestrator(
                new Mock<IOllamaClient>().Object,
                whisperClientMock.Object,
                ffmpegClientMock.Object);

            // Create temporary test files
            var inputPath = TestHelpers.CreateDummyAudioFile("orchestrator_input.wav");
            var outputPath = Path.Combine(Path.GetTempPath(), "orchestrator_output.wav");

            try
            {
                // Act
                var result = await orchestrator.TranscribeAndNormalizeAsync(
                    inputPath,
                    outputPath);

                // Assert
                Assert.NotNull(result);
                Assert.True(result.Success);
                Assert.NotNull(result.TranscriptionText);
                Assert.NotNull(result.NormalizedAudioPath);
            }
            finally
            {
                TestHelpers.CleanupFile(inputPath);
                TestHelpers.CleanupFile(outputPath);
            }
        }

        [Fact]
        [Trait("Category", "Unit")]
        public async Task ProcessVideoAsync_WithInputFile_ReturnsProcessedVideo()
        {
            // Arrange
            var ffmpegClientMock = new Mock<IFFmpegClient>();
            ffmpegClientMock
                .Setup(x => x.CropVideoAsync(
                    It.IsAny<string>(),
                    It.IsAny<string>(),
                    It.IsAny<int>(),
                    It.IsAny<int>(),
                    It.IsAny<string>(),
                    It.IsAny<CancellationToken>()))
                .ReturnsAsync(new VideoProcessingResult
                {
                    Success = true,
                    OutputPath = "cropped.mp4",
                    Width = 1080,
                    Height = 1920
                });

            var orchestrator = new Orchestrator(
                new Mock<IOllamaClient>().Object,
                new Mock<IWhisperClient>().Object,
                ffmpegClientMock.Object);

            // Act
            var result = await orchestrator.ProcessVideoAsync(
                "input.mp4",
                "output.mp4");

            // Assert
            Assert.NotNull(result);
            Assert.True(result.Success);
        }

        [Fact]
        [Trait("Category", "Unit")]
        public async Task GenerateIdeasAsync_WithTopic_ReturnsIdeas()
        {
            // Arrange
            var ollamaClientMock = new Mock<IOllamaClient>();
            ollamaClientMock
                .Setup(x => x.GenerateAsync(
                    It.IsAny<string>(),
                    It.IsAny<string>(),
                    It.IsAny<float>(),
                    It.IsAny<int?>(),
                    It.IsAny<CancellationToken>()))
                .ReturnsAsync("1. Idea one\n2. Idea two\n3. Idea three");

            var orchestrator = new Orchestrator(
                ollamaClientMock.Object,
                new Mock<IWhisperClient>().Object,
                new Mock<IFFmpegClient>().Object);

            // Act
            var ideas = await orchestrator.GenerateIdeasAsync(
                "Technology trends",
                count: 20);

            // Assert
            Assert.NotNull(ideas);
            Assert.NotEmpty(ideas);
        }

        [Fact]
        [Trait("Category", "Unit")]
        public async Task ScoreTitleAsync_WithTitle_ReturnsScore()
        {
            // Arrange
            var ollamaClientMock = new Mock<IOllamaClient>();
            ollamaClientMock
                .Setup(x => x.GenerateAsync(
                    It.IsAny<string>(),
                    It.IsAny<string>(),
                    It.IsAny<float>(),
                    It.IsAny<int?>(),
                    It.IsAny<CancellationToken>()))
                .ReturnsAsync("Score: 85/100\nNovelty: 20\nEmotional: 18");

            var orchestrator = new Orchestrator(
                ollamaClientMock.Object,
                new Mock<IWhisperClient>().Object,
                new Mock<IFFmpegClient>().Object);

            // Act
            var score = await orchestrator.ScoreTitleAsync("Amazing Story Title");

            // Assert
            Assert.NotNull(score);
            Assert.True(score.Total >= 0 && score.Total <= 100);
        }
    }
}
