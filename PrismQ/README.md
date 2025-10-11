# PrismQ - Modular Story Generation Framework

PrismQ is a well-organized, namespace-based architecture for the StoryGenerator project, providing clean separation of concerns and modular functionality.

# PrismQ - Modular Story Generation Framework

PrismQ is a pipeline-based architecture for the StoryGenerator project, organizing functionality by content creation stages from idea to final video.

## Pipeline Structure

```
PrismQ/
├── Pipeline/                  # Sequential Content Creation Pipeline
│   ├── 01_IdeaGeneration/    # Stage 1: Idea Generation
│   │   └── IdeaScraper/      # Idea scraping and generation
│   │       ├── idea_generation.py
│   │       ├── topic_clustering.py
│   │       └── scripts/
│   │
│   ├── 02_TextGeneration/    # Stage 2: Text Content Creation
│   │   ├── StoryGenerator/   # Story and script development
│   │   ├── StoryTitleProcessor/  # Title generation
│   │   ├── StoryTitleScoring/    # Title quality scoring
│   │   ├── StoryTitleFineTune/   # Title fine-tuning
│   │   ├── SceneDescriptions/    # Scene planning
│   │   ├── DescriptionGenerator/ # Metadata descriptions
│   │   ├── TagsGenerator/        # Tag generation
│   │   ├── StoryDescriptionScoring/
│   │   ├── StoryDescriptionFineTune/
│   │   └── FinalizeText/         # Text finalization
│   │
│   ├── 03_AudioGeneration/   # Stage 3: Audio Content Creation
│   │   ├── VoiceOverGenerator/   # Voice synthesis and audio
│   │   ├── SubtitleGenerator/    # Subtitle generation
│   │   └── FinalizeAudio/        # Audio finalization
│   │
│   ├── 04_ImageGeneration/   # Stage 4: Image Content Creation
│   │   └── SparseKeyFramesGenerator/  # Keyframe generation
│   │
│   └── 05_VideoGeneration/   # Stage 5: Video Assembly & Finalization
│       ├── VideoGenerator/   # Video assembly
│       ├── FrameInterpolation/  # Frame processing
│       └── FinalizeVideo/    # Video finalization
│
├── Infrastructure/           # Core Infrastructure
│   ├── Core/                # Shared utilities and configuration
│   │   └── Shared/         # Configuration, logging, database, models
│   │       ├── interfaces/  # Provider interfaces
│   │       ├── cache.py
│   │       ├── config.py
│   │       ├── database.py
│   │       ├── errors.py
│   │       ├── logging.py
│   │       ├── models.py
│   │       ├── retry.py
│   │       └── validation.py
│   │
│   ├── Platform/            # External service integrations
│   │   ├── Providers/      # Service providers
│   │   │   ├── openai_provider.py
│   │   │   ├── youtube_provider.py
│   │   │   ├── tiktok_provider.py
│   │   │   └── ...
│   │   └── Pipeline/       # Pipeline orchestration
│   │       ├── orchestration/
│   │       └── scripts/
│   │
│   └── Utilities/          # Tools, scripts, and automation
│       ├── Tools/          # Publishing and quality tools
│       └── Scripts/        # Automation scripts
│
├── Resources/              # Project Resources
│   ├── Assets/            # Static media assets
│   ├── Data/              # Runtime data and generated content
│   └── Configuration/     # YAML configuration files
│
├── Development/           # Development Resources
│   ├── Tests/            # Test suite
│   ├── Examples/         # Usage examples and demonstrations
│   └── Documentation/    # Project documentation
│
└── Projects/             # Related Projects
    ├── CSharp/          # C# implementation
    ├── Research/        # Research documents
    ├── Issues/          # Issue tracking
    └── Podcasts/        # Podcast content
```

## Import Convention

### Pipeline-Based Imports

Always import using the pipeline stage path:

```python
# Stage 1: Idea Generation
from PrismQ.Pipeline.01_IdeaGeneration.IdeaScraper.idea_generation import IdeaGenerator

# Stage 2: Text Generation
from PrismQ.Pipeline.02_TextGeneration.StoryGenerator.script_development import ScriptGenerator
from PrismQ.Pipeline.02_TextGeneration.StoryTitleScoring.title_scoring import TitleScorer

# Stage 3: Audio Generation
from PrismQ.Pipeline.03_AudioGeneration.VoiceOverGenerator.voice_recommendation import VoiceRecommender

# Stage 4: Image Generation
from PrismQ.Pipeline.04_ImageGeneration.SparseKeyFramesGenerator import KeyFrameGenerator

# Stage 5: Video Generation
from PrismQ.Pipeline.05_VideoGeneration.VideoGenerator import VideoAssembler

# Infrastructure
from PrismQ.Infrastructure.Core.Shared.config import settings
from PrismQ.Infrastructure.Platform.Providers import OpenAIProvider
from PrismQ.Infrastructure.Utilities.Tools import MultiPlatformPublisher
```

### Backward Compatibility

Existing code can continue using the old `core.*` imports, which are automatically redirected:

```python
# Old imports (still work via compatibility layer)
from core.errors import APIError
from core.pipeline.idea_generation import IdeaAdapter
```

However, **all new code should use the PrismQ imports**.

## Design Principles

1. **Separation of Concerns**: Each subproject handles a specific part of the pipeline
2. **Independence**: Subprojects can be developed, tested, and deployed independently
3. **Shared Resources**: Common utilities live in `PrismQ/Shared/`
4. **Clear Interfaces**: Well-defined interfaces in `PrismQ/Shared/interfaces/`
5. **Backward Compatibility**: Old imports continue to work during transition

## Migration Guide

### Moving Code to PrismQ

When adding new functionality:

1. Identify the appropriate subproject (e.g., `VoiceOverGenerator` for audio features)
2. Create your module in that subproject
3. Use `PrismQ.Shared.*` for common utilities
4. Follow the CamelCase naming for subproject directories
5. Use snake_case for Python module files

### Updating Existing Code

To migrate existing code:

1. Update imports from `core.*` to `PrismQ.*`
2. Update any path references if needed
3. Run tests to verify functionality
4. Remove the compatibility layer once all references are updated

## Benefits

- **Modularity**: Easy to understand what each component does
- **Maintainability**: Changes in one subproject don't affect others
- **Scalability**: Can add new subprojects without modifying existing ones
- **Testing**: Can test subprojects in isolation
- **Future Packaging**: Foundation for distributing components as separate packages

## Status

As of the initial migration:
- ✅ Python modules migrated to PrismQ structure
- ✅ Backward compatibility layer created
- ✅ Tests passing with backward compatibility
- ⏳ C# code migration (in progress)
- ⏳ Documentation updates (in progress)
- ⏳ Remove backward compatibility layer (future)

## Questions?

See the main repository documentation or create an issue for questions about the PrismQ architecture.
