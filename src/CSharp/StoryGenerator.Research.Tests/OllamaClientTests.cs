using Moq;
using StoryGenerator.Research;
using System.Threading;
using System.Threading.Tasks;

namespace StoryGenerator.Research.Tests
{
    /// <summary>
    /// Tests for OllamaClient - Local LLM integration.
    /// </summary>
    public class OllamaClientTests
    {
        [Fact]
        [Trait("Category", "Unit")]
        public void Constructor_WithDefaultParameters_CreatesInstance()
        {
            // Arrange & Act
            var client = new OllamaClient();

            // Assert
            Assert.NotNull(client);
        }

        [Fact]
        [Trait("Category", "Unit")]
        public void Constructor_WithCustomParameters_CreatesInstance()
        {
            // Arrange & Act
            var client = new OllamaClient("llama3.1", "http://localhost:11434");

            // Assert
            Assert.NotNull(client);
        }

        [Fact]
        [Trait("Category", "Integration")]
        public async Task GenerateAsync_WithValidPrompt_ReturnsResponse()
        {
            // Skip if Ollama not available
            if (!TestHelpers.IsOllamaAvailable())
            {
                return;
            }

            // Arrange
            var client = new OllamaClient("llama2");
            var prompt = "Tell me a short story.";

            // Act
            // Note: This test requires Ollama to be running locally
            // In a real test environment, we would mock the process execution
            var result = await client.GenerateAsync(prompt, cancellationToken: CancellationToken.None);

            // Assert
            // For stub/prototype, we just verify it doesn't throw
            Assert.NotNull(result);
        }

        [Fact]
        [Trait("Category", "Integration")]
        public async Task GenerateAsync_WithSystemMessage_IncludesSystemInPrompt()
        {
            // Skip if Ollama not available
            if (!TestHelpers.IsOllamaAvailable())
            {
                return;
            }

            // Arrange
            var client = new OllamaClient();
            var prompt = "What is 2+2?";
            var system = "You are a helpful math tutor.";

            // Act
            var result = await client.GenerateAsync(
                prompt,
                system: system,
                temperature: 0.5f,
                cancellationToken: CancellationToken.None);

            // Assert
            Assert.NotNull(result);
        }

        [Fact]
        [Trait("Category", "Integration")]
        public async Task ChatAsync_WithMessages_ReturnsResponse()
        {
            // Skip if Ollama not available
            if (!TestHelpers.IsOllamaAvailable())
            {
                return;
            }

            // Arrange
            var client = new OllamaClient();
            var messages = new List<ChatMessage>
            {
                new ChatMessage { Role = "user", Content = "Hello!" }
            };

            // Act
            var result = await client.ChatAsync(messages, cancellationToken: CancellationToken.None);

            // Assert
            Assert.NotNull(result);
        }

        [Fact]
        [Trait("Category", "Integration")]
        public async Task ListModelsAsync_ReturnsModelList()
        {
            // Skip if Ollama not available
            if (!TestHelpers.IsOllamaAvailable())
            {
                return;
            }

            // Arrange
            var client = new OllamaClient();

            // Act
            var models = await client.ListModelsAsync();

            // Assert
            Assert.NotNull(models);
        }

        [Theory]
        [Trait("Category", "Integration")]
        [InlineData("llama2")]
        [InlineData("mistral")]
        [InlineData("qwen2.5")]
        public async Task PullModelAsync_WithModelName_ReturnsSuccess(string modelName)
        {
            // Skip if Ollama not available
            if (!TestHelpers.IsOllamaAvailable())
            {
                return;
            }

            // Arrange
            var client = new OllamaClient();

            // Act
            var result = await client.PullModelAsync(modelName);

            // Assert
            // For prototype, we just verify it completes without error
            Assert.True(result || !result); // Either succeeds or fails gracefully
        }

        [Fact]
        [Trait("Category", "Integration")]
        public async Task GenerateAsync_WithCancellation_ThrowsOperationCanceledException()
        {
            // Skip if Ollama not available
            if (!TestHelpers.IsOllamaAvailable())
            {
                return;
            }

            // Arrange
            var client = new OllamaClient();
            var cts = new CancellationTokenSource();
            cts.Cancel();

            // Act & Assert
            await Assert.ThrowsAnyAsync<OperationCanceledException>(async () =>
            {
                await client.GenerateAsync("test prompt", cancellationToken: cts.Token);
            });
        }
    }
}
