using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Threading.Tasks;

namespace StoryGenerator.Generators
{
    /// <summary>
    /// Configuration for keyframe-based video synthesis using SDXL + frame interpolation
    /// </summary>
    public class KeyframeVideoConfig
    {
        /// <summary>
        /// Target frames per second for output video
        /// </summary>
        public int TargetFps { get; set; } = 30;
        
        /// <summary>
        /// Frame interpolation method to use
        /// </summary>
        public InterpolationMethod Method { get; set; } = InterpolationMethod.RIFE;
        
        /// <summary>
        /// Output video width
        /// </summary>
        public int Width { get; set; } = 1080;
        
        /// <summary>
        /// Output video height
        /// </summary>
        public int Height { get; set; } = 1920;
        
        /// <summary>
        /// Number of keyframes to generate per scene
        /// </summary>
        public int KeyframesPerScene { get; set; } = 3;
        
        /// <summary>
        /// SDXL inference steps for keyframe generation
        /// </summary>
        public int InferenceSteps { get; set; } = 40;
        
        /// <summary>
        /// Guidance scale for SDXL generation
        /// </summary>
        public double GuidanceScale { get; set; } = 7.5;
    }
    
    /// <summary>
    /// Frame interpolation methods
    /// </summary>
    public enum InterpolationMethod
    {
        /// <summary>
        /// Real-Time Intermediate Flow Estimation (fastest, good quality)
        /// </summary>
        RIFE,
        
        /// <summary>
        /// Depth-Aware Video Frame Interpolation (slower, best quality)
        /// </summary>
        DAIN,
        
        /// <summary>
        /// Frame Interpolation for Large Motion (balanced speed and quality)
        /// </summary>
        FILM
    }
    
    /// <summary>
    /// SDXL + Frame Interpolation video synthesis
    /// Provides highest quality keyframes with flexible interpolation
    /// </summary>
    public class KeyframeVideoSynthesizer : VideoSynthesisBase
    {
        private readonly KeyframeVideoConfig _config;
        
        /// <summary>
        /// Initialize keyframe-based video synthesizer
        /// </summary>
        /// <param name="config">Configuration options</param>
        /// <param name="pythonPath">Path to Python executable</param>
        public KeyframeVideoSynthesizer(
            KeyframeVideoConfig config = null,
            string pythonPath = "python") : base(pythonPath)
        {
            _config = config ?? new KeyframeVideoConfig();
        }
        
        /// <summary>
        /// Generate video from existing keyframes
        /// </summary>
        /// <param name="keyframePaths">List of keyframe image paths</param>
        /// <param name="outputPath">Output video file path</param>
        /// <param name="totalDuration">Total video duration in seconds</param>
        /// <param name="audioPath">Optional audio file to sync with video</param>
        /// <returns>True if generation succeeded</returns>
        public async Task<bool> GenerateFromKeyframesAsync(
            List<string> keyframePaths,
            string outputPath,
            double totalDuration,
            string audioPath = null)
        {
            try
            {
                Console.WriteLine($"🎬 Generating video from {keyframePaths.Count} keyframes");
                
                // Step 1: Validate keyframes
                if (!ValidateKeyframes(keyframePaths))
                    return false;
                
                if (!EnsureOutputDirectory(outputPath))
                    return false;
                
                // Step 2: Calculate frame distribution
                var frameDistribution = CalculateFrameDistribution(
                    keyframePaths.Count, totalDuration);
                
                Console.WriteLine($"   Total duration: {totalDuration}s");
                Console.WriteLine($"   Target FPS: {_config.TargetFps}");
                Console.WriteLine($"   Interpolation method: {_config.Method}");
                
                // Step 3: Interpolate between keyframes
                var interpolatedFrames = await InterpolateFramesAsync(
                    keyframePaths, frameDistribution);
                
                if (interpolatedFrames == null || !interpolatedFrames.Any())
                {
                    Console.WriteLine("❌ Frame interpolation failed");
                    return false;
                }
                
                Console.WriteLine($"   Generated {interpolatedFrames.Count} interpolated frames");
                
                // Step 4: Assemble video with FFmpeg
                bool assembled = await AssembleVideoAsync(
                    interpolatedFrames, outputPath, audioPath);
                
                if (assembled)
                {
                    Console.WriteLine($"✅ Video generated: {outputPath}");
                    return true;
                }
                
                return false;
            }
            catch (Exception ex)
            {
                Console.WriteLine($"❌ Error in keyframe video generation: {ex.Message}");
                return false;
            }
        }
        
        /// <summary>
        /// Generate complete scene with automatic keyframe generation
        /// </summary>
        /// <param name="sceneDescription">Description of the scene</param>
        /// <param name="outputPath">Output video file path</param>
        /// <param name="duration">Scene duration in seconds</param>
        /// <param name="audioPath">Optional audio file</param>
        /// <param name="stylePrompts">Additional style prompts for SDXL</param>
        /// <returns>True if generation succeeded</returns>
        public async Task<bool> GenerateSceneAsync(
            string sceneDescription,
            string outputPath,
            double duration,
            string audioPath = null,
            List<string> stylePrompts = null)
        {
            try
            {
                Console.WriteLine($"🎬 Generating scene with SDXL + {_config.Method}");
                Console.WriteLine($"   Description: {sceneDescription}");
                
                // Step 1: Generate keyframes with SDXL
                var keyframes = await GenerateKeyframesAsync(
                    sceneDescription, stylePrompts);
                
                if (keyframes == null || !keyframes.Any())
                {
                    Console.WriteLine("❌ Keyframe generation failed");
                    return false;
                }
                
                // Step 2: Interpolate and assemble
                return await GenerateFromKeyframesAsync(
                    keyframes, outputPath, duration, audioPath);
            }
            catch (Exception ex)
            {
                Console.WriteLine($"❌ Error in scene generation: {ex.Message}");
                return false;
            }
        }
        
        /// <summary>
        /// Generate keyframes using SDXL
        /// </summary>
        private async Task<List<string>> GenerateKeyframesAsync(
            string sceneDescription,
            List<string> stylePrompts = null)
        {
            var keyframes = new List<string>();
            string tempDir = Path.Combine(
                Path.GetTempPath(),
                $"keyframes_{Guid.NewGuid()}");
            Directory.CreateDirectory(tempDir);
            
            try
            {
                Console.WriteLine($"   Generating {_config.KeyframesPerScene} keyframes with SDXL...");
                
                // Generate keyframes at different scene positions
                for (int i = 0; i < _config.KeyframesPerScene; i++)
                {
                    double position = _config.KeyframesPerScene > 1
                        ? i / (double)(_config.KeyframesPerScene - 1)
                        : 0.5;
                    
                    string prompt = BuildKeyframePrompt(
                        sceneDescription, position, stylePrompts);
                    
                    string keyframePath = Path.Combine(
                        tempDir, $"keyframe_{i:D3}.png");
                    
                    Console.WriteLine($"     Keyframe {i + 1}/{_config.KeyframesPerScene} " +
                        $"(position: {position:P0})");
                    
                    bool generated = await GenerateKeyframeWithSDXLAsync(
                        prompt, keyframePath);
                    
                    if (generated)
                        keyframes.Add(keyframePath);
                    else
                        Console.WriteLine($"⚠️ Failed to generate keyframe {i}");
                }
                
                return keyframes;
            }
            catch (Exception ex)
            {
                Console.WriteLine($"❌ Keyframe generation error: {ex.Message}");
                return null;
            }
        }
        
        /// <summary>
        /// Build prompt for keyframe at specific position
        /// </summary>
        private string BuildKeyframePrompt(
            string description,
            double position,
            List<string> stylePrompts)
        {
            string prompt = description;
            
            // Add position-based variations for better scene flow
            if (position <= 0.1)
                prompt += ", opening shot, establishing scene, wide angle";
            else if (position >= 0.9)
                prompt += ", closing shot, conclusion, pull back";
            else
                prompt += ", mid action, dynamic composition";
            
            // Add style elements
            if (stylePrompts != null && stylePrompts.Any())
            {
                prompt += ", " + string.Join(", ", stylePrompts);
            }
            
            // Add quality enhancers
            prompt += ", cinematic lighting, high detail, 4k quality, professional photography";
            
            return prompt;
        }
        
        /// <summary>
        /// Generate single keyframe using SDXL
        /// </summary>
        private async Task<bool> GenerateKeyframeWithSDXLAsync(
            string prompt,
            string outputPath)
        {
            string escapedPrompt = EscapePythonString(prompt);
            string normalizedOutput = NormalizePath(outputPath);
            
            string pythonScript = $@"
import torch
from diffusers import StableDiffusionXLPipeline
import sys

try:
    print('Loading SDXL pipeline...')
    
    # Load SDXL pipeline with optimizations
    pipe = StableDiffusionXLPipeline.from_pretrained(
        'stabilityai/stable-diffusion-xl-base-1.0',
        torch_dtype=torch.float16,
        use_safetensors=True,
        variant='fp16'
    )
    pipe.to('cuda')
    
    # Enable memory optimizations
    pipe.enable_attention_slicing()
    
    print('Generating keyframe...')
    
    # Generate image
    image = pipe(
        prompt='''{escapedPrompt}''',
        height={_config.Height},
        width={_config.Width},
        num_inference_steps={_config.InferenceSteps},
        guidance_scale={_config.GuidanceScale}
    ).images[0]
    
    # Save image
    image.save('{normalizedOutput}')
    print('Keyframe saved successfully')
    
except Exception as e:
    print(f'Error: {{str(e)}}', file=sys.stderr)
    sys.exit(1)
";
            
            return await ExecutePythonScriptAsync(pythonScript);
        }
        
        /// <summary>
        /// Interpolate frames between keyframes
        /// </summary>
        private async Task<List<string>> InterpolateFramesAsync(
            List<string> keyframePaths,
            Dictionary<int, int> frameDistribution)
        {
            var allFrames = new List<string>();
            string outputDir = Path.Combine(
                Path.GetTempPath(),
                $"interpolated_{Guid.NewGuid()}");
            Directory.CreateDirectory(outputDir);
            
            try
            {
                Console.WriteLine("   Interpolating frames...");
                
                // Add first keyframe
                allFrames.Add(keyframePaths[0]);
                
                // Process each keyframe pair
                for (int i = 0; i < keyframePaths.Count - 1; i++)
                {
                    string frame1 = keyframePaths[i];
                    string frame2 = keyframePaths[i + 1];
                    int targetFrames = frameDistribution[i];
                    
                    Console.WriteLine($"     Segment {i + 1}: {targetFrames} frames");
                    
                    var interpolated = await InterpolatePairAsync(
                        frame1, frame2, targetFrames, outputDir, i);
                    
                    if (interpolated != null && interpolated.Any())
                    {
                        // Skip first frame (duplicate of previous keyframe)
                        allFrames.AddRange(interpolated.Skip(1));
                    }
                }
                
                return allFrames;
            }
            catch (Exception ex)
            {
                Console.WriteLine($"❌ Interpolation error: {ex.Message}");
                return null;
            }
        }
        
        /// <summary>
        /// Interpolate frames between two keyframes using selected method
        /// </summary>
        private async Task<List<string>> InterpolatePairAsync(
            string frame1Path,
            string frame2Path,
            int targetFrames,
            string outputDir,
            int segmentIndex)
        {
            string method = _config.Method.ToString().ToLower();
            string normalizedFrame1 = NormalizePath(frame1Path);
            string normalizedFrame2 = NormalizePath(frame2Path);
            string normalizedOutput = NormalizePath(outputDir);
            
            // Build Python script based on interpolation method
            string pythonScript = BuildInterpolationScript(
                method, normalizedFrame1, normalizedFrame2,
                targetFrames, normalizedOutput, segmentIndex);
            
            bool success = await ExecutePythonScriptAsync(pythonScript);
            
            if (!success)
                return null;
            
            // Collect generated frame paths
            var frames = new List<string>();
            for (int i = 0; i < targetFrames; i++)
            {
                string framePath = Path.Combine(
                    outputDir,
                    $"seg{segmentIndex:D2}_frame_{i:06d}.png");
                
                if (File.Exists(framePath))
                    frames.Add(framePath);
            }
            
            return frames;
        }
        
        /// <summary>
        /// Build interpolation script for the specified method
        /// </summary>
        private string BuildInterpolationScript(
            string method,
            string frame1,
            string frame2,
            int numFrames,
            string outputDir,
            int segmentIndex)
        {
            // Note: This is a simplified example. Actual implementation would
            // depend on the specific interpolation library being used.
            
            string script = $@"
import sys
import os
from PIL import Image
import numpy as np

try:
    print('Loading frames...')
    frame1 = Image.open('{frame1}').convert('RGB')
    frame2 = Image.open('{frame2}').convert('RGB')
    
    # Method-specific interpolation
    method = '{method}'
    num_frames = {numFrames}
    
    frames = []
    
    if method == 'rife':
        # RIFE implementation (requires rife library)
        # Note: This is pseudocode - actual implementation varies
        try:
            from rife import RIFE
            model = RIFE()
            frames = model.interpolate(frame1, frame2, num_frames)
        except ImportError:
            print('RIFE not available, using linear interpolation', file=sys.stderr)
            # Fallback to simple blend
            for i in range(num_frames):
                alpha = i / (num_frames - 1)
                blended = Image.blend(frame1, frame2, alpha)
                frames.append(blended)
    
    elif method == 'film':
        # FILM implementation
        try:
            from film import FILM
            model = FILM()
            frames = model.interpolate(frame1, frame2, num_frames)
        except ImportError:
            print('FILM not available, using linear interpolation', file=sys.stderr)
            for i in range(num_frames):
                alpha = i / (num_frames - 1)
                blended = Image.blend(frame1, frame2, alpha)
                frames.append(blended)
    
    elif method == 'dain':
        # DAIN implementation
        try:
            from dain import DAIN
            model = DAIN()
            frames = model.interpolate(frame1, frame2, num_frames)
        except ImportError:
            print('DAIN not available, using linear interpolation', file=sys.stderr)
            for i in range(num_frames):
                alpha = i / (num_frames - 1)
                blended = Image.blend(frame1, frame2, alpha)
                frames.append(blended)
    
    else:
        # Default: linear interpolation
        for i in range(num_frames):
            alpha = i / (num_frames - 1) if num_frames > 1 else 0.5
            blended = Image.blend(frame1, frame2, alpha)
            frames.append(blended)
    
    # Save interpolated frames
    for i, frame in enumerate(frames):
        output_path = os.path.join(
            '{outputDir}',
            f'seg{segmentIndex:02d}_frame_{{i:06d}}.png'
        )
        frame.save(output_path)
    
    print(f'Generated {{len(frames)}} frames')
    
except Exception as e:
    print(f'Error: {{str(e)}}', file=sys.stderr)
    sys.exit(1)
";
            
            return script;
        }
        
        /// <summary>
        /// Assemble video from frames using FFmpeg
        /// </summary>
        private async Task<bool> AssembleVideoAsync(
            List<string> framePaths,
            string outputPath,
            string audioPath)
        {
            try
            {
                Console.WriteLine("   Assembling video with FFmpeg...");
                
                // Create temporary file list for FFmpeg concat
                string fileList = Path.Combine(
                    Path.GetTempPath(),
                    $"frames_{Guid.NewGuid()}.txt");
                
                // Write frame paths to file list
                var fileListContent = framePaths.Select(p =>
                    $"file '{NormalizePath(p)}'").ToList();
                await File.WriteAllLinesAsync(fileList, fileListContent);
                
                // Build FFmpeg command
                string normalizedOutput = NormalizePath(outputPath);
                string ffmpegArgs = $"-y -f concat -safe 0 -i \"{fileList}\" " +
                    $"-vf \"fps={_config.TargetFps},scale={_config.Width}:{_config.Height}:flags=lanczos\" " +
                    $"-c:v libx264 -preset medium -crf 23 -pix_fmt yuv420p ";
                
                // Add audio if provided
                if (!string.IsNullOrEmpty(audioPath) && File.Exists(audioPath))
                {
                    string normalizedAudio = NormalizePath(audioPath);
                    ffmpegArgs += $"-i \"{normalizedAudio}\" -c:a aac -b:a 192k -shortest ";
                }
                
                ffmpegArgs += $"\"{normalizedOutput}\"";
                
                // Execute FFmpeg
                var processInfo = new System.Diagnostics.ProcessStartInfo
                {
                    FileName = "ffmpeg",
                    Arguments = ffmpegArgs,
                    RedirectStandardOutput = true,
                    RedirectStandardError = true,
                    UseShellExecute = false,
                    CreateNoWindow = true
                };
                
                using var process = System.Diagnostics.Process.Start(processInfo);
                if (process == null)
                    return false;
                
                await process.WaitForExitAsync();
                
                // Cleanup
                if (File.Exists(fileList))
                    File.Delete(fileList);
                
                bool success = process.ExitCode == 0 && File.Exists(outputPath);
                
                if (success)
                    Console.WriteLine("   Video assembly complete");
                else
                    Console.WriteLine("   Video assembly failed");
                
                return success;
            }
            catch (Exception ex)
            {
                Console.WriteLine($"❌ FFmpeg assembly error: {ex.Message}");
                return false;
            }
        }
        
        /// <summary>
        /// Calculate frame distribution across keyframe segments
        /// </summary>
        private Dictionary<int, int> CalculateFrameDistribution(
            int numKeyframes,
            double totalDuration)
        {
            int totalFrames = (int)(totalDuration * _config.TargetFps);
            int segments = numKeyframes - 1;
            
            if (segments <= 0)
                return new Dictionary<int, int>();
            
            int framesPerSegment = totalFrames / segments;
            int remainder = totalFrames % segments;
            
            var distribution = new Dictionary<int, int>();
            for (int i = 0; i < segments; i++)
            {
                // Distribute remainder frames across segments
                distribution[i] = framesPerSegment + (i < remainder ? 1 : 0);
            }
            
            return distribution;
        }
        
        /// <summary>
        /// Validate that all keyframes exist and are valid images
        /// </summary>
        private bool ValidateKeyframes(List<string> keyframePaths)
        {
            if (keyframePaths == null || !keyframePaths.Any())
            {
                Console.WriteLine("❌ No keyframes provided");
                return false;
            }
            
            if (keyframePaths.Count < 2)
            {
                Console.WriteLine("❌ At least 2 keyframes are required for interpolation");
                return false;
            }
            
            for (int i = 0; i < keyframePaths.Count; i++)
            {
                if (!ValidateFile(keyframePaths[i], $"Keyframe {i + 1}"))
                    return false;
            }
            
            return true;
        }
    }
}
