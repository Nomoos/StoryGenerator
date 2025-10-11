using System.Text;
using System.Text.RegularExpressions;
using Microsoft.Extensions.Logging;
using PrismQ.Shared.Core.Services;
using PrismQ.Shared.Core;
using StoryGenerator.Providers.OpenAI;

namespace PrismQ.SubtitleGenerator;

/// <summary>
/// Generates word-level SRT subtitles by aligning scripts with audio.
/// Ported from Python Generators/GTitles.py with OpenAI Whisper integration.
/// </summary>
public class SubtitleGenerator : ISubtitleGenerator
{
    private readonly OpenAIClient _openAIClient;
    private readonly ILogger<SubtitleGenerator> _logger;
    private readonly PerformanceMonitor _performanceMonitor;

    public string Name => "SubtitleGenerator";
    public string Version => "1.0.0";

    public SubtitleGenerator(
        OpenAIClient openAIClient,
        ILogger<SubtitleGenerator> logger,
        PerformanceMonitor performanceMonitor)
    {
        _openAIClient = openAIClient;
        _logger = logger;
        _performanceMonitor = performanceMonitor;
    }

    public async Task<SubtitleGenerationResult> GenerateSubtitlesAsync(
        string audioPath,
        string scriptPath,
        string outputSrtPath,
        CancellationToken cancellationToken = default)
    {
        return await _performanceMonitor.MeasureAsync(
            "Subtitle_Generation",
            Path.GetFileNameWithoutExtension(audioPath),
            async () => await GenerateSubtitlesInternalAsync(audioPath, scriptPath, outputSrtPath, cancellationToken),
            new Dictionary<string, object>
            {
                { "audio_path", audioPath },
                { "script_path", scriptPath }
            });
    }

    private async Task<SubtitleGenerationResult> GenerateSubtitlesInternalAsync(
        string audioPath,
        string scriptPath,
        string outputSrtPath,
        CancellationToken cancellationToken)
    {
        _logger.LogInformation("🎧 Generating subtitles for audio: {AudioPath}", audioPath);

        // Read the script
        var scriptText = await File.ReadAllTextAsync(scriptPath, cancellationToken);
        var scriptWords = NormalizeText(scriptText);

        _logger.LogInformation("Transcribing audio with OpenAI Whisper...");
        
        // Transcribe audio with word-level timestamps
        var transcription = await _openAIClient.TranscribeAudioAsync(
            audioPath,
            language: "en",
            timestampGranularity: "word",
            cancellationToken: cancellationToken);

        if (transcription.Words == null || transcription.Words.Count == 0)
        {
            throw new InvalidOperationException("No word-level timestamps returned from Whisper API");
        }

        _logger.LogInformation("✅ Transcription completed. Duration: {Duration}s, Words: {WordCount}",
            transcription.Duration, transcription.Words.Count);

        // Normalize transcribed words
        var spokenWords = transcription.Words
            .Select(w => new SpokenWord
            {
                Original = w.Word.Trim(),
                Normalized = NormalizeWord(w.Word),
                Start = w.Start,
                End = w.End
            })
            .ToList();

        var spokenClean = spokenWords.Select(w => w.Normalized).ToList();

        // Align script words with spoken words using sequence matching
        var alignedSegments = AlignWordsWithTimestamps(scriptWords, spokenWords, spokenClean);

        // Calculate alignment accuracy
        var estimatedCount = alignedSegments.Count(s => s.Start == s.End);
        var accuracy = estimatedCount == 0 ? 100.0 : 
            ((alignedSegments.Count - estimatedCount) / (double)alignedSegments.Count) * 100.0;

        _logger.LogInformation("🧾 Estimated {EstimatedCount} timestamps out of {TotalCount} words. Accuracy: {Accuracy:F1}%",
            estimatedCount, alignedSegments.Count, accuracy);

        // Export to SRT format
        await ExportWordLevelSrtAsync(alignedSegments, outputSrtPath, cancellationToken);

        _logger.LogInformation("✅ Subtitles saved to: {OutputPath}", outputSrtPath);

        return new SubtitleGenerationResult
        {
            SrtFilePath = outputSrtPath,
            WordCount = alignedSegments.Count,
            AlignmentAccuracy = accuracy,
            AudioDuration = transcription.Duration
        };
    }

    public async Task<SubtitleGenerationResult> GenerateSubtitlesForStoryAsync(
        string storyFolderPath,
        string storyTitle,
        CancellationToken cancellationToken = default)
    {
        var audioPath = Path.Combine(storyFolderPath, "voiceover_normalized.mp3");
        var scriptPath = Path.Combine(storyFolderPath, "Revised.txt");
        var outputPath = Path.Combine(storyFolderPath, "subtitles_wbw.srt");

        if (!File.Exists(audioPath))
        {
            throw new FileNotFoundException($"Audio file not found: {audioPath}");
        }

        if (!File.Exists(scriptPath))
        {
            throw new FileNotFoundException($"Script file not found: {scriptPath}");
        }

        return await GenerateSubtitlesAsync(audioPath, scriptPath, outputPath, cancellationToken);
    }

    /// <summary>
    /// Aligns script words with spoken words using sequence matching algorithm.
    /// </summary>
    private List<WordSegment> AlignWordsWithTimestamps(
        List<string> scriptWords,
        List<SpokenWord> spokenWords,
        List<string> spokenClean)
    {
        var segments = new List<WordSegment>();
        
        // Use a simple greedy matching algorithm
        // For each script word, find the closest matching spoken word
        int spokenIndex = 0;
        
        for (int scriptIndex = 0; scriptIndex < scriptWords.Count; scriptIndex++)
        {
            var scriptWord = scriptWords[scriptIndex];
            
            // Try to find exact match in remaining spoken words
            bool foundMatch = false;
            for (int i = spokenIndex; i < spokenClean.Count && i < spokenIndex + 5; i++)
            {
                if (spokenClean[i] == scriptWord)
                {
                    segments.Add(new WordSegment
                    {
                        Word = scriptWord,
                        Start = spokenWords[i].Start,
                        End = spokenWords[i].End
                    });
                    spokenIndex = i + 1;
                    foundMatch = true;
                    break;
                }
            }

            if (!foundMatch)
            {
                // Estimate timestamp based on surrounding words
                var (start, end) = EstimateTimestamp(scriptIndex, segments, spokenWords, spokenIndex);
                segments.Add(new WordSegment
                {
                    Word = scriptWord,
                    Start = start,
                    End = end
                });
            }
        }

        return segments;
    }

    /// <summary>
    /// Estimates timestamp for a word based on surrounding aligned words.
    /// </summary>
    private (double start, double end) EstimateTimestamp(
        int index,
        List<WordSegment> segments,
        List<SpokenWord> spokenWords,
        int currentSpokenIndex)
    {
        double? prevTime = null;
        double? nextTime = null;

        // Look for previous aligned timestamp
        for (int i = index - 1; i >= 0; i--)
        {
            if (i < segments.Count && segments[i].Start != segments[i].End)
            {
                prevTime = segments[i].End;
                break;
            }
        }

        // Look for next aligned timestamp (estimate from current spoken position)
        if (currentSpokenIndex < spokenWords.Count)
        {
            nextTime = spokenWords[currentSpokenIndex].Start;
        }

        // Calculate estimated time
        if (prevTime.HasValue && nextTime.HasValue)
        {
            var mid = (prevTime.Value + nextTime.Value) / 2.0;
            return (Math.Max(0, mid - 0.05), mid + 0.05);
        }
        else if (prevTime.HasValue)
        {
            return (prevTime.Value, prevTime.Value + 0.1);
        }
        else if (nextTime.HasValue)
        {
            return (Math.Max(0, nextTime.Value - 0.1), nextTime.Value);
        }
        else
        {
            return (0.0, 0.1);
        }
    }

    /// <summary>
    /// Exports word segments to SRT format.
    /// </summary>
    private async Task ExportWordLevelSrtAsync(
        List<WordSegment> segments,
        string outputPath,
        CancellationToken cancellationToken)
    {
        var sb = new StringBuilder();

        for (int i = 0; i < segments.Count; i++)
        {
            var segment = segments[i];
            sb.AppendLine($"{i + 1}");
            sb.AppendLine($"{FormatSrtTime(segment.Start)} --> {FormatSrtTime(segment.End)}");
            sb.AppendLine(segment.Word);
            sb.AppendLine();
        }

        // Ensure output directory exists
        var directory = Path.GetDirectoryName(outputPath);
        if (!string.IsNullOrEmpty(directory))
        {
            Directory.CreateDirectory(directory);
        }

        await File.WriteAllTextAsync(outputPath, sb.ToString(), cancellationToken);
    }

    /// <summary>
    /// Formats seconds to SRT time format (HH:MM:SS,mmm).
    /// </summary>
    private string FormatSrtTime(double seconds)
    {
        var timeSpan = TimeSpan.FromSeconds(seconds);
        var hours = (int)timeSpan.TotalHours;
        var minutes = timeSpan.Minutes;
        var secs = timeSpan.Seconds;
        var milliseconds = timeSpan.Milliseconds;
        return $"{hours:D2}:{minutes:D2}:{secs:D2},{milliseconds:D3}";
    }

    /// <summary>
    /// Normalizes text to a list of lowercase words.
    /// </summary>
    private List<string> NormalizeText(string text)
    {
        // Extract words (alphanumeric sequences)
        var matches = Regex.Matches(text.ToLower(), @"\b\w+\b");
        return matches.Select(m => m.Value).ToList();
    }

    /// <summary>
    /// Normalizes a single word by removing non-word characters.
    /// </summary>
    private string NormalizeWord(string word)
    {
        return Regex.Replace(word.ToLower(), @"[^\w]", "");
    }

    /// <summary>
    /// Represents a word segment with timing information.
    /// </summary>
    private class WordSegment
    {
        public string Word { get; set; } = string.Empty;
        public double Start { get; set; }
        public double End { get; set; }
    }

    /// <summary>
    /// Represents a spoken word from transcription.
    /// </summary>
    private class SpokenWord
    {
        public string Original { get; set; } = string.Empty;
        public string Normalized { get; set; } = string.Empty;
        public double Start { get; set; }
        public double End { get; set; }
    }
}
