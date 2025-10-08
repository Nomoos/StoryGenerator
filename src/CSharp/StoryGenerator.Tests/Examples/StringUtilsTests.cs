using Xunit;

namespace StoryGenerator.Tests.Examples;

/// <summary>
/// Test-Driven Development example: String utilities.
/// Demonstrates Red-Green-Refactor cycle with small, incremental steps.
/// </summary>
public class StringUtilsTests
{
    [Fact]
    public void TruncateWithEllipsis_TextShorterThanMaxLength_ReturnsOriginalText()
    {
        // Arrange
        string text = "Hello World";
        int maxLength = 20;

        // Act
        string result = StringUtils.TruncateWithEllipsis(text, maxLength);

        // Assert
        Assert.Equal("Hello World", result);
    }
}
