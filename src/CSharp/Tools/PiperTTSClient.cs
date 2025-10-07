using System;
using System.IO;
using System.Threading;
using System.Threading.Tasks;
using StoryGenerator.Interfaces;
using StoryGenerator.Models;

namespace StoryGenerator.Tools
{
    /// <summary>
    /// Client for generating voiceover audio using Piper TTS.
    /// Piper is a fast, local neural text to speech system.
    /// </summary>
    public class PiperTTSClient : ITTSClient
    {
        private readonly string _piperExecutable;
        private readonly string _maleModelPath;
        private readonly string _femaleModelPath;

        /// <summary>
        /// Initialize Piper TTS client.
        /// </summary>
        /// <param name="piperExecutable">Path to piper executable (defaults to "piper" in PATH)</param>
        /// <param name="maleModelPath">Path to male voice model file</param>
        /// <param name="femaleModelPath">Path to female voice model file</param>
        public PiperTTSClient(
            string piperExecutable = "piper",
            string? maleModelPath = null,
            string? femaleModelPath = null)
        {
            _piperExecutable = piperExecutable;
            _maleModelPath = maleModelPath ?? "en_US-lessac-medium.onnx";
            _femaleModelPath = femaleModelPath ?? "en_US-amy-medium.onnx";
        }

        /// <summary>
        /// Generate voiceover audio from text using Piper TTS.
        /// </summary>
        public async Task GenerateVoiceoverAsync(
            string text,
            string outputPath,
            VoiceGender voiceGender,
            int sampleRate = 48000,
            CancellationToken cancellationToken = default)
        {
            if (string.IsNullOrWhiteSpace(text))
            {
                throw new ArgumentException("Text cannot be empty", nameof(text));
            }

            if (string.IsNullOrWhiteSpace(outputPath))
            {
                throw new ArgumentException("Output path cannot be empty", nameof(outputPath));
            }

            // Ensure output directory exists
            var outputDir = Path.GetDirectoryName(outputPath);
            if (!string.IsNullOrEmpty(outputDir) && !Directory.Exists(outputDir))
            {
                Directory.CreateDirectory(outputDir);
            }

            // Select voice model based on gender
            var modelPath = voiceGender == VoiceGender.Male ? _maleModelPath : _femaleModelPath;

            // Build piper command
            // piper --model <model> --output_file <output> < input.txt
            var arguments = $"--model \"{modelPath}\" --output_file \"{outputPath}\"";

            if (sampleRate != 22050) // Piper default is 22050
            {
                arguments += $" --sample_rate {sampleRate}";
            }

            var startInfo = new System.Diagnostics.ProcessStartInfo
            {
                FileName = _piperExecutable,
                Arguments = arguments,
                RedirectStandardInput = true,
                RedirectStandardOutput = true,
                RedirectStandardError = true,
                UseShellExecute = false,
                CreateNoWindow = true
            };

            using var process = new System.Diagnostics.Process { StartInfo = startInfo };

            try
            {
                process.Start();

                // Write text to stdin
                await process.StandardInput.WriteAsync(text);
                await process.StandardInput.FlushAsync();
                process.StandardInput.Close();

                var errorTask = process.StandardError.ReadToEndAsync();

                await process.WaitForExitAsync(cancellationToken);

                var error = await errorTask;

                if (process.ExitCode != 0)
                {
                    throw new Exception($"Piper TTS failed with exit code {process.ExitCode}: {error}");
                }

                if (!File.Exists(outputPath))
                {
                    throw new Exception($"Piper TTS did not generate output file: {outputPath}");
                }
            }
            catch (Exception ex)
            {
                throw new Exception($"Failed to generate voiceover with Piper TTS: {ex.Message}", ex);
            }
        }

        /// <summary>
        /// Check if Piper TTS is available.
        /// </summary>
        public async Task<bool> IsTTSAvailableAsync()
        {
            try
            {
                var startInfo = new System.Diagnostics.ProcessStartInfo
                {
                    FileName = _piperExecutable,
                    Arguments = "--version",
                    RedirectStandardOutput = true,
                    RedirectStandardError = true,
                    UseShellExecute = false,
                    CreateNoWindow = true
                };

                using var process = new System.Diagnostics.Process { StartInfo = startInfo };
                process.Start();
                await process.WaitForExitAsync();

                return process.ExitCode == 0;
            }
            catch
            {
                return false;
            }
        }
    }
}
