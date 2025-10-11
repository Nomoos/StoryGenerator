using System.Text.Json;
using StoryGenerator.Pipeline.Core;
using StoryGenerator.Pipeline.Interfaces;
using StoryGenerator.Pipeline.Stages.Models;

namespace StoryGenerator.Pipeline.Stages;

/// <summary>
/// Stage 1: Final Video Encode
/// Encodes video to final distribution format with platform-specific settings.
/// </summary>
public class FinalEncodeStage : BasePipelineStage<FinalEncodeInput, FinalEncodeOutput>
{
    public override string StageName => "FinalEncode";

    protected override async Task<FinalEncodeOutput> ExecuteCoreAsync(
        FinalEncodeInput input,
        IProgress<PipelineProgress>? progress,
        CancellationToken cancellationToken)
    {
        ReportProgress(progress, 10, "Starting final video encoding...");

        if (!File.Exists(input.InputVideoPath))
        {
            throw new FileNotFoundException($"Input video file not found: {input.InputVideoPath}");
        }

        // Create output directory
        var outputPath = Path.Combine(
            "data",
            "Generator",
            "final",
            input.Gender,
            input.AgeGroup);

        Directory.CreateDirectory(outputPath);

        var finalFileName = $"{input.TitleId}.mp4";
        var finalPath = Path.Combine(outputPath, finalFileName);

        ReportProgress(progress, 30, $"Encoding for {input.Platform} platform...");

        // Encode video with platform-specific settings
        await EncodeVideoAsync(
            input.InputVideoPath,
            finalPath,
            input.Platform,
            input.Codec,
            input.Bitrate,
            input.Resolution,
            cancellationToken);

        ReportProgress(progress, 70, "Analyzing encoded video...");

        // Get video properties
        var fileInfo = new FileInfo(finalPath);
        var duration = await GetVideoDurationAsync(finalPath, cancellationToken);

        ReportProgress(progress, 90, "Final encoding complete");

        return new FinalEncodeOutput
        {
            FinalVideoPath = finalPath,
            FileSizeBytes = fileInfo.Length,
            DurationSeconds = duration,
            Codec = input.Codec,
            Bitrate = input.Bitrate,
            Resolution = input.Resolution
        };
    }

    private async Task EncodeVideoAsync(
        string inputPath,
        string outputPath,
        string platform,
        string codec,
        string bitrate,
        string resolution,
        CancellationToken cancellationToken)
    {
        // Simulate video encoding
        await Task.Delay(300, cancellationToken);

        // In real implementation, this would use FFmpeg to encode with platform-specific settings:
        // YouTube Shorts: H.264, 1080x1920, 8-10Mbps
        // TikTok: H.264, 1080x1920, 6-8Mbps  
        // Instagram Reels: H.264, 1080x1920, 8-10Mbps

        // Platform-specific encoding profiles:
        var encodingProfile = platform.ToLower() switch
        {
            "youtube" => "High quality H.264 with -14 LUFS audio",
            "tiktok" => "Optimized H.264 for mobile, lower bitrate",
            "instagram" => "H.264 with Instagram-specific encoding",
            _ => "Standard H.264 encoding"
        };

        // Copy input to output (placeholder)
        File.Copy(inputPath, outputPath, overwrite: true);
    }

    private async Task<double> GetVideoDurationAsync(string videoPath, CancellationToken cancellationToken)
    {
        // Simulate duration extraction
        await Task.Delay(50, cancellationToken);

        // In real implementation, this would use FFmpeg to extract duration
        // For now, estimate based on file size (very rough)
        var fileInfo = new FileInfo(videoPath);
        var estimatedDuration = Math.Max(30.0, Math.Min(60.0, fileInfo.Length / 100000.0));
        
        return Math.Round(estimatedDuration, 2);
    }
}

/// <summary>
/// Stage 2: Thumbnail Generation
/// Extracts and generates thumbnail image from video.
/// </summary>
public class ThumbnailGenerationStage : BasePipelineStage<ThumbnailGenerationInput, ThumbnailGenerationOutput>
{
    public override string StageName => "ThumbnailGeneration";

    protected override async Task<ThumbnailGenerationOutput> ExecuteCoreAsync(
        ThumbnailGenerationInput input,
        IProgress<PipelineProgress>? progress,
        CancellationToken cancellationToken)
    {
        ReportProgress(progress, 10, "Starting thumbnail generation...");

        if (!File.Exists(input.VideoPath))
        {
            throw new FileNotFoundException($"Video file not found: {input.VideoPath}");
        }

        // Create output directory
        var outputPath = Path.Combine(
            "data",
            "Generator",
            "final",
            input.Gender,
            input.AgeGroup);

        Directory.CreateDirectory(outputPath);

        var thumbnailFileName = $"{input.TitleId}_thumbnail.jpg";
        var thumbnailPath = Path.Combine(outputPath, thumbnailFileName);

        ReportProgress(progress, 40, "Extracting frame from video...");

        // Determine timestamp for thumbnail extraction
        var timestamp = input.TimestampSeconds ?? await GetMiddleTimestampAsync(input.VideoPath, cancellationToken);

        ReportProgress(progress, 60, "Generating thumbnail image...");

        // Extract and save thumbnail
        await GenerateThumbnailAsync(
            input.VideoPath,
            thumbnailPath,
            timestamp,
            input.Width,
            input.Height,
            input.Quality,
            cancellationToken);

        var fileInfo = new FileInfo(thumbnailPath);

        ReportProgress(progress, 90, "Thumbnail generation complete");

        return new ThumbnailGenerationOutput
        {
            ThumbnailPath = thumbnailPath,
            Width = input.Width,
            Height = input.Height,
            FileSizeBytes = fileInfo.Length,
            TimestampSeconds = timestamp
        };
    }

    private async Task<double> GetMiddleTimestampAsync(string videoPath, CancellationToken cancellationToken)
    {
        // Simulate duration extraction
        await Task.Delay(50, cancellationToken);

        // In real implementation, get video duration via FFmpeg
        // For now, assume middle of a 30-60 second video
        return 25.0; // Middle of ~50 second video
    }

    private async Task GenerateThumbnailAsync(
        string videoPath,
        string thumbnailPath,
        double timestamp,
        int width,
        int height,
        int quality,
        CancellationToken cancellationToken)
    {
        // Simulate thumbnail extraction
        await Task.Delay(200, cancellationToken);

        // In real implementation, use FFmpeg to extract frame:
        // ffmpeg -ss {timestamp} -i {videoPath} -vframes 1 -s {width}x{height} -q:v {quality} {thumbnailPath}

        // Create a placeholder thumbnail file
        File.WriteAllText(thumbnailPath, $"Thumbnail extracted at {timestamp}s from {Path.GetFileName(videoPath)}");
    }
}

/// <summary>
/// Stage 3: Metadata Creation
/// Creates comprehensive metadata JSON for video distribution.
/// </summary>
public class MetadataCreationStage : BasePipelineStage<MetadataCreationInput, MetadataCreationOutput>
{
    public override string StageName => "MetadataCreation";

    protected override async Task<MetadataCreationOutput> ExecuteCoreAsync(
        MetadataCreationInput input,
        IProgress<PipelineProgress>? progress,
        CancellationToken cancellationToken)
    {
        ReportProgress(progress, 10, "Starting metadata creation...");

        if (!File.Exists(input.VideoPath))
        {
            throw new FileNotFoundException($"Video file not found: {input.VideoPath}");
        }

        if (!File.Exists(input.ThumbnailPath))
        {
            throw new FileNotFoundException($"Thumbnail file not found: {input.ThumbnailPath}");
        }

        // Create output directory
        var outputPath = Path.Combine(
            "data",
            "Generator",
            "final",
            input.Gender,
            input.AgeGroup);

        Directory.CreateDirectory(outputPath);

        var metadataFileName = $"{input.TitleId}_metadata.json";
        var metadataPath = Path.Combine(outputPath, metadataFileName);

        ReportProgress(progress, 30, "Gathering video information...");

        // Extract video properties
        var videoInfo = await ExtractVideoPropertiesAsync(input.VideoPath, cancellationToken);

        ReportProgress(progress, 50, "Loading quality report...");

        // Load quality report if available
        string? qualityStatus = null;
        if (!string.IsNullOrEmpty(input.QualityReportPath) && File.Exists(input.QualityReportPath))
        {
            qualityStatus = await ExtractQualityStatusAsync(input.QualityReportPath, cancellationToken);
        }

        ReportProgress(progress, 70, "Creating metadata structure...");

        // Build metadata
        var metadata = new VideoMetadata
        {
            TitleId = input.TitleId,
            Title = input.Title,
            Description = input.Description,
            Platform = input.Platform,
            Gender = input.Gender,
            AgeGroup = input.AgeGroup,
            VideoPath = Path.GetFileName(input.VideoPath),
            ThumbnailPath = Path.GetFileName(input.ThumbnailPath),
            DurationSeconds = videoInfo.Duration,
            FileSizeBytes = videoInfo.FileSize,
            Resolution = videoInfo.Resolution,
            Codec = videoInfo.Codec,
            Bitrate = videoInfo.Bitrate,
            Tags = input.Tags,
            QualityStatus = qualityStatus
        };

        ReportProgress(progress, 80, "Saving metadata file...");

        // Save metadata to JSON
        await SaveMetadataAsync(metadata, metadataPath, cancellationToken);

        ReportProgress(progress, 90, "Metadata creation complete");

        return new MetadataCreationOutput
        {
            MetadataPath = metadataPath,
            Metadata = metadata
        };
    }

    private async Task<(double Duration, long FileSize, string Resolution, string Codec, string Bitrate)> ExtractVideoPropertiesAsync(
        string videoPath,
        CancellationToken cancellationToken)
    {
        // Simulate property extraction
        await Task.Delay(100, cancellationToken);

        // In real implementation, use FFmpeg/FFprobe to extract properties
        var fileInfo = new FileInfo(videoPath);
        var duration = Math.Max(30.0, Math.Min(60.0, fileInfo.Length / 100000.0));

        return (
            Duration: Math.Round(duration, 2),
            FileSize: fileInfo.Length,
            Resolution: "1080x1920",
            Codec: "h264",
            Bitrate: "8M"
        );
    }

    private async Task<string> ExtractQualityStatusAsync(string reportPath, CancellationToken cancellationToken)
    {
        try
        {
            var reportJson = await File.ReadAllTextAsync(reportPath, cancellationToken);
            var report = JsonSerializer.Deserialize<Dictionary<string, JsonElement>>(reportJson);
            
            if (report != null && report.TryGetValue("overallStatus", out var status))
            {
                return status.GetString() ?? "UNKNOWN";
            }
        }
        catch
        {
            // If we can't read the report, return UNKNOWN
        }

        return "UNKNOWN";
    }

    private async Task SaveMetadataAsync(
        VideoMetadata metadata,
        string metadataPath,
        CancellationToken cancellationToken)
    {
        var json = JsonSerializer.Serialize(metadata, new JsonSerializerOptions
        {
            WriteIndented = true,
            PropertyNamingPolicy = JsonNamingPolicy.CamelCase
        });

        await File.WriteAllTextAsync(metadataPath, json, cancellationToken);
    }
}
