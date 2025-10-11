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
    /// <exception cref="ArgumentNullException">Thrown when text is null.</exception>
    /// <exception cref="ArgumentException">Thrown when maxLength is less than or equal to 0.</exception>
    public static string TruncateWithEllipsis(string text, int maxLength)
    {
        ArgumentNullException.ThrowIfNull(text);
        
        if (maxLength <= 0)
        {
            throw new ArgumentException("Maximum length must be greater than 0.", nameof(maxLength));
        }

        if (text.Length <= maxLength)
        {
            return text;
        }

        const string ellipsis = "...";
        int truncateLength = maxLength - ellipsis.Length;
        return text.Substring(0, truncateLength) + ellipsis;
    }
}
