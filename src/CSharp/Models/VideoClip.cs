using System;
using System.Collections.Generic;

namespace StoryGenerator.Models
{
    /// <summary>
    /// Represents a generated video clip with metadata
    /// </summary>
    public class VideoClip
    {
        /// <summary>
        /// Unique identifier for the clip
        /// </summary>
        public string ClipId { get; set; }
        
        /// <summary>
        /// Scene identifier this clip belongs to
        /// </summary>
        public int SceneId { get; set; }
        
        /// <summary>
        /// Path to the generated video file
        /// </summary>
        public string VideoPath { get; set; }
        
        /// <summary>
        /// Start time in the final composition (seconds)
        /// </summary>
        public double StartTime { get; set; }
        
        /// <summary>
        /// End time in the final composition (seconds)
        /// </summary>
        public double EndTime { get; set; }
        
        /// <summary>
        /// Clip duration in seconds
        /// </summary>
        public double Duration => EndTime - StartTime;
        
        /// <summary>
        /// Video frames per second
        /// </summary>
        public int Fps { get; set; }
        
        /// <summary>
        /// Video resolution (width, height)
        /// </summary>
        public (int Width, int Height) Resolution { get; set; }
        
        /// <summary>
        /// Paths to keyframes used in generation
        /// </summary>
        public List<string> KeyframesUsed { get; set; }
        
        /// <summary>
        /// Motion/camera movement prompt used
        /// </summary>
        public string MotionPrompt { get; set; }
        
        /// <summary>
        /// Scene description/prompt
        /// </summary>
        public string SceneDescription { get; set; }
        
        /// <summary>
        /// Time taken to generate the clip (seconds)
        /// </summary>
        public double GenerationTime { get; set; }
        
        /// <summary>
        /// Synthesis method used (LTX-Video, SDXL+RIFE, etc.)
        /// </summary>
        public string SynthesisMethod { get; set; }
        
        /// <summary>
        /// Timestamp when clip was created
        /// </summary>
        public DateTime CreatedAt { get; set; }
        
        /// <summary>
        /// File size in bytes
        /// </summary>
        public long FileSizeBytes { get; set; }
        
        /// <summary>
        /// Quality metrics (if evaluated)
        /// </summary>
        public VideoQualityMetrics QualityMetrics { get; set; }
        
        /// <summary>
        /// Additional metadata
        /// </summary>
        public Dictionary<string, object> Metadata { get; set; }
        
        public VideoClip()
        {
            ClipId = Guid.NewGuid().ToString();
            KeyframesUsed = new List<string>();
            CreatedAt = DateTime.UtcNow;
            Metadata = new Dictionary<string, object>();
        }
        
        /// <summary>
        /// Format resolution as string (e.g., "1080x1920")
        /// </summary>
        public string ResolutionString => $"{Resolution.Width}x{Resolution.Height}";
        
        /// <summary>
        /// Get file size in megabytes
        /// </summary>
        public double FileSizeMB => FileSizeBytes / (1024.0 * 1024.0);
    }
    
    /// <summary>
    /// Quality metrics for video evaluation
    /// </summary>
    public class VideoQualityMetrics
    {
        /// <summary>
        /// Visual quality score (0-10)
        /// </summary>
        public double VisualQuality { get; set; }
        
        /// <summary>
        /// Temporal consistency score (0-10)
        /// </summary>
        public double TemporalConsistency { get; set; }
        
        /// <summary>
        /// Motion smoothness score (0-10)
        /// </summary>
        public double MotionSmoothness { get; set; }
        
        /// <summary>
        /// Audio-video sync quality (0-10)
        /// </summary>
        public double AudioVideoSync { get; set; }
        
        /// <summary>
        /// Overall quality score (average of other metrics)
        /// </summary>
        public double OverallScore =>
            (VisualQuality + TemporalConsistency + MotionSmoothness + AudioVideoSync) / 4.0;
        
        /// <summary>
        /// Additional notes about quality
        /// </summary>
        public string Notes { get; set; }
    }
    
    /// <summary>
    /// Represents a complete scene composed of multiple clips
    /// </summary>
    public class SceneComposition
    {
        /// <summary>
        /// Scene identifier
        /// </summary>
        public int SceneId { get; set; }
        
        /// <summary>
        /// Scene title or description
        /// </summary>
        public string Title { get; set; }
        
        /// <summary>
        /// All clips in this scene
        /// </summary>
        public List<VideoClip> Clips { get; set; }
        
        /// <summary>
        /// Total scene duration
        /// </summary>
        public double TotalDuration { get; set; }
        
        /// <summary>
        /// Transition effect to next scene
        /// </summary>
        public string TransitionEffect { get; set; }
        
        /// <summary>
        /// Transition duration in seconds
        /// </summary>
        public double TransitionDuration { get; set; }
        
        public SceneComposition()
        {
            Clips = new List<VideoClip>();
            TransitionEffect = "fade";
            TransitionDuration = 0.5;
        }
    }
}
