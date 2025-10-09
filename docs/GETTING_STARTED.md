# Getting Started with StoryGenerator

This guide will help you get up and running with the StoryGenerator pipeline in 15 minutes.

## Prerequisites

Before you begin, ensure you have:

- **.NET 9.0 SDK or later** - [Download here](https://dotnet.microsoft.com/download/dotnet/9.0)
- **Git** - For cloning the repository
- **API Keys** (for production use):
  - [OpenAI API Key](https://platform.openai.com/api-keys) - For GPT-based script generation
  - [ElevenLabs API Key](https://elevenlabs.io/app/settings/api-keys) - For voice generation
- **Optional**: Python 3.11+ (for ML model inference like Whisper ASR, SDXL, LTX-Video)
- **Optional**: CUDA-capable GPU (for local ML model inference)

## Quick Start (5 Minutes)

### 1. Clone the Repository

```bash
git clone https://github.com/Nomoos/StoryGenerator.git
cd StoryGenerator
```

### 2. Navigate to C# Implementation

```bash
cd src/CSharp
```

### 3. Build the Solution

```bash
dotnet restore
dotnet build StoryGenerator.sln
```

### 4. Run Tests (Optional)

```bash
dotnet test
```

### 5. Set Up Environment Variables

```bash
# Copy the example environment file
cp .env.example .env

# Edit .env and add your API keys
# - OpenAI__ApiKey=your-openai-key
# - ElevenLabs__ApiKey=your-elevenlabs-key
```

## Understanding the Architecture

StoryGenerator uses a **hybrid C# + Python architecture**:

- **C# (.NET 9.0)**: Orchestration, APIs, I/O, configuration, and business logic
- **Python**: ML model inference via subprocess calls (Whisper ASR, SDXL, LTX-Video)

The C# implementation is the **primary and actively maintained** version.

## Project Structure

```
StoryGenerator/
├── src/CSharp/                    # C# implementation (PRIMARY)
│   ├── StoryGenerator.Core/       # Core models and utilities
│   ├── StoryGenerator.Providers/  # API client implementations
│   ├── StoryGenerator.Generators/ # Content generators
│   ├── StoryGenerator.Pipeline/   # Pipeline orchestration
│   ├── StoryGenerator.CLI/        # Command-line interface
│   ├── StoryGenerator.Data/       # Data access layer
│   └── StoryGenerator.Tests/      # Unit tests
├── docs/                          # Documentation
├── data/                          # Generated content storage
└── research/                      # Research prototypes
```

## Next Steps

### For Developers

1. **Review Architecture Documentation**:
   - [ARCHITECTURE.md](ARCHITECTURE.md) - System architecture overview
   - [Technology Stack](TECHNOLOGY_STACK_FINAL.md) - Recommended technology stack
   - [C# Implementation Guide](../src/CSharp/IMPLEMENTATION_GUIDE.md)

2. **Explore the Pipeline**:
   - [Pipeline Overview](PIPELINE.md) - Complete pipeline breakdown
   - [Pipeline Orchestration](PIPELINE_ORCHESTRATION.md) - Orchestration details
   - [Quick Start Guide](QUICK_START_GUIDE.md) - Developer quick start for pipeline stages

3. **Learn About Specific Components**:
   - [Idea Collector](IDEA_COLLECTOR.md) - Content source collection
   - [Script Improvement](SCRIPT_IMPROVEMENT_QUICKSTART.md) - Script enhancement
   - [Title Improvement](TITLE_IMPROVEMENT.md) - Title optimization
   - [Video Export](VIDEO_EXPORT.md) - Video export and metadata

### For Content Creators

1. **Understand the Pipeline Stages**:
   - Idea Collection → Script Generation → Voice Generation → Video Synthesis
   - See [PIPELINE.md](PIPELINE.md) for detailed stage information

2. **Configure for Your Needs**:
   - Review [GPU Comparison Guide](GPU_COMPARISON.md) for hardware recommendations
   - Check [RTX 5090 Quick Reference](RTX5090_QUICKREF.md) for optimal setup

3. **Generate Your First Story**:
   - Follow examples in [EXAMPLES.md](EXAMPLES.md)
   - Use the CLI tools in `src/CSharp/StoryGenerator.CLI/`

## Common Tasks

### Building the Solution

```bash
cd src/CSharp
dotnet build StoryGenerator.sln --configuration Release
```

### Running Tests

```bash
cd src/CSharp
dotnet test --configuration Release
```

### Running the Pipeline

```bash
cd src/CSharp/StoryGenerator.Pipeline
dotnet run --configuration Release
```

## Troubleshooting

If you encounter issues, see:
- [TROUBLESHOOTING.md](TROUBLESHOOTING.md) - Common issues and solutions
- [GitHub Issues](https://github.com/Nomoos/StoryGenerator/issues) - Report bugs or ask questions

## Security Best Practices

⚠️ **IMPORTANT**: Never commit API keys to version control!

1. Use the `.env` file for sensitive configuration
2. Rotate API keys regularly
3. Follow guidelines in [SECURITY_CHECKLIST.md](../SECURITY_CHECKLIST.md)

## Getting Help

- **Documentation**: Start with [INDEX.md](INDEX.md) for navigation
- **Issues**: Create a [GitHub Issue](https://github.com/Nomoos/StoryGenerator/issues/new)
- **Discussions**: Join [GitHub Discussions](https://github.com/Nomoos/StoryGenerator/discussions)

## What's Next?

- ✅ You've set up the development environment
- 📖 Review the [Pipeline Documentation](PIPELINE.md)
- 🔨 Follow the [Implementation Roadmap](IMPLEMENTATION_ROADMAP.md)
- 🚀 Start contributing to the project!

---

**Welcome to StoryGenerator! 🎉**
