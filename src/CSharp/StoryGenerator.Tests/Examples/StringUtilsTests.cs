using Xunit;

namespace StoryGenerator.Tests.Examples;

/// <summary>
/// Test-Driven Development example: String utilities.
/// Demonstrates Red-Green-Refactor cycle with small, incremental steps.
/// </summary>
public class StringUtilsTests
{
    [Theory]
    [InlineData("Hello World", 20, "Hello World")]
    [InlineData("Short", 100, "Short")]
    [InlineData("Exactly twenty c", 16, "Exactly twenty c")]
    public void TruncateWithEllipsis_TextShorterOrEqualToMaxLength_ReturnsOriginalText(
        string text,
        int maxLength,
        string expected)
    {
        // Act
        string result = StringUtils.TruncateWithEllipsis(text, maxLength);

        // Assert
        Assert.Equal(expected, result);
    }

    [Theory]
    [InlineData("This is a very long text that needs to be truncated", 20, "This is a very lo...")]
    [InlineData("Another long text for testing purposes", 15, "Another long...")]
    [InlineData("Short text but needs truncation", 10, "Short t...")]
    public void TruncateWithEllipsis_TextLongerThanMaxLength_ReturnsTruncatedWithEllipsis(
        string text,
        int maxLength,
        string expected)
    {
        // Act
        string result = StringUtils.TruncateWithEllipsis(text, maxLength);

        // Assert
        Assert.Equal(expected, result);
        Assert.Equal(maxLength, result.Length);
    }
}
