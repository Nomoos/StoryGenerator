namespace PrismQ.Shared.Core.Configuration;

/// <summary>
/// Configuration options for FFmpeg operations.
/// </summary>
public class FfmpegOptions
{
    /// <summary>
    /// Path to the ffmpeg executable.
    /// Default: "ffmpeg"
    /// </summary>
    public string ExecutablePath { get; set; } = "ffmpeg";

    /// <summary>
    /// Path to the ffprobe executable.
    /// Default: "ffprobe"
    /// </summary>
    public string FfprobePath { get; set; } = "ffprobe";

    /// <summary>
    /// Timeout for FFmpeg operations in seconds.
    /// Default: 600 (10 minutes)
    /// </summary>
    public int TimeoutSeconds { get; set; } = 600;

    /// <summary>
    /// Default Constant Rate Factor (CRF) for video encoding.
    /// Range: 0-51, lower is better quality.
    /// Default: 23 (good balance)
    /// </summary>
    public int DefaultCrf { get; set; } = 23;

    /// <summary>
    /// Default encoding preset.
    /// Options: ultrafast, superfast, veryfast, faster, fast, medium, slow, slower, veryslow
    /// Default: "medium"
    /// </summary>
    public string DefaultPreset { get; set; } = "medium";
}
