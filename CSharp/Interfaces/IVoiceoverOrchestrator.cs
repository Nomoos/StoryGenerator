using System;
using System.Threading;
using System.Threading.Tasks;
using StoryGenerator.Models;

namespace StoryGenerator.Interfaces
{
    /// <summary>
    /// Interface for voiceover generation orchestration.
    /// Manages the complete workflow: TTS generation, normalization, and file versioning.
    /// </summary>
    public interface IVoiceoverOrchestrator
    {
        /// <summary>
        /// Generate voiceover with versioning support for quality tracking.
        /// </summary>
        /// <param name="request">Voiceover generation request</param>
        /// <param name="cancellationToken">Cancellation token</param>
        /// <returns>Voiceover generation result with file paths</returns>
        Task<VoiceoverGenerationResult> GenerateVoiceoverAsync(
            VoiceoverRequest request,
            CancellationToken cancellationToken = default);

        /// <summary>
        /// Get the current version identifier for the voiceover generation.
        /// Used for file versioning and quality comparison.
        /// </summary>
        string GetVersionIdentifier();
    }

    /// <summary>
    /// Request for voiceover generation.
    /// </summary>
    public class VoiceoverRequest
    {
        /// <summary>
        /// Unique identifier for the content.
        /// </summary>
        public string TitleId { get; set; } = string.Empty;

        /// <summary>
        /// Title text for content analysis.
        /// </summary>
        public string Title { get; set; } = string.Empty;

        /// <summary>
        /// Text content to convert to speech.
        /// </summary>
        public string Text { get; set; } = string.Empty;

        /// <summary>
        /// Target audience segment.
        /// </summary>
        public AudienceSegment Segment { get; set; } = new();

        /// <summary>
        /// Optional version suffix for quality comparison (e.g., "v1", "v2").
        /// If not specified, uses the orchestrator's default version.
        /// </summary>
        public string? VersionSuffix { get; set; }
    }

    /// <summary>
    /// Result of voiceover generation.
    /// </summary>
    public class VoiceoverGenerationResult
    {
        /// <summary>
        /// Whether the generation was successful.
        /// </summary>
        public bool Success { get; set; }

        /// <summary>
        /// Title ID.
        /// </summary>
        public string TitleId { get; set; } = string.Empty;

        /// <summary>
        /// Audience segment.
        /// </summary>
        public AudienceSegment Segment { get; set; } = new();

        /// <summary>
        /// Recommended voice gender.
        /// </summary>
        public VoiceGender VoiceGender { get; set; }

        /// <summary>
        /// Version identifier used for this generation.
        /// </summary>
        public string Version { get; set; } = string.Empty;

        /// <summary>
        /// Path to generated TTS audio file.
        /// </summary>
        public string TTSPath { get; set; } = string.Empty;

        /// <summary>
        /// Path to normalized audio file.
        /// </summary>
        public string NormalizedPath { get; set; } = string.Empty;

        /// <summary>
        /// Path to LUFS parameters JSON file.
        /// </summary>
        public string LufsJsonPath { get; set; } = string.Empty;

        /// <summary>
        /// Error message if generation failed.
        /// </summary>
        public string? ErrorMessage { get; set; }

        /// <summary>
        /// Duration of TTS generation in seconds.
        /// </summary>
        public double? TtsDuration { get; set; }

        /// <summary>
        /// Duration of normalization in seconds.
        /// </summary>
        public double? NormalizationDuration { get; set; }
    }
}
