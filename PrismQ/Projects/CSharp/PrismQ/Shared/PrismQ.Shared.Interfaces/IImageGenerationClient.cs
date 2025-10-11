using System;
using System.Threading;
using System.Threading.Tasks;

namespace PrismQ.Shared.Interfaces
{
    /// <summary>
    /// Result of image generation
    /// </summary>
    public class ImageGenerationResult
    {
        public byte[] ImageData { get; set; } = Array.Empty<byte>();
        public int Width { get; set; }
        public int Height { get; set; }
        public int? Seed { get; set; }
        public long GenerationTimeMs { get; set; }
    }

    /// <summary>
    /// Interface for image generation clients (SDXL, Stable Diffusion, etc.)
    /// </summary>
    public interface IImageGenerationClient
    {
        /// <summary>
        /// Generate an image from a text prompt
        /// </summary>
        /// <param name="prompt">Text prompt for image generation</param>
        /// <param name="negativePrompt">Negative prompt to avoid unwanted elements</param>
        /// <param name="width">Image width</param>
        /// <param name="height">Image height</param>
        /// <param name="steps">Number of inference steps</param>
        /// <param name="guidanceScale">Guidance scale</param>
        /// <param name="seed">Random seed (optional)</param>
        /// <param name="cancellationToken">Cancellation token</param>
        /// <returns>Path to the generated image</returns>
        Task<string> GenerateImageAsync(
            string prompt,
            string negativePrompt,
            int width,
            int height,
            int steps,
            double guidanceScale,
            int? seed = null,
            CancellationToken cancellationToken = default);

        /// <summary>
        /// Generate an image with refiner
        /// </summary>
        Task<ImageGenerationResult> GenerateImageWithRefinerAsync(
            string prompt,
            string negativePrompt,
            int width,
            int height,
            int baseSteps,
            int refinerSteps,
            double guidanceScale,
            int? seed = null,
            CancellationToken cancellationToken = default);

        /// <summary>
        /// Load a LoRA model
        /// </summary>
        Task LoadLoraAsync(string loraPath, double scale, CancellationToken cancellationToken = default);

        /// <summary>
        /// Unload LoRA model
        /// </summary>
        Task UnloadLoraAsync(CancellationToken cancellationToken = default);

        /// <summary>
        /// Save image data to file
        /// </summary>
        Task<string> SaveImageAsync(byte[] imageData, string outputPath, CancellationToken cancellationToken = default);
    }
}
