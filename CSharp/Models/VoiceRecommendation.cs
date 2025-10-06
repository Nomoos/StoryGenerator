using System;

namespace StoryGenerator.Models
{
    /// <summary>
    /// Represents a voice recommendation for title narration.
    /// </summary>
    public class VoiceRecommendation
    {
        /// <summary>
        /// Gets or sets the recommended voice gender.
        /// </summary>
        public VoiceGender Gender { get; set; }

        /// <summary>
        /// Gets or sets the reasoning for the recommendation.
        /// </summary>
        public string Reasoning { get; set; } = string.Empty;

        /// <summary>
        /// Creates a new voice recommendation.
        /// </summary>
        public VoiceRecommendation() { }

        /// <summary>
        /// Creates a new voice recommendation with specified gender and reasoning.
        /// </summary>
        /// <param name="gender">Recommended voice gender</param>
        /// <param name="reasoning">Reasoning for the recommendation</param>
        public VoiceRecommendation(VoiceGender gender, string reasoning)
        {
            Gender = gender;
            Reasoning = reasoning ?? throw new ArgumentNullException(nameof(reasoning));
        }
    }

    /// <summary>
    /// Enum representing voice gender options.
    /// </summary>
    public enum VoiceGender
    {
        /// <summary>
        /// Male voice.
        /// </summary>
        Male,

        /// <summary>
        /// Female voice.
        /// </summary>
        Female
    }

    /// <summary>
    /// Extension methods for VoiceGender enum.
    /// </summary>
    public static class VoiceGenderExtensions
    {
        /// <summary>
        /// Converts VoiceGender to short string representation (M/F).
        /// </summary>
        /// <param name="gender">Voice gender</param>
        /// <returns>Single character string ("M" or "F")</returns>
        public static string ToShortString(this VoiceGender gender)
        {
            return gender == VoiceGender.Male ? "M" : "F";
        }

        /// <summary>
        /// Parses a string to VoiceGender enum.
        /// </summary>
        /// <param name="value">String value ("M", "F", "Male", "Female")</param>
        /// <returns>VoiceGender enum value</returns>
        public static VoiceGender Parse(string value)
        {
            if (string.IsNullOrWhiteSpace(value))
                throw new ArgumentException("Value cannot be null or empty", nameof(value));

            return value.Trim().ToUpperInvariant() switch
            {
                "M" or "MALE" => VoiceGender.Male,
                "F" or "FEMALE" => VoiceGender.Female,
                _ => throw new ArgumentException($"Invalid voice gender value: {value}", nameof(value))
            };
        }
    }
}
