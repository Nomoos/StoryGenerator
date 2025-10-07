using System;
using System.Collections.Generic;
using System.Threading;
using System.Threading.Tasks;

namespace StoryGenerator.Core.Interfaces
{
    /// <summary>
    /// Interface for image generation using Stable Diffusion XL and similar models.
    /// Supports text-to-image generation with optional refiner for higher quality.
    /// </summary>
    /// <remarks>
    /// Recommended model: stabilityai/stable-diffusion-xl-base-1.0
    /// See https://huggingface.co/docs/diffusers/en/using-diffusers/sdxl
    /// Native resolution: 1024x1024
    /// Optional refiner: stabilityai/stable-diffusion-xl-refiner-1.0
    /// </remarks>
    public interface IImageGenerationClient
    {
        /// <summary>
        /// Generate an image from a text prompt.
        /// </summary>
        /// <param name="prompt">Positive text prompt describing the desired image</param>
        /// <param name="negativePrompt">Optional negative prompt to avoid unwanted elements</param>
        /// <param name="width">Image width in pixels (default: 1024)</param>
        /// <param name="height">Image height in pixels (default: 1024)</param>
        /// <param name="numInferenceSteps">Number of denoising steps (default: 30)</param>
        /// <param name="guidanceScale">How closely to follow the prompt (default: 7.5)</param>
        /// <param name="seed">Random seed for reproducibility (optional)</param>
        /// <param name="cancellationToken">Cancellation token</param>
        /// <returns>Generated image result</returns>
        Task<ImageGenerationResult> GenerateImageAsync(
            string prompt,
            string? negativePrompt = null,
            int width = 1024,
            int height = 1024,
            int numInferenceSteps = 30,
            double guidanceScale = 7.5,
            int? seed = null,
            CancellationToken cancellationToken = default);

        /// <summary>
        /// Generate an image with the refiner for higher quality.
        /// Requires both base and refiner models to be loaded.
        /// </summary>
        /// <param name="prompt">Positive text prompt</param>
        /// <param name="negativePrompt">Optional negative prompt</param>
        /// <param name="width">Image width in pixels</param>
        /// <param name="height">Image height in pixels</param>
        /// <param name="baseSteps">Number of steps for base model (default: 40)</param>
        /// <param name="refinerSteps">Number of steps for refiner (default: 20)</param>
        /// <param name="guidanceScale">Guidance scale</param>
        /// <param name="seed">Random seed for reproducibility</param>
        /// <param name="cancellationToken">Cancellation token</param>
        /// <returns>Generated image result</returns>
        Task<ImageGenerationResult> GenerateImageWithRefinerAsync(
            string prompt,
            string? negativePrompt = null,
            int width = 1024,
            int height = 1024,
            int baseSteps = 40,
            int refinerSteps = 20,
            double guidanceScale = 7.5,
            int? seed = null,
            CancellationToken cancellationToken = default);

        /// <summary>
        /// Generate multiple images from the same prompt for variety.
        /// </summary>
        /// <param name="prompt">Positive text prompt</param>
        /// <param name="negativePrompt">Optional negative prompt</param>
        /// <param name="count">Number of images to generate</param>
        /// <param name="width">Image width in pixels</param>
        /// <param name="height">Image height in pixels</param>
        /// <param name="numInferenceSteps">Number of denoising steps</param>
        /// <param name="guidanceScale">Guidance scale</param>
        /// <param name="cancellationToken">Cancellation token</param>
        /// <returns>List of generated image results</returns>
        Task<List<ImageGenerationResult>> GenerateImageBatchAsync(
            string prompt,
            string? negativePrompt = null,
            int count = 4,
            int width = 1024,
            int height = 1024,
            int numInferenceSteps = 30,
            double guidanceScale = 7.5,
            CancellationToken cancellationToken = default);

        /// <summary>
        /// Apply a LoRA (Low-Rank Adaptation) to the model for style transfer.
        /// </summary>
        /// <param name="loraPath">Path to the LoRA weights</param>
        /// <param name="scale">LoRA scale/strength (0.0-1.0, default: 0.75)</param>
        /// <returns>True if LoRA was loaded successfully</returns>
        Task<bool> LoadLoraAsync(string loraPath, double scale = 0.75);

        /// <summary>
        /// Remove currently loaded LoRA.
        /// </summary>
        /// <returns>True if LoRA was unloaded successfully</returns>
        Task<bool> UnloadLoraAsync();

        /// <summary>
        /// Save generated image to disk.
        /// </summary>
        /// <param name="result">Image generation result</param>
        /// <param name="outputPath">Path to save the image (PNG format)</param>
        /// <returns>Path to saved image</returns>
        Task<string> SaveImageAsync(ImageGenerationResult result, string outputPath);

        /// <summary>
        /// Get information about the loaded model(s).
        /// </summary>
        /// <returns>Model information</returns>
        ModelInfo GetModelInfo();

        /// <summary>
        /// Check if the model is ready for generation.
        /// </summary>
        /// <returns>True if model is loaded and ready</returns>
        Task<bool> IsReadyAsync();
    }

    /// <summary>
    /// Result of image generation.
    /// </summary>
    public class ImageGenerationResult
    {
        /// <summary>
        /// Generated image as byte array (PNG format).
        /// </summary>
        public byte[] ImageData { get; set; } = Array.Empty<byte>();

        /// <summary>
        /// Image width in pixels.
        /// </summary>
        public int Width { get; set; }

        /// <summary>
        /// Image height in pixels.
        /// </summary>
        public int Height { get; set; }

        /// <summary>
        /// Prompt used for generation.
        /// </summary>
        public string Prompt { get; set; } = string.Empty;

        /// <summary>
        /// Negative prompt used (if any).
        /// </summary>
        public string? NegativePrompt { get; set; }

        /// <summary>
        /// Random seed used for generation.
        /// </summary>
        public int? Seed { get; set; }

        /// <summary>
        /// Number of inference steps used.
        /// </summary>
        public int InferenceSteps { get; set; }

        /// <summary>
        /// Guidance scale used.
        /// </summary>
        public double GuidanceScale { get; set; }

        /// <summary>
        /// Generation time in milliseconds.
        /// </summary>
        public long GenerationTimeMs { get; set; }

        /// <summary>
        /// Model used for generation.
        /// </summary>
        public string Model { get; set; } = string.Empty;

        /// <summary>
        /// Whether refiner was used.
        /// </summary>
        public bool UsedRefiner { get; set; }
    }
}
