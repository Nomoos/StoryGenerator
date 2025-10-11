using System;
using System.Collections.Generic;

namespace PrismQ.Shared.Models
{
    /// <summary>
    /// Represents a structured shotlist with detailed metadata.
    /// Extends the basic Shotlist class with LLM-generated structured data.
    /// </summary>
    public class StructuredShotlist : Shotlist
    {
        /// <summary>
        /// Gets or sets the overall story mood/tone.
        /// </summary>
        public string OverallMood { get; set; } = string.Empty;

        /// <summary>
        /// Gets or sets the genre or style.
        /// </summary>
        public string Style { get; set; } = string.Empty;

        /// <summary>
        /// Gets or sets the target audience.
        /// </summary>
        public string TargetAudience { get; set; } = string.Empty;

        /// <summary>
        /// Gets or sets the list of structured shots with enhanced metadata.
        /// </summary>
        public new List<StructuredShot> Shots { get; set; } = new();

        /// <summary>
        /// Gets or sets metadata about the generation process.
        /// </summary>
        public GenerationMetadata Metadata { get; set; } = new();
    }

    /// <summary>
    /// Represents a single shot with detailed structured information.
    /// Extends the basic Shot class with emotions, camera details, and more.
    /// </summary>
    public class StructuredShot : Shot
    {
        /// <summary>
        /// Gets or sets the primary emotion conveyed in the shot.
        /// </summary>
        public string PrimaryEmotion { get; set; } = string.Empty;

        /// <summary>
        /// Gets or sets secondary emotions present in the shot.
        /// </summary>
        public List<string> SecondaryEmotions { get; set; } = new();

        /// <summary>
        /// Gets or sets detailed camera direction information.
        /// </summary>
        public CameraDirection CameraDirection { get; set; } = new();

        /// <summary>
        /// Gets or sets the movement type (static, pan, zoom, dolly, etc.).
        /// </summary>
        public string MovementType { get; set; } = string.Empty;

        /// <summary>
        /// Gets or sets the transition to next shot (cut, fade, dissolve, etc.).
        /// </summary>
        public string Transition { get; set; } = string.Empty;

        /// <summary>
        /// Gets or sets the audio description for this shot.
        /// </summary>
        public string AudioDescription { get; set; } = string.Empty;

        /// <summary>
        /// Gets or sets character focus information.
        /// </summary>
        public List<string> CharacterFocus { get; set; } = new();

        /// <summary>
        /// Gets or sets the shot importance (1-10 scale).
        /// </summary>
        public int Importance { get; set; } = 5;
    }

    /// <summary>
    /// Represents detailed camera direction information.
    /// </summary>
    public class CameraDirection
    {
        /// <summary>
        /// Gets or sets the shot type (wide, medium, close-up, extreme close-up, etc.).
        /// </summary>
        public string ShotType { get; set; } = string.Empty;

        /// <summary>
        /// Gets or sets the camera angle (eye level, high angle, low angle, dutch angle, etc.).
        /// </summary>
        public string Angle { get; set; } = string.Empty;

        /// <summary>
        /// Gets or sets the camera movement (static, pan left/right, tilt up/down, zoom in/out, dolly, tracking, etc.).
        /// </summary>
        public string Movement { get; set; } = string.Empty;

        /// <summary>
        /// Gets or sets the focus point or subject.
        /// </summary>
        public string FocusPoint { get; set; } = string.Empty;

        /// <summary>
        /// Gets or sets the depth of field description (shallow, deep).
        /// </summary>
        public string DepthOfField { get; set; } = string.Empty;

        /// <summary>
        /// Gets or sets composition notes (rule of thirds, centered, symmetrical, etc.).
        /// </summary>
        public string Composition { get; set; } = string.Empty;

        /// <summary>
        /// Gets or sets additional camera notes.
        /// </summary>
        public string Notes { get; set; } = string.Empty;
    }

    /// <summary>
    /// Metadata about the shotlist generation process.
    /// </summary>
    public class GenerationMetadata
    {
        /// <summary>
        /// Gets or sets the model used for generation.
        /// </summary>
        public string ModelUsed { get; set; } = string.Empty;

        /// <summary>
        /// Gets or sets the generation timestamp.
        /// </summary>
        public DateTime GeneratedAt { get; set; } = DateTime.UtcNow;

        /// <summary>
        /// Gets or sets the temperature used.
        /// </summary>
        public float Temperature { get; set; }

        /// <summary>
        /// Gets or sets the generation time in seconds.
        /// </summary>
        public float GenerationTimeSeconds { get; set; }

        /// <summary>
        /// Gets or sets the provider used (Ollama, Transformers, etc.).
        /// </summary>
        public string Provider { get; set; } = string.Empty;
    }
}
