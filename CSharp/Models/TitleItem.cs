using System;

namespace StoryGenerator.Models
{
    /// <summary>
    /// Represents a title item extracted from a file.
    /// </summary>
    public class TitleItem
    {
        /// <summary>
        /// Gets or sets the title text.
        /// </summary>
        public string Title { get; set; } = string.Empty;

        /// <summary>
        /// Gets or sets the source file path.
        /// </summary>
        public string SourceFile { get; set; } = string.Empty;

        /// <summary>
        /// Gets or sets additional metadata from the source file.
        /// </summary>
        public TitleMetadata? Metadata { get; set; }

        /// <summary>
        /// Creates a new title item.
        /// </summary>
        public TitleItem() { }

        /// <summary>
        /// Creates a new title item with specified title and source.
        /// </summary>
        /// <param name="title">The title text</param>
        /// <param name="sourceFile">The source file path</param>
        public TitleItem(string title, string sourceFile)
        {
            Title = title ?? throw new ArgumentNullException(nameof(title));
            SourceFile = sourceFile ?? throw new ArgumentNullException(nameof(sourceFile));
        }
    }

    /// <summary>
    /// Additional metadata that may be present in title files.
    /// </summary>
    public class TitleMetadata
    {
        /// <summary>
        /// Gets or sets the genre (e.g., "mystery", "beauty", "tech").
        /// </summary>
        public string? Genre { get; set; }

        /// <summary>
        /// Gets or sets the synopsis or description.
        /// </summary>
        public string? Synopsis { get; set; }

        /// <summary>
        /// Gets or sets the hook or tagline.
        /// </summary>
        public string? Hook { get; set; }

        /// <summary>
        /// Gets or sets themes associated with the title.
        /// </summary>
        public string[]? Themes { get; set; }
    }
}
