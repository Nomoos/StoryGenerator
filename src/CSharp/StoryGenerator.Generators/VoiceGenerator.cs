using Microsoft.Extensions.Logging;
using StoryGenerator.Core.Services;
using StoryGenerator.Providers.ElevenLabs;

namespace StoryGenerator.Generators;

/// <summary>
/// Generates voiceovers from scripts using ElevenLabs TTS.
/// Ported from Python Generators/GVoice.py with C# enhancements.
/// </summary>
public class VoiceGenerator : IVoiceGenerator
{
    private readonly ElevenLabsClient _elevenLabsClient;
    private readonly ILogger<VoiceGenerator> _logger;
    private readonly PerformanceMonitor _performanceMonitor;

    public string Name => "VoiceGenerator";
    public string Version => "1.0.0";

    public VoiceGenerator(
        ElevenLabsClient elevenLabsClient,
        ILogger<VoiceGenerator> logger,
        PerformanceMonitor performanceMonitor)
    {
        _elevenLabsClient = elevenLabsClient;
        _logger = logger;
        _performanceMonitor = performanceMonitor;
    }

    public async Task<byte[]> GenerateAudioAsync(
        string scriptText,
        string? voiceId = null,
        float? voiceStability = null,
        float? voiceSimilarityBoost = null,
        float? voiceStyleExaggeration = null,
        CancellationToken cancellationToken = default)
    {
        return await _performanceMonitor.MeasureAsync(
            "TTS_Generation",
            "Audio",
            async () => await GenerateAudioInternalAsync(
                scriptText,
                voiceId,
                voiceStability,
                voiceSimilarityBoost,
                voiceStyleExaggeration,
                cancellationToken),
            new Dictionary<string, object>
            {
                { "script_length", scriptText.Length },
                { "word_count", scriptText.Split(' ', StringSplitOptions.RemoveEmptyEntries).Length }
            });
    }

    private async Task<byte[]> GenerateAudioInternalAsync(
        string scriptText,
        string? voiceId,
        float? voiceStability,
        float? voiceSimilarityBoost,
        float? voiceStyleExaggeration,
        CancellationToken cancellationToken)
    {
        var voiceSettings = new VoiceSettings
        {
            Stability = voiceStability ?? 0.5f,
            SimilarityBoost = voiceSimilarityBoost ?? 0.75f,
            Style = voiceStyleExaggeration ?? 0.0f
        };

        _logger.LogInformation("Generating audio ({Words} words)", 
            scriptText.Split(' ', StringSplitOptions.RemoveEmptyEntries).Length);

        var audioData = await _elevenLabsClient.GenerateAudioAsync(
            scriptText,
            voiceId,
            voiceSettings,
            cancellationToken);

        _logger.LogInformation("✅ Audio generated: {Size} bytes", audioData.Length);

        return audioData;
    }

    public async Task<string> GenerateAndSaveAudioAsync(
        string scriptText,
        string outputPath,
        string? voiceId = null,
        float? voiceStability = null,
        float? voiceSimilarityBoost = null,
        float? voiceStyleExaggeration = null,
        CancellationToken cancellationToken = default)
    {
        var audioData = await GenerateAudioAsync(
            scriptText,
            voiceId,
            voiceStability,
            voiceSimilarityBoost,
            voiceStyleExaggeration,
            cancellationToken);

        // Ensure output directory exists
        var directory = Path.GetDirectoryName(outputPath);
        if (!string.IsNullOrEmpty(directory))
        {
            Directory.CreateDirectory(directory);
        }

        // Save audio file
        await File.WriteAllBytesAsync(outputPath, audioData, cancellationToken);

        _logger.LogInformation("Saved audio to: {OutputPath}", outputPath);

        return outputPath;
    }
}
