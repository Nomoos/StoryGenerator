# StoryGenerator - PrismQ Framework

A comprehensive, modular framework for automated story generation, media processing, and multi-platform content distribution.

## 🏗️ Project Structure

This project follows a **pipeline-based architecture** organized by content creation stages:

```
StoryGenerator/
├── PrismQ/                    # Main project namespace
│   ├── Pipeline/              # Content Creation Pipeline (Sequential Stages)
│   │   ├── 01_IdeaGeneration/       # Stage 1: Idea Generation
│   │   │   └── IdeaScraper/         # Idea scraping and generation
│   │   ├── 02_TextGeneration/       # Stage 2: Text Content
│   │   │   ├── StoryGenerator/      # Story and script development
│   │   │   ├── StoryTitleProcessor/ # Title generation
│   │   │   ├── StoryTitleScoring/   # Title quality scoring
│   │   │   ├── SceneDescriptions/   # Scene planning
│   │   │   ├── DescriptionGenerator/# Metadata descriptions
│   │   │   ├── TagsGenerator/       # Tag generation
│   │   │   └── FinalizeText/        # Text finalization
│   │   ├── 03_AudioGeneration/      # Stage 3: Audio Content
│   │   │   ├── VoiceOverGenerator/  # Voice synthesis
│   │   │   ├── SubtitleGenerator/   # Subtitle generation
│   │   │   └── FinalizeAudio/       # Audio finalization
│   │   ├── 04_ImageGeneration/      # Stage 4: Image Content
│   │   │   └── SparseKeyFramesGenerator/ # Keyframe generation
│   │   └── 05_VideoGeneration/      # Stage 5: Video Assembly
│   │       ├── VideoGenerator/      # Video assembly
│   │       ├── FrameInterpolation/  # Frame processing
│   │       └── FinalizeVideo/       # Video finalization
│   │
│   ├── Infrastructure/        # Core Infrastructure
│   │   ├── Core/             # Shared utilities and configuration
│   │   ├── Platform/         # External service integrations
│   │   └── Utilities/        # Tools, scripts, and automation
│   │
│   ├── Resources/            # Project Resources
│   │   ├── Assets/          # Static media assets
│   │   ├── Data/            # Runtime data
│   │   └── Configuration/   # Configuration files
│   │
│   ├── Development/          # Development Resources
│   │   ├── Tests/           # Test suite
│   │   ├── Examples/        # Usage examples
│   │   └── Documentation/   # Project documentation
│   │
│   └── Projects/             # Related Projects
│       ├── CSharp/          # C# implementation
│       ├── Research/        # Research documents
│       ├── Issues/          # Issue tracking
│       └── Podcasts/        # Podcast content
│
├── .github/                  # GitHub workflows and config
├── pyproject.toml           # Python project configuration
├── requirements.txt          # Python dependencies
└── README.md                 # This file
```

## 🚀 Quick Start

### Installation

```bash
# Install dependencies
pip install -r requirements.txt

# For development
pip install -r requirements-dev.txt
```

### Basic Usage

```python
from PrismQ.Pipeline.01_IdeaGeneration.IdeaScraper.idea_generation import IdeaGenerator
from PrismQ.Infrastructure.Core.Shared.config import settings
from PrismQ.Infrastructure.Platform.Providers import OpenAIProvider

# Configure
api_key = settings.openai_api_key

# Generate ideas
generator = IdeaGenerator()
ideas = generator.generate()
```

## 📦 Pipeline Stages

### Stage 1: Idea Generation (`Pipeline/01_IdeaGeneration/`)
Generate and scrape content ideas from various sources.

### Stage 2: Text Generation (`Pipeline/02_TextGeneration/`)
Create story scripts, titles, descriptions, and scene plans.

### Stage 3: Audio Generation (`Pipeline/03_AudioGeneration/`)
Generate voice-overs and subtitles for the content.

### Stage 4: Image Generation (`Pipeline/04_ImageGeneration/`)
Create keyframes and visual elements.

### Stage 5: Video Generation (`Pipeline/05_VideoGeneration/`)
Assemble and finalize the complete video.

## 🎯 Key Features

- **Pipeline-Based Architecture**: Sequential stages from idea to video
- **Multi-Platform Support**: YouTube, TikTok, Instagram, Facebook, WordPress
- **AI-Powered Content**: Automated story generation and optimization
- **Complete Workflow**: Idea → Text → Audio → Images → Video
- **Quality Tools**: Automated quality checking and scoring
- **Extensible Design**: Easy to add new pipeline stages

## 📚 Documentation

### 🎯 New: Comprehensive Repository Documentation

- **[Repository Overview](REPOSITORY_OVERVIEW.md)** - Complete repository structure and architecture
- **[SOLID Principles Guide](SOLID_PRINCIPLES_IMPLEMENTATION.md)** - Real-world SOLID examples from this codebase
- **[Project Splitting Guide](PROJECT_SPLITTING_GUIDE.md)** - How to extract components for smaller projects
- **[Reference Guide](REFERENCE_GUIDE_FOR_SMALL_PROJECTS.md)** - Quick reference for developers building small projects

### Existing Documentation

- **Getting Started**: See `PrismQ/Development/Documentation/guides/`
- **API Reference**: See `PrismQ/README.md`
- **Examples**: See `PrismQ/Development/Examples/`
- **Migration Guide**: See `PrismQ/Development/Documentation/migration/`
- **Complete Index**: See `PrismQ/Development/Documentation/INDEX.md`

## 🧪 Testing

```bash
# Run all tests
pytest PrismQ/Development/Tests/

# Run specific test suite
pytest PrismQ/Development/Tests/test_core_config.py
```

## 🤝 Contributing

See `PrismQ/Development/Documentation/CONTRIBUTING.md` for contribution guidelines.

## 📄 License

See LICENSE file for details.

## 🔗 Links

- [Project Documentation](PrismQ/Development/Documentation/)
- [API Documentation](PrismQ/README.md)
- [Issue Tracker](PrismQ/Projects/Issues/)
