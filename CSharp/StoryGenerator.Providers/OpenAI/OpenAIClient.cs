using System.Net.Http.Json;
using System.Text;
using System.Text.Json;
using System.Text.Json.Serialization;
using Microsoft.Extensions.Logging;
using Microsoft.Extensions.Options;
using StoryGenerator.Core.Services;

namespace StoryGenerator.Providers.OpenAI;

/// <summary>
/// Client for interacting with OpenAI API.
/// Provides chat completion functionality similar to Python's openai library.
/// </summary>
public class OpenAIClient
{
    private readonly HttpClient _httpClient;
    private readonly ILogger<OpenAIClient> _logger;
    private readonly OpenAIOptions _options;
    private readonly RetryService _retryService;

    public OpenAIClient(
        HttpClient httpClient,
        IOptions<OpenAIOptions> options,
        ILogger<OpenAIClient> logger,
        RetryService retryService)
    {
        _httpClient = httpClient;
        _logger = logger;
        _options = options.Value;
        _retryService = retryService;

        // Configure HTTP client
        _httpClient.BaseAddress = new Uri(_options.ApiBaseUrl ?? "https://api.openai.com/v1/");
        _httpClient.DefaultRequestHeaders.Add("Authorization", $"Bearer {_options.ApiKey}");
    }

    /// <summary>
    /// Creates a chat completion with retry and circuit breaker.
    /// </summary>
    /// <param name="messages">List of chat messages.</param>
    /// <param name="model">Model to use (overrides default).</param>
    /// <param name="temperature">Temperature for generation (overrides default).</param>
    /// <param name="maxTokens">Maximum tokens for completion.</param>
    /// <param name="cancellationToken">Cancellation token.</param>
    /// <returns>Chat completion response.</returns>
    public async Task<ChatCompletionResponse> CreateChatCompletionAsync(
        List<ChatMessage> messages,
        string? model = null,
        float? temperature = null,
        int? maxTokens = null,
        CancellationToken cancellationToken = default)
    {
        var request = new ChatCompletionRequest
        {
            Model = model ?? _options.Model,
            Messages = messages,
            Temperature = temperature ?? _options.Temperature,
            MaxTokens = maxTokens ?? _options.MaxTokens
        };

        return await _retryService.ExecuteWithRetryAndCircuitBreakerAsync(
            "openai",
            async () => await SendChatCompletionRequestAsync(request, cancellationToken),
            maxRetries: 3,
            baseDelay: 2.0,
            maxDelay: 30.0);
    }

    /// <summary>
    /// Transcribes audio to text with word-level timestamps using Whisper.
    /// </summary>
    /// <param name="audioFilePath">Path to the audio file.</param>
    /// <param name="language">Language code (e.g., "en"). If null, auto-detects.</param>
    /// <param name="timestampGranularity">Granularity of timestamps ("word" or "segment").</param>
    /// <param name="cancellationToken">Cancellation token.</param>
    /// <returns>Transcription response with word-level timestamps.</returns>
    public async Task<TranscriptionResponse> TranscribeAudioAsync(
        string audioFilePath,
        string? language = null,
        string timestampGranularity = "word",
        CancellationToken cancellationToken = default)
    {
        return await _retryService.ExecuteWithRetryAndCircuitBreakerAsync(
            "openai",
            async () => await SendTranscriptionRequestAsync(audioFilePath, language, timestampGranularity, cancellationToken),
            maxRetries: 3,
            baseDelay: 2.0,
            maxDelay: 30.0);
    }

    /// <summary>
    /// Sends the actual HTTP request to OpenAI API.
    /// </summary>
    private async Task<ChatCompletionResponse> SendChatCompletionRequestAsync(
        ChatCompletionRequest request,
        CancellationToken cancellationToken)
    {
        var jsonContent = JsonSerializer.Serialize(request, new JsonSerializerOptions
        {
            PropertyNamingPolicy = JsonNamingPolicy.SnakeCaseLower,
            DefaultIgnoreCondition = JsonIgnoreCondition.WhenWritingNull
        });

        var content = new StringContent(jsonContent, Encoding.UTF8, "application/json");
        var response = await _httpClient.PostAsync("chat/completions", content, cancellationToken);

        if (!response.IsSuccessStatusCode)
        {
            var errorContent = await response.Content.ReadAsStringAsync(cancellationToken);
            _logger.LogError("OpenAI API error: {StatusCode} - {Error}", response.StatusCode, errorContent);
            throw new HttpRequestException($"OpenAI API returned {response.StatusCode}: {errorContent}");
        }

        var result = await response.Content.ReadFromJsonAsync<ChatCompletionResponse>(
            new JsonSerializerOptions
            {
                PropertyNamingPolicy = JsonNamingPolicy.SnakeCaseLower
            },
            cancellationToken);

        return result ?? throw new InvalidOperationException("Failed to deserialize OpenAI response");
    }

    /// <summary>
    /// Sends transcription request to OpenAI Whisper API.
    /// </summary>
    private async Task<TranscriptionResponse> SendTranscriptionRequestAsync(
        string audioFilePath,
        string? language,
        string timestampGranularity,
        CancellationToken cancellationToken)
    {
        using var form = new MultipartFormDataContent();
        using var fileStream = File.OpenRead(audioFilePath);
        using var fileContent = new StreamContent(fileStream);
        
        fileContent.Headers.ContentType = new System.Net.Http.Headers.MediaTypeHeaderValue("audio/mpeg");
        form.Add(fileContent, "file", Path.GetFileName(audioFilePath));
        form.Add(new StringContent("whisper-1"), "model");
        form.Add(new StringContent("verbose_json"), "response_format");
        form.Add(new StringContent(timestampGranularity), "timestamp_granularities[]");
        
        if (!string.IsNullOrEmpty(language))
        {
            form.Add(new StringContent(language), "language");
        }

        var response = await _httpClient.PostAsync("audio/transcriptions", form, cancellationToken);

        if (!response.IsSuccessStatusCode)
        {
            var errorContent = await response.Content.ReadAsStringAsync(cancellationToken);
            _logger.LogError("OpenAI Transcription API error: {StatusCode} - {Error}", response.StatusCode, errorContent);
            throw new HttpRequestException($"OpenAI Transcription API returned {response.StatusCode}: {errorContent}");
        }

        var result = await response.Content.ReadFromJsonAsync<TranscriptionResponse>(
            new JsonSerializerOptions
            {
                PropertyNamingPolicy = JsonNamingPolicy.SnakeCaseLower
            },
            cancellationToken);

        return result ?? throw new InvalidOperationException("Failed to deserialize transcription response");
    }
}

/// <summary>
/// Chat completion request model.
/// </summary>
public class ChatCompletionRequest
{
    [JsonPropertyName("model")]
    public string Model { get; set; } = string.Empty;

    [JsonPropertyName("messages")]
    public List<ChatMessage> Messages { get; set; } = new();

    [JsonPropertyName("temperature")]
    public float? Temperature { get; set; }

    [JsonPropertyName("max_tokens")]
    public int? MaxTokens { get; set; }
}

/// <summary>
/// Chat message model.
/// </summary>
public class ChatMessage
{
    [JsonPropertyName("role")]
    public string Role { get; set; } = string.Empty;

    [JsonPropertyName("content")]
    public string Content { get; set; } = string.Empty;

    public static ChatMessage System(string content) => new() { Role = "system", Content = content };
    public static ChatMessage User(string content) => new() { Role = "user", Content = content };
    public static ChatMessage Assistant(string content) => new() { Role = "assistant", Content = content };
}

/// <summary>
/// Chat completion response model.
/// </summary>
public class ChatCompletionResponse
{
    [JsonPropertyName("id")]
    public string Id { get; set; } = string.Empty;

    [JsonPropertyName("object")]
    public string Object { get; set; } = string.Empty;

    [JsonPropertyName("created")]
    public long Created { get; set; }

    [JsonPropertyName("model")]
    public string Model { get; set; } = string.Empty;

    [JsonPropertyName("choices")]
    public List<ChatChoice> Choices { get; set; } = new();

    [JsonPropertyName("usage")]
    public TokenUsage? Usage { get; set; }
}

/// <summary>
/// Chat choice model.
/// </summary>
public class ChatChoice
{
    [JsonPropertyName("index")]
    public int Index { get; set; }

    [JsonPropertyName("message")]
    public ChatMessage Message { get; set; } = new();

    [JsonPropertyName("finish_reason")]
    public string? FinishReason { get; set; }
}

/// <summary>
/// Token usage model.
/// </summary>
public class TokenUsage
{
    [JsonPropertyName("prompt_tokens")]
    public int PromptTokens { get; set; }

    [JsonPropertyName("completion_tokens")]
    public int CompletionTokens { get; set; }

    [JsonPropertyName("total_tokens")]
    public int TotalTokens { get; set; }
}

/// <summary>
/// Transcription response model for Whisper API.
/// </summary>
public class TranscriptionResponse
{
    [JsonPropertyName("text")]
    public string Text { get; set; } = string.Empty;

    [JsonPropertyName("language")]
    public string? Language { get; set; }

    [JsonPropertyName("duration")]
    public double Duration { get; set; }

    [JsonPropertyName("words")]
    public List<TranscriptionWord>? Words { get; set; }

    [JsonPropertyName("segments")]
    public List<TranscriptionSegment>? Segments { get; set; }
}

/// <summary>
/// Word-level transcription with timestamp.
/// </summary>
public class TranscriptionWord
{
    [JsonPropertyName("word")]
    public string Word { get; set; } = string.Empty;

    [JsonPropertyName("start")]
    public double Start { get; set; }

    [JsonPropertyName("end")]
    public double End { get; set; }
}

/// <summary>
/// Segment-level transcription with timestamp.
/// </summary>
public class TranscriptionSegment
{
    [JsonPropertyName("id")]
    public int Id { get; set; }

    [JsonPropertyName("seek")]
    public int Seek { get; set; }

    [JsonPropertyName("start")]
    public double Start { get; set; }

    [JsonPropertyName("end")]
    public double End { get; set; }

    [JsonPropertyName("text")]
    public string Text { get; set; } = string.Empty;

    [JsonPropertyName("tokens")]
    public List<int>? Tokens { get; set; }

    [JsonPropertyName("temperature")]
    public double Temperature { get; set; }

    [JsonPropertyName("avg_logprob")]
    public double AvgLogprob { get; set; }

    [JsonPropertyName("compression_ratio")]
    public double CompressionRatio { get; set; }

    [JsonPropertyName("no_speech_prob")]
    public double NoSpeechProb { get; set; }
}
