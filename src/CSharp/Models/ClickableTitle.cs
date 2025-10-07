using System;
using System.Collections.Generic;

namespace StoryGenerator.Models
{
    /// <summary>
    /// Represents a clickable, viral-optimized title derived from a topic cluster.
    /// </summary>
    public class ClickableTitle
    {
        /// <summary>
        /// Gets or sets the unique identifier for the title.
        /// </summary>
        public string Id { get; set; } = Guid.NewGuid().ToString();

        /// <summary>
        /// Gets or sets the title text.
        /// </summary>
        public string Title { get; set; } = string.Empty;

        /// <summary>
        /// Gets or sets the topic cluster ID this title was derived from.
        /// </summary>
        public string? TopicClusterId { get; set; }

        /// <summary>
        /// Gets or sets the audience segment this title targets.
        /// </summary>
        public AudienceSegment? Segment { get; set; }

        /// <summary>
        /// Gets or sets the timestamp when this title was generated.
        /// </summary>
        public DateTime GeneratedAt { get; set; } = DateTime.UtcNow;

        /// <summary>
        /// Gets or sets the estimated viral potential score (0-10).
        /// </summary>
        public int? ViralPotential { get; set; }

        /// <summary>
        /// Gets or sets the clickability score (0-10).
        /// </summary>
        public int? ClickabilityScore { get; set; }

        /// <summary>
        /// Gets or sets keywords extracted from the title for SEO.
        /// </summary>
        public List<string> Keywords { get; set; } = new();

        /// <summary>
        /// Gets or sets the emotional hook used in the title (e.g., "curiosity", "surprise").
        /// </summary>
        public string? EmotionalHook { get; set; }

        /// <summary>
        /// Gets or sets the title format/pattern (e.g., "list", "how-to", "question").
        /// </summary>
        public string? TitleFormat { get; set; }

        /// <summary>
        /// Gets or sets additional metadata for the title.
        /// </summary>
        public Dictionary<string, object>? Metadata { get; set; }

        /// <summary>
        /// Creates a new clickable title.
        /// </summary>
        public ClickableTitle() { }

        /// <summary>
        /// Creates a new clickable title with specified text and segment.
        /// </summary>
        /// <param name="title">The title text</param>
        /// <param name="segment">The target audience segment</param>
        public ClickableTitle(string title, AudienceSegment segment)
        {
            Title = title ?? throw new ArgumentNullException(nameof(title));
            Segment = segment ?? throw new ArgumentNullException(nameof(segment));
        }

        /// <summary>
        /// Gets a string representation of the clickable title.
        /// </summary>
        public override string ToString() => Title;
    }

    /// <summary>
    /// Represents a collection of clickable titles for a specific segment.
    /// </summary>
    public class ClickableTitleCollection
    {
        /// <summary>
        /// Gets or sets the audience segment for this collection.
        /// </summary>
        public AudienceSegment? Segment { get; set; }

        /// <summary>
        /// Gets or sets the list of clickable titles.
        /// </summary>
        public List<ClickableTitle> Titles { get; set; } = new();

        /// <summary>
        /// Gets or sets the timestamp when this collection was generated.
        /// </summary>
        public DateTime GeneratedAt { get; set; } = DateTime.UtcNow;

        /// <summary>
        /// Gets or sets metadata about the title generation process.
        /// </summary>
        public Dictionary<string, object>? Metadata { get; set; }

        /// <summary>
        /// Gets the total number of titles in this collection.
        /// </summary>
        public int TitleCount => Titles.Count;
    }
}
