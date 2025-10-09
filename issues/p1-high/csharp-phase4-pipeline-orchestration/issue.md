# C# Phase 4: Pipeline Orchestration

**ID:** `csharp-phase4-pipeline-orchestration`  
**Priority:** P1 (High)  
**Effort:** 20-30 hours  
**Status:** ✅ Complete (95% - Core functionality complete)  
**Phase:** 4 - Pipeline Orchestration

## Overview

Build a complete end-to-end pipeline orchestrator in C# that chains all generators together, manages state, handles errors, and provides progress tracking. This is the final major component needed before the C# implementation can be considered feature-complete.

## Dependencies

**Requires:**
- Phase 1: Core Infrastructure (✅ Complete)
- Phase 2: API Providers (✅ Complete)
- Phase 3: Generators (🔄 Must be complete)

**Blocks:**
- Python code removal
- Production deployment
- Full migration from Python

## Acceptance Criteria

### Core Pipeline
- [x] PipelineOrchestrator class implemented following SRP (Single Responsibility Principle)
- [x] Support for complete pipeline: Idea → Script → Revision → Enhancement → Voice → Subtitles
- [x] Checkpoint management for resumable pipelines
- [x] Progress tracking and reporting
- [x] Comprehensive error handling and recovery
- [ ] Cancellation token support throughout (partial - needs enhancement)

### Configuration
- [x] Pipeline configuration via appsettings.json
- [x] Environment variable support
- [x] Per-stage configuration (model selection, parameters, etc.)
- [x] Path configuration for outputs
- [x] API key management (secure, never hardcoded)

### State Management
- [x] Checkpoint save/load functionality
- [x] Resume from any pipeline stage
- [x] State persistence to disk (JSON)
- [x] Atomic operations for state updates
- [x] Rollback capability on errors

### CLI Interface
- [x] Command-line interface for pipeline execution
- [x] Pipeline resume command
- [x] Pipeline validate command
- [x] Verbose logging option (added to full-pipeline command)
- [ ] Interactive mode for step-by-step execution (OPTIONAL - deferred)
- [ ] Batch processing mode (OPTIONAL - deferred)
- [ ] Progress display with estimated time remaining (BASIC - needs enhancement)

### Testing
- [x] Unit tests for orchestrator logic (partial tests exist)
- [x] Integration tests for complete pipelines (Phase4IntegrationTests.cs created with 12 tests)
- [x] Error handling and recovery tests (included in integration tests)
- [x] Checkpoint/resume tests (comprehensive checkpoint tests in Phase4IntegrationTests.cs)
- [ ] Performance benchmarks (NOT IMPLEMENTED)

### Documentation
- [x] Pipeline architecture documentation (PIPELINE_GUIDE.md created)
- [x] Configuration guide (included in PIPELINE_GUIDE.md)
- [x] CLI usage guide (CLI_USAGE.md created)
- [x] Examples for common workflows (included in CLI_USAGE.md)
- [x] Troubleshooting guide (included in both guides)

## Task Details

### 1. Pipeline Orchestrator Design (4-6 hours)

Follow SOLID principles from `SOLID_OOP_CLEAN_CODE_GUIDE.md`:

```csharp
// Refactored from single class to focused components
public interface IPipelineOrchestrator
{
    Task<PipelineResult> ExecuteAsync(
        PipelineConfig config,
        CancellationToken cancellationToken = default);
        
    Task<PipelineResult> ResumeAsync(
        string checkpointPath,
        CancellationToken cancellationToken = default);
}

public class PipelineOrchestrator : IPipelineOrchestrator
{
    private readonly IPipelineStageFactory _stageFactory;
    private readonly IPipelineCheckpointManager _checkpointManager;
    private readonly IProgressReporter _progressReporter;
    private readonly ILogger<PipelineOrchestrator> _logger;
    
    // Clean, testable, focused implementation
}
```

### 2. Pipeline Stages (6-8 hours)

Implement each stage as a separate, testable component:

```csharp
public interface IPipelineStage<TInput, TOutput>
{
    string StageName { get; }
    Task<TOutput> ExecuteAsync(
        TInput input,
        IProgress<PipelineProgress> progress,
        CancellationToken cancellationToken);
}

// Stages:
// - IdeaGenerationStage
// - ScriptGenerationStage
// - ScriptRevisionStage
// - ScriptEnhancementStage
// - VoiceGenerationStage
// - SubtitleGenerationStage
```

### 3. Checkpoint Management (4-6 hours)

```csharp
public interface IPipelineCheckpointManager
{
    Task SaveCheckpointAsync(PipelineState state);
    Task<PipelineState> LoadCheckpointAsync(string path);
    Task<bool> CheckpointExistsAsync(string path);
}

public class PipelineState
{
    public string CurrentStage { get; set; }
    public DateTime StartTime { get; set; }
    public Dictionary<string, object> StageOutputs { get; set; }
    public PipelineConfig Config { get; set; }
}
```

### 4. CLI Implementation (6-8 hours)

```bash
# Example CLI usage
storygen pipeline run --config pipeline.json
storygen pipeline run --idea "falling for someone" --output ./outputs
storygen pipeline resume --checkpoint ./checkpoint.json
storygen pipeline run --interactive
storygen pipeline validate --config pipeline.json
```

```csharp
// CLI Command structure
public class PipelineRunCommand : ICommand
{
    [Option("--config", "Path to pipeline configuration")]
    public string? ConfigPath { get; set; }
    
    [Option("--idea", "Story idea or topic")]
    public string? Idea { get; set; }
    
    [Option("--checkpoint", "Path to save checkpoints")]
    public string? CheckpointPath { get; set; }
    
    [Option("--interactive", "Run in interactive mode")]
    public bool Interactive { get; set; }
}
```

### 5. Configuration System (2-4 hours)

**appsettings.json:**
```json
{
  "Pipeline": {
    "DefaultModel": "gpt-4o-mini",
    "CheckpointInterval": "AfterEachStage",
    "MaxRetries": 3,
    "TimeoutMinutes": 30
  },
  "OpenAI": {
    "ApiKey": "${OPENAI_API_KEY}",
    "Model": "gpt-4o-mini",
    "MaxTokens": 4000
  },
  "ElevenLabs": {
    "ApiKey": "${ELEVENLABS_API_KEY}",
    "VoiceId": "default",
    "ModelId": "eleven_multilingual_v2"
  },
  "Paths": {
    "Ideas": "./data/ideas",
    "Scripts": "./data/scripts",
    "Audio": "./data/audio",
    "Checkpoints": "./data/checkpoints"
  }
}
```

### 6. Error Handling & Recovery (2-4 hours)

```csharp
public class PipelineErrorHandler
{
    public async Task<PipelineResult> HandleErrorAsync(
        Exception error,
        PipelineState state,
        PipelineConfig config)
    {
        // Log error
        // Save checkpoint
        // Determine if recoverable
        // Apply recovery strategy
    }
}
```

## Testing Strategy

### Unit Tests
```csharp
[Fact]
public async Task Orchestrator_SavesCheckpointAfterEachStage()
{
    // Arrange
    var orchestrator = CreateOrchestrator();
    
    // Act
    await orchestrator.ExecuteAsync(config);
    
    // Assert
    Assert.True(File.Exists(checkpointPath));
}
```

### Integration Tests
```csharp
[Fact]
public async Task CompletePipeline_GeneratesAllArtifacts()
{
    // Test full pipeline execution
    // Verify all output files created
    // Validate content quality
}
```

### Recovery Tests
```csharp
[Fact]
public async Task Pipeline_ResumesFromCheckpoint()
{
    // Execute pipeline partially
    // Simulate failure
    // Resume from checkpoint
    // Verify completion
}
```

## Output Files

**Code:**
- `src/CSharp/StoryGenerator.Pipeline/PipelineOrchestrator.cs`
- `src/CSharp/StoryGenerator.Pipeline/Stages/*.cs`
- `src/CSharp/StoryGenerator.Pipeline/CheckpointManager.cs`
- `src/CSharp/StoryGenerator.CLI/Commands/PipelineCommands.cs`
- `src/CSharp/StoryGenerator.Pipeline.Tests/*.cs`

**Configuration:**
- `src/CSharp/StoryGenerator.CLI/appsettings.json`
- `src/CSharp/StoryGenerator.CLI/appsettings.Development.json`

**Documentation:**
- `src/CSharp/PIPELINE_GUIDE.md` (new)
- `src/CSharp/CLI_USAGE.md` (new)
- `src/CSharp/MIGRATION_GUIDE.md` (updated)

## Related Files

- `src/CSharp/SOLID_OOP_CLEAN_CODE_GUIDE.md` - Architecture guidelines
- `src/CSharp/StoryGenerator.Pipeline/` - Pipeline implementation
- `src/CSharp/StoryGenerator.Generators/` - Generator implementations
- `docs/PIPELINE.md` - Overall pipeline documentation

## Validation

```bash
# Build solution
cd src/CSharp
dotnet build StoryGenerator.sln

# Run pipeline tests
dotnet test --filter "Category=Pipeline"

# Test CLI
cd StoryGenerator.CLI
dotnet run -- pipeline --help
dotnet run -- pipeline run --idea "test story" --output ./test-output

# Test checkpoint/resume
dotnet run -- pipeline run --idea "test" --checkpoint ./test-checkpoint.json
# Kill process mid-execution
dotnet run -- pipeline resume --checkpoint ./test-checkpoint.json
```

## Examples

### Simple Pipeline Execution
```bash
storygen pipeline run --idea "A story about friendship" --output ./outputs
```

### Custom Configuration
```bash
storygen pipeline run --config custom-pipeline.json
```

### Interactive Mode
```bash
storygen pipeline run --interactive
# > Enter story idea: falling for someone
# > Select narrator gender: female
# > Select tone: romantic, heartwarming
# Pipeline executing...
# ✓ Idea generated
# ✓ Script generated
# ...
```

### Resume from Checkpoint
```bash
storygen pipeline resume --checkpoint ./outputs/checkpoint.json
```

## Notes

- Follow dependency injection patterns throughout
- Use ILogger for all logging (structured logging)
- Implement proper cancellation token handling
- Consider memory usage for large-scale batch processing
- Add telemetry/metrics for production monitoring
- Ensure thread-safety for concurrent pipeline execution

## Success Metrics

- Complete pipeline executes without errors
- Checkpoint/resume functionality works reliably
- CLI is intuitive and well-documented
- Performance matches or exceeds Python implementation
- All tests pass with >80% coverage
- Ready for production deployment

## Next Steps

After completion:
1. Update documentation to reflect Phase 4 = 100% Complete
2. Create issue for Python code removal
3. Create production deployment guide
4. Plan beta testing with real users
5. Performance optimization and tuning
