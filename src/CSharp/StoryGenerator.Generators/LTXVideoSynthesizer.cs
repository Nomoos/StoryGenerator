using System;
using System.Diagnostics;
using System.IO;
using System.Threading.Tasks;

namespace StoryGenerator.Generators
{
    /// <summary>
    /// LTX-Video integration for generating short-form vertical videos (10-20 seconds)
    /// Recommended for TikTok, YouTube Shorts, and Instagram Reels
    /// </summary>
    public class LTXVideoSynthesizer : VideoSynthesisBase, ISceneVideoSynthesizer
    {
        private readonly string _modelId = "Lightricks/LTX-Video";
        private readonly int _defaultWidth;
        private readonly int _defaultHeight;
        private readonly int _defaultFps;
        
        /// <summary>
        /// Initialize LTX-Video synthesizer
        /// </summary>
        /// <param name="width">Video width (default: 1080 for vertical)</param>
        /// <param name="height">Video height (default: 1920 for vertical)</param>
        /// <param name="fps">Target frames per second (default: 30)</param>
        /// <param name="pythonPath">Path to Python executable</param>
        public LTXVideoSynthesizer(
            int width = 1080,
            int height = 1920,
            int fps = 30,
            string pythonPath = "python") : base(pythonPath)
        {
            _defaultWidth = width;
            _defaultHeight = height;
            _defaultFps = fps;
        }
        
        /// <summary>
        /// Generate video from text prompt (IVideoSynthesizer implementation)
        /// </summary>
        public async Task<bool> GenerateVideoAsync(
            string prompt,
            string outputPath,
            int duration,
            int? fps = null)
        {
            return await GenerateVideoAsync(prompt, outputPath, null, duration, fps);
        }
        
        /// <summary>
        /// Generate video from text prompt and optional keyframe
        /// </summary>
        /// <param name="prompt">Text description for video generation</param>
        /// <param name="outputPath">Path for output video file</param>
        /// <param name="keyframePath">Optional starting keyframe image</param>
        /// <param name="duration">Video duration in seconds (5-25)</param>
        /// <param name="fps">Target frames per second (24-30), overrides default</param>
        /// <returns>True if generation succeeded</returns>
        public async Task<bool> GenerateVideoAsync(
            string prompt,
            string outputPath,
            string? keyframePath,
            int duration,
            int? fps = null)
        {
            try
            {
                // Validate inputs
                if (string.IsNullOrEmpty(prompt))
                {
                    Console.WriteLine("❌ Prompt cannot be empty");
                    return false;
                }
                
                if (duration < 5 || duration > 25)
                {
                    Console.WriteLine("❌ Duration must be between 5 and 25 seconds");
                    return false;
                }
                
                if (!EnsureOutputDirectory(outputPath))
                    return false;
                
                // Validate keyframe if provided
                if (!string.IsNullOrEmpty(keyframePath) && !ValidateFile(keyframePath, "Keyframe"))
                    return false;
                
                Console.WriteLine($"🎬 Generating video with LTX-Video...");
                Console.WriteLine($"   Prompt: {prompt}");
                Console.WriteLine($"   Duration: {duration}s");
                
                // Build and execute Python script
                int targetFps = fps ?? _defaultFps;
                string pythonScript = BuildPythonScript(
                    prompt, outputPath, keyframePath, duration, targetFps);
                
                var stopwatch = Stopwatch.StartNew();
                bool success = await ExecutePythonScriptAsync(pythonScript);
                stopwatch.Stop();
                
                // Verify output
                if (success && File.Exists(outputPath))
                {
                    Console.WriteLine($"✅ Video generated in {stopwatch.Elapsed.TotalSeconds:F2}s: {outputPath}");
                    return true;
                }
                
                Console.WriteLine($"❌ Video generation failed");
                return false;
            }
            catch (Exception ex)
            {
                Console.WriteLine($"❌ Error in LTX-Video generation: {ex.Message}");
                return false;
            }
        }
        
        /// <summary>
        /// Generate video clip from scene with motion hints
        /// </summary>
        /// <param name="sceneDescription">Description of the scene</param>
        /// <param name="motionHint">Camera movement or motion guidance</param>
        /// <param name="outputPath">Path for output video file</param>
        /// <param name="startKeyframe">Optional starting keyframe</param>
        /// <param name="endKeyframe">Optional ending keyframe (not used by LTX-Video directly)</param>
        /// <param name="duration">Scene duration in seconds</param>
        /// <returns>True if generation succeeded</returns>
        public async Task<bool> GenerateSceneClipAsync(
            string sceneDescription,
            string motionHint,
            string outputPath,
            string? startKeyframe = null,
            string? endKeyframe = null,
            double duration = 5.0)
        {
            // Combine scene description with motion hint
            string fullPrompt = BuildScenePrompt(sceneDescription, motionHint);
            
            // Use start keyframe if available
            int durationSec = (int)Math.Ceiling(duration);
            
            return await GenerateVideoAsync(
                fullPrompt,
                outputPath,
                startKeyframe,
                durationSec,
                _defaultFps
            );
        }
        
        /// <summary>
        /// Build enhanced prompt with motion guidance and quality enhancers
        /// </summary>
        private string BuildScenePrompt(string description, string motionHint)
        {
            string prompt = description;
            
            // Add motion guidance
            if (!string.IsNullOrEmpty(motionHint))
            {
                prompt += $", {motionHint}";
            }
            
            // Add quality enhancers for better results
            prompt += ", smooth motion, cinematic, high quality, 4k, professional";
            
            return prompt;
        }
        
        /// <summary>
        /// Build Python script for LTX-Video execution
        /// </summary>
        private string BuildPythonScript(
            string prompt,
            string outputPath,
            string? keyframePath,
            int duration,
            int fps)
        {
            // Escape and normalize paths
            string escapedPrompt = EscapePythonString(prompt);
            string normalizedOutput = NormalizePath(outputPath);
            string normalizedKeyframe = !string.IsNullOrEmpty(keyframePath) 
                ? NormalizePath(keyframePath) 
                : "";
            
            int numFrames = duration * fps;
            
            string script = $@"
import torch
from diffusers import LTXPipeline
from PIL import Image
import sys

try:
    print('Loading LTX-Video pipeline...')
    
    # Load pipeline with optimizations
    pipe = LTXPipeline.from_pretrained(
        '{_modelId}',
        torch_dtype=torch.float16,
        use_safetensors=True
    )
    
    # Enable memory optimizations
    pipe.to('cuda')
    pipe.enable_attention_slicing()
    
    print('Pipeline loaded successfully')
    
    # Prepare parameters
    prompt = '''{escapedPrompt}'''
    num_frames = {numFrames}
    height = {_defaultHeight}
    width = {_defaultWidth}
    
    # Load keyframe if provided
    image = None
    keyframe_path = '{normalizedKeyframe}'
    if keyframe_path and keyframe_path != '':
        print(f'Loading keyframe: {{keyframe_path}}')
        image = Image.open(keyframe_path).convert('RGB')
        image = image.resize((width, height))
    
    print(f'Generating video: {{num_frames}} frames at {{width}}x{{height}}')
    
    # Generate video
    video = pipe(
        prompt=prompt,
        image=image,
        num_frames=num_frames,
        height=height,
        width=width,
        guidance_scale=7.5,
        num_inference_steps=50
    ).frames
    
    print('Video generated, exporting...')
    
    # Export video
    from diffusers.utils import export_to_video
    export_to_video(video[0], '{normalizedOutput}', fps={fps})
    
    print('Video exported successfully')
    
except Exception as e:
    print(f'Error: {{str(e)}}', file=sys.stderr)
    sys.exit(1)
";
            
            return script;
        }
    }
}
