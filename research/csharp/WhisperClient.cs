using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.IO;
using System.Linq;
using System.Text;
using System.Text.Json;
using System.Threading;
using System.Threading.Tasks;

namespace StoryGenerator.Research
{
    /// <summary>
    /// Client for Whisper ASR (Automatic Speech Recognition).
    /// Research prototype for local-only speech-to-text transcription.
    /// </summary>
    public class WhisperClient : IWhisperClient
    {
        private readonly string _modelSize;
        private readonly string _device;
        private readonly string _computeType;

        /// <summary>
        /// Initialize Whisper client.
        /// </summary>
        /// <param name="modelSize">Model size ("tiny", "base", "small", "medium", "large-v2", "large-v3")</param>
        /// <param name="device">Device to use ("cpu", "cuda", "auto")</param>
        /// <param name="computeType">Computation type ("float16", "float32", "int8")</param>
        public WhisperClient(
            string modelSize = "large-v2",
            string device = "auto",
            string computeType = "float16")
        {
            _modelSize = modelSize;
            _device = device;
            _computeType = computeType;
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

            // In a production implementation, this would call faster-whisper
            // For now, this is a stub showing the interface
            
            // Placeholder: Would call Python script or native whisper implementation
            var result = new TranscriptionResult
            {
                Text = "[Transcription would appear here]",
                Language = language ?? "en",
                LanguageProbability = 0.95,
                Segments = new List<TranscriptionSegment>(),
                Words = wordTimestamps ? new List<WordTimestamp>() : null
            };

            await Task.CompletedTask; // Placeholder for async operation
            
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
        /// Format seconds as SRT timestamp (HH:MM:SS,mmm).
        /// </summary>
        private string FormatSrtTimestamp(double seconds)
        {
            var timeSpan = TimeSpan.FromSeconds(seconds);
            return $"{(int)timeSpan.TotalHours:D2}:{timeSpan.Minutes:D2}:{timeSpan.Seconds:D2},{timeSpan.Milliseconds:D3}";
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
            var result = await TranscribeAsync(audioPath, null, cancellationToken: cancellationToken);
            return (result.Language, result.LanguageProbability);
        }
    }

    /// <summary>
    /// Represents a transcription result.
    /// </summary>
    public class TranscriptionResult
    {
        public string Text { get; set; }
        public string Language { get; set; }
        public double LanguageProbability { get; set; }
        public List<TranscriptionSegment> Segments { get; set; }
        public List<WordTimestamp> Words { get; set; }
    }

    /// <summary>
    /// Represents a transcription segment.
    /// </summary>
    public class TranscriptionSegment
    {
        public int Id { get; set; }
        public double Start { get; set; }
        public double End { get; set; }
        public string Text { get; set; }
        public double? Confidence { get; set; }
    }

    /// <summary>
    /// Represents a word with timestamp.
    /// </summary>
    public class WordTimestamp
    {
        public string Word { get; set; }
        public double Start { get; set; }
        public double End { get; set; }
        public double Confidence { get; set; }
    }
}
