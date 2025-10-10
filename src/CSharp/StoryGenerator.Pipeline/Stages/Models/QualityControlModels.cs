namespace StoryGenerator.Pipeline.Stages.Models;

/// <summary>
/// Input for Device Preview Stage
/// </summary>
public class DevicePreviewInput
{
    /// <summary>
    /// Path to the video file to preview
    /// </summary>
    public string VideoPath { get; set; } = string.Empty;

    /// <summary>
    /// Title ID for organizing output
    /// </summary>
    public string TitleId { get; set; } = string.Empty;

    /// <summary>
    /// Target gender audience
    /// </summary>
    public string Gender { get; set; } = string.Empty;

    /// <summary>
    /// Target age group
    /// </summary>
    public string AgeGroup { get; set; } = string.Empty;

    /// <summary>
    /// Device profiles to test
    /// </summary>
    public List<DeviceProfile> DeviceProfiles { get; set; } = new();
}

/// <summary>
/// Output from Device Preview Stage
/// </summary>
public class DevicePreviewOutput
{
    /// <summary>
    /// Generated previews
    /// </summary>
    public List<DevicePreview> Previews { get; set; } = new();

    /// <summary>
    /// Output directory path
    /// </summary>
    public string OutputPath { get; set; } = string.Empty;
}

/// <summary>
/// Represents a device profile for preview testing
/// </summary>
public class DeviceProfile
{
    /// <summary>
    /// Device name (e.g., "iPhone 14", "Samsung Galaxy S23")
    /// </summary>
    public string Name { get; set; } = string.Empty;

    /// <summary>
    /// Screen width in pixels
    /// </summary>
    public int Width { get; set; }

    /// <summary>
    /// Screen height in pixels
    /// </summary>
    public int Height { get; set; }

    /// <summary>
    /// Aspect ratio (e.g., "16:9", "9:16")
    /// </summary>
    public string AspectRatio { get; set; } = string.Empty;

    /// <summary>
    /// Safe zone percentage (e.g., 0.9 for 90%)
    /// </summary>
    public double SafeZonePercentage { get; set; } = 0.9;
}

/// <summary>
/// Represents a generated device preview
/// </summary>
public class DevicePreview
{
    /// <summary>
    /// Device profile used
    /// </summary>
    public DeviceProfile Profile { get; set; } = new();

    /// <summary>
    /// Preview file path
    /// </summary>
    public string PreviewPath { get; set; } = string.Empty;

    /// <summary>
    /// Readability score (0-100)
    /// </summary>
    public double ReadabilityScore { get; set; }

    /// <summary>
    /// Safe zone compliance (true if content fits within safe zone)
    /// </summary>
    public bool SafeZoneCompliant { get; set; }

    /// <summary>
    /// Issues detected during preview generation
    /// </summary>
    public List<string> Issues { get; set; } = new();
}

/// <summary>
/// Input for Sync Check Stage
/// </summary>
public class SyncCheckInput
{
    /// <summary>
    /// Path to the video file
    /// </summary>
    public string VideoPath { get; set; } = string.Empty;

    /// <summary>
    /// Path to the subtitle file (SRT format)
    /// </summary>
    public string SubtitlePath { get; set; } = string.Empty;

    /// <summary>
    /// Title ID for organizing output
    /// </summary>
    public string TitleId { get; set; } = string.Empty;

    /// <summary>
    /// Target gender audience
    /// </summary>
    public string Gender { get; set; } = string.Empty;

    /// <summary>
    /// Target age group
    /// </summary>
    public string AgeGroup { get; set; } = string.Empty;

    /// <summary>
    /// Maximum allowed drift in milliseconds (default: 50ms)
    /// </summary>
    public int MaxDriftMs { get; set; } = 50;
}

/// <summary>
/// Output from Sync Check Stage
/// </summary>
public class SyncCheckOutput
{
    /// <summary>
    /// Sync validation results
    /// </summary>
    public SyncCheckResult Result { get; set; } = new();

    /// <summary>
    /// Output report path
    /// </summary>
    public string ReportPath { get; set; } = string.Empty;
}

/// <summary>
/// Represents sync check results
/// </summary>
public class SyncCheckResult
{
    /// <summary>
    /// Overall sync status
    /// </summary>
    public bool IsSynced { get; set; }

    /// <summary>
    /// Maximum drift detected in milliseconds
    /// </summary>
    public int MaxDriftMs { get; set; }

    /// <summary>
    /// Average drift in milliseconds
    /// </summary>
    public double AverageDriftMs { get; set; }

    /// <summary>
    /// Number of subtitles analyzed
    /// </summary>
    public int SubtitleCount { get; set; }

    /// <summary>
    /// Individual subtitle sync issues
    /// </summary>
    public List<SubtitleSyncIssue> Issues { get; set; } = new();

    /// <summary>
    /// Timestamp of the check
    /// </summary>
    public DateTime CheckedAt { get; set; } = DateTime.UtcNow;
}

/// <summary>
/// Represents a subtitle sync issue
/// </summary>
public class SubtitleSyncIssue
{
    /// <summary>
    /// Subtitle index
    /// </summary>
    public int SubtitleIndex { get; set; }

    /// <summary>
    /// Subtitle start time
    /// </summary>
    public TimeSpan StartTime { get; set; }

    /// <summary>
    /// Subtitle end time
    /// </summary>
    public TimeSpan EndTime { get; set; }

    /// <summary>
    /// Detected drift in milliseconds
    /// </summary>
    public int DriftMs { get; set; }

    /// <summary>
    /// Issue description
    /// </summary>
    public string Description { get; set; } = string.Empty;
}

/// <summary>
/// Input for Quality Report Stage
/// </summary>
public class QualityReportInput
{
    /// <summary>
    /// Path to the video file
    /// </summary>
    public string VideoPath { get; set; } = string.Empty;

    /// <summary>
    /// Title ID
    /// </summary>
    public string TitleId { get; set; } = string.Empty;

    /// <summary>
    /// Target gender audience
    /// </summary>
    public string Gender { get; set; } = string.Empty;

    /// <summary>
    /// Target age group
    /// </summary>
    public string AgeGroup { get; set; } = string.Empty;

    /// <summary>
    /// Device preview results
    /// </summary>
    public DevicePreviewOutput? DevicePreviewResults { get; set; }

    /// <summary>
    /// Sync check results
    /// </summary>
    public SyncCheckOutput? SyncCheckResults { get; set; }
}

/// <summary>
/// Output from Quality Report Stage
/// </summary>
public class QualityReportOutput
{
    /// <summary>
    /// Quality report
    /// </summary>
    public QualityReport Report { get; set; } = new();

    /// <summary>
    /// Report file path (JSON)
    /// </summary>
    public string ReportPath { get; set; } = string.Empty;
}

/// <summary>
/// Represents a comprehensive quality report
/// </summary>
public class QualityReport
{
    /// <summary>
    /// Title ID
    /// </summary>
    public string TitleId { get; set; } = string.Empty;

    /// <summary>
    /// Report timestamp
    /// </summary>
    public DateTime Timestamp { get; set; } = DateTime.UtcNow;

    /// <summary>
    /// Overall status (PASS, FAIL, WARNING)
    /// </summary>
    public string OverallStatus { get; set; } = "UNKNOWN";

    /// <summary>
    /// Audio level metrics
    /// </summary>
    public AudioMetrics AudioLevels { get; set; } = new();

    /// <summary>
    /// A/V sync metrics
    /// </summary>
    public SyncMetrics AvSync { get; set; } = new();

    /// <summary>
    /// Video quality metrics
    /// </summary>
    public VideoQualityMetrics VideoQuality { get; set; } = new();

    /// <summary>
    /// Subtitle metrics
    /// </summary>
    public SubtitleMetrics Subtitles { get; set; } = new();

    /// <summary>
    /// Device compatibility metrics
    /// </summary>
    public DeviceCompatibilityMetrics Devices { get; set; } = new();

    /// <summary>
    /// List of issues found
    /// </summary>
    public List<string> Issues { get; set; } = new();

    /// <summary>
    /// Recommendations for improvement
    /// </summary>
    public List<string> Recommendations { get; set; } = new();
}

/// <summary>
/// Audio level metrics
/// </summary>
public class AudioMetrics
{
    /// <summary>
    /// LUFS (Loudness Units Full Scale) value
    /// </summary>
    public double Lufs { get; set; }

    /// <summary>
    /// Status (PASS, FAIL, WARNING)
    /// </summary>
    public string Status { get; set; } = "UNKNOWN";

    /// <summary>
    /// Target LUFS value
    /// </summary>
    public double TargetLufs { get; set; } = -14.0;

    /// <summary>
    /// Tolerance in LUFS
    /// </summary>
    public double Tolerance { get; set; } = 1.0;
}

/// <summary>
/// Sync metrics
/// </summary>
public class SyncMetrics
{
    /// <summary>
    /// Maximum drift in milliseconds
    /// </summary>
    public int MaxDrift { get; set; }

    /// <summary>
    /// Status (PASS, FAIL, WARNING)
    /// </summary>
    public string Status { get; set; } = "UNKNOWN";

    /// <summary>
    /// Allowed drift tolerance in milliseconds
    /// </summary>
    public int ToleranceMs { get; set; } = 50;
}

/// <summary>
/// Video quality metrics
/// </summary>
public class VideoQualityMetrics
{
    /// <summary>
    /// Video bitrate
    /// </summary>
    public string Bitrate { get; set; } = string.Empty;

    /// <summary>
    /// Resolution (e.g., "1080x1920")
    /// </summary>
    public string Resolution { get; set; } = string.Empty;

    /// <summary>
    /// Detected artifacts (if any)
    /// </summary>
    public string Artifacts { get; set; } = "none";

    /// <summary>
    /// Status (PASS, FAIL, WARNING)
    /// </summary>
    public string Status { get; set; } = "UNKNOWN";
}

/// <summary>
/// Subtitle metrics
/// </summary>
public class SubtitleMetrics
{
    /// <summary>
    /// Readability score (0-100)
    /// </summary>
    public double Readability { get; set; }

    /// <summary>
    /// Contrast quality (good, fair, poor)
    /// </summary>
    public string Contrast { get; set; } = "unknown";

    /// <summary>
    /// Status (PASS, FAIL, WARNING)
    /// </summary>
    public string Status { get; set; } = "UNKNOWN";
}

/// <summary>
/// Device compatibility metrics
/// </summary>
public class DeviceCompatibilityMetrics
{
    /// <summary>
    /// iOS device compatibility status
    /// </summary>
    public string Ios { get; set; } = "UNKNOWN";

    /// <summary>
    /// Android device compatibility status
    /// </summary>
    public string Android { get; set; } = "UNKNOWN";
}
