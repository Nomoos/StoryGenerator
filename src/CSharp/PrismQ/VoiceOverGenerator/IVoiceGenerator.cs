using PrismQ.Shared.Interfaces;
namespace PrismQ.VoiceOverGenerator;

/// <summary>
/// Interface for generating voiceovers from scripts using TTS.
/// Ported from Python Generators/GVoice.py.
/// </summary>
public interface IVoiceGenerator : IGenerator
{
    /// <summary>
    /// Generates audio from a script using text-to-speech.
    /// </summary>
    /// <param name="scriptText">The script text to convert to speech.</param>
    /// <param name="voiceId">The voice ID to use (ElevenLabs voice ID).</param>
    /// <param name="voiceStability">Voice stability parameter (0.0 to 1.0).</param>
    /// <param name="voiceSimilarityBoost">Voice similarity boost parameter (0.0 to 1.0).</param>
    /// <param name="voiceStyleExaggeration">Voice style exaggeration parameter (0.0 to 1.0).</param>
    /// <param name="cancellationToken">Cancellation token.</param>
    /// <returns>The generated audio as a byte array.</returns>
    Task<byte[]> GenerateAudioAsync(
        string scriptText,
        string? voiceId = null,
        float? voiceStability = null,
        float? voiceSimilarityBoost = null,
        float? voiceStyleExaggeration = null,
        CancellationToken cancellationToken = default);

    /// <summary>
    /// Generates audio and saves it to the specified path with LUFS normalization.
    /// </summary>
    /// <param name="scriptText">The script text to convert to speech.</param>
    /// <param name="outputPath">Path to save the generated audio (MP3 format).</param>
    /// <param name="voiceId">The voice ID to use (optional).</param>
    /// <param name="voiceStability">Voice stability parameter (optional).</param>
    /// <param name="voiceSimilarityBoost">Voice similarity boost parameter (optional).</param>
    /// <param name="voiceStyleExaggeration">Voice style exaggeration parameter (optional).</param>
    /// <param name="cancellationToken">Cancellation token.</param>
    /// <returns>Path to the saved audio file.</returns>
    Task<string> GenerateAndSaveAudioAsync(
        string scriptText,
        string outputPath,
        string? voiceId = null,
        float? voiceStability = null,
        float? voiceSimilarityBoost = null,
        float? voiceStyleExaggeration = null,
        CancellationToken cancellationToken = default);
}
