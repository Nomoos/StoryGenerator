using System.Collections.Generic;
using System.Text.Json.Serialization;

namespace PrismQ.Shared.Models
{
    /// <summary>
    /// Represents the mapping of subtitles to shots in a video.
    /// </summary>
    public class SubtitleToShotMapping
    {
        /// <summary>
        /// Gets or sets the title/story ID.
        /// </summary>
        [JsonPropertyName("title_id")]
        public string TitleId { get; set; } = string.Empty;

        /// <summary>
        /// Gets or sets the total duration in seconds.
        /// </summary>
        [JsonPropertyName("total_duration")]
        public double TotalDuration { get; set; }

        /// <summary>
        /// Gets or sets the list of subtitle entries mapped to shots.
        /// </summary>
        [JsonPropertyName("subtitle_mappings")]
        public List<SubtitleEntry> SubtitleMappings { get; set; } = new();
    }

    /// <summary>
    /// Represents a single subtitle entry with its shot mapping.
    /// </summary>
    public class SubtitleEntry
    {
        /// <summary>
        /// Gets or sets the subtitle index (1-based).
        /// </summary>
        [JsonPropertyName("subtitle_index")]
        public int SubtitleIndex { get; set; }

        /// <summary>
        /// Gets or sets the subtitle text.
        /// </summary>
        [JsonPropertyName("text")]
        public string Text { get; set; } = string.Empty;

        /// <summary>
        /// Gets or sets the start time in seconds.
        /// </summary>
        [JsonPropertyName("start_time")]
        public double StartTime { get; set; }

        /// <summary>
        /// Gets or sets the end time in seconds.
        /// </summary>
        [JsonPropertyName("end_time")]
        public double EndTime { get; set; }

        /// <summary>
        /// Gets or sets the shot number this subtitle belongs to.
        /// </summary>
        [JsonPropertyName("shot_number")]
        public int ShotNumber { get; set; }

        /// <summary>
        /// Gets or sets the list of words with individual timestamps.
        /// </summary>
        [JsonPropertyName("words")]
        public List<SubtitleWord>? Words { get; set; }
    }

    /// <summary>
    /// Represents a single word with timestamp information.
    /// </summary>
    public class SubtitleWord
    {
        /// <summary>
        /// Gets or sets the word text.
        /// </summary>
        [JsonPropertyName("word")]
        public string Word { get; set; } = string.Empty;

        /// <summary>
        /// Gets or sets the start time in seconds.
        /// </summary>
        [JsonPropertyName("start")]
        public double Start { get; set; }

        /// <summary>
        /// Gets or sets the end time in seconds.
        /// </summary>
        [JsonPropertyName("end")]
        public double End { get; set; }

        /// <summary>
        /// Gets or sets the confidence score.
        /// </summary>
        [JsonPropertyName("confidence")]
        public double Confidence { get; set; }
    }
}
