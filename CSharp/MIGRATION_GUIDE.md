# C# Implementation - Migration Guide

## Overview

This document provides a comprehensive guide for the C# port of the StoryGenerator Python codebase. The C# implementation provides feature parity with improved performance, type safety, and maintainability.

## Architecture

### Project Structure

```
CSharp/
├── StoryGenerator.Core/           # Core models, utilities, and services
│   ├── Models/                    # Data models (StoryIdea, ViralPotential)
│   ├── Utils/                     # Utilities (FileHelper, PathConfiguration)
│   └── Services/                  # Core services (PerformanceMonitor, RetryService)
├── StoryGenerator.Providers/      # External API integrations
│   ├── OpenAI/                    # OpenAI API client
│   └── ElevenLabs/                # ElevenLabs TTS API client
├── StoryGenerator.Generators/     # Content generation implementations
│   └── IdeaGenerator.cs           # Story idea generation
├── StoryGenerator.CLI/            # Command-line interface
└── StoryGenerator.Tests/          # Unit and integration tests
```

### Key Design Patterns

1. **Dependency Injection**: All components use constructor injection for dependencies
2. **Async/Await**: All I/O operations are asynchronous
3. **Retry Pattern**: Polly library for exponential backoff and circuit breaker
4. **Structured Logging**: Microsoft.Extensions.Logging throughout
5. **Options Pattern**: Configuration via strongly-typed options classes

## Completed Components

### Phase 1: Core Infrastructure ✅

#### Models

**StoryIdea** (`StoryGenerator.Core/Models/StoryIdea.cs`)
- Full property parity with Python version
- JSON serialization with snake_case naming
- Async file I/O operations
- Automatic viral potential calculation

**ViralPotential** (`StoryGenerator.Core/Models/StoryIdea.cs`)
- Platform, region, age group, and gender scoring
- Overall score calculation

#### Utilities

**FileHelper** (`StoryGenerator.Core/Utils/FileHelper.cs`)
- Filename sanitization (cross-platform)
- Language code to name mapping
- Directory operations
- Async file read/write

**PathConfiguration** (`StoryGenerator.Core/Utils/PathConfiguration.cs`)
- Centralized path management
- Standard folder structure (0_Ideas, 1_Scripts, etc.)
- Story folder path helpers

#### Services

**PerformanceMonitor** (`StoryGenerator.Core/Services/PerformanceMonitor.cs`)
- Operation timing and metrics tracking
- JSON-based metrics persistence
- Performance summary generation
- Structured logging integration

**RetryService** (`StoryGenerator.Core/Services/RetryService.cs`)
- Exponential backoff retry policy
- Circuit breaker pattern
- Per-service circuit breaker instances
- Combined retry + circuit breaker support

### Phase 2: API Providers ✅

#### OpenAI Provider

**OpenAIClient** (`StoryGenerator.Providers/OpenAI/OpenAIClient.cs`)
- Chat completion API
- Strongly-typed request/response models
- Retry and circuit breaker integration
- HTTP client-based implementation

**OpenAIOptions** (`StoryGenerator.Providers/OpenAI/OpenAIOptions.cs`)
- API key configuration
- Model selection (default: gpt-4o-mini)
- Temperature and max tokens
- Custom API base URL support

#### ElevenLabs Provider

**ElevenLabsClient** (`StoryGenerator.Providers/ElevenLabs/ElevenLabsClient.cs`)
- Text-to-speech generation
- Voice settings configuration
- Audio file saving
- Streaming support ready

**ElevenLabsOptions** (`StoryGenerator.Providers/ElevenLabs/ElevenLabsOptions.cs`)
- API key configuration
- Voice ID and model selection
- Output format configuration
- Default voice settings

### Phase 3: Generators ✅

#### IdeaGenerator

**IIdeaGenerator** (`StoryGenerator.Generators/IIdeaGenerator.cs`)
- Interface definition for story idea generation

**IdeaGenerator** (`StoryGenerator.Generators/IdeaGenerator.cs`)
- Complete port of Python GStoryIdeas.py
- Async idea generation
- JSON response parsing with error handling
- Performance monitoring integration
- Batch idea generation and file saving

## Configuration

### appsettings.json Example

```json
{
  "OpenAI": {
    "ApiKey": "your-openai-api-key",
    "Model": "gpt-4o-mini",
    "Temperature": 0.9
  },
  "ElevenLabs": {
    "ApiKey": "your-elevenlabs-api-key",
    "VoiceId": "BZgkqPqms7Kj9ulSkVzn",
    "Model": "eleven_v3",
    "OutputFormat": "mp3_44100_192",
    "VoiceStability": 0.5,
    "VoiceSimilarityBoost": 0.75,
    "VoiceStyleExaggeration": 0.0
  },
  "PathConfiguration": {
    "StoryRoot": "./Stories"
  },
  "Logging": {
    "LogLevel": {
      "Default": "Information",
      "Microsoft": "Warning"
    }
  }
}
```

### Environment Variables

For production, use environment variables or user secrets:

```bash
export OpenAI__ApiKey="your-key"
export ElevenLabs__ApiKey="your-key"
```

## Dependency Injection Setup

```csharp
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Logging;
using StoryGenerator.Core.Services;
using StoryGenerator.Core.Utils;
using StoryGenerator.Generators;
using StoryGenerator.Providers.ElevenLabs;
using StoryGenerator.Providers.OpenAI;

var services = new ServiceCollection();

// Logging
services.AddLogging(builder => builder.AddConsole());

// Configuration
services.Configure<OpenAIOptions>(configuration.GetSection(OpenAIOptions.SectionName));
services.Configure<ElevenLabsOptions>(configuration.GetSection(ElevenLabsOptions.SectionName));

// Core services
services.AddSingleton<PathConfiguration>();
services.AddSingleton<PerformanceMonitor>();
services.AddSingleton<RetryService>();

// HTTP clients
services.AddHttpClient<OpenAIClient>();
services.AddHttpClient<ElevenLabsClient>();

// Generators
services.AddScoped<IIdeaGenerator, IdeaGenerator>();

var serviceProvider = services.BuildServiceProvider();
```

## Usage Examples

### Generate Story Ideas

```csharp
var ideaGenerator = serviceProvider.GetRequiredService<IIdeaGenerator>();
var pathConfig = serviceProvider.GetRequiredService<PathConfiguration>();

// Generate ideas
var ideas = await ideaGenerator.GenerateIdeasAsync(
    topic: "A person who discovers something unexpected",
    count: 5,
    tone: "emotional",
    theme: "family"
);

// Save ideas to files
var savedPaths = await ideaGenerator.GenerateAndSaveIdeasAsync(
    topic: "A person who discovers something unexpected",
    outputDirectory: pathConfig.IdeasPath,
    count: 5
);

foreach (var path in savedPaths)
{
    Console.WriteLine($"Saved: {path}");
}
```

### Load Existing Story Idea

```csharp
var ideaPath = Path.Combine(pathConfig.IdeasPath, "My_Story.json");
var idea = await StoryIdea.FromFileAsync(ideaPath);

Console.WriteLine($"Title: {idea.StoryTitle}");
Console.WriteLine($"Overall Potential: {idea.Potential.Overall}");
```

## Remaining Work

### Phase 3: Primary Generators

The following generators need to be implemented following the IdeaGenerator pattern:

1. **ScriptGenerator** (Python: `GScript.py`)
   - Generates ~360 word scripts from StoryIdea
   - Uses OpenAI with custom system/user prompts
   - Includes personalization support
   - Multi-language support

2. **RevisionGenerator** (Python: `GRevise.py`)
   - Revises scripts for AI voice clarity
   - Removes awkward phrasing
   - Optimizes for TTS synthesis

3. **EnhancementGenerator** (Python: `GEnhanceScript.py`)
   - Adds ElevenLabs voice tags
   - Emotion and pacing markers
   - Non-destructive text enhancement

4. **VoiceGenerator** (Python: `GVoice.py`)
   - TTS generation with ElevenLabs
   - Audio normalization (LUFS)
   - Silence trimming and padding

### Implementation Template for New Generators

```csharp
public interface IXxxGenerator : IGenerator
{
    Task<Result> GenerateAsync(Input input, CancellationToken cancellationToken = default);
}

public class XxxGenerator : IXxxGenerator
{
    private readonly OpenAIClient _openAIClient;  // or ElevenLabsClient
    private readonly ILogger<XxxGenerator> _logger;
    private readonly PerformanceMonitor _performanceMonitor;
    private readonly PathConfiguration _pathConfiguration;

    public string Name => "XxxGenerator";
    public string Version => "1.0.0";

    public XxxGenerator(
        OpenAIClient openAIClient,
        ILogger<XxxGenerator> logger,
        PerformanceMonitor performanceMonitor,
        PathConfiguration pathConfiguration)
    {
        _openAIClient = openAIClient;
        _logger = logger;
        _performanceMonitor = performanceMonitor;
        _pathConfiguration = pathConfiguration;
    }

    public async Task<Result> GenerateAsync(
        Input input,
        CancellationToken cancellationToken = default)
    {
        return await _performanceMonitor.MeasureAsync(
            "Operation_Name",
            input.StoryTitle,
            async () => await GenerateInternalAsync(input, cancellationToken),
            new Dictionary<string, object> { /* metrics */ });
    }

    private async Task<Result> GenerateInternalAsync(
        Input input,
        CancellationToken cancellationToken)
    {
        // Implementation
        _logger.LogInformation("Starting generation...");
        
        // Use OpenAI or ElevenLabs client
        // Process result
        // Return
    }
}
```

### Phase 4: Advanced Generators

These require additional external dependencies:

- **SubtitleGenerator**: WhisperX integration
- **VideoGenerator**: FFmpeg wrapper
- **VideoPipelineGenerator**: Orchestrates video pipeline
- **VideoCompositor**: Combines audio/video/subtitles
- **VideoInterpolator**: Frame interpolation

### Phase 5: Vision & AI Features

These are optional enhancements:

- **VisionGenerator**: LLaVA-OneVision integration
- **SceneAnalyzer**: Scene understanding
- **SceneDescriber**: Visual prompt generation
- **KeyframeGenerator**: SDXL integration
- **IncrementalImprover**: Iterative content improvement

## Python to C# Mapping

### Common Patterns

| Python | C# |
|--------|-----|
| `def method():` | `public async Task MethodAsync()` |
| `with open(file):` | `await File.ReadAllTextAsync(file)` |
| `try/except` | `try/catch` |
| `json.loads()` | `JsonSerializer.Deserialize<T>()` |
| `@decorator` | `await _retryService.ExecuteWithRetryAsync()` |
| `time.time()` | `Stopwatch.StartNew()` |
| `os.path.join()` | `Path.Combine()` |

### Naming Conventions

| Python | C# |
|--------|-----|
| `snake_case` | `PascalCase` (public), `camelCase` (private) |
| `__init__` | Constructor |
| `self` | `this` |
| Type hints optional | Strong typing required |

## Testing

### Unit Test Example

```csharp
using Xunit;
using Moq;
using Microsoft.Extensions.Logging;

public class IdeaGeneratorTests
{
    [Fact]
    public async Task GenerateIdeasAsync_ReturnsCorrectCount()
    {
        // Arrange
        var mockClient = new Mock<OpenAIClient>();
        var mockLogger = new Mock<ILogger<IdeaGenerator>>();
        var monitor = new PerformanceMonitor(Mock.Of<ILogger<PerformanceMonitor>>());
        var pathConfig = new PathConfiguration();
        
        var generator = new IdeaGenerator(
            mockClient.Object,
            mockLogger.Object,
            monitor,
            pathConfig);

        // Act
        var ideas = await generator.GenerateIdeasAsync("test topic", count: 3);

        // Assert
        Assert.Equal(3, ideas.Count);
    }
}
```

## Performance Optimizations

### Already Implemented

1. **Async I/O**: All file and network operations are async
2. **Connection pooling**: HttpClient instances are reused
3. **Circuit breaker**: Prevents cascading failures
4. **Exponential backoff**: Reduces API rate limit issues

### Future Optimizations

1. **JSON Source Generators**: Compile-time JSON serialization
2. **Memory pooling**: Reduce GC pressure
3. **Parallel processing**: Process multiple stories concurrently
4. **Caching**: Cache frequently accessed data
5. **Span<T>**: Zero-allocation string operations

## Deployment

### Single-File Executable

```bash
dotnet publish StoryGenerator.CLI -c Release -r win-x64 --self-contained -p:PublishSingleFile=true
```

### Docker

```dockerfile
FROM mcr.microsoft.com/dotnet/runtime:8.0
WORKDIR /app
COPY published/ .
ENTRYPOINT ["dotnet", "StoryGenerator.CLI.dll"]
```

## Migration Checklist

- [x] Core models (StoryIdea, ViralPotential)
- [x] Core utilities (FileHelper, PathConfiguration)
- [x] Core services (PerformanceMonitor, RetryService)
- [x] OpenAI provider
- [x] ElevenLabs provider
- [x] IdeaGenerator
- [ ] ScriptGenerator
- [ ] RevisionGenerator
- [ ] EnhancementGenerator
- [ ] VoiceGenerator
- [ ] SubtitleGenerator
- [ ] VideoGenerator
- [ ] VideoPipelineGenerator
- [ ] VideoCompositor
- [ ] VideoInterpolator
- [ ] VisionGenerator
- [ ] SceneAnalyzer
- [ ] SceneDescriber
- [ ] KeyframeGenerator
- [ ] IncrementalImprover
- [ ] CLI implementation
- [ ] Unit tests
- [ ] Integration tests
- [ ] Documentation
- [ ] Performance benchmarks

## Contributing

When implementing new generators:

1. Follow the established patterns (see IdeaGenerator)
2. Use async/await for all I/O
3. Integrate PerformanceMonitor
4. Use RetryService for external API calls
5. Add structured logging
6. Write unit tests
7. Update this documentation

## References

- Python codebase: `/Python/Generators/`
- C# interfaces: `CSharp/Interfaces/IGenerators.cs`
- Polly documentation: https://www.pollydocs.org/
- OpenAI API: https://platform.openai.com/docs/
- ElevenLabs API: https://elevenlabs.io/docs/
