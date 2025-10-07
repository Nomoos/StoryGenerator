namespace StoryGenerator.Providers.ElevenLabs;

/// <summary>
/// Configuration options for ElevenLabs API.
/// </summary>
public class ElevenLabsOptions
{
    /// <summary>
    /// Section name in configuration.
    /// </summary>
    public const string SectionName = "ElevenLabs";

    /// <summary>
    /// Gets or sets the API key for ElevenLabs.
    /// </summary>
    public string ApiKey { get; set; } = string.Empty;

    /// <summary>
    /// Gets or sets the voice ID to use for generation.
    /// </summary>
    public string VoiceId { get; set; } = "BZgkqPqms7Kj9ulSkVzn";

    /// <summary>
    /// Gets or sets the model to use (default: eleven_v3).
    /// </summary>
    public string Model { get; set; } = "eleven_v3";

    /// <summary>
    /// Gets or sets the output format.
    /// </summary>
    public string OutputFormat { get; set; } = "mp3_44100_192";

    /// <summary>
    /// Gets or sets the default voice stability (0.0 to 1.0).
    /// </summary>
    public float VoiceStability { get; set; } = 0.5f;

    /// <summary>
    /// Gets or sets the default voice similarity boost (0.0 to 1.0).
    /// </summary>
    public float VoiceSimilarityBoost { get; set; } = 0.75f;

    /// <summary>
    /// Gets or sets the default voice style exaggeration (0.0 to 1.0).
    /// </summary>
    public float VoiceStyleExaggeration { get; set; } = 0.0f;

    /// <summary>
    /// Gets or sets the API base URL.
    /// </summary>
    public string ApiBaseUrl { get; set; } = "https://api.elevenlabs.io/v1/";
}
