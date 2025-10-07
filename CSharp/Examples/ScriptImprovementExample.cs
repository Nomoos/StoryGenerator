using System;
using System.Threading;
using System.Threading.Tasks;
using StoryGenerator.Core.LLM;
using StoryGenerator.Tools;

namespace StoryGenerator.Examples
{
    /// <summary>
    /// Example demonstrating script improvement using GPT or local LLM.
    /// Improves scripts iteratively until quality plateaus.
    /// </summary>
    public class ScriptImprovementExample
    {
        public static async Task Main(string[] args)
        {
            try
            {
                Console.WriteLine("=".PadRight(80, '='));
                Console.WriteLine("Script Improvement Example");
                Console.WriteLine("Improves scripts using GPT or local LLM (qwen2.5_14b)");
                Console.WriteLine("=".PadRight(80, '='));
                Console.WriteLine();

                // Parse command line arguments
                var baseProjectPath = GetArgument(args, "--base-path", "/home/runner/work/StoryGenerator/StoryGenerator");
                var modelName = GetArgument(args, "--model", "qwen2.5:14b-instruct");
                var segment = GetArgument(args, "--segment", "men");
                var age = GetArgument(args, "--age", "18-23");
                var titleId = GetArgument(args, "--title-id", null);
                var improveAll = HasFlag(args, "--all");

                Console.WriteLine($"Configuration:");
                Console.WriteLine($"  Base Path: {baseProjectPath}");
                Console.WriteLine($"  Model: {modelName}");
                Console.WriteLine($"  Segment: {segment}");
                Console.WriteLine($"  Age: {age}");
                if (!string.IsNullOrEmpty(titleId))
                    Console.WriteLine($"  Title ID: {titleId}");
                Console.WriteLine();

                // Initialize components
                Console.WriteLine("Initializing components...");
                var modelProvider = new OllamaModelProvider(modelName);
                var fileManager = new ScriptFileManager();
                var scriptScorer = new ScriptScorer(modelProvider, fileManager, modelName);
                var scriptIterator = new ScriptIterator(modelProvider, fileManager, modelName);
                var scriptImprover = new ScriptImprover(
                    modelProvider,
                    scriptScorer,
                    scriptIterator,
                    fileManager,
                    baseProjectPath,
                    baseProjectPath);

                Console.WriteLine("✓ Components initialized");
                Console.WriteLine();

                // Check if model is available
                Console.WriteLine($"Checking if model '{modelName}' is available...");
                var isAvailable = await modelProvider.IsModelAvailableAsync(modelName);
                
                if (!isAvailable)
                {
                    Console.WriteLine($"Model '{modelName}' not found locally.");
                    Console.WriteLine($"Attempting to pull model...");
                    
                    var pulled = await modelProvider.PullModelAsync(modelName);
                    
                    if (!pulled)
                    {
                        Console.WriteLine($"Failed to pull model '{modelName}'.");
                        Console.WriteLine("Please ensure Ollama is installed and the model name is correct.");
                        return;
                    }
                    
                    Console.WriteLine($"✓ Model '{modelName}' pulled successfully");
                }
                else
                {
                    Console.WriteLine($"✓ Model '{modelName}' is available");
                }
                Console.WriteLine();

                // Run improvement process
                if (improveAll)
                {
                    Console.WriteLine("Improving all scripts across all segments...");
                    var results = await scriptImprover.ImproveAllScriptsAsync(CancellationToken.None);
                    Console.WriteLine($"\n✓ Improved {results.Count()} scripts total");
                }
                else if (!string.IsNullOrEmpty(titleId))
                {
                    // Improve a specific script
                    var scriptPath = System.IO.Path.Combine(
                        baseProjectPath, 
                        "scripts", 
                        "raw_local", 
                        segment, 
                        age, 
                        $"{titleId}.md");

                    if (!System.IO.File.Exists(scriptPath))
                    {
                        Console.WriteLine($"Error: Script not found at {scriptPath}");
                        return;
                    }

                    var audience = new Models.AudienceSegment(segment, age);
                    var bestVersion = await scriptImprover.ImproveScriptAsync(
                        scriptPath,
                        titleId,
                        audience,
                        CancellationToken.None);

                    Console.WriteLine($"\n✓ Script improved successfully");
                    Console.WriteLine($"  Best version: {bestVersion.Version}");
                    Console.WriteLine($"  Score: {bestVersion.Score:F1}/100");
                    Console.WriteLine($"  Output: {bestVersion.FilePath}");
                }
                else
                {
                    // Improve all scripts in a specific segment
                    Console.WriteLine($"Improving scripts for {segment}/{age}...");
                    var results = await scriptImprover.ImproveScriptsInSegmentAsync(
                        segment,
                        age,
                        "raw_local",
                        CancellationToken.None);

                    Console.WriteLine($"\n✓ Improved {results.Count()} scripts");
                }

                Console.WriteLine();
                Console.WriteLine("=".PadRight(80, '='));
                Console.WriteLine("✓ Script improvement completed successfully!");
                Console.WriteLine("=".PadRight(80, '='));
            }
            catch (Exception ex)
            {
                Console.ForegroundColor = ConsoleColor.Red;
                Console.WriteLine();
                Console.WriteLine("=".PadRight(80, '='));
                Console.WriteLine("❌ Error during script improvement");
                Console.WriteLine("=".PadRight(80, '='));
                Console.WriteLine($"Error: {ex.Message}");
                Console.WriteLine();
                Console.WriteLine("Stack trace:");
                Console.WriteLine(ex.StackTrace);
                Console.ResetColor();
            }
        }

        private static string GetArgument(string[] args, string flag, string defaultValue)
        {
            for (int i = 0; i < args.Length - 1; i++)
            {
                if (args[i] == flag)
                {
                    return args[i + 1];
                }
            }
            return defaultValue;
        }

        private static bool HasFlag(string[] args, string flag)
        {
            return Array.IndexOf(args, flag) >= 0;
        }

        private static void ShowHelp()
        {
            Console.WriteLine("Script Improvement Example");
            Console.WriteLine();
            Console.WriteLine("Usage: ScriptImprovementExample [options]");
            Console.WriteLine();
            Console.WriteLine("Options:");
            Console.WriteLine("  --base-path <path>     Base project path (default: /home/runner/work/StoryGenerator/StoryGenerator)");
            Console.WriteLine("  --model <name>         Model name (default: qwen2.5:14b-instruct)");
            Console.WriteLine("  --segment <segment>    Audience segment (default: men)");
            Console.WriteLine("  --age <range>          Age range (default: 18-23)");
            Console.WriteLine("  --title-id <id>        Specific title ID to improve");
            Console.WriteLine("  --all                  Improve all scripts across all segments");
            Console.WriteLine("  --help, -h             Show this help message");
            Console.WriteLine();
            Console.WriteLine("Examples:");
            Console.WriteLine("  # Improve all scripts in men/18-23 segment");
            Console.WriteLine("  ScriptImprovementExample --segment men --age 18-23");
            Console.WriteLine();
            Console.WriteLine("  # Improve a specific script");
            Console.WriteLine("  ScriptImprovementExample --segment men --age 18-23 --title-id story_123");
            Console.WriteLine();
            Console.WriteLine("  # Improve all scripts across all segments");
            Console.WriteLine("  ScriptImprovementExample --all");
            Console.WriteLine();
            Console.WriteLine("  # Use a different model");
            Console.WriteLine("  ScriptImprovementExample --model llama3.1:8b-instruct --segment women --age 24-30");
        }
    }
}
