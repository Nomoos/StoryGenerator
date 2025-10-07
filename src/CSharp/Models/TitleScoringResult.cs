using System;
using System.Collections.Generic;

namespace StoryGenerator.Models
{
    /// <summary>
    /// Represents the result of scoring a video title.
    /// Contains overall score, individual criterion scores, rationale, and voice recommendation.
    /// </summary>
    public class TitleScoringResult
    {
        /// <summary>
        /// Gets or sets the video title that was scored.
        /// </summary>
        public string Title { get; set; } = string.Empty;

        /// <summary>
        /// Gets or sets the source file from which the title was extracted.
        /// </summary>
        public string SourceFile { get; set; } = string.Empty;

        /// <summary>
        /// Gets or sets the target audience segment.
        /// </summary>
        public AudienceSegment TargetAudience { get; set; } = new();

        /// <summary>
        /// Gets or sets the timestamp when the title was scored.
        /// </summary>
        public DateTime ScoredAt { get; set; } = DateTime.UtcNow;

        /// <summary>
        /// Gets or sets the individual scores for each criterion.
        /// </summary>
        public CriterionScores Scores { get; set; } = new();

        /// <summary>
        /// Gets or sets the overall weighted score (0-100).
        /// </summary>
        public double OverallScore { get; set; }

        /// <summary>
        /// Gets or sets the rationale explaining the score.
        /// </summary>
        public string Rationale { get; set; } = string.Empty;

        /// <summary>
        /// Gets or sets the voice recommendation for narration.
        /// </summary>
        public VoiceRecommendation VoiceRecommendation { get; set; } = new();
    }

    /// <summary>
    /// Individual criterion scores for a title.
    /// </summary>
    public class CriterionScores
    {
        /// <summary>
        /// Hook strength score (0-100).
        /// Measures curiosity, emotional appeal, and urgency.
        /// </summary>
        public int HookStrength { get; set; }

        /// <summary>
        /// Clarity score (0-100).
        /// Measures how easy the title is to understand.
        /// </summary>
        public int Clarity { get; set; }

        /// <summary>
        /// Relevance score (0-100).
        /// Measures alignment with target audience and trends.
        /// </summary>
        public int Relevance { get; set; }

        /// <summary>
        /// Length and format score (0-100).
        /// Measures optimal length for social media platforms.
        /// </summary>
        public int LengthFormat { get; set; }

        /// <summary>
        /// Viral potential score (0-100).
        /// Measures shareability and viral characteristics.
        /// </summary>
        public int ViralPotential { get; set; }
    }
}
