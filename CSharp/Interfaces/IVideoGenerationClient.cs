using System;
using System.Collections.Generic;
using System.Threading;
using System.Threading.Tasks;

namespace StoryGenerator.Core.Interfaces
{
    /// <summary>
    /// Interface for video generation/synthesis using models like LTX-Video.
    /// Supports text-to-video and image-to-video generation.
    /// </summary>
    /// <remarks>
    /// Recommended model: Lightricks/LTX-Video
    /// See https://huggingface.co/Lightricks/LTX-Video
    /// Supports variable resolutions and frame rates.
    /// Alternative: Stable Video Diffusion for image-to-video.
    /// </remarks>
    public interface IVideoGenerationClient
    {
        /// <summary>
        /// Generate video from a text prompt.
        /// </summary>
        /// <param name="prompt">Text description of the desired video</param>
        /// <param name="numFrames">Number of frames to generate (default: 121 for 5s at 24fps)</param>
        /// <param name="fps">Target frames per second (default: 24)</param>
        /// <param name="width">Video width in pixels (default: 768)</param>
        /// <param name="height">Video height in pixels (default: 512)</param>
        /// <param name="numInferenceSteps">Number of denoising steps (default: 50)</param>
        /// <param name="guidanceScale">How closely to follow the prompt (default: 7.5)</param>
        /// <param name="seed">Random seed for reproducibility</param>
        /// <param name="cancellationToken">Cancellation token</param>
        /// <returns>Generated video result</returns>
        Task<VideoGenerationResult> GenerateVideoAsync(
            string prompt,
            int numFrames = 121,
            int fps = 24,
            int width = 768,
            int height = 512,
            int numInferenceSteps = 50,
            double guidanceScale = 7.5,
            int? seed = null,
            CancellationToken cancellationToken = default);

        /// <summary>
        /// Generate video from an initial keyframe image.
        /// Useful for creating video clips from generated keyframes.
        /// </summary>
        /// <param name="keyframePath">Path to the starting keyframe image</param>
        /// <param name="prompt">Text description to guide the video generation</param>
        /// <param name="numFrames">Number of frames to generate</param>
        /// <param name="fps">Target frames per second</param>
        /// <param name="numInferenceSteps">Number of denoising steps</param>
        /// <param name="guidanceScale">Guidance scale</param>
        /// <param name="seed">Random seed for reproducibility</param>
        /// <param name="cancellationToken">Cancellation token</param>
        /// <returns>Generated video result</returns>
        Task<VideoGenerationResult> GenerateVideoFromKeyframeAsync(
            string keyframePath,
            string prompt,
            int numFrames = 121,
            int fps = 24,
            int numInferenceSteps = 50,
            double guidanceScale = 7.5,
            int? seed = null,
            CancellationToken cancellationToken = default);

        /// <summary>
        /// Generate video interpolating between two keyframes.
        /// Creates smooth transitions between scene changes.
        /// </summary>
        /// <param name="startKeyframePath">Path to the starting keyframe</param>
        /// <param name="endKeyframePath">Path to the ending keyframe</param>
        /// <param name="prompt">Text description for the transition</param>
        /// <param name="numFrames">Number of frames for the transition</param>
        /// <param name="fps">Target frames per second</param>
        /// <param name="cancellationToken">Cancellation token</param>
        /// <returns>Generated video result</returns>
        Task<VideoGenerationResult> GenerateVideoTransitionAsync(
            string startKeyframePath,
            string endKeyframePath,
            string prompt,
            int numFrames = 121,
            int fps = 24,
            CancellationToken cancellationToken = default);

        /// <summary>
        /// Generate a complete video sequence from multiple keyframes and scene descriptions.
        /// Automatically handles transitions between scenes.
        /// </summary>
        /// <param name="scenes">List of video scenes with keyframes and descriptions</param>
        /// <param name="fps">Target frames per second</param>
        /// <param name="transitionFrames">Number of frames for transitions between scenes</param>
        /// <param name="cancellationToken">Cancellation token</param>
        /// <returns>Generated video result</returns>
        Task<VideoGenerationResult> GenerateVideoSequenceAsync(
            List<VideoScene> scenes,
            int fps = 24,
            int transitionFrames = 24,
            CancellationToken cancellationToken = default);

        /// <summary>
        /// Add motion hints or camera movement instructions.
        /// </summary>
        /// <param name="motionType">Type of motion (pan, zoom, rotate, etc.)</param>
        /// <param name="intensity">Motion intensity (0.0-1.0)</param>
        /// <returns>True if motion hint was applied</returns>
        Task<bool> SetMotionHintAsync(string motionType, double intensity = 0.5);

        /// <summary>
        /// Save generated video to disk.
        /// </summary>
        /// <param name="result">Video generation result</param>
        /// <param name="outputPath">Path to save the video (MP4 format)</param>
        /// <param name="audioPath">Optional audio file to merge with video</param>
        /// <returns>Path to saved video</returns>
        Task<string> SaveVideoAsync(
            VideoGenerationResult result,
            string outputPath,
            string? audioPath = null);

        /// <summary>
        /// Get information about the loaded model.
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
    /// Represents a video scene for sequence generation.
    /// </summary>
    public class VideoScene
    {
        /// <summary>
        /// Scene number/index.
        /// </summary>
        public int SceneNumber { get; set; }

        /// <summary>
        /// Scene description/prompt.
        /// </summary>
        public string Description { get; set; } = string.Empty;

        /// <summary>
        /// Path to the keyframe image for this scene.
        /// </summary>
        public string KeyframePath { get; set; } = string.Empty;

        /// <summary>
        /// Duration of this scene in frames.
        /// </summary>
        public int DurationFrames { get; set; }

        /// <summary>
        /// Optional motion hint (e.g., "slow pan left", "zoom in").
        /// </summary>
        public string? MotionHint { get; set; }

        /// <summary>
        /// Optional camera angle (e.g., "wide shot", "close-up").
        /// </summary>
        public string? CameraAngle { get; set; }
    }

    /// <summary>
    /// Result of video generation.
    /// </summary>
    public class VideoGenerationResult
    {
        /// <summary>
        /// Generated video frames as byte arrays.
        /// Each frame is encoded as PNG or JPEG.
        /// </summary>
        public List<byte[]> Frames { get; set; } = new();

        /// <summary>
        /// Video frames per second.
        /// </summary>
        public int Fps { get; set; }

        /// <summary>
        /// Video width in pixels.
        /// </summary>
        public int Width { get; set; }

        /// <summary>
        /// Video height in pixels.
        /// </summary>
        public int Height { get; set; }

        /// <summary>
        /// Total number of frames.
        /// </summary>
        public int TotalFrames => Frames.Count;

        /// <summary>
        /// Video duration in seconds.
        /// </summary>
        public double DurationSeconds => Fps > 0 ? (double)TotalFrames / Fps : 0;

        /// <summary>
        /// Prompt(s) used for generation.
        /// </summary>
        public string Prompt { get; set; } = string.Empty;

        /// <summary>
        /// Random seed used for generation.
        /// </summary>
        public int? Seed { get; set; }

        /// <summary>
        /// Number of inference steps used.
        /// </summary>
        public int InferenceSteps { get; set; }

        /// <summary>
        /// Generation time in milliseconds.
        /// </summary>
        public long GenerationTimeMs { get; set; }

        /// <summary>
        /// Model used for generation.
        /// </summary>
        public string Model { get; set; } = string.Empty;

        /// <summary>
        /// Number of keyframes used (if any).
        /// </summary>
        public int KeyframeCount { get; set; }

        /// <summary>
        /// Metadata about the generated video.
        /// </summary>
        public Dictionary<string, string> Metadata { get; set; } = new();
    }
}
