using System;
using System.Threading.Tasks;
using StoryGenerator.Interfaces;
using StoryGenerator.Models;
using StoryGenerator.Tools;

namespace StoryGenerator.Examples
{
    /// <summary>
    /// Example demonstrating versioned voiceover generation for quality comparison.
    /// Shows how to generate multiple versions of the same content for A/B testing.
    /// </summary>
    public class VoiceoverGenerationExample
    {
        public static async Task Main(string[] args)
        {
            Console.WriteLine("=== Versioned Voiceover Generation Example ===\n");

            // Check if TTS is available first
            var ttsClient = new PiperTTSClient(
                piperExecutable: "piper",
                maleModelPath: "en_US-lessac-medium.onnx",
                femaleModelPath: "en_US-amy-medium.onnx"
            );

            var isTTSAvailable = await ttsClient.IsTTSAvailableAsync();
            if (!isTTSAvailable)
            {
                Console.WriteLine("❌ Piper TTS is not available. Please install Piper TTS.");
                Console.WriteLine("   Visit: https://github.com/rhasspy/piper");
                Console.WriteLine("\n   For demonstration purposes, showing the workflow structure:");
                DemonstrateWorkflowStructure();
                return;
            }

            Console.WriteLine("✓ Piper TTS is available\n");

            // Initialize components
            var ffmpegClient = new FFmpegClient();
            var voiceRecommender = new SimpleVoiceRecommender();

            // Create orchestrators for different versions
            var orchestratorV1 = new VoiceoverOrchestrator(
                ttsClient,
                ffmpegClient,
                voiceRecommender,
                versionIdentifier: "v1",
                audioRoot: "audio"
            );

            var orchestratorV2 = new VoiceoverOrchestrator(
                ttsClient,
                ffmpegClient,
                voiceRecommender,
                versionIdentifier: "v2",
                audioRoot: "audio"
            );

            // Sample content for different audience segments
            var segments = new[]
            {
                new AudienceSegment("men", "18-23"),
                new AudienceSegment("women", "18-23")
            };

            var sampleText = "Welcome to this amazing story about technology and innovation. " +
                           "In today's episode, we'll explore the fascinating world of artificial intelligence " +
                           "and how it's changing our lives.";

            foreach (var segment in segments)
            {
                try
                {
                    Console.WriteLine($"\n=== Processing segment: {segment} ===\n");

                    // Generate Version 1
                    var requestV1 = new VoiceoverRequest
                    {
                        TitleId = "tech_story_001",
                        Title = "The Future of AI Technology",
                        Text = sampleText,
                        Segment = segment
                    };

                    var resultV1 = await orchestratorV1.GenerateVoiceoverAsync(requestV1);

                    if (resultV1.Success)
                    {
                        Console.WriteLine($"\n✓ Version 1 generated successfully!");
                        Console.WriteLine($"  Voice: {resultV1.VoiceGender}");
                        Console.WriteLine($"  TTS: {resultV1.TTSPath}");
                        Console.WriteLine($"  Normalized: {resultV1.NormalizedPath}");
                        Console.WriteLine($"  Timings: TTS={resultV1.TtsDuration:F2}s, Norm={resultV1.NormalizationDuration:F2}s");
                    }

                    // Generate Version 2 (for comparison)
                    Console.WriteLine($"\n--- Generating Version 2 for comparison ---");
                    
                    var requestV2 = new VoiceoverRequest
                    {
                        TitleId = "tech_story_001",
                        Title = "The Future of AI Technology",
                        Text = sampleText,
                        Segment = segment
                    };

                    var resultV2 = await orchestratorV2.GenerateVoiceoverAsync(requestV2);

                    if (resultV2.Success)
                    {
                        Console.WriteLine($"\n✓ Version 2 generated successfully!");
                        Console.WriteLine($"  Voice: {resultV2.VoiceGender}");
                        Console.WriteLine($"  TTS: {resultV2.TTSPath}");
                        Console.WriteLine($"  Normalized: {resultV2.NormalizedPath}");
                        Console.WriteLine($"  Timings: TTS={resultV2.TtsDuration:F2}s, Norm={resultV2.NormalizationDuration:F2}s");
                    }

                    Console.WriteLine($"\n--- Quality Comparison ---");
                    Console.WriteLine($"Both versions are saved separately for quality review.");
                    Console.WriteLine($"Compare files to determine which version performs better.");
                }
                catch (Exception ex)
                {
                    Console.WriteLine($"❌ Error processing {segment}: {ex.Message}");
                }
            }

            Console.WriteLine("\n=== Voiceover Generation Complete ===");
            Console.WriteLine("\nFile Structure:");
            Console.WriteLine("  audio/tts/{gender}/{age}/{titleId}_v1.wav");
            Console.WriteLine("  audio/tts/{gender}/{age}/{titleId}_v2.wav");
            Console.WriteLine("  audio/normalized/{gender}/{age}/{titleId}_v1_lufs.wav");
            Console.WriteLine("  audio/normalized/{gender}/{age}/{titleId}_v2_lufs.wav");
            Console.WriteLine("  audio/normalized/{gender}/{age}/{titleId}_v1_lufs.json");
            Console.WriteLine("  audio/normalized/{gender}/{age}/{titleId}_v2_lufs.json");
        }

        private static void DemonstrateWorkflowStructure()
        {
            Console.WriteLine("\n=== Voiceover Generation Workflow ===\n");
            Console.WriteLine("1. Voice Recommendation");
            Console.WriteLine("   - Analyzes title and audience segment");
            Console.WriteLine("   - Selects appropriate voice gender (M/F)");
            Console.WriteLine();
            Console.WriteLine("2. TTS Generation");
            Console.WriteLine("   - Generates audio using local Piper TTS");
            Console.WriteLine("   - Output: 48 kHz WAV format");
            Console.WriteLine("   - Location: /audio/tts/{segment}/{age}/{titleId}_{version}.wav");
            Console.WriteLine();
            Console.WriteLine("3. Audio Normalization");
            Console.WriteLine("   - Applies FFmpeg loudnorm filter");
            Console.WriteLine("   - Target: -14 LUFS (EBU R128 standard)");
            Console.WriteLine("   - Two-pass for accuracy");
            Console.WriteLine("   - Output: /audio/normalized/{segment}/{age}/{titleId}_{version}_lufs.wav");
            Console.WriteLine();
            Console.WriteLine("4. Metadata Storage");
            Console.WriteLine("   - Saves LUFS measurements as JSON");
            Console.WriteLine("   - Includes version, timings, and normalization parameters");
            Console.WriteLine("   - Location: /audio/normalized/{segment}/{age}/{titleId}_{version}_lufs.json");
            Console.WriteLine();
            Console.WriteLine("=== Version Management ===");
            Console.WriteLine("- Each version (v1, v2, etc.) is saved separately");
            Console.WriteLine("- Enables quality comparison and A/B testing");
            Console.WriteLine("- Original Python generation remains untouched");
            Console.WriteLine("- All versions coexist for quality tracking");
        }
    }
}
