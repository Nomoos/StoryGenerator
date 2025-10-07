using System;

namespace StoryGenerator.Models
{
    /// <summary>
    /// Represents an audience segment defined by gender and age range.
    /// </summary>
    public class AudienceSegment
    {
        /// <summary>
        /// Gets or sets the target gender (e.g., "men", "women").
        /// </summary>
        public string Gender { get; set; } = string.Empty;

        /// <summary>
        /// Gets or sets the target age range (e.g., "18-23").
        /// </summary>
        public string Age { get; set; } = string.Empty;

        /// <summary>
        /// Creates a new audience segment.
        /// </summary>
        public AudienceSegment() { }

        /// <summary>
        /// Creates a new audience segment with specified gender and age.
        /// </summary>
        /// <param name="gender">Target gender</param>
        /// <param name="age">Target age range</param>
        public AudienceSegment(string gender, string age)
        {
            Gender = gender ?? throw new ArgumentNullException(nameof(gender));
            Age = age ?? throw new ArgumentNullException(nameof(age));
        }

        /// <summary>
        /// Gets a string representation of the segment.
        /// </summary>
        /// <returns>Formatted segment string (e.g., "women/18-23")</returns>
        public override string ToString() => $"{Gender}/{Age}";

        /// <summary>
        /// Checks equality with another audience segment.
        /// </summary>
        public override bool Equals(object? obj)
        {
            if (obj is not AudienceSegment other)
                return false;

            return Gender.Equals(other.Gender, StringComparison.OrdinalIgnoreCase) &&
                   Age.Equals(other.Age, StringComparison.OrdinalIgnoreCase);
        }

        /// <summary>
        /// Gets the hash code for this segment.
        /// </summary>
        public override int GetHashCode()
        {
            return HashCode.Combine(
                Gender.ToLowerInvariant(), 
                Age.ToLowerInvariant()
            );
        }
    }
}
