using System.Collections.Generic;

namespace StoryGenerator.Core.Interfaces
{
    /// <summary>
    /// Represents a shotlist with scene descriptions and timing.
    /// </summary>
    public class Shotlist
    {
        /// <summary>
        /// Gets or sets the story title.
        /// </summary>
        public string StoryTitle { get; set; } = string.Empty;

        /// <summary>
        /// Gets or sets the total duration in seconds.
        /// </summary>
        public float TotalDuration { get; set; }

        /// <summary>
        /// Gets or sets the list of shots/scenes.
        /// </summary>
        public List<Shot> Shots { get; set; } = new();
    }

    /// <summary>
    /// Represents a single shot/scene in a shotlist.
    /// </summary>
    public class Shot
    {
        /// <summary>
        /// Gets or sets the shot number.
        /// </summary>
        public int ShotNumber { get; set; }

        /// <summary>
        /// Gets or sets the start time in seconds.
        /// </summary>
        public float StartTime { get; set; }

        /// <summary>
        /// Gets or sets the end time in seconds.
        /// </summary>
        public float EndTime { get; set; }

        /// <summary>
        /// Gets or sets the duration in seconds.
        /// </summary>
        public float Duration { get; set; }

        /// <summary>
        /// Gets or sets the scene description.
        /// </summary>
        public string SceneDescription { get; set; } = string.Empty;

        /// <summary>
        /// Gets or sets the visual prompt for image generation.
        /// </summary>
        public string VisualPrompt { get; set; } = string.Empty;

        /// <summary>
        /// Gets or sets the mood of the scene.
        /// </summary>
        public string Mood { get; set; } = string.Empty;

        /// <summary>
        /// Gets or sets the camera angle.
        /// </summary>
        public string CameraAngle { get; set; } = string.Empty;

        /// <summary>
        /// Gets or sets the lighting description.
        /// </summary>
        public string Lighting { get; set; } = string.Empty;

        /// <summary>
        /// Gets or sets the color palette.
        /// </summary>
        public string ColorPalette { get; set; } = string.Empty;

        /// <summary>
        /// Gets or sets key visual elements.
        /// </summary>
        public List<string> KeyElements { get; set; } = new();
    }
}
