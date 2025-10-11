# StoryGenerator - PrismQ Framework

A comprehensive, modular framework for automated story generation, media processing, and multi-platform content distribution.

## 🏗️ Project Structure

This project follows a clean, namespace-based architecture with all components organized at the top level:

```
StoryGenerator/
├── PrismQ/                    # Main Python application namespace
│   ├── Core/                  # Core utilities and shared components
│   │   └── Shared/           # Configuration, logging, database, models
│   ├── Content/               # Content generation modules
│   │   ├── IdeaScraper/      # Idea generation and scraping
│   │   ├── StoryGenerator/   # Story and script development
│   │   ├── StoryTitleProcessor/ # Title generation
│   │   ├── StoryTitleScoring/   # Title quality scoring
│   │   ├── SceneDescriptions/   # Scene planning
│   │   ├── DescriptionGenerator/ # Metadata descriptions
│   │   └── TagsGenerator/       # Tag generation
│   ├── Media/                 # Media processing modules
│   │   ├── VoiceOverGenerator/  # Voice synthesis
│   │   ├── SubtitleGenerator/   # Subtitle generation
│   │   ├── VideoGenerator/      # Video assembly
│   │   └── FrameInterpolation/  # Frame processing
│   ├── Platform/              # Platform integrations
│   │   ├── Providers/        # Service providers (OpenAI, etc.)
│   │   └── Pipeline/         # Pipeline orchestration
│   ├── Utilities/             # Tools and utilities
│   │   ├── Tools/            # Publishing tools
│   │   └── Scripts/          # Automation scripts
│   └── Documentation/         # Examples and guides
│       └── Examples/         # Usage examples
├── CSharp/                    # C# implementation
│   ├── PrismQ/               # C# PrismQ modules
│   └── MLScripts/            # ML subprocess scripts
├── Tests/                     # Test suite
├── Documentation/             # Project documentation
├── Configuration/             # Configuration files
├── Assets/                    # Static assets
├── Data/                      # Runtime data
├── Research/                  # Research documents
├── Issues/                    # Issue tracking
├── Podcasts/                  # Podcast content
├── .github/                   # GitHub workflows and config
├── pyproject.toml            # Python project configuration
├── requirements.txt           # Python dependencies
└── README.md                  # This file
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
from PrismQ.Core.Shared.config import settings
from PrismQ.Content.IdeaScraper.idea_generation import IdeaGenerator
from PrismQ.Platform.Providers import OpenAIProvider

# Configure
api_key = settings.openai_api_key

# Generate ideas
generator = IdeaGenerator()
ideas = generator.generate()
```

## 📦 Namespace Organization

### Core (`PrismQ/Core/`)
Foundation components including configuration, logging, database utilities, error handling, caching, and data models.

### Content (`PrismQ/Content/`)
All content generation and processing modules for ideas, stories, titles, scenes, and metadata.

### Media (`PrismQ/Media/`)
Media processing pipeline for audio, video, subtitles, and frame processing.

### Platform (`PrismQ/Platform/`)
External service integrations including LLM providers, platform providers (YouTube, TikTok, etc.), and pipeline orchestration.

### Utilities (`PrismQ/Utilities/`)
Tools for publishing, quality checking, and automation scripts.

### Documentation (`PrismQ/Documentation/`)
Usage examples, guides, and demonstrations.

## 🎯 Key Features

- **Modular Architecture**: Clean namespace-based organization
- **Multi-Platform Support**: YouTube, TikTok, Instagram, Facebook, WordPress
- **AI-Powered Content**: Automated story generation and optimization
- **Media Pipeline**: Complete audio/video processing workflow
- **Quality Tools**: Automated quality checking and scoring
- **Extensible Design**: Easy to add new providers and modules

## 📚 Documentation

- **Getting Started**: See `Documentation/guides/`
- **API Reference**: See `PrismQ/README.md`
- **Examples**: See `PrismQ/Documentation/Examples/`
- **Migration Guide**: See `Documentation/migration/`

## 🧪 Testing

```bash
# Run all tests
pytest Tests/

# Run specific test suite
pytest Tests/test_core_config.py
```

## 🤝 Contributing

See `Documentation/CONTRIBUTING.md` for contribution guidelines.

## 📄 License

See LICENSE file for details.

## 🔗 Links

- [Project Documentation](Documentation/)
- [API Documentation](PrismQ/README.md)
- [Issue Tracker](Issues/)
