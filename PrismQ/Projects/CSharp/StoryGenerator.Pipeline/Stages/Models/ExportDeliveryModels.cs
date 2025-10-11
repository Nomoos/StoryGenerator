namespace StoryGenerator.Pipeline.Stages.Models;

/// <summary>
/// Input for Final Video Encode Stage
/// </summary>
public class FinalEncodeInput
{
    /// <summary>
    /// Path to the input video file (from QC/post-production)
    /// </summary>
    public string InputVideoPath { get; set; } = string.Empty;

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
    /// Target platform (e.g., "youtube", "tiktok", "instagram")
    /// </summary>
    public string Platform { get; set; } = "youtube";

    /// <summary>
    /// Target video codec (e.g., "h264", "h265")
    /// </summary>
    public string Codec { get; set; } = "h264";

    /// <summary>
    /// Target bitrate (e.g., "8M", "10M")
    /// </summary>
    public string Bitrate { get; set; } = "8M";

    /// <summary>
    /// Target resolution (e.g., "1080x1920" for vertical video)
    /// </summary>
    public string Resolution { get; set; } = "1080x1920";
}

/// <summary>
/// Output from Final Video Encode Stage
/// </summary>
public class FinalEncodeOutput
{
    /// <summary>
    /// Path to final encoded video file
    /// </summary>
    public string FinalVideoPath { get; set; } = string.Empty;

    /// <summary>
    /// File size in bytes
    /// </summary>
    public long FileSizeBytes { get; set; }

    /// <summary>
    /// Video duration in seconds
    /// </summary>
    public double DurationSeconds { get; set; }

    /// <summary>
    /// Actual codec used
    /// </summary>
    public string Codec { get; set; } = string.Empty;

    /// <summary>
    /// Actual bitrate
    /// </summary>
    public string Bitrate { get; set; } = string.Empty;

    /// <summary>
    /// Actual resolution
    /// </summary>
    public string Resolution { get; set; } = string.Empty;
}

/// <summary>
/// Input for Thumbnail Generation Stage
/// </summary>
public class ThumbnailGenerationInput
{
    /// <summary>
    /// Path to the video file
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
    /// Timestamp in seconds to extract thumbnail (null for middle frame)
    /// </summary>
    public double? TimestampSeconds { get; set; }

    /// <summary>
    /// Thumbnail width in pixels
    /// </summary>
    public int Width { get; set; } = 1920;

    /// <summary>
    /// Thumbnail height in pixels
    /// </summary>
    public int Height { get; set; } = 1080;

    /// <summary>
    /// JPEG quality (1-100)
    /// </summary>
    public int Quality { get; set; } = 90;
}

/// <summary>
/// Output from Thumbnail Generation Stage
/// </summary>
public class ThumbnailGenerationOutput
{
    /// <summary>
    /// Path to generated thumbnail image
    /// </summary>
    public string ThumbnailPath { get; set; } = string.Empty;

    /// <summary>
    /// Thumbnail width in pixels
    /// </summary>
    public int Width { get; set; }

    /// <summary>
    /// Thumbnail height in pixels
    /// </summary>
    public int Height { get; set; }

    /// <summary>
    /// File size in bytes
    /// </summary>
    public long FileSizeBytes { get; set; }

    /// <summary>
    /// Timestamp used for extraction
    /// </summary>
    public double TimestampSeconds { get; set; }
}

/// <summary>
/// Input for Metadata Creation Stage
/// </summary>
public class MetadataCreationInput
{
    /// <summary>
    /// Path to the final video file
    /// </summary>
    public string VideoPath { get; set; } = string.Empty;

    /// <summary>
    /// Path to the thumbnail file
    /// </summary>
    public string ThumbnailPath { get; set; } = string.Empty;

    /// <summary>
    /// Title ID
    /// </summary>
    public string TitleId { get; set; } = string.Empty;

    /// <summary>
    /// Video title
    /// </summary>
    public string Title { get; set; } = string.Empty;

    /// <summary>
    /// Video description
    /// </summary>
    public string Description { get; set; } = string.Empty;

    /// <summary>
    /// Target gender audience
    /// </summary>
    public string Gender { get; set; } = string.Empty;

    /// <summary>
    /// Target age group
    /// </summary>
    public string AgeGroup { get; set; } = string.Empty;

    /// <summary>
    /// Tags/keywords for the video
    /// </summary>
    public List<string> Tags { get; set; } = new();

    /// <summary>
    /// Target platform
    /// </summary>
    public string Platform { get; set; } = "youtube";

    /// <summary>
    /// Quality report results (optional)
    /// </summary>
    public string? QualityReportPath { get; set; }
}

/// <summary>
/// Output from Metadata Creation Stage
/// </summary>
public class MetadataCreationOutput
{
    /// <summary>
    /// Path to generated metadata JSON file
    /// </summary>
    public string MetadataPath { get; set; } = string.Empty;

    /// <summary>
    /// Metadata content
    /// </summary>
    public VideoMetadata Metadata { get; set; } = new();
}

/// <summary>
/// Represents video metadata for distribution
/// </summary>
public class VideoMetadata
{
    /// <summary>
    /// Unique title ID
    /// </summary>
    public string TitleId { get; set; } = string.Empty;

    /// <summary>
    /// Video title
    /// </summary>
    public string Title { get; set; } = string.Empty;

    /// <summary>
    /// Video description
    /// </summary>
    public string Description { get; set; } = string.Empty;

    /// <summary>
    /// Target platform
    /// </summary>
    public string Platform { get; set; } = string.Empty;

    /// <summary>
    /// Target gender audience
    /// </summary>
    public string Gender { get; set; } = string.Empty;

    /// <summary>
    /// Target age group
    /// </summary>
    public string AgeGroup { get; set; } = string.Empty;

    /// <summary>
    /// Video file path
    /// </summary>
    public string VideoPath { get; set; } = string.Empty;

    /// <summary>
    /// Thumbnail file path
    /// </summary>
    public string ThumbnailPath { get; set; } = string.Empty;

    /// <summary>
    /// Video duration in seconds
    /// </summary>
    public double DurationSeconds { get; set; }

    /// <summary>
    /// File size in bytes
    /// </summary>
    public long FileSizeBytes { get; set; }

    /// <summary>
    /// Video resolution
    /// </summary>
    public string Resolution { get; set; } = string.Empty;

    /// <summary>
    /// Video codec
    /// </summary>
    public string Codec { get; set; } = string.Empty;

    /// <summary>
    /// Video bitrate
    /// </summary>
    public string Bitrate { get; set; } = string.Empty;

    /// <summary>
    /// Tags/keywords
    /// </summary>
    public List<string> Tags { get; set; } = new();

    /// <summary>
    /// Creation timestamp
    /// </summary>
    public DateTime CreatedAt { get; set; } = DateTime.UtcNow;

    /// <summary>
    /// Quality report status (if available)
    /// </summary>
    public string? QualityStatus { get; set; }
}
