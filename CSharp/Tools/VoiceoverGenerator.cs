using System;
using System.IO;
using System.Text.Json;
using System.Threading;
using System.Threading.Tasks;
using StoryGenerator.Interfaces;
using StoryGenerator.Models;

namespace StoryGenerator.Tools
{
    /// <summary>
    /// Generator for creating and normalizing voiceover audio.
    /// Handles TTS generation, audio normalization, and file organization.
    /// </summary>
    public class VoiceoverGenerator
    {
        private readonly ITTSClient _ttsClient;
        private readonly IFFmpegClient _ffmpegClient;
        private readonly IVoiceRecommender _voiceRecommender;
        private readonly string _audioRoot;

        /// <summary>
        /// Initialize voiceover generator.
        /// </summary>
        /// <param name="ttsClient">TTS client for audio generation</param>
        /// <param name="ffmpegClient">FFmpeg client for audio normalization</param>
        /// <param name="voiceRecommender">Voice recommender for gender selection</param>
        /// <param name="audioRoot">Root directory for audio files (defaults to "audio")</param>
        public VoiceoverGenerator(
            ITTSClient ttsClient,
            IFFmpegClient ffmpegClient,
            IVoiceRecommender voiceRecommender,
            string audioRoot = "audio")
        {
            _ttsClient = ttsClient ?? throw new ArgumentNullException(nameof(ttsClient));
            _ffmpegClient = ffmpegClient ?? throw new ArgumentNullException(nameof(ffmpegClient));
            _voiceRecommender = voiceRecommender ?? throw new ArgumentNullException(nameof(voiceRecommender));
            _audioRoot = audioRoot;
        }

        /// <summary>
        /// Generate and normalize voiceover for a title and audience segment.
        /// </summary>
        /// <param name="titleId">Unique identifier for the title</param>
        /// <param name="title">The title text</param>
        /// <param name="text">Text to convert to speech</param>
        /// <param name="segment">Audience segment (gender/age)</param>
        /// <param name="cancellationToken">Cancellation token</param>
        /// <returns>Paths to generated TTS and normalized audio files</returns>
        public async Task<VoiceoverResult> GenerateVoiceoverAsync(
            string titleId,
            string title,
            string text,
            AudienceSegment segment,
            CancellationToken cancellationToken = default)
        {
            if (string.IsNullOrWhiteSpace(titleId))
                throw new ArgumentException("Title ID cannot be empty", nameof(titleId));
            
            if (string.IsNullOrWhiteSpace(text))
                throw new ArgumentException("Text cannot be empty", nameof(text));

            if (segment == null)
                throw new ArgumentNullException(nameof(segment));

            // Get voice recommendation
            var voiceRecommendation = await _voiceRecommender.RecommendVoiceAsync(
                title, segment.Gender, segment.Age, cancellationToken);

            // Build output paths
            var ttsPath = GetTTSPath(titleId, segment);
            var normalizedPath = GetNormalizedPath(titleId, segment);
            var lufsJsonPath = GetLufsJsonPath(titleId, segment);

            // Ensure directories exist
            EnsureDirectoryExists(ttsPath);
            EnsureDirectoryExists(normalizedPath);

            // Generate TTS audio
            Console.WriteLine($"Generating voiceover for {titleId} ({segment.Gender}/{segment.Age}) with {voiceRecommendation.Gender} voice...");
            await _ttsClient.GenerateVoiceoverAsync(
                text,
                ttsPath,
                voiceRecommendation.Gender,
                sampleRate: 48000,
                cancellationToken);

            Console.WriteLine($"✓ TTS audio generated: {ttsPath}");

            // Normalize audio to -14 LUFS
            Console.WriteLine($"Normalizing audio to -14 LUFS...");
            var normalizationResult = await _ffmpegClient.NormalizeAudioAsync(
                inputPath: ttsPath,
                outputPath: normalizedPath,
                targetLufs: -14.0,
                targetLra: 7.0,
                targetTp: -1.0,
                twoPass: true,
                sampleRate: 48000,
                cancellationToken: cancellationToken);

            Console.WriteLine($"✓ Audio normalized: {normalizedPath}");

            // Save loudnorm parameters as JSON
            if (normalizationResult.Measurements != null)
            {
                var jsonOptions = new JsonSerializerOptions
                {
                    WriteIndented = true,
                    PropertyNamingPolicy = JsonNamingPolicy.CamelCase
                };

                var lufsData = new
                {
                    titleId,
                    segment = segment.ToString(),
                    voiceGender = voiceRecommendation.Gender.ToString(),
                    targetLufs = -14.0,
                    targetLra = 7.0,
                    targetTp = -1.0,
                    measurements = normalizationResult.Measurements
                };

                var jsonContent = JsonSerializer.Serialize(lufsData, jsonOptions);
                await File.WriteAllTextAsync(lufsJsonPath, jsonContent, cancellationToken);

                Console.WriteLine($"✓ LUFS parameters saved: {lufsJsonPath}");
            }

            return new VoiceoverResult
            {
                TitleId = titleId,
                Segment = segment,
                VoiceGender = voiceRecommendation.Gender,
                TTSPath = ttsPath,
                NormalizedPath = normalizedPath,
                LufsJsonPath = lufsJsonPath,
                Success = true
            };
        }

        /// <summary>
        /// Get the TTS output path for a title and segment.
        /// Path format: /audio/tts/{segment}/{age}/{title_id}.wav
        /// </summary>
        private string GetTTSPath(string titleId, AudienceSegment segment)
        {
            return Path.Combine(_audioRoot, "tts", segment.Gender, segment.Age, $"{titleId}.wav");
        }

        /// <summary>
        /// Get the normalized audio output path.
        /// Path format: /audio/normalized/{segment}/{age}/{title_id}_lufs.wav
        /// </summary>
        private string GetNormalizedPath(string titleId, AudienceSegment segment)
        {
            return Path.Combine(_audioRoot, "normalized", segment.Gender, segment.Age, $"{titleId}_lufs.wav");
        }

        /// <summary>
        /// Get the LUFS JSON parameters path.
        /// </summary>
        private string GetLufsJsonPath(string titleId, AudienceSegment segment)
        {
            return Path.Combine(_audioRoot, "normalized", segment.Gender, segment.Age, $"{titleId}_lufs.json");
        }

        /// <summary>
        /// Ensure the directory for a file path exists.
        /// </summary>
        private void EnsureDirectoryExists(string filePath)
        {
            var directory = Path.GetDirectoryName(filePath);
            if (!string.IsNullOrEmpty(directory) && !Directory.Exists(directory))
            {
                Directory.CreateDirectory(directory);
            }
        }
    }

    /// <summary>
    /// Result of voiceover generation.
    /// </summary>
    public class VoiceoverResult
    {
        public string TitleId { get; set; } = string.Empty;
        public AudienceSegment Segment { get; set; } = new();
        public VoiceGender VoiceGender { get; set; }
        public string TTSPath { get; set; } = string.Empty;
        public string NormalizedPath { get; set; } = string.Empty;
        public string LufsJsonPath { get; set; } = string.Empty;
        public bool Success { get; set; }
    }
}
