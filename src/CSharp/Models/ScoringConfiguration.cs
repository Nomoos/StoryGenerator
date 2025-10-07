using System;
using System.Collections.Generic;

namespace StoryGenerator.Models
{
    /// <summary>
    /// Represents the complete scoring configuration loaded from YAML.
    /// </summary>
    public class ScoringConfiguration
    {
        /// <summary>
        /// Gets or sets the title scoring configuration.
        /// </summary>
        public TitleScoringConfig TitleScoring { get; set; } = new();

        /// <summary>
        /// Gets or sets the LLM prompt template (for future use).
        /// </summary>
        public string PromptTemplate { get; set; } = string.Empty;
    }

    /// <summary>
    /// Configuration specific to title scoring.
    /// </summary>
    public class TitleScoringConfig
    {
        /// <summary>
        /// Gets or sets the description of the scoring system.
        /// </summary>
        public string Description { get; set; } = string.Empty;

        /// <summary>
        /// Gets or sets the scoring criteria with their weights.
        /// </summary>
        public List<ScoringCriterion> Criteria { get; set; } = new();

        /// <summary>
        /// Gets or sets the voice recommendation configuration.
        /// </summary>
        public VoiceRecommendationConfig VoiceRecommendation { get; set; } = new();

        /// <summary>
        /// Gets or sets the top title selection configuration.
        /// </summary>
        public TopSelectionConfig TopSelection { get; set; } = new();
    }

    /// <summary>
    /// Represents a scoring criterion with its weight and guidelines.
    /// </summary>
    public class ScoringCriterion
    {
        /// <summary>
        /// Gets or sets the criterion name (e.g., "Hook Strength").
        /// </summary>
        public string Name { get; set; } = string.Empty;

        /// <summary>
        /// Gets or sets the weight of this criterion (0.0 - 1.0).
        /// </summary>
        public double Weight { get; set; }

        /// <summary>
        /// Gets or sets the description of what this criterion measures.
        /// </summary>
        public string Description { get; set; } = string.Empty;

        /// <summary>
        /// Gets or sets the scoring guide with score ranges.
        /// </summary>
        public Dictionary<string, string> ScoringGuide { get; set; } = new();
    }

    /// <summary>
    /// Voice recommendation configuration and guidelines.
    /// </summary>
    public class VoiceRecommendationConfig
    {
        /// <summary>
        /// Gets or sets the description of voice recommendation.
        /// </summary>
        public string Description { get; set; } = string.Empty;

        /// <summary>
        /// Gets or sets the factors considered in voice recommendation.
        /// </summary>
        public List<string> Factors { get; set; } = new();

        /// <summary>
        /// Gets or sets the guidelines for voice selection.
        /// </summary>
        public List<string> Guidelines { get; set; } = new();
    }

    /// <summary>
    /// Guidelines for voice recommendations.
    /// </summary>
    public class VoiceRecommendationGuidelines
    {
        /// <summary>
        /// Gets or sets the description.
        /// </summary>
        public string Description { get; set; } = string.Empty;

        /// <summary>
        /// Gets or sets content-type to voice mappings.
        /// </summary>
        public Dictionary<string, VoiceGender> ContentTypeMapping { get; set; } = new();

        /// <summary>
        /// Gets or sets the guidelines text.
        /// </summary>
        public List<string> Guidelines { get; set; } = new();
    }

    /// <summary>
    /// Configuration for top title selection.
    /// </summary>
    public class TopSelectionConfig
    {
        /// <summary>
        /// Gets or sets the number of top titles to select.
        /// </summary>
        public int Count { get; set; } = 5;

        /// <summary>
        /// Gets or sets the description of selection criteria.
        /// </summary>
        public string Description { get; set; } = string.Empty;

        /// <summary>
        /// Gets or sets the criteria used for top selection.
        /// </summary>
        public List<string> Criteria { get; set; } = new();
    }
}
