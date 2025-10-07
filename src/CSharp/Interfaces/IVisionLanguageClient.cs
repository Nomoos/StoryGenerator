using System;
using System.Collections.Generic;
using System.Threading;
using System.Threading.Tasks;

namespace StoryGenerator.Core.Interfaces
{
    /// <summary>
    /// Interface for vision-language models that can understand and analyze images.
    /// Supports models like LLaVA-OneVision and Phi-3.5-vision.
    /// </summary>
    /// <remarks>
    /// Recommended models:
    /// - LLaVA-OneVision: https://huggingface.co/docs/transformers/en/model_doc/llava_onevision
    /// - Phi-3.5-vision: https://huggingface.co/microsoft/Phi-3.5-vision-instruct
    /// Used for scene understanding, keyframe validation, and visual consistency checking.
    /// </remarks>
    public interface IVisionLanguageClient
    {
        /// <summary>
        /// Analyze an image with a text prompt.
        /// </summary>
        /// <param name="imagePath">Path to the image file</param>
        /// <param name="prompt">Text prompt or question about the image</param>
        /// <param name="maxTokens">Maximum tokens to generate (default: 512)</param>
        /// <param name="temperature">Sampling temperature (default: 0.7)</param>
        /// <param name="cancellationToken">Cancellation token</param>
        /// <returns>Model's analysis or response</returns>
        Task<VisionLanguageResult> AnalyzeImageAsync(
            string imagePath,
            string prompt,
            int maxTokens = 512,
            double temperature = 0.7,
            CancellationToken cancellationToken = default);

        /// <summary>
        /// Analyze multiple images with a text prompt.
        /// Useful for comparing scenes or checking consistency across keyframes.
        /// </summary>
        /// <param name="imagePaths">Paths to multiple image files</param>
        /// <param name="prompt">Text prompt or question about the images</param>
        /// <param name="maxTokens">Maximum tokens to generate</param>
        /// <param name="temperature">Sampling temperature</param>
        /// <param name="cancellationToken">Cancellation token</param>
        /// <returns>Model's analysis or response</returns>
        Task<VisionLanguageResult> AnalyzeImagesAsync(
            List<string> imagePaths,
            string prompt,
            int maxTokens = 512,
            double temperature = 0.7,
            CancellationToken cancellationToken = default);

        /// <summary>
        /// Generate a description of an image.
        /// </summary>
        /// <param name="imagePath">Path to the image file</param>
        /// <param name="detailLevel">Level of detail (low, medium, high)</param>
        /// <param name="cancellationToken">Cancellation token</param>
        /// <returns>Generated description</returns>
        Task<string> DescribeImageAsync(
            string imagePath,
            string detailLevel = "medium",
            CancellationToken cancellationToken = default);

        /// <summary>
        /// Validate that a generated keyframe matches the expected scene description.
        /// </summary>
        /// <param name="imagePath">Path to the keyframe image</param>
        /// <param name="sceneDescription">Expected scene description</param>
        /// <param name="cancellationToken">Cancellation token</param>
        /// <returns>Validation result with match score and explanation</returns>
        Task<SceneValidationResult> ValidateSceneAsync(
            string imagePath,
            string sceneDescription,
            CancellationToken cancellationToken = default);

        /// <summary>
        /// Check visual consistency between multiple keyframes.
        /// </summary>
        /// <param name="keyframePaths">Paths to keyframe images in sequence</param>
        /// <param name="cancellationToken">Cancellation token</param>
        /// <returns>Consistency analysis</returns>
        Task<ConsistencyAnalysisResult> CheckConsistencyAsync(
            List<string> keyframePaths,
            CancellationToken cancellationToken = default);

        /// <summary>
        /// Get information about the loaded model.
        /// </summary>
        /// <returns>Model information</returns>
        ModelInfo GetModelInfo();
    }

    /// <summary>
    /// Result of vision-language analysis.
    /// </summary>
    public class VisionLanguageResult
    {
        /// <summary>
        /// Generated text response.
        /// </summary>
        public string Text { get; set; } = string.Empty;

        /// <summary>
        /// Number of tokens generated.
        /// </summary>
        public int TokensGenerated { get; set; }

        /// <summary>
        /// Processing time in milliseconds.
        /// </summary>
        public long ProcessingTimeMs { get; set; }

        /// <summary>
        /// Model used for analysis.
        /// </summary>
        public string Model { get; set; } = string.Empty;

        /// <summary>
        /// Number of images processed.
        /// </summary>
        public int ImageCount { get; set; }
    }

    /// <summary>
    /// Result of scene validation.
    /// </summary>
    public class SceneValidationResult
    {
        /// <summary>
        /// Whether the scene matches the description.
        /// </summary>
        public bool IsValid { get; set; }

        /// <summary>
        /// Match score (0.0-1.0).
        /// </summary>
        public double MatchScore { get; set; }

        /// <summary>
        /// Explanation of the validation result.
        /// </summary>
        public string Explanation { get; set; } = string.Empty;

        /// <summary>
        /// Elements that match the description.
        /// </summary>
        public List<string> MatchingElements { get; set; } = new();

        /// <summary>
        /// Elements that don't match or are missing.
        /// </summary>
        public List<string> MismatchedElements { get; set; } = new();

        /// <summary>
        /// Suggestions for improvement.
        /// </summary>
        public List<string> Suggestions { get; set; } = new();
    }

    /// <summary>
    /// Result of visual consistency analysis.
    /// </summary>
    public class ConsistencyAnalysisResult
    {
        /// <summary>
        /// Overall consistency score (0.0-1.0).
        /// </summary>
        public double ConsistencyScore { get; set; }

        /// <summary>
        /// Whether the keyframes are visually consistent.
        /// </summary>
        public bool IsConsistent { get; set; }

        /// <summary>
        /// Detailed analysis of consistency.
        /// </summary>
        public string Analysis { get; set; } = string.Empty;

        /// <summary>
        /// Consistent elements across keyframes.
        /// </summary>
        public List<string> ConsistentElements { get; set; } = new();

        /// <summary>
        /// Inconsistent elements or issues found.
        /// </summary>
        public List<string> InconsistentElements { get; set; } = new();

        /// <summary>
        /// Pairwise consistency scores between adjacent keyframes.
        /// </summary>
        public Dictionary<string, double> PairwiseScores { get; set; } = new();
    }
}
