# Quick Start Guide - P1 Pipeline Implementation

**Target Audience:** Developers implementing pipeline stages  
**Prerequisites:** C# .NET 8.0, familiarity with async/await patterns

## Getting Started

### 1. Environment Setup (5 minutes)

```bash
# Clone repository
git clone https://github.com/Nomoos/StoryGenerator.git
cd StoryGenerator

# Build solution
cd src/CSharp
dotnet build StoryGenerator.sln

# Run tests
dotnet test

# Set up environment variables
cp .env.example .env
# Edit .env and add your API keys
```

### 2. Understanding the Pipeline

**Pipeline Flow:**
```
Content → Ideas → Scripts → Scenes → Audio → Subtitles → 
Images → Video → Post-Production → Quality Control → Export
```

**Key Concepts:**
- **Stage**: A single processing step (e.g., "Generate Script")
- **Group**: Related stages (e.g., "Script Development" group has 5 stages)
- **Checkpoint**: Saved state for resume capability
- **Orchestrator**: Coordinates all stages

### 3. Implementing a Pipeline Stage

#### Template Structure

```csharp
using StoryGenerator.Pipeline.Interfaces;
using StoryGenerator.Pipeline.Config;

namespace StoryGenerator.Pipeline.Stages;

/// <summary>
/// [Stage description - what it does and why]
/// </summary>
public class MyStage : IPipelineStage<MyInput, MyOutput>
{
    private readonly ILogger<MyStage> _logger;
    private readonly PipelineConfig _config;
    private readonly IMyService _service;

    public string StageName => "my-stage";

    public MyStage(
        ILogger<MyStage> logger,
        PipelineConfig config,
        IMyService service)
    {
        _logger = logger ?? throw new ArgumentNullException(nameof(logger));
        _config = config ?? throw new ArgumentNullException(nameof(config));
        _service = service ?? throw new ArgumentNullException(nameof(service));
    }

    public async Task<MyOutput> ExecuteAsync(
        MyInput input, 
        CancellationToken cancellationToken = default)
    {
        _logger.LogInformation("Starting {StageName} stage", StageName);
        
        // Validate input
        if (!await ValidateInputAsync(input))
        {
            throw new InvalidOperationException("Invalid input for stage");
        }

        try
        {
            // Main processing logic
            var result = await ProcessAsync(input, cancellationToken);
            
            _logger.LogInformation("Completed {StageName} stage", StageName);
            return result;
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Error in {StageName} stage", StageName);
            throw;
        }
    }

    public async Task<bool> ValidateInputAsync(MyInput input)
    {
        // Validate input data
        return input != null && !string.IsNullOrEmpty(input.RequiredField);
    }

    private async Task<MyOutput> ProcessAsync(
        MyInput input, 
        CancellationToken cancellationToken)
    {
        // Implementation logic here
        var output = new MyOutput();
        
        // Example: Call service
        output.Data = await _service.ProcessAsync(input.Data);
        
        // Example: Save to file
        var outputPath = Path.Combine(
            _config.Paths.StoryRoot, 
            "output", 
            $"{input.Id}.json");
        await File.WriteAllTextAsync(outputPath, 
            JsonSerializer.Serialize(output), 
            cancellationToken);
        
        return output;
    }
}
```

#### Input/Output Models

```csharp
public class MyInput
{
    public string Id { get; set; } = string.Empty;
    public string RequiredField { get; set; } = string.Empty;
    public Dictionary<string, object> Metadata { get; set; } = new();
}

public class MyOutput
{
    public string Data { get; set; } = string.Empty;
    public DateTime CompletedAt { get; set; } = DateTime.UtcNow;
    public string OutputPath { get; set; } = string.Empty;
}
```

### 4. Writing Tests

#### Unit Test Example

```csharp
using Xunit;
using Moq;
using Microsoft.Extensions.Logging;

namespace StoryGenerator.Pipeline.Tests.Stages;

public class MyStageTests
{
    [Fact]
    public async Task ExecuteAsync_ValidInput_ReturnsOutput()
    {
        // Arrange
        var mockLogger = new Mock<ILogger<MyStage>>();
        var mockConfig = new PipelineConfig();
        var mockService = new Mock<IMyService>();
        
        mockService
            .Setup(s => s.ProcessAsync(It.IsAny<string>()))
            .ReturnsAsync("processed data");
        
        var stage = new MyStage(
            mockLogger.Object, 
            mockConfig, 
            mockService.Object);
        
        var input = new MyInput 
        { 
            Id = "test-1",
            RequiredField = "test data" 
        };
        
        // Act
        var output = await stage.ExecuteAsync(input);
        
        // Assert
        Assert.NotNull(output);
        Assert.Equal("processed data", output.Data);
        mockService.Verify(
            s => s.ProcessAsync(It.IsAny<string>()), 
            Times.Once);
    }
    
    [Fact]
    public async Task ValidateInputAsync_InvalidInput_ReturnsFalse()
    {
        // Arrange
        var stage = CreateStage();
        var input = new MyInput { RequiredField = "" };
        
        // Act
        var isValid = await stage.ValidateInputAsync(input);
        
        // Assert
        Assert.False(isValid);
    }
    
    [Fact]
    public async Task ExecuteAsync_ServiceThrows_ThrowsException()
    {
        // Arrange
        var mockService = new Mock<IMyService>();
        mockService
            .Setup(s => s.ProcessAsync(It.IsAny<string>()))
            .ThrowsAsync(new InvalidOperationException("Service error"));
        
        var stage = CreateStage(mockService.Object);
        var input = new MyInput { RequiredField = "test" };
        
        // Act & Assert
        await Assert.ThrowsAsync<InvalidOperationException>(
            () => stage.ExecuteAsync(input));
    }
    
    private MyStage CreateStage(IMyService? service = null)
    {
        var mockLogger = new Mock<ILogger<MyStage>>();
        var mockConfig = new PipelineConfig();
        service ??= new Mock<IMyService>().Object;
        
        return new MyStage(mockLogger.Object, mockConfig, service);
    }
}
```

### 5. Integration with Orchestrator

#### Register Stage in DI Container

```csharp
// In Program.cs or Startup.cs
services.AddScoped<IPipelineStage<MyInput, MyOutput>, MyStage>();
services.AddScoped<IMyService, MyServiceImplementation>();
```

#### Add to Orchestrator

```csharp
public class PipelineOrchestrator
{
    private readonly IPipelineStage<MyInput, MyOutput> _myStage;
    
    public async Task<string> RunFullPipelineAsync(string? storyTitle = null)
    {
        // ... other stages
        
        // Execute your stage
        if (_config.Pipeline.Steps.MyStageEnabled && 
            !checkpoint.IsStepComplete("my_stage"))
        {
            _logger.LogInfo("\n🎯 STEP X: My Stage");
            _logger.LogInfo(new string('-', 80));
            
            var input = new MyInput 
            { 
                Id = storyTitle,
                RequiredField = "data from previous stage" 
            };
            
            var output = await _myStage.ExecuteAsync(input);
            
            checkpoint.CompleteStep("my_stage", output.OutputPath);
            await _checkpointManager.SaveCheckpointAsync(checkpoint);
        }
        
        // ... next stages
    }
}
```

### 6. Configuration

Add stage configuration to `appsettings.json`:

```json
{
  "Pipeline": {
    "Steps": {
      "MyStageEnabled": true
    }
  },
  "MyStage": {
    "Timeout": 300,
    "MaxRetries": 3,
    "BatchSize": 10
  }
}
```

Load configuration in stage:

```csharp
public class MyStageConfig
{
    public int Timeout { get; set; } = 300;
    public int MaxRetries { get; set; } = 3;
    public int BatchSize { get; set; } = 10;
}

// In stage constructor
var myStageConfig = _config.GetSection("MyStage").Get<MyStageConfig>();
```

### 7. Error Handling

#### Retry Logic

```csharp
public async Task<MyOutput> ExecuteWithRetryAsync(
    MyInput input, 
    CancellationToken cancellationToken)
{
    var retryCount = 0;
    var maxRetries = _config.MyStage.MaxRetries;
    var delay = TimeSpan.FromSeconds(5);
    
    while (retryCount < maxRetries)
    {
        try
        {
            return await ExecuteAsync(input, cancellationToken);
        }
        catch (Exception ex) when (IsTransientError(ex))
        {
            retryCount++;
            _logger.LogWarning(
                "Transient error in {StageName}, retry {Count}/{Max}", 
                StageName, retryCount, maxRetries);
            
            if (retryCount >= maxRetries)
            {
                throw;
            }
            
            await Task.Delay(delay * retryCount, cancellationToken);
        }
    }
    
    throw new InvalidOperationException("Max retries exceeded");
}

private bool IsTransientError(Exception ex)
{
    return ex is HttpRequestException || 
           ex is TimeoutException ||
           ex is TaskCanceledException;
}
```

### 8. Progress Reporting

```csharp
public async Task<MyOutput> ExecuteAsync(
    MyInput input, 
    CancellationToken cancellationToken)
{
    var progress = new Progress<StageProgress>(p => 
    {
        _logger.LogInformation(
            "{StageName}: {Progress}% - {Message}", 
            StageName, p.PercentComplete, p.Message);
    });
    
    // Report progress at key points
    ((IProgress<StageProgress>)progress).Report(new StageProgress 
    { 
        PercentComplete = 25, 
        Message = "Input validated" 
    });
    
    // ... processing
    
    ((IProgress<StageProgress>)progress).Report(new StageProgress 
    { 
        PercentComplete = 50, 
        Message = "Processing..." 
    });
    
    // ... more processing
    
    ((IProgress<StageProgress>)progress).Report(new StageProgress 
    { 
        PercentComplete = 100, 
        Message = "Complete" 
    });
    
    return output;
}

public class StageProgress
{
    public int PercentComplete { get; set; }
    public string Message { get; set; } = string.Empty;
}
```

### 9. Best Practices

#### ✅ Do's

1. **Use dependency injection** for all dependencies
2. **Validate input** before processing
3. **Log at key points** (start, progress, completion, errors)
4. **Handle cancellation** via CancellationToken
5. **Save outputs to disk** for checkpoint/resume support
6. **Write comprehensive tests** (unit + integration)
7. **Document public APIs** with XML comments
8. **Use async/await** properly (avoid blocking)

#### ❌ Don'ts

1. **Don't hardcode paths** - use configuration
2. **Don't ignore CancellationToken** - check it periodically
3. **Don't swallow exceptions** - log and rethrow
4. **Don't block on async code** - use await
5. **Don't create new threads** - use Task-based patterns
6. **Don't use static state** - use instance fields
7. **Don't skip validation** - always validate input

### 10. Testing Your Stage

```bash
# Unit tests
dotnet test --filter "ClassName=MyStageTests"

# Integration test
dotnet test --filter "ClassName=MyStageIntegrationTests"

# Run in isolation
cd src/CSharp/StoryGenerator.CLI
dotnet run -- my-stage --input test-input.json --output test-output

# Debug with logs
export LOG_LEVEL=Debug
dotnet run -- my-stage --input test-input.json
```

### 11. Common Patterns

#### File I/O

```csharp
// Read JSON
var input = await JsonSerializer.DeserializeAsync<MyInput>(
    File.OpenRead(inputPath), 
    cancellationToken: cancellationToken);

// Write JSON
await using var stream = File.Create(outputPath);
await JsonSerializer.SerializeAsync(stream, output, 
    cancellationToken: cancellationToken);
```

#### HTTP Calls

```csharp
private readonly HttpClient _httpClient;

public async Task<string> CallApiAsync(
    string endpoint, 
    CancellationToken cancellationToken)
{
    using var timeout = new CancellationTokenSource(
        TimeSpan.FromSeconds(_config.MyStage.Timeout));
    using var linked = CancellationTokenSource.CreateLinkedTokenSource(
        cancellationToken, timeout.Token);
    
    var response = await _httpClient.GetAsync(endpoint, linked.Token);
    response.EnsureSuccessStatusCode();
    
    return await response.Content.ReadAsStringAsync(linked.Token);
}
```

#### Parallel Processing

```csharp
public async Task<List<MyOutput>> ProcessBatchAsync(
    List<MyInput> inputs, 
    CancellationToken cancellationToken)
{
    var tasks = inputs
        .Select(input => ExecuteAsync(input, cancellationToken))
        .ToList();
    
    var results = await Task.WhenAll(tasks);
    return results.ToList();
}
```

### 12. Debugging Tips

1. **Enable detailed logging:**
   ```bash
   export LOG_LEVEL=Debug
   ```

2. **Use breakpoints in VS Code:**
   - Set breakpoint in your stage
   - F5 to start debugging
   - Step through execution

3. **Check checkpoint files:**
   ```bash
   cat .pipeline_checkpoint.json | jq .
   ```

4. **Validate outputs:**
   ```bash
   # Check if output file created
   ls -lah output/
   
   # Validate JSON format
   jq . output/result.json
   ```

5. **Monitor resource usage:**
   ```bash
   # CPU and memory
   top
   
   # GPU usage
   nvidia-smi -l 1
   ```

### 13. Next Steps

1. **Pick a task** from the [Task Execution Matrix](../docs/TASK_EXECUTION_MATRIX.md)
2. **Create feature branch**: `git checkout -b feature/my-stage`
3. **Implement stage** following this guide
4. **Write tests** (aim for 80%+ coverage)
5. **Test locally** with sample data
6. **Create PR** with description and test results
7. **Address review comments**
8. **Merge and deploy**

## Resources

- [Pipeline Orchestration Guide](../docs/PIPELINE_ORCHESTRATION.md)
- [Implementation Roadmap](../docs/IMPLEMENTATION_ROADMAP.md)
- [Task Execution Matrix](../docs/TASK_EXECUTION_MATRIX.md)
- [C# Coding Standards](../src/CSharp/SOLID_OOP_CLEAN_CODE_GUIDE.md)

## Getting Help

- **Code Reviews:** Tag `@lead-developer` in PR
- **Questions:** Use GitHub Discussions
- **Bugs:** Create GitHub Issue with `bug` label
- **Documentation:** Update this guide with improvements

---

**Happy Coding! 🚀**
