namespace StoryGenerator.Tests.Examples;

/// <summary>
/// String utility methods for text processing.
/// Example class for demonstrating TDD principles.
/// </summary>
public static class StringUtils
{
    /// <summary>
    /// Truncates text to a maximum length, adding ellipsis if needed.
    /// </summary>
    /// <param name="text">The text to truncate.</param>
    /// <param name="maxLength">Maximum length of the result.</param>
    /// <returns>Truncated text with ellipsis if needed, or original text if shorter than maxLength.</returns>
    public static string TruncateWithEllipsis(string text, int maxLength)
    {
        if (text.Length <= maxLength)
        {
            return text;
        }

        const string ellipsis = "...";
        int truncateLength = maxLength - ellipsis.Length;
        return text.Substring(0, truncateLength) + ellipsis;
    }
}
