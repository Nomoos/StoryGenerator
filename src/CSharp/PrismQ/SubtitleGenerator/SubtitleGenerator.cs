using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading;
using System.Threading.Tasks;
using StoryGenerator.Models;

namespace PrismQ.SubtitleGenerator
{
    /// <summary>
    /// Generates draft SRT subtitles from scripts.
    /// Saves as /subtitles/srt/{segment}/{age}/{title_id}_draft.srt
    /// </summary>
    public class SubtitleGenerator
    {
        private readonly string _subtitlesRootPath;
        private const int AverageWordsPerMinute = 150; // Average speaking rate
        private const int MaxCharsPerLine = 42; // SRT recommendation

        /// <summary>
        /// Creates a new subtitle generator.
        /// </summary>
        /// <param name="subtitlesRootPath">Root path for subtitles output (defaults to ./subtitles)</param>
        public SubtitleGenerator(string? subtitlesRootPath = null)
        {
            _subtitlesRootPath = subtitlesRootPath ?? Path.Combine(Directory.GetCurrentDirectory(), "subtitles");
        }

        /// <summary>
        /// Generates draft SRT subtitles from script text and saves to file.
        /// </summary>
        /// <param name="scriptText">The script text to convert to subtitles</param>
        /// <param name="titleId">The title ID for the story</param>
        /// <param name="segment">Audience segment (gender)</param>
        /// <param name="age">Age range</param>
        /// <param name="audioDuration">Optional total audio duration in seconds for better timing accuracy</param>
        /// <param name="cancellationToken">Cancellation token</param>
        /// <returns>Path to the saved SRT file</returns>
        public async Task<string> GenerateAndSaveSubtitlesAsync(
            string scriptText,
            string titleId,
            string segment,
            string age,
            float? audioDuration = null,
            CancellationToken cancellationToken = default)
        {
            if (string.IsNullOrWhiteSpace(scriptText))
                throw new ArgumentException("Script text cannot be empty", nameof(scriptText));
            if (string.IsNullOrWhiteSpace(titleId))
                throw new ArgumentException("Title ID cannot be empty", nameof(titleId));
            if (string.IsNullOrWhiteSpace(segment))
                throw new ArgumentException("Segment cannot be empty", nameof(segment));
            if (string.IsNullOrWhiteSpace(age))
                throw new ArgumentException("Age cannot be empty", nameof(age));

            // Generate SRT content
            var srtContent = GenerateSrtFromScript(scriptText, audioDuration);

            // Build output path: /subtitles/srt/{segment}/{age}/{title_id}_draft.srt
            var outputDir = Path.Combine(_subtitlesRootPath, "srt", segment, age);
            Directory.CreateDirectory(outputDir);

            var outputPath = Path.Combine(outputDir, $"{titleId}_draft.srt");

            // Save to file
            await File.WriteAllTextAsync(outputPath, srtContent, cancellationToken);

            return outputPath;
        }

        /// <summary>
        /// Generates draft SRT subtitles from script version.
        /// </summary>
        /// <param name="scriptVersion">The script version containing all metadata</param>
        /// <param name="audioDuration">Optional total audio duration in seconds</param>
        /// <param name="cancellationToken">Cancellation token</param>
        /// <returns>Path to the saved SRT file</returns>
        public async Task<string> GenerateFromScriptVersionAsync(
            ScriptVersion scriptVersion,
            float? audioDuration = null,
            CancellationToken cancellationToken = default)
        {
            if (scriptVersion == null)
                throw new ArgumentNullException(nameof(scriptVersion));

            return await GenerateAndSaveSubtitlesAsync(
                scriptVersion.Content,
                scriptVersion.TitleId,
                scriptVersion.TargetAudience.Gender,
                scriptVersion.TargetAudience.Age,
                audioDuration,
                cancellationToken
            );
        }

        /// <summary>
        /// Generates SRT content from script text.
        /// Creates time-aligned subtitle entries based on estimated word timing.
        /// </summary>
        /// <param name="scriptText">The script text</param>
        /// <param name="totalDuration">Optional total duration to calibrate timing</param>
        /// <returns>SRT formatted string</returns>
        private string GenerateSrtFromScript(string scriptText, float? totalDuration = null)
        {
            // Split script into sentences
            var sentences = SplitIntoSentences(scriptText);
            if (!sentences.Any())
                return string.Empty;

            // Calculate word count and timing
            var totalWords = sentences.Sum(s => CountWords(s));
            var wordsPerSecond = totalDuration.HasValue 
                ? totalWords / totalDuration.Value 
                : AverageWordsPerMinute / 60.0f;

            var srtBuilder = new StringBuilder();
            var currentTime = 0.0f;
            var subtitleIndex = 1;

            foreach (var sentence in sentences)
            {
                var words = CountWords(sentence);
                if (words == 0)
                    continue;

                var duration = words / wordsPerSecond;
                
                // Split long sentences into multiple subtitle entries
                var subtitleLines = SplitIntoSubtitleLines(sentence);
                
                foreach (var line in subtitleLines)
                {
                    var lineWords = CountWords(line);
                    var lineDuration = lineWords / wordsPerSecond;
                    
                    var startTime = FormatSrtTime(currentTime);
                    var endTime = FormatSrtTime(currentTime + lineDuration);

                    srtBuilder.AppendLine(subtitleIndex.ToString());
                    srtBuilder.AppendLine($"{startTime} --> {endTime}");
                    srtBuilder.AppendLine(line.Trim());
                    srtBuilder.AppendLine();

                    currentTime += lineDuration;
                    subtitleIndex++;
                }
            }

            return srtBuilder.ToString();
        }

        /// <summary>
        /// Splits text into sentences.
        /// </summary>
        private List<string> SplitIntoSentences(string text)
        {
            if (string.IsNullOrWhiteSpace(text))
                return new List<string>();

            // Clean and normalize text
            text = text.Replace("\r\n", " ").Replace("\n", " ").Replace("\r", " ");
            text = System.Text.RegularExpressions.Regex.Replace(text, @"\s+", " ").Trim();

            // Split by sentence-ending punctuation
            var sentences = System.Text.RegularExpressions.Regex.Split(text, @"(?<=[.!?])\s+");
            return sentences.Where(s => !string.IsNullOrWhiteSpace(s)).ToList();
        }

        /// <summary>
        /// Splits a sentence into subtitle lines respecting character limits.
        /// </summary>
        private List<string> SplitIntoSubtitleLines(string sentence)
        {
            var lines = new List<string>();
            
            if (sentence.Length <= MaxCharsPerLine)
            {
                lines.Add(sentence);
                return lines;
            }

            var words = sentence.Split(' ', StringSplitOptions.RemoveEmptyEntries);
            var currentLine = new StringBuilder();

            foreach (var word in words)
            {
                if (currentLine.Length + word.Length + 1 > MaxCharsPerLine && currentLine.Length > 0)
                {
                    lines.Add(currentLine.ToString().Trim());
                    currentLine.Clear();
                }

                if (currentLine.Length > 0)
                    currentLine.Append(' ');
                currentLine.Append(word);
            }

            if (currentLine.Length > 0)
                lines.Add(currentLine.ToString().Trim());

            return lines;
        }

        /// <summary>
        /// Counts words in a text string.
        /// </summary>
        private int CountWords(string text)
        {
            if (string.IsNullOrWhiteSpace(text))
                return 0;

            return text.Split(new[] { ' ', '\t', '\n', '\r' }, StringSplitOptions.RemoveEmptyEntries).Length;
        }

        /// <summary>
        /// Formats time in seconds to SRT timestamp format (HH:MM:SS,mmm).
        /// </summary>
        private string FormatSrtTime(float seconds)
        {
            var timeSpan = TimeSpan.FromSeconds(seconds);
            return $"{(int)timeSpan.TotalHours:D2}:{timeSpan.Minutes:D2}:{timeSpan.Seconds:D2},{timeSpan.Milliseconds:D3}";
        }
    }
}
