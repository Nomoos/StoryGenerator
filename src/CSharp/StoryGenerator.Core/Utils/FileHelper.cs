using System.IO;
using System.Text.RegularExpressions;

namespace StoryGenerator.Core.Utils;

/// <summary>
/// Utility class for file operations and path management.
/// Ported from Python Tools/Utils.py with C# enhancements.
/// </summary>
public static class FileHelper
{
    /// <summary>
    /// Sanitizes a filename by removing or replacing invalid characters.
    /// </summary>
    /// <param name="filename">The filename to sanitize.</param>
    /// <returns>A sanitized filename safe for filesystem use.</returns>
    public static string SanitizeFilename(string filename)
    {
        if (string.IsNullOrWhiteSpace(filename))
            return "unnamed";

        // Remove invalid path characters
        var invalidChars = new string(Path.GetInvalidFileNameChars()) + new string(Path.GetInvalidPathChars());
        var pattern = $"[{Regex.Escape(invalidChars)}]";
        var sanitized = Regex.Replace(filename, pattern, "");

        // Replace spaces with underscores and trim
        sanitized = sanitized.Trim().Replace(" ", "_");

        // Remove multiple consecutive underscores
        sanitized = Regex.Replace(sanitized, "_+", "_");

        // Ensure the result is not empty
        return string.IsNullOrWhiteSpace(sanitized) ? "unnamed" : sanitized;
    }

    /// <summary>
    /// Gets the full language name from a language code.
    /// </summary>
    /// <param name="languageCode">The language code (e.g., "en", "es").</param>
    /// <returns>The full language name.</returns>
    public static string GetLanguageName(string languageCode)
    {
        var languages = new Dictionary<string, string>(StringComparer.OrdinalIgnoreCase)
        {
            { "en", "English" },
            { "es", "Spanish" },
            { "fr", "French" },
            { "de", "German" },
            { "it", "Italian" },
            { "pt", "Portuguese" },
            { "ja", "Japanese" },
            { "ko", "Korean" },
            { "zh", "Chinese" },
            { "ar", "Arabic" },
            { "hi", "Hindi" },
            { "ru", "Russian" }
        };

        return languages.GetValueOrDefault(languageCode, "English");
    }

    /// <summary>
    /// Ensures a directory exists, creating it if necessary.
    /// </summary>
    /// <param name="path">The directory path.</param>
    public static void EnsureDirectoryExists(string path)
    {
        if (!Directory.Exists(path))
        {
            Directory.CreateDirectory(path);
        }
    }

    /// <summary>
    /// Deletes a directory and all its contents if it exists.
    /// </summary>
    /// <param name="path">The directory path.</param>
    public static void DeleteDirectoryIfExists(string path)
    {
        if (Directory.Exists(path))
        {
            Directory.Delete(path, recursive: true);
        }
    }

    /// <summary>
    /// Moves a directory from source to destination, optionally overwriting.
    /// </summary>
    /// <param name="sourcePath">Source directory path.</param>
    /// <param name="destinationPath">Destination directory path.</param>
    /// <param name="overwrite">Whether to overwrite if destination exists.</param>
    public static void MoveDirectory(string sourcePath, string destinationPath, bool overwrite = true)
    {
        if (!Directory.Exists(sourcePath))
        {
            throw new DirectoryNotFoundException($"Source directory not found: {sourcePath}");
        }

        if (overwrite && Directory.Exists(destinationPath))
        {
            Directory.Delete(destinationPath, recursive: true);
        }

        Directory.Move(sourcePath, destinationPath);
    }

    /// <summary>
    /// Reads all text from a file asynchronously.
    /// </summary>
    /// <param name="filePath">Path to the file.</param>
    /// <returns>The file contents as a string.</returns>
    public static async Task<string> ReadFileAsync(string filePath)
    {
        if (!File.Exists(filePath))
        {
            throw new FileNotFoundException($"File not found: {filePath}");
        }

        return await File.ReadAllTextAsync(filePath);
    }

    /// <summary>
    /// Writes text to a file asynchronously.
    /// </summary>
    /// <param name="filePath">Path to the file.</param>
    /// <param name="content">Content to write.</param>
    public static async Task WriteFileAsync(string filePath, string content)
    {
        var directory = Path.GetDirectoryName(filePath);
        if (!string.IsNullOrEmpty(directory))
        {
            EnsureDirectoryExists(directory);
        }

        await File.WriteAllTextAsync(filePath, content);
    }
}
