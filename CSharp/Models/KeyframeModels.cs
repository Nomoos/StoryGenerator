using System;
using System.Collections.Generic;

namespace StoryGenerator.Models
{
    /// <summary>
    /// Represents a keyframe prompt for image generation
    /// </summary>
    public class KeyframePrompt
    {
        /// <summary>
        /// Shot identifier
        /// </summary>
        public int ShotNumber { get; set; }

        /// <summary>
        /// Main visual description
        /// </summary>
        public string VisualPrompt { get; set; } = string.Empty;

        /// <summary>
        /// Style elements (cinematic, artistic, etc.)
        /// </summary>
        public string Style { get; set; } = string.Empty;

        /// <summary>
        /// Camera angle and composition
        /// </summary>
        public string Camera { get; set; } = string.Empty;

        /// <summary>
        /// Mood and atmosphere
        /// </summary>
        public string Mood { get; set; } = string.Empty;

        /// <summary>
        /// Age-safe content filtering applied
        /// </summary>
        public bool AgeSafe { get; set; } = true;

        /// <summary>
        /// Negative prompt to avoid unwanted elements
        /// </summary>
        public string NegativePrompt { get; set; } = string.Empty;

        /// <summary>
        /// Complete combined prompt for generation
        /// </summary>
        public string CombinedPrompt
        {
            get
            {
                var parts = new List<string>();
                
                if (!string.IsNullOrWhiteSpace(VisualPrompt))
                    parts.Add(VisualPrompt);
                
                if (!string.IsNullOrWhiteSpace(Camera))
                    parts.Add(Camera);
                
                if (!string.IsNullOrWhiteSpace(Mood))
                    parts.Add(Mood);
                
                if (!string.IsNullOrWhiteSpace(Style))
                    parts.Add(Style);

                return string.Join(", ", parts);
            }
        }
    }

    /// <summary>
    /// Represents a generated keyframe with metadata
    /// </summary>
    public class GeneratedKeyframe
    {
        /// <summary>
        /// Shot number this keyframe belongs to
        /// </summary>
        public int ShotNumber { get; set; }

        /// <summary>
        /// Keyframe variant identifier (A1, A2, B1, etc.)
        /// </summary>
        public string VariantId { get; set; } = string.Empty;

        /// <summary>
        /// File path to the generated image
        /// </summary>
        public string FilePath { get; set; } = string.Empty;

        /// <summary>
        /// Prompt used for generation
        /// </summary>
        public KeyframePrompt Prompt { get; set; } = new();

        /// <summary>
        /// Generation method (base, base+refiner, lora, controlnet)
        /// </summary>
        public string GenerationMethod { get; set; } = string.Empty;

        /// <summary>
        /// Image width
        /// </summary>
        public int Width { get; set; }

        /// <summary>
        /// Image height
        /// </summary>
        public int Height { get; set; }

        /// <summary>
        /// Random seed used
        /// </summary>
        public int? Seed { get; set; }

        /// <summary>
        /// Generation time in milliseconds
        /// </summary>
        public long GenerationTimeMs { get; set; }

        /// <summary>
        /// Quality score (if evaluated)
        /// </summary>
        public double? QualityScore { get; set; }

        /// <summary>
        /// Whether this keyframe was selected as top N
        /// </summary>
        public bool IsSelected { get; set; }

        /// <summary>
        /// Timestamp when generated
        /// </summary>
        public DateTime GeneratedAt { get; set; } = DateTime.UtcNow;
    }

    /// <summary>
    /// Manifest for all keyframes generated for a story/segment
    /// </summary>
    public class KeyframeManifest
    {
        /// <summary>
        /// Story/title identifier
        /// </summary>
        public string TitleId { get; set; } = string.Empty;

        /// <summary>
        /// Segment identifier (e.g., "shorts", "long-form")
        /// </summary>
        public string Segment { get; set; } = string.Empty;

        /// <summary>
        /// Age rating (e.g., "all-ages", "13+", "18+")
        /// </summary>
        public string Age { get; set; } = string.Empty;

        /// <summary>
        /// Version identifier (v1 for base+refiner, v2 for LoRA/ControlNet)
        /// </summary>
        public string Version { get; set; } = "v1";

        /// <summary>
        /// All prompts used for generation
        /// </summary>
        public List<KeyframePrompt> Prompts { get; set; } = new();

        /// <summary>
        /// All generated keyframes
        /// </summary>
        public List<GeneratedKeyframe> Keyframes { get; set; } = new();

        /// <summary>
        /// Selected top N keyframes per shot
        /// </summary>
        public Dictionary<int, List<string>> SelectedKeyframes { get; set; } = new();

        /// <summary>
        /// Number of variants generated per shot
        /// </summary>
        public int VariantsPerShot { get; set; } = 4;

        /// <summary>
        /// Number of top keyframes selected per shot
        /// </summary>
        public int TopNPerShot { get; set; } = 2;

        /// <summary>
        /// Generation configuration used
        /// </summary>
        public Dictionary<string, object> GenerationConfig { get; set; } = new();

        /// <summary>
        /// Timestamp when manifest was created
        /// </summary>
        public DateTime CreatedAt { get; set; } = DateTime.UtcNow;

        /// <summary>
        /// Total generation time in seconds
        /// </summary>
        public double TotalGenerationTimeSeconds { get; set; }
    }

    /// <summary>
    /// Configuration for keyframe generation
    /// </summary>
    public class KeyframeGenerationConfig
    {
        /// <summary>
        /// Number of variants to generate per shot
        /// </summary>
        public int VariantsPerShot { get; set; } = 4;

        /// <summary>
        /// Number of top keyframes to select per shot
        /// </summary>
        public int TopNPerShot { get; set; } = 2;

        /// <summary>
        /// Image width
        /// </summary>
        public int Width { get; set; } = 1024;

        /// <summary>
        /// Image height
        /// </summary>
        public int Height { get; set; } = 1024;

        /// <summary>
        /// Number of inference steps for base model
        /// </summary>
        public int BaseSteps { get; set; } = 40;

        /// <summary>
        /// Number of inference steps for refiner
        /// </summary>
        public int RefinerSteps { get; set; } = 20;

        /// <summary>
        /// Guidance scale
        /// </summary>
        public double GuidanceScale { get; set; } = 7.5;

        /// <summary>
        /// Whether to use refiner
        /// </summary>
        public bool UseRefiner { get; set; } = true;

        /// <summary>
        /// LoRA path (optional, for v2)
        /// </summary>
        public string? LoraPath { get; set; }

        /// <summary>
        /// LoRA scale (0.0-1.0)
        /// </summary>
        public double LoraScale { get; set; } = 0.75;

        /// <summary>
        /// Whether to use ControlNet (optional, for v2)
        /// </summary>
        public bool UseControlNet { get; set; } = false;

        /// <summary>
        /// Age-safe content filtering
        /// </summary>
        public bool AgeSafeContent { get; set; } = true;

        /// <summary>
        /// Output base directory
        /// </summary>
        public string OutputBaseDir { get; set; } = "images";
    }
}
