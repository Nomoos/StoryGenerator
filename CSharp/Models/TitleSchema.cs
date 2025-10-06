using System;

namespace StoryGenerator.Models
{
    /// <summary>
    /// Represents a title item according to the title.json schema.
    /// This model corresponds to the schema defined in /config/schemas/title.json
    /// </summary>
    public class TitleSchema
    {
        /// <summary>
        /// Gets or sets the unique identifier (UUID) for the title.
        /// </summary>
        public string Id { get; set; } = string.Empty;

        /// <summary>
        /// Gets or sets the target audience segment (women|men).
        /// </summary>
        public string Segment { get; set; } = string.Empty;

        /// <summary>
        /// Gets or sets the target age bucket (10-13|14-17|18-23).
        /// </summary>
        public string AgeBucket { get; set; } = string.Empty;

        /// <summary>
        /// Gets or sets the title text.
        /// </summary>
        public string Title { get; set; } = string.Empty;

        /// <summary>
        /// Gets or sets the array of related topic identifiers.
        /// </summary>
        public string[] TopicIds { get; set; } = Array.Empty<string>();

        /// <summary>
        /// Gets or sets the creation timestamp in ISO-8601 format.
        /// </summary>
        public DateTime CreatedUtc { get; set; }

        /// <summary>
        /// Creates a new title schema instance.
        /// </summary>
        public TitleSchema() { }

        /// <summary>
        /// Creates a new title schema instance with all required fields.
        /// </summary>
        /// <param name="id">Unique identifier (UUID)</param>
        /// <param name="segment">Target audience segment</param>
        /// <param name="ageBucket">Target age bucket</param>
        /// <param name="title">Title text</param>
        /// <param name="topicIds">Related topic identifiers</param>
        /// <param name="createdUtc">Creation timestamp</param>
        public TitleSchema(string id, string segment, string ageBucket, string title, string[] topicIds, DateTime createdUtc)
        {
            Id = id ?? throw new ArgumentNullException(nameof(id));
            Segment = segment ?? throw new ArgumentNullException(nameof(segment));
            AgeBucket = ageBucket ?? throw new ArgumentNullException(nameof(ageBucket));
            Title = title ?? throw new ArgumentNullException(nameof(title));
            TopicIds = topicIds ?? throw new ArgumentNullException(nameof(topicIds));
            CreatedUtc = createdUtc;
        }
    }
}
