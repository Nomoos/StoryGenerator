using System;

namespace PrismQ.VideoGenerator
{
    /// <summary>
    /// Video synthesis method types
    /// </summary>
    public enum VideoSynthesisMethod
    {
        /// <summary>
        /// LTX-Video - Fast generation for short vertical videos
        /// </summary>
        LTXVideo,
        
        /// <summary>
        /// SDXL + RIFE interpolation - High quality with fast interpolation
        /// </summary>
        SDXLWithRIFE,
        
        /// <summary>
        /// SDXL + FILM interpolation - High quality with balanced interpolation
        /// </summary>
        SDXLWithFILM,
        
        /// <summary>
        /// SDXL + DAIN interpolation - Maximum quality with slower interpolation
        /// </summary>
        SDXLWithDAIN
    }
    
    /// <summary>
    /// Factory interface for creating video synthesizer instances
    /// </summary>
    public interface IVideoSynthesizerFactory
    {
        /// <summary>
        /// Create a video synthesizer of the specified type
        /// </summary>
        /// <param name="method">The synthesis method to use</param>
        /// <param name="width">Video width</param>
        /// <param name="height">Video height</param>
        /// <param name="fps">Target frames per second</param>
        /// <returns>Configured video synthesizer instance</returns>
        IVideoSynthesizer CreateSynthesizer(
            VideoSynthesisMethod method,
            int width = 1080,
            int height = 1920,
            int fps = 30);
        
        /// <summary>
        /// Create a scene video synthesizer (with motion control)
        /// </summary>
        /// <param name="method">The synthesis method to use</param>
        /// <param name="width">Video width</param>
        /// <param name="height">Video height</param>
        /// <param name="fps">Target frames per second</param>
        /// <returns>Configured scene video synthesizer instance</returns>
        ISceneVideoSynthesizer CreateSceneSynthesizer(
            VideoSynthesisMethod method,
            int width = 1080,
            int height = 1920,
            int fps = 30);
        
        /// <summary>
        /// Create a keyframe-based video synthesizer
        /// </summary>
        /// <param name="interpolationMethod">Frame interpolation method</param>
        /// <param name="config">Optional custom configuration</param>
        /// <returns>Configured keyframe video synthesizer instance</returns>
        IKeyframeVideoSynthesizer CreateKeyframeSynthesizer(
            InterpolationMethod interpolationMethod = InterpolationMethod.RIFE,
            KeyframeVideoConfig config = null);
    }
    
    /// <summary>
    /// Default factory implementation for creating video synthesizers
    /// </summary>
    public class VideoSynthesizerFactory : IVideoSynthesizerFactory
    {
        private readonly string _pythonPath;
        
        /// <summary>
        /// Initialize video synthesizer factory
        /// </summary>
        /// <param name="pythonPath">Path to Python executable</param>
        public VideoSynthesizerFactory(string pythonPath = "python")
        {
            _pythonPath = pythonPath;
        }
        
        /// <summary>
        /// Create a video synthesizer of the specified type
        /// </summary>
        public IVideoSynthesizer CreateSynthesizer(
            VideoSynthesisMethod method,
            int width = 1080,
            int height = 1920,
            int fps = 30)
        {
            switch (method)
            {
                case VideoSynthesisMethod.LTXVideo:
                    return new LTXVideoSynthesizer(width, height, fps, _pythonPath);
                
                case VideoSynthesisMethod.SDXLWithRIFE:
                    return CreateKeyframeSynthesizerInternal(InterpolationMethod.RIFE, width, height, fps);
                
                case VideoSynthesisMethod.SDXLWithFILM:
                    return CreateKeyframeSynthesizerInternal(InterpolationMethod.FILM, width, height, fps);
                
                case VideoSynthesisMethod.SDXLWithDAIN:
                    return CreateKeyframeSynthesizerInternal(InterpolationMethod.DAIN, width, height, fps);
                
                default:
                    throw new ArgumentException($"Unsupported synthesis method: {method}");
            }
        }
        
        /// <summary>
        /// Create a scene video synthesizer (with motion control)
        /// </summary>
        public ISceneVideoSynthesizer CreateSceneSynthesizer(
            VideoSynthesisMethod method,
            int width = 1080,
            int height = 1920,
            int fps = 30)
        {
            switch (method)
            {
                case VideoSynthesisMethod.LTXVideo:
                    return new LTXVideoSynthesizer(width, height, fps, _pythonPath);
                
                // Other methods don't directly support ISceneVideoSynthesizer
                default:
                    throw new ArgumentException(
                        $"Method {method} does not support scene-based synthesis with motion control. " +
                        "Use LTXVideo for scene synthesis with motion hints.");
            }
        }
        
        /// <summary>
        /// Create a keyframe-based video synthesizer
        /// </summary>
        public IKeyframeVideoSynthesizer CreateKeyframeSynthesizer(
            InterpolationMethod interpolationMethod = InterpolationMethod.RIFE,
            KeyframeVideoConfig config = null)
        {
            if (config == null)
            {
                config = new KeyframeVideoConfig
                {
                    Method = interpolationMethod,
                    TargetFps = 30,
                    Width = 1080,
                    Height = 1920
                };
            }
            else
            {
                config.Method = interpolationMethod;
            }
            
            return new KeyframeVideoSynthesizer(config, _pythonPath);
        }
        
        /// <summary>
        /// Internal helper to create keyframe synthesizer as IVideoSynthesizer
        /// </summary>
        private IVideoSynthesizer CreateKeyframeSynthesizerInternal(
            InterpolationMethod method,
            int width,
            int height,
            int fps)
        {
            var config = new KeyframeVideoConfig
            {
                Method = method,
                TargetFps = fps,
                Width = width,
                Height = height
            };
            
            return new KeyframeVideoSynthesizer(config, _pythonPath);
        }
    }
}
