using System;
using System.Collections.Generic;

namespace StoryGenerator.Models
{
    /// <summary>
    /// Represents a cluster of related ideas grouped by topic.
    /// </summary>
    public class TopicCluster
    {
        /// <summary>
        /// Gets or sets the unique identifier for the topic cluster.
        /// </summary>
        public string Id { get; set; } = Guid.NewGuid().ToString();

        /// <summary>
        /// Gets or sets the name/title of the topic.
        /// </summary>
        public string TopicName { get; set; } = string.Empty;

        /// <summary>
        /// Gets or sets a description of the topic cluster.
        /// </summary>
        public string? Description { get; set; }

        /// <summary>
        /// Gets or sets the list of idea IDs that belong to this cluster.
        /// </summary>
        public List<string> IdeaIds { get; set; } = new();

        /// <summary>
        /// Gets or sets keywords or themes associated with this topic.
        /// </summary>
        public List<string> Keywords { get; set; } = new();

        /// <summary>
        /// Gets or sets the audience segment this topic targets.
        /// </summary>
        public AudienceSegment? Segment { get; set; }

        /// <summary>
        /// Gets or sets the timestamp when this cluster was created.
        /// </summary>
        public DateTime CreatedAt { get; set; } = DateTime.UtcNow;

        /// <summary>
        /// Gets or sets the estimated viral potential score for this topic (0-10).
        /// </summary>
        public int? ViralPotential { get; set; }

        /// <summary>
        /// Gets or sets the number of ideas in this cluster.
        /// </summary>
        public int IdeaCount => IdeaIds.Count;

        /// <summary>
        /// Creates a new topic cluster.
        /// </summary>
        public TopicCluster() { }

        /// <summary>
        /// Creates a new topic cluster with specified name and segment.
        /// </summary>
        /// <param name="topicName">The topic name</param>
        /// <param name="segment">The target audience segment</param>
        public TopicCluster(string topicName, AudienceSegment segment)
        {
            TopicName = topicName ?? throw new ArgumentNullException(nameof(topicName));
            Segment = segment ?? throw new ArgumentNullException(nameof(segment));
        }

        /// <summary>
        /// Gets a string representation of the topic cluster.
        /// </summary>
        public override string ToString() => $"{TopicName} ({IdeaCount} ideas)";
    }

    /// <summary>
    /// Represents a collection of topic clusters for a specific segment.
    /// </summary>
    public class TopicClusterCollection
    {
        /// <summary>
        /// Gets or sets the audience segment for this collection.
        /// </summary>
        public AudienceSegment? Segment { get; set; }

        /// <summary>
        /// Gets or sets the list of topic clusters.
        /// </summary>
        public List<TopicCluster> Topics { get; set; } = new();

        /// <summary>
        /// Gets or sets the timestamp when this collection was created.
        /// </summary>
        public DateTime GeneratedAt { get; set; } = DateTime.UtcNow;

        /// <summary>
        /// Gets or sets metadata about the clustering process.
        /// </summary>
        public Dictionary<string, object>? Metadata { get; set; }

        /// <summary>
        /// Gets the total number of topics in this collection.
        /// </summary>
        public int TopicCount => Topics.Count;
    }
}
