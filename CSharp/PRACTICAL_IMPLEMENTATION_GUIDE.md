# Practical Implementation Guide: SOLID + OOP + Clean Code

> **Real-world examples for the StoryGenerator video pipeline**

---

## Table of Contents

1. [Video Processing Service Implementation](#video-processing-service-implementation)
2. [Script Generation Pipeline](#script-generation-pipeline)
3. [Error Handling Patterns](#error-handling-patterns)
4. [Testing Strategies](#testing-strategies)
5. [Configuration Management](#configuration-management)
6. [Logging and Monitoring](#logging-and-monitoring)

---

## Video Processing Service Implementation

### Scenario: Creating a Multi-Stage Video Processing Service

**Requirements:**
- Process videos through multiple stages (audio extraction, normalization, subtitle generation, composition)
- Support different video formats
- Handle errors gracefully
- Support progress tracking
- Be testable

### Step 1: Define Interfaces (SOLID - ISP, DIP)

```csharp
/// <summary>
/// Represents a single stage in the video processing pipeline.
/// Follows ISP by being small and focused.
/// </summary>
public interface IVideoProcessingStage
{
    string StageName { get; }
    Task<StageResult> ProcessAsync(string inputPath, VideoProcessingContext context, CancellationToken ct = default);
    Task<bool> ValidateInputAsync(string inputPath);
}

/// <summary>
/// Result from a processing stage.
/// </summary>
public class StageResult
{
    public bool Success { get; set; }
    public string OutputPath { get; set; }
    public string ErrorMessage { get; set; }
    public Dictionary<string, object> Metadata { get; set; } = new();
}

/// <summary>
/// Context passed through all stages.
/// </summary>
public class VideoProcessingContext
{
    public string WorkingDirectory { get; set; }
    public Dictionary<string, string> IntermediateFiles { get; set; } = new();
    public IProgress<ProcessingProgress> ProgressReporter { get; set; }
}

/// <summary>
/// Progress information.
/// </summary>
public class ProcessingProgress
{
    public string CurrentStage { get; set; }
    public int PercentComplete { get; set; }
    public string Message { get; set; }
}
```

### Step 2: Implement Concrete Stages (SOLID - SRP, OCP)

```csharp
/// <summary>
/// Stage 1: Extract audio from video.
/// Follows SRP - only handles audio extraction.
/// </summary>
public class AudioExtractionStage : IVideoProcessingStage
{
    private readonly IFFmpegClient _ffmpegClient;
    private readonly ILogger<AudioExtractionStage> _logger;
    
    public string StageName => "Audio Extraction";
    
    public AudioExtractionStage(IFFmpegClient ffmpegClient, ILogger<AudioExtractionStage> logger)
    {
        _ffmpegClient = ffmpegClient ?? throw new ArgumentNullException(nameof(ffmpegClient));
        _logger = logger ?? throw new ArgumentNullException(nameof(logger));
    }
    
    public async Task<bool> ValidateInputAsync(string inputPath)
    {
        if (!File.Exists(inputPath))
            return false;
        
        var extension = Path.GetExtension(inputPath).ToLowerInvariant();
        return extension is ".mp4" or ".avi" or ".mov" or ".mkv";
    }
    
    public async Task<StageResult> ProcessAsync(
        string inputPath, 
        VideoProcessingContext context, 
        CancellationToken ct = default)
    {
        try
        {
            _logger.LogInformation("Extracting audio from {VideoPath}", inputPath);
            
            // Report progress
            context.ProgressReporter?.Report(new ProcessingProgress
            {
                CurrentStage = StageName,
                PercentComplete = 0,
                Message = "Starting audio extraction"
            });
            
            // Generate output path
            var outputPath = Path.Combine(
                context.WorkingDirectory, 
                $"{Path.GetFileNameWithoutExtension(inputPath)}_audio.mp3"
            );
            
            // Extract audio using FFmpeg
            var args = $"-i \"{inputPath}\" -vn -acodec libmp3lame -q:a 2 \"{outputPath}\"";
            await _ffmpegClient.ExecuteAsync(args, ct);
            
            // Store intermediate file
            context.IntermediateFiles["audio"] = outputPath;
            
            // Report completion
            context.ProgressReporter?.Report(new ProcessingProgress
            {
                CurrentStage = StageName,
                PercentComplete = 100,
                Message = "Audio extraction complete"
            });
            
            _logger.LogInformation("Audio extracted to {OutputPath}", outputPath);
            
            return new StageResult
            {
                Success = true,
                OutputPath = outputPath,
                Metadata = { ["format"] = "mp3", ["quality"] = "high" }
            };
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Failed to extract audio from {VideoPath}", inputPath);
            return new StageResult
            {
                Success = false,
                ErrorMessage = $"Audio extraction failed: {ex.Message}"
            };
        }
    }
}

/// <summary>
/// Stage 2: Normalize audio levels.
/// Follows SRP - only handles audio normalization.
/// </summary>
public class AudioNormalizationStage : IVideoProcessingStage
{
    private readonly IFFmpegClient _ffmpegClient;
    private readonly ILogger<AudioNormalizationStage> _logger;
    private const double TargetLUFS = -14.0; // Standard for social media
    
    public string StageName => "Audio Normalization";
    
    public AudioNormalizationStage(IFFmpegClient ffmpegClient, ILogger<AudioNormalizationStage> logger)
    {
        _ffmpegClient = ffmpegClient ?? throw new ArgumentNullException(nameof(ffmpegClient));
        _logger = logger ?? throw new ArgumentNullException(nameof(logger));
    }
    
    public async Task<bool> ValidateInputAsync(string inputPath)
    {
        if (!File.Exists(inputPath))
            return false;
        
        var extension = Path.GetExtension(inputPath).ToLowerInvariant();
        return extension is ".mp3" or ".wav" or ".aac";
    }
    
    public async Task<StageResult> ProcessAsync(
        string inputPath, 
        VideoProcessingContext context, 
        CancellationToken ct = default)
    {
        try
        {
            _logger.LogInformation("Normalizing audio {AudioPath} to {TargetLUFS} LUFS", 
                inputPath, TargetLUFS);
            
            context.ProgressReporter?.Report(new ProcessingProgress
            {
                CurrentStage = StageName,
                PercentComplete = 0,
                Message = "Starting audio normalization"
            });
            
            // Generate output path
            var outputPath = Path.Combine(
                context.WorkingDirectory,
                $"{Path.GetFileNameWithoutExtension(inputPath)}_normalized.mp3"
            );
            
            // Normalize using FFmpeg loudnorm filter
            var args = $"-i \"{inputPath}\" " +
                      $"-af \"loudnorm=I={TargetLUFS}:TP=-1.5:LRA=11\" " +
                      $"-ar 44100 \"{outputPath}\"";
            
            await _ffmpegClient.ExecuteAsync(args, ct);
            
            // Update intermediate files
            context.IntermediateFiles["normalized_audio"] = outputPath;
            
            context.ProgressReporter?.Report(new ProcessingProgress
            {
                CurrentStage = StageName,
                PercentComplete = 100,
                Message = "Audio normalization complete"
            });
            
            _logger.LogInformation("Audio normalized to {OutputPath}", outputPath);
            
            return new StageResult
            {
                Success = true,
                OutputPath = outputPath,
                Metadata = { ["target_lufs"] = TargetLUFS, ["sample_rate"] = 44100 }
            };
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Failed to normalize audio {AudioPath}", inputPath);
            return new StageResult
            {
                Success = false,
                ErrorMessage = $"Audio normalization failed: {ex.Message}"
            };
        }
    }
}

/// <summary>
/// Stage 3: Generate subtitles from audio.
/// Follows SRP - only handles subtitle generation.
/// </summary>
public class SubtitleGenerationStage : IVideoProcessingStage
{
    private readonly ISpeechRecognitionClient _speechClient;
    private readonly ILogger<SubtitleGenerationStage> _logger;
    
    public string StageName => "Subtitle Generation";
    
    public SubtitleGenerationStage(
        ISpeechRecognitionClient speechClient, 
        ILogger<SubtitleGenerationStage> logger)
    {
        _speechClient = speechClient ?? throw new ArgumentNullException(nameof(speechClient));
        _logger = logger ?? throw new ArgumentNullException(nameof(logger));
    }
    
    public async Task<bool> ValidateInputAsync(string inputPath)
    {
        return File.Exists(inputPath) && 
               Path.GetExtension(inputPath).ToLowerInvariant() is ".mp3" or ".wav";
    }
    
    public async Task<StageResult> ProcessAsync(
        string inputPath, 
        VideoProcessingContext context, 
        CancellationToken ct = default)
    {
        try
        {
            _logger.LogInformation("Generating subtitles from {AudioPath}", inputPath);
            
            context.ProgressReporter?.Report(new ProcessingProgress
            {
                CurrentStage = StageName,
                PercentComplete = 0,
                Message = "Starting subtitle generation"
            });
            
            // Generate output path
            var outputPath = Path.Combine(
                context.WorkingDirectory,
                $"{Path.GetFileNameWithoutExtension(inputPath)}.srt"
            );
            
            // Transcribe audio to subtitles
            var subtitles = await _speechClient.TranscribeAsync(inputPath, outputFormat: "srt", ct);
            await File.WriteAllTextAsync(outputPath, subtitles, ct);
            
            context.IntermediateFiles["subtitles"] = outputPath;
            
            context.ProgressReporter?.Report(new ProcessingProgress
            {
                CurrentStage = StageName,
                PercentComplete = 100,
                Message = "Subtitle generation complete"
            });
            
            _logger.LogInformation("Subtitles generated to {OutputPath}", outputPath);
            
            return new StageResult
            {
                Success = true,
                OutputPath = outputPath,
                Metadata = { ["format"] = "srt", ["language"] = "en" }
            };
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Failed to generate subtitles from {AudioPath}", inputPath);
            return new StageResult
            {
                Success = false,
                ErrorMessage = $"Subtitle generation failed: {ex.Message}"
            };
        }
    }
}
```

### Step 3: Create Pipeline Orchestrator (Facade Pattern, Clean Code)

```csharp
/// <summary>
/// Orchestrates multi-stage video processing pipeline.
/// Implements Facade pattern to simplify complex operations.
/// Follows SOLID principles with dependency injection.
/// </summary>
public class VideoProcessingPipeline
{
    private readonly List<IVideoProcessingStage> _stages;
    private readonly ILogger<VideoProcessingPipeline> _logger;
    private readonly string _workingDirectory;
    
    public VideoProcessingPipeline(
        IEnumerable<IVideoProcessingStage> stages,
        ILogger<VideoProcessingPipeline> logger,
        string workingDirectory = null)
    {
        _stages = stages?.ToList() ?? throw new ArgumentNullException(nameof(stages));
        _logger = logger ?? throw new ArgumentNullException(nameof(logger));
        _workingDirectory = workingDirectory ?? Path.Combine(Path.GetTempPath(), $"video_processing_{Guid.NewGuid()}");
        
        Directory.CreateDirectory(_workingDirectory);
    }
    
    /// <summary>
    /// Process video through all stages.
    /// </summary>
    /// <param name="inputVideoPath">Path to input video file.</param>
    /// <param name="progress">Progress reporter for UI updates.</param>
    /// <param name="ct">Cancellation token.</param>
    /// <returns>Result with final output path.</returns>
    public async Task<PipelineResult> ProcessAsync(
        string inputVideoPath,
        IProgress<ProcessingProgress> progress = null,
        CancellationToken ct = default)
    {
        // Validate input (Clean Code: early validation)
        if (string.IsNullOrWhiteSpace(inputVideoPath))
            throw new ArgumentException("Input video path cannot be empty", nameof(inputVideoPath));
        
        if (!File.Exists(inputVideoPath))
            throw new FileNotFoundException($"Input video not found: {inputVideoPath}");
        
        _logger.LogInformation("Starting video processing pipeline for {VideoPath}", inputVideoPath);
        
        var context = new VideoProcessingContext
        {
            WorkingDirectory = _workingDirectory,
            ProgressReporter = progress
        };
        
        var results = new List<StageResult>();
        var currentInput = inputVideoPath;
        
        try
        {
            // Process through each stage
            for (int i = 0; i < _stages.Count; i++)
            {
                var stage = _stages[i];
                
                _logger.LogInformation(
                    "Executing stage {StageNumber}/{TotalStages}: {StageName}", 
                    i + 1, _stages.Count, stage.StageName);
                
                // Validate stage input
                if (!await stage.ValidateInputAsync(currentInput))
                {
                    throw new InvalidOperationException(
                        $"Stage {stage.StageName} validation failed for input: {currentInput}");
                }
                
                // Execute stage
                var result = await stage.ProcessAsync(currentInput, context, ct);
                results.Add(result);
                
                // Check if stage failed
                if (!result.Success)
                {
                    _logger.LogError("Stage {StageName} failed: {Error}", 
                        stage.StageName, result.ErrorMessage);
                    
                    return new PipelineResult
                    {
                        Success = false,
                        ErrorMessage = $"Pipeline failed at stage: {stage.StageName}",
                        FailedStage = stage.StageName,
                        StageResults = results
                    };
                }
                
                // Use stage output as next input
                currentInput = result.OutputPath;
                
                _logger.LogInformation("Stage {StageName} completed successfully", stage.StageName);
            }
            
            _logger.LogInformation("Video processing pipeline completed successfully");
            
            return new PipelineResult
            {
                Success = true,
                OutputPath = currentInput,
                StageResults = results,
                IntermediateFiles = context.IntermediateFiles
            };
        }
        catch (OperationCanceledException)
        {
            _logger.LogWarning("Video processing pipeline was cancelled");
            throw;
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Video processing pipeline failed with unexpected error");
            
            return new PipelineResult
            {
                Success = false,
                ErrorMessage = $"Pipeline failed: {ex.Message}",
                StageResults = results
            };
        }
    }
    
    /// <summary>
    /// Clean up working directory and intermediate files.
    /// </summary>
    public void Cleanup()
    {
        try
        {
            if (Directory.Exists(_workingDirectory))
            {
                Directory.Delete(_workingDirectory, recursive: true);
                _logger.LogInformation("Cleaned up working directory: {Directory}", _workingDirectory);
            }
        }
        catch (Exception ex)
        {
            _logger.LogWarning(ex, "Failed to clean up working directory: {Directory}", _workingDirectory);
        }
    }
}

/// <summary>
/// Result from the complete pipeline execution.
/// </summary>
public class PipelineResult
{
    public bool Success { get; set; }
    public string OutputPath { get; set; }
    public string ErrorMessage { get; set; }
    public string FailedStage { get; set; }
    public List<StageResult> StageResults { get; set; } = new();
    public Dictionary<string, string> IntermediateFiles { get; set; } = new();
}
```

### Step 4: Register Services (DI Container)

```csharp
// Program.cs or Startup.cs
public static void ConfigureServices(IServiceCollection services, IConfiguration configuration)
{
    // Register FFmpeg client
    services.AddSingleton<IFFmpegClient, FFmpegClient>();
    
    // Register speech recognition client
    services.AddSingleton<ISpeechRecognitionClient, WhisperClient>();
    
    // Register individual stages
    services.AddTransient<IVideoProcessingStage, AudioExtractionStage>();
    services.AddTransient<IVideoProcessingStage, AudioNormalizationStage>();
    services.AddTransient<IVideoProcessingStage, SubtitleGenerationStage>();
    
    // Register pipeline orchestrator
    services.AddTransient<VideoProcessingPipeline>();
    
    // Add logging
    services.AddLogging(builder =>
    {
        builder.AddConsole();
        builder.AddDebug();
    });
}
```

### Step 5: Usage Example

```csharp
public class VideoProcessingExample
{
    private readonly VideoProcessingPipeline _pipeline;
    private readonly ILogger<VideoProcessingExample> _logger;
    
    public VideoProcessingExample(
        VideoProcessingPipeline pipeline, 
        ILogger<VideoProcessingExample> logger)
    {
        _pipeline = pipeline;
        _logger = logger;
    }
    
    public async Task ProcessVideoWithProgressAsync(string videoPath)
    {
        // Create progress reporter
        var progress = new Progress<ProcessingProgress>(p =>
        {
            Console.WriteLine($"[{p.CurrentStage}] {p.PercentComplete}% - {p.Message}");
        });
        
        try
        {
            // Process video
            var result = await _pipeline.ProcessAsync(videoPath, progress);
            
            if (result.Success)
            {
                _logger.LogInformation("Video processed successfully: {OutputPath}", result.OutputPath);
                
                // Display stage results
                foreach (var stageResult in result.StageResults)
                {
                    Console.WriteLine($"✓ {stageResult.OutputPath}");
                }
            }
            else
            {
                _logger.LogError("Video processing failed: {Error}", result.ErrorMessage);
            }
        }
        finally
        {
            // Clean up
            _pipeline.Cleanup();
        }
    }
}
```

---

## Script Generation Pipeline

### Scenario: LLM-Based Script Generation with Iteration

**Requirements:**
- Generate script using LLM (OpenAI or local)
- Score script quality
- Iterate to improve based on feedback
- Support cancellation
- Track version history

### Implementation

```csharp
/// <summary>
/// Service for generating and iterating on scripts using LLM.
/// Follows SOLID principles and Clean Code practices.
/// </summary>
public class ScriptGenerationService
{
    private readonly ILLMModelProvider _llmProvider;
    private readonly IScriptScorer _scriptScorer;
    private readonly IScriptFileManager _fileManager;
    private readonly ILogger<ScriptGenerationService> _logger;
    
    private const int MaxIterations = 5;
    private const int MinScoreImprovement = 2;
    private const int TargetScore = 85;
    
    public ScriptGenerationService(
        ILLMModelProvider llmProvider,
        IScriptScorer scriptScorer,
        IScriptFileManager fileManager,
        ILogger<ScriptGenerationService> logger)
    {
        _llmProvider = llmProvider ?? throw new ArgumentNullException(nameof(llmProvider));
        _scriptScorer = scriptScorer ?? throw new ArgumentNullException(nameof(scriptScorer));
        _fileManager = fileManager ?? throw new ArgumentNullException(nameof(fileManager));
        _logger = logger ?? throw new ArgumentNullException(nameof(logger));
    }
    
    /// <summary>
    /// Generate and iteratively improve a script.
    /// </summary>
    public async Task<ScriptGenerationResult> GenerateAndImproveAsync(
        StoryIdea idea,
        AudienceSegment audience,
        IProgress<IterationProgress> progress = null,
        CancellationToken ct = default)
    {
        ValidateInputs(idea, audience);
        
        _logger.LogInformation(
            "Starting script generation for idea: {IdeaTitle}, audience: {Audience}",
            idea.StoryTitle, audience);
        
        var versions = new List<ScriptVersion>();
        var currentVersion = 0;
        
        try
        {
            // Generate initial script (v0)
            var initialScript = await GenerateInitialScriptAsync(idea, audience, ct);
            var scriptPath = await _fileManager.SaveRawScriptAsync(
                initialScript.Content, 
                audience.Gender, 
                audience.Age, 
                idea.StoryTitle);
            
            initialScript.FilePath = scriptPath;
            versions.Add(initialScript);
            
            // Score initial script
            var score = await _scriptScorer.ScoreScriptAsync(
                scriptPath, 
                idea.StoryTitle, 
                $"v{currentVersion}", 
                audience, 
                ct);
            
            initialScript.Score = score;
            
            _logger.LogInformation(
                "Initial script (v0) generated with score: {Score}/100", 
                score.OverallScore);
            
            progress?.Report(new IterationProgress
            {
                Iteration = 0,
                Score = score.OverallScore,
                Message = $"Initial script generated (score: {score.OverallScore})"
            });
            
            // Iterate to improve
            var previousScore = score.OverallScore;
            
            while (currentVersion < MaxIterations && 
                   score.OverallScore < TargetScore)
            {
                ct.ThrowIfCancellationRequested();
                
                currentVersion++;
                
                _logger.LogInformation(
                    "Starting iteration {Iteration} to improve script", 
                    currentVersion);
                
                // Generate improved version
                var improvedScript = await IterateScriptAsync(
                    versions.Last(), 
                    score, 
                    ct);
                
                var improvedPath = await _fileManager.SaveIteratedScriptAsync(
                    improvedScript.Content,
                    audience.Gender,
                    audience.Age,
                    idea.StoryTitle,
                    currentVersion);
                
                improvedScript.FilePath = improvedPath;
                improvedScript.Version = $"v{currentVersion}";
                versions.Add(improvedScript);
                
                // Score improved version
                var improvedScore = await _scriptScorer.ScoreScriptAsync(
                    improvedPath,
                    idea.StoryTitle,
                    $"v{currentVersion}",
                    audience,
                    ct);
                
                improvedScript.Score = improvedScore;
                
                var improvement = improvedScore.OverallScore - previousScore;
                
                _logger.LogInformation(
                    "Iteration {Iteration} completed. Score: {Score}/100 (improvement: {Improvement:+0;-0})",
                    currentVersion, improvedScore.OverallScore, improvement);
                
                progress?.Report(new IterationProgress
                {
                    Iteration = currentVersion,
                    Score = improvedScore.OverallScore,
                    Improvement = improvement,
                    Message = $"Iteration {currentVersion} completed (score: {improvedScore.OverallScore})"
                });
                
                // Check if improvement is too small
                if (improvement < MinScoreImprovement)
                {
                    _logger.LogInformation(
                        "Improvement plateaued at iteration {Iteration}. Stopping.", 
                        currentVersion);
                    break;
                }
                
                previousScore = improvedScore.OverallScore;
                score = improvedScore;
            }
            
            // Get best version
            var bestVersion = versions.OrderByDescending(v => v.Score.OverallScore).First();
            
            _logger.LogInformation(
                "Script generation completed. Best version: {Version} with score {Score}/100",
                bestVersion.Version, bestVersion.Score.OverallScore);
            
            return new ScriptGenerationResult
            {
                Success = true,
                BestVersion = bestVersion,
                AllVersions = versions,
                TotalIterations = currentVersion
            };
        }
        catch (OperationCanceledException)
        {
            _logger.LogWarning("Script generation was cancelled at iteration {Iteration}", currentVersion);
            throw;
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Script generation failed at iteration {Iteration}", currentVersion);
            
            return new ScriptGenerationResult
            {
                Success = false,
                ErrorMessage = ex.Message,
                AllVersions = versions,
                TotalIterations = currentVersion
            };
        }
    }
    
    private void ValidateInputs(StoryIdea idea, AudienceSegment audience)
    {
        if (idea == null)
            throw new ArgumentNullException(nameof(idea));
        
        if (string.IsNullOrWhiteSpace(idea.StoryTitle))
            throw new ArgumentException("Story idea must have a title", nameof(idea));
        
        if (audience == null)
            throw new ArgumentNullException(nameof(audience));
    }
    
    private async Task<ScriptVersion> GenerateInitialScriptAsync(
        StoryIdea idea,
        AudienceSegment audience,
        CancellationToken ct)
    {
        var prompt = BuildInitialScriptPrompt(idea, audience);
        var content = await _llmProvider.GenerateTextAsync(prompt, ct);
        
        return new ScriptVersion
        {
            TitleId = idea.StoryTitle,
            Version = "v0",
            Content = content,
            TargetAudience = audience,
            GeneratedAt = DateTime.UtcNow,
            Prompt = prompt
        };
    }
    
    private async Task<ScriptVersion> IterateScriptAsync(
        ScriptVersion currentVersion,
        ScriptScoringResult score,
        CancellationToken ct)
    {
        var prompt = BuildImprovementPrompt(currentVersion, score);
        var content = await _llmProvider.GenerateTextAsync(prompt, ct);
        
        return new ScriptVersion
        {
            TitleId = currentVersion.TitleId,
            Content = content,
            TargetAudience = currentVersion.TargetAudience,
            PreviousVersion = currentVersion,
            GeneratedAt = DateTime.UtcNow,
            Prompt = prompt,
            AppliedFeedback = score.AreasForImprovement
        };
    }
    
    private string BuildInitialScriptPrompt(StoryIdea idea, AudienceSegment audience)
    {
        return $@"Generate a compelling 60-second video script based on this story idea:

Title: {idea.StoryTitle}
Theme: {idea.Theme}
Tone: {idea.Tone}
Target Audience: {audience.Gender}, {audience.Age} years old

Requirements:
- Approximately 150-180 words (for 60-second read time)
- Strong hook in the first 5 seconds
- Clear narrative arc with beginning, middle, and end
- Emotionally engaging content appropriate for {audience.Gender} aged {audience.Age}
- Natural, conversational language suitable for voiceover
- Include subtle pauses marked with [pause]

Generate ONLY the script content, no additional commentary.";
    }
    
    private string BuildImprovementPrompt(ScriptVersion currentVersion, ScriptScoringResult score)
    {
        var feedback = string.Join("\n", score.AreasForImprovement.Select(a => $"- {a}"));
        var strengths = string.Join("\n", score.Strengths.Select(s => $"- {s}"));
        
        return $@"Improve this video script based on the feedback below.

CURRENT SCRIPT:
{currentVersion.Content}

CURRENT SCORE: {score.OverallScore}/100

STRENGTHS TO MAINTAIN:
{strengths}

AREAS FOR IMPROVEMENT:
{feedback}

Requirements:
- Keep the same approximate length (150-180 words)
- Maintain the strengths mentioned above
- Address ALL areas for improvement
- Keep the script natural and conversational
- Preserve the [pause] markers where appropriate

Generate ONLY the improved script content, no additional commentary.";
    }
}

/// <summary>
/// Result from script generation process.
/// </summary>
public class ScriptGenerationResult
{
    public bool Success { get; set; }
    public ScriptVersion BestVersion { get; set; }
    public List<ScriptVersion> AllVersions { get; set; } = new();
    public int TotalIterations { get; set; }
    public string ErrorMessage { get; set; }
}

/// <summary>
/// Progress information for script iteration.
/// </summary>
public class IterationProgress
{
    public int Iteration { get; set; }
    public int Score { get; set; }
    public int Improvement { get; set; }
    public string Message { get; set; }
}
```

---

## Error Handling Patterns

### Custom Exception Hierarchy

```csharp
/// <summary>
/// Base exception for all StoryGenerator errors.
/// </summary>
public class StoryGeneratorException : Exception
{
    public StoryGeneratorException(string message) : base(message) { }
    public StoryGeneratorException(string message, Exception innerException) 
        : base(message, innerException) { }
}

/// <summary>
/// Exception for script-related errors.
/// </summary>
public class ScriptException : StoryGeneratorException
{
    public string ScriptPath { get; set; }
    public string TitleId { get; set; }
    
    public ScriptException(string message) : base(message) { }
    public ScriptException(string message, Exception innerException) 
        : base(message, innerException) { }
}

/// <summary>
/// Exception for scoring errors.
/// </summary>
public class ScriptScoringException : ScriptException
{
    public ScriptScoringException(string message) : base(message) { }
    public ScriptScoringException(string message, Exception innerException) 
        : base(message, innerException) { }
}

/// <summary>
/// Exception for video processing errors.
/// </summary>
public class VideoProcessingException : StoryGeneratorException
{
    public string VideoPath { get; set; }
    public string FailedStage { get; set; }
    
    public VideoProcessingException(string message) : base(message) { }
    public VideoProcessingException(string message, Exception innerException) 
        : base(message, innerException) { }
}

/// <summary>
/// Exception for LLM provider errors.
/// </summary>
public class LLMProviderException : StoryGeneratorException
{
    public string ProviderName { get; set; }
    public int? StatusCode { get; set; }
    
    public LLMProviderException(string message) : base(message) { }
    public LLMProviderException(string message, Exception innerException) 
        : base(message, innerException) { }
}
```

### Error Handling Service

```csharp
/// <summary>
/// Centralized error handling and logging service.
/// </summary>
public class ErrorHandler
{
    private readonly ILogger<ErrorHandler> _logger;
    
    public ErrorHandler(ILogger<ErrorHandler> logger)
    {
        _logger = logger ?? throw new ArgumentNullException(nameof(logger));
    }
    
    /// <summary>
    /// Handle exception and return user-friendly message.
    /// </summary>
    public string HandleException(Exception ex, string context = null)
    {
        var contextMessage = string.IsNullOrWhiteSpace(context) ? "" : $" Context: {context}";
        
        return ex switch
        {
            OperationCanceledException => HandleCancellation(ex, contextMessage),
            HttpRequestException httpEx => HandleNetworkError(httpEx, contextMessage),
            FileNotFoundException fileEx => HandleFileNotFound(fileEx, contextMessage),
            UnauthorizedAccessException authEx => HandleAccessDenied(authEx, contextMessage),
            LLMProviderException llmEx => HandleLLMError(llmEx, contextMessage),
            ScriptScoringException scoreEx => HandleScoringError(scoreEx, contextMessage),
            VideoProcessingException videoEx => HandleVideoError(videoEx, contextMessage),
            _ => HandleGenericError(ex, contextMessage)
        };
    }
    
    private string HandleCancellation(Exception ex, string context)
    {
        _logger.LogWarning("Operation was cancelled.{Context}", context);
        return "Operation was cancelled by user.";
    }
    
    private string HandleNetworkError(HttpRequestException ex, string context)
    {
        _logger.LogError(ex, "Network error occurred.{Context}", context);
        
        if (ex.InnerException is SocketException)
            return "Unable to connect to the service. Please check your internet connection.";
        
        if (ex.StatusCode == System.Net.HttpStatusCode.Unauthorized)
            return "API key is invalid or expired. Please check your configuration.";
        
        if (ex.StatusCode == System.Net.HttpStatusCode.TooManyRequests)
            return "Rate limit exceeded. Please wait a moment and try again.";
        
        return "Network error occurred. Please check your connection and try again.";
    }
    
    private string HandleFileNotFound(FileNotFoundException ex, string context)
    {
        _logger.LogError(ex, "File not found.{Context}", context);
        return $"Required file not found: {ex.FileName}. Please verify the file path.";
    }
    
    private string HandleAccessDenied(UnauthorizedAccessException ex, string context)
    {
        _logger.LogError(ex, "Access denied.{Context}", context);
        return "Access denied. Please check file permissions.";
    }
    
    private string HandleLLMError(LLMProviderException ex, string context)
    {
        _logger.LogError(ex, "LLM provider error.{Context}", context);
        return $"AI service error ({ex.ProviderName}): {ex.Message}";
    }
    
    private string HandleScoringError(ScriptScoringException ex, string context)
    {
        _logger.LogError(ex, "Script scoring error.{Context}", context);
        return $"Failed to score script: {ex.Message}";
    }
    
    private string HandleVideoError(VideoProcessingException ex, string context)
    {
        _logger.LogError(ex, "Video processing error.{Context}", context);
        return $"Video processing failed at stage '{ex.FailedStage}': {ex.Message}";
    }
    
    private string HandleGenericError(Exception ex, string context)
    {
        _logger.LogError(ex, "Unexpected error occurred.{Context}", context);
        return $"An unexpected error occurred: {ex.Message}";
    }
}
```

---

## Testing Strategies

### Unit Test Example with Mocking

```csharp
public class ScriptGenerationServiceTests
{
    private readonly Mock<ILLMModelProvider> _mockLLMProvider;
    private readonly Mock<IScriptScorer> _mockScorer;
    private readonly Mock<IScriptFileManager> _mockFileManager;
    private readonly Mock<ILogger<ScriptGenerationService>> _mockLogger;
    private readonly ScriptGenerationService _service;
    
    public ScriptGenerationServiceTests()
    {
        _mockLLMProvider = new Mock<ILLMModelProvider>();
        _mockScorer = new Mock<IScriptScorer>();
        _mockFileManager = new Mock<IScriptFileManager>();
        _mockLogger = new Mock<ILogger<ScriptGenerationService>>();
        
        _service = new ScriptGenerationService(
            _mockLLMProvider.Object,
            _mockScorer.Object,
            _mockFileManager.Object,
            _mockLogger.Object);
    }
    
    [Fact]
    public async Task GenerateAndImproveAsync_ValidInput_GeneratesScript()
    {
        // Arrange
        var idea = new StoryIdea 
        { 
            StoryTitle = "Test Story",
            Theme = "Adventure",
            Tone = "Exciting"
        };
        var audience = new AudienceSegment("women", "18-23");
        
        _mockLLMProvider
            .Setup(x => x.GenerateTextAsync(It.IsAny<string>(), default))
            .ReturnsAsync("Generated script content");
        
        _mockFileManager
            .Setup(x => x.SaveRawScriptAsync(It.IsAny<string>(), It.IsAny<string>(), It.IsAny<string>(), It.IsAny<string>()))
            .ReturnsAsync("/path/to/script.md");
        
        _mockScorer
            .Setup(x => x.ScoreScriptAsync(It.IsAny<string>(), It.IsAny<string>(), It.IsAny<string>(), It.IsAny<AudienceSegment>(), default))
            .ReturnsAsync(new ScriptScoringResult { OverallScore = 85 });
        
        // Act
        var result = await _service.GenerateAndImproveAsync(idea, audience);
        
        // Assert
        Assert.True(result.Success);
        Assert.NotNull(result.BestVersion);
        Assert.Equal("v0", result.BestVersion.Version);
        Assert.Equal(85, result.BestVersion.Score.OverallScore);
        
        // Verify interactions
        _mockLLMProvider.Verify(x => x.GenerateTextAsync(It.IsAny<string>(), default), Times.Once);
        _mockFileManager.Verify(x => x.SaveRawScriptAsync(It.IsAny<string>(), audience.Gender, audience.Age, idea.StoryTitle), Times.Once);
        _mockScorer.Verify(x => x.ScoreScriptAsync(It.IsAny<string>(), idea.StoryTitle, "v0", audience, default), Times.Once);
    }
    
    [Fact]
    public async Task GenerateAndImproveAsync_NullIdea_ThrowsArgumentNullException()
    {
        // Arrange
        var audience = new AudienceSegment("women", "18-23");
        
        // Act & Assert
        await Assert.ThrowsAsync<ArgumentNullException>(() => 
            _service.GenerateAndImproveAsync(null, audience));
    }
    
    [Fact]
    public async Task GenerateAndImproveAsync_LowScoreWithImprovement_IteratesUntilTargetScore()
    {
        // Arrange
        var idea = new StoryIdea { StoryTitle = "Test Story", Theme = "Adventure", Tone = "Exciting" };
        var audience = new AudienceSegment("women", "18-23");
        
        // First generation returns low score
        var callCount = 0;
        _mockScorer
            .Setup(x => x.ScoreScriptAsync(It.IsAny<string>(), It.IsAny<string>(), It.IsAny<string>(), It.IsAny<AudienceSegment>(), default))
            .ReturnsAsync(() =>
            {
                callCount++;
                // Scores improve each iteration: 70, 75, 80, 85 (target)
                return new ScriptScoringResult 
                { 
                    OverallScore = 65 + (callCount * 5),
                    AreasForImprovement = new List<string> { "Improve hook" }
                };
            });
        
        _mockLLMProvider
            .Setup(x => x.GenerateTextAsync(It.IsAny<string>(), default))
            .ReturnsAsync("Improved script content");
        
        _mockFileManager
            .Setup(x => x.SaveRawScriptAsync(It.IsAny<string>(), It.IsAny<string>(), It.IsAny<string>(), It.IsAny<string>()))
            .ReturnsAsync("/path/to/script_v0.md");
        
        _mockFileManager
            .Setup(x => x.SaveIteratedScriptAsync(It.IsAny<string>(), It.IsAny<string>(), It.IsAny<string>(), It.IsAny<string>(), It.IsAny<int>()))
            .ReturnsAsync((string content, string gender, string age, string title, int version) => 
                $"/path/to/script_v{version}.md");
        
        // Act
        var result = await _service.GenerateAndImproveAsync(idea, audience);
        
        // Assert
        Assert.True(result.Success);
        Assert.True(result.TotalIterations >= 3); // Should iterate multiple times
        Assert.True(result.BestVersion.Score.OverallScore >= 85); // Should reach target score
        
        // Verify LLM was called multiple times (initial + iterations)
        _mockLLMProvider.Verify(
            x => x.GenerateTextAsync(It.IsAny<string>(), default), 
            Times.AtLeast(4));
    }
}
```

---

## Configuration Management

### Options Pattern Implementation

```csharp
/// <summary>
/// Configuration options for video processing.
/// </summary>
public class VideoProcessingOptions
{
    public const string SectionName = "VideoProcessing";
    
    public string WorkingDirectory { get; set; } = Path.GetTempPath();
    public string FFmpegPath { get; set; } = "ffmpeg";
    public string FFprobePath { get; set; } = "ffprobe";
    
    public AudioOptions Audio { get; set; } = new();
    public VideoOptions Video { get; set; } = new();
    public SubtitleOptions Subtitles { get; set; } = new();
    
    public class AudioOptions
    {
        public double TargetLUFS { get; set; } = -14.0;
        public int SampleRate { get; set; } = 44100;
        public string Codec { get; set; } = "libmp3lame";
        public int Quality { get; set; } = 2;
    }
    
    public class VideoOptions
    {
        public string Codec { get; set; } = "libx264";
        public string Preset { get; set; } = "medium";
        public int CRF { get; set; } = 23;
        public int Width { get; set; } = 1080;
        public int Height { get; set; } = 1920;
        public int FPS { get; set; } = 30;
    }
    
    public class SubtitleOptions
    {
        public string FontFamily { get; set; } = "Arial";
        public int FontSize { get; set; } = 24;
        public string FontColor { get; set; } = "white";
        public string BackgroundColor { get; set; } = "black";
        public double BackgroundOpacity { get; set; } = 0.7;
    }
}

/// <summary>
/// Validator for video processing options.
/// </summary>
public class VideoProcessingOptionsValidator : IValidateOptions<VideoProcessingOptions>
{
    public ValidateOptionsResult Validate(string name, VideoProcessingOptions options)
    {
        var errors = new List<string>();
        
        // Validate working directory
        if (string.IsNullOrWhiteSpace(options.WorkingDirectory))
            errors.Add("WorkingDirectory cannot be empty");
        
        // Validate FFmpeg paths
        if (string.IsNullOrWhiteSpace(options.FFmpegPath))
            errors.Add("FFmpegPath cannot be empty");
        
        // Validate audio options
        if (options.Audio.TargetLUFS < -70 || options.Audio.TargetLUFS > 0)
            errors.Add("TargetLUFS must be between -70 and 0");
        
        if (options.Audio.SampleRate < 8000 || options.Audio.SampleRate > 192000)
            errors.Add("SampleRate must be between 8000 and 192000");
        
        // Validate video options
        if (options.Video.Width < 1 || options.Video.Height < 1)
            errors.Add("Video dimensions must be positive");
        
        if (options.Video.FPS < 1 || options.Video.FPS > 120)
            errors.Add("FPS must be between 1 and 120");
        
        // Validate subtitle options
        if (options.Subtitles.FontSize < 1 || options.Subtitles.FontSize > 100)
            errors.Add("FontSize must be between 1 and 100");
        
        if (options.Subtitles.BackgroundOpacity < 0 || options.Subtitles.BackgroundOpacity > 1)
            errors.Add("BackgroundOpacity must be between 0 and 1");
        
        if (errors.Any())
            return ValidateOptionsResult.Fail(errors);
        
        return ValidateOptionsResult.Success;
    }
}

// appsettings.json
{
  "VideoProcessing": {
    "WorkingDirectory": "C:/Temp/VideoProcessing",
    "FFmpegPath": "ffmpeg",
    "FFprobePath": "ffprobe",
    "Audio": {
      "TargetLUFS": -14.0,
      "SampleRate": 44100,
      "Codec": "libmp3lame",
      "Quality": 2
    },
    "Video": {
      "Codec": "libx264",
      "Preset": "medium",
      "CRF": 23,
      "Width": 1080,
      "Height": 1920,
      "FPS": 30
    },
    "Subtitles": {
      "FontFamily": "Arial",
      "FontSize": 24,
      "FontColor": "white",
      "BackgroundColor": "black",
      "BackgroundOpacity": 0.7
    }
  }
}

// Registration in Program.cs
services.AddOptions<VideoProcessingOptions>()
    .Bind(configuration.GetSection(VideoProcessingOptions.SectionName))
    .ValidateDataAnnotations()
    .ValidateOnStart();

services.AddSingleton<IValidateOptions<VideoProcessingOptions>, VideoProcessingOptionsValidator>();
```

---

## Logging and Monitoring

### Structured Logging Example

```csharp
public class VideoProcessingService
{
    private readonly ILogger<VideoProcessingService> _logger;
    
    public async Task<string> ProcessVideoAsync(string videoPath)
    {
        using var _ = _logger.BeginScope(new Dictionary<string, object>
        {
            ["VideoPath"] = videoPath,
            ["OperationId"] = Guid.NewGuid().ToString()
        });
        
        var stopwatch = Stopwatch.StartNew();
        
        try
        {
            _logger.LogInformation(
                "Starting video processing for {VideoPath} at {StartTime}",
                videoPath,
                DateTime.UtcNow);
            
            // Process video...
            var result = await InternalProcessAsync(videoPath);
            
            stopwatch.Stop();
            
            _logger.LogInformation(
                "Video processing completed successfully in {ElapsedMs}ms. Output: {OutputPath}",
                stopwatch.ElapsedMilliseconds,
                result);
            
            return result;
        }
        catch (Exception ex)
        {
            stopwatch.Stop();
            
            _logger.LogError(
                ex,
                "Video processing failed after {ElapsedMs}ms for {VideoPath}",
                stopwatch.ElapsedMilliseconds,
                videoPath);
            
            throw;
        }
    }
}
```

---

## Conclusion

This guide provides practical, real-world examples of applying SOLID principles, OOP, and Clean Code practices in the StoryGenerator video pipeline. Use these patterns as templates for your own implementations.

**Key Takeaways:**
1. Start with interfaces (SOLID-DIP, ISP)
2. Keep classes small and focused (SOLID-SRP, Clean Code)
3. Use dependency injection throughout
4. Validate inputs early
5. Handle errors gracefully with custom exceptions
6. Write comprehensive tests
7. Use structured logging
8. Configure via Options pattern

**Document Version**: 1.0  
**Last Updated**: January 2025
