using System.Threading;
using System.Threading.Tasks;

namespace StoryGenerator.Core.Interfaces
{
    /// <summary>
    /// Interface for generating detailed shotlists using Large Language Models.
    /// Extends IShotlistGenerator with LLM-specific features including emotions, 
    /// camera directions, and structured JSON output.
    /// </summary>
    /// <remarks>
    /// Recommended models:
    /// - Qwen2.5-14B-Instruct: Better for detailed creative descriptions
    /// - Llama-3.1-8B-Instruct: Faster inference, good balance
    /// Outputs structured JSON with scene metadata, emotions, camera angles, and visual elements.
    /// </remarks>
    public interface ILLMShotlistGenerator : IShotlistGenerator
    {
        /// <summary>
        /// Gets the underlying LLM content generator.
        /// </summary>
        ILLMContentGenerator ContentGenerator { get; }

        /// <summary>
        /// Generates a structured shotlist with emotions and camera directions.
        /// Parses LLM output into structured JSON format.
        /// </summary>
        /// <param name="scriptText">The script text to analyze.</param>
        /// <param name="audioDuration">Duration of the audio in seconds.</param>
        /// <param name="temperature">Sampling temperature for LLM (0.0-1.0, default: 0.5).</param>
        /// <param name="cancellationToken">Cancellation token.</param>
        /// <returns>Structured shotlist with detailed scene information.</returns>
        Task<StructuredShotlist> GenerateStructuredShotlistAsync(
            string scriptText,
            float audioDuration,
            float temperature = 0.5f,
            CancellationToken cancellationToken = default);

        /// <summary>
        /// Refines a shotlist by adding more detailed emotions and camera directions.
        /// </summary>
        /// <param name="shotlist">The initial shotlist to refine.</param>
        /// <param name="temperature">Sampling temperature (0.0-1.0, default: 0.4).</param>
        /// <param name="cancellationToken">Cancellation token.</param>
        /// <returns>Refined shotlist with enhanced details.</returns>
        Task<StructuredShotlist> RefineShotlistAsync(
            StructuredShotlist shotlist,
            float temperature = 0.4f,
            CancellationToken cancellationToken = default);

        /// <summary>
        /// Generates camera direction suggestions for a specific shot.
        /// </summary>
        /// <param name="shot">The shot to generate camera directions for.</param>
        /// <param name="cancellationToken">Cancellation token.</param>
        /// <returns>Detailed camera direction information.</returns>
        Task<CameraDirection> GenerateCameraDirectionAsync(
            StructuredShot shot,
            CancellationToken cancellationToken = default);

        /// <summary>
        /// Validates and corrects shotlist timing to match audio duration.
        /// </summary>
        /// <param name="shotlist">The shotlist to validate.</param>
        /// <param name="audioDuration">The actual audio duration in seconds.</param>
        /// <param name="cancellationToken">Cancellation token.</param>
        /// <returns>Validated and corrected shotlist.</returns>
        Task<StructuredShotlist> ValidateAndCorrectTimingAsync(
            StructuredShotlist shotlist,
            float audioDuration,
            CancellationToken cancellationToken = default);
    }

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
        public new System.Collections.Generic.List<StructuredShot> Shots { get; set; } = new();

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
        public System.Collections.Generic.List<string> SecondaryEmotions { get; set; } = new();

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
        public System.Collections.Generic.List<string> CharacterFocus { get; set; } = new();

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
        public System.DateTime GeneratedAt { get; set; } = System.DateTime.UtcNow;

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
