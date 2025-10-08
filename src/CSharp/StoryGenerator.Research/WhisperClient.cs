using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.IO;
using System.Linq;
using System.Text;
using System.Text.Json;
using System.Text.Json.Serialization;
using System.Threading;
using System.Threading.Tasks;

namespace StoryGenerator.Research
{
    /// <summary>
    /// Client for Whisper ASR (Automatic Speech Recognition).
    /// Uses subprocess to call Python faster-whisper implementation.
    /// </summary>
    public class WhisperClient : IWhisperClient
    {
        private readonly string _modelSize;
        private readonly string _device;
        private readonly string _computeType;
        private readonly string _pythonExecutable;
        private readonly string _scriptPath;

        /// <summary>
        /// Initialize Whisper client.
        /// </summary>
        /// <param name="modelSize">Model size ("tiny", "base", "small", "medium", "large-v2", "large-v3")</param>
        /// <param name="device">Device to use ("cpu", "cuda", "auto")</param>
        /// <param name="computeType">Computation type ("float16", "float32", "int8")</param>
        /// <param name="pythonExecutable">Path to Python executable (default: auto-detected)</param>
        /// <param name="scriptPath">Path to whisper_subprocess.py (default: auto-detected)</param>
        public WhisperClient(
            string modelSize = "large-v3",
            string device = "auto",
            string computeType = "float16",
            string pythonExecutable = null,
            string scriptPath = null)
        {
            _modelSize = modelSize;
            _device = device;
            _computeType = computeType;
            _pythonExecutable = pythonExecutable ?? GetDefaultPythonExecutable();
            _scriptPath = scriptPath ?? FindScriptPath();
        }

        /// <summary>
        /// Get default Python executable based on platform.
        /// </summary>
        private static string GetDefaultPythonExecutable()
        {
            // On Windows, Python is typically installed as "python"
            // On Linux/Mac, it's typically "python3"
            if (Environment.OSVersion.Platform == PlatformID.Win32NT)
            {
                return "python";
            }
            return "python3";
        }

        /// <summary>
        /// Find the whisper_subprocess.py script path.
        /// </summary>
        private string FindScriptPath()
        {
            // Try to find the script relative to the current directory
            var possiblePaths = new[]
            {
                "research/python/whisper_subprocess.py",
                Path.Combine("research", "python", "whisper_subprocess.py"),
                "../research/python/whisper_subprocess.py",
                Path.Combine("..", "research", "python", "whisper_subprocess.py"),
                "../../research/python/whisper_subprocess.py",
                Path.Combine("..", "..", "research", "python", "whisper_subprocess.py"),
                "../../../research/python/whisper_subprocess.py",
                Path.Combine("..", "..", "..", "research", "python", "whisper_subprocess.py")
            };

            foreach (var path in possiblePaths)
            {
                try
                {
                    if (File.Exists(path))
                    {
                        return Path.GetFullPath(path);
                    }
                }
                catch
                {
                    // Ignore path resolution errors and try next path
                    continue;
                }
            }

            throw new FileNotFoundException(
                "Could not find whisper_subprocess.py. " +
                "Please provide the script path in the constructor or ensure the script is in research/python/");
        }

        /// <summary>
        /// Transcribe audio file.
        /// </summary>
        /// <param name="audioPath">Path to audio file</param>
        /// <param name="language">Language code (e.g., "en", "es") or null for auto-detection</param>
        /// <param name="task">Task type ("transcribe" or "translate")</param>
        /// <param name="wordTimestamps">Include word-level timestamps</param>
        /// <param name="vadFilter">Apply voice activity detection filter</param>
        /// <param name="cancellationToken">Cancellation token</param>
        /// <returns>Transcription result</returns>
        public async Task<TranscriptionResult> TranscribeAsync(
            string audioPath,
            string language = null,
            string task = "transcribe",
            bool wordTimestamps = true,
            bool vadFilter = true,
            CancellationToken cancellationToken = default)
        {
            if (!File.Exists(audioPath))
            {
                throw new FileNotFoundException($"Audio file not found: {audioPath}");
            }

            // Build command arguments
            var args = new List<string>
            {
                _scriptPath,
                "transcribe",
                "--audio-path", audioPath,
                "--model-size", _modelSize,
                "--device", _device,
                "--compute-type", _computeType,
                "--task", task
            };

            if (!string.IsNullOrEmpty(language))
            {
                args.Add("--language");
                args.Add(language);
            }

            if (wordTimestamps)
            {
                args.Add("--word-timestamps");
            }
            else
            {
                args.Add("--no-word-timestamps");
            }

            if (vadFilter)
            {
                args.Add("--vad-filter");
            }
            else
            {
                args.Add("--no-vad-filter");
            }

            // Execute Python script
            var jsonResult = await ExecutePythonScriptAsync(args, cancellationToken);

            // Parse JSON result
            var jsonResponse = JsonSerializer.Deserialize<WhisperJsonResponse>(jsonResult);

            if (!jsonResponse.Success)
            {
                throw new Exception($"Whisper transcription failed: {jsonResponse.Error}");
            }

            // Convert to TranscriptionResult
            var result = new TranscriptionResult
            {
                Text = jsonResponse.Text,
                Language = jsonResponse.Language,
                LanguageProbability = jsonResponse.LanguageProbability,
                Segments = jsonResponse.Segments?.Select(s => new TranscriptionSegment
                {
                    Id = s.Id,
                    Start = s.Start,
                    End = s.End,
                    Text = s.Text,
                    Confidence = s.Confidence
                }).ToList() ?? new List<TranscriptionSegment>(),
                Words = jsonResponse.Words?.Select(w => new WordTimestamp
                {
                    Word = w.Word,
                    Start = w.Start,
                    End = w.End,
                    Confidence = w.Confidence
                }).ToList()
            };

            return result;
        }

        /// <summary>
        /// Transcribe audio and generate SRT subtitle file.
        /// </summary>
        /// <param name="audioPath">Path to audio file</param>
        /// <param name="outputPath">Path to save SRT file</param>
        /// <param name="language">Language code or null for auto-detection</param>
        /// <param name="maxWordsPerLine">Maximum words per subtitle line</param>
        /// <param name="cancellationToken">Cancellation token</param>
        /// <returns>SRT content as string</returns>
        public async Task<string> TranscribeToSrtAsync(
            string audioPath,
            string outputPath = null,
            string language = null,
            int maxWordsPerLine = 10,
            CancellationToken cancellationToken = default)
        {
            var result = await TranscribeAsync(
                audioPath,
                language,
                wordTimestamps: true,
                cancellationToken: cancellationToken);

            var srtContent = WordsToSrt(result.Words, maxWordsPerLine);

            if (!string.IsNullOrEmpty(outputPath))
            {
                await File.WriteAllTextAsync(outputPath, srtContent, Encoding.UTF8, cancellationToken);
            }

            return srtContent;
        }

        /// <summary>
        /// Transcribe audio and generate VTT subtitle file.
        /// </summary>
        /// <param name="audioPath">Path to audio file</param>
        /// <param name="outputPath">Path to save VTT file</param>
        /// <param name="language">Language code or null for auto-detection</param>
        /// <param name="maxWordsPerLine">Maximum words per subtitle line</param>
        /// <param name="cancellationToken">Cancellation token</param>
        /// <returns>VTT content as string</returns>
        public async Task<string> TranscribeToVttAsync(
            string audioPath,
            string outputPath = null,
            string language = null,
            int maxWordsPerLine = 10,
            CancellationToken cancellationToken = default)
        {
            var result = await TranscribeAsync(
                audioPath,
                language,
                wordTimestamps: true,
                cancellationToken: cancellationToken);

            var vttContent = WordsToVtt(result.Words, maxWordsPerLine);

            if (!string.IsNullOrEmpty(outputPath))
            {
                await File.WriteAllTextAsync(outputPath, vttContent, Encoding.UTF8, cancellationToken);
            }

            return vttContent;
        }

        /// <summary>
        /// Convert word timestamps to SRT format.
        /// </summary>
        /// <param name="words">List of word timestamps</param>
        /// <param name="maxWordsPerLine">Maximum words per subtitle line</param>
        /// <returns>SRT formatted string</returns>
        private string WordsToSrt(List<WordTimestamp> words, int maxWordsPerLine)
        {
            if (words == null || words.Count == 0)
            {
                return string.Empty;
            }

            var srtBuilder = new StringBuilder();
            var entryId = 1;

            for (int i = 0; i < words.Count; i += maxWordsPerLine)
            {
                var lineWords = words.Skip(i).Take(maxWordsPerLine).ToList();
                
                var startTime = lineWords.First().Start;
                var endTime = lineWords.Last().End;
                var text = string.Join(" ", lineWords.Select(w => w.Word.Trim()));

                srtBuilder.AppendLine(entryId.ToString());
                srtBuilder.AppendLine($"{FormatSrtTimestamp(startTime)} --> {FormatSrtTimestamp(endTime)}");
                srtBuilder.AppendLine(text);
                srtBuilder.AppendLine();

                entryId++;
            }

            return srtBuilder.ToString();
        }

        /// <summary>
        /// Convert word timestamps to VTT format.
        /// </summary>
        /// <param name="words">List of word timestamps</param>
        /// <param name="maxWordsPerLine">Maximum words per subtitle line</param>
        /// <returns>VTT formatted string</returns>
        private string WordsToVtt(List<WordTimestamp> words, int maxWordsPerLine)
        {
            if (words == null || words.Count == 0)
            {
                return "WEBVTT\n\n";
            }

            var vttBuilder = new StringBuilder();
            vttBuilder.AppendLine("WEBVTT");
            vttBuilder.AppendLine();

            for (int i = 0; i < words.Count; i += maxWordsPerLine)
            {
                var lineWords = words.Skip(i).Take(maxWordsPerLine).ToList();
                
                var startTime = lineWords.First().Start;
                var endTime = lineWords.Last().End;
                var text = string.Join(" ", lineWords.Select(w => w.Word.Trim()));

                vttBuilder.AppendLine($"{FormatVttTimestamp(startTime)} --> {FormatVttTimestamp(endTime)}");
                vttBuilder.AppendLine(text);
                vttBuilder.AppendLine();
            }

            return vttBuilder.ToString();
        }

        /// <summary>
        /// Format seconds as SRT timestamp (HH:MM:SS,mmm).
        /// </summary>
        private string FormatSrtTimestamp(double seconds)
        {
            var timeSpan = TimeSpan.FromSeconds(seconds);
            return $"{(int)timeSpan.TotalHours:D2}:{timeSpan.Minutes:D2}:{timeSpan.Seconds:D2},{timeSpan.Milliseconds:D3}";
        }

        /// <summary>
        /// Format seconds as VTT timestamp (HH:MM:SS.mmm).
        /// </summary>
        private string FormatVttTimestamp(double seconds)
        {
            var timeSpan = TimeSpan.FromSeconds(seconds);
            return $"{(int)timeSpan.TotalHours:D2}:{timeSpan.Minutes:D2}:{timeSpan.Seconds:D2}.{timeSpan.Milliseconds:D3}";
        }

        /// <summary>
        /// Detect the language of an audio file.
        /// </summary>
        /// <param name="audioPath">Path to audio file</param>
        /// <param name="cancellationToken">Cancellation token</param>
        /// <returns>Tuple of language code and confidence</returns>
        public async Task<(string Language, double Confidence)> DetectLanguageAsync(
            string audioPath,
            CancellationToken cancellationToken = default)
        {
            if (!File.Exists(audioPath))
            {
                throw new FileNotFoundException($"Audio file not found: {audioPath}");
            }

            // Build command arguments
            var args = new List<string>
            {
                _scriptPath,
                "detect_language",
                "--audio-path", audioPath,
                "--model-size", _modelSize,
                "--device", _device,
                "--compute-type", _computeType
            };

            // Execute Python script
            var jsonResult = await ExecutePythonScriptAsync(args, cancellationToken);

            // Parse JSON result
            var jsonResponse = JsonSerializer.Deserialize<LanguageDetectionResponse>(jsonResult);

            if (!jsonResponse.Success)
            {
                throw new Exception($"Language detection failed: {jsonResponse.Error}");
            }

            return (jsonResponse.Language, jsonResponse.Confidence);
        }

        /// <summary>
        /// Execute Python script and return output.
        /// </summary>
        private async Task<string> ExecutePythonScriptAsync(
            List<string> args,
            CancellationToken cancellationToken)
        {
            var startInfo = new ProcessStartInfo
            {
                FileName = _pythonExecutable,
                Arguments = string.Join(" ", args.Select(EscapeArgument)),
                RedirectStandardOutput = true,
                RedirectStandardError = true,
                UseShellExecute = false,
                CreateNoWindow = true
            };

            using var process = new Process { StartInfo = startInfo };
            var outputBuilder = new StringBuilder();
            var errorBuilder = new StringBuilder();

            process.OutputDataReceived += (sender, e) =>
            {
                if (e.Data != null)
                {
                    outputBuilder.AppendLine(e.Data);
                }
            };

            process.ErrorDataReceived += (sender, e) =>
            {
                if (e.Data != null)
                {
                    errorBuilder.AppendLine(e.Data);
                }
            };

            process.Start();
            process.BeginOutputReadLine();
            process.BeginErrorReadLine();

            await process.WaitForExitAsync(cancellationToken);

            if (process.ExitCode != 0)
            {
                var error = errorBuilder.ToString();
                throw new Exception($"Python script failed with exit code {process.ExitCode}: {error}");
            }

            return outputBuilder.ToString();
        }

        /// <summary>
        /// Escape command line argument for cross-platform compatibility.
        /// </summary>
        private string EscapeArgument(string arg)
        {
            if (string.IsNullOrEmpty(arg))
            {
                return "\"\"";
            }

            // No escaping needed if no special characters
            if (!arg.Contains(' ') && !arg.Contains('"') && !arg.Contains('\\'))
            {
                return arg;
            }

            // For Windows, handle backslashes and quotes properly
            if (Environment.OSVersion.Platform == PlatformID.Win32NT)
            {
                // Escape backslashes that precede quotes
                arg = arg.Replace("\\", "\\\\").Replace("\"", "\\\"");
                return $"\"{arg}\"";
            }

            // For Unix-like systems
            return $"\"{arg.Replace("\"", "\\\"")}\"";
        }

        /// <summary>
        /// Get list of available Whisper models.
        /// </summary>
        public async Task<List<string>> GetAvailableModelsAsync()
        {
            // Standard faster-whisper models
            return await Task.FromResult(new List<string>
            {
                "tiny",
                "tiny.en",
                "base",
                "base.en",
                "small",
                "small.en",
                "medium",
                "medium.en",
                "large-v1",
                "large-v2",
                "large-v3"
            });
        }
    }

    /// <summary>
    /// JSON response from Python whisper script.
    /// </summary>
    internal class WhisperJsonResponse
    {
        [JsonPropertyName("success")]
        public bool Success { get; set; }

        [JsonPropertyName("error")]
        public string Error { get; set; }

        [JsonPropertyName("text")]
        public string Text { get; set; }

        [JsonPropertyName("language")]
        public string Language { get; set; }

        [JsonPropertyName("languageProbability")]
        public double LanguageProbability { get; set; }

        [JsonPropertyName("segments")]
        public List<JsonSegment> Segments { get; set; }

        [JsonPropertyName("words")]
        public List<JsonWord> Words { get; set; }
    }

    /// <summary>
    /// JSON segment from Python response.
    /// </summary>
    internal class JsonSegment
    {
        [JsonPropertyName("id")]
        public int Id { get; set; }

        [JsonPropertyName("start")]
        public double Start { get; set; }

        [JsonPropertyName("end")]
        public double End { get; set; }

        [JsonPropertyName("text")]
        public string Text { get; set; }

        [JsonPropertyName("confidence")]
        public double? Confidence { get; set; }
    }

    /// <summary>
    /// JSON word from Python response.
    /// </summary>
    internal class JsonWord
    {
        [JsonPropertyName("word")]
        public string Word { get; set; }

        [JsonPropertyName("start")]
        public double Start { get; set; }

        [JsonPropertyName("end")]
        public double End { get; set; }

        [JsonPropertyName("confidence")]
        public double Confidence { get; set; }
    }

    /// <summary>
    /// Language detection JSON response.
    /// </summary>
    internal class LanguageDetectionResponse
    {
        [JsonPropertyName("success")]
        public bool Success { get; set; }

        [JsonPropertyName("error")]
        public string Error { get; set; }

        [JsonPropertyName("language")]
        public string Language { get; set; }

        [JsonPropertyName("confidence")]
        public double Confidence { get; set; }
    }
}
