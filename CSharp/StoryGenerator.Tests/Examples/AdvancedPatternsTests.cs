using System;
using System.Threading;
using System.Threading.Tasks;
using Microsoft.Extensions.Logging;
using Moq;
using Xunit;

namespace StoryGenerator.Tests.Examples
{
    /// <summary>
    /// Simple service for demonstrating testing patterns.
    /// </summary>
    public class TestService
    {
        private readonly ILogger<TestService> _logger;

        public TestService(ILogger<TestService> logger)
        {
            _logger = logger ?? throw new ArgumentNullException(nameof(logger));
        }

        public async Task<string> ProcessAsync(
            string input,
            CancellationToken cancellationToken = default
        )
        {
            ArgumentNullException.ThrowIfNull(input);

            // Simulate async work
            await Task.Delay(10, cancellationToken);

            return $"PROCESSED: {input.ToUpperInvariant()}";
        }

        public void LogMessage(string message)
        {
            _logger.LogInformation("{Message}", message);
        }

        public void LogError(string message)
        {
            _logger.LogError("{Message}", message);
        }

        public void ValidateInput(string input)
        {
            ArgumentNullException.ThrowIfNull(input);

            if (string.IsNullOrWhiteSpace(input))
            {
                throw new ArgumentException("Input cannot be empty", nameof(input));
            }
        }
    }

    /// <summary>
    /// Advanced C# testing patterns demonstrating:
    /// - Async/await testing
    /// - Mocking with Moq
    /// - IDisposable pattern for test cleanup
    /// - CancellationToken propagation
    /// - Exception testing
    /// </summary>
    public class AdvancedPatternsTests : IDisposable
    {
        private readonly Mock<ILogger<TestService>> _mockLogger;
        private readonly TestService _service;

        public AdvancedPatternsTests()
        {
            _mockLogger = new Mock<ILogger<TestService>>();
            _service = new TestService(_mockLogger.Object);
        }

        public void Dispose()
        {
            // Cleanup code runs after each test
            _mockLogger.Reset();
        }

        #region Async/Await Testing

        [Fact]
        public async Task ProcessAsync_ValidInput_ReturnsProcessedResult()
        {
            // Arrange
            var input = "test input";

            // Act
            var result = await _service.ProcessAsync(input);

            // Assert
            Assert.Equal("PROCESSED: TEST INPUT", result);
        }

        [Fact]
        public async Task ProcessAsync_WithCancellation_ThrowsTaskCanceledException()
        {
            // Arrange
            var cts = new CancellationTokenSource();
            cts.Cancel(); // Cancel immediately

            // Act & Assert
            await Assert.ThrowsAnyAsync<OperationCanceledException>(
                () => _service.ProcessAsync("test", cts.Token)
            );
        }

        [Theory]
        [InlineData("hello", "PROCESSED: HELLO")]
        [InlineData("world", "PROCESSED: WORLD")]
        [InlineData("", "PROCESSED: ")]
        public async Task ProcessAsync_VariousInputs_ReturnsExpectedResults(
            string input,
            string expected
        )
        {
            // Act
            var result = await _service.ProcessAsync(input);

            // Assert
            Assert.Equal(expected, result);
        }

        #endregion

        #region Mocking with Moq

        [Fact]
        public void LogMessage_WhenCalled_LogsToLogger()
        {
            // Arrange
            var message = "Test message";

            // Act
            _service.LogMessage(message);

            // Assert - Verify logger was called
            _mockLogger.Verify(
                x => x.Log(
                    LogLevel.Information,
                    It.IsAny<EventId>(),
                    It.Is<It.IsAnyType>((v, t) => v.ToString()!.Contains(message)),
                    It.IsAny<Exception>(),
                    It.IsAny<Func<It.IsAnyType, Exception?, string>>()
                ),
                Times.Once
            );
        }

        [Fact]
        public void LogError_WhenCalled_LogsErrorLevel()
        {
            // Arrange
            var errorMessage = "Error occurred";

            // Act
            _service.LogError(errorMessage);

            // Assert
            _mockLogger.Verify(
                x => x.Log(
                    LogLevel.Error,
                    It.IsAny<EventId>(),
                    It.IsAny<It.IsAnyType>(),
                    It.IsAny<Exception>(),
                    It.IsAny<Func<It.IsAnyType, Exception?, string>>()
                ),
                Times.Once
            );
        }

        #endregion

        #region Exception Testing

        [Fact]
        public void ValidateInput_NullInput_ThrowsArgumentNullException()
        {
            // Act & Assert
            var exception = Assert.Throws<ArgumentNullException>(() => _service.ValidateInput(null!));
            Assert.Contains("input", exception.ParamName);
        }

        [Fact]
        public void ValidateInput_EmptyInput_ThrowsArgumentException()
        {
            // Act & Assert
            var exception = Assert.Throws<ArgumentException>(() => _service.ValidateInput(string.Empty));
            Assert.Contains("cannot be empty", exception.Message);
        }

        [Theory]
        [InlineData("valid")]
        [InlineData("also valid")]
        public void ValidateInput_ValidInput_DoesNotThrow(string input)
        {
            // Act & Assert - Should not throw
            var exception = Record.Exception(() => _service.ValidateInput(input));
            Assert.Null(exception);
        }

        #endregion
    }

    /// <summary>
    /// Collection fixture example for sharing expensive setup across multiple test classes.
    /// </summary>
    [CollectionDefinition("Database collection")]
    public class DatabaseCollection : ICollectionFixture<DatabaseFixture>
    {
        // This class is never instantiated
    }

    /// <summary>
    /// Fixture that is created once and shared across all tests in the collection.
    /// </summary>
    public class DatabaseFixture : IDisposable
    {
        public DatabaseFixture()
        {
            // Expensive setup code here (e.g., database connection)
            ConnectionString = "mock://connection";
        }

        public string ConnectionString { get; }

        public void Dispose()
        {
            // Cleanup expensive resources
        }
    }

    /// <summary>
    /// Example test class using a collection fixture.
    /// </summary>
    [Collection("Database collection")]
    public class DatabaseTests
    {
        private readonly DatabaseFixture _fixture;

        public DatabaseTests(DatabaseFixture fixture)
        {
            _fixture = fixture;
        }

        [Fact]
        public void Database_HasConnectionString()
        {
            Assert.NotNull(_fixture.ConnectionString);
            Assert.Contains("connection", _fixture.ConnectionString);
        }
    }
}
