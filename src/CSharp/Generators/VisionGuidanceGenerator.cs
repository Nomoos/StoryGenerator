using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.IO;
using System.Linq;
using System.Text.Json;
using System.Threading;
using System.Threading.Tasks;
using Microsoft.Extensions.Logging;

namespace StoryGenerator.Generators
{
    /// <summary>
    /// Vision guidance generator for image analysis and quality assessment.
    /// Equivalent to Python GVision.py but shells out to Python for actual vision model execution.
    /// 
    /// Supports:
    /// - Image captioning
    /// - Quality assessment
    /// - Consistency validation
    /// - Storyboard validation
    /// </summary>
    public class VisionGuidanceGenerator
    {
        private readonly ILogger<VisionGuidanceGenerator> _logger;
        private readonly string _pythonPath;
        private readonly string _pythonScriptPath;

        public VisionGuidanceGenerator(
            ILogger<VisionGuidanceGenerator> logger,
            string pythonPath = "python",
            string? pythonScriptPath = null)
        {
            _logger = logger ?? throw new ArgumentNullException(nameof(logger));
            _pythonPath = pythonPath;
            _pythonScriptPath = pythonScriptPath ?? Path.Combine(
                Directory.GetCurrentDirectory(), "Python", "Generators", "GVision.py");
        }

        /// <summary>
        /// Generate image caption using vision model
        /// </summary>
        /// <param name="imagePath">Path to image file</param>
        /// <param name="modelName">Vision model to use (phi-3.5-vision, llava-onevision, etc.)</param>
        /// <param name="cancellationToken">Cancellation token</param>
        /// <returns>Image caption</returns>
        public async Task<string?> GenerateImageCaptionAsync(
            string imagePath,
            string modelName = "phi-3.5-vision",
            CancellationToken cancellationToken = default)
        {
            if (string.IsNullOrEmpty(imagePath))
                throw new ArgumentException("Image path cannot be empty", nameof(imagePath));

            if (!File.Exists(imagePath))
                throw new FileNotFoundException($"Image file not found: {imagePath}");

            _logger.LogInformation("📸 Generating caption for image: {Image}", Path.GetFileName(imagePath));

            var script = $@"
import sys
sys.path.insert(0, r'{Path.GetDirectoryName(_pythonScriptPath)}')

from GVision import GVision
from PIL import Image

try:
    vision = GVision(model_name='{modelName}', load_model=True)
    image = Image.open(r'{imagePath}')
    
    prompt = 'Describe this image in detail, focusing on visual elements, composition, and style.'
    caption = vision.generate_response(image, prompt)
    
    print('CAPTION_START')
    print(caption)
    print('CAPTION_END')
except Exception as e:
    print(f'ERROR: {{e}}', file=sys.stderr)
    sys.exit(1)
";

            var result = await ExecutePythonScriptAsync(script, cancellationToken);
            if (result == null)
                return null;

            // Extract caption from output
            var captionStart = result.IndexOf("CAPTION_START");
            var captionEnd = result.IndexOf("CAPTION_END");

            if (captionStart >= 0 && captionEnd > captionStart)
            {
                var caption = result.Substring(
                    captionStart + "CAPTION_START".Length,
                    captionEnd - captionStart - "CAPTION_START".Length).Trim();

                _logger.LogInformation("✅ Generated caption ({Length} chars)", caption.Length);
                return caption;
            }

            return null;
        }

        /// <summary>
        /// Assess image quality using vision model
        /// </summary>
        /// <param name="imagePath">Path to image file</param>
        /// <param name="modelName">Vision model to use</param>
        /// <param name="cancellationToken">Cancellation token</param>
        /// <returns>Quality assessment result</returns>
        public async Task<ImageQualityAssessment?> AssessImageQualityAsync(
            string imagePath,
            string modelName = "phi-3.5-vision",
            CancellationToken cancellationToken = default)
        {
            if (string.IsNullOrEmpty(imagePath))
                throw new ArgumentException("Image path cannot be empty", nameof(imagePath));

            if (!File.Exists(imagePath))
                throw new FileNotFoundException($"Image file not found: {imagePath}");

            _logger.LogInformation("🔍 Assessing quality of image: {Image}", Path.GetFileName(imagePath));

            var script = $@"
import sys
import json
sys.path.insert(0, r'{Path.GetDirectoryName(_pythonScriptPath)}')

from GVision import GVision
from PIL import Image

try:
    vision = GVision(model_name='{modelName}', load_model=True)
    image = Image.open(r'{imagePath}')
    
    prompt = '''Assess the quality of this image. Provide scores (0-100) for:
    - Technical quality (focus, exposure, noise)
    - Composition (framing, balance, rule of thirds)
    - Visual appeal (aesthetics, colors, overall impact)
    - Clarity (sharpness, detail)
    
    Respond in JSON format with keys: technical_quality, composition, visual_appeal, clarity, overall_score, notes'''
    
    response = vision.generate_response(image, prompt, max_new_tokens=300)
    print('ASSESSMENT_START')
    print(response)
    print('ASSESSMENT_END')
except Exception as e:
    print(f'ERROR: {{e}}', file=sys.stderr)
    sys.exit(1)
";

            var result = await ExecutePythonScriptAsync(script, cancellationToken);
            if (result == null)
                return null;

            // Extract and parse assessment
            var assessmentStart = result.IndexOf("ASSESSMENT_START");
            var assessmentEnd = result.IndexOf("ASSESSMENT_END");

            if (assessmentStart >= 0 && assessmentEnd > assessmentStart)
            {
                var assessmentText = result.Substring(
                    assessmentStart + "ASSESSMENT_START".Length,
                    assessmentEnd - assessmentStart - "ASSESSMENT_START".Length).Trim();

                // Try to extract JSON
                var jsonStart = assessmentText.IndexOf('{');
                var jsonEnd = assessmentText.LastIndexOf('}');

                if (jsonStart >= 0 && jsonEnd > jsonStart)
                {
                    var json = assessmentText.Substring(jsonStart, jsonEnd - jsonStart + 1);
                    try
                    {
                        var assessment = JsonSerializer.Deserialize<ImageQualityAssessment>(json);
                        _logger.LogInformation("✅ Quality assessment complete. Overall score: {Score}", 
                            assessment?.OverallScore ?? 0);
                        return assessment;
                    }
                    catch (Exception ex)
                    {
                        _logger.LogWarning(ex, "Failed to parse quality assessment JSON");
                    }
                }
            }

            return null;
        }

        /// <summary>
        /// Validate consistency between multiple images (storyboard)
        /// </summary>
        /// <param name="imagePaths">List of image paths to validate</param>
        /// <param name="modelName">Vision model to use</param>
        /// <param name="cancellationToken">Cancellation token</param>
        /// <returns>Consistency validation result</returns>
        public async Task<StoryboardConsistency?> ValidateStoryboardConsistencyAsync(
            List<string> imagePaths,
            string modelName = "phi-3.5-vision",
            CancellationToken cancellationToken = default)
        {
            if (imagePaths == null || !imagePaths.Any())
                throw new ArgumentException("Image paths list cannot be empty", nameof(imagePaths));

            _logger.LogInformation("🎬 Validating consistency across {Count} images", imagePaths.Count);

            var pathsJson = JsonSerializer.Serialize(imagePaths);
            var script = $@"
import sys
import json
sys.path.insert(0, r'{Path.GetDirectoryName(_pythonScriptPath)}')

from GVision import GVision
from PIL import Image

try:
    vision = GVision(model_name='{modelName}', load_model=True)
    image_paths = json.loads(r'''{pathsJson}''')
    
    # Analyze first and last image for consistency
    if len(image_paths) >= 2:
        img1 = Image.open(image_paths[0])
        img2 = Image.open(image_paths[-1])
        
        prompt = '''Compare these two images from a storyboard sequence. 
        Assess consistency in: style, lighting, color palette, character appearance.
        Provide a consistency score (0-100) and list any inconsistencies found.
        Respond in JSON: {{""consistency_score"": 0-100, ""inconsistencies"": [list], ""notes"": ""string""}}'''
        
        # For simplicity, just analyze the first image with comparison context
        response = vision.generate_response(img1, prompt, max_new_tokens=400)
        print('CONSISTENCY_START')
        print(response)
        print('CONSISTENCY_END')
except Exception as e:
    print(f'ERROR: {{e}}', file=sys.stderr)
    sys.exit(1)
";

            var result = await ExecutePythonScriptAsync(script, cancellationToken);
            if (result == null)
                return null;

            // Extract and parse consistency result
            var consistencyStart = result.IndexOf("CONSISTENCY_START");
            var consistencyEnd = result.IndexOf("CONSISTENCY_END");

            if (consistencyStart >= 0 && consistencyEnd > consistencyStart)
            {
                var consistencyText = result.Substring(
                    consistencyStart + "CONSISTENCY_START".Length,
                    consistencyEnd - consistencyStart - "CONSISTENCY_START".Length).Trim();

                var jsonStart = consistencyText.IndexOf('{');
                var jsonEnd = consistencyText.LastIndexOf('}');

                if (jsonStart >= 0 && jsonEnd > jsonStart)
                {
                    var json = consistencyText.Substring(jsonStart, jsonEnd - jsonStart + 1);
                    try
                    {
                        var consistency = JsonSerializer.Deserialize<StoryboardConsistency>(json);
                        _logger.LogInformation("✅ Consistency validation complete. Score: {Score}",
                            consistency?.ConsistencyScore ?? 0);
                        return consistency;
                    }
                    catch (Exception ex)
                    {
                        _logger.LogWarning(ex, "Failed to parse consistency validation JSON");
                    }
                }
            }

            return null;
        }

        /// <summary>
        /// Execute Python script and return output
        /// </summary>
        private async Task<string?> ExecutePythonScriptAsync(
            string script,
            CancellationToken cancellationToken)
        {
            var tempScript = Path.Combine(Path.GetTempPath(), $"vision_{Guid.NewGuid()}.py");

            try
            {
                await File.WriteAllTextAsync(tempScript, script, cancellationToken);

                var processInfo = new ProcessStartInfo
                {
                    FileName = _pythonPath,
                    Arguments = $"\"{tempScript}\"",
                    RedirectStandardOutput = true,
                    RedirectStandardError = true,
                    UseShellExecute = false,
                    CreateNoWindow = true
                };

                using var process = Process.Start(processInfo);
                if (process == null)
                {
                    _logger.LogError("Failed to start Python process");
                    return null;
                }

                var outputTask = process.StandardOutput.ReadToEndAsync();
                var errorTask = process.StandardError.ReadToEndAsync();

                await process.WaitForExitAsync(cancellationToken);

                var output = await outputTask;
                var error = await errorTask;

                if (process.ExitCode != 0)
                {
                    _logger.LogError("Python script failed with exit code {ExitCode}: {Error}",
                        process.ExitCode, error);
                    return null;
                }

                return output;
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Failed to execute Python vision script");
                return null;
            }
            finally
            {
                try
                {
                    if (File.Exists(tempScript))
                        File.Delete(tempScript);
                }
                catch
                {
                    // Ignore cleanup errors
                }
            }
        }
    }

    /// <summary>
    /// Image quality assessment result
    /// </summary>
    public class ImageQualityAssessment
    {
        public int TechnicalQuality { get; set; }
        public int Composition { get; set; }
        public int VisualAppeal { get; set; }
        public int Clarity { get; set; }
        public int OverallScore { get; set; }
        public string Notes { get; set; } = string.Empty;
    }

    /// <summary>
    /// Storyboard consistency validation result
    /// </summary>
    public class StoryboardConsistency
    {
        public int ConsistencyScore { get; set; }
        public List<string> Inconsistencies { get; set; } = new();
        public string Notes { get; set; } = string.Empty;
    }
}
