using System;
using System.Threading.Tasks;
using StoryGenerator.Models;
using StoryGenerator.Tools;

namespace StoryGenerator.Examples
{
    /// <summary>
    /// Example demonstrating voiceover generation and normalization.
    /// </summary>
    public class VoiceoverGenerationExample
    {
        public static async Task Main(string[] args)
        {
            Console.WriteLine("=== Voiceover Generation Example ===\n");

            // Initialize components
            var ttsClient = new PiperTTSClient(
                piperExecutable: "piper",
                maleModelPath: "en_US-lessac-medium.onnx",
                femaleModelPath: "en_US-amy-medium.onnx"
            );

            var ffmpegClient = new FFmpegClient();
            var voiceRecommender = new SimpleVoiceRecommender();

            var voiceoverGenerator = new VoiceoverGenerator(
                ttsClient,
                ffmpegClient,
                voiceRecommender,
                audioRoot: "audio"
            );

            // Check if TTS is available
            var isTTSAvailable = await ttsClient.IsTTSAvailableAsync();
            if (!isTTSAvailable)
            {
                Console.WriteLine("❌ Piper TTS is not available. Please install Piper TTS.");
                Console.WriteLine("   Visit: https://github.com/rhasspy/piper");
                return;
            }

            Console.WriteLine("✓ Piper TTS is available\n");

            // Example: Generate voiceover for different segments
            var segments = new[]
            {
                new AudienceSegment("men", "18-23"),
                new AudienceSegment("women", "18-23"),
                new AudienceSegment("men", "24-30"),
                new AudienceSegment("women", "24-30")
            };

            var sampleText = "Welcome to this amazing story about technology and innovation. " +
                           "In today's episode, we'll explore the fascinating world of artificial intelligence " +
                           "and how it's changing our lives.";

            foreach (var segment in segments)
            {
                try
                {
                    Console.WriteLine($"\n--- Processing segment: {segment} ---");

                    var result = await voiceoverGenerator.GenerateVoiceoverAsync(
                        titleId: "example_001",
                        title: "The Future of AI Technology",
                        text: sampleText,
                        segment: segment
                    );

                    if (result.Success)
                    {
                        Console.WriteLine($"✓ Voiceover generated successfully!");
                        Console.WriteLine($"  Voice Gender: {result.VoiceGender}");
                        Console.WriteLine($"  TTS Path: {result.TTSPath}");
                        Console.WriteLine($"  Normalized Path: {result.NormalizedPath}");
                        Console.WriteLine($"  LUFS JSON: {result.LufsJsonPath}");
                    }
                    else
                    {
                        Console.WriteLine($"❌ Voiceover generation failed for {segment}");
                    }
                }
                catch (Exception ex)
                {
                    Console.WriteLine($"❌ Error processing {segment}: {ex.Message}");
                }
            }

            Console.WriteLine("\n=== Voiceover Generation Complete ===");
        }
    }
}
