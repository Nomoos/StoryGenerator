# StoryGenerator - C# Implementation

[![.NET](https://img.shields.io/badge/.NET-8.0-purple.svg)](https://dotnet.microsoft.com/download)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

## 🎯 Overview

The C# implementation of StoryGenerator provides a high-performance, type-safe alternative to the Python version. Built with modern .NET features, it offers improved performance, better tooling support, and production-ready reliability.

## ✨ Key Features

- **🚀 High Performance**: Async/await throughout, optimized for throughput
- **🔒 Type Safety**: Strong typing with nullable reference types
- **🔄 Resilience**: Polly-based retry and circuit breaker patterns
- **📊 Monitoring**: Built-in performance tracking and metrics
- **🔧 Extensible**: Clean architecture with dependency injection
- **📝 Well-Documented**: Comprehensive XML docs and migration guides

## 📦 Requirements

- .NET 8.0 or later
- OpenAI API key
- ElevenLabs API key (for voice generation)

## 🏗️ Architecture

```
CSharp/
├── StoryGenerator.Core/        # Core models, utilities, and services
│   ├── Models/                 # StoryIdea, ViralPotential
│   ├── Utils/                  # FileHelper, PathConfiguration
│   └── Services/               # PerformanceMonitor, RetryService
├── StoryGenerator.Providers/   # External API integrations
│   ├── OpenAI/                 # OpenAI API client
│   └── ElevenLabs/             # ElevenLabs TTS client
├── StoryGenerator.Generators/  # Content generation implementations
│   └── IdeaGenerator.cs        # ✅ Implemented
├── StoryGenerator.CLI/         # Command-line interface
└── StoryGenerator.Tests/       # Unit and integration tests
```

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/Nomoos/StoryGenerator.git
cd StoryGenerator/CSharp

# Build the solution
dotnet build

# Run tests
dotnet test
```

### Configuration

Create an `appsettings.json` file:

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
    "OutputFormat": "mp3_44100_192"
  },
  "PathConfiguration": {
    "StoryRoot": "./Stories"
  }
}
```

Or use environment variables:

```bash
export OpenAI__ApiKey="your-key"
export ElevenLabs__ApiKey="your-key"
```

### Usage Example

```csharp
using Microsoft.Extensions.DependencyInjection;
using StoryGenerator.Generators;

// Set up dependency injection
var services = new ServiceCollection();
ConfigureServices(services);
var serviceProvider = services.BuildServiceProvider();

// Generate story ideas
var ideaGenerator = serviceProvider.GetRequiredService<IIdeaGenerator>();
var ideas = await ideaGenerator.GenerateIdeasAsync(
    topic: "A person who discovers something unexpected",
    count: 5,
    tone: "emotional"
);

foreach (var idea in ideas)
{
    Console.WriteLine($"Title: {idea.StoryTitle}");
    Console.WriteLine($"Potential: {idea.Potential.Overall}/100");
}
```

## 📋 Implementation Status

### ✅ Phase 1: Core Infrastructure (Completed)

- [x] StoryIdea model with JSON serialization
- [x] ViralPotential scoring model
- [x] FileHelper utilities
- [x] PathConfiguration
- [x] PerformanceMonitor with metrics tracking
- [x] RetryService with Polly integration

### ✅ Phase 2: API Providers (Completed)

- [x] OpenAI client with chat completions
- [x] ElevenLabs client for TTS
- [x] Retry and circuit breaker integration
- [x] Strongly-typed request/response models

### ✅ Phase 3: Generators (Partial)

- [x] **IdeaGenerator** - Story idea generation with viral potential
- [ ] **ScriptGenerator** - ~360 word script generation
- [ ] **RevisionGenerator** - Script revision for voice clarity
- [ ] **EnhancementGenerator** - ElevenLabs tag enhancement
- [ ] **VoiceGenerator** - TTS with audio normalization

### 🔄 Phase 4: Advanced Features (Planned)

- [ ] SubtitleGenerator (WhisperX integration)
- [ ] VideoGenerator (FFmpeg wrapper)
- [ ] VideoPipelineGenerator
- [ ] VideoCompositor
- [ ] VideoInterpolator

### 🔄 Phase 5: Vision & AI (Planned)

- [ ] VisionGenerator
- [ ] SceneAnalyzer
- [ ] SceneDescriber
- [ ] KeyframeGenerator (SDXL)
- [ ] IncrementalImprover

## 🎨 C# Improvements Over Python

### Performance
- **Async I/O**: True non-blocking operations
- **Connection pooling**: Reused HTTP clients
- **Compiled code**: Native execution speed

### Reliability
- **Polly integration**: Exponential backoff and circuit breakers
- **Strong typing**: Compile-time error detection
- **Null safety**: Nullable reference types

### Developer Experience
- **IntelliSense**: Full IDE support
- **Refactoring**: Safe automated refactoring
- **Debugging**: Excellent debugging tools

### Maintainability
- **Dependency injection**: Testable, decoupled code
- **LINQ**: Expressive data transformations
- **XML docs**: Built-in documentation

## 📚 Documentation

- **[MIGRATION_GUIDE.md](MIGRATION_GUIDE.md)** - Complete migration guide from Python
- **[Interfaces/IGenerators.cs](Interfaces/IGenerators.cs)** - Generator interfaces
- **XML Documentation** - Inline with code

## 🔧 Development

### Building

```bash
dotnet build
```

### Running Tests

```bash
dotnet test
```

### Publishing

```bash
# Single-file executable
dotnet publish StoryGenerator.CLI -c Release -r win-x64 --self-contained -p:PublishSingleFile=true

# Cross-platform
dotnet publish StoryGenerator.CLI -c Release -r linux-x64 --self-contained
dotnet publish StoryGenerator.CLI -c Release -r osx-x64 --self-contained
```

## 🤝 Contributing

When implementing new generators:

1. Follow the IdeaGenerator pattern
2. Use async/await for all I/O operations
3. Integrate PerformanceMonitor for metrics
4. Use RetryService for external API calls
5. Add comprehensive logging
6. Write unit tests
7. Update documentation

See [MIGRATION_GUIDE.md](MIGRATION_GUIDE.md) for detailed implementation patterns.

## 📊 Performance Metrics

Performance monitoring is built-in. View metrics:

```csharp
var monitor = serviceProvider.GetRequiredService<PerformanceMonitor>();
var summary = await monitor.GetPerformanceSummaryAsync();

Console.WriteLine($"Total Operations: {summary.TotalOperations}");
Console.WriteLine($"Success Rate: {summary.SuccessRate}%");
```

Metrics are automatically saved to `logs/metrics.json`.

## 🐛 Troubleshooting

### API Key Issues
Ensure your API keys are properly configured in `appsettings.json` or environment variables.

### Build Errors
```bash
dotnet clean
dotnet restore
dotnet build
```

### Missing Dependencies
```bash
dotnet restore
```

## 📄 License

MIT License - see LICENSE file for details

## 🔗 Related Projects

- **Python Implementation**: [/Python](../Python/)
- **Documentation**: [/docs](../docs/)

## 👥 Contributors

- Initial C# port and architecture design
- OpenAI and ElevenLabs provider implementations
- Core infrastructure and utilities

## 📮 Support

For issues and questions:
- GitHub Issues: https://github.com/Nomoos/StoryGenerator/issues
- Documentation: See MIGRATION_GUIDE.md

## 🗺️ Roadmap

- [ ] Complete all generator implementations
- [ ] Add CLI with rich commands
- [ ] Implement configuration validation
- [ ] Add performance benchmarks vs Python
- [ ] Create Docker images
- [ ] Add API server (optional)
- [ ] Implement streaming responses
- [ ] Add batch processing support

## ⚙️ Configuration Options

Full configuration reference available in [MIGRATION_GUIDE.md](MIGRATION_GUIDE.md#configuration).

## 💻 Development Prerequisites

- [.NET 8.0 SDK](https://dotnet.microsoft.com/download)
- Visual Studio 2022, Rider, or VS Code
- Git

### Building

```bash
dotnet restore
dotnet build
```

### Testing

```bash
dotnet test
```

### Code Style

This project follows C# coding conventions:
- PascalCase for public members
- camelCase for private fields with _ prefix
- 4 spaces for indentation
- Use of `var` when type is obvious
- Async methods end with `Async`

## 🔄 Migration from Python

When the C# implementation is complete, migration guides will be provided to help transition from the Python version.

Key differences to be aware of:
- **API**: Different method signatures and patterns
- **Configuration**: JSON-based instead of .env files
- **Async**: All generator methods will be async
- **Types**: Strong typing vs Python's dynamic typing

## 📈 Roadmap

### Phase 1: Core Infrastructure
- [ ] Set up solution structure
- [ ] Implement core models
- [ ] Create service interfaces
- [ ] Set up dependency injection
- [ ] Implement configuration system

### Phase 2: Generator Implementation
- [ ] Port IdeaGenerator
- [ ] Port ScriptGenerator
- [ ] Port RevisionGenerator
- [ ] Port EnhancementGenerator
- [ ] Port VoiceGenerator

### Phase 3: Testing & Quality
- [ ] Unit tests for all components
- [ ] Integration tests
- [ ] Code coverage > 80%
- [ ] Performance benchmarks

### Phase 4: CLI & Deployment
- [ ] Command-line interface
- [ ] NuGet package publishing
- [ ] Docker support
- [ ] CI/CD pipeline

### Phase 5: Advanced Features
- [ ] Web API
- [ ] Web UI
- [ ] Batch processing
- [ ] Cloud deployment guides

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Follow C# coding conventions
4. Add unit tests
5. Submit a pull request

## 📞 Support

For questions or issues:
- Check the [main README](../README.md)
- Open a GitHub issue
- Review [ARCHITECTURE.md](../ARCHITECTURE.md)

## 📄 License

[Same as main project]

---

**Status**: 🚧 Under Development  
**Target Release**: TBD  
**Current Progress**: Planning & Design Phase

Check back soon for updates!
