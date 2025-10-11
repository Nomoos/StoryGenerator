using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.IO;
using System.Linq;
using System.Threading.Tasks;
using StoryGenerator.Pipeline.Config;

namespace StoryGenerator.Pipeline.Services;

/// <summary>
/// Service for composing the final video with clips, audio, and subtitles using FFmpeg.
/// </summary>
public class VideoCompositionService
{
    private readonly PathsConfig _paths;
    private readonly VideoConfig _videoConfig;

    public VideoCompositionService(PathsConfig paths, VideoConfig videoConfig)
    {
        _paths = paths ?? throw new ArgumentNullException(nameof(paths));
        _videoConfig = videoConfig ?? throw new ArgumentNullException(nameof(videoConfig));
    }

    /// <summary>
    /// Compose final video from clips, audio, and subtitles.
    /// </summary>
    /// <param name="storyTitle">The story title</param>
    /// <param name="clipPaths">List of video clip paths</param>
    /// <returns>Path to the final composed video</returns>
    public async Task<string> ComposeVideoAsync(string storyTitle, List<string> clipPaths)
    {
        Console.WriteLine($"Composing final video for: {storyTitle}");

        if (clipPaths == null || clipPaths.Count == 0)
        {
            throw new ArgumentException("No video clips provided for composition");
        }

        // Get audio and subtitle paths
        var audioPath = Path.Combine(_paths.StoryRoot, _paths.Voiceover, $"{storyTitle}.mp3");
        var subtitlePath = Path.Combine(_paths.StoryRoot, _paths.Titles, $"{storyTitle}.srt");

        if (!File.Exists(audioPath))
        {
            throw new FileNotFoundException($"Audio file not found: {audioPath}");
        }

        // Create final output directory
        var finalDir = Path.Combine(_paths.StoryRoot, _paths.Final, storyTitle);
        Directory.CreateDirectory(finalDir);

        var outputPath = Path.Combine(finalDir, $"{storyTitle}.mp4");

        // Step 1: Concatenate video clips
        var concatenatedPath = Path.Combine(Path.GetTempPath(), $"{storyTitle}_concat.mp4");
        await ConcatenateClipsAsync(clipPaths, concatenatedPath);

        // Step 2: Add audio
        var withAudioPath = Path.Combine(Path.GetTempPath(), $"{storyTitle}_with_audio.mp4");
        await AddAudioAsync(concatenatedPath, audioPath, withAudioPath);

        // Step 3: Add subtitles if available
        if (File.Exists(subtitlePath))
        {
            await AddSubtitlesAsync(withAudioPath, subtitlePath, outputPath);
        }
        else
        {
            // No subtitles, just copy the video with audio
            File.Copy(withAudioPath, outputPath, true);
        }

        // Cleanup temporary files
        CleanupTempFiles(concatenatedPath, withAudioPath);

        Console.WriteLine($"✅ Final video composed: {outputPath}");
        return outputPath;
    }

    private async Task ConcatenateClipsAsync(List<string> clipPaths, string outputPath)
    {
        Console.WriteLine($"  Concatenating {clipPaths.Count} clips...");

        // Create file list for FFmpeg concat
        var fileListPath = Path.Combine(Path.GetTempPath(), $"filelist_{Guid.NewGuid()}.txt");
        var fileListContent = clipPaths.Select(p => $"file '{p.Replace("\\", "/")}'").ToList();
        await File.WriteAllLinesAsync(fileListPath, fileListContent);

        try
        {
            var args = $"-f concat -safe 0 -i \"{fileListPath}\" " +
                       $"-c copy \"{outputPath}\"";

            await RunFFmpegAsync(args);
        }
        finally
        {
            if (File.Exists(fileListPath))
            {
                File.Delete(fileListPath);
            }
        }
    }

    private async Task AddAudioAsync(string videoPath, string audioPath, string outputPath)
    {
        Console.WriteLine("  Adding audio track...");

        var args = $"-i \"{videoPath}\" -i \"{audioPath}\" " +
                   $"-map 0:v:0 -map 1:a:0 " +
                   $"-c:v copy -c:a {_videoConfig.AudioCodec} " +
                   $"-shortest \"{outputPath}\"";

        await RunFFmpegAsync(args);
    }

    private async Task AddSubtitlesAsync(string videoPath, string subtitlePath, string outputPath)
    {
        Console.WriteLine("  Adding subtitles...");

        // Convert SRT to ASS for better styling (optional, but recommended for vertical videos)
        var args = $"-i \"{videoPath}\" " +
                   $"-vf \"subtitles='{subtitlePath.Replace("\\", "/")}':force_style='Fontsize=24,PrimaryColour=&H00FFFFFF,OutlineColour=&H00000000,BorderStyle=3,Outline=2,Shadow=0,Alignment=10'\" " +
                   $"-c:a copy \"{outputPath}\"";

        await RunFFmpegAsync(args);
    }

    private async Task RunFFmpegAsync(string arguments)
    {
        var processInfo = new ProcessStartInfo
        {
            FileName = "ffmpeg",
            Arguments = $"-y {arguments}", // -y to overwrite files
            RedirectStandardOutput = true,
            RedirectStandardError = true,
            UseShellExecute = false,
            CreateNoWindow = true
        };

        using var process = Process.Start(processInfo);
        if (process == null)
        {
            throw new InvalidOperationException("Failed to start FFmpeg process");
        }

        var output = await process.StandardOutput.ReadToEndAsync();
        var error = await process.StandardError.ReadToEndAsync();

        await process.WaitForExitAsync();

        if (process.ExitCode != 0)
        {
            Console.WriteLine($"FFmpeg Error: {error}");
            throw new InvalidOperationException($"FFmpeg failed with exit code {process.ExitCode}");
        }
    }

    private void CleanupTempFiles(params string[] paths)
    {
        foreach (var path in paths)
        {
            try
            {
                if (File.Exists(path))
                {
                    File.Delete(path);
                }
            }
            catch (Exception ex)
            {
                Console.WriteLine($"  ⚠️ Failed to delete temp file {path}: {ex.Message}");
            }
        }
    }
}
