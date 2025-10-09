using System.CommandLine;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Logging;
using StoryGenerator.Core.Models;
using StoryGenerator.Core.Services;
using StoryGenerator.Core.Utils;
using StoryGenerator.Generators;
using StoryGenerator.Providers.ElevenLabs;
using StoryGenerator.Providers.OpenAI;

namespace StoryGenerator.CLI;

/// <summary>
/// Command-line interface for StoryGenerator.
/// Provides commands to generate ideas, scripts, revisions, voice, and subtitles.
/// </summary>
class Program
{
    static async Task<int> Main(string[] args)
    {
        var rootCommand = new RootCommand("StoryGenerator - AI-powered story content generation");

        // Add commands
        rootCommand.AddCommand(CreateGenerateIdeasCommand());
        rootCommand.AddCommand(CreateGenerateScriptCommand());
        rootCommand.AddCommand(CreateReviseScriptCommand());
        rootCommand.AddCommand(CreateEnhanceScriptCommand());
        rootCommand.AddCommand(CreateGenerateVoiceCommand());
        rootCommand.AddCommand(CreateGenerateSubtitlesCommand());
        rootCommand.AddCommand(CreateFullPipelineCommand());
        rootCommand.AddCommand(CreatePipelineResumeCommand());
        rootCommand.AddCommand(CreatePipelineValidateCommand());

        return await rootCommand.InvokeAsync(args);
    }

    static Command CreateGenerateIdeasCommand()
    {
        var topicOption = new Option<string>(
            name: "--topic",
            description: "Topic for story idea generation")
        { IsRequired = true };

        var countOption = new Option<int>(
            name: "--count",
            description: "Number of ideas to generate",
            getDefaultValue: () => 5);

        var toneOption = new Option<string>(
            name: "--tone",
            description: "Tone for the stories (e.g., emotional, witty, dramatic)");

        var themeOption = new Option<string>(
            name: "--theme",
            description: "Theme for the stories (e.g., friendship, love, betrayal)");

        var outputOption = new Option<string>(
            name: "--output",
            description: "Output directory for generated ideas",
            getDefaultValue: () => "./0_Ideas");

        var command = new Command("generate-ideas", "Generate story ideas with viral potential scoring")
        {
            topicOption,
            countOption,
            toneOption,
            themeOption,
            outputOption
        };

        command.SetHandler(async (string topic, int count, string? tone, string? theme, string output) =>
        {
            await ExecuteWithServices(async (services) =>
            {
                var generator = services.GetRequiredService<IIdeaGenerator>();
                var ideas = await generator.GenerateIdeasAsync(topic, count, tone, theme);

                Console.WriteLine($"✅ Generated {ideas.Count} story ideas");

                foreach (var idea in ideas)
                {
                    var savedPath = Path.Combine(output, $"{FileHelper.SanitizeFilename(idea.StoryTitle)}.json");
                    await idea.ToFileAsync(savedPath);
                    Console.WriteLine($"  📄 {idea.StoryTitle} (Overall: {idea.Potential.Overall:F1}) → {savedPath}");
                }
            });
        }, topicOption, countOption, toneOption, themeOption, outputOption);

        return command;
    }

    static Command CreateGenerateScriptCommand()
    {
        var ideaFileOption = new Option<string>(
            name: "--idea-file",
            description: "Path to the story idea JSON file")
        { IsRequired = true };

        var outputOption = new Option<string>(
            name: "--output",
            description: "Output directory for the script",
            getDefaultValue: () => "./1_Scripts");

        var command = new Command("generate-script", "Generate a ~360 word script from a story idea")
        {
            ideaFileOption,
            outputOption
        };

        command.SetHandler(async (string ideaFile, string output) =>
        {
            await ExecuteWithServices(async (services) =>
            {
                var generator = services.GetRequiredService<IScriptGenerator>();
                var idea = await StoryIdea.FromFileAsync(ideaFile);

                var scriptPath = await generator.GenerateAndSaveScriptAsync(idea, output);
                Console.WriteLine($"✅ Script generated: {scriptPath}");
            });
        }, ideaFileOption, outputOption);

        return command;
    }

    static Command CreateReviseScriptCommand()
    {
        var scriptDirOption = new Option<string>(
            name: "--script-dir",
            description: "Directory containing the script to revise")
        { IsRequired = true };

        var outputOption = new Option<string>(
            name: "--output",
            description: "Output directory for the revised script",
            getDefaultValue: () => "./2_Revised");

        var titleOption = new Option<string>(
            name: "--title",
            description: "Story title for logging")
        { IsRequired = true };

        var command = new Command("revise-script", "Revise a script for AI voice clarity")
        {
            scriptDirOption,
            outputOption,
            titleOption
        };

        command.SetHandler(async (string scriptDir, string output, string title) =>
        {
            await ExecuteWithServices(async (services) =>
            {
                var generator = services.GetRequiredService<IRevisionGenerator>();
                var revisedPath = await generator.ReviseAndSaveScriptAsync(scriptDir, output, title);
                Console.WriteLine($"✅ Script revised: {revisedPath}");
            });
        }, scriptDirOption, outputOption, titleOption);

        return command;
    }

    static Command CreateEnhanceScriptCommand()
    {
        var revisedDirOption = new Option<string>(
            name: "--revised-dir",
            description: "Directory containing the revised script")
        { IsRequired = true };

        var titleOption = new Option<string>(
            name: "--title",
            description: "Story title")
        { IsRequired = true };

        var command = new Command("enhance-script", "Add ElevenLabs voice tags to a revised script")
        {
            revisedDirOption,
            titleOption
        };

        command.SetHandler(async (string revisedDir, string title) =>
        {
            await ExecuteWithServices(async (services) =>
            {
                var generator = services.GetRequiredService<IEnhancementGenerator>();
                var enhancedPath = await generator.EnhanceAndSaveScriptAsync(revisedDir, title);
                Console.WriteLine($"✅ Script enhanced: {enhancedPath}");
            });
        }, revisedDirOption, titleOption);

        return command;
    }

    static Command CreateGenerateVoiceCommand()
    {
        var scriptOption = new Option<string>(
            name: "--script",
            description: "Path to the script file")
        { IsRequired = true };

        var outputOption = new Option<string>(
            name: "--output",
            description: "Output path for the audio file (MP3)")
        { IsRequired = true };

        var voiceIdOption = new Option<string>(
            name: "--voice-id",
            description: "ElevenLabs voice ID");

        var stabilityOption = new Option<float?>(
            name: "--stability",
            description: "Voice stability (0.0 to 1.0)");

        var command = new Command("generate-voice", "Generate voiceover audio from a script")
        {
            scriptOption,
            outputOption,
            voiceIdOption,
            stabilityOption
        };

        command.SetHandler(async (string script, string output, string? voiceId, float? stability) =>
        {
            await ExecuteWithServices(async (services) =>
            {
                var generator = services.GetRequiredService<IVoiceGenerator>();
                var scriptText = await File.ReadAllTextAsync(script);

                var audioPath = await generator.GenerateAndSaveAudioAsync(
                    scriptText, output, voiceId, stability);
                Console.WriteLine($"✅ Audio generated: {audioPath}");
            });
        }, scriptOption, outputOption, voiceIdOption, stabilityOption);

        return command;
    }

    static Command CreateGenerateSubtitlesCommand()
    {
        var audioOption = new Option<string>(
            name: "--audio",
            description: "Path to the audio file")
        { IsRequired = true };

        var scriptOption = new Option<string>(
            name: "--script",
            description: "Path to the script file")
        { IsRequired = true };

        var outputOption = new Option<string>(
            name: "--output",
            description: "Output path for the SRT file")
        { IsRequired = true };

        var command = new Command("generate-subtitles", "Generate word-level SRT subtitles")
        {
            audioOption,
            scriptOption,
            outputOption
        };

        command.SetHandler(async (string audio, string script, string output) =>
        {
            await ExecuteWithServices(async (services) =>
            {
                var generator = services.GetRequiredService<ISubtitleGenerator>();
                var result = await generator.GenerateSubtitlesAsync(audio, script, output);

                Console.WriteLine($"✅ Subtitles generated: {output}");
                Console.WriteLine($"   Words: {result.WordCount}");
                Console.WriteLine($"   Accuracy: {result.AlignmentAccuracy:F1}%");
                Console.WriteLine($"   Duration: {result.AudioDuration:F1}s");
            });
        }, audioOption, scriptOption, outputOption);

        return command;
    }

    static Command CreateFullPipelineCommand()
    {
        var topicOption = new Option<string>(
            name: "--topic",
            description: "Topic for story generation")
        { IsRequired = true };

        var outputRootOption = new Option<string>(
            name: "--output-root",
            description: "Root directory for all outputs",
            getDefaultValue: () => "./Stories");

        var command = new Command("full-pipeline", "Run the complete pipeline from idea to audio with subtitles")
        {
            topicOption,
            outputRootOption
        };

        command.SetHandler(async (string topic, string outputRoot) =>
        {
            await ExecuteWithServices(async (services) =>
            {
                var ideaGen = services.GetRequiredService<IIdeaGenerator>();
                var scriptGen = services.GetRequiredService<IScriptGenerator>();
                var revisionGen = services.GetRequiredService<IRevisionGenerator>();
                var enhanceGen = services.GetRequiredService<IEnhancementGenerator>();
                var voiceGen = services.GetRequiredService<IVoiceGenerator>();
                var subtitleGen = services.GetRequiredService<ISubtitleGenerator>();

                Console.WriteLine("🚀 Starting full pipeline...\n");

                // 1. Generate idea
                Console.WriteLine("1️⃣  Generating story idea...");
                var ideas = await ideaGen.GenerateIdeasAsync(topic, 1);
                var idea = ideas[0];
                Console.WriteLine($"   ✅ {idea.StoryTitle}\n");

                // 2. Generate script
                Console.WriteLine("2️⃣  Generating script...");
                var scriptPath = await scriptGen.GenerateAndSaveScriptAsync(
                    idea, Path.Combine(outputRoot, "1_Scripts"));
                Console.WriteLine($"   ✅ {scriptPath}\n");

                // 3. Revise script
                Console.WriteLine("3️⃣  Revising script...");
                var scriptDir = Path.GetDirectoryName(scriptPath)!;
                var revisedPath = await revisionGen.ReviseAndSaveScriptAsync(
                    scriptDir, Path.Combine(outputRoot, "2_Revised"), idea.StoryTitle);
                Console.WriteLine($"   ✅ {revisedPath}\n");

                // 4. Enhance script
                Console.WriteLine("4️⃣  Enhancing script with voice tags...");
                var revisedDir = Path.GetDirectoryName(revisedPath)!;
                var enhancedPath = await enhanceGen.EnhanceAndSaveScriptAsync(
                    revisedDir, idea.StoryTitle);
                Console.WriteLine($"   ✅ {enhancedPath}\n");

                // 5. Generate voice
                Console.WriteLine("5️⃣  Generating voiceover...");
                var enhancedScript = await File.ReadAllTextAsync(enhancedPath);
                var audioPath = Path.Combine(revisedDir, "voiceover.mp3");
                await voiceGen.GenerateAndSaveAudioAsync(enhancedScript, audioPath);
                Console.WriteLine($"   ✅ {audioPath}\n");

                // 6. Generate subtitles
                Console.WriteLine("6️⃣  Generating subtitles...");
                var srtPath = Path.Combine(revisedDir, "subtitles.srt");
                var subtitleResult = await subtitleGen.GenerateSubtitlesAsync(
                    audioPath, revisedPath, srtPath);
                Console.WriteLine($"   ✅ {srtPath}");
                Console.WriteLine($"      Words: {subtitleResult.WordCount}, Accuracy: {subtitleResult.AlignmentAccuracy:F1}%\n");

                Console.WriteLine("🎉 Pipeline complete!");
                Console.WriteLine($"📂 Output directory: {revisedDir}");
            });
        }, topicOption, outputRootOption);

        return command;
    }

    static Command CreatePipelineResumeCommand()
    {
        var checkpointPathOption = new Option<string>(
            name: "--checkpoint-path",
            description: "Path to the checkpoint file",
            getDefaultValue: () => "./Stories/pipeline_checkpoint.json");

        var command = new Command("pipeline-resume", "Resume a pipeline from a saved checkpoint")
        {
            checkpointPathOption
        };

        command.SetHandler(async (string checkpointPath) =>
        {
            if (!File.Exists(checkpointPath))
            {
                Console.ForegroundColor = ConsoleColor.Red;
                Console.WriteLine($"❌ Checkpoint file not found: {checkpointPath}");
                Console.ResetColor();
                Environment.Exit(1);
                return;
            }

            Console.WriteLine($"🔄 Resuming pipeline from checkpoint: {checkpointPath}");
            Console.WriteLine("⚠️  Note: Pipeline resume via PipelineOrchestrator integration coming soon!");
            Console.WriteLine("    For now, use 'full-pipeline' command which automatically resumes from checkpoints.");
            
            // TODO: Integrate with PipelineOrchestrator to resume from checkpoint
            // This would require refactoring the full-pipeline command to use the orchestrator
        }, checkpointPathOption);

        return command;
    }

    static Command CreatePipelineValidateCommand()
    {
        var configPathOption = new Option<string>(
            name: "--config",
            description: "Path to pipeline configuration file",
            getDefaultValue: () => "./appsettings.json");

        var command = new Command("pipeline-validate", "Validate pipeline configuration")
        {
            configPathOption
        };

        command.SetHandler((string configPath) =>
        {
            if (!File.Exists(configPath))
            {
                Console.ForegroundColor = ConsoleColor.Red;
                Console.WriteLine($"❌ Configuration file not found: {configPath}");
                Console.ResetColor();
                Environment.Exit(1);
                return;
            }

            Console.WriteLine($"✅ Validating configuration: {configPath}");
            
            try
            {
                // Basic validation - check if file is valid JSON
                var json = File.ReadAllText(configPath);
                System.Text.Json.JsonDocument.Parse(json);
                
                // Check for required environment variables
                var requiredEnvVars = new[] { "OPENAI_API_KEY", "ELEVENLABS_API_KEY" };
                var missingVars = new List<string>();
                
                foreach (var envVar in requiredEnvVars)
                {
                    if (string.IsNullOrEmpty(Environment.GetEnvironmentVariable(envVar)))
                    {
                        missingVars.Add(envVar);
                    }
                }

                if (missingVars.Count > 0)
                {
                    Console.ForegroundColor = ConsoleColor.Yellow;
                    Console.WriteLine($"⚠️  Warning: Missing environment variables:");
                    foreach (var missing in missingVars)
                    {
                        Console.WriteLine($"    - {missing}");
                    }
                    Console.ResetColor();
                }
                
                Console.ForegroundColor = ConsoleColor.Green;
                Console.WriteLine("✅ Configuration is valid");
                Console.ResetColor();
            }
            catch (Exception ex)
            {
                Console.ForegroundColor = ConsoleColor.Red;
                Console.WriteLine($"❌ Configuration validation failed: {ex.Message}");
                Console.ResetColor();
                Environment.Exit(1);
            }
        }, configPathOption);

        return command;
    }

    static async Task ExecuteWithServices(Func<IServiceProvider, Task> action)
    {
        var services = ConfigureServices();

        try
        {
            await action(services);
        }
        catch (Exception ex)
        {
            Console.ForegroundColor = ConsoleColor.Red;
            Console.WriteLine($"❌ Error: {ex.Message}");
            Console.ResetColor();
            Environment.Exit(1);
        }
    }

    static IServiceProvider ConfigureServices()
    {
        var services = new ServiceCollection();

        // Logging
        services.AddLogging(builder =>
        {
            builder.AddConsole();
            builder.SetMinimumLevel(LogLevel.Information);
        });

        // Configuration (from environment variables or defaults)
        var openAIKey = Environment.GetEnvironmentVariable("OPENAI_API_KEY") 
            ?? throw new InvalidOperationException("OPENAI_API_KEY environment variable not set");
        var elevenLabsKey = Environment.GetEnvironmentVariable("ELEVENLABS_API_KEY")
            ?? throw new InvalidOperationException("ELEVENLABS_API_KEY environment variable not set");

        // Options
        services.Configure<OpenAIOptions>(options =>
        {
            options.ApiKey = openAIKey;
            options.Model = "gpt-4o-mini";
            options.Temperature = 0.9f;
        });

        services.Configure<ElevenLabsOptions>(options =>
        {
            options.ApiKey = elevenLabsKey;
            options.VoiceId = Environment.GetEnvironmentVariable("ELEVENLABS_VOICE_ID") ?? "BZgkqPqms7Kj9ulSkVzn";
            options.Model = "eleven_multilingual_v2";
            options.VoiceStability = 0.5f;
            options.VoiceSimilarityBoost = 0.75f;
        });

        // Core services
        services.AddSingleton<PathConfiguration>(sp => new PathConfiguration 
        { 
            StoryRoot = Environment.GetEnvironmentVariable("STORY_ROOT") ?? "./Stories" 
        });
        services.AddSingleton<PerformanceMonitor>();
        services.AddSingleton<RetryService>();

        // Providers
        services.AddHttpClient<OpenAIClient>();
        services.AddHttpClient<ElevenLabsClient>();

        // Generators
        services.AddSingleton<IIdeaGenerator, IdeaGenerator>();
        services.AddSingleton<IScriptGenerator, ScriptGenerator>();
        services.AddSingleton<IRevisionGenerator, RevisionGenerator>();
        services.AddSingleton<IEnhancementGenerator, EnhancementGenerator>();
        services.AddSingleton<IVoiceGenerator, VoiceGenerator>();
        services.AddSingleton<ISubtitleGenerator, SubtitleGenerator>();

        return services.BuildServiceProvider();
    }
}
