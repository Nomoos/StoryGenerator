using System.Collections.Generic;

namespace StoryGenerator.Models
{
    /// <summary>
    /// Configuration for complete video production from keyframes, subtitles, script/text, and other sources.
    /// </summary>
    public class VideoProductionConfig
    {
        /// <summary>
        /// List of keyframe image file paths (required).
        /// These will be interpolated to create smooth video.
        /// </summary>
        public List<string> KeyframePaths { get; set; }

        /// <summary>
        /// Total duration of the output video in seconds.
        /// </summary>
        public double DurationSeconds { get; set; }

        /// <summary>
        /// Output file path for the final video.
        /// Format: /final/{segment}/{age}/{title_id}_draft.mp4
        /// </summary>
        public string? OutputPath { get; set; }

        /// <summary>
        /// SRT subtitle file path (optional).
        /// If not provided, subtitles can be generated from ScriptText.
        /// </summary>
        public string? SrtPath { get; set; }

        /// <summary>
        /// Script text for subtitle generation (optional).
        /// Used if SrtPath is not provided.
        /// </summary>
        public string? ScriptText { get; set; }

        /// <summary>
        /// Audio file path for voiceover or narration (optional).
        /// This audio will be synced with the video.
        /// </summary>
        public string? AudioPath { get; set; }

        /// <summary>
        /// Background music file path (optional).
        /// Must be licensed music.
        /// </summary>
        public string? BackgroundMusicPath { get; set; }

        /// <summary>
        /// Sound effects file paths (optional).
        /// Must be licensed SFX.
        /// </summary>
        public List<string> SoundEffectsPaths { get; set; }

        /// <summary>
        /// Target frames per second (default: 30).
        /// </summary>
        public int Fps { get; set; } = 30;

        /// <summary>
        /// Target aspect ratio width (default: 1080 for 9:16).
        /// </summary>
        public int TargetWidth { get; set; } = 1080;

        /// <summary>
        /// Target aspect ratio height (default: 1920 for 9:16).
        /// </summary>
        public int TargetHeight { get; set; } = 1920;

        /// <summary>
        /// Burn in subtitles (true) or use soft subtitles (false).
        /// </summary>
        public bool BurnInSubtitles { get; set; } = true;

        /// <summary>
        /// Safe text margins for subtitle positioning.
        /// </summary>
        public SafeTextMargins SafeMargins { get; set; }

        /// <summary>
        /// Background music volume (0.0-1.0, default: 0.2).
        /// </summary>
        public double MusicVolume { get; set; } = 0.2;

        /// <summary>
        /// Enable audio ducking for background music during voiceover (default: true).
        /// </summary>
        public bool EnableDucking { get; set; } = true;

        /// <summary>
        /// Video bitrate for output encoding (default: 8M for high quality).
        /// </summary>
        public string VideoBitrate { get; set; } = "8M";

        /// <summary>
        /// Audio bitrate for output encoding (default: 192k).
        /// </summary>
        public string AudioBitrate { get; set; } = "192k";

        /// <summary>
        /// Story segment identifier (e.g., "intro", "main", "outro").
        /// </summary>
        public string? Segment { get; set; }

        /// <summary>
        /// Target age group (e.g., "10-13", "14-17", "18-23", "24-30").
        /// </summary>
        public string? Age { get; set; }

        /// <summary>
        /// Gender category (e.g., "men", "women").
        /// </summary>
        public string? Gender { get; set; }

        /// <summary>
        /// Unique title identifier.
        /// </summary>
        public string? TitleId { get; set; }

        /// <summary>
        /// Frame interpolation method (RIFE, FILM, DAIN).
        /// </summary>
        public string InterpolationMethod { get; set; } = "RIFE";

        /// <summary>
        /// Generate SRT file from script text if no SRT is provided.
        /// </summary>
        public bool GenerateSubtitlesFromScript { get; set; } = true;

        /// <summary>
        /// Words per minute for subtitle timing (default: 150).
        /// Used when generating subtitles from script text.
        /// </summary>
        public int WordsPerMinute { get; set; } = 150;

        /// <summary>
        /// Enable cinematic camera motion effects (pan, zoom, tilt) for smoother transitions (default: true).
        /// </summary>
        public bool EnableCameraMotion { get; set; } = true;

        /// <summary>
        /// Camera motion intensity (0.0-1.0, default: 0.3).
        /// Controls the strength of zoom and pan effects.
        /// </summary>
        public double CameraMotionIntensity { get; set; } = 0.3;

        /// <summary>
        /// Camera motion type for keyframe transitions.
        /// </summary>
        public CameraMotionType CameraMotion { get; set; } = CameraMotionType.Dynamic;

        public VideoProductionConfig()
        {
            KeyframePaths = new List<string>();
            SoundEffectsPaths = new List<string>();
            SafeMargins = new SafeTextMargins();
        }
    }

    /// <summary>
    /// Types of camera motion for video production.
    /// </summary>
    public enum CameraMotionType
    {
        /// <summary>
        /// No camera motion, static keyframes only.
        /// </summary>
        None,

        /// <summary>
        /// Slow zoom in effect on each keyframe.
        /// </summary>
        ZoomIn,

        /// <summary>
        /// Slow zoom out effect on each keyframe.
        /// </summary>
        ZoomOut,

        /// <summary>
        /// Pan left to right across keyframes.
        /// </summary>
        PanRight,

        /// <summary>
        /// Pan right to left across keyframes.
        /// </summary>
        PanLeft,

        /// <summary>
        /// Combination of zoom and pan for cinematic effect.
        /// </summary>
        ZoomAndPan,

        /// <summary>
        /// Dynamic motion that varies between keyframes (default).
        /// Alternates between different effects for visual interest.
        /// </summary>
        Dynamic
    }

    /// <summary>
    /// Result of video production operation.
    /// </summary>
    public class VideoProductionResult
    {
        /// <summary>
        /// Path to the produced video file.
        /// </summary>
        public string? OutputPath { get; set; }

        /// <summary>
        /// Indicates if the operation was successful.
        /// </summary>
        public bool Success { get; set; }

        /// <summary>
        /// Total processing time in seconds.
        /// </summary>
        public double ProcessingTimeSeconds { get; set; }

        /// <summary>
        /// Output video duration in seconds.
        /// </summary>
        public double VideoDurationSeconds { get; set; }

        /// <summary>
        /// Output file size in bytes.
        /// </summary>
        public long FileSizeBytes { get; set; }

        /// <summary>
        /// Output file size in megabytes.
        /// </summary>
        public double FileSizeMB => FileSizeBytes / (1024.0 * 1024.0);

        /// <summary>
        /// Error message if operation failed.
        /// </summary>
        public string? ErrorMessage { get; set; }

        /// <summary>
        /// Path to the generated SRT file (if created).
        /// </summary>
        public string? GeneratedSrtPath { get; set; }

        /// <summary>
        /// Path to the intermediate video file (before post-production).
        /// </summary>
        public string? IntermediateVideoPath { get; set; }

        /// <summary>
        /// Additional processing details and warnings.
        /// </summary>
        public List<string> ProcessingNotes { get; set; }

        public VideoProductionResult()
        {
            ProcessingNotes = new List<string>();
        }
    }
}
