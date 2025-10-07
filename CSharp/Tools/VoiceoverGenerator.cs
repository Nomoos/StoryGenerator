using System;
using System.Diagnostics;
using System.IO;
using System.Text.Json;
using System.Threading;
using System.Threading.Tasks;
using StoryGenerator.Interfaces;
using StoryGenerator.Models;

namespace StoryGenerator.Tools
{
    /// <summary>
    /// Orchestrator for voiceover generation with versioning support.
    /// Implements versioned file outputs for quality comparison and revision tracking.
    /// </summary>
    public class VoiceoverOrchestrator : IVoiceoverOrchestrator
    {
        private readonly ITTSClient _ttsClient;
        private readonly IFFmpegClient _ffmpegClient;
        private readonly IVoiceRecommender _voiceRecommender;
        private readonly string _audioRoot;
        private readonly string _versionIdentifier;

        /// <summary>
        /// Initialize voiceover orchestrator with versioning.
        /// </summary>
        /// <param name="ttsClient">TTS client for audio generation</param>
        /// <param name="ffmpegClient">FFmpeg client for audio normalization</param>
        /// <param name="voiceRecommender">Voice recommender for gender selection</param>
        /// <param name="versionIdentifier">Version identifier (e.g., "v1", "v2") for tracking quality changes</param>
        /// <param name="audioRoot">Root directory for audio files (defaults to "audio")</param>
        public VoiceoverOrchestrator(
            ITTSClient ttsClient,
            IFFmpegClient ffmpegClient,
            IVoiceRecommender voiceRecommender,
            string versionIdentifier = "v1",
            string audioRoot = "audio")
        {
            _ttsClient = ttsClient ?? throw new ArgumentNullException(nameof(ttsClient));
            _ffmpegClient = ffmpegClient ?? throw new ArgumentNullException(nameof(ffmpegClient));
            _voiceRecommender = voiceRecommender ?? throw new ArgumentNullException(nameof(voiceRecommender));
            _versionIdentifier = versionIdentifier;
            _audioRoot = audioRoot;
        }

        /// <summary>
        /// Get the version identifier.
        /// </summary>
        public string GetVersionIdentifier() => _versionIdentifier;

        /// <summary>
        /// Generate voiceover with versioning support.
        /// </summary>
        public async Task<VoiceoverGenerationResult> GenerateVoiceoverAsync(
            VoiceoverRequest request,
            CancellationToken cancellationToken = default)
        {
            if (request == null)
                throw new ArgumentNullException(nameof(request));

            if (string.IsNullOrWhiteSpace(request.TitleId))
                throw new ArgumentException("Title ID cannot be empty", nameof(request));

            if (string.IsNullOrWhiteSpace(request.Text))
                throw new ArgumentException("Text cannot be empty", nameof(request));

            if (request.Segment == null)
                throw new ArgumentNullException(nameof(request.Segment));

            var result = new VoiceoverGenerationResult
            {
                TitleId = request.TitleId,
                Segment = request.Segment,
                Version = request.VersionSuffix ?? _versionIdentifier
            };

            var stopwatch = Stopwatch.StartNew();

            try
            {
                // Get voice recommendation
                var voiceRecommendation = await _voiceRecommender.RecommendVoiceAsync(
                    request.Title, request.Segment.Gender, request.Segment.Age, cancellationToken);

                result.VoiceGender = voiceRecommendation.Gender;

                // Build versioned output paths
                var ttsPath = GetVersionedTTSPath(request.TitleId, request.Segment, result.Version);
                var normalizedPath = GetVersionedNormalizedPath(request.TitleId, request.Segment, result.Version);
                var lufsJsonPath = GetVersionedLufsJsonPath(request.TitleId, request.Segment, result.Version);

                // Ensure directories exist
                EnsureDirectoryExists(ttsPath);
                EnsureDirectoryExists(normalizedPath);

                // Generate TTS audio
                Console.WriteLine($"[{result.Version}] Generating voiceover for {request.TitleId} ({request.Segment.Gender}/{request.Segment.Age}) with {voiceRecommendation.Gender} voice...");
                
                var ttsStart = stopwatch.Elapsed;
                await _ttsClient.GenerateVoiceoverAsync(
                    request.Text,
                    ttsPath,
                    voiceRecommendation.Gender,
                    sampleRate: 48000,
                    cancellationToken);
                
                result.TtsDuration = (stopwatch.Elapsed - ttsStart).TotalSeconds;
                result.TTSPath = ttsPath;

                Console.WriteLine($"✓ TTS audio generated in {result.TtsDuration:F2}s: {ttsPath}");

                // Normalize audio to -14 LUFS
                Console.WriteLine($"[{result.Version}] Normalizing audio to -14 LUFS...");
                
                var normStart = stopwatch.Elapsed;
                var normalizationResult = await _ffmpegClient.NormalizeAudioAsync(
                    inputPath: ttsPath,
                    outputPath: normalizedPath,
                    targetLufs: -14.0,
                    targetLra: 7.0,
                    targetTp: -1.0,
                    twoPass: true,
                    sampleRate: 48000,
                    cancellationToken: cancellationToken);

                result.NormalizationDuration = (stopwatch.Elapsed - normStart).TotalSeconds;
                result.NormalizedPath = normalizedPath;

                Console.WriteLine($"✓ Audio normalized in {result.NormalizationDuration:F2}s: {normalizedPath}");

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
                        titleId = request.TitleId,
                        segment = request.Segment.ToString(),
                        voiceGender = voiceRecommendation.Gender.ToString(),
                        version = result.Version,
                        targetLufs = -14.0,
                        targetLra = 7.0,
                        targetTp = -1.0,
                        measurements = normalizationResult.Measurements,
                        generationTimings = new
                        {
                            ttsDuration = result.TtsDuration,
                            normalizationDuration = result.NormalizationDuration
                        }
                    };

                    var jsonContent = JsonSerializer.Serialize(lufsData, jsonOptions);
                    await File.WriteAllTextAsync(lufsJsonPath, jsonContent, cancellationToken);

                    result.LufsJsonPath = lufsJsonPath;
                    Console.WriteLine($"✓ LUFS parameters saved: {lufsJsonPath}");
                }

                result.Success = true;
            }
            catch (Exception ex)
            {
                result.Success = false;
                result.ErrorMessage = ex.Message;
                Console.WriteLine($"❌ Voiceover generation failed: {ex.Message}");
            }

            stopwatch.Stop();
            return result;
        }

        /// <summary>
        /// Get the versioned TTS output path.
        /// Path format: /audio/tts/{segment}/{age}/{title_id}_{version}.wav
        /// </summary>
        private string GetVersionedTTSPath(string titleId, AudienceSegment segment, string version)
        {
            return Path.Combine(_audioRoot, "tts", segment.Gender, segment.Age, $"{titleId}_{version}.wav");
        }

        /// <summary>
        /// Get the versioned normalized audio output path.
        /// Path format: /audio/normalized/{segment}/{age}/{title_id}_{version}_lufs.wav
        /// </summary>
        private string GetVersionedNormalizedPath(string titleId, AudienceSegment segment, string version)
        {
            return Path.Combine(_audioRoot, "normalized", segment.Gender, segment.Age, $"{titleId}_{version}_lufs.wav");
        }

        /// <summary>
        /// Get the versioned LUFS JSON parameters path.
        /// Path format: /audio/normalized/{segment}/{age}/{title_id}_{version}_lufs.json
        /// </summary>
        private string GetVersionedLufsJsonPath(string titleId, AudienceSegment segment, string version)
        {
            return Path.Combine(_audioRoot, "normalized", segment.Gender, segment.Age, $"{titleId}_{version}_lufs.json");
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
    /// Legacy generator for creating and normalizing voiceover audio.
    /// Maintained for backward compatibility. Use VoiceoverOrchestrator for new code.
    /// </summary>
    [Obsolete("Use VoiceoverOrchestrator with versioning support instead")]
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
