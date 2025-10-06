using System;
using System.IO;
using System.Threading.Tasks;
using StoryGenerator.Research;

namespace StoryGenerator.Research.Examples
{
    /// <summary>
    /// Example usage of WhisperClient for ASR transcription.
    /// </summary>
    public class WhisperExample
    {
        public static async Task Main(string[] args)
        {
            Console.WriteLine("Whisper ASR Example");
            Console.WriteLine("===================\n");

            // Check for audio file argument
            if (args.Length == 0)
            {
                Console.WriteLine("Usage: WhisperExample <audio-file-path>");
                Console.WriteLine("\nExample:");
                Console.WriteLine("  WhisperExample audio.mp3");
                return;
            }

            string audioPath = args[0];

            if (!File.Exists(audioPath))
            {
                Console.WriteLine($"Error: Audio file not found: {audioPath}");
                return;
            }

            Console.WriteLine($"Audio file: {audioPath}\n");

            try
            {
                // Example 1: Basic transcription
                await BasicTranscriptionExample(audioPath);

                // Example 2: Language detection
                await LanguageDetectionExample(audioPath);

                // Example 3: Generate SRT subtitles
                await SrtGenerationExample(audioPath);

                // Example 4: Generate VTT subtitles
                await VttGenerationExample(audioPath);

                // Example 5: Transcription with different model sizes
                await DifferentModelSizeExample(audioPath);
            }
            catch (Exception ex)
            {
                Console.WriteLine($"\nError: {ex.Message}");
                if (ex.InnerException != null)
                {
                    Console.WriteLine($"Inner error: {ex.InnerException.Message}");
                }
            }
        }

        /// <summary>
        /// Example 1: Basic transcription with word timestamps.
        /// </summary>
        private static async Task BasicTranscriptionExample(string audioPath)
        {
            Console.WriteLine("Example 1: Basic Transcription");
            Console.WriteLine("-------------------------------");

            // Initialize client with large-v3 model
            var client = new WhisperClient(
                modelSize: "large-v3",
                device: "auto",
                computeType: "float16"
            );

            Console.WriteLine("Transcribing audio...");
            var result = await client.TranscribeAsync(
                audioPath,
                language: "en",
                wordTimestamps: true
            );

            Console.WriteLine($"\nFull Transcription:");
            Console.WriteLine($"{result.Text}\n");

            Console.WriteLine($"Language: {result.Language} (confidence: {result.LanguageProbability:P2})");
            Console.WriteLine($"Segments: {result.Segments.Count}");
            Console.WriteLine($"Words: {result.Words?.Count ?? 0}\n");

            // Show first few words with timestamps
            if (result.Words != null && result.Words.Count > 0)
            {
                Console.WriteLine("First 10 words with timestamps:");
                for (int i = 0; i < Math.Min(10, result.Words.Count); i++)
                {
                    var word = result.Words[i];
                    Console.WriteLine($"  [{word.Start:F2}s - {word.End:F2}s] {word.Word} (confidence: {word.Confidence:F3})");
                }
            }

            Console.WriteLine();
        }

        /// <summary>
        /// Example 2: Detect language of audio file.
        /// </summary>
        private static async Task LanguageDetectionExample(string audioPath)
        {
            Console.WriteLine("Example 2: Language Detection");
            Console.WriteLine("------------------------------");

            var client = new WhisperClient(modelSize: "base");

            Console.WriteLine("Detecting language...");
            var (language, confidence) = await client.DetectLanguageAsync(audioPath);

            Console.WriteLine($"Detected Language: {language}");
            Console.WriteLine($"Confidence: {confidence:P2}\n");
        }

        /// <summary>
        /// Example 3: Generate SRT subtitle file.
        /// </summary>
        private static async Task SrtGenerationExample(string audioPath)
        {
            Console.WriteLine("Example 3: SRT Subtitle Generation");
            Console.WriteLine("-----------------------------------");

            var client = new WhisperClient(modelSize: "large-v3");

            string srtPath = Path.ChangeExtension(audioPath, ".srt");
            Console.WriteLine($"Generating SRT subtitles to: {srtPath}");

            var srtContent = await client.TranscribeToSrtAsync(
                audioPath,
                outputPath: srtPath,
                language: "en",
                maxWordsPerLine: 10
            );

            Console.WriteLine("SRT generated successfully!");
            Console.WriteLine("\nFirst 500 characters of SRT:");
            Console.WriteLine(srtContent.Substring(0, Math.Min(500, srtContent.Length)));
            Console.WriteLine();
        }

        /// <summary>
        /// Example 4: Generate VTT subtitle file.
        /// </summary>
        private static async Task VttGenerationExample(string audioPath)
        {
            Console.WriteLine("Example 4: VTT Subtitle Generation");
            Console.WriteLine("-----------------------------------");

            var client = new WhisperClient(modelSize: "large-v3");

            string vttPath = Path.ChangeExtension(audioPath, ".vtt");
            Console.WriteLine($"Generating VTT subtitles to: {vttPath}");

            var vttContent = await client.TranscribeToVttAsync(
                audioPath,
                outputPath: vttPath,
                language: "en",
                maxWordsPerLine: 10
            );

            Console.WriteLine("VTT generated successfully!");
            Console.WriteLine("\nFirst 500 characters of VTT:");
            Console.WriteLine(vttContent.Substring(0, Math.Min(500, vttContent.Length)));
            Console.WriteLine();
        }

        /// <summary>
        /// Example 5: Compare different model sizes.
        /// </summary>
        private static async Task DifferentModelSizeExample(string audioPath)
        {
            Console.WriteLine("Example 5: Different Model Sizes");
            Console.WriteLine("---------------------------------");

            var modelSizes = new[] { "tiny", "base", "small" };

            foreach (var modelSize in modelSizes)
            {
                Console.WriteLine($"\nTesting with {modelSize} model...");
                
                var client = new WhisperClient(
                    modelSize: modelSize,
                    device: "auto"
                );

                var startTime = DateTime.Now;
                var result = await client.TranscribeAsync(
                    audioPath,
                    wordTimestamps: false
                );
                var elapsed = (DateTime.Now - startTime).TotalSeconds;

                Console.WriteLine($"  Time: {elapsed:F2}s");
                Console.WriteLine($"  Language: {result.Language} ({result.LanguageProbability:P2})");
                Console.WriteLine($"  Text length: {result.Text.Length} chars");
                Console.WriteLine($"  First 100 chars: {result.Text.Substring(0, Math.Min(100, result.Text.Length))}...");
            }

            Console.WriteLine();
        }
    }
}
