namespace StoryGenerator.Providers.OpenAI;

/// <summary>
/// Configuration options for OpenAI API.
/// </summary>
public class OpenAIOptions
{
    /// <summary>
    /// Section name in configuration.
    /// </summary>
    public const string SectionName = "OpenAI";

    /// <summary>
    /// Gets or sets the API key for OpenAI.
    /// </summary>
    public string ApiKey { get; set; } = string.Empty;

    /// <summary>
    /// Gets or sets the model to use (default: gpt-4o-mini).
    /// </summary>
    public string Model { get; set; } = "gpt-4o-mini";

    /// <summary>
    /// Gets or sets the temperature for generation (0.0 to 2.0).
    /// </summary>
    public float Temperature { get; set; } = 0.9f;

    /// <summary>
    /// Gets or sets the maximum tokens for completion.
    /// </summary>
    public int? MaxTokens { get; set; }

    /// <summary>
    /// Gets or sets the API base URL (optional, for custom endpoints).
    /// </summary>
    public string? ApiBaseUrl { get; set; }
}
