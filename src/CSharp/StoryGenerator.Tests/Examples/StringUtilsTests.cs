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

    [Fact]
    public void TruncateWithEllipsis_TextLongerThanMaxLength_ReturnsTruncatedWithEllipsis()
    {
        // Arrange
        string text = "This is a very long text that needs to be truncated";
        int maxLength = 20;

        // Act
        string result = StringUtils.TruncateWithEllipsis(text, maxLength);

        // Assert
        Assert.Equal("This is a very lo...", result);
        Assert.Equal(20, result.Length);
    }
}
