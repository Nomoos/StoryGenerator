namespace PrismQ.Shared.Interfaces;

/// <summary>
/// Service for executing FFmpeg operations.
/// </summary>
public interface IFFmpegService
{
    /// <summary>
    /// Probes a media file to get information about streams and duration.
    /// </summary>
    /// <param name="filePath">Path to the media file.</param>
    /// <param name="cancellationToken">Cancellation token.</param>
    /// <returns>Media file information.</returns>
    Task<Result<MediaInfo>> ProbeAsync(string filePath, CancellationToken cancellationToken = default);

    /// <summary>
    /// Concatenates multiple media files into one.
    /// </summary>
    /// <param name="inputPaths">Paths to input files.</param>
    /// <param name="outputPath">Path to output file.</param>
    /// <param name="cancellationToken">Cancellation token.</param>
    /// <returns>Result of the concatenation operation.</returns>
    Task<Result<string>> ConcatenateAsync(
        IEnumerable<string> inputPaths,
        string outputPath,
        CancellationToken cancellationToken = default);

    /// <summary>
    /// Re-encodes a media file with specified parameters.
    /// </summary>
    /// <param name="inputPath">Path to input file.</param>
    /// <param name="outputPath">Path to output file.</param>
    /// <param name="options">Encoding options.</param>
    /// <param name="cancellationToken">Cancellation token.</param>
    /// <returns>Result of the encoding operation.</returns>
    Task<Result<string>> EncodeAsync(
        string inputPath,
        string outputPath,
        FfmpegEncodeOptions? options = null,
        CancellationToken cancellationToken = default);

    /// <summary>
    /// Normalizes audio volume to a target LUFS level.
    /// </summary>
    /// <param name="inputPath">Path to input audio file.</param>
    /// <param name="outputPath">Path to output audio file.</param>
    /// <param name="targetLufs">Target LUFS level (default: -16).</param>
    /// <param name="cancellationToken">Cancellation token.</param>
    /// <returns>Result of the normalization operation.</returns>
    Task<Result<string>> NormalizeAudioAsync(
        string inputPath,
        string outputPath,
        double targetLufs = -16.0,
        CancellationToken cancellationToken = default);

    /// <summary>
    /// Checks if FFmpeg is available and properly configured.
    /// </summary>
    /// <returns>True if FFmpeg is available.</returns>
    Task<bool> IsAvailableAsync();
}

/// <summary>
/// Information about a media file.
/// </summary>
public class MediaInfo
{
    /// <summary>
    /// Duration in seconds.
    /// </summary>
    public double Duration { get; set; }

    /// <summary>
    /// Video stream information (null if no video).
    /// </summary>
    public VideoStreamInfo? Video { get; set; }

    /// <summary>
    /// Audio stream information (null if no audio).
    /// </summary>
    public AudioStreamInfo? Audio { get; set; }
}

/// <summary>
/// Video stream information.
/// </summary>
public class VideoStreamInfo
{
    /// <summary>
    /// Video codec name.
    /// </summary>
    public string Codec { get; set; } = string.Empty;

    /// <summary>
    /// Width in pixels.
    /// </summary>
    public int Width { get; set; }

    /// <summary>
    /// Height in pixels.
    /// </summary>
    public int Height { get; set; }

    /// <summary>
    /// Frame rate.
    /// </summary>
    public double FrameRate { get; set; }
}

/// <summary>
/// Audio stream information.
/// </summary>
public class AudioStreamInfo
{
    /// <summary>
    /// Audio codec name.
    /// </summary>
    public string Codec { get; set; } = string.Empty;

    /// <summary>
    /// Sample rate in Hz.
    /// </summary>
    public int SampleRate { get; set; }

    /// <summary>
    /// Number of audio channels.
    /// </summary>
    public int Channels { get; set; }
}

/// <summary>
/// FFmpeg encoding options.
/// </summary>
public class FfmpegEncodeOptions
{
    /// <summary>
    /// Video codec (default: "libx264").
    /// </summary>
    public string VideoCodec { get; set; } = "libx264";

    /// <summary>
    /// Audio codec (default: "aac").
    /// </summary>
    public string AudioCodec { get; set; } = "aac";

    /// <summary>
    /// Constant Rate Factor for quality (default: 23).
    /// </summary>
    public int Crf { get; set; } = 23;

    /// <summary>
    /// Encoding preset (default: "medium").
    /// </summary>
    public string Preset { get; set; } = "medium";

    /// <summary>
    /// Target resolution (e.g., "1920x1080"), null to keep original.
    /// </summary>
    public string? Resolution { get; set; }
}
