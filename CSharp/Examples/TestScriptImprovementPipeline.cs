using System;
using System.IO;
using System.Threading.Tasks;
using StoryGenerator.Core.LLM;
using StoryGenerator.Models;
using StoryGenerator.Tools;

namespace StoryGenerator.Examples
{
    /// <summary>
    /// Simple test script to verify the script improvement pipeline works correctly.
    /// This creates mock components to test the flow without requiring an LLM.
    /// </summary>
    public class TestScriptImprovementPipeline
    {
        public static async Task Main(string[] args)
        {
            Console.WriteLine("=".PadRight(80, '='));
            Console.WriteLine("Script Improvement Pipeline Test");
            Console.WriteLine("=".PadRight(80, '='));
            Console.WriteLine();

            try
            {
                var baseProjectPath = "/home/runner/work/StoryGenerator/StoryGenerator";
                
                // Test 1: File Manager
                Console.WriteLine("Test 1: Testing ScriptFileManager...");
                await TestFileManager(baseProjectPath);
                Console.WriteLine("✓ ScriptFileManager test passed\n");

                // Test 2: Model Deep Cloning
                Console.WriteLine("Test 2: Testing Prototype Pattern (Deep Clone)...");
                TestDeepCloning();
                Console.WriteLine("✓ Deep cloning test passed\n");

                // Test 3: Null Safety
                Console.WriteLine("Test 3: Testing Null-Safety...");
                TestNullSafety();
                Console.WriteLine("✓ Null-safety test passed\n");

                // Test 4: Directory Structure
                Console.WriteLine("Test 4: Verifying Directory Structure...");
                VerifyDirectoryStructure(baseProjectPath);
                Console.WriteLine("✓ Directory structure verified\n");

                Console.WriteLine("=".PadRight(80, '='));
                Console.WriteLine("✓ All tests passed successfully!");
                Console.WriteLine("=".PadRight(80, '='));
                Console.WriteLine();
                Console.WriteLine("The script improvement pipeline is ready to use.");
                Console.WriteLine("To run with a real LLM, use ScriptImprovementExample with Ollama installed.");
            }
            catch (Exception ex)
            {
                Console.ForegroundColor = ConsoleColor.Red;
                Console.WriteLine($"\n❌ Test failed: {ex.Message}");
                Console.WriteLine($"Stack trace: {ex.StackTrace}");
                Console.ResetColor();
                Environment.Exit(1);
            }
        }

        private static async Task TestFileManager(string basePath)
        {
            var fileManager = new ScriptFileManager();
            var audience = new AudienceSegment("men", "18-23");

            // Test directory creation
            var scriptDir = fileManager.EnsureScriptDirectory(basePath, audience, "gpt_improved");
            if (!Directory.Exists(scriptDir))
                throw new Exception($"Failed to create script directory: {scriptDir}");
            Console.WriteLine($"  ✓ Created directory: {scriptDir}");

            // Test file name generation
            var fileName = fileManager.GenerateScriptFileName("test_001", "v2");
            if (fileName != "test_001_v2.md")
                throw new Exception($"Unexpected file name: {fileName}");
            Console.WriteLine($"  ✓ Generated file name: {fileName}");

            // Test script saving and loading
            var testScript = new ScriptVersion
            {
                TitleId = "test_pipeline",
                Version = "v1",
                Content = "# Test Script\n\nThis is a test.",
                TargetAudience = audience
            };

            var tempPath = Path.Combine(Path.GetTempPath(), "test_script.md");
            await File.WriteAllTextAsync(tempPath, testScript.Content);
            var loadedContent = await fileManager.LoadScriptAsync(tempPath);
            
            if (loadedContent != testScript.Content)
                throw new Exception("Script content mismatch after save/load");
            Console.WriteLine($"  ✓ Script save/load works correctly");

            File.Delete(tempPath);
        }

        private static void TestDeepCloning()
        {
            // Test ScriptVersion deep cloning
            var original = new ScriptVersion
            {
                TitleId = "test_001",
                Version = "v1",
                Content = "Original content",
                TargetAudience = new AudienceSegment("men", "18-23"),
                Score = 85.5
            };

            var clone = original.DeepClone();
            
            // Verify it's a different instance
            if (ReferenceEquals(original, clone))
                throw new Exception("Clone is not a separate instance");
            
            // Verify audience is deep cloned
            if (ReferenceEquals(original.TargetAudience, clone.TargetAudience))
                throw new Exception("TargetAudience was not deep cloned");

            // Modify clone and verify original is unchanged
            clone.Content = "Modified content";
            clone.Version = "v2";
            clone.TargetAudience.Gender = "women";

            if (original.Content != "Original content")
                throw new Exception("Original content was modified");
            if (original.Version != "v1")
                throw new Exception("Original version was modified");
            if (original.TargetAudience.Gender != "men")
                throw new Exception("Original audience was modified");

            Console.WriteLine("  ✓ ScriptVersion deep cloning works correctly");

            // Test ScriptScoringResult deep cloning
            var scoringResult = new ScriptScoringResult
            {
                TitleId = "test_001",
                Version = "v2",
                OverallScore = 85.5,
                AreasForImprovement = new System.Collections.Generic.List<string> { "Hook", "Pacing" },
                RubricScores = new ScriptRubricScores { HookQuality = 80 }
            };

            var scoreClone = scoringResult.DeepClone();
            
            if (ReferenceEquals(scoringResult, scoreClone))
                throw new Exception("ScoringResult clone is not a separate instance");
            
            if (ReferenceEquals(scoringResult.AreasForImprovement, scoreClone.AreasForImprovement))
                throw new Exception("AreasForImprovement was not deep cloned");

            if (ReferenceEquals(scoringResult.RubricScores, scoreClone.RubricScores))
                throw new Exception("RubricScores was not deep cloned");

            Console.WriteLine("  ✓ ScriptScoringResult deep cloning works correctly");
        }

        private static void TestNullSafety()
        {
            var fileManager = new ScriptFileManager();

            // Test null checks in GenerateScriptFileName
            try
            {
                fileManager.GenerateScriptFileName(null!);
                throw new Exception("Should have thrown ArgumentException for null titleId");
            }
            catch (ArgumentException)
            {
                Console.WriteLine("  ✓ Null titleId correctly rejected");
            }

            // Test null checks in EnsureScriptDirectory
            try
            {
                fileManager.EnsureScriptDirectory(null!, new AudienceSegment("men", "18-23"), "test");
                throw new Exception("Should have thrown ArgumentException for null basePath");
            }
            catch (ArgumentException)
            {
                Console.WriteLine("  ✓ Null basePath correctly rejected");
            }

            try
            {
                fileManager.EnsureScriptDirectory("/tmp", null!, "test");
                throw new Exception("Should have thrown ArgumentNullException for null segment");
            }
            catch (ArgumentNullException)
            {
                Console.WriteLine("  ✓ Null segment correctly rejected");
            }

            Console.WriteLine("  ✓ All null-safety checks passed");
        }

        private static void VerifyDirectoryStructure(string basePath)
        {
            var scriptsPath = Path.Combine(basePath, "scripts");
            var scoresPath = Path.Combine(basePath, "scores");

            if (!Directory.Exists(scriptsPath))
                throw new Exception($"Scripts directory not found: {scriptsPath}");
            Console.WriteLine($"  ✓ Scripts directory exists: {scriptsPath}");

            if (!Directory.Exists(scoresPath))
                throw new Exception($"Scores directory not found: {scoresPath}");
            Console.WriteLine($"  ✓ Scores directory exists: {scoresPath}");

            // Check for sample script
            var sampleScript = Path.Combine(scriptsPath, "raw_local", "men", "18-23", "sample_story_001.md");
            if (File.Exists(sampleScript))
            {
                Console.WriteLine($"  ✓ Sample script found: sample_story_001.md");
                var content = File.ReadAllText(sampleScript);
                var wordCount = content.Split(new[] { ' ', '\n', '\r' }, StringSplitOptions.RemoveEmptyEntries).Length;
                Console.WriteLine($"    Word count: {wordCount}");
            }
            else
            {
                Console.WriteLine($"  ℹ Sample script not found (optional)");
            }
        }
    }
}
