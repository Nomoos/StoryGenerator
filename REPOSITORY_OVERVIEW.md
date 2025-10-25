# StoryGenerator Repository Overview

## 📋 Table of Contents
- [Purpose and Vision](#purpose-and-vision)
- [Repository Architecture](#repository-architecture)
- [Core Design Philosophy](#core-design-philosophy)
- [Technology Stack](#technology-stack)
- [Key Components](#key-components)
- [SOLID Principles Implementation](#solid-principles-implementation)
- [Getting Started](#getting-started)
- [Related Documentation](#related-documentation)

## Purpose and Vision

**StoryGenerator** (PrismQ Framework) is a comprehensive, modular framework for automated story generation, media processing, and multi-platform content distribution. The repository is designed as a **reference implementation** demonstrating best practices in:

- **Modular Architecture**: Clean separation of concerns across pipeline stages
- **SOLID Principles**: Interface-driven design with dependency inversion
- **Extensibility**: Easy to add new providers, stages, and features
- **Testability**: Components designed for independent testing
- **Reusability**: Components can be extracted for smaller projects

### Primary Use Cases

1. **Full Pipeline Execution**: Complete workflow from idea generation to video publishing
2. **Component Extraction**: Use individual stages in smaller projects
3. **Reference Implementation**: Learn SOLID principles and clean architecture
4. **Educational Resource**: Understand production-level Python/C# hybrid systems

## Repository Architecture

### High-Level Structure

```
StoryGenerator/
├── PrismQ/                         # Main Framework Namespace
│   ├── Pipeline/                   # Content Creation Pipeline (5 Stages)
│   │   ├── 01_IdeaGeneration/     # Stage 1: Content idea sourcing
│   │   ├── 02_TextGeneration/     # Stage 2: Script and metadata
│   │   ├── 03_AudioGeneration/    # Stage 3: Voice and subtitles
│   │   ├── 04_ImageGeneration/    # Stage 4: Visual keyframes
│   │   └── 05_VideoGeneration/    # Stage 5: Video assembly
│   │
│   ├── Infrastructure/             # Shared Infrastructure
│   │   ├── Core/                  # Configuration, logging, shared utilities
│   │   ├── Platform/              # External service integrations
│   │   └── Utilities/             # Tools and automation scripts
│   │
│   ├── Resources/                  # Project Resources
│   │   ├── Assets/                # Static media files
│   │   ├── Data/                  # Runtime data and templates
│   │   └── Configuration/         # Configuration files
│   │
│   ├── Development/                # Development Resources
│   │   ├── Tests/                 # Test suite
│   │   ├── Examples/              # Usage examples
│   │   └── Documentation/         # Comprehensive docs
│   │
│   └── Projects/                   # Related Projects
│       ├── CSharp/                # C# implementation
│       ├── Research/              # Research and experiments
│       └── Issues/                # Issue tracking
│
├── requirements.txt                # Python dependencies
├── pyproject.toml                 # Python project configuration
└── README.md                      # Quick start guide
```

### Architecture Patterns

The repository implements a **Hybrid Architecture** combining:

1. **Pipeline Architecture**: Sequential stages for content creation
2. **Layered Architecture**: Clear separation between pipeline, infrastructure, and resources
3. **Plugin Architecture**: Swappable providers (OpenAI, local models, etc.)
4. **Repository Pattern**: Data access abstraction
5. **Strategy Pattern**: Different implementations for same interface

## Core Design Philosophy

### 1. Separation of Concerns

Each component has a **single, well-defined responsibility**:

- **Pipeline Stages**: Focused on content transformation (idea → text → audio → image → video)
- **Infrastructure**: Provides reusable services (logging, caching, retry logic)
- **Providers**: Handle external integrations (OpenAI, YouTube, TikTok)
- **Resources**: Store configuration and data

### 2. Interface-Driven Design

All major components implement **abstract interfaces**:

```python
# Example: LLM Provider Interface
class ILLMProvider(ABC):
    @abstractmethod
    def generate_completion(self, prompt: str, **kwargs) -> str:
        pass
    
    @property
    @abstractmethod
    def model_name(self) -> str:
        pass
```

**Benefits**:
- Easy to swap implementations (OpenAI → Local Model)
- Testable with mock providers
- Clear contracts between components

### 3. Dependency Inversion

High-level modules don't depend on low-level modules. Both depend on **abstractions**:

```python
# High-level module depends on interface, not concrete implementation
class StoryGenerator:
    def __init__(self, llm_provider: ILLMProvider):
        self.llm = llm_provider  # Depends on abstraction
    
    def generate(self, prompt: str) -> str:
        return self.llm.generate_completion(prompt)

# Concrete implementations
generator = StoryGenerator(OpenAIProvider())  # Production
generator_test = StoryGenerator(MockLLMProvider())  # Testing
```

### 4. Modular and Composable

Components can be used **independently** or **composed**:

```python
# Use individual stage
from PrismQ.Pipeline.02_TextGeneration.StoryTitleProcessor import TitleGenerator
title_gen = TitleGenerator()

# Or compose full pipeline
from PrismQ.Infrastructure.Platform.Pipeline import PipelineOrchestrator
pipeline = PipelineOrchestrator()
result = pipeline.run_all_stages(input_data)
```

## Technology Stack

### Core Technologies

- **Python 3.10+**: Main implementation language
- **C# .NET 8**: High-performance components
- **TypeScript**: Type safety and tooling
- **Git**: Version control with conventional commits

### Key Libraries

#### Python Dependencies
- **praw**: Reddit API integration
- **requests**: HTTP client
- **pytest**: Testing framework
- **black/ruff**: Code formatting and linting
- **mypy**: Static type checking

#### Development Tools
- **pre-commit**: Git hooks for quality checks
- **pytest-cov**: Code coverage
- **flake8**: Linting

### External Services

- **OpenAI API**: LLM for text generation
- **YouTube API**: Video publishing
- **TikTok API**: Short-form video distribution
- **Instagram API**: Social media publishing

## Key Components

### 1. Pipeline Stages

Each stage is **independently testable** and follows the `IPipelineStage` interface:

#### Stage 1: Idea Generation
- **Purpose**: Generate or scrape content ideas
- **Input**: Configuration (audience, topics)
- **Output**: List of validated ideas
- **Providers**: Reddit scraper, topic clusterer

#### Stage 2: Text Generation
- **Purpose**: Create story scripts and metadata
- **Components**: StoryGenerator, TitleProcessor, SceneDescriptions, TagsGenerator
- **Input**: Idea/topic
- **Output**: Complete script with title, description, tags

#### Stage 3: Audio Generation
- **Purpose**: Generate voice-over and subtitles
- **Components**: VoiceOverGenerator, SubtitleGenerator
- **Input**: Script text
- **Output**: Audio file + SRT subtitle file

#### Stage 4: Image Generation
- **Purpose**: Create visual keyframes
- **Components**: SparseKeyFramesGenerator
- **Input**: Scene descriptions
- **Output**: Keyframe images

#### Stage 5: Video Generation
- **Purpose**: Assemble final video
- **Components**: VideoGenerator, FrameInterpolation
- **Input**: Audio + keyframes
- **Output**: Rendered video file

### 2. Infrastructure Components

#### Core Shared Services
Located in `PrismQ/Infrastructure/Core/Shared/`:

- **config.py**: Centralized configuration management
- **logging.py**: Structured logging with context
- **database.py**: Data persistence layer
- **validation.py**: Input/output validation
- **cache.py**: Caching layer for API responses
- **retry.py**: Retry logic with exponential backoff

#### Interfaces
Located in `PrismQ/Infrastructure/Core/Shared/interfaces/`:

- **pipeline_stage.py**: `IPipelineStage` interface
- **llm_provider.py**: `ILLMProvider` interface
- **platform_provider.py**: `IPlatformProvider` interface
- **storage_provider.py**: `IStorageProvider` interface
- **voice_provider.py**: `IVoiceProvider` interface

#### Platform Providers
Located in `PrismQ/Infrastructure/Platform/Providers/`:

- **openai_provider.py**: OpenAI API integration
- **youtube_provider.py**: YouTube publishing
- **tiktok_provider.py**: TikTok publishing
- **mock_provider.py**: Testing mock

### 3. Resources

#### Configuration
- **regions/**: Regional settings (US, DE, JP, etc.)
- **config/**: Audience targeting, schemas
- **prompts/**: LLM prompt templates

#### Data
- **ideas/**: Generated content ideas
- **topics/**: Topic databases
- **titles/**: Title registry

## SOLID Principles Implementation

The repository is designed as a **reference implementation** of SOLID principles. See [SOLID_PRINCIPLES_IMPLEMENTATION.md](./SOLID_PRINCIPLES_IMPLEMENTATION.md) for detailed examples.

### Quick Overview

1. **Single Responsibility Principle (SRP)**
   - Each class has one reason to change
   - Example: `PerformanceMonitor` only handles metrics, `RetryService` only handles retries

2. **Open/Closed Principle (OCP)**
   - Open for extension, closed for modification
   - Example: Add new LLM providers by implementing `ILLMProvider` interface

3. **Liskov Substitution Principle (LSP)**
   - Derived classes can replace base classes
   - Example: Any `ILLMProvider` implementation works in place of another

4. **Interface Segregation Principle (ISP)**
   - Clients shouldn't depend on unused methods
   - Example: Separate `ILLMProvider` and `IAsyncLLMProvider` interfaces

5. **Dependency Inversion Principle (DIP)**
   - Depend on abstractions, not concretions
   - Example: Pipeline stages depend on `ILLMProvider`, not `OpenAIProvider`

## Getting Started

### Prerequisites

- Python 3.10 or higher
- Git
- Optional: C# .NET 8 SDK (for C# components)

### Installation

```bash
# Clone repository
git clone https://github.com/Nomoos/StoryGenerator.git
cd StoryGenerator

# Install Python dependencies
pip install -r requirements.txt

# For development
pip install -r requirements-dev.txt

# Run tests
pytest PrismQ/Development/Tests/
```

### Quick Start

```python
from PrismQ.Infrastructure.Core.Shared.config import settings
from PrismQ.Infrastructure.Platform.Providers import OpenAIProvider
from PrismQ.Pipeline.02_TextGeneration.StoryGenerator import StoryGenerator

# Configure
settings.openai_api_key = "your-key"

# Create generator with dependency injection
llm = OpenAIProvider()
generator = StoryGenerator(llm)

# Generate story
story = generator.generate("A tale about a brave knight")
print(story)
```

### Running the Full Pipeline

```python
from PrismQ.Infrastructure.Platform.Pipeline import PipelineOrchestrator

# Initialize orchestrator
orchestrator = PipelineOrchestrator()

# Run complete pipeline
result = orchestrator.run_all_stages({
    "topic": "technology trends",
    "audience": "developers",
    "platform": "youtube"
})

print(f"Video created: {result.video_path}")
```

## Related Documentation

### For Learning SOLID Principles
- [SOLID_PRINCIPLES_IMPLEMENTATION.md](./SOLID_PRINCIPLES_IMPLEMENTATION.md) - Detailed SOLID examples from this codebase
- [PrismQ/Development/Documentation/csharp/architecture/SOLID_OOP_CLEAN_CODE_GUIDE.md](./PrismQ/Development/Documentation/csharp/architecture/SOLID_OOP_CLEAN_CODE_GUIDE.md) - C# SOLID guide

### For Extracting Components
- [PROJECT_SPLITTING_GUIDE.md](./PROJECT_SPLITTING_GUIDE.md) - How to extract components for smaller projects
- [REFERENCE_GUIDE_FOR_SMALL_PROJECTS.md](./REFERENCE_GUIDE_FOR_SMALL_PROJECTS.md) - Quick reference for developers

### Architecture Documentation
- [PrismQ/Development/Documentation/architecture/ARCHITECTURE.md](./PrismQ/Development/Documentation/architecture/ARCHITECTURE.md) - Detailed architecture
- [PrismQ/Development/Documentation/architecture/REPOSITORY_STRUCTURE.md](./PrismQ/Development/Documentation/architecture/structure/REPOSITORY_STRUCTURE.md) - Folder structure

### API Documentation
- [PrismQ/README.md](./PrismQ/README.md) - PrismQ framework overview
- [README.md](./README.md) - Project quick start

### Development Guides
- [PrismQ/Development/Documentation/INDEX.md](./PrismQ/Development/Documentation/INDEX.md) - Complete documentation index
- [PrismQ/Development/Documentation/CONTRIBUTING.md](./PrismQ/Development/Documentation/CONTRIBUTING.md) - Contribution guidelines
- [PrismQ/Development/Documentation/CODE_STYLE_GUIDE.md](./PrismQ/Development/Documentation/CODE_STYLE_GUIDE.md) - Code style

## Support and Community

- **Issues**: [GitHub Issues](https://github.com/Nomoos/StoryGenerator/issues)
- **Documentation**: [Full Documentation Index](./PrismQ/Development/Documentation/INDEX.md)
- **License**: See [LICENSE](./LICENSE)

---

**Last Updated**: October 2025  
**Version**: 0.1.0  
**Status**: Active Development
