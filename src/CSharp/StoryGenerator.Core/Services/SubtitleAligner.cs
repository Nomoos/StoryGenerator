using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text;
using System.Text.Json;
using System.Threading;
using System.Threading.Tasks;
using StoryGenerator.Core.Interfaces;
using StoryGenerator.Core.Models;

namespace StoryGenerator.Core.Services
{
    /// <summary>
    /// Service for aligning subtitles to audio using faster-whisper and mapping them to shots.
    /// Implements forced alignment with word-level timestamps for precise subtitle synchronization.
    /// </summary>
    public class SubtitleAligner : ISubtitleAligner
    {
        private readonly StoryGenerator.Research.IWhisperClient _whisperClient;

        /// <summary>
        /// Initializes a new instance of the SubtitleAligner class.
        /// </summary>
        /// <param name="whisperClient">Whisper client for speech recognition.</param>
        public SubtitleAligner(StoryGenerator.Research.IWhisperClient whisperClient)
        {
            _whisperClient = whisperClient ?? throw new ArgumentNullException(nameof(whisperClient));
        }

        /// <summary>
        /// Generates aligned subtitles from audio file using forced alignment.
        /// </summary>
        public async Task<string> GenerateAlignedSubtitlesAsync(
            string audioPath,
            string? language = null,
            int maxWordsPerLine = 10,
            CancellationToken cancellationToken = default)
        {
            if (string.IsNullOrEmpty(audioPath))
                throw new ArgumentException("Audio path cannot be null or empty.", nameof(audioPath));

            if (!File.Exists(audioPath))
                throw new FileNotFoundException($"Audio file not found: {audioPath}");

            // Use the WhisperClient to generate SRT with word timestamps
            var srtContent = await _whisperClient.TranscribeToSrtAsync(
                audioPath,
                outputPath: null, // Don't save yet, just return content
                language: language,
                maxWordsPerLine: maxWordsPerLine,
                cancellationToken: cancellationToken);

            return srtContent;
        }

        /// <summary>
        /// Generates aligned SRT file and saves it to the specified path.
        /// </summary>
        public async Task<string> GenerateAndSaveSrtAsync(
            string audioPath,
            string outputPath,
            string? language = null,
            int maxWordsPerLine = 10,
            CancellationToken cancellationToken = default)
        {
            if (string.IsNullOrEmpty(outputPath))
                throw new ArgumentException("Output path cannot be null or empty.", nameof(outputPath));

            // Ensure output directory exists
            var outputDir = Path.GetDirectoryName(outputPath);
            if (!string.IsNullOrEmpty(outputDir) && !Directory.Exists(outputDir))
            {
                Directory.CreateDirectory(outputDir);
            }

            // Generate and save SRT using WhisperClient
            var srtContent = await _whisperClient.TranscribeToSrtAsync(
                audioPath,
                outputPath: outputPath,
                language: language,
                maxWordsPerLine: maxWordsPerLine,
                cancellationToken: cancellationToken);

            return outputPath;
        }

        /// <summary>
        /// Generates aligned VTT file and saves it to the specified path.
        /// </summary>
        public async Task<string> GenerateAndSaveVttAsync(
            string audioPath,
            string outputPath,
            string? language = null,
            int maxWordsPerLine = 10,
            CancellationToken cancellationToken = default)
        {
            if (string.IsNullOrEmpty(outputPath))
                throw new ArgumentException("Output path cannot be null or empty.", nameof(outputPath));

            // Ensure output directory exists
            var outputDir = Path.GetDirectoryName(outputPath);
            if (!string.IsNullOrEmpty(outputDir) && !Directory.Exists(outputDir))
            {
                Directory.CreateDirectory(outputDir);
            }

            // Generate and save VTT using WhisperClient
            var vttContent = await _whisperClient.TranscribeToVttAsync(
                audioPath,
                outputPath: outputPath,
                language: language,
                maxWordsPerLine: maxWordsPerLine,
                cancellationToken: cancellationToken);

            return outputPath;
        }

        /// <summary>
        /// Maps subtitle time ranges to shot IDs from a shotlist.
        /// </summary>
        public async Task<SubtitleToShotMapping> MapSubtitlesToShotsAsync(
            string audioPath,
            Shotlist shotlist,
            string titleId,
            string? language = null,
            int maxWordsPerLine = 10,
            CancellationToken cancellationToken = default)
        {
            if (string.IsNullOrEmpty(audioPath))
                throw new ArgumentException("Audio path cannot be null or empty.", nameof(audioPath));

            if (shotlist == null)
                throw new ArgumentNullException(nameof(shotlist));

            if (string.IsNullOrEmpty(titleId))
                throw new ArgumentException("Title ID cannot be null or empty.", nameof(titleId));

            if (!File.Exists(audioPath))
                throw new FileNotFoundException($"Audio file not found: {audioPath}");

            // Get transcription with word timestamps
            var transcription = await _whisperClient.TranscribeAsync(
                audioPath,
                language: language,
                wordTimestamps: true,
                cancellationToken: cancellationToken);

            if (transcription.Words == null || transcription.Words.Count == 0)
                throw new InvalidOperationException("Transcription did not return word timestamps.");

            // Create subtitle entries from words
            var subtitleEntries = new List<SubtitleEntry>();
            var subtitleIndex = 1;

            for (int i = 0; i < transcription.Words.Count; i += maxWordsPerLine)
            {
                var lineWords = transcription.Words.Skip(i).Take(maxWordsPerLine).ToList();
                
                if (lineWords.Count == 0)
                    continue;

                var startTime = lineWords.First().Start;
                var endTime = lineWords.Last().End;
                var text = string.Join(" ", lineWords.Select(w => w.Word.Trim()));

                // Find which shot this subtitle belongs to
                var shotNumber = FindShotForTime(shotlist, startTime, endTime);

                var entry = new SubtitleEntry
                {
                    SubtitleIndex = subtitleIndex++,
                    Text = text,
                    StartTime = startTime,
                    EndTime = endTime,
                    ShotNumber = shotNumber,
                    Words = lineWords.Select(w => new SubtitleWord
                    {
                        Word = w.Word,
                        Start = w.Start,
                        End = w.End,
                        Confidence = w.Confidence
                    }).ToList()
                };

                subtitleEntries.Add(entry);
            }

            var mapping = new SubtitleToShotMapping
            {
                TitleId = titleId,
                TotalDuration = transcription.Words.Max(w => w.End),
                SubtitleMappings = subtitleEntries
            };

            return mapping;
        }

        /// <summary>
        /// Maps subtitle time ranges to shot IDs and saves the mapping as JSON.
        /// </summary>
        public async Task<string> MapAndSaveSubtitlesToShotsAsync(
            string audioPath,
            Shotlist shotlist,
            string titleId,
            string outputPath,
            string? language = null,
            int maxWordsPerLine = 10,
            CancellationToken cancellationToken = default)
        {
            if (string.IsNullOrEmpty(outputPath))
                throw new ArgumentException("Output path cannot be null or empty.", nameof(outputPath));

            // Generate the mapping
            var mapping = await MapSubtitlesToShotsAsync(
                audioPath,
                shotlist,
                titleId,
                language,
                maxWordsPerLine,
                cancellationToken);

            // Ensure output directory exists
            var outputDir = Path.GetDirectoryName(outputPath);
            if (!string.IsNullOrEmpty(outputDir) && !Directory.Exists(outputDir))
            {
                Directory.CreateDirectory(outputDir);
            }

            // Serialize to JSON and save
            var options = new JsonSerializerOptions
            {
                WriteIndented = true,
                PropertyNamingPolicy = JsonNamingPolicy.CamelCase
            };

            var json = JsonSerializer.Serialize(mapping, options);
            await File.WriteAllTextAsync(outputPath, json, Encoding.UTF8, cancellationToken);

            return outputPath;
        }

        /// <summary>
        /// Finds the shot number that contains the given time range.
        /// </summary>
        /// <param name="shotlist">The shotlist to search.</param>
        /// <param name="startTime">The start time of the subtitle.</param>
        /// <param name="endTime">The end time of the subtitle.</param>
        /// <returns>The shot number, or -1 if no shot is found.</returns>
        private int FindShotForTime(Shotlist shotlist, double startTime, double endTime)
        {
            if (shotlist.Shots == null || shotlist.Shots.Count == 0)
                return -1;

            // Use the midpoint of the subtitle to determine which shot it belongs to
            var midTime = (startTime + endTime) / 2.0;

            foreach (var shot in shotlist.Shots)
            {
                if (midTime >= shot.StartTime && midTime <= shot.EndTime)
                {
                    return shot.ShotNumber;
                }
            }

            // If not found by midpoint, find the shot with the most overlap
            var maxOverlap = 0.0;
            var bestShotNumber = -1;

            foreach (var shot in shotlist.Shots)
            {
                var overlapStart = Math.Max(startTime, shot.StartTime);
                var overlapEnd = Math.Min(endTime, shot.EndTime);
                var overlap = overlapEnd - overlapStart;

                if (overlap > maxOverlap)
                {
                    maxOverlap = overlap;
                    bestShotNumber = shot.ShotNumber;
                }
            }

            return bestShotNumber;
        }
    }
}
