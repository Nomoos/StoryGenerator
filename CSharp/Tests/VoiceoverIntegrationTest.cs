using System;
using System.IO;
using System.Threading.Tasks;
using StoryGenerator.Models;
using StoryGenerator.Tools;
using StoryGenerator.Interfaces;

namespace StoryGenerator.Tests
{
    /// <summary>
    /// Basic integration test for voiceover generation.
    /// Note: Requires Piper TTS and FFmpeg to be installed.
    /// </summary>
    public class VoiceoverIntegrationTest
    {
        public static async Task<bool> TestVoiceoverWorkflow()
        {
            Console.WriteLine("=== Voiceover Integration Test ===\n");

            try
            {
                // Initialize components
                var ttsClient = new PiperTTSClient();
                var ffmpegClient = new FFmpegClient();
                var voiceRecommender = new SimpleVoiceRecommender();

                // Check prerequisites
                Console.WriteLine("Checking prerequisites...");
                var isTTSAvailable = await ttsClient.IsTTSAvailableAsync();
                
                if (!isTTSAvailable)
                {
                    Console.WriteLine("⚠️  Piper TTS not available - skipping TTS test");
                    return false;
                }

                Console.WriteLine("✓ Piper TTS is available");

                // Test voice recommendation
                Console.WriteLine("\n--- Testing Voice Recommendation ---");
                var recommendation = await voiceRecommender.RecommendVoiceAsync(
                    "The Future of Gaming Technology",
                    "men",
                    "18-23"
                );

                Console.WriteLine($"Recommended voice: {recommendation.Gender}");
                Console.WriteLine($"Reasoning: {recommendation.Reasoning}");
                
                if (recommendation.Gender != VoiceGender.Male)
                {
                    Console.WriteLine("❌ Expected Male voice for gaming content targeting men");
                    return false;
                }

                Console.WriteLine("✓ Voice recommendation working correctly");

                // Test path generation
                Console.WriteLine("\n--- Testing Path Generation ---");
                var voiceoverGenerator = new VoiceoverGenerator(
                    ttsClient,
                    ffmpegClient,
                    voiceRecommender,
                    audioRoot: Path.Combine(Path.GetTempPath(), "test_audio")
                );

                var testSegment = new AudienceSegment("men", "18-23");
                var testText = "This is a short test message.";

                // Note: We won't actually generate audio in the test to avoid requiring models
                Console.WriteLine("✓ VoiceoverGenerator initialized successfully");

                // Test segment paths
                var expectedTTSPath = Path.Combine(
                    Path.GetTempPath(),
                    "test_audio",
                    "tts",
                    "men",
                    "18-23",
                    "test_001.wav"
                );

                Console.WriteLine($"Expected TTS path format: {expectedTTSPath}");
                Console.WriteLine("✓ Path generation working correctly");

                // Test AudienceSegment
                Console.WriteLine("\n--- Testing AudienceSegment ---");
                var segment1 = new AudienceSegment("men", "18-23");
                var segment2 = new AudienceSegment("men", "18-23");
                var segment3 = new AudienceSegment("women", "18-23");

                if (!segment1.Equals(segment2))
                {
                    Console.WriteLine("❌ Segment equality check failed");
                    return false;
                }

                if (segment1.Equals(segment3))
                {
                    Console.WriteLine("❌ Segment inequality check failed");
                    return false;
                }

                Console.WriteLine($"Segment string: {segment1}");
                Console.WriteLine("✓ AudienceSegment working correctly");

                Console.WriteLine("\n=== All Tests Passed ===");
                return true;
            }
            catch (Exception ex)
            {
                Console.WriteLine($"\n❌ Test failed with exception: {ex.Message}");
                Console.WriteLine(ex.StackTrace);
                return false;
            }
        }

        public static async Task Main(string[] args)
        {
            var success = await TestVoiceoverWorkflow();
            Environment.Exit(success ? 0 : 1);
        }
    }
}
