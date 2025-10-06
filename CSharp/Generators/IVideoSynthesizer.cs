using System;
using System.Collections.Generic;
using System.Threading.Tasks;

namespace StoryGenerator.Generators
{
    /// <summary>
    /// Core interface for video synthesis implementations
    /// Defines the contract for generating videos from prompts and keyframes
    /// </summary>
    public interface IVideoSynthesizer
    {
        /// <summary>
        /// Generate video from text prompt
        /// </summary>
        /// <param name="prompt">Text description for video generation</param>
        /// <param name="outputPath">Path for output video file</param>
        /// <param name="duration">Video duration in seconds</param>
        /// <param name="fps">Target frames per second</param>
        /// <returns>True if generation succeeded</returns>
        Task<bool> GenerateVideoAsync(
            string prompt,
            string outputPath,
            int duration,
            int? fps = null);
        
        /// <summary>
        /// Generate video from text prompt with optional keyframe
        /// </summary>
        /// <param name="prompt">Text description for video generation</param>
        /// <param name="outputPath">Path for output video file</param>
        /// <param name="keyframePath">Optional starting keyframe image</param>
        /// <param name="duration">Video duration in seconds</param>
        /// <param name="fps">Target frames per second</param>
        /// <returns>True if generation succeeded</returns>
        Task<bool> GenerateVideoAsync(
            string prompt,
            string outputPath,
            string keyframePath,
            int duration,
            int? fps = null);
    }
    
    /// <summary>
    /// Extended interface for video synthesis with scene and motion control
    /// </summary>
    public interface ISceneVideoSynthesizer : IVideoSynthesizer
    {
        /// <summary>
        /// Generate video clip from scene with motion hints
        /// </summary>
        /// <param name="sceneDescription">Description of the scene</param>
        /// <param name="motionHint">Camera movement or motion guidance</param>
        /// <param name="outputPath">Path for output video file</param>
        /// <param name="startKeyframe">Optional starting keyframe</param>
        /// <param name="endKeyframe">Optional ending keyframe</param>
        /// <param name="duration">Scene duration in seconds</param>
        /// <returns>True if generation succeeded</returns>
        Task<bool> GenerateSceneClipAsync(
            string sceneDescription,
            string motionHint,
            string outputPath,
            string startKeyframe = null,
            string endKeyframe = null,
            double duration = 5.0);
    }
    
    /// <summary>
    /// Interface for keyframe-based video synthesis
    /// </summary>
    public interface IKeyframeVideoSynthesizer : IVideoSynthesizer
    {
        /// <summary>
        /// Generate video from existing keyframes
        /// </summary>
        /// <param name="keyframePaths">List of keyframe image paths</param>
        /// <param name="outputPath">Output video file path</param>
        /// <param name="totalDuration">Total video duration in seconds</param>
        /// <param name="audioPath">Optional audio file to sync with video</param>
        /// <returns>True if generation succeeded</returns>
        Task<bool> GenerateFromKeyframesAsync(
            List<string> keyframePaths,
            string outputPath,
            double totalDuration,
            string audioPath = null);
        
        /// <summary>
        /// Generate complete scene with automatic keyframe generation
        /// </summary>
        /// <param name="sceneDescription">Description of the scene</param>
        /// <param name="outputPath">Output video file path</param>
        /// <param name="duration">Scene duration in seconds</param>
        /// <param name="audioPath">Optional audio file</param>
        /// <param name="stylePrompts">Additional style prompts for generation</param>
        /// <returns>True if generation succeeded</returns>
        Task<bool> GenerateSceneAsync(
            string sceneDescription,
            string outputPath,
            double duration,
            string audioPath = null,
            List<string> stylePrompts = null);
    }
    
    /// <summary>
    /// Interface for video synthesis configuration
    /// </summary>
    public interface IVideoSynthesisConfig
    {
        /// <summary>
        /// Target frames per second for output video
        /// </summary>
        int TargetFps { get; set; }
        
        /// <summary>
        /// Output video width
        /// </summary>
        int Width { get; set; }
        
        /// <summary>
        /// Output video height
        /// </summary>
        int Height { get; set; }
        
        /// <summary>
        /// Validate configuration settings
        /// </summary>
        /// <returns>True if configuration is valid</returns>
        bool Validate();
    }
    
    /// <summary>
    /// Interface for video synthesis comparison and evaluation
    /// </summary>
    public interface IVideoSynthesisComparator
    {
        /// <summary>
        /// Compare multiple video synthesis approaches
        /// </summary>
        /// <param name="testPrompt">Test scene description</param>
        /// <param name="testKeyframe">Optional test keyframe image</param>
        /// <param name="duration">Test video duration in seconds</param>
        /// <param name="outputDir">Directory for test outputs</param>
        /// <returns>Comparison results for each approach</returns>
        Task<Dictionary<string, Models.VideoClip>> CompareApproachesAsync(
            string testPrompt,
            string testKeyframe = null,
            double duration = 10.0,
            string outputDir = null);
    }
}
