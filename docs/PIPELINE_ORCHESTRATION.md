# Pipeline Orchestration

The Pipeline Orchestration system provides a flexible, declarative way to define and execute multi-stage pipelines with built-in error handling, retry logic, and lifecycle hooks.

## Table of Contents

- [Overview](#overview)
- [Key Features](#key-features)
- [Quick Start](#quick-start)
- [Configuration](#configuration)
- [Usage Examples](#usage-examples)
- [Advanced Features](#advanced-features)
- [API Reference](#api-reference)

## Overview

The orchestration engine coordinates the execution of pipeline stages, managing:
- Stage registration and execution order
- Lifecycle hooks (OnStageStart, OnStageComplete, OnStageError)
- Error handling with configurable retry policies
- Conditional stage execution
- Progress reporting and logging

## Key Features

### 1. Declarative Configuration
Define pipelines using YAML or JSON configuration files:

```yaml
metadata:
  name: "My Pipeline"
  version: "1.0.0"
  description: "Pipeline description"

stages:
  - id: "stage_1"
    name: "First Stage"
    order: 10
    enabled: true
    max_retries: 3
    continue_on_error: false
```

### 2. Lifecycle Hooks
Subscribe to events during pipeline execution:

```csharp
engine.OnStageStart += (sender, args) => 
{
    Console.WriteLine($"Starting: {args.StageName}");
};

engine.OnStageComplete += (sender, args) => 
{
    Console.WriteLine($"Completed: {args.StageName}");
};

engine.OnStageError += (sender, args) => 
{
    Console.WriteLine($"Error in {args.StageName}: {args.Exception?.Message}");
};
```

### 3. Retry Logic
Automatic retry with configurable policies:
- Per-stage retry count
- Configurable delay between retries
- Exponential backoff support
- Detailed logging of retry attempts

### 4. Error Handling
Flexible error handling strategies:
- Fail-fast mode (stop on first error)
- Continue-on-error mode (complete remaining stages)
- Per-stage error handling configuration

### 5. Conditional Execution
Skip stages based on runtime conditions:

```yaml
stages:
  - id: "optional_stage"
    condition: "variables.enable_feature == true"
```

## Quick Start

### 1. Create a Pipeline Configuration

Create a file `pipeline.yaml`:

```yaml
metadata:
  name: "Example Pipeline"
  version: "1.0.0"

stages:
  - id: "stage_1"
    name: "Data Collection"
    order: 10
    max_retries: 3
    
  - id: "stage_2"
    name: "Data Processing"
    order: 20
    max_retries: 2
```

### 2. Run the Pipeline

Using the CLI:

```bash
# Show execution plan (dry run)
dotnet run --project StoryGenerator.CLI -- run -c pipeline.yaml --dry-run

# Execute the pipeline
dotnet run --project StoryGenerator.CLI -- run -c pipeline.yaml

# With verbose logging
dotnet run --project StoryGenerator.CLI -- run -c pipeline.yaml --verbose
```

Using the API:

```csharp
// Load configuration
var loader = new PipelineOrchestrationConfigLoader();
var config = await loader.LoadFromFileAsync("pipeline.yaml");

// Create orchestration engine
var logger = new PipelineLogger(loggingConfig);
var engine = new OrchestrationEngine(logger);

// Register stages
var registry = new StageRegistry();
// ... register your stages

// Execute pipeline
var context = new OrchestrationContext();
var result = await engine.ExecuteAsync(context);

if (result.Success)
{
    Console.WriteLine("Pipeline completed successfully!");
}
```

## Configuration

### Pipeline Metadata

```yaml
metadata:
  name: "Pipeline Name"
  version: "1.0.0"
  description: "Pipeline description"
  author: "Your Name"
  tags:
    - category1
    - category2
```

### Stage Configuration

Each stage can be configured with the following properties:

```yaml
stages:
  - id: "unique_stage_id"           # Required: Unique identifier
    name: "Display Name"             # Optional: Human-readable name
    enabled: true                    # Optional: Enable/disable stage
    order: 10                        # Required: Execution order (lower first)
    continue_on_error: false         # Optional: Continue if stage fails
    max_retries: 3                   # Optional: Number of retry attempts
    retry_delay_seconds: 5           # Optional: Delay between retries
    condition: "expression"          # Optional: Conditional execution
    timeout_seconds: 3600            # Optional: Stage timeout
    parameters:                      # Optional: Stage-specific parameters
      param1: "value1"
      param2: 42
```

### Global Error Handling

```yaml
error_handling:
  continue_on_error: false
  retry_count: 3
  retry_delay: 5

retry:
  max_retries: 3
  delay_seconds: 5
  exponential_backoff: true
  backoff_multiplier: 2.0
```

### Logging Configuration

```yaml
logging:
  level: "INFO"                      # DEBUG, INFO, WARNING, ERROR
  console: true
  file: "pipeline.log"
  format: "[{timestamp}] {level}: {message}"
```

### Variables

Define variables that can be referenced in stage parameters:

```yaml
variables:
  story_title: "${STORY_TITLE}"      # From environment variable
  output_root: "./Stories"
  enable_video_generation: true
```

## Usage Examples

### Example 1: Simple Linear Pipeline

```yaml
metadata:
  name: "Simple Pipeline"
  version: "1.0.0"

stages:
  - id: "collect"
    order: 10
    max_retries: 3
    
  - id: "process"
    order: 20
    max_retries: 2
    
  - id: "export"
    order: 30
    max_retries: 1
```

### Example 2: Pipeline with Conditional Stages

```yaml
variables:
  skip_optional: false

stages:
  - id: "required_stage"
    order: 10
    
  - id: "optional_stage"
    order: 20
    condition: "variables.skip_optional == false"
    
  - id: "final_stage"
    order: 30
```

### Example 3: Error Handling Strategies

```yaml
# Fail-fast: Stop on first error
error_handling:
  continue_on_error: false

stages:
  - id: "critical_stage"
    order: 10
    continue_on_error: false  # Stop if this fails
    
  - id: "optional_stage"
    order: 20
    continue_on_error: true   # Continue even if this fails
```

### Example 4: Retry with Exponential Backoff

```yaml
retry:
  max_retries: 5
  delay_seconds: 2
  exponential_backoff: true
  backoff_multiplier: 2.0
  # Delays: 2s, 4s, 8s, 16s, 32s

stages:
  - id: "api_call"
    order: 10
    # Uses global retry config with exponential backoff
```

## Advanced Features

### Dynamic Stage Registration

Register stages programmatically:

```csharp
var registry = new StageRegistry();

registry.Register("my_stage", new StageMetadata
{
    Id = "my_stage",
    Name = "My Custom Stage",
    Description = "Does something useful",
    Category = "processing",
    CreateDefinition = config => new StageDefinition
    {
        Id = config.Id,
        Name = "My Custom Stage",
        ExecuteFunc = async (context, ct) =>
        {
            // Stage implementation
            await DoWorkAsync();
        }
    }
});
```

### Custom Lifecycle Hooks

Implement custom behavior on lifecycle events:

```csharp
var engine = new OrchestrationEngine(logger);

engine.OnStageStart += (sender, args) =>
{
    // Log to monitoring system
    Telemetry.LogStageStart(args.StageName);
};

engine.OnStageComplete += (sender, args) =>
{
    var duration = args.Context["Duration"] as TimeSpan?;
    Telemetry.LogStageComplete(args.StageName, duration);
};

engine.OnStageError += (sender, args) =>
{
    // Send alert
    if (!args.WillRetry)
    {
        AlertSystem.SendAlert($"Stage {args.StageName} failed permanently");
    }
};
```

### Sharing Data Between Stages

Use the OrchestrationContext to pass data:

```csharp
// In stage 1
context.SetData("output_path", "/path/to/output");

// In stage 2
var inputPath = context.GetData<string>("output_path");
```

### Cancellation Support

Gracefully cancel pipeline execution:

```csharp
var cts = new CancellationTokenSource();

// Start pipeline
var executeTask = engine.ExecuteAsync(context, cts.Token);

// Cancel after some condition
if (shouldCancel)
{
    cts.Cancel();
}

var result = await executeTask;
// result.Success will be false if cancelled
```

## API Reference

### IOrchestrationEngine

Main interface for pipeline orchestration.

```csharp
public interface IOrchestrationEngine
{
    event EventHandler<StageLifecycleEventArgs>? OnStageStart;
    event EventHandler<StageLifecycleEventArgs>? OnStageComplete;
    event EventHandler<StageErrorEventArgs>? OnStageError;
    
    void RegisterStage(StageDefinition stageDefinition);
    Task<OrchestrationResult> ExecuteAsync(OrchestrationContext context, CancellationToken cancellationToken = default);
    IReadOnlyList<string> GetExecutionPlan();
}
```

### StageDefinition

Defines a pipeline stage.

```csharp
public class StageDefinition
{
    public string Id { get; set; }
    public string Name { get; set; }
    public int Order { get; set; }
    public bool Enabled { get; set; }
    public Func<OrchestrationContext, bool>? Condition { get; set; }
    public Func<OrchestrationContext, CancellationToken, Task>? ExecuteFunc { get; set; }
    public bool ContinueOnError { get; set; }
    public int MaxRetries { get; set; }
    public int RetryDelaySeconds { get; set; }
}
```

### OrchestrationContext

Context passed to stages during execution.

```csharp
public class OrchestrationContext
{
    public Dictionary<string, object> Data { get; set; }
    public object? Configuration { get; set; }
    
    public T? GetData<T>(string key);
    public void SetData<T>(string key, T value);
}
```

### OrchestrationResult

Result of pipeline execution.

```csharp
public class OrchestrationResult
{
    public bool Success { get; set; }
    public List<string> ExecutedStages { get; set; }
    public List<string> SkippedStages { get; set; }
    public List<string> FailedStages { get; set; }
    public TimeSpan TotalDuration { get; set; }
    public string? ErrorMessage { get; set; }
    public Exception? Exception { get; set; }
}
```

## Best Practices

1. **Stage Naming**: Use clear, descriptive IDs and names
2. **Order Values**: Use increments of 10 (10, 20, 30) to allow easy insertion of new stages
3. **Error Handling**: Set `continue_on_error: true` only for truly optional stages
4. **Retries**: Use retries for transient failures (network, API timeouts), not for logic errors
5. **Logging**: Use appropriate log levels (DEBUG for detailed info, INFO for progress, ERROR for failures)
6. **Configuration**: Store sensitive data in environment variables, reference them with `${VAR_NAME}`
7. **Testing**: Test your pipeline with `--dry-run` before executing

## Troubleshooting

### Pipeline fails immediately
- Check that all required environment variables are set
- Verify pipeline configuration is valid using validation
- Check logs for specific error messages

### Stage keeps retrying
- Verify `max_retries` is set appropriately
- Check if the error is transient or permanent
- Review retry delay to ensure it's not too short

### Stage is skipped
- Check if `enabled: true` is set
- Verify condition expression evaluates to true
- Check execution order

## Related Documentation

- [Quick Start Guide](../../docs/quickstarts/general/QUICK_START_GUIDE.md)
- [Pipeline Configuration](../../config/pipeline.yaml)
- [Task Execution Matrix](../../docs/roadmaps/planning/TASK_EXECUTION_MATRIX.md)

## Support

For issues or questions:
- Check existing issues in the GitHub repository
- Review test cases for examples
- Consult the API reference documentation
