using System.Collections.Generic;

namespace StoryGenerator.Core.Interfaces
{
    /// <summary>
    /// Represents a story idea with metadata and viral potential scoring.
    /// </summary>
    public interface IStoryIdea
    {
        /// <summary>
        /// Gets or sets the title of the story.
        /// </summary>
        string StoryTitle { get; set; }

        /// <summary>
        /// Gets or sets the narrator's gender (e.g., "male", "female").
        /// </summary>
        string NarratorGender { get; set; }

        /// <summary>
        /// Gets or sets the tone of the story (e.g., "emotional, heartwarming").
        /// </summary>
        string? Tone { get; set; }

        /// <summary>
        /// Gets or sets the theme of the story (e.g., "friendship, acceptance").
        /// </summary>
        string? Theme { get; set; }

        /// <summary>
        /// Gets or sets the narrator type (e.g., "first-person", "third-person").
        /// </summary>
        string? NarratorType { get; set; }

        /// <summary>
        /// Gets or sets the other main character in the story.
        /// </summary>
        string? OtherCharacter { get; set; }

        /// <summary>
        /// Gets or sets the key plot outcome.
        /// </summary>
        string? Outcome { get; set; }

        /// <summary>
        /// Gets or sets the emotional core of the story.
        /// </summary>
        string? EmotionalCore { get; set; }

        /// <summary>
        /// Gets or sets the power dynamic between characters.
        /// </summary>
        string? PowerDynamic { get; set; }

        /// <summary>
        /// Gets or sets the timeline of the story.
        /// </summary>
        string? Timeline { get; set; }

        /// <summary>
        /// Gets or sets the type of twist in the story.
        /// </summary>
        string? TwistType { get; set; }

        /// <summary>
        /// Gets or sets the character arc.
        /// </summary>
        string? CharacterArc { get; set; }

        /// <summary>
        /// Gets or sets the voice style for narration.
        /// </summary>
        string? VoiceStyle { get; set; }

        /// <summary>
        /// Gets or sets the target moral or message.
        /// </summary>
        string? TargetMoral { get; set; }

        /// <summary>
        /// Gets or sets the locations featured in the story.
        /// </summary>
        string? Locations { get; set; }

        /// <summary>
        /// Gets or sets any brands mentioned in the story.
        /// </summary>
        string? MentionedBrands { get; set; }

        /// <summary>
        /// Gets or sets the goal or purpose of the story.
        /// </summary>
        string? Goal { get; set; }

        /// <summary>
        /// Gets or sets the language code (e.g., "en", "es", "fr").
        /// Default is "en" for English.
        /// </summary>
        string Language { get; set; }

        /// <summary>
        /// Gets or sets personalization replacements for the story.
        /// Key-value pairs where keys are placeholders and values are replacement text.
        /// </summary>
        Dictionary<string, string> Personalization { get; set; }

        /// <summary>
        /// Gets or sets the video style (e.g., "cinematic", "documentary").
        /// Default is "cinematic".
        /// </summary>
        string VideoStyle { get; set; }

        /// <summary>
        /// Gets or sets the voice stability parameter (0.0 to 1.0).
        /// Default is 0.5.
        /// </summary>
        float VoiceStability { get; set; }

        /// <summary>
        /// Gets or sets the voice similarity boost parameter (0.0 to 1.0).
        /// Default is 0.75.
        /// </summary>
        float VoiceSimilarityBoost { get; set; }

        /// <summary>
        /// Gets or sets the voice style exaggeration parameter (0.0 to 1.0).
        /// Default is 0.0.
        /// </summary>
        float VoiceStyleExaggeration { get; set; }

        /// <summary>
        /// Gets or sets the viral potential scores across platforms, regions, age groups, and gender.
        /// </summary>
        ViralPotential Potential { get; set; }
    }

    /// <summary>
    /// Represents viral potential scoring across different dimensions.
    /// </summary>
    public class ViralPotential
    {
        /// <summary>
        /// Gets or sets the overall viral potential score (0-10).
        /// </summary>
        public int Overall { get; set; }

        /// <summary>
        /// Gets or sets platform-specific scores.
        /// </summary>
        public Dictionary<string, int> Platforms { get; set; } = new()
        {
            { "youtube", 0 },
            { "tiktok", 0 },
            { "instagram", 0 }
        };

        /// <summary>
        /// Gets or sets region-specific scores.
        /// </summary>
        public Dictionary<string, int> Regions { get; set; } = new()
        {
            { "US", 0 },
            { "AU", 0 },
            { "GB", 0 }
        };

        /// <summary>
        /// Gets or sets age group scores.
        /// </summary>
        public Dictionary<string, int> AgeGroups { get; set; } = new()
        {
            { "10_15", 0 },
            { "15_20", 0 },
            { "20_25", 0 },
            { "25_30", 0 },
            { "30_50", 0 },
            { "50_70", 0 }
        };

        /// <summary>
        /// Gets or sets gender-specific scores.
        /// </summary>
        public Dictionary<string, int> Gender { get; set; } = new()
        {
            { "woman", 0 },
            { "man", 0 }
        };
    }
}
