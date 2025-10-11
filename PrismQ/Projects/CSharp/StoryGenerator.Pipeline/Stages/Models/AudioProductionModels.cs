namespace StoryGenerator.Pipeline.Stages.Models;

/// <summary>
/// Input for TTS Generation Stage
/// </summary>
public class TtsGenerationInput
{
    /// <summary>
    /// Script content to convert to speech
    /// </summary>
    public string ScriptContent { get; set; } = string.Empty;

    /// <summary>
    /// Title ID for organizing output
    /// </summary>
    public string TitleId { get; set; } = string.Empty;

    /// <summary>
    /// Target gender audience
    /// </summary>
    public string Gender { get; set; } = string.Empty;

    /// <summary>
    /// Target age group
    /// </summary>
    public string AgeGroup { get; set; } = string.Empty;

    /// <summary>
    /// Voice ID or name to use for TTS
    /// </summary>
    public string VoiceId { get; set; } = "default";

    /// <summary>
    /// TTS provider (e.g., "elevenlabs", "openai", "azure")
    /// </summary>
    public string Provider { get; set; } = "openai";
}

/// <summary>
/// Output from TTS Generation Stage
/// </summary>
public class TtsGenerationOutput
{
    /// <summary>
    /// Path to generated audio file
    /// </summary>
    public string AudioPath { get; set; } = string.Empty;

    /// <summary>
    /// Duration of audio in seconds
    /// </summary>
    public double DurationSeconds { get; set; }

    /// <summary>
    /// Audio format (e.g., "mp3", "wav")
    /// </summary>
    public string Format { get; set; } = "mp3";

    /// <summary>
    /// Sample rate in Hz
    /// </summary>
    public int SampleRate { get; set; } = 44100;
}

/// <summary>
/// Input for Audio Normalization Stage
/// </summary>
public class AudioNormalizationInput
{
    /// <summary>
    /// Path to input audio file
    /// </summary>
    public string InputAudioPath { get; set; } = string.Empty;

    /// <summary>
    /// Title ID for organizing output
    /// </summary>
    public string TitleId { get; set; } = string.Empty;

    /// <summary>
    /// Target gender audience
    /// </summary>
    public string Gender { get; set; } = string.Empty;

    /// <summary>
    /// Target age group
    /// </summary>
    public string AgeGroup { get; set; } = string.Empty;

    /// <summary>
    /// Target LUFS (Loudness Units Full Scale) value
    /// YouTube/TikTok standard is -14.0 LUFS
    /// </summary>
    public double TargetLufs { get; set; } = -14.0;

    /// <summary>
    /// Target loudness range in LU
    /// </summary>
    public double TargetLra { get; set; } = 7.0;

    /// <summary>
    /// Target true peak in dBTP
    /// </summary>
    public double TargetTp { get; set; } = -1.0;

    /// <summary>
    /// Use two-pass normalization for better accuracy
    /// </summary>
    public bool TwoPass { get; set; } = true;
}

/// <summary>
/// Output from Audio Normalization Stage
/// </summary>
public class AudioNormalizationOutput
{
    /// <summary>
    /// Path to normalized audio file
    /// </summary>
    public string NormalizedAudioPath { get; set; } = string.Empty;

    /// <summary>
    /// Actual measured LUFS before normalization
    /// </summary>
    public double InputLufs { get; set; }

    /// <summary>
    /// Actual measured LUFS after normalization
    /// </summary>
    public double OutputLufs { get; set; }

    /// <summary>
    /// Target LUFS that was requested
    /// </summary>
    public double TargetLufs { get; set; }

    /// <summary>
    /// Whether normalization met the target (within tolerance)
    /// </summary>
    public bool MeetsTarget { get; set; }

    /// <summary>
    /// Duration of audio in seconds
    /// </summary>
    public double DurationSeconds { get; set; }
}
