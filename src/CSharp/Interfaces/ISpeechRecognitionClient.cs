using System;
using System.Collections.Generic;
using System.Threading;
using System.Threading.Tasks;

namespace StoryGenerator.Core.Interfaces
{
    /// <summary>
    /// Interface for speech recognition using faster-whisper or similar ASR models.
    /// Supports transcription with word-level timestamps and subtitle generation.
    /// </summary>
    /// <remarks>
    /// Recommended model: Systran/faster-whisper-large-v3
    /// See https://huggingface.co/Systran/faster-whisper-large-v3
    /// Performance: 4x faster than original Whisper, 50% less VRAM
    /// </remarks>
    public interface ISpeechRecognitionClient
    {
        /// <summary>
        /// Transcribe audio file to text with word-level timestamps.
        /// </summary>
        /// <param name="audioPath">Path to the audio file</param>
        /// <param name="language">Language code (e.g., "en", "es") or null for auto-detection</param>
        /// <param name="beamSize">Beam search size for better accuracy (default: 5)</param>
        /// <param name="wordTimestamps">Include word-level timestamps</param>
        /// <param name="cancellationToken">Cancellation token</param>
        /// <returns>Transcription result with segments and timing information</returns>
        Task<TranscriptionResult> TranscribeAsync(
            string audioPath,
            string? language = null,
            int beamSize = 5,
            bool wordTimestamps = true,
            CancellationToken cancellationToken = default);

        /// <summary>
        /// Transcribe audio and generate SRT subtitle file.
        /// </summary>
        /// <param name="audioPath">Path to the audio file</param>
        /// <param name="outputPath">Path to save the SRT file</param>
        /// <param name="language">Language code or null for auto-detection</param>
        /// <param name="maxWordsPerLine">Maximum words per subtitle line (default: 10)</param>
        /// <param name="cancellationToken">Cancellation token</param>
        /// <returns>Path to the generated SRT file</returns>
        Task<string> TranscribeToSrtAsync(
            string audioPath,
            string outputPath,
            string? language = null,
            int maxWordsPerLine = 10,
            CancellationToken cancellationToken = default);

        /// <summary>
        /// Detect the language of an audio file.
        /// </summary>
        /// <param name="audioPath">Path to the audio file</param>
        /// <param name="cancellationToken">Cancellation token</param>
        /// <returns>Detected language code and confidence score</returns>
        Task<LanguageDetectionResult> DetectLanguageAsync(
            string audioPath,
            CancellationToken cancellationToken = default);

        /// <summary>
        /// Get information about the loaded model.
        /// </summary>
        /// <returns>Model information including name, size, and capabilities</returns>
        ModelInfo GetModelInfo();
    }

    /// <summary>
    /// Result of a transcription operation.
    /// </summary>
    public class TranscriptionResult
    {
        /// <summary>
        /// Full transcribed text.
        /// </summary>
        public string Text { get; set; } = string.Empty;

        /// <summary>
        /// Detected language code (e.g., "en").
        /// </summary>
        public string Language { get; set; } = string.Empty;

        /// <summary>
        /// Confidence score for language detection (0.0-1.0).
        /// </summary>
        public double LanguageConfidence { get; set; }

        /// <summary>
        /// List of transcription segments with timing information.
        /// </summary>
        public List<TranscriptionSegment> Segments { get; set; } = new();

        /// <summary>
        /// Duration of the audio in seconds.
        /// </summary>
        public double Duration { get; set; }
    }

    /// <summary>
    /// A segment of transcribed audio with timing information.
    /// </summary>
    public class TranscriptionSegment
    {
        /// <summary>
        /// Segment ID.
        /// </summary>
        public int Id { get; set; }

        /// <summary>
        /// Start time in seconds.
        /// </summary>
        public double Start { get; set; }

        /// <summary>
        /// End time in seconds.
        /// </summary>
        public double End { get; set; }

        /// <summary>
        /// Transcribed text for this segment.
        /// </summary>
        public string Text { get; set; } = string.Empty;

        /// <summary>
        /// Word-level timestamps (if available).
        /// </summary>
        public List<WordTimestamp>? Words { get; set; }

        /// <summary>
        /// Confidence score for this segment (0.0-1.0).
        /// </summary>
        public double Confidence { get; set; }
    }

    /// <summary>
    /// Word-level timestamp information.
    /// </summary>
    public class WordTimestamp
    {
        /// <summary>
        /// The word text.
        /// </summary>
        public string Word { get; set; } = string.Empty;

        /// <summary>
        /// Start time in seconds.
        /// </summary>
        public double Start { get; set; }

        /// <summary>
        /// End time in seconds.
        /// </summary>
        public double End { get; set; }

        /// <summary>
        /// Confidence score (0.0-1.0).
        /// </summary>
        public double Confidence { get; set; }
    }

    /// <summary>
    /// Result of language detection.
    /// </summary>
    public class LanguageDetectionResult
    {
        /// <summary>
        /// Detected language code (e.g., "en", "es").
        /// </summary>
        public string Language { get; set; } = string.Empty;

        /// <summary>
        /// Confidence score (0.0-1.0).
        /// </summary>
        public double Confidence { get; set; }

        /// <summary>
        /// Alternative language predictions with confidence scores.
        /// </summary>
        public Dictionary<string, double> Alternatives { get; set; } = new();
    }

    /// <summary>
    /// Information about a loaded model.
    /// </summary>
    public class ModelInfo
    {
        /// <summary>
        /// Model name (e.g., "faster-whisper-large-v3").
        /// </summary>
        public string Name { get; set; } = string.Empty;

        /// <summary>
        /// Model version.
        /// </summary>
        public string Version { get; set; } = string.Empty;

        /// <summary>
        /// Model size in parameters.
        /// </summary>
        public string Size { get; set; } = string.Empty;

        /// <summary>
        /// Device the model is running on (e.g., "cuda", "cpu").
        /// </summary>
        public string Device { get; set; } = string.Empty;

        /// <summary>
        /// Compute type (e.g., "float16", "int8").
        /// </summary>
        public string ComputeType { get; set; } = string.Empty;

        /// <summary>
        /// Supported languages.
        /// </summary>
        public List<string> SupportedLanguages { get; set; } = new();
    }
}
