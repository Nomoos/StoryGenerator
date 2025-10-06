using System;
using System.Collections.Generic;

namespace StoryGenerator.Models
{
    /// <summary>
    /// Represents the result of scoring a script for quality and narrative cohesion.
    /// Contains rubric scores, narrative cohesion score, overall score, and feedback.
    /// </summary>
    public class ScriptScoringResult
    {
        /// <summary>
        /// Gets or sets the script version being scored (e.g., "v0", "v1").
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
        /// Gets or sets the source file path of the script.
        /// </summary>
        public string ScriptPath { get; set; } = string.Empty;

        /// <summary>
        /// Gets or sets the target audience segment.
        /// </summary>
        public AudienceSegment TargetAudience { get; set; } = new();

        /// <summary>
        /// Gets or sets the timestamp when the script was scored.
        /// </summary>
        public DateTime ScoredAt { get; set; } = DateTime.UtcNow;

        /// <summary>
        /// Gets or sets the individual rubric scores for the script.
        /// </summary>
        public ScriptRubricScores RubricScores { get; set; } = new();

        /// <summary>
        /// Gets or sets the narrative cohesion score (0-100).
        /// Measures how well the story flows and maintains coherence.
        /// </summary>
        public double NarrativeCohesion { get; set; }

        /// <summary>
        /// Gets or sets the overall weighted score (0-100).
        /// Combines rubric scores and narrative cohesion.
        /// </summary>
        public double OverallScore { get; set; }

        /// <summary>
        /// Gets or sets detailed feedback on the script.
        /// </summary>
        public string Feedback { get; set; } = string.Empty;

        /// <summary>
        /// Gets or sets specific areas for improvement.
        /// </summary>
        public List<string> AreasForImprovement { get; set; } = new();

        /// <summary>
        /// Gets or sets the strengths of the script.
        /// </summary>
        public List<string> Strengths { get; set; } = new();

        /// <summary>
        /// Gets or sets additional metadata about the scoring.
        /// </summary>
        public Dictionary<string, object> Metadata { get; set; } = new();
    }

    /// <summary>
    /// Individual rubric scores for a script.
    /// Each criterion is scored 0-100.
    /// </summary>
    public class ScriptRubricScores
    {
        /// <summary>
        /// Hook and opening score (0-100).
        /// Measures how engaging and attention-grabbing the opening is.
        /// </summary>
        public int HookQuality { get; set; }

        /// <summary>
        /// Character development score (0-100).
        /// Measures how well characters are developed and relatable.
        /// </summary>
        public int CharacterDevelopment { get; set; }

        /// <summary>
        /// Plot structure score (0-100).
        /// Measures story structure, pacing, and progression.
        /// </summary>
        public int PlotStructure { get; set; }

        /// <summary>
        /// Dialogue quality score (0-100).
        /// Measures naturalness and effectiveness of dialogue.
        /// </summary>
        public int DialogueQuality { get; set; }

        /// <summary>
        /// Emotional impact score (0-100).
        /// Measures emotional resonance and engagement.
        /// </summary>
        public int EmotionalImpact { get; set; }

        /// <summary>
        /// Target audience alignment score (0-100).
        /// Measures how well the content fits the target demographic.
        /// </summary>
        public int AudienceAlignment { get; set; }

        /// <summary>
        /// Clarity and readability score (0-100).
        /// Measures how clear and easy to follow the script is.
        /// </summary>
        public int Clarity { get; set; }

        /// <summary>
        /// Voice suitability score (0-100).
        /// Measures how well the script works for text-to-speech/voiceover.
        /// </summary>
        public int VoiceSuitability { get; set; }
    }
}
