using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.IO;
using System.Linq;
using System.Text.Json;
using System.Threading.Tasks;
using StoryGenerator.Models;

namespace StoryGenerator.Tools
{
    /// <summary>
    /// Utility for comparing different video synthesis approaches
    /// Helps determine the best method for your use case
    /// </summary>
    public class VideoSynthesisComparator
    {
        private readonly Generators.LTXVideoSynthesizer _ltxSynthesizer;
        private readonly Generators.KeyframeVideoSynthesizer _keyframeSynthesizer;
        
        public VideoSynthesisComparator()
        {
            _ltxSynthesizer = new Generators.LTXVideoSynthesizer();
            
            var keyframeConfig = new Generators.KeyframeVideoConfig
            {
                TargetFps = 30,
                Method = Generators.InterpolationMethod.RIFE,
                Width = 1080,
                Height = 1920
            };
            _keyframeSynthesizer = new Generators.KeyframeVideoSynthesizer(keyframeConfig);
        }
        
        /// <summary>
        /// Compare all available video synthesis approaches
        /// </summary>
        /// <param name="testPrompt">Test scene description</param>
        /// <param name="testKeyframe">Optional test keyframe image</param>
        /// <param name="duration">Test video duration in seconds</param>
        /// <param name="outputDir">Directory for test outputs</param>
        /// <returns>Comparison results for each approach</returns>
        public async Task<Dictionary<string, VideoClip>> CompareApproachesAsync(
            string testPrompt,
            string testKeyframe = null,
            double duration = 10.0,
            string outputDir = null)
        {
            var results = new Dictionary<string, VideoClip>();
            
            // Use temp directory if not specified
            if (string.IsNullOrEmpty(outputDir))
            {
                outputDir = Path.Combine(
                    Path.GetTempPath(),
                    $"video_comparison_{Guid.NewGuid()}");
            }
            
            Directory.CreateDirectory(outputDir);
            
            Console.WriteLine("🔬 Starting Video Synthesis Comparison");
            Console.WriteLine($"Test Prompt: {testPrompt}");
            Console.WriteLine($"Duration: {duration}s");
            Console.WriteLine($"Output Directory: {outputDir}\n");
            Console.WriteLine(new string('=', 80));
            
            // Test LTX-Video
            Console.WriteLine("\n📹 Testing LTX-Video Approach...");
            Console.WriteLine(new string('-', 80));
            var ltxClip = await TestApproachAsync(
                "LTX-Video",
                Path.Combine(outputDir, "ltx_video_test.mp4"),
                async (output) => await _ltxSynthesizer.GenerateVideoAsync(
                    testPrompt, output, testKeyframe, (int)duration)
            );
            if (ltxClip != null)
            {
                ltxClip.SynthesisMethod = "LTX-Video";
                results["LTX-Video"] = ltxClip;
            }
            
            // Test SDXL + Frame Interpolation
            Console.WriteLine("\n🖼️  Testing SDXL + Frame Interpolation...");
            Console.WriteLine(new string('-', 80));
            var keyframeClip = await TestApproachAsync(
                "SDXL+RIFE",
                Path.Combine(outputDir, "sdxl_rife_test.mp4"),
                async (output) => await _keyframeSynthesizer.GenerateSceneAsync(
                    testPrompt, output, duration)
            );
            if (keyframeClip != null)
            {
                keyframeClip.SynthesisMethod = "SDXL+RIFE";
                results["SDXL+RIFE"] = keyframeClip;
            }
            
            // Print comparison
            Console.WriteLine("\n" + new string('=', 80));
            PrintComparison(results);
            
            // Save results to JSON
            await SaveComparisonResultsAsync(results, outputDir);
            
            return results;
        }
        
        /// <summary>
        /// Test a single approach and collect metrics
        /// </summary>
        private async Task<VideoClip> TestApproachAsync(
            string approachName,
            string outputPath,
            Func<string, Task<bool>> generateFunc)
        {
            try
            {
                Console.WriteLine($"Generating test video...");
                
                var stopwatch = Stopwatch.StartNew();
                bool success = await generateFunc(outputPath);
                stopwatch.Stop();
                
                if (!success || !File.Exists(outputPath))
                {
                    Console.WriteLine($"❌ {approachName} generation failed");
                    return null;
                }
                
                // Create video clip with metrics
                var clip = new VideoClip
                {
                    VideoPath = outputPath,
                    GenerationTime = stopwatch.Elapsed.TotalSeconds,
                    SynthesisMethod = approachName
                };
                
                // Analyze video properties
                await AnalyzeVideoAsync(clip);
                
                Console.WriteLine($"✅ {approachName} completed");
                Console.WriteLine($"   Generation Time: {clip.GenerationTime:F2}s");
                Console.WriteLine($"   File Size: {clip.FileSizeMB:F2} MB");
                Console.WriteLine($"   Resolution: {clip.ResolutionString}");
                
                return clip;
            }
            catch (Exception ex)
            {
                Console.WriteLine($"❌ {approachName} error: {ex.Message}");
                return null;
            }
        }
        
        /// <summary>
        /// Analyze video file and extract properties
        /// </summary>
        private async Task AnalyzeVideoAsync(VideoClip clip)
        {
            try
            {
                // Get file size
                var fileInfo = new FileInfo(clip.VideoPath);
                clip.FileSizeBytes = fileInfo.Length;
                
                // Use FFprobe to get video properties
                var ffprobeArgs = $"-v quiet -print_format json -show_streams \"{clip.VideoPath}\"";
                
                var processInfo = new ProcessStartInfo
                {
                    FileName = "ffprobe",
                    Arguments = ffprobeArgs,
                    RedirectStandardOutput = true,
                    UseShellExecute = false,
                    CreateNoWindow = true
                };
                
                using var process = Process.Start(processInfo);
                if (process == null)
                    return;
                
                string output = await process.StandardOutput.ReadToEndAsync();
                await process.WaitForExitAsync();
                
                if (process.ExitCode == 0 && !string.IsNullOrEmpty(output))
                {
                    // Parse JSON output
                    var ffprobeData = JsonDocument.Parse(output);
                    var streams = ffprobeData.RootElement.GetProperty("streams");
                    
                    foreach (var stream in streams.EnumerateArray())
                    {
                        if (stream.GetProperty("codec_type").GetString() == "video")
                        {
                            int width = stream.GetProperty("width").GetInt32();
                            int height = stream.GetProperty("height").GetInt32();
                            clip.Resolution = (width, height);
                            
                            if (stream.TryGetProperty("avg_frame_rate", out var fpsElement))
                            {
                                string fpsStr = fpsElement.GetString();
                                if (fpsStr.Contains('/'))
                                {
                                    var parts = fpsStr.Split('/');
                                    if (parts.Length == 2 &&
                                        double.TryParse(parts[0], out double num) &&
                                        double.TryParse(parts[1], out double den) &&
                                        den != 0)
                                    {
                                        clip.Fps = (int)(num / den);
                                    }
                                }
                            }
                            
                            if (stream.TryGetProperty("duration", out var durationElement))
                            {
                                if (durationElement.TryGetDouble(out double duration))
                                {
                                    clip.EndTime = duration;
                                }
                            }
                            
                            break;
                        }
                    }
                }
            }
            catch (Exception ex)
            {
                Console.WriteLine($"⚠️ Video analysis warning: {ex.Message}");
            }
        }
        
        /// <summary>
        /// Print comparison table to console
        /// </summary>
        private void PrintComparison(Dictionary<string, VideoClip> results)
        {
            Console.WriteLine("COMPARISON RESULTS");
            Console.WriteLine(new string('=', 80));
            
            if (!results.Any())
            {
                Console.WriteLine("No results to compare.");
                return;
            }
            
            // Header
            Console.WriteLine($"\n{"Metric",-30} {string.Join(" | ", results.Keys.Select(k => $"{k,-20}"))}");
            Console.WriteLine(new string('-', 80));
            
            // Generation Time
            Console.Write($"{"Generation Time (s)",-30} ");
            foreach (var clip in results.Values)
            {
                Console.Write($"{clip.GenerationTime,-20:F2} | ");
            }
            Console.WriteLine();
            
            // File Size
            Console.Write($"{"File Size (MB)",-30} ");
            foreach (var clip in results.Values)
            {
                Console.Write($"{clip.FileSizeMB,-20:F2} | ");
            }
            Console.WriteLine();
            
            // Resolution
            Console.Write($"{"Resolution",-30} ");
            foreach (var clip in results.Values)
            {
                Console.Write($"{clip.ResolutionString,-20} | ");
            }
            Console.WriteLine();
            
            // FPS
            Console.Write($"{"FPS",-30} ");
            foreach (var clip in results.Values)
            {
                Console.Write($"{clip.Fps,-20} | ");
            }
            Console.WriteLine();
            
            // Duration
            Console.Write($"{"Duration (s)",-30} ");
            foreach (var clip in results.Values)
            {
                Console.Write($"{clip.Duration,-20:F2} | ");
            }
            Console.WriteLine();
            
            Console.WriteLine(new string('=', 80));
            
            // Recommendation
            Console.WriteLine("\n💡 RECOMMENDATION:");
            var winner = DetermineWinner(results);
            Console.WriteLine($"   Best overall: {winner.Key}");
            Console.WriteLine($"   Reason: {winner.Value}");
        }
        
        /// <summary>
        /// Determine the best approach based on metrics
        /// </summary>
        private KeyValuePair<string, string> DetermineWinner(
            Dictionary<string, VideoClip> results)
        {
            if (!results.Any())
                return new KeyValuePair<string, string>("None", "No results available");
            
            // Score each approach
            var scores = new Dictionary<string, (double Score, string Reason)>();
            
            foreach (var kvp in results)
            {
                var clip = kvp.Value;
                double score = 0;
                var reasons = new List<string>();
                
                // Faster generation is better (weighted 30%)
                double speedScore = Math.Max(0, 100.0 - clip.GenerationTime * 2);
                score += speedScore * 0.3;
                
                // Smaller file size is better (weighted 20%)
                double sizeScore = Math.Max(0, 100.0 - clip.FileSizeMB * 5);
                score += sizeScore * 0.2;
                
                // Correct resolution (weighted 20%)
                if (clip.Resolution.Width == 1080 && clip.Resolution.Height == 1920)
                {
                    score += 20;
                    reasons.Add("correct resolution");
                }
                
                // Good FPS (weighted 15%)
                if (clip.Fps >= 24 && clip.Fps <= 30)
                {
                    score += 15;
                    reasons.Add("optimal FPS");
                }
                
                // Reasonable file size (weighted 15%)
                if (clip.FileSizeMB > 0 && clip.FileSizeMB < 50)
                {
                    score += 15;
                    reasons.Add("efficient encoding");
                }
                
                string reasonStr = reasons.Any()
                    ? string.Join(", ", reasons)
                    : "acceptable quality";
                
                scores[kvp.Key] = (score, reasonStr);
            }
            
            var winner = scores.OrderByDescending(kvp => kvp.Value.Score).First();
            return new KeyValuePair<string, string>(winner.Key, winner.Value.Reason);
        }
        
        /// <summary>
        /// Save comparison results to JSON file
        /// </summary>
        private async Task SaveComparisonResultsAsync(
            Dictionary<string, VideoClip> results,
            string outputDir)
        {
            try
            {
                string jsonPath = Path.Combine(outputDir, "comparison_results.json");
                
                var options = new JsonSerializerOptions
                {
                    WriteIndented = true,
                    PropertyNamingPolicy = JsonNamingPolicy.CamelCase
                };
                
                string json = JsonSerializer.Serialize(results, options);
                await File.WriteAllTextAsync(jsonPath, json);
                
                Console.WriteLine($"\n📄 Results saved to: {jsonPath}");
            }
            catch (Exception ex)
            {
                Console.WriteLine($"⚠️ Failed to save results: {ex.Message}");
            }
        }
    }
}
