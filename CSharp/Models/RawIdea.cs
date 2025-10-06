using System;

namespace StoryGenerator.Models
{
    /// <summary>
    /// Represents a raw story idea generated for a specific audience segment.
    /// </summary>
    public class RawIdea
    {
        /// <summary>
        /// Gets or sets the unique identifier for the idea.
        /// </summary>
        public string Id { get; set; } = Guid.NewGuid().ToString();

        /// <summary>
        /// Gets or sets the idea text/description.
        /// </summary>
        public string Content { get; set; } = string.Empty;

        /// <summary>
        /// Gets or sets the audience segment this idea targets.
        /// </summary>
        public AudienceSegment? Segment { get; set; }

        /// <summary>
        /// Gets or sets the timestamp when this idea was generated.
        /// </summary>
        public DateTime GeneratedAt { get; set; } = DateTime.UtcNow;

        /// <summary>
        /// Gets or sets optional tags or keywords associated with the idea.
        /// </summary>
        public string[]? Tags { get; set; }

        /// <summary>
        /// Gets or sets the estimated viral potential score (0-10).
        /// </summary>
        public int? ViralPotential { get; set; }

        /// <summary>
        /// Creates a new raw idea.
        /// </summary>
        public RawIdea() { }

        /// <summary>
        /// Creates a new raw idea with specified content and segment.
        /// </summary>
        /// <param name="content">The idea content</param>
        /// <param name="segment">The target audience segment</param>
        public RawIdea(string content, AudienceSegment segment)
        {
            Content = content ?? throw new ArgumentNullException(nameof(content));
            Segment = segment ?? throw new ArgumentNullException(nameof(segment));
        }

        /// <summary>
        /// Gets a string representation of the raw idea.
        /// </summary>
        public override string ToString() => Content;
    }
}
