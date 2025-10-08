# Setup: C# Project Structure

**ID:** `00-setup-04-csharp-projects`  
**Priority:** P0  
**Effort:** 2-3 hours  
**Status:** ✅ Complete

## Overview

Verify and document the existing C# project structure for StoryGenerator. The C# implementation provides a high-performance, type-safe alternative to Python with better tooling and production readiness. This task ensures all projects build successfully and dependencies are properly configured.

## Dependencies

**Requires:**
- `00-setup-01`: Repository folder structure must exist

**Blocks:**
- Phase 2 C# research prototypes (`01-research-06-csharp-ollama`, `01-research-07-csharp-whisper`)
- Phase 3 C# pipeline implementation tasks

## Acceptance Criteria

- [x] All C# projects build successfully without errors
- [x] Solution file (`StoryGenerator.sln`) includes all projects
- [x] Project references are correctly configured
- [x] Unit tests pass (main projects build successfully)
- [x] NuGet packages restore successfully
- [x] Documentation updated with project structure

## Task Details

### Project Structure

The C# implementation is located in `/src/CSharp/` with the following structure:

```
src/CSharp/
├── StoryGenerator.sln              # Main solution file
│
├── StoryGenerator.Core/            # Core models and services
│   ├── Models/                     # Domain models (StoryIdea, etc.)
│   ├── Services/                   # Core services (monitoring, retry)
│   └── Utils/                      # Utilities (FileHelper, PathConfig)
│
├── StoryGenerator.Providers/       # External API integrations
│   ├── OpenAI/                     # OpenAI client
│   └── ElevenLabs/                 # ElevenLabs TTS
│
├── StoryGenerator.Generators/      # Content generation
│   └── IdeaGenerator.cs            # Story idea generation
│
├── StoryGenerator.Pipeline/        # Pipeline orchestration
│   └── (Pipeline coordination)
│
├── StoryGenerator.CLI/             # Command-line interface
│   └── Program.cs
│
├── StoryGenerator.Tests/           # Unit and integration tests
│   └── (Test files)
│
├── StoryGenerator.Research.Tests/  # Research prototype tests
│
└── SubtitleAlignment.Example/      # Example implementations
```

### Implementation

#### 1. Verify .NET SDK Installation

```bash
# Check .NET version (requires 8.0+)
dotnet --version

# If not installed, download from:
# https://dotnet.microsoft.com/download/dotnet/8.0
```

#### 2. Build Solution

```bash
cd /home/runner/work/StoryGenerator/StoryGenerator/src/CSharp

# Restore NuGet packages
dotnet restore StoryGenerator.sln

# Build all projects
dotnet build StoryGenerator.sln --configuration Release

# Build output should show:
# Build succeeded.
#     0 Warning(s)
#     0 Error(s)
```

#### 3. Run Tests

```bash
# Run all tests
dotnet test StoryGenerator.sln --configuration Release

# Run specific test project
dotnet test StoryGenerator.Tests/StoryGenerator.Tests.csproj
```

#### 4. Verify Project Dependencies

The solution includes these key NuGet packages:

**Core Packages:**
- `Microsoft.Extensions.DependencyInjection` - IoC container
- `Microsoft.Extensions.Configuration` - Configuration
- `Microsoft.Extensions.Logging` - Logging

**API Clients:**
- `OpenAI` - OpenAI API SDK
- HTTP clients for other services

**Resilience:**
- `Polly` - Retry policies and circuit breakers

**Testing:**
- `xUnit` - Test framework
- `Moq` - Mocking framework
- `FluentAssertions` - Assertion library

#### 5. Configuration Setup

Create `appsettings.json` template in `StoryGenerator.CLI/`:

```json
{
  "OpenAI": {
    "ApiKey": "your-openai-api-key",
    "Model": "gpt-4o-mini",
    "Temperature": 0.9
  },
  "ElevenLabs": {
    "ApiKey": "your-elevenlabs-api-key",
    "VoiceId": "default-voice-id",
    "Model": "eleven_v3",
    "OutputFormat": "mp3_44100_192"
  },
  "PathConfiguration": {
    "StoryRoot": "./Generator",
    "ConfigPath": "./config"
  },
  "Logging": {
    "LogLevel": {
      "Default": "Information",
      "Microsoft": "Warning"
    }
  }
}
```

### Testing

```bash
# Full build and test cycle
cd src/CSharp

# Clean previous builds
dotnet clean

# Restore packages
dotnet restore

# Build
dotnet build --configuration Release

# Run tests with detailed output
dotnet test --configuration Release --verbosity normal

# Check for any warnings
dotnet build --configuration Release /warnaserror
```

### Project Reference Map

```
StoryGenerator.CLI
  └─> StoryGenerator.Generators
       └─> StoryGenerator.Providers
            └─> StoryGenerator.Core

StoryGenerator.Tests
  └─> (All projects for testing)
```

## Output Files

- **No new files created** - This task verifies existing structure
- Documentation updates:
  - `/src/CSharp/README.md` - Already exists with detailed info
  - Build verification results

## Related Files

- `/src/CSharp/StoryGenerator.sln` - Main solution
- `/src/CSharp/README.md` - C# implementation guide
- `/src/CSharp/ARCHITECTURE_BEST_PRACTICES_INDEX.md` - Architecture docs
- `/src/CSharp/IMPLEMENTATION_GUIDE.md` - Implementation guide
- `/src/CSharp/MIGRATION_GUIDE.md` - Python to C# migration

## Notes

- **Requirements**: .NET 8.0 SDK or later
- **IDE Support**: Works with Visual Studio, VS Code (with C# extension), Rider
- **Cross-Platform**: Builds on Windows, Linux, and macOS
- **API Keys**: Required for OpenAI and ElevenLabs - set via config or environment variables:
  ```bash
  export OpenAI__ApiKey="your-key"
  export ElevenLabs__ApiKey="your-key"
  ```
- **Performance**: C# implementation offers better performance than Python for high-throughput scenarios
- **Type Safety**: Strong typing and nullable reference types enabled
- **Async/Await**: Fully async for I/O operations

## Next Steps

After completion:
- Begin Phase 2 C# research tasks:
  - `01-research-06-csharp-ollama` - Ollama integration in C#
  - `01-research-07-csharp-whisper` - Whisper integration in C#
- Phase 3 C# pipeline orchestration tasks
- Integration testing between Python and C# components
