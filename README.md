# StoryGenerator - AI Video Content Pipeline

> **An AI-driven video content pipeline that creates engaging short-form vertical videos for TikTok, YouTube Shorts, and Instagram Reels.**

Transform story ideas into complete videos with AI-powered voiceovers, subtitles, and visual content. Built with a modern **hybrid C# + Python architecture** combining .NET 9.0's performance with Python's ML ecosystem.

---

## 🚀 Quick Links

<table>
<tr>
<td width="50%">

### 🏁 Getting Started
- **[Quick Start Guide](docs/quickstarts/general/GETTING_STARTED.md)** - Get up and running in 15 minutes
- **[Installation](docs/guides/setup/INSTALLATION.md)** - Detailed setup instructions
- **[Hardware Requirements](docs/hardware/HARDWARE_REQUIREMENTS.md)** - Choose the right hardware
- **[Troubleshooting](docs/guides/general/TROUBLESHOOTING.md)** - Common issues and solutions

</td>
<td width="50%">

### 📖 Core Documentation
- **[Features](docs/features/FEATURES.md)** - Complete feature list
- **[Pipeline Overview](docs/pipeline/PIPELINE.md)** - How the pipeline works
- **[Architecture](docs/architecture/ARCHITECTURE.md)** - System design
- **[Examples](docs/EXAMPLES.md)** - Input/output examples

</td>
</tr>
<tr>
<td>

### 🔨 For Developers
- **[C# Implementation Guide](src/CSharp/IMPLEMENTATION_GUIDE.md)** - Development guide
- **[Pipeline Quick Start](docs/quickstarts/general/QUICK_START_GUIDE.md)** - Developer quick start
- **[SOLID Principles](src/CSharp/SOLID_OOP_CLEAN_CODE_GUIDE.md)** - Code standards
- **[Testing Guide](docs/testing/tdd/TDD_GUIDE.md)** - Test-driven development
- **[Contributing](CONTRIBUTING.md)** - How to contribute

</td>
<td>

### 🎨 For Content Creators
- **[Idea Collector](docs/content/ideas/IDEA_COLLECTOR.md)** - Content source collection
- **[Script Improvement](docs/quickstarts/content/SCRIPT_IMPROVEMENT_QUICKSTART.md)** - Enhance scripts
- **[Title Optimization](docs/content/ideas/TITLE_IMPROVEMENT.md)** - Viral title generation
- **[Video Export](docs/content/video/VIDEO_EXPORT.md)** - Export and metadata
- **[Quality Control](docs/content/video/VIDEO_QUALITY_CONTROL.md)** - QC reports
- **[Platform Integration](docs/guides/integration/PLATFORM_INTEGRATION.md)** - 🚀 **NEW: YouTube, TikTok, Instagram**

</td>
</tr>
<tr>
<td>

### 🔬 Research & Architecture
- **[Technology Stack](docs/architecture/hybrid/TECHNOLOGY_STACK_FINAL.md)** - C# + Python + SQLite
- **[Hybrid Architecture](docs/architecture/hybrid/HYBRID_ARCHITECTURE_QUICKREF.md)** - Architecture guide
- **[Hybrid Roadmap](docs/roadmaps/HYBRID_ROADMAP.md)** - 📋 Complete implementation status
- **[Roadmap Analysis](docs/roadmaps/ROADMAP_ANALYSIS.md)** - 🎯 **NEW: Current status & next steps**
- **[GPU Comparison](docs/hardware/GPU_COMPARISON.md)** - Hardware benchmarks
- **[Models Documentation](docs/features/MODELS.md)** - ML model references
- **[C# vs Python](docs/architecture/hybrid/CSHARP_VS_PYTHON_COMPARISON.md)** - Technology comparison

</td>
<td>

### 🔐 Security & Maintenance
- **[Security Checklist](docs/features/system/SECURITY_CHECKLIST.md)** - Security procedures
- **[Repository Cleanup](CLEANUP_REPO.md)** - Maintenance guide
- **[Issue Tracking](docs/guides/issues/ISSUE_TRACKING.md)** - Task management
- **[Migration Guide](src/CSharp/MIGRATION_GUIDE.md)** - Python to C#
- **[Roadmap](docs/roadmaps/IMPLEMENTATION_ROADMAP.md)** - Development timeline

</td>
</tr>
</table>

---

## 🎯 What is StoryGenerator?

StoryGenerator automates the creation of emotional, dramatic vertical stories targeting viewers aged 10-30 in the US, Canada, and Australia. The pipeline transforms story ideas into complete videos with voiceovers, subtitles, and visual content.

**Key Features:**
- 🎯 AI-powered story idea generation with viral potential scoring
- ✍️ GPT-4 script generation optimized for short-form video
- 🎙️ Professional voice synthesis using ElevenLabs
- 📝 Word-level subtitle alignment with WhisperX
- 🎬 Complete video export with metadata and thumbnails
- 📊 Automated quality control and reporting
- 🚀 **Platform integration for YouTube, TikTok, and Instagram**
- 📈 **Analytics collection and performance tracking**

➡️ **[See full feature list](docs/features/FEATURES.md)**

---

## 🏗️ Architecture Overview

StoryGenerator uses a **hybrid C# + Python architecture**:

- **C# (.NET 9.0)**: Orchestration, APIs, I/O, configuration, and business logic
- **Python**: ML model inference via subprocess calls (Whisper ASR, SDXL, LTX-Video)

**Why Hybrid?**
- C# provides performance, type safety, and excellent tooling
- Python gives access to the rich ML ecosystem
- Best of both worlds for production-grade content generation

➡️ **[Learn more about the architecture](docs/architecture/ARCHITECTURE.md)**

---

## ⚡ Quick Start

### Prerequisites
- **.NET 9.0 SDK** - [Download](https://dotnet.microsoft.com/download/dotnet/9.0)
- **Git** - For cloning the repository
- **API Keys** (optional): [OpenAI](https://platform.openai.com/api-keys), [ElevenLabs](https://elevenlabs.io/app/settings/api-keys)

> 💡 **For local model inference**: Install [optional dependencies](docs/guides/setup/OPTIONAL_DEPENDENCIES.md) (FFmpeg, Ollama, Python/faster-whisper)

### Get Started in 5 Minutes

```bash
# 1. Clone the repository
git clone https://github.com/Nomoos/StoryGenerator.git
cd StoryGenerator

# 2. Navigate to C# implementation
cd src/CSharp

# 3. Build the solution
dotnet restore
dotnet build StoryGenerator.sln

# 4. Run tests (optional)
dotnet test

# 5. Set up environment (optional for API usage)
cp .env.example .env
# Edit .env and add your API keys
```

### Optional: Install Local Model Dependencies

For local model inference (alternative to cloud APIs):

```bash
# Install FFmpeg (audio/video processing)
# Ubuntu: sudo apt install ffmpeg
# macOS: brew install ffmpeg
# Windows: choco install ffmpeg

# Install Ollama (local LLM)
# Visit: https://ollama.com/download

# Install Python + faster-whisper (speech-to-text)
pip install faster-whisper>=0.10.0
```

➡️ **[Complete local setup guide](docs/guides/setup/OPTIONAL_DEPENDENCIES.md)**

➡️ **[Complete setup guide](docs/quickstarts/general/GETTING_STARTED.md)** | **[Troubleshooting](docs/guides/general/TROUBLESHOOTING.md)**

---

## 🏗️ Pipeline Stages

The complete pipeline consists of several major stages:

| Stage | Status | Description |
|-------|--------|-------------|
| **Idea Collection** | ✅ Complete | Gather story ideas from multiple sources |
| **Script Generation** | ✅ Complete | Generate ~360-word scripts with GPT-4 |
| **Script Improvement** | ✅ Complete | Iterative refinement with quality scoring |
| **Title Optimization** | ✅ Complete | Generate and score title variations |
| **Voice Generation** | ✅ Complete | Professional AI voice with ElevenLabs |
| **Subtitle Generation** | ✅ Complete | Word-level alignment with WhisperX |
| **Video Export** | ✅ Complete | Export with metadata and thumbnails |
| **Keyframe Generation** | 🔄 Planned | SDXL-based image generation |
| **Video Synthesis** | 🔄 Planned | LTX-Video or Stable Video Diffusion |
| **Post-Production** | 🔄 Planned | Subtitle overlay and final rendering |

➡️ **[Detailed pipeline documentation](docs/pipeline/PIPELINE.md)** | **[Implementation roadmap](docs/roadmaps/IMPLEMENTATION_ROADMAP.md)**

---

## 📂 Project Structure

```
StoryGenerator/
├── src/CSharp/                    # C# implementation (PRIMARY)
│   ├── StoryGenerator.Core/       # Core models and utilities
│   ├── StoryGenerator.Providers/  # API client implementations
│   ├── StoryGenerator.Generators/ # Content generators
│   ├── StoryGenerator.Pipeline/   # Pipeline orchestration
│   ├── StoryGenerator.CLI/        # Command-line interface
│   └── StoryGenerator.Tests/      # Unit tests
├── docs/                          # Documentation
├── data/                          # Generated content storage
└── research/                      # Research prototypes
```

➡️ **[Complete structure documentation](docs/architecture/structure/REPOSITORY_STRUCTURE.md)**

---

## 🤖 AI Models & Technology Stack

**Core Technologies:**
- **C# .NET 9.0** - Primary orchestration and business logic
- **OpenAI GPT-4** - Script generation and improvement
- **ElevenLabs** - Professional voice synthesis
- **WhisperX** - Speech recognition and subtitle alignment
- **SDXL** - Image generation (planned)
- **LTX-Video** - Video synthesis (planned)

➡️ **[Complete model documentation](docs/features/MODELS.md)** | **[Technology stack details](docs/architecture/hybrid/TECHNOLOGY_STACK_FINAL.md)**

---

## 🎯 Target Audience & Content

- **Age Range**: 10-30 years old
- **Regions**: United States, Canada, Australia
- **Platforms**: TikTok, YouTube Shorts, Instagram Reels
- **Content Style**: Emotional drama, identity, connection, viral-optimized

➡️ **[Content strategy guide](docs/content/ideas/CONTENT_RANKING.md)**

---

## 💻 Development & Contributing

We welcome contributions! Whether you're fixing bugs, adding features, or improving documentation, your help is appreciated.

**Getting Started:**
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Follow the [C# Implementation Guide](src/CSharp/IMPLEMENTATION_GUIDE.md)
4. Write tests for your changes
5. Submit a pull request

➡️ **[Contributing guidelines](CONTRIBUTING.md)** | **[Code standards](src/CSharp/SOLID_OOP_CLEAN_CODE_GUIDE.md)** | **[Testing guide](docs/testing/tdd/TDD_GUIDE.md)**

---

## 📋 Project Status & Roadmap

> **📊 For complete implementation status, progress tracking, and detailed roadmap, see [Hybrid Architecture Roadmap](docs/roadmaps/HYBRID_ROADMAP.md)**

**Current Status:**
- ✅ Phase 1: Foundation Complete (15/15 tasks, 100%)
- 🔄 Phase 2: Pipeline Orchestration (0/5 tasks, 15%)
- 🔄 Phase 3: P1 High Priority (30/47 tasks, 64%)
- 📋 Phase 4: P2 Medium Priority (0/18 tasks, 0%)

**Quick Links:**
- [Hybrid Roadmap](docs/roadmaps/HYBRID_ROADMAP.md) - Complete status and progress tracking
- [Roadmap Analysis](docs/roadmaps/ROADMAP_ANALYSIS.md) - Current status and next steps
- [Issue Tracking](issues/README.md) - Task organization by priority

---

## 🔐 Security

⚠️ **Important Security Notice:**

- **Never commit API keys** to version control
- Use `.env` files for sensitive configuration
- Rotate API keys regularly
- Follow security best practices

➡️ **[Security checklist](docs/features/system/SECURITY_CHECKLIST.md)** | **[Security procedures](docs/features/system/SECURITY_CHECKLIST.md)**

---

## 📞 Support & Community

- 📖 **Documentation**: [INDEX.md](docs/INDEX.md) - Complete documentation index
- 🐛 **Bug Reports**: [GitHub Issues](https://github.com/Nomoos/StoryGenerator/issues)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/Nomoos/StoryGenerator/discussions)
- 🆘 **Troubleshooting**: [TROUBLESHOOTING.md](docs/guides/general/TROUBLESHOOTING.md)

---

## 📄 License

[Add your license here]

---

## 🙏 Acknowledgments

- **OpenAI** - GPT models for script generation
- **ElevenLabs** - Professional voice synthesis
- **Stability AI** - Image and video generation models
- **Microsoft** - .NET platform
- **Community Contributors** - Thank you for your contributions!

---

<div align="center">

**Built with ❤️ using C# .NET 9.0 and Python**

[Getting Started](docs/quickstarts/general/GETTING_STARTED.md) • [Documentation](docs/INDEX.md) • [GitHub](https://github.com/Nomoos/StoryGenerator)

</div>
