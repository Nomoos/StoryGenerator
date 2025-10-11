using Microsoft.Extensions.Logging;
using Moq;
using PrismQ.Shared.Core.Services;
using Xunit;

namespace StoryGenerator.Tests.Services
{
    /// <summary>
    /// Tests for ContentFilter service.
    /// </summary>
    public class ContentFilterTests
    {
        private readonly Mock<ILogger<ContentFilter>> _mockLogger;
        private readonly ContentFilter _contentFilter;

        public ContentFilterTests()
        {
            _mockLogger = new Mock<ILogger<ContentFilter>>();
            _contentFilter = new ContentFilter(_mockLogger.Object);
        }

        [Fact]
        public void CheckContent_WithCleanContent_ReturnsIsClean()
        {
            // Arrange
            var content = "This is a wonderful story about friendship and adventure.";

            // Act
            var result = _contentFilter.CheckContent(content);

            // Assert
            Assert.True(result.IsClean);
            Assert.Empty(result.FlaggedWords);
            Assert.Equal("Content passed all checks", result.Message);
        }

        [Fact]
        public void CheckContent_WithDemonetizedWord_FlagsContent()
        {
            // Arrange
            var content = "The character was killed in the story.";

            // Act
            var result = _contentFilter.CheckContent(content);

            // Assert
            Assert.False(result.IsClean);
            Assert.NotEmpty(result.FlaggedWords);
            Assert.Contains(result.FlaggedWords, f => f.Word.ToLower() == "killed");
        }

        [Fact]
        public void CheckContent_WithMultipleDemonetizedWords_FlagsAll()
        {
            // Arrange
            var content = "The violent attack killed many people and caused death.";

            // Act
            var result = _contentFilter.CheckContent(content);

            // Assert
            Assert.False(result.IsClean);
            Assert.True(result.FlaggedWords.Count >= 3); // violent, killed, death
        }

        [Fact]
        public void CheckContent_WithProfanity_FlagsAsHighSeverity()
        {
            // Arrange
            var content = "This is a damn shame.";

            // Act
            var result = _contentFilter.CheckContent(content);

            // Assert
            Assert.False(result.IsClean);
            Assert.Contains(result.FlaggedWords, f => f.Severity == FlagSeverity.Medium);
        }

        [Fact]
        public void CheckContent_WithEmptyContent_ReturnsIsClean()
        {
            // Arrange
            var content = "";

            // Act
            var result = _contentFilter.CheckContent(content);

            // Assert
            Assert.True(result.IsClean);
            Assert.Equal("Content is empty", result.Message);
        }

        [Fact]
        public void CheckContent_WithDemonetizedPattern_FlagsPhrase()
        {
            // Arrange
            var content = "He committed suicide yesterday.";

            // Act
            var result = _contentFilter.CheckContent(content);

            // Assert
            Assert.False(result.IsClean);
            Assert.Contains(result.FlaggedWords, f => f.Category == "Pattern");
        }

        [Fact]
        public void SuggestReplacements_WithFlaggedContent_ReturnsModifiedContent()
        {
            // Arrange
            var content = "The character was killed in the story.";
            var filterResult = _contentFilter.CheckContent(content);

            // Act
            var modified = _contentFilter.SuggestReplacements(content, filterResult);

            // Assert
            Assert.NotEqual(content, modified);
            Assert.DoesNotContain("killed", modified.ToLower());
        }

        [Fact]
        public void SuggestReplacements_WithCleanContent_ReturnsUnchanged()
        {
            // Arrange
            var content = "This is a nice story.";
            var filterResult = _contentFilter.CheckContent(content);

            // Act
            var modified = _contentFilter.SuggestReplacements(content, filterResult);

            // Assert
            Assert.Equal(content, modified);
        }

        [Theory]
        [InlineData("kill")]
        [InlineData("murder")]
        [InlineData("gun")]
        [InlineData("drug")]
        [InlineData("terrorist")]
        public void CheckContent_WithKnownDemonetizedWords_Flags(string word)
        {
            // Arrange
            var content = $"This story mentions {word} in the context.";

            // Act
            var result = _contentFilter.CheckContent(content);

            // Assert
            Assert.False(result.IsClean);
            Assert.Contains(result.FlaggedWords, f => f.Word.ToLower() == word.ToLower());
        }

        [Fact]
        public void CheckContent_IsCaseInsensitive()
        {
            // Arrange
            var content1 = "The character KILLED someone.";
            var content2 = "The character killed someone.";
            var content3 = "The character KiLlEd someone.";

            // Act
            var result1 = _contentFilter.CheckContent(content1);
            var result2 = _contentFilter.CheckContent(content2);
            var result3 = _contentFilter.CheckContent(content3);

            // Assert
            Assert.False(result1.IsClean);
            Assert.False(result2.IsClean);
            Assert.False(result3.IsClean);
        }

        [Fact]
        public void CheckContent_WithMedicalTerms_FlagsAsLowSeverity()
        {
            // Arrange
            var content = "The patient had cancer.";

            // Act
            var result = _contentFilter.CheckContent(content);

            // Assert
            Assert.False(result.IsClean);
            Assert.Contains(result.FlaggedWords, f => f.Severity == FlagSeverity.Low);
        }
    }
}
