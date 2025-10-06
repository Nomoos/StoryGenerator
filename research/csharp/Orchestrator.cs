using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Threading;
using System.Threading.Tasks;

namespace StoryGenerator.Research
{
    /// <summary>
    /// Orchestrator for coordinating local model operations.
    /// Research prototype for managing the full pipeline of LLM, ASR, and media processing.
    /// </summary>
    public class Orchestrator
    {
        private readonly OllamaClient _ollamaClient;
        private readonly WhisperClient _whisperClient;
        private readonly FFmpegClient _ffmpegClient;

        /// <summary>
        /// Initialize the orchestrator with default clients.
        /// </summary>
        public Orchestrator()
            : this(
                new OllamaClient(),
                new WhisperClient(),
                new FFmpegClient())
        {
        }

        /// <summary>
        /// Initialize the orchestrator with custom clients.
        /// </summary>
        /// <param name="ollamaClient">Ollama LLM client</param>
        /// <param name="whisperClient">Whisper ASR client</param>
        /// <param name="ffmpegClient">FFmpeg media processing client</param>
        public Orchestrator(
            OllamaClient ollamaClient,
            WhisperClient whisperClient,
            FFmpegClient ffmpegClient)
        {
            _ollamaClient = ollamaClient ?? throw new ArgumentNullException(nameof(ollamaClient));
            _whisperClient = whisperClient ?? throw new ArgumentNullException(nameof(whisperClient));
            _ffmpegClient = ffmpegClient ?? throw new ArgumentNullException(nameof(ffmpegClient));
        }

        /// <summary>
        /// Generate a complete story from a topic.
        /// </summary>
        /// <param name="topic">Story topic or prompt</param>
        /// <param name="style">Story style (e.g., "dramatic", "comedic", "horror")</param>
        /// <param name="cancellationToken">Cancellation token</param>
        /// <returns>Generated story script</returns>
        public async Task<StoryScript> GenerateStoryAsync(
            string topic,
            string style = "dramatic",
            CancellationToken cancellationToken = default)
        {
            // Step 1: Generate story ideas
            var ideaPrompt = $"Generate a {style} story idea about: {topic}\n" +
                "Include: title, brief synopsis, main character, conflict, and resolution.";

            var ideaText = await _ollamaClient.GenerateAsync(
                ideaPrompt,
                system: "You are a creative storytelling assistant.",
                temperature: 0.9f,
                cancellationToken: cancellationToken);

            // Step 2: Generate full script
            var scriptPrompt = $"Based on this story idea, write a complete script:\n\n{ideaText}\n\n" +
                "Format the script with clear narration, dialogue, and scene descriptions.";

            var scriptText = await _ollamaClient.GenerateAsync(
                scriptPrompt,
                system: "You are a professional screenwriter.",
                temperature: 0.8f,
                cancellationToken: cancellationToken);

            // Step 3: Generate scene descriptions for visual generation
            var scenesPrompt = $"Based on this script, create detailed visual descriptions for 5-7 key scenes:\n\n{scriptText}";

            var scenesText = await _ollamaClient.GenerateAsync(
                scenesPrompt,
                system: "You are a visual storytelling expert.",
                temperature: 0.7f,
                cancellationToken: cancellationToken);

            return new StoryScript
            {
                Idea = ideaText,
                Script = scriptText,
                SceneDescriptions = ParseSceneDescriptions(scenesText),
                GeneratedAt = DateTime.UtcNow
            };
        }

        /// <summary>
        /// Process audio file: transcribe and generate subtitles.
        /// </summary>
        /// <param name="audioPath">Path to audio file</param>
        /// <param name="outputDir">Output directory for results</param>
        /// <param name="language">Language code or null for auto-detection</param>
        /// <param name="cancellationToken">Cancellation token</param>
        /// <returns>Processing result with paths to generated files</returns>
        public async Task<AudioProcessingResult> ProcessAudioAsync(
            string audioPath,
            string outputDir,
            string language = null,
            CancellationToken cancellationToken = default)
        {
            Directory.CreateDirectory(outputDir);

            var fileName = Path.GetFileNameWithoutExtension(audioPath);

            // Step 1: Normalize audio
            var normalizedPath = Path.Combine(outputDir, $"{fileName}_normalized.mp3");
            var normResult = await _ffmpegClient.NormalizeAudioAsync(
                audioPath,
                normalizedPath,
                targetLufs: -16.0,
                twoPass: true,
                cancellationToken: cancellationToken);

            // Step 2: Transcribe audio
            var transcription = await _whisperClient.TranscribeAsync(
                normalizedPath,
                language: language,
                wordTimestamps: true,
                cancellationToken: cancellationToken);

            // Step 3: Generate SRT subtitles
            var srtPath = Path.Combine(outputDir, $"{fileName}.srt");
            var srtContent = await _whisperClient.TranscribeToSrtAsync(
                normalizedPath,
                srtPath,
                language: language,
                cancellationToken: cancellationToken);

            // Step 4: Get audio info
            var audioInfo = await _ffmpegClient.GetAudioInfoAsync(
                normalizedPath,
                cancellationToken);

            return new AudioProcessingResult
            {
                Success = true,
                NormalizedAudioPath = normalizedPath,
                TranscriptionText = transcription.Text,
                SubtitlePath = srtPath,
                Language = transcription.Language,
                Duration = audioInfo.Duration,
                ProcessedAt = DateTime.UtcNow
            };
        }

        /// <summary>
        /// Create a complete video pipeline: script → audio → video.
        /// </summary>
        /// <param name="topic">Story topic</param>
        /// <param name="outputDir">Output directory</param>
        /// <param name="style">Story style</param>
        /// <param name="cancellationToken">Cancellation token</param>
        /// <returns>Pipeline result with all generated assets</returns>
        public async Task<VideoPipelineResult> CreateVideoAsync(
            string topic,
            string outputDir,
            string style = "cinematic",
            CancellationToken cancellationToken = default)
        {
            Directory.CreateDirectory(outputDir);

            // Step 1: Generate story script
            var story = await GenerateStoryAsync(topic, style, cancellationToken);

            var scriptPath = Path.Combine(outputDir, "script.txt");
            await File.WriteAllTextAsync(scriptPath, story.Script, cancellationToken);

            // Step 2: Generate voiceover (placeholder - would use TTS service)
            // For now, this is a stub
            var voiceoverPath = Path.Combine(outputDir, "voiceover.mp3");
            // await GenerateVoiceoverAsync(story.Script, voiceoverPath, cancellationToken);

            // Step 3: Process audio (normalize + transcribe)
            // This would work once voiceover is generated
            // var audioResult = await ProcessAudioAsync(voiceoverPath, outputDir, cancellationToken: cancellationToken);

            // Step 4: Generate keyframes from scene descriptions
            // This would call SDXL or similar image generation
            var keyframesDir = Path.Combine(outputDir, "keyframes");
            Directory.CreateDirectory(keyframesDir);

            // Placeholder for keyframe generation
            var keyframePaths = new List<string>();
            // foreach (var scene in story.SceneDescriptions)
            // {
            //     var keyframePath = await GenerateKeyframeAsync(scene, keyframesDir, cancellationToken);
            //     keyframePaths.Add(keyframePath);
            // }

            // Step 5: Generate video clips from keyframes
            // This would call video generation models
            var clipsDir = Path.Combine(outputDir, "clips");
            Directory.CreateDirectory(clipsDir);

            // Step 6: Combine clips into final video
            // This would use FFmpeg to merge clips with audio and subtitles
            var finalVideoPath = Path.Combine(outputDir, "final_video.mp4");

            return new VideoPipelineResult
            {
                Success = true,
                StoryScript = story,
                ScriptPath = scriptPath,
                VoiceoverPath = voiceoverPath,
                KeyframePaths = keyframePaths,
                FinalVideoPath = finalVideoPath,
                OutputDirectory = outputDir,
                CompletedAt = DateTime.UtcNow
            };
        }

        /// <summary>
        /// Batch process multiple stories.
        /// </summary>
        /// <param name="topics">List of story topics</param>
        /// <param name="outputBaseDir">Base output directory</param>
        /// <param name="style">Story style</param>
        /// <param name="cancellationToken">Cancellation token</param>
        /// <returns>List of pipeline results</returns>
        public async Task<List<VideoPipelineResult>> BatchCreateVideosAsync(
            List<string> topics,
            string outputBaseDir,
            string style = "cinematic",
            CancellationToken cancellationToken = default)
        {
            Directory.CreateDirectory(outputBaseDir);

            var results = new List<VideoPipelineResult>();

            for (int i = 0; i < topics.Count; i++)
            {
                var topic = topics[i];
                var outputDir = Path.Combine(outputBaseDir, $"story_{i + 1:D3}");

                Console.WriteLine($"Processing story {i + 1}/{topics.Count}: {topic}");

                try
                {
                    var result = await CreateVideoAsync(
                        topic,
                        outputDir,
                        style,
                        cancellationToken);

                    results.Add(result);
                }
                catch (Exception ex)
                {
                    Console.WriteLine($"Error processing story '{topic}': {ex.Message}");
                    
                    results.Add(new VideoPipelineResult
                    {
                        Success = false,
                        ErrorMessage = ex.Message,
                        OutputDirectory = outputDir
                    });
                }
            }

            return results;
        }

        /// <summary>
        /// Parse scene descriptions from LLM output.
        /// </summary>
        private List<string> ParseSceneDescriptions(string scenesText)
        {
            // Simple parsing - split by common scene markers
            var scenes = scenesText
                .Split(new[] { "\n\n", "Scene ", "scene " }, StringSplitOptions.RemoveEmptyEntries)
                .Select(s => s.Trim())
                .Where(s => !string.IsNullOrWhiteSpace(s))
                .ToList();

            return scenes;
        }
    }

    /// <summary>
    /// Represents a generated story script.
    /// </summary>
    public class StoryScript
    {
        public string Idea { get; set; }
        public string Script { get; set; }
        public List<string> SceneDescriptions { get; set; }
        public DateTime GeneratedAt { get; set; }
    }

    /// <summary>
    /// Represents audio processing result.
    /// </summary>
    public class AudioProcessingResult
    {
        public bool Success { get; set; }
        public string NormalizedAudioPath { get; set; }
        public string TranscriptionText { get; set; }
        public string SubtitlePath { get; set; }
        public string Language { get; set; }
        public double Duration { get; set; }
        public DateTime ProcessedAt { get; set; }
    }

    /// <summary>
    /// Represents video pipeline result.
    /// </summary>
    public class VideoPipelineResult
    {
        public bool Success { get; set; }
        public string ErrorMessage { get; set; }
        public StoryScript StoryScript { get; set; }
        public string ScriptPath { get; set; }
        public string VoiceoverPath { get; set; }
        public List<string> KeyframePaths { get; set; }
        public string FinalVideoPath { get; set; }
        public string OutputDirectory { get; set; }
        public DateTime CompletedAt { get; set; }
    }
}
