using System.Threading;
using System.Threading.Tasks;

namespace StoryGenerator.Core.Interfaces
{
    /// <summary>
    /// Base interface for all generators in the pipeline.
    /// </summary>
    public interface IGenerator
    {
        /// <summary>
        /// Gets the name of the generator.
        /// </summary>
        string Name { get; }

        /// <summary>
        /// Gets the version of the generator.
        /// </summary>
        string Version { get; }
    }

    /// <summary>
    /// Interface for generating scripts from story ideas.
    /// Uses OpenAI GPT-4o-mini or other LLM models.
    /// </summary>
    /// <remarks>
    /// See docs/MODELS.md for detailed model information.
    /// Default model: GPT-4o-mini
    /// Alternative models: Qwen2.5-14B-Instruct, Llama-3.1-8B-Instruct
    /// </remarks>
    public interface IScriptGenerator : IGenerator
    {
        /// <summary>
        /// Generates a script from a story idea.
        /// Target length: ~360 words (~60 seconds of speech).
        /// </summary>
        /// <param name="storyIdea">The story idea to generate a script from.</param>
        /// <param name="cancellationToken">Cancellation token.</param>
        /// <returns>The generated script text.</returns>
        Task<string> GenerateScriptAsync(IStoryIdea storyIdea, CancellationToken cancellationToken = default);

        /// <summary>
        /// Generates a script and saves it to the specified path.
        /// </summary>
        /// <param name="storyIdea">The story idea to generate a script from.</param>
        /// <param name="outputPath">Path to save the generated script.</param>
        /// <param name="cancellationToken">Cancellation token.</param>
        /// <returns>Path to the saved script file.</returns>
        Task<string> GenerateAndSaveScriptAsync(IStoryIdea storyIdea, string outputPath, CancellationToken cancellationToken = default);
    }

    /// <summary>
    /// Interface for revising scripts for AI voice clarity.
    /// Optimizes scripts for text-to-speech synthesis.
    /// </summary>
    /// <remarks>
    /// Removes awkward phrasing, optimizes for ElevenLabs voice synthesis.
    /// Uses GPT-4o-mini for revision.
    /// </remarks>
    public interface IScriptRevisionGenerator : IGenerator
    {
        /// <summary>
        /// Revises a script for better voice clarity and natural speech patterns.
        /// </summary>
        /// <param name="originalScript">The original script text to revise.</param>
        /// <param name="cancellationToken">Cancellation token.</param>
        /// <returns>The revised script text.</returns>
        Task<string> ReviseScriptAsync(string originalScript, CancellationToken cancellationToken = default);

        /// <summary>
        /// Revises a script from file and saves the revised version.
        /// </summary>
        /// <param name="scriptPath">Path to the original script file.</param>
        /// <param name="outputPath">Path to save the revised script.</param>
        /// <param name="cancellationToken">Cancellation token.</param>
        /// <returns>Path to the saved revised script file.</returns>
        Task<string> ReviseAndSaveScriptAsync(string scriptPath, string outputPath, CancellationToken cancellationToken = default);
    }

    /// <summary>
    /// Interface for generating voiceovers from scripts.
    /// Uses ElevenLabs API for high-quality voice synthesis.
    /// </summary>
    /// <remarks>
    /// Model: eleven_multilingual_v2 (eleven_v3 series)
    /// See docs/MODELS.md for configuration details.
    /// Post-processing: LUFS normalization (-16.0 dB), silence trimming, padding.
    /// </remarks>
    public interface IVoiceGenerator : IGenerator
    {
        /// <summary>
        /// Generates audio from a script using text-to-speech.
        /// </summary>
        /// <param name="scriptText">The script text to convert to speech.</param>
        /// <param name="voiceId">The voice ID to use (ElevenLabs voice ID).</param>
        /// <param name="storyIdea">Optional story idea for voice parameters.</param>
        /// <param name="cancellationToken">Cancellation token.</param>
        /// <returns>The generated audio as a byte array.</returns>
        Task<byte[]> GenerateAudioAsync(string scriptText, string voiceId, IStoryIdea? storyIdea = null, CancellationToken cancellationToken = default);

        /// <summary>
        /// Generates audio and saves it to the specified path.
        /// </summary>
        /// <param name="scriptText">The script text to convert to speech.</param>
        /// <param name="voiceId">The voice ID to use (ElevenLabs voice ID).</param>
        /// <param name="outputPath">Path to save the generated audio (MP3 format).</param>
        /// <param name="storyIdea">Optional story idea for voice parameters.</param>
        /// <param name="cancellationToken">Cancellation token.</param>
        /// <returns>Path to the saved audio file.</returns>
        Task<string> GenerateAndSaveAudioAsync(string scriptText, string voiceId, string outputPath, IStoryIdea? storyIdea = null, CancellationToken cancellationToken = default);

        /// <summary>
        /// Normalizes audio to target LUFS level (-16.0 dB standard).
        /// </summary>
        /// <param name="audioPath">Path to the audio file to normalize.</param>
        /// <param name="targetLufs">Target LUFS level (default: -16.0).</param>
        /// <param name="cancellationToken">Cancellation token.</param>
        /// <returns>Path to the normalized audio file.</returns>
        Task<string> NormalizeAudioAsync(string audioPath, float targetLufs = -16.0f, CancellationToken cancellationToken = default);
    }

    /// <summary>
    /// Interface for generating subtitles from audio using ASR.
    /// Uses WhisperX for word-level alignment.
    /// </summary>
    /// <remarks>
    /// Current model: WhisperX large-v2
    /// Planned upgrade: faster-whisper large-v3 (4x faster, 50% less VRAM)
    /// See docs/MODELS.md for model details.
    /// Output format: SRT with word-level timestamps (±50ms precision).
    /// </remarks>
    public interface ISubtitleGenerator : IGenerator
    {
        /// <summary>
        /// Generates word-level subtitles from audio file.
        /// </summary>
        /// <param name="audioPath">Path to the audio file.</param>
        /// <param name="scriptText">Optional script text for alignment verification.</param>
        /// <param name="cancellationToken">Cancellation token.</param>
        /// <returns>Subtitle data in SRT format.</returns>
        Task<string> GenerateSubtitlesAsync(string audioPath, string? scriptText = null, CancellationToken cancellationToken = default);

        /// <summary>
        /// Generates subtitles and saves them to SRT file.
        /// </summary>
        /// <param name="audioPath">Path to the audio file.</param>
        /// <param name="outputPath">Path to save the SRT file.</param>
        /// <param name="scriptText">Optional script text for alignment verification.</param>
        /// <param name="cancellationToken">Cancellation token.</param>
        /// <returns>Path to the saved SRT file.</returns>
        Task<string> GenerateAndSaveSubtitlesAsync(string audioPath, string outputPath, string? scriptText = null, CancellationToken cancellationToken = default);
    }

    /// <summary>
    /// Interface for generating shotlists from scripts.
    /// Analyzes script to create scene-by-scene visual descriptions.
    /// </summary>
    /// <remarks>
    /// Planned feature - not yet implemented.
    /// Will use Qwen2.5-14B-Instruct or Llama-3.1-8B-Instruct.
    /// See docs/MODELS.md and docs/EXAMPLES.md for shotlist format.
    /// </remarks>
    public interface IShotlistGenerator : IGenerator
    {
        /// <summary>
        /// Generates a shotlist from a script.
        /// </summary>
        /// <param name="scriptText">The script text to analyze.</param>
        /// <param name="audioDuration">Duration of the audio in seconds.</param>
        /// <param name="cancellationToken">Cancellation token.</param>
        /// <returns>Shotlist data containing scene descriptions and visual prompts.</returns>
        Task<Shotlist> GenerateShotlistAsync(string scriptText, float audioDuration, CancellationToken cancellationToken = default);
    }

    /// <summary>
    /// Interface for generating keyframes from shotlist.
    /// Uses Stable Diffusion XL for high-quality image generation.
    /// </summary>
    /// <remarks>
    /// Planned feature - not yet implemented.
    /// Model: stabilityai/stable-diffusion-xl-base-1.0
    /// Resolution: 1024x1024 (will be cropped to 1080x1920 for vertical video)
    /// See docs/MODELS.md for SDXL configuration details.
    /// </remarks>
    public interface IKeyframeGenerator : IGenerator
    {
        /// <summary>
        /// Generates a keyframe image from a visual prompt.
        /// </summary>
        /// <param name="prompt">The visual description/prompt for the image.</param>
        /// <param name="negativePrompt">Negative prompt to avoid unwanted elements.</param>
        /// <param name="seed">Random seed for reproducibility (optional).</param>
        /// <param name="cancellationToken">Cancellation token.</param>
        /// <returns>The generated image as a byte array (PNG format).</returns>
        Task<byte[]> GenerateKeyframeAsync(string prompt, string? negativePrompt = null, int? seed = null, CancellationToken cancellationToken = default);

        /// <summary>
        /// Generates all keyframes for a shotlist.
        /// </summary>
        /// <param name="shotlist">The shotlist containing scene descriptions.</param>
        /// <param name="outputDirectory">Directory to save keyframe images.</param>
        /// <param name="cancellationToken">Cancellation token.</param>
        /// <returns>Dictionary mapping shot numbers to keyframe file paths.</returns>
        Task<System.Collections.Generic.Dictionary<int, string>> GenerateKeyframesAsync(Shotlist shotlist, string outputDirectory, CancellationToken cancellationToken = default);
    }

    /// <summary>
    /// Interface for synthesizing video from keyframes.
    /// Uses LTX-Video or Stable Video Diffusion.
    /// </summary>
    /// <remarks>
    /// Planned feature - not yet implemented.
    /// Model options: LTX-Video (recommended), Stable Video Diffusion
    /// See docs/MODELS.md for model comparison.
    /// Output: 1080x1920 MP4 video with 30 fps.
    /// </remarks>
    public interface IVideoSynthesizer : IGenerator
    {
        /// <summary>
        /// Synthesizes video from keyframes and audio.
        /// </summary>
        /// <param name="keyframes">Paths to keyframe images.</param>
        /// <param name="audioPath">Path to the audio file.</param>
        /// <param name="shotlist">Shotlist with timing information.</param>
        /// <param name="outputPath">Path to save the generated video.</param>
        /// <param name="cancellationToken">Cancellation token.</param>
        /// <returns>Path to the generated video file.</returns>
        Task<string> SynthesizeVideoAsync(string[] keyframes, string audioPath, Shotlist shotlist, string outputPath, CancellationToken cancellationToken = default);
    }

    /// <summary>
    /// Represents a shotlist with scene descriptions and timing.
    /// </summary>
    public class Shotlist
    {
        /// <summary>
        /// Gets or sets the story title.
        /// </summary>
        public string StoryTitle { get; set; } = string.Empty;

        /// <summary>
        /// Gets or sets the total duration in seconds.
        /// </summary>
        public float TotalDuration { get; set; }

        /// <summary>
        /// Gets or sets the list of shots/scenes.
        /// </summary>
        public System.Collections.Generic.List<Shot> Shots { get; set; } = new();
    }

    /// <summary>
    /// Represents a single shot/scene in a shotlist.
    /// </summary>
    public class Shot
    {
        /// <summary>
        /// Gets or sets the shot number.
        /// </summary>
        public int ShotNumber { get; set; }

        /// <summary>
        /// Gets or sets the start time in seconds.
        /// </summary>
        public float StartTime { get; set; }

        /// <summary>
        /// Gets or sets the end time in seconds.
        /// </summary>
        public float EndTime { get; set; }

        /// <summary>
        /// Gets or sets the duration in seconds.
        /// </summary>
        public float Duration { get; set; }

        /// <summary>
        /// Gets or sets the scene description.
        /// </summary>
        public string SceneDescription { get; set; } = string.Empty;

        /// <summary>
        /// Gets or sets the visual prompt for image generation.
        /// </summary>
        public string VisualPrompt { get; set; } = string.Empty;

        /// <summary>
        /// Gets or sets the mood of the scene.
        /// </summary>
        public string Mood { get; set; } = string.Empty;

        /// <summary>
        /// Gets or sets the camera angle.
        /// </summary>
        public string CameraAngle { get; set; } = string.Empty;

        /// <summary>
        /// Gets or sets the lighting description.
        /// </summary>
        public string Lighting { get; set; } = string.Empty;

        /// <summary>
        /// Gets or sets the color palette.
        /// </summary>
        public string ColorPalette { get; set; } = string.Empty;

        /// <summary>
        /// Gets or sets key visual elements.
        /// </summary>
        public System.Collections.Generic.List<string> KeyElements { get; set; } = new();
    }
}
