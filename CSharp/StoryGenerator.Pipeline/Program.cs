using StoryGenerator.Pipeline.Config;
using StoryGenerator.Pipeline.Core;

namespace StoryGenerator.Pipeline;

class Program
{
    static async Task<int> Main(string[] args)
    {
        try
        {
            Console.WriteLine(new string('=', 80));
            Console.WriteLine("StoryGenerator - Complete Pipeline Orchestrator");
            Console.WriteLine(new string('=', 80));
            Console.WriteLine();

            // Parse command line arguments
            var configPath = GetConfigPath(args);
            var storyTitle = GetStoryTitle(args);
            var resume = HasFlag(args, "--resume");

            // Load configuration
            Console.WriteLine($"Loading configuration from: {configPath ?? "default"}");
            var config = ConfigLoader.LoadOrDefault(configPath);

            // Validate configuration
            var validationErrors = ConfigLoader.Validate(config);
            if (validationErrors.Any())
            {
                Console.WriteLine("\nConfiguration validation errors:");
                foreach (var error in validationErrors)
                {
                    Console.WriteLine($"  - {error}");
                }
                return 1;
            }

            Console.WriteLine("Configuration loaded successfully");
            Console.WriteLine($"Pipeline: {config.Pipeline.Name}");
            Console.WriteLine($"Story Root: {config.Paths.StoryRoot}");
            Console.WriteLine();

            // Create services using dependency injection
            var logger = new PipelineLogger(config.Logging);
            var pythonExecutor = new Services.PythonExecutor(config, logger);
            var checkpointManager = new Services.PipelineCheckpointManager(config, logger);
            
            // Create and run orchestrator
            var orchestrator = new PipelineOrchestrator(config, logger, pythonExecutor, checkpointManager);
            var outputPath = await orchestrator.RunFullPipelineAsync(storyTitle);

            Console.WriteLine();
            Console.WriteLine(new string('=', 80));
            Console.WriteLine("✅ Pipeline completed successfully!");
            Console.WriteLine($"Output: {outputPath}");
            Console.WriteLine(new string('=', 80));

            return 0;
        }
        catch (Exception ex)
        {
            Console.ForegroundColor = ConsoleColor.Red;
            Console.WriteLine();
            Console.WriteLine(new string('=', 80));
            Console.WriteLine("❌ Pipeline failed!");
            Console.WriteLine(new string('=', 80));
            Console.WriteLine($"Error: {ex.Message}");
            Console.WriteLine();
            Console.WriteLine("Stack trace:");
            Console.WriteLine(ex.StackTrace);
            Console.ResetColor();
            return 1;
        }
    }

    private static string? GetConfigPath(string[] args)
    {
        for (int i = 0; i < args.Length - 1; i++)
        {
            if (args[i] == "--config" || args[i] == "-c")
            {
                return args[i + 1];
            }
        }
        
        // Check for default config file
        var defaultPath = Path.Combine("config", "pipeline_config.yaml");
        if (File.Exists(defaultPath))
        {
            return defaultPath;
        }

        return null;
    }

    private static string? GetStoryTitle(string[] args)
    {
        for (int i = 0; i < args.Length - 1; i++)
        {
            if (args[i] == "--story" || args[i] == "-s")
            {
                return args[i + 1];
            }
        }
        return null;
    }

    private static bool HasFlag(string[] args, string flag)
    {
        return args.Contains(flag);
    }

    private static void ShowHelp()
    {
        Console.WriteLine("Usage: StoryGenerator.Pipeline [options]");
        Console.WriteLine();
        Console.WriteLine("Options:");
        Console.WriteLine("  --config, -c <path>    Path to YAML configuration file");
        Console.WriteLine("  --story, -s <title>    Story title (generates new if not provided)");
        Console.WriteLine("  --resume               Resume from last checkpoint");
        Console.WriteLine("  --help, -h             Show this help message");
        Console.WriteLine();
        Console.WriteLine("Examples:");
        Console.WriteLine("  StoryGenerator.Pipeline");
        Console.WriteLine("  StoryGenerator.Pipeline --config custom_config.yaml");
        Console.WriteLine("  StoryGenerator.Pipeline --story \"My Amazing Story\"");
        Console.WriteLine("  StoryGenerator.Pipeline --resume");
    }
}
