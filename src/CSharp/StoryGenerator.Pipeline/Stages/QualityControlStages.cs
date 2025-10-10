using System.Text.Json;
using StoryGenerator.Pipeline.Core;
using StoryGenerator.Pipeline.Interfaces;
using StoryGenerator.Pipeline.Stages.Models;

namespace StoryGenerator.Pipeline.Stages;

/// <summary>
/// Stage 1: Device Preview Generation
/// Generates device-specific preview renders to test video appearance on target platforms.
/// </summary>
public class DevicePreviewStage : BasePipelineStage<DevicePreviewInput, DevicePreviewOutput>
{
    public override string StageName => "DevicePreview";

    protected override async Task<DevicePreviewOutput> ExecuteCoreAsync(
        DevicePreviewInput input,
        IProgress<PipelineProgress>? progress,
        CancellationToken cancellationToken)
    {
        ReportProgress(progress, 10, "Starting device preview generation...");

        if (!File.Exists(input.VideoPath))
        {
            throw new FileNotFoundException($"Video file not found: {input.VideoPath}");
        }

        // Create output directory
        var outputPath = Path.Combine(
            "data",
            "Generator",
            "qc",
            "device_tests",
            input.Gender,
            input.AgeGroup,
            input.TitleId);

        Directory.CreateDirectory(outputPath);

        var previews = new List<DevicePreview>();

        // Use default device profiles if none provided
        var deviceProfiles = input.DeviceProfiles.Any()
            ? input.DeviceProfiles
            : GetDefaultDeviceProfiles();

        int processedCount = 0;
        int totalCount = deviceProfiles.Count;

        foreach (var profile in deviceProfiles)
        {
            cancellationToken.ThrowIfCancellationRequested();

            var preview = await GenerateDevicePreviewAsync(
                input.VideoPath,
                profile,
                outputPath,
                cancellationToken);

            previews.Add(preview);

            processedCount++;
            int percentComplete = 10 + (int)((processedCount / (double)totalCount) * 80);
            ReportProgress(progress, percentComplete, $"Generated preview for {profile.Name}");
        }

        ReportProgress(progress, 90, "Device preview generation complete");

        return new DevicePreviewOutput
        {
            Previews = previews,
            OutputPath = outputPath
        };
    }

    private List<DeviceProfile> GetDefaultDeviceProfiles()
    {
        return new List<DeviceProfile>
        {
            new DeviceProfile
            {
                Name = "iPhone 14",
                Width = 1170,
                Height = 2532,
                AspectRatio = "9:19.5",
                SafeZonePercentage = 0.9
            },
            new DeviceProfile
            {
                Name = "Samsung Galaxy S23",
                Width = 1080,
                Height = 2340,
                AspectRatio = "9:19.5",
                SafeZonePercentage = 0.9
            },
            new DeviceProfile
            {
                Name = "iPad Pro",
                Width = 2048,
                Height = 2732,
                AspectRatio = "3:4",
                SafeZonePercentage = 0.92
            }
        };
    }

    private async Task<DevicePreview> GenerateDevicePreviewAsync(
        string videoPath,
        DeviceProfile profile,
        string outputPath,
        CancellationToken cancellationToken)
    {
        // Simulate preview generation (in real implementation, this would use FFmpeg)
        await Task.Delay(100, cancellationToken);

        var previewFileName = $"{profile.Name.Replace(" ", "_")}_preview.mp4";
        var previewPath = Path.Combine(outputPath, previewFileName);

        // Calculate readability score (simplified simulation)
        var readabilityScore = CalculateReadabilityScore(profile);

        // Check safe zone compliance
        var safeZoneCompliant = CheckSafeZoneCompliance(profile);

        var issues = new List<string>();
        if (readabilityScore < 70)
        {
            issues.Add($"Low readability score: {readabilityScore:F1}");
        }
        if (!safeZoneCompliant)
        {
            issues.Add("Content extends beyond safe zone");
        }

        return new DevicePreview
        {
            Profile = profile,
            PreviewPath = previewPath,
            ReadabilityScore = readabilityScore,
            SafeZoneCompliant = safeZoneCompliant,
            Issues = issues
        };
    }

    private double CalculateReadabilityScore(DeviceProfile profile)
    {
        // Simplified readability calculation based on screen size
        // Larger screens generally have better readability
        var pixelArea = profile.Width * profile.Height;
        var baseScore = Math.Min(100, (pixelArea / 20000.0)); // Normalize to 0-100
        return Math.Round(baseScore, 1);
    }

    private bool CheckSafeZoneCompliance(DeviceProfile profile)
    {
        // Simplified check - in real implementation, this would analyze actual content
        return profile.SafeZonePercentage >= 0.85;
    }
}

/// <summary>
/// Stage 2: A/V Sync Check
/// Verifies audio-subtitle synchronization accuracy.
/// </summary>
public class SyncCheckStage : BasePipelineStage<SyncCheckInput, SyncCheckOutput>
{
    public override string StageName => "SyncCheck";

    protected override async Task<SyncCheckOutput> ExecuteCoreAsync(
        SyncCheckInput input,
        IProgress<PipelineProgress>? progress,
        CancellationToken cancellationToken)
    {
        ReportProgress(progress, 10, "Starting A/V sync check...");

        if (!File.Exists(input.VideoPath))
        {
            throw new FileNotFoundException($"Video file not found: {input.VideoPath}");
        }

        if (!File.Exists(input.SubtitlePath))
        {
            throw new FileNotFoundException($"Subtitle file not found: {input.SubtitlePath}");
        }

        // Create output directory
        var outputPath = Path.Combine(
            "data",
            "Generator",
            "qc",
            "sync_reports",
            input.Gender,
            input.AgeGroup);

        Directory.CreateDirectory(outputPath);

        ReportProgress(progress, 30, "Extracting subtitle timing...");

        var subtitles = await ExtractSubtitleTimingAsync(input.SubtitlePath, cancellationToken);

        ReportProgress(progress, 50, "Analyzing audio sync...");

        var syncResult = await AnalyzeSyncAsync(
            input.VideoPath,
            subtitles,
            input.MaxDriftMs,
            cancellationToken);

        ReportProgress(progress, 70, "Generating sync report...");

        var reportPath = Path.Combine(outputPath, $"{input.TitleId}_sync_report.json");
        await SaveSyncReportAsync(syncResult, reportPath, cancellationToken);

        ReportProgress(progress, 90, "Sync check complete");

        return new SyncCheckOutput
        {
            Result = syncResult,
            ReportPath = reportPath
        };
    }

    private async Task<List<SubtitleEntry>> ExtractSubtitleTimingAsync(
        string subtitlePath,
        CancellationToken cancellationToken)
    {
        var subtitles = new List<SubtitleEntry>();

        // Read and parse SRT file
        var lines = await File.ReadAllLinesAsync(subtitlePath, cancellationToken);
        
        for (int i = 0; i < lines.Length; i++)
        {
            // SRT format: index, timestamp, text
            if (int.TryParse(lines[i].Trim(), out int index))
            {
                if (i + 1 < lines.Length && lines[i + 1].Contains("-->"))
                {
                    var timeParts = lines[i + 1].Split(new[] { "-->" }, StringSplitOptions.None);
                    if (timeParts.Length == 2)
                    {
                        var startTime = ParseSrtTimestamp(timeParts[0].Trim());
                        var endTime = ParseSrtTimestamp(timeParts[1].Trim());

                        subtitles.Add(new SubtitleEntry
                        {
                            Index = index,
                            StartTime = startTime,
                            EndTime = endTime
                        });
                    }
                }
            }
        }

        return subtitles;
    }

    private TimeSpan ParseSrtTimestamp(string timestamp)
    {
        // SRT format: HH:MM:SS,mmm
        var parts = timestamp.Replace(',', '.').Split(':');
        if (parts.Length == 3)
        {
            var secondsParts = parts[2].Split('.');
            var hours = int.Parse(parts[0]);
            var minutes = int.Parse(parts[1]);
            var seconds = int.Parse(secondsParts[0]);
            var milliseconds = secondsParts.Length > 1 ? int.Parse(secondsParts[1]) : 0;

            return new TimeSpan(0, hours, minutes, seconds, milliseconds);
        }

        return TimeSpan.Zero;
    }

    private async Task<SyncCheckResult> AnalyzeSyncAsync(
        string videoPath,
        List<SubtitleEntry> subtitles,
        int maxDriftMs,
        CancellationToken cancellationToken)
    {
        // Simulate sync analysis
        await Task.Delay(200, cancellationToken);

        var issues = new List<SubtitleSyncIssue>();
        var driftValues = new List<int>();

        // Simulate sync check for each subtitle
        var random = new Random(42); // Use fixed seed for consistent results
        foreach (var subtitle in subtitles)
        {
            // Simulate drift detection (in real implementation, this would use audio analysis)
            var drift = random.Next(-30, 30); // Random drift between -30ms and +30ms
            driftValues.Add(Math.Abs(drift));

            if (Math.Abs(drift) > maxDriftMs)
            {
                issues.Add(new SubtitleSyncIssue
                {
                    SubtitleIndex = subtitle.Index,
                    StartTime = subtitle.StartTime,
                    EndTime = subtitle.EndTime,
                    DriftMs = drift,
                    Description = $"Sync drift of {drift}ms exceeds tolerance of {maxDriftMs}ms"
                });
            }
        }

        var maxDrift = driftValues.Any() ? driftValues.Max() : 0;
        var averageDrift = driftValues.Any() ? driftValues.Average() : 0;

        return new SyncCheckResult
        {
            IsSynced = issues.Count == 0,
            MaxDriftMs = maxDrift,
            AverageDriftMs = Math.Round(averageDrift, 1),
            SubtitleCount = subtitles.Count,
            Issues = issues
        };
    }

    private async Task SaveSyncReportAsync(
        SyncCheckResult result,
        string reportPath,
        CancellationToken cancellationToken)
    {
        var json = JsonSerializer.Serialize(result, new JsonSerializerOptions
        {
            WriteIndented = true
        });

        await File.WriteAllTextAsync(reportPath, json, cancellationToken);
    }

    private class SubtitleEntry
    {
        public int Index { get; set; }
        public TimeSpan StartTime { get; set; }
        public TimeSpan EndTime { get; set; }
    }
}

/// <summary>
/// Stage 3: Quality Report Generation
/// Generates comprehensive quality assessment report.
/// </summary>
public class QualityReportStage : BasePipelineStage<QualityReportInput, QualityReportOutput>
{
    public override string StageName => "QualityReport";

    protected override async Task<QualityReportOutput> ExecuteCoreAsync(
        QualityReportInput input,
        IProgress<PipelineProgress>? progress,
        CancellationToken cancellationToken)
    {
        ReportProgress(progress, 10, "Starting quality report generation...");

        if (!File.Exists(input.VideoPath))
        {
            throw new FileNotFoundException($"Video file not found: {input.VideoPath}");
        }

        // Create output directory
        var outputPath = Path.Combine(
            "data",
            "Generator",
            "qc",
            "quality_reports",
            input.Gender,
            input.AgeGroup);

        Directory.CreateDirectory(outputPath);

        ReportProgress(progress, 30, "Collecting audio metrics...");
        var audioMetrics = await CollectAudioMetricsAsync(input.VideoPath, cancellationToken);

        ReportProgress(progress, 40, "Collecting video metrics...");
        var videoMetrics = await CollectVideoMetricsAsync(input.VideoPath, cancellationToken);

        ReportProgress(progress, 50, "Analyzing sync results...");
        var syncMetrics = AnalyzeSyncMetrics(input.SyncCheckResults);

        ReportProgress(progress, 60, "Analyzing subtitle quality...");
        var subtitleMetrics = AnalyzeSubtitleMetrics(input.DevicePreviewResults);

        ReportProgress(progress, 70, "Analyzing device compatibility...");
        var deviceMetrics = AnalyzeDeviceCompatibility(input.DevicePreviewResults);

        ReportProgress(progress, 80, "Generating report...");

        var report = GenerateQualityReport(
            input.TitleId,
            audioMetrics,
            videoMetrics,
            syncMetrics,
            subtitleMetrics,
            deviceMetrics);

        var reportPath = Path.Combine(outputPath, $"{input.TitleId}_qc_report.json");
        await SaveQualityReportAsync(report, reportPath, cancellationToken);

        ReportProgress(progress, 90, "Quality report generation complete");

        return new QualityReportOutput
        {
            Report = report,
            ReportPath = reportPath
        };
    }

    private async Task<AudioMetrics> CollectAudioMetricsAsync(
        string videoPath,
        CancellationToken cancellationToken)
    {
        // Simulate audio analysis (in real implementation, this would use FFmpeg)
        await Task.Delay(100, cancellationToken);

        var lufs = -14.2; // Simulated LUFS value
        var targetLufs = -14.0;
        var tolerance = 1.0;

        var status = Math.Abs(lufs - targetLufs) <= tolerance ? "PASS" : "FAIL";

        return new AudioMetrics
        {
            Lufs = lufs,
            Status = status,
            TargetLufs = targetLufs,
            Tolerance = tolerance
        };
    }

    private async Task<VideoQualityMetrics> CollectVideoMetricsAsync(
        string videoPath,
        CancellationToken cancellationToken)
    {
        // Simulate video analysis
        await Task.Delay(100, cancellationToken);

        return new VideoQualityMetrics
        {
            Bitrate = "8M",
            Resolution = "1080x1920",
            Artifacts = "none",
            Status = "PASS"
        };
    }

    private SyncMetrics AnalyzeSyncMetrics(SyncCheckOutput? syncCheckResults)
    {
        if (syncCheckResults?.Result == null)
        {
            return new SyncMetrics
            {
                MaxDrift = 0,
                Status = "UNKNOWN",
                ToleranceMs = 50
            };
        }

        var maxDrift = syncCheckResults.Result.MaxDriftMs;
        var toleranceMs = 50;
        var status = maxDrift <= toleranceMs ? "PASS" : "FAIL";

        return new SyncMetrics
        {
            MaxDrift = maxDrift,
            Status = status,
            ToleranceMs = toleranceMs
        };
    }

    private SubtitleMetrics AnalyzeSubtitleMetrics(DevicePreviewOutput? devicePreviewResults)
    {
        if (devicePreviewResults?.Previews == null || !devicePreviewResults.Previews.Any())
        {
            return new SubtitleMetrics
            {
                Readability = 0,
                Contrast = "unknown",
                Status = "UNKNOWN"
            };
        }

        var avgReadability = devicePreviewResults.Previews
            .Average(p => p.ReadabilityScore);

        var status = avgReadability >= 70 ? "PASS" : avgReadability >= 50 ? "WARNING" : "FAIL";

        return new SubtitleMetrics
        {
            Readability = Math.Round(avgReadability, 1),
            Contrast = "good",
            Status = status
        };
    }

    private DeviceCompatibilityMetrics AnalyzeDeviceCompatibility(DevicePreviewOutput? devicePreviewResults)
    {
        if (devicePreviewResults?.Previews == null || !devicePreviewResults.Previews.Any())
        {
            return new DeviceCompatibilityMetrics
            {
                Ios = "UNKNOWN",
                Android = "UNKNOWN"
            };
        }

        var iosDevices = devicePreviewResults.Previews
            .Where(p => p.Profile.Name.Contains("iPhone") || p.Profile.Name.Contains("iPad"))
            .ToList();

        var androidDevices = devicePreviewResults.Previews
            .Where(p => p.Profile.Name.Contains("Galaxy") || p.Profile.Name.Contains("Android"))
            .ToList();

        var iosStatus = iosDevices.Any()
            ? (iosDevices.All(d => d.SafeZoneCompliant && d.ReadabilityScore >= 70) ? "PASS" : "WARNING")
            : "UNKNOWN";

        var androidStatus = androidDevices.Any()
            ? (androidDevices.All(d => d.SafeZoneCompliant && d.ReadabilityScore >= 70) ? "PASS" : "WARNING")
            : "UNKNOWN";

        return new DeviceCompatibilityMetrics
        {
            Ios = iosStatus,
            Android = androidStatus
        };
    }

    private QualityReport GenerateQualityReport(
        string titleId,
        AudioMetrics audioMetrics,
        VideoQualityMetrics videoMetrics,
        SyncMetrics syncMetrics,
        SubtitleMetrics subtitleMetrics,
        DeviceCompatibilityMetrics deviceMetrics)
    {
        var issues = new List<string>();
        var recommendations = new List<string>();

        // Check each metric and collect issues/recommendations
        if (audioMetrics.Status == "FAIL")
        {
            issues.Add($"Audio levels out of range: {audioMetrics.Lufs:F1} LUFS (target: {audioMetrics.TargetLufs} ±{audioMetrics.Tolerance})");
            recommendations.Add("Re-normalize audio to target -14.0 LUFS");
        }

        if (syncMetrics.Status == "FAIL")
        {
            issues.Add($"A/V sync drift exceeds tolerance: {syncMetrics.MaxDrift}ms (max: {syncMetrics.ToleranceMs}ms)");
            recommendations.Add("Re-sync audio and subtitle tracks");
        }

        if (subtitleMetrics.Status == "FAIL")
        {
            issues.Add($"Low subtitle readability: {subtitleMetrics.Readability:F1}");
            recommendations.Add("Increase subtitle font size or improve contrast");
        }
        else if (subtitleMetrics.Status == "WARNING")
        {
            recommendations.Add("Consider improving subtitle readability for better user experience");
        }

        if (deviceMetrics.Ios == "WARNING" || deviceMetrics.Android == "WARNING")
        {
            recommendations.Add("Optimize content for device safe zones");
        }

        // Determine overall status
        var hasFailures = new[] { audioMetrics.Status, syncMetrics.Status, subtitleMetrics.Status, videoMetrics.Status }
            .Any(s => s == "FAIL");

        var hasWarnings = new[] { audioMetrics.Status, syncMetrics.Status, subtitleMetrics.Status, videoMetrics.Status }
            .Any(s => s == "WARNING");

        var overallStatus = hasFailures ? "FAIL" : hasWarnings ? "WARNING" : "PASS";

        return new QualityReport
        {
            TitleId = titleId,
            OverallStatus = overallStatus,
            AudioLevels = audioMetrics,
            AvSync = syncMetrics,
            VideoQuality = videoMetrics,
            Subtitles = subtitleMetrics,
            Devices = deviceMetrics,
            Issues = issues,
            Recommendations = recommendations
        };
    }

    private async Task SaveQualityReportAsync(
        QualityReport report,
        string reportPath,
        CancellationToken cancellationToken)
    {
        var json = JsonSerializer.Serialize(report, new JsonSerializerOptions
        {
            WriteIndented = true
        });

        await File.WriteAllTextAsync(reportPath, json, cancellationToken);
    }
}
