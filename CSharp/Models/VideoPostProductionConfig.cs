using System.Collections.Generic;

namespace StoryGenerator.Models
{
    /// <summary>
    /// Configuration for video post-production pipeline.
    /// </summary>
    public class VideoPostProductionConfig
    {
        /// <summary>
        /// List of video segment file paths to process.
        /// </summary>
        public List<string> SegmentPaths { get; set; }

        /// <summary>
        /// Output file path for the final video.
        /// Format: /final/{segment}/{age}/{title_id}_draft.mp4
        /// </summary>
        public string? OutputPath { get; set; }

        /// <summary>
        /// SRT subtitle file path (optional).
        /// </summary>
        public string? SrtPath { get; set; }

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
        /// Type of transition between segments (fade, xfade, none).
        /// </summary>
        public string TransitionType { get; set; } = "fade";

        /// <summary>
        /// Duration of transitions in seconds (default: 0.5).
        /// </summary>
        public double TransitionDuration { get; set; } = 0.5;

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

        public VideoPostProductionConfig()
        {
            SegmentPaths = new List<string>();
            SoundEffectsPaths = new List<string>();
            SafeMargins = new SafeTextMargins();
        }
    }

    /// <summary>
    /// Safe margins for text positioning in video (in pixels).
    /// Ensures subtitles don't get cut off on different devices.
    /// </summary>
    public class SafeTextMargins
    {
        /// <summary>
        /// Top margin in pixels (default: 100).
        /// </summary>
        public int Top { get; set; } = 100;

        /// <summary>
        /// Bottom margin in pixels (default: 150).
        /// </summary>
        public int Bottom { get; set; } = 150;

        /// <summary>
        /// Left margin in pixels (default: 50).
        /// </summary>
        public int Left { get; set; } = 50;

        /// <summary>
        /// Right margin in pixels (default: 50).
        /// </summary>
        public int Right { get; set; } = 50;
    }

    /// <summary>
    /// Result of video post-production operation.
    /// </summary>
    public class VideoPostProductionResult
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
        /// Additional processing details and warnings.
        /// </summary>
        public List<string> ProcessingNotes { get; set; }

        public VideoPostProductionResult()
        {
            ProcessingNotes = new List<string>();
        }
    }
}
