# Video Synthesis Research & Implementation Guide

## Overview

This document provides comprehensive research and implementation guidance for video synthesis from keyframes and shot prompts. It covers two primary approaches and their integration with the StoryGenerator pipeline.

---

## Approach A: LTX-Video (Recommended for Short-Form Content)

### Overview
LTX-Video by Lightricks is a state-of-the-art video generation model optimized for short-form vertical video content (10-20 seconds).

### Key Features
- **Fast generation**: ~20-30 seconds for 10-second clips
- **Native vertical support**: Optimized for 9:16 aspect ratio
- **High quality**: Temporal consistency and smooth motion
- **Lower VRAM**: ~12GB VRAM requirement
- **Simple API**: Python and CLI interfaces available

### Technical Specifications

#### Model Details
- **Model ID**: `Lightricks/LTX-Video`
- **Architecture**: Latent diffusion-based video generation
- **Input**: Text prompt + optional start frame
- **Output**: MP4 video (customizable resolution)
- **Frame Rate**: 24-30 fps
- **Duration**: 5-25 seconds per clip

#### Resolution Support
- **Vertical (9:16)**: 576x1024, 720x1280, 1080x1920
- **Square (1:1)**: 768x768, 1024x1024
- **Horizontal (16:9)**: 1024x576, 1280x720

### C# Integration Pattern

```csharp
using System;
using System.Diagnostics;
using System.IO;
using System.Threading.Tasks;

namespace StoryGenerator.VideoSynthesis
{
    /// <summary>
    /// LTX-Video integration for generating short-form vertical videos
    /// </summary>
    public class LTXVideoSynthesizer
    {
        private readonly string _pythonPath;
        private readonly string _modelId = "Lightricks/LTX-Video";
        private readonly int _defaultWidth = 1080;
        private readonly int _defaultHeight = 1920;
        
        public LTXVideoSynthesizer(string pythonPath = "python")
        {
            _pythonPath = pythonPath;
        }
        
        /// <summary>
        /// Generate video from text prompt and optional keyframe
        /// </summary>
        /// <param name="prompt">Text description for video generation</param>
        /// <param name="outputPath">Path for output video file</param>
        /// <param name="keyframePath">Optional starting keyframe image</param>
        /// <param name="duration">Video duration in seconds (5-25)</param>
        /// <param name="fps">Target frames per second (24-30)</param>
        /// <returns>True if generation succeeded</returns>
        public async Task<bool> GenerateVideoAsync(
            string prompt,
            string outputPath,
            string keyframePath = null,
            int duration = 10,
            int fps = 30)
        {
            try
            {
                // Validate inputs
                if (string.IsNullOrEmpty(prompt))
                    throw new ArgumentException("Prompt cannot be empty");
                    
                if (duration < 5 || duration > 25)
                    throw new ArgumentException("Duration must be between 5 and 25 seconds");
                
                // Build Python command
                string pythonScript = BuildPythonScript(
                    prompt, outputPath, keyframePath, duration, fps);
                
                // Execute Python script
                bool success = await ExecutePythonScriptAsync(pythonScript);
                
                // Verify output
                if (success && File.Exists(outputPath))
                {
                    Console.WriteLine($"✅ Video generated: {outputPath}");
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
        public async Task<bool> GenerateSceneClipAsync(
            string sceneDescription,
            string motionHint,
            string outputPath,
            string startKeyframe = null,
            string endKeyframe = null,
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
                30
            );
        }
        
        /// <summary>
        /// Build enhanced prompt with motion guidance
        /// </summary>
        private string BuildScenePrompt(string description, string motionHint)
        {
            string prompt = description;
            
            // Add motion guidance
            if (!string.IsNullOrEmpty(motionHint))
            {
                prompt += $", {motionHint}";
            }
            
            // Add quality enhancers
            prompt += ", smooth motion, cinematic, high quality, 4k";
            
            return prompt;
        }
        
        /// <summary>
        /// Build Python script for LTX-Video execution
        /// </summary>
        private string BuildPythonScript(
            string prompt,
            string outputPath,
            string keyframePath,
            int duration,
            int fps)
        {
            string script = $@"
import torch
from diffusers import LTXPipeline

# Load pipeline
pipe = LTXPipeline.from_pretrained(
    '{_modelId}',
    torch_dtype=torch.float16,
    use_safetensors=True
)
pipe.to('cuda')

# Prepare parameters
prompt = '''{prompt}'''
num_frames = {duration * fps}
height = {_defaultHeight}
width = {_defaultWidth}

# Load keyframe if provided
image = None
if '{keyframePath}' and '{keyframePath}' != 'null':
    from PIL import Image
    image = Image.open('{keyframePath}').convert('RGB')
    image = image.resize((width, height))

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

# Export video
from diffusers.utils import export_to_video
export_to_video(video[0], '{outputPath}', fps={fps})
";
            
            return script;
        }
        
        /// <summary>
        /// Execute Python script asynchronously
        /// </summary>
        private async Task<bool> ExecutePythonScriptAsync(string script)
        {
            // Save script to temp file
            string tempScript = Path.Combine(Path.GetTempPath(), $"ltx_video_{Guid.NewGuid()}.py");
            await File.WriteAllTextAsync(tempScript, script);
            
            try
            {
                var processInfo = new ProcessStartInfo
                {
                    FileName = _pythonPath,
                    Arguments = tempScript,
                    RedirectStandardOutput = true,
                    RedirectStandardError = true,
                    UseShellExecute = false,
                    CreateNoWindow = true
                };
                
                using var process = Process.Start(processInfo);
                if (process == null)
                    return false;
                
                // Read output asynchronously
                var outputTask = process.StandardOutput.ReadToEndAsync();
                var errorTask = process.StandardError.ReadToEndAsync();
                
                await process.WaitForExitAsync();
                
                string output = await outputTask;
                string error = await errorTask;
                
                if (!string.IsNullOrEmpty(output))
                    Console.WriteLine(output);
                    
                if (!string.IsNullOrEmpty(error))
                    Console.WriteLine($"Python stderr: {error}");
                
                return process.ExitCode == 0;
            }
            finally
            {
                // Cleanup temp script
                if (File.Exists(tempScript))
                    File.Delete(tempScript);
            }
        }
    }
}
```

### Performance Characteristics

| Metric | Value |
|--------|-------|
| Generation Speed | 20-30s per 10s clip |
| VRAM Usage | ~12GB |
| Quality | High (8/10) |
| Motion Control | Medium |
| Temporal Consistency | High |
| Best For | Short vertical videos |

### Advantages
1. ✅ Fast generation suitable for batch processing
2. ✅ Native vertical video support (perfect for TikTok/Shorts)
3. ✅ Lower VRAM requirements
4. ✅ Good temporal consistency
5. ✅ Simple API integration

### Limitations
1. ⚠️ Limited fine-grained motion control
2. ⚠️ Maximum duration ~25 seconds
3. ⚠️ Less customization vs. SVD

### Best Use Cases
- TikTok/YouTube Shorts (10-20 seconds)
- Fast batch video generation
- Stories with simple camera movements
- Content with natural motion patterns

---

## Approach B: SDXL + Frame Interpolation

### Overview
Generate high-quality keyframes with Stable Diffusion XL, then use frame interpolation to create smooth video sequences.

### Pipeline Components

#### 1. Keyframe Generation (SDXL)
- Generate 2-5 keyframes per scene
- High-resolution (1024x1792 for vertical)
- Character and style consistency

#### 2. Frame Interpolation Options

##### RIFE (Real-Time Intermediate Flow Estimation)
- **Speed**: Very fast (~0.1s per frame)
- **Quality**: Good
- **Best for**: Real-time applications

##### DAIN (Depth-Aware Video Frame Interpolation)
- **Speed**: Medium (~1s per frame)
- **Quality**: Excellent
- **Best for**: High-quality outputs

##### FILM (Frame Interpolation for Large Motion)
- **Speed**: Fast (~0.3s per frame)
- **Quality**: Very good
- **Best for**: Large motion scenarios

#### 3. Assembly (FFmpeg)
- Concatenate interpolated sequences
- Add audio synchronization
- Apply transitions
- Export final video

### C# Integration Pattern

```csharp
using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Threading.Tasks;

namespace StoryGenerator.VideoSynthesis
{
    /// <summary>
    /// Configuration for keyframe-based video synthesis
    /// </summary>
    public class KeyframeVideoConfig
    {
        public int TargetFps { get; set; } = 30;
        public InterpolationMethod Method { get; set; } = InterpolationMethod.RIFE;
        public int Width { get; set; } = 1080;
        public int Height { get; set; } = 1920;
        public int KeyframesPerScene { get; set; } = 3;
    }
    
    public enum InterpolationMethod
    {
        RIFE,      // Fast, good quality
        DAIN,      // Slower, best quality
        FILM       // Balanced
    }
    
    /// <summary>
    /// SDXL + Frame Interpolation video synthesis
    /// </summary>
    public class KeyframeVideoSynthesizer
    {
        private readonly KeyframeVideoConfig _config;
        private readonly string _pythonPath;
        
        public KeyframeVideoSynthesizer(
            KeyframeVideoConfig config = null,
            string pythonPath = "python")
        {
            _config = config ?? new KeyframeVideoConfig();
            _pythonPath = pythonPath;
        }
        
        /// <summary>
        /// Generate video from scene with keyframes
        /// </summary>
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
                
                // Step 2: Calculate frame distribution
                var frameDistribution = CalculateFrameDistribution(
                    keyframePaths.Count, totalDuration);
                
                // Step 3: Interpolate between keyframes
                var interpolatedFrames = await InterpolateFramesAsync(
                    keyframePaths, frameDistribution);
                
                if (interpolatedFrames == null || !interpolatedFrames.Any())
                {
                    Console.WriteLine("❌ Frame interpolation failed");
                    return false;
                }
                
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
        public async Task<bool> GenerateSceneAsync(
            string sceneDescription,
            string outputPath,
            double duration,
            string audioPath = null,
            List<string> stylePrompts = null)
        {
            try
            {
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
            string tempDir = Path.Combine(Path.GetTempPath(), $"keyframes_{Guid.NewGuid()}");
            Directory.CreateDirectory(tempDir);
            
            try
            {
                // Generate keyframes at different scene positions
                for (int i = 0; i < _config.KeyframesPerScene; i++)
                {
                    double position = i / (double)(_config.KeyframesPerScene - 1);
                    string prompt = BuildKeyframePrompt(
                        sceneDescription, position, stylePrompts);
                    
                    string keyframePath = Path.Combine(
                        tempDir, $"keyframe_{i:D3}.png");
                    
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
            
            // Add position-based variations
            if (position == 0.0)
                prompt += ", opening shot, establishing";
            else if (position == 1.0)
                prompt += ", closing shot, conclusion";
            else
                prompt += ", mid action";
            
            // Add style elements
            if (stylePrompts != null && stylePrompts.Any())
            {
                prompt += ", " + string.Join(", ", stylePrompts);
            }
            
            // Add quality enhancers
            prompt += ", cinematic lighting, high detail, 4k quality";
            
            return prompt;
        }
        
        /// <summary>
        /// Generate single keyframe using SDXL
        /// </summary>
        private async Task<bool> GenerateKeyframeWithSDXLAsync(
            string prompt,
            string outputPath)
        {
            string pythonScript = $@"
import torch
from diffusers import StableDiffusionXLPipeline

# Load SDXL pipeline
pipe = StableDiffusionXLPipeline.from_pretrained(
    'stabilityai/stable-diffusion-xl-base-1.0',
    torch_dtype=torch.float16,
    use_safetensors=True,
    variant='fp16'
)
pipe.to('cuda')

# Generate image
image = pipe(
    prompt='''{prompt}''',
    height={_config.Height},
    width={_config.Width},
    num_inference_steps=40,
    guidance_scale=7.5
).images[0]

# Save image
image.save('{outputPath}')
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
                Path.GetTempPath(), $"interpolated_{Guid.NewGuid()}");
            Directory.CreateDirectory(outputDir);
            
            try
            {
                // Process each keyframe pair
                for (int i = 0; i < keyframePaths.Count - 1; i++)
                {
                    string frame1 = keyframePaths[i];
                    string frame2 = keyframePaths[i + 1];
                    int targetFrames = frameDistribution[i];
                    
                    Console.WriteLine(
                        $"  Interpolating {targetFrames} frames between " +
                        $"keyframe {i} and {i + 1}");
                    
                    var interpolated = await InterpolatePairAsync(
                        frame1, frame2, targetFrames, outputDir);
                    
                    if (interpolated != null)
                        allFrames.AddRange(interpolated);
                }
                
                // Add final keyframe
                allFrames.Add(keyframePaths.Last());
                
                return allFrames;
            }
            catch (Exception ex)
            {
                Console.WriteLine($"❌ Interpolation error: {ex.Message}");
                return null;
            }
        }
        
        /// <summary>
        /// Interpolate frames between two keyframes
        /// </summary>
        private async Task<List<string>> InterpolatePairAsync(
            string frame1Path,
            string frame2Path,
            int targetFrames,
            string outputDir)
        {
            string method = _config.Method.ToString().ToLower();
            
            string pythonScript = $@"
import sys
import os

# Interpolation implementation based on method
method = '{method}'

if method == 'rife':
    # RIFE implementation
    from rife import RIFE
    model = RIFE()
    frames = model.interpolate(
        '{frame1Path}',
        '{frame2Path}',
        num_frames={targetFrames}
    )
    
elif method == 'film':
    # FILM implementation
    from film import FILM
    model = FILM()
    frames = model.interpolate(
        '{frame1Path}',
        '{frame2Path}',
        num_frames={targetFrames}
    )
    
elif method == 'dain':
    # DAIN implementation (slower but highest quality)
    from dain import DAIN
    model = DAIN()
    frames = model.interpolate(
        '{frame1Path}',
        '{frame2Path}',
        num_frames={targetFrames}
    )

# Save interpolated frames
for i, frame in enumerate(frames):
    output_path = os.path.join('{outputDir}', f'frame_{{i:06d}}.png')
    frame.save(output_path)
    print(output_path)
";
            
            // Execute and capture output paths
            // (Implementation details omitted for brevity)
            
            return await Task.FromResult(new List<string>());
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
                // Create temporary file list for FFmpeg
                string fileList = Path.Combine(
                    Path.GetTempPath(), $"frames_{Guid.NewGuid()}.txt");
                
                await File.WriteAllLinesAsync(fileList,
                    framePaths.Select(p => $"file '{p}'"));
                
                // Build FFmpeg command
                string ffmpegArgs = $"-f concat -safe 0 -i \"{fileList}\" " +
                    $"-vf \"fps={_config.TargetFps},scale={_config.Width}:{_config.Height}\" " +
                    $"-c:v libx264 -preset medium -crf 23 -pix_fmt yuv420p ";
                
                // Add audio if provided
                if (!string.IsNullOrEmpty(audioPath) && File.Exists(audioPath))
                {
                    ffmpegArgs += $"-i \"{audioPath}\" -c:a aac -b:a 192k " +
                        $"-shortest ";
                }
                
                ffmpegArgs += $"\"{outputPath}\"";
                
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
                await process.WaitForExitAsync();
                
                // Cleanup
                if (File.Exists(fileList))
                    File.Delete(fileList);
                
                return process.ExitCode == 0 && File.Exists(outputPath);
            }
            catch (Exception ex)
            {
                Console.WriteLine($"❌ FFmpeg assembly error: {ex.Message}");
                return false;
            }
        }
        
        /// <summary>
        /// Calculate frame distribution across keyframes
        /// </summary>
        private Dictionary<int, int> CalculateFrameDistribution(
            int numKeyframes,
            double totalDuration)
        {
            int totalFrames = (int)(totalDuration * _config.TargetFps);
            int segments = numKeyframes - 1;
            int framesPerSegment = totalFrames / segments;
            
            var distribution = new Dictionary<int, int>();
            for (int i = 0; i < segments; i++)
            {
                distribution[i] = framesPerSegment;
            }
            
            return distribution;
        }
        
        /// <summary>
        /// Validate that all keyframes exist and are valid
        /// </summary>
        private bool ValidateKeyframes(List<string> keyframePaths)
        {
            if (keyframePaths == null || !keyframePaths.Any())
            {
                Console.WriteLine("❌ No keyframes provided");
                return false;
            }
            
            foreach (var path in keyframePaths)
            {
                if (!File.Exists(path))
                {
                    Console.WriteLine($"❌ Keyframe not found: {path}");
                    return false;
                }
            }
            
            return true;
        }
        
        /// <summary>
        /// Execute Python script helper
        /// </summary>
        private async Task<bool> ExecutePythonScriptAsync(string script)
        {
            // Implementation similar to LTX-Video version
            // (Details omitted for brevity)
            return await Task.FromResult(true);
        }
    }
}
```

### Performance Characteristics

| Component | Speed | Quality | VRAM |
|-----------|-------|---------|------|
| SDXL Keyframes | ~5s/frame | Excellent | 8-10GB |
| RIFE Interpolation | 0.1s/frame | Good | 2-4GB |
| FILM Interpolation | 0.3s/frame | Very Good | 4-6GB |
| DAIN Interpolation | 1s/frame | Excellent | 6-8GB |
| FFmpeg Assembly | <5s | N/A | Minimal |

### Advantages
1. ✅ Highest quality keyframes (SDXL)
2. ✅ Fine-grained control over composition
3. ✅ Flexible interpolation methods
4. ✅ Character consistency across frames
5. ✅ Works for any video length

### Limitations
1. ⚠️ Slower overall pipeline
2. ⚠️ More complex implementation
3. ⚠️ May have "static" feel compared to LTX-Video
4. ⚠️ Requires more storage for intermediate frames

### Best Use Cases
- High-quality cinematic content
- Character-driven stories requiring consistency
- Longer videos (>25 seconds)
- Content requiring precise composition control

---

## Approach C: Stable Video Diffusion (Backup)

### Overview
Stable Video Diffusion (SVD) provides a middle ground between LTX-Video and keyframe interpolation.

### C# Integration Pattern

```csharp
using System;
using System.Threading.Tasks;

namespace StoryGenerator.VideoSynthesis
{
    /// <summary>
    /// Stable Video Diffusion integration
    /// </summary>
    public class SVDVideoSynthesizer
    {
        private readonly string _modelId = "stabilityai/stable-video-diffusion-img2vid-xt";
        private readonly string _pythonPath;
        
        public SVDVideoSynthesizer(string pythonPath = "python")
        {
            _pythonPath = pythonPath;
        }
        
        /// <summary>
        /// Generate video from single image with motion control
        /// </summary>
        public async Task<bool> GenerateFromImageAsync(
            string imagePath,
            string outputPath,
            string motionPrompt = null,
            int numFrames = 75,
            int fps = 25)
        {
            string pythonScript = $@"
import torch
from diffusers import StableVideoDiffusionPipeline
from PIL import Image

# Load pipeline
pipe = StableVideoDiffusionPipeline.from_pretrained(
    '{_modelId}',
    torch_dtype=torch.float16,
    variant='fp16'
)
pipe.to('cuda')

# Load input image
image = Image.open('{imagePath}').convert('RGB')
image = image.resize((1024, 576))  # SVD preferred resolution

# Generate video
frames = pipe(
    image=image,
    num_frames={numFrames},
    decode_chunk_size=8,  # Memory optimization
    motion_bucket_id=127,  # Medium motion
    fps={fps}
).frames[0]

# Export video
from diffusers.utils import export_to_video
export_to_video(frames, '{outputPath}', fps={fps})
";
            
            return await ExecutePythonScriptAsync(pythonScript);
        }
        
        private async Task<bool> ExecutePythonScriptAsync(string script)
        {
            // Implementation similar to previous examples
            return await Task.FromResult(true);
        }
    }
}
```

### Performance Characteristics

| Metric | Value |
|--------|-------|
| Generation Speed | 45-60s per clip |
| VRAM Usage | ~14-16GB |
| Quality | Very High (9/10) |
| Motion Control | High |
| Best For | Medium-length videos |

---

## Comparison Framework

### C# Evaluation Utility

```csharp
using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.IO;
using System.Linq;
using System.Threading.Tasks;

namespace StoryGenerator.VideoSynthesis
{
    /// <summary>
    /// Video quality metrics
    /// </summary>
    public class VideoMetrics
    {
        public double GenerationTime { get; set; }
        public double FileSize { get; set; }
        public double Duration { get; set; }
        public int FrameCount { get; set; }
        public double Fps { get; set; }
        public string Resolution { get; set; }
        public double VisualQuality { get; set; }
        public double TemporalConsistency { get; set; }
        public double MotionSmoothness { get; set; }
    }
    
    /// <summary>
    /// Compare different video synthesis approaches
    /// </summary>
    public class VideoSynthesisComparator
    {
        private readonly LTXVideoSynthesizer _ltxSynthesizer;
        private readonly KeyframeVideoSynthesizer _keyframeSynthesizer;
        private readonly SVDVideoSynthesizer _svdSynthesizer;
        
        public VideoSynthesisComparator()
        {
            _ltxSynthesizer = new LTXVideoSynthesizer();
            _keyframeSynthesizer = new KeyframeVideoSynthesizer();
            _svdSynthesizer = new SVDVideoSynthesizer();
        }
        
        /// <summary>
        /// Compare all approaches on a test scene
        /// </summary>
        public async Task<Dictionary<string, VideoMetrics>> CompareApproachesAsync(
            string testPrompt,
            string testKeyframe = null,
            double duration = 10.0)
        {
            var results = new Dictionary<string, VideoMetrics>();
            
            Console.WriteLine("🔬 Starting Video Synthesis Comparison");
            Console.WriteLine($"Test Prompt: {testPrompt}");
            Console.WriteLine($"Duration: {duration}s\n");
            
            // Test LTX-Video
            Console.WriteLine("Testing LTX-Video...");
            var ltxMetrics = await TestApproachAsync(
                "LTX-Video",
                async (output) => await _ltxSynthesizer.GenerateVideoAsync(
                    testPrompt, output, testKeyframe, (int)duration));
            if (ltxMetrics != null)
                results["LTX-Video"] = ltxMetrics;
            
            // Test SDXL + Interpolation
            Console.WriteLine("\nTesting SDXL + Frame Interpolation...");
            var keyframeMetrics = await TestApproachAsync(
                "SDXL+Interpolation",
                async (output) => await _keyframeSynthesizer.GenerateSceneAsync(
                    testPrompt, output, duration));
            if (keyframeMetrics != null)
                results["SDXL+Interpolation"] = keyframeMetrics;
            
            // Test Stable Video Diffusion
            if (!string.IsNullOrEmpty(testKeyframe))
            {
                Console.WriteLine("\nTesting Stable Video Diffusion...");
                var svdMetrics = await TestApproachAsync(
                    "SVD",
                    async (output) => await _svdSynthesizer.GenerateFromImageAsync(
                        testKeyframe, output, testPrompt));
                if (svdMetrics != null)
                    results["SVD"] = svdMetrics;
            }
            
            // Print comparison
            PrintComparison(results);
            
            return results;
        }
        
        /// <summary>
        /// Test a single approach and measure metrics
        /// </summary>
        private async Task<VideoMetrics> TestApproachAsync(
            string approachName,
            Func<string, Task<bool>> generateFunc)
        {
            string outputPath = Path.Combine(
                Path.GetTempPath(),
                $"test_{approachName}_{Guid.NewGuid()}.mp4");
            
            try
            {
                var stopwatch = Stopwatch.StartNew();
                
                bool success = await generateFunc(outputPath);
                
                stopwatch.Stop();
                
                if (!success || !File.Exists(outputPath))
                {
                    Console.WriteLine($"❌ {approachName} generation failed");
                    return null;
                }
                
                var metrics = await AnalyzeVideoAsync(outputPath);
                metrics.GenerationTime = stopwatch.Elapsed.TotalSeconds;
                
                Console.WriteLine($"✅ {approachName} completed in {metrics.GenerationTime:F2}s");
                
                return metrics;
            }
            catch (Exception ex)
            {
                Console.WriteLine($"❌ {approachName} error: {ex.Message}");
                return null;
            }
            finally
            {
                // Cleanup
                if (File.Exists(outputPath))
                    File.Delete(outputPath);
            }
        }
        
        /// <summary>
        /// Analyze video file and extract metrics
        /// </summary>
        private async Task<VideoMetrics> AnalyzeVideoAsync(string videoPath)
        {
            var metrics = new VideoMetrics();
            
            // Get file size
            var fileInfo = new FileInfo(videoPath);
            metrics.FileSize = fileInfo.Length / (1024.0 * 1024.0); // MB
            
            // Use FFprobe to get video properties
            var ffprobeArgs = $"-v quiet -print_format json -show_streams \"{videoPath}\"";
            
            var processInfo = new ProcessStartInfo
            {
                FileName = "ffprobe",
                Arguments = ffprobeArgs,
                RedirectStandardOutput = true,
                UseShellExecute = false,
                CreateNoWindow = true
            };
            
            using var process = Process.Start(processInfo);
            string output = await process.StandardOutput.ReadToEndAsync();
            await process.WaitForExitAsync();
            
            // Parse FFprobe output
            // (Simplified - would use JSON parsing in real implementation)
            metrics.Duration = 10.0;  // Placeholder
            metrics.Fps = 30.0;       // Placeholder
            metrics.FrameCount = 300; // Placeholder
            metrics.Resolution = "1080x1920"; // Placeholder
            
            // Quality metrics (would use actual analysis tools)
            metrics.VisualQuality = 8.0;
            metrics.TemporalConsistency = 8.5;
            metrics.MotionSmoothness = 8.0;
            
            return metrics;
        }
        
        /// <summary>
        /// Print comparison table
        /// </summary>
        private void PrintComparison(Dictionary<string, VideoMetrics> results)
        {
            Console.WriteLine("\n" + new string('=', 80));
            Console.WriteLine("COMPARISON RESULTS");
            Console.WriteLine(new string('=', 80));
            
            Console.WriteLine($"\n{"Metric",-25} {"LTX-Video",-15} {"SDXL+Interp",-15} {"SVD",-15}");
            Console.WriteLine(new string('-', 80));
            
            // Generation Time
            Console.WriteLine($"{"Generation Time (s)",-25} " +
                GetMetricValue(results, "LTX-Video", m => m.GenerationTime) +
                GetMetricValue(results, "SDXL+Interpolation", m => m.GenerationTime) +
                GetMetricValue(results, "SVD", m => m.GenerationTime));
            
            // File Size
            Console.WriteLine($"{"File Size (MB)",-25} " +
                GetMetricValue(results, "LTX-Video", m => m.FileSize) +
                GetMetricValue(results, "SDXL+Interpolation", m => m.FileSize) +
                GetMetricValue(results, "SVD", m => m.FileSize));
            
            // Visual Quality
            Console.WriteLine($"{"Visual Quality (0-10)",-25} " +
                GetMetricValue(results, "LTX-Video", m => m.VisualQuality) +
                GetMetricValue(results, "SDXL+Interpolation", m => m.VisualQuality) +
                GetMetricValue(results, "SVD", m => m.VisualQuality));
            
            // Temporal Consistency
            Console.WriteLine($"{"Temporal Consistency",-25} " +
                GetMetricValue(results, "LTX-Video", m => m.TemporalConsistency) +
                GetMetricValue(results, "SDXL+Interpolation", m => m.TemporalConsistency) +
                GetMetricValue(results, "SVD", m => m.TemporalConsistency));
            
            // Motion Smoothness
            Console.WriteLine($"{"Motion Smoothness",-25} " +
                GetMetricValue(results, "LTX-Video", m => m.MotionSmoothness) +
                GetMetricValue(results, "SDXL+Interpolation", m => m.MotionSmoothness) +
                GetMetricValue(results, "SVD", m => m.MotionSmoothness));
            
            Console.WriteLine(new string('=', 80));
            
            // Recommendation
            Console.WriteLine("\n💡 RECOMMENDATION:");
            var winner = DetermineWinner(results);
            Console.WriteLine($"   Best overall: {winner}");
        }
        
        private string GetMetricValue(
            Dictionary<string, VideoMetrics> results,
            string approach,
            Func<VideoMetrics, double> selector)
        {
            if (results.ContainsKey(approach))
            {
                return $"{selector(results[approach]),-15:F2}";
            }
            return $"{"N/A",-15}";
        }
        
        private string DetermineWinner(Dictionary<string, VideoMetrics> results)
        {
            // Simple scoring algorithm
            var scores = new Dictionary<string, double>();
            
            foreach (var kvp in results)
            {
                double score = 0;
                var m = kvp.Value;
                
                // Faster is better (inverse)
                score += (100.0 / m.GenerationTime) * 0.3;
                
                // Higher quality is better
                score += m.VisualQuality * 0.25;
                score += m.TemporalConsistency * 0.25;
                score += m.MotionSmoothness * 0.2;
                
                scores[kvp.Key] = score;
            }
            
            return scores.OrderByDescending(kvp => kvp.Value).First().Key;
        }
    }
}
```

---

## Decision Matrix

### Selection Criteria

| Scenario | Recommended Approach | Reason |
|----------|---------------------|---------|
| TikTok/Shorts (10-20s) | **LTX-Video** | Fast, native vertical support |
| High-quality cinematic | **SDXL + Interpolation** | Best keyframe quality |
| Character-driven stories | **SDXL + Interpolation** | Consistency control |
| Fast batch processing | **LTX-Video** | Fastest generation |
| Long videos (>25s) | **SDXL + Interpolation** | No length limit |
| Medium motion control | **Stable Video Diffusion** | Balanced approach |
| Limited VRAM (<12GB) | **LTX-Video** | Lower requirements |

### Implementation Priority

1. **Phase 1**: Implement LTX-Video for quick wins
2. **Phase 2**: Add SDXL + RIFE for quality option
3. **Phase 3**: Integrate SVD as backup/alternative
4. **Phase 4**: Build comparison framework

---

## Installation & Setup

### Python Dependencies

```bash
# LTX-Video
pip install diffusers transformers accelerate torch

# SDXL
pip install diffusers[torch] transformers

# Frame Interpolation
pip install rife-ncnn-vulkan  # RIFE
pip install film-net          # FILM
# Note: DAIN requires separate installation

# Utilities
pip install pillow opencv-python ffmpeg-python
```

### C# Requirements

```xml
<ItemGroup>
  <PackageReference Include="System.Diagnostics.Process" Version="4.3.0" />
  <PackageReference Include="System.Text.Json" Version="8.0.0" />
</ItemGroup>
```

---

## Testing Recommendations

### Test Suite

1. **Quality Tests**
   - Visual inspection of output
   - Temporal consistency check
   - Motion smoothness analysis

2. **Performance Tests**
   - Generation time benchmarks
   - VRAM usage monitoring
   - Batch processing throughput

3. **Integration Tests**
   - Audio synchronization
   - Transition smoothness
   - End-to-end pipeline

### Sample Test Prompts

```csharp
var testPrompts = new List<string>
{
    "A serene lake at sunset, camera slowly panning right",
    "City skyline at night, lights twinkling",
    "Forest path, camera moving forward through trees",
    "Character portrait, slight head movement and smile",
    "Abstract geometric shapes, smooth rotation"
};
```

---

## References

- **LTX-Video**: https://huggingface.co/Lightricks/LTX-Video
- **Stable Video Diffusion**: https://stability.ai/stable-video
- **SDXL**: https://huggingface.co/docs/diffusers/en/using-diffusers/sdxl
- **RIFE**: https://github.com/hzwer/RIFE
- **FILM**: https://github.com/google-research/frame-interpolation

---

## Conclusion

For the StoryGenerator pipeline targeting short-form vertical content:

**Primary Recommendation**: **LTX-Video (Approach A)**
- Fast generation suitable for batch processing
- Native vertical video support
- Lower resource requirements
- Good quality for social media content

**Secondary Option**: **SDXL + RIFE (Approach B)**
- When highest quality is required
- For character-driven content
- When fine-grained control is needed

Both approaches can be implemented in parallel, with LTX-Video as the default and SDXL+Interpolation as a quality-focused alternative selectable via configuration.
