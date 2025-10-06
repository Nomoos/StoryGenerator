# StoryGenerator - C# Implementation

## 🚧 Under Development

The C# implementation of StoryGenerator is currently under development. This will be the **primary/preferred** implementation going forward.

## 🎯 Goals

- **Performance**: Faster execution compared to Python
- **Type Safety**: Strong typing with compile-time checks
- **Modern Features**: Async/await, LINQ, and more
- **Cross-Platform**: Run on Windows, macOS, and Linux with .NET
- **Easy Deployment**: Single binary deployment
- **Better Tooling**: Excellent IDE support (Visual Studio, Rider, VS Code)

## 📋 Planned Architecture

```
CSharp/
├── StoryGenerator.Core/        # Core library
│   ├── Models/                 # Data models
│   ├── Interfaces/             # Abstractions
│   └── Services/               # Business logic
├── StoryGenerator.Generators/  # Generator implementations
│   ├── IdeaGenerator.cs
│   ├── ScriptGenerator.cs
│   ├── RevisionGenerator.cs
│   ├── EnhancementGenerator.cs
│   └── VoiceGenerator.cs
├── StoryGenerator.Providers/   # External service providers
│   ├── OpenAI/                 # OpenAI integration
│   └── ElevenLabs/             # ElevenLabs integration
├── StoryGenerator.CLI/         # Command-line interface
├── StoryGenerator.API/         # Web API (optional)
└── StoryGenerator.Tests/       # Unit and integration tests
```

## 🚀 Quick Start (Coming Soon)

```bash
# Clone the repository
git clone https://github.com/Nomoos/StoryGenerator.git
cd StoryGenerator/CSharp

# Build the solution
dotnet build

# Run the CLI
dotnet run --project StoryGenerator.CLI -- generate-ideas --topic "your topic"
```

## 📦 Requirements

- .NET 8.0 or later
- OpenAI API key
- ElevenLabs API key (for voice generation)

## ⚙️ Configuration

Configuration will be managed through:
- `appsettings.json` for application settings
- Environment variables for secrets
- User secrets for local development

Example configuration:
```json
{
  "OpenAI": {
    "ApiKey": "YOUR_API_KEY",
    "Model": "gpt-4o-mini",
    "Temperature": 0.9
  },
  "ElevenLabs": {
    "ApiKey": "YOUR_API_KEY",
    "VoiceId": "BZgkqPqms7Kj9ulSkVzn",
    "Model": "eleven_v3"
  },
  "Storage": {
    "StoriesPath": "./Stories"
  }
}
```

## 🔧 Features (Planned)

- ✅ **Async/Await**: Native async support for better performance
- ✅ **Dependency Injection**: Built-in DI container
- ✅ **Strong Typing**: Compile-time type safety
- ✅ **LINQ**: Powerful query capabilities
- ✅ **NuGet Packages**: Easy dependency management
- ✅ **Unit Testing**: Comprehensive test coverage
- ✅ **Logging**: Built-in logging infrastructure
- ✅ **Configuration**: Flexible configuration system
- ✅ **CLI**: Rich command-line interface
- ✅ **API**: RESTful API (optional)

## ✨ Features (Implemented)

### Video Post-Production 🎬

**Status**: ✅ **Implemented and Ready**

Complete video post-production pipeline for processing raw video segments into polished, social-media-ready content.

**Features:**
- ✅ Crop videos to 9:16 aspect ratio (1080×1920) at 30fps
- ✅ Burn-in or soft subtitles from SRT files with safe text margins
- ✅ Background music mixing with audio ducking during voiceover
- ✅ Video concatenation with smooth transitions
- ✅ Final encoding with H.264, 8Mbps bitrate, AAC audio
- ✅ Automatic output path formatting: `/final/{segment}/{age}/{title_id}_draft.mp4`

**Quick Start:**
```csharp
using StoryGenerator.Models;
using StoryGenerator.Tools;

var producer = new VideoPostProducer();
var config = new VideoPostProductionConfig
{
    SegmentPaths = new List<string> { "video1.mp4", "video2.mp4" },
    OutputPath = "final/tech/18-23/my_video_draft.mp4",
    SrtPath = "subtitles.srt",
    BackgroundMusicPath = "music.mp3",
    Fps = 30,
    MusicVolume = 0.2,
    EnableDucking = true
};

string output = await producer.ProduceVideoAsync(config);
```

**Documentation:**
- [Quick Start Guide](POST_PRODUCTION_QUICKSTART.md) - Get started in 5 minutes
- [Complete Documentation](POST_PRODUCTION_CSHARP.md) - Full API reference and examples
- [Example Code](Examples/VideoPostProductionExample.cs) - Working examples

**Requirements:**
- FFmpeg must be installed and available in PATH
- .NET 8.0 or later

## 💻 Development

### Prerequisites

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
- [x] Implement core models (VideoPostProductionConfig, VideoClip, etc.)
- [x] Create service interfaces (IVideoPostProducer)
- [ ] Set up dependency injection
- [ ] Implement configuration system

### Phase 2: Generator Implementation
- [ ] Port IdeaGenerator
- [ ] Port ScriptGenerator
- [ ] Port RevisionGenerator
- [ ] Port EnhancementGenerator
- [ ] Port VoiceGenerator
- [x] **Implement VideoPostProducer** ✅

### Phase 2.5: Video Post-Production ✅ **COMPLETED**
- [x] Crop videos to 9:16 (1080×1920) at 30fps
- [x] Add subtitle support (burn-in and soft subtitles)
- [x] Background music mixing with ducking
- [x] Video concatenation with transitions
- [x] Safe text margins for subtitles
- [x] Final encoding with target specifications
- [x] Output path formatting (/final/{segment}/{age}/{title_id}_draft.mp4)
- [x] Complete documentation and examples

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
