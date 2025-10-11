using System.Net.Http.Json;
using System.Text;
using System.Text.Json;
using System.Text.Json.Serialization;
using Microsoft.Extensions.Logging;
using Microsoft.Extensions.Options;
using PrismQ.Shared.Core.Services;

namespace StoryGenerator.Providers.ElevenLabs;

/// <summary>
/// Client for interacting with ElevenLabs API.
/// Provides text-to-speech functionality.
/// </summary>
public class ElevenLabsClient
{
    private readonly HttpClient _httpClient;
    private readonly ILogger<ElevenLabsClient> _logger;
    private readonly ElevenLabsOptions _options;
    private readonly RetryService _retryService;

    public ElevenLabsClient(
        HttpClient httpClient,
        IOptions<ElevenLabsOptions> options,
        ILogger<ElevenLabsClient> logger,
        RetryService retryService)
    {
        _httpClient = httpClient;
        _logger = logger;
        _options = options.Value;
        _retryService = retryService;

        // Configure HTTP client
        _httpClient.BaseAddress = new Uri(_options.ApiBaseUrl);
        _httpClient.DefaultRequestHeaders.Add("xi-api-key", _options.ApiKey);
    }

    /// <summary>
    /// Generates audio from text using text-to-speech.
    /// </summary>
    /// <param name="text">Text to convert to speech.</param>
    /// <param name="voiceId">Voice ID to use (overrides default).</param>
    /// <param name="voiceSettings">Voice settings (optional).</param>
    /// <param name="cancellationToken">Cancellation token.</param>
    /// <returns>Audio data as byte array.</returns>
    public async Task<byte[]> GenerateAudioAsync(
        string text,
        string? voiceId = null,
        VoiceSettings? voiceSettings = null,
        CancellationToken cancellationToken = default)
    {
        var effectiveVoiceId = voiceId ?? _options.VoiceId;
        var effectiveSettings = voiceSettings ?? new VoiceSettings
        {
            Stability = _options.VoiceStability,
            SimilarityBoost = _options.VoiceSimilarityBoost,
            Style = _options.VoiceStyleExaggeration
        };

        return await _retryService.ExecuteWithRetryAndCircuitBreakerAsync(
            "elevenlabs",
            async () => await SendTextToSpeechRequestAsync(text, effectiveVoiceId, effectiveSettings, cancellationToken),
            maxRetries: 3,
            baseDelay: 2.0,
            maxDelay: 30.0);
    }

    /// <summary>
    /// Sends the actual HTTP request to ElevenLabs API.
    /// </summary>
    private async Task<byte[]> SendTextToSpeechRequestAsync(
        string text,
        string voiceId,
        VoiceSettings settings,
        CancellationToken cancellationToken)
    {
        var request = new TextToSpeechRequest
        {
            Text = text,
            ModelId = _options.Model,
            VoiceSettings = settings
        };

        var jsonContent = JsonSerializer.Serialize(request, new JsonSerializerOptions
        {
            PropertyNamingPolicy = JsonNamingPolicy.SnakeCaseLower,
            DefaultIgnoreCondition = JsonIgnoreCondition.WhenWritingNull
        });

        var content = new StringContent(jsonContent, Encoding.UTF8, "application/json");
        var endpoint = $"text-to-speech/{voiceId}?output_format={_options.OutputFormat}";
        
        var response = await _httpClient.PostAsync(endpoint, content, cancellationToken);

        if (!response.IsSuccessStatusCode)
        {
            var errorContent = await response.Content.ReadAsStringAsync(cancellationToken);
            _logger.LogError("ElevenLabs API error: {StatusCode} - {Error}", response.StatusCode, errorContent);
            throw new HttpRequestException($"ElevenLabs API returned {response.StatusCode}: {errorContent}");
        }

        return await response.Content.ReadAsByteArrayAsync(cancellationToken);
    }

    /// <summary>
    /// Saves generated audio to a file.
    /// </summary>
    /// <param name="audioData">Audio data to save.</param>
    /// <param name="outputPath">Path to save the audio file.</param>
    public async Task SaveAudioAsync(byte[] audioData, string outputPath)
    {
        var directory = Path.GetDirectoryName(outputPath);
        if (!string.IsNullOrEmpty(directory))
        {
            Directory.CreateDirectory(directory);
        }

        await File.WriteAllBytesAsync(outputPath, audioData);
        _logger.LogInformation("Audio saved to: {OutputPath}", outputPath);
    }
}

/// <summary>
/// Text-to-speech request model.
/// </summary>
public class TextToSpeechRequest
{
    [JsonPropertyName("text")]
    public string Text { get; set; } = string.Empty;

    [JsonPropertyName("model_id")]
    public string ModelId { get; set; } = string.Empty;

    [JsonPropertyName("voice_settings")]
    public VoiceSettings VoiceSettings { get; set; } = new();
}

/// <summary>
/// Voice settings model for ElevenLabs.
/// </summary>
public class VoiceSettings
{
    /// <summary>
    /// Gets or sets the voice stability (0.0 to 1.0).
    /// Lower values make speech more variable, higher values make it more stable.
    /// </summary>
    [JsonPropertyName("stability")]
    public float Stability { get; set; } = 0.5f;

    /// <summary>
    /// Gets or sets the voice similarity boost (0.0 to 1.0).
    /// Higher values make the voice sound more similar to the original.
    /// </summary>
    [JsonPropertyName("similarity_boost")]
    public float SimilarityBoost { get; set; } = 0.75f;

    /// <summary>
    /// Gets or sets the voice style exaggeration (0.0 to 1.0).
    /// Higher values exaggerate the style of the voice.
    /// </summary>
    [JsonPropertyName("style")]
    public float Style { get; set; } = 0.0f;

    /// <summary>
    /// Gets or sets whether to use speaker boost.
    /// </summary>
    [JsonPropertyName("use_speaker_boost")]
    public bool UseSpeakerBoost { get; set; } = true;
}
