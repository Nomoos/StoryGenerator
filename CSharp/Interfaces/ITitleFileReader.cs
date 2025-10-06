using System.Threading;
using System.Threading.Tasks;

namespace StoryGenerator.Interfaces
{
    /// <summary>
    /// Interface for finding and extracting titles from various file formats.
    /// Supports JSON, text, and nested directory structures.
    /// </summary>
    public interface ITitleFileReader
    {
        /// <summary>
        /// Find all title files in a segment directory.
        /// </summary>
        /// <param name="segment">Audience segment</param>
        /// <param name="basePath">Base titles directory path</param>
        /// <param name="cancellationToken">Cancellation token</param>
        /// <returns>Collection of title file paths</returns>
        Task<IEnumerable<string>> FindTitleFilesAsync(
            AudienceSegment segment,
            string basePath,
            CancellationToken cancellationToken = default);

        /// <summary>
        /// Extract title text from a file.
        /// </summary>
        /// <param name="filePath">Path to the title file</param>
        /// <param name="cancellationToken">Cancellation token</param>
        /// <returns>Extracted title text, or null if extraction fails</returns>
        Task<string?> ExtractTitleFromFileAsync(
            string filePath,
            CancellationToken cancellationToken = default);

        /// <summary>
        /// Extract titles from multiple files.
        /// </summary>
        /// <param name="filePaths">Collection of file paths</param>
        /// <param name="cancellationToken">Cancellation token</param>
        /// <returns>Collection of title items with source file info</returns>
        Task<IEnumerable<TitleItem>> ExtractTitlesAsync(
            IEnumerable<string> filePaths,
            CancellationToken cancellationToken = default);

        /// <summary>
        /// Check if a file contains title information.
        /// </summary>
        /// <param name="filePath">Path to check</param>
        /// <returns>True if file is a valid title source</returns>
        bool IsTitleFile(string filePath);
    }
}
