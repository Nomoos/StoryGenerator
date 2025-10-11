using StoryGenerator.Pipeline.Config;
using StoryGenerator.Pipeline.Interfaces;

namespace StoryGenerator.Pipeline.Core;

/// <summary>
/// Adapter that bridges the new orchestration engine with the existing pipeline stages.
/// Provides a unified way to execute pipelines using either the new or legacy approach.
/// </summary>
public class OrchestrationAdapter
{
    private readonly OrchestrationEngine _engine;
    private readonly IStageRegistry _registry;
    private readonly PipelineConfig _pipelineConfig;
    private readonly PipelineOrchestrator _legacyOrchestrator;
    private readonly PipelineLogger _logger;

    public OrchestrationAdapter(
        PipelineConfig pipelineConfig,
        PipelineLogger logger,
        PipelineOrchestrator legacyOrchestrator)
    {
        _pipelineConfig = pipelineConfig ?? throw new ArgumentNullException(nameof(pipelineConfig));
        _logger = logger ?? throw new ArgumentNullException(nameof(logger));
        _legacyOrchestrator = legacyOrchestrator ?? throw new ArgumentNullException(nameof(legacyOrchestrator));
        
        _engine = new OrchestrationEngine(logger, pipelineConfig.Processing?.ErrorHandling);
        _registry = new StageRegistry();
        
        RegisterBuiltInStages();
    }

    /// <summary>
    /// Execute pipeline using orchestration configuration
    /// </summary>
    public async Task<OrchestrationResult> ExecutePipelineAsync(
        PipelineOrchestrationConfig orchestrationConfig,
        string? storyTitle = null,
        CancellationToken cancellationToken = default)
    {
        // Create orchestration context
        var context = new OrchestrationContext
        {
            Configuration = _pipelineConfig,
            Data = new Dictionary<string, object>
            {
                ["StoryTitle"] = storyTitle ?? $"Story_{_pipelineConfig.Seeds.RandomSeed}",
                ["PipelineConfig"] = _pipelineConfig
            }
        };

        // Add variables from config
        foreach (var variable in orchestrationConfig.Variables)
        {
            context.Data[$"var_{variable.Key}"] = variable.Value;
        }

        // Register stages from configuration
        foreach (var stageConfig in orchestrationConfig.Stages)
        {
            var metadata = _registry.GetMetadata(stageConfig.Id);
            if (metadata == null)
            {
                _logger.LogWarning($"Stage '{stageConfig.Id}' is not registered, skipping");
                continue;
            }

            var stageDefinition = CreateStageDefinition(stageConfig, metadata);
            _engine.RegisterStage(stageDefinition);
        }

        // Subscribe to lifecycle events for logging
        _engine.OnStageStart += (sender, args) =>
        {
            _logger.LogInfo($"▶️  Starting stage: {args.StageName}");
        };

        _engine.OnStageComplete += (sender, args) =>
        {
            var duration = args.Context.TryGetValue("Duration", out var durationObj) && durationObj is TimeSpan ts
                ? ts
                : TimeSpan.Zero;
            _logger.LogInfo($"✅ Completed stage: {args.StageName} ({duration.TotalSeconds:F2}s)");
        };

        _engine.OnStageError += (sender, args) =>
        {
            _logger.LogError($"❌ Stage failed: {args.StageName} - {args.Exception?.Message}");
            if (args.WillRetry)
            {
                _logger.LogWarning($"   Will retry (attempt {args.RetryAttempt + 1})");
            }
        };

        // Execute pipeline
        return await _engine.ExecuteAsync(context, cancellationToken);
    }

    /// <summary>
    /// Get execution plan from configuration
    /// </summary>
    public List<string> GetExecutionPlan(PipelineOrchestrationConfig config)
    {
        return config.Stages
            .Where(s => s.Enabled)
            .OrderBy(s => s.Order)
            .Select(s => s.Name ?? s.Id)
            .ToList();
    }

    private StageDefinition CreateStageDefinition(PipelineStageConfig config, StageMetadata metadata)
    {
        return new StageDefinition
        {
            Id = config.Id,
            Name = config.Name ?? metadata.Name,
            Order = config.Order,
            Enabled = config.Enabled,
            ContinueOnError = config.ContinueOnError,
            MaxRetries = config.MaxRetries ?? metadata.DefaultConfiguration.MaxRetries,
            RetryDelaySeconds = config.RetryDelaySeconds ?? metadata.DefaultConfiguration.RetryDelaySeconds,
            Condition = EvaluateCondition(config.Condition),
            ExecuteFunc = async (context, cancellationToken) =>
            {
                // Get stage-specific executor from metadata
                if (metadata.CreateDefinition != null)
                {
                    var stageConfig = new StageConfiguration
                    {
                        Id = config.Id,
                        Enabled = config.Enabled,
                        Order = config.Order,
                        ContinueOnError = config.ContinueOnError,
                        MaxRetries = config.MaxRetries ?? 0,
                        RetryDelaySeconds = config.RetryDelaySeconds ?? 5,
                        Parameters = config.Parameters
                    };

                    var definition = metadata.CreateDefinition(stageConfig);
                    if (definition.ExecuteFunc != null)
                    {
                        await definition.ExecuteFunc(context, cancellationToken);
                    }
                }
            }
        };
    }

    private Func<OrchestrationContext, bool>? EvaluateCondition(string? conditionExpression)
    {
        if (string.IsNullOrWhiteSpace(conditionExpression))
        {
            return null;
        }

        // Simple condition evaluation (can be enhanced with a proper expression parser)
        return context =>
        {
            try
            {
                // For now, just return true for any non-empty condition
                // In a real implementation, this would parse and evaluate the expression
                return true;
            }
            catch
            {
                return true;
            }
        };
    }

    private void RegisterBuiltInStages()
    {
        // Register story idea generation stage
        _registry.Register("story_idea", new StageMetadata
        {
            Id = "story_idea",
            Name = "Story Idea Generation",
            Description = "Generate story ideas with viral potential",
            Category = "generation",
            DefaultConfiguration = new StageConfiguration
            {
                MaxRetries = 3,
                RetryDelaySeconds = 5
            },
            CreateDefinition = config => new StageDefinition
            {
                Id = config.Id,
                Name = "Story Idea Generation",
                ExecuteFunc = async (context, ct) =>
                {
                    // For now, just use a placeholder
                    var storyTitle = $"Story_{DateTime.Now:yyyyMMddHHmmss}";
                    context.SetData("StoryTitle", storyTitle);
                }
            }
        });

        // Register other stages similarly
        var stageIds = new[]
        {
            ("script_generation", "Script Generation", "Generate script from story idea"),
            ("script_revision", "Script Revision", "Revise script for AI voice clarity"),
            ("script_enhancement", "Script Enhancement", "Add voice tags and enhancements"),
            ("voice_synthesis", "Voice Synthesis", "Generate voiceover audio"),
            ("asr_subtitles", "ASR & Subtitles", "Generate subtitles using ASR"),
            ("scene_analysis", "Scene Analysis", "Analyze script for scene boundaries"),
            ("scene_description", "Scene Description", "Generate scene descriptions"),
            ("keyframe_generation", "Keyframe Generation", "Generate keyframes for scenes"),
            ("video_interpolation", "Video Interpolation", "Generate video from keyframes"),
            ("video_composition", "Video Composition", "Compose final video with audio")
        };

        var order = 20;
        foreach (var (id, name, description) in stageIds)
        {
            _registry.Register(id, new StageMetadata
            {
                Id = id,
                Name = name,
                Description = description,
                Category = "generation",
                DefaultConfiguration = new StageConfiguration
                {
                    Order = order,
                    MaxRetries = 2,
                    RetryDelaySeconds = 5
                },
                CreateDefinition = config => new StageDefinition
                {
                    Id = config.Id,
                    Name = name,
                    ExecuteFunc = async (context, ct) =>
                    {
                        // Placeholder - actual implementation would call appropriate methods
                        _logger.LogInfo($"Executing {name}...");
                        await Task.CompletedTask;
                    }
                }
            });
            order += 10;
        }
    }
}
