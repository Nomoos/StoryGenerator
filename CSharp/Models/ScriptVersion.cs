using System;

namespace StoryGenerator.Models
{
    /// <summary>
    /// Represents a version of a script with tracking information.
    /// Used to manage script iterations and improvements.
    /// </summary>
    public class ScriptVersion
    {
        /// <summary>
        /// Gets or sets the version identifier (e.g., "v0", "v1", "v2").
        /// </summary>
        public string Version { get; set; } = "v0";

        /// <summary>
        /// Gets or sets the title ID for this script.
        /// </summary>
        public string TitleId { get; set; } = string.Empty;

        /// <summary>
        /// Gets or sets the script title.
        /// </summary>
        public string Title { get; set; } = string.Empty;

        /// <summary>
        /// Gets or sets the script content.
        /// </summary>
        public string Content { get; set; } = string.Empty;

        /// <summary>
        /// Gets or sets the file path where this version is saved.
        /// </summary>
        public string FilePath { get; set; } = string.Empty;

        /// <summary>
        /// Gets or sets the target audience segment.
        /// </summary>
        public AudienceSegment TargetAudience { get; set; } = new();

        /// <summary>
        /// Gets or sets the timestamp when this version was created.
        /// </summary>
        public DateTime CreatedAt { get; set; } = DateTime.UtcNow;

        /// <summary>
        /// Gets or sets the previous version identifier, if this is an iteration.
        /// </summary>
        public string? PreviousVersion { get; set; }

        /// <summary>
        /// Gets or sets the score of this version, if scored.
        /// </summary>
        public double? Score { get; set; }

        /// <summary>
        /// Gets or sets the feedback that was applied to create this version.
        /// </summary>
        public string? AppliedFeedback { get; set; }

        /// <summary>
        /// Gets or sets the generation source (e.g., "local_llm", "gpt4", "iteration").
        /// </summary>
        public string GenerationSource { get; set; } = "local_llm";

        /// <summary>
        /// Creates a new script version.
        /// </summary>
        public ScriptVersion() { }

        /// <summary>
        /// Creates a new script version with specified parameters.
        /// </summary>
        /// <param name="titleId">The title ID</param>
        /// <param name="version">The version identifier</param>
        /// <param name="content">The script content</param>
        /// <param name="audience">The target audience</param>
        public ScriptVersion(string titleId, string version, string content, AudienceSegment audience)
        {
            TitleId = titleId ?? throw new ArgumentNullException(nameof(titleId));
            Version = version ?? throw new ArgumentNullException(nameof(version));
            Content = content ?? throw new ArgumentNullException(nameof(content));
            TargetAudience = audience ?? throw new ArgumentNullException(nameof(audience));
        }

        /// <summary>
        /// Gets a string representation of this script version.
        /// </summary>
        /// <returns>Formatted version string</returns>
        public override string ToString() => $"{TitleId}_{Version} ({TargetAudience})";
    }
}
