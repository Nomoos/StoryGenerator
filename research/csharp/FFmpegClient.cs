using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.IO;
using System.Text;
using System.Text.Json;
using System.Threading;
using System.Threading.Tasks;

namespace StoryGenerator.Research
{
    /// <summary>
    /// Client for FFmpeg media processing operations.
    /// Research prototype for audio/video manipulation.
    /// </summary>
    public class FFmpegClient
    {
        private readonly string _ffmpegPath;
        private readonly string _ffprobePath;

        /// <summary>
        /// Initialize FFmpeg client.
        /// </summary>
        /// <param name="ffmpegPath">Path to ffmpeg executable (defaults to "ffmpeg" in PATH)</param>
        /// <param name="ffprobePath">Path to ffprobe executable (defaults to "ffprobe" in PATH)</param>
        public FFmpegClient(string ffmpegPath = "ffmpeg", string ffprobePath = "ffprobe")
        {
            _ffmpegPath = ffmpegPath;
            _ffprobePath = ffprobePath;
        }

        /// <summary>
        /// Normalize audio to target LUFS using loudnorm filter.
        /// </summary>
        /// <param name="inputPath">Input audio file path</param>
        /// <param name="outputPath">Output audio file path</param>
        /// <param name="targetLufs">Target integrated loudness in LUFS (typically -14 to -16)</param>
        /// <param name="targetLra">Target loudness range in LU</param>
        /// <param name="targetTp">Target true peak in dBTP</param>
        /// <param name="twoPass">Use two-pass normalization for better accuracy</param>
        /// <param name="sampleRate">Output sample rate in Hz</param>
        /// <param name="cancellationToken">Cancellation token</param>
        /// <returns>Normalization result with metrics</returns>
        public async Task<NormalizationResult> NormalizeAudioAsync(
            string inputPath,
            string outputPath,
            double targetLufs = -14.0,
            double targetLra = 7.0,
            double targetTp = -1.0,
            bool twoPass = true,
            int sampleRate = 48000,
            CancellationToken cancellationToken = default)
        {
            if (!File.Exists(inputPath))
            {
                throw new FileNotFoundException($"Input file not found: {inputPath}");
            }

            if (twoPass)
            {
                return await NormalizeAudioTwoPassAsync(
                    inputPath, outputPath, targetLufs, targetLra, targetTp, sampleRate, cancellationToken);
            }
            else
            {
                return await NormalizeAudioSinglePassAsync(
                    inputPath, outputPath, targetLufs, targetLra, targetTp, sampleRate, cancellationToken);
            }
        }

        /// <summary>
        /// Single-pass audio normalization (faster but less accurate).
        /// </summary>
        private async Task<NormalizationResult> NormalizeAudioSinglePassAsync(
            string inputPath,
            string outputPath,
            double targetLufs,
            double targetLra,
            double targetTp,
            int sampleRate,
            CancellationToken cancellationToken)
        {
            var arguments = $"-y -i \"{inputPath}\" " +
                $"-af \"loudnorm=I={targetLufs}:LRA={targetLra}:TP={targetTp}\" " +
                $"-ar {sampleRate} \"{outputPath}\"";

            await ExecuteFFmpegAsync(arguments, cancellationToken);

            return new NormalizationResult
            {
                Success = true,
                Method = "single_pass",
                OutputPath = outputPath
            };
        }

        /// <summary>
        /// Two-pass audio normalization for accurate results.
        /// </summary>
        private async Task<NormalizationResult> NormalizeAudioTwoPassAsync(
            string inputPath,
            string outputPath,
            double targetLufs,
            double targetLra,
            double targetTp,
            int sampleRate,
            CancellationToken cancellationToken)
        {
            // First pass: measure
            var measurements = await MeasureLoudnessAsync(
                inputPath, targetLufs, targetLra, targetTp, cancellationToken);

            // Second pass: normalize with measurements
            var arguments = $"-y -i \"{inputPath}\" " +
                $"-af \"loudnorm=I={targetLufs}:LRA={targetLra}:TP={targetTp}:" +
                $"measured_I={measurements.InputI}:" +
                $"measured_LRA={measurements.InputLra}:" +
                $"measured_TP={measurements.InputTp}:" +
                $"measured_thresh={measurements.InputThresh}:" +
                $"offset={measurements.TargetOffset}:" +
                $"linear=true:print_format=json\" " +
                $"-ar {sampleRate} \"{outputPath}\"";

            await ExecuteFFmpegAsync(arguments, cancellationToken);

            return new NormalizationResult
            {
                Success = true,
                Method = "two_pass",
                OutputPath = outputPath,
                Measurements = measurements
            };
        }

        /// <summary>
        /// Measure audio loudness using FFmpeg loudnorm filter.
        /// </summary>
        private async Task<LoudnessMeasurements> MeasureLoudnessAsync(
            string audioPath,
            double targetLufs,
            double targetLra,
            double targetTp,
            CancellationToken cancellationToken)
        {
            var arguments = $"-i \"{audioPath}\" " +
                $"-af \"loudnorm=I={targetLufs}:LRA={targetLra}:TP={targetTp}:print_format=json\" " +
                "-f null -";

            var output = await ExecuteFFmpegAsync(arguments, cancellationToken, captureStderr: true);

            // Parse JSON from stderr output
            var jsonStart = output.LastIndexOf('{');
            var jsonEnd = output.LastIndexOf('}') + 1;

            if (jsonStart == -1 || jsonEnd <= jsonStart)
            {
                throw new Exception("Could not find JSON output in FFmpeg response");
            }

            var jsonStr = output.Substring(jsonStart, jsonEnd - jsonStart);
            var measurements = JsonSerializer.Deserialize<LoudnessMeasurements>(jsonStr);

            return measurements;
        }

        /// <summary>
        /// Get audio file information using FFprobe.
        /// </summary>
        /// <param name="audioPath">Path to audio file</param>
        /// <param name="cancellationToken">Cancellation token</param>
        /// <returns>Audio file information</returns>
        public async Task<AudioInfo> GetAudioInfoAsync(
            string audioPath,
            CancellationToken cancellationToken = default)
        {
            if (!File.Exists(audioPath))
            {
                throw new FileNotFoundException($"Audio file not found: {audioPath}");
            }

            var arguments = $"-v quiet -print_format json -show_format -show_streams \"{audioPath}\"";

            var output = await ExecuteFFprobeAsync(arguments, cancellationToken);
            
            // Parse JSON output
            using var doc = JsonDocument.Parse(output);
            var root = doc.RootElement;

            // Find audio stream
            var streams = root.GetProperty("streams");
            JsonElement? audioStream = null;

            foreach (var stream in streams.EnumerateArray())
            {
                if (stream.GetProperty("codec_type").GetString() == "audio")
                {
                    audioStream = stream;
                    break;
                }
            }

            if (!audioStream.HasValue)
            {
                throw new Exception("No audio stream found in file");
            }

            var format = root.GetProperty("format");

            return new AudioInfo
            {
                Duration = double.Parse(format.GetProperty("duration").GetString()),
                SampleRate = audioStream.Value.GetProperty("sample_rate").GetInt32(),
                Channels = audioStream.Value.GetProperty("channels").GetInt32(),
                Codec = audioStream.Value.GetProperty("codec_name").GetString(),
                BitRate = audioStream.Value.TryGetProperty("bit_rate", out var br) 
                    ? int.Parse(br.GetString()) 
                    : 0
            };
        }

        /// <summary>
        /// Extract audio from video file.
        /// </summary>
        /// <param name="videoPath">Input video file path</param>
        /// <param name="audioPath">Output audio file path</param>
        /// <param name="codec">Audio codec (e.g., "mp3", "aac", "wav")</param>
        /// <param name="bitrate">Audio bitrate (e.g., "192k")</param>
        /// <param name="cancellationToken">Cancellation token</param>
        public async Task ExtractAudioAsync(
            string videoPath,
            string audioPath,
            string codec = "mp3",
            string bitrate = "192k",
            CancellationToken cancellationToken = default)
        {
            var arguments = $"-y -i \"{videoPath}\" -vn -acodec {codec} -b:a {bitrate} \"{audioPath}\"";
            await ExecuteFFmpegAsync(arguments, cancellationToken);
        }

        /// <summary>
        /// Convert video to different format.
        /// </summary>
        /// <param name="inputPath">Input video file path</param>
        /// <param name="outputPath">Output video file path</param>
        /// <param name="codec">Video codec (e.g., "libx264", "libx265")</param>
        /// <param name="preset">Encoding preset (e.g., "medium", "fast")</param>
        /// <param name="crf">Constant Rate Factor (0-51, lower = better quality)</param>
        /// <param name="cancellationToken">Cancellation token</param>
        public async Task ConvertVideoAsync(
            string inputPath,
            string outputPath,
            string codec = "libx264",
            string preset = "medium",
            int crf = 23,
            CancellationToken cancellationToken = default)
        {
            var arguments = $"-y -i \"{inputPath}\" -c:v {codec} -preset {preset} -crf {crf} -c:a copy \"{outputPath}\"";
            await ExecuteFFmpegAsync(arguments, cancellationToken);
        }

        /// <summary>
        /// Execute FFmpeg command.
        /// </summary>
        private async Task<string> ExecuteFFmpegAsync(
            string arguments,
            CancellationToken cancellationToken,
            bool captureStderr = false)
        {
            return await ExecuteProcessAsync(_ffmpegPath, arguments, cancellationToken, captureStderr);
        }

        /// <summary>
        /// Execute FFprobe command.
        /// </summary>
        private async Task<string> ExecuteFFprobeAsync(
            string arguments,
            CancellationToken cancellationToken)
        {
            return await ExecuteProcessAsync(_ffprobePath, arguments, cancellationToken);
        }

        /// <summary>
        /// Execute a process and capture output.
        /// </summary>
        private async Task<string> ExecuteProcessAsync(
            string fileName,
            string arguments,
            CancellationToken cancellationToken,
            bool captureStderr = false)
        {
            var startInfo = new ProcessStartInfo
            {
                FileName = fileName,
                Arguments = arguments,
                RedirectStandardOutput = true,
                RedirectStandardError = true,
                UseShellExecute = false,
                CreateNoWindow = true
            };

            using var process = new Process { StartInfo = startInfo };

            try
            {
                process.Start();

                var outputTask = process.StandardOutput.ReadToEndAsync();
                var errorTask = process.StandardError.ReadToEndAsync();

                await process.WaitForExitAsync(cancellationToken);

                var output = await outputTask;
                var error = await errorTask;

                if (process.ExitCode != 0 && !captureStderr)
                {
                    throw new Exception($"{fileName} error: {error}");
                }

                return captureStderr ? error : output;
            }
            catch (Exception ex)
            {
                throw new Exception($"Failed to execute {fileName}: {ex.Message}", ex);
            }
        }
    }

    /// <summary>
    /// Represents audio normalization result.
    /// </summary>
    public class NormalizationResult
    {
        public bool Success { get; set; }
        public string Method { get; set; }
        public string OutputPath { get; set; }
        public LoudnessMeasurements Measurements { get; set; }
    }

    /// <summary>
    /// Represents loudness measurements.
    /// </summary>
    public class LoudnessMeasurements
    {
        [JsonPropertyName("input_i")]
        public string InputI { get; set; }

        [JsonPropertyName("input_lra")]
        public string InputLra { get; set; }

        [JsonPropertyName("input_tp")]
        public string InputTp { get; set; }

        [JsonPropertyName("input_thresh")]
        public string InputThresh { get; set; }

        [JsonPropertyName("target_offset")]
        public string TargetOffset { get; set; }
    }

    /// <summary>
    /// Represents audio file information.
    /// </summary>
    public class AudioInfo
    {
        public double Duration { get; set; }
        public int SampleRate { get; set; }
        public int Channels { get; set; }
        public string Codec { get; set; }
        public int BitRate { get; set; }
    }
}
