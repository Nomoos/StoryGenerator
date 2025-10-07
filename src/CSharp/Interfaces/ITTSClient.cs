using System.Threading;
using System.Threading.Tasks;
using StoryGenerator.Models;

namespace StoryGenerator.Interfaces
{
    /// <summary>
    /// Interface for Text-to-Speech client operations.
    /// Provides methods for generating voiceover audio using local TTS.
    /// </summary>
    public interface ITTSClient
    {
        /// <summary>
        /// Generate voiceover audio from text using local TTS.
        /// </summary>
        /// <param name="text">Text to convert to speech</param>
        /// <param name="outputPath">Output path for the generated audio file (WAV format)</param>
        /// <param name="voiceGender">Voice gender (Male or Female)</param>
        /// <param name="sampleRate">Sample rate in Hz (default 48000)</param>
        /// <param name="cancellationToken">Cancellation token</param>
        /// <returns>Task representing the async operation</returns>
        Task GenerateVoiceoverAsync(
            string text,
            string outputPath,
            VoiceGender voiceGender,
            int sampleRate = 48000,
            CancellationToken cancellationToken = default);

        /// <summary>
        /// Check if the TTS engine is available and properly configured.
        /// </summary>
        /// <returns>True if TTS is available, false otherwise</returns>
        Task<bool> IsTTSAvailableAsync();
    }
}
