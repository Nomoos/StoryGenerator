# PrismQ - Modular Story Generation Framework

PrismQ is a well-organized, namespace-based architecture for the StoryGenerator project, providing clean separation of concerns and modular functionality.

## Namespace Structure

```
src/PrismQ/
├── Core/                      # Core utilities and shared components
│   └── Shared/               # Configuration, logging, database, models
│       ├── interfaces/       # Provider interfaces
│       ├── cache.py         # Caching utilities
│       ├── config.py        # Configuration management
│       ├── database.py      # Database utilities
│       ├── errors.py        # Custom exceptions
│       ├── logging.py       # Logging utilities
│       ├── models.py        # Shared data models
│       ├── retry.py         # Retry logic
│       └── validation.py    # Validation utilities
│
├── Content/                   # Content generation modules
│   ├── IdeaScraper/          # Idea scraping and generation
│   ├── StoryGenerator/       # Story and script development
│   ├── StoryTitleProcessor/  # Title generation
│   ├── StoryTitleScoring/    # Title quality scoring
│   ├── SceneDescriptions/    # Scene planning
│   ├── DescriptionGenerator/ # Metadata descriptions
│   ├── TagsGenerator/        # Tag generation
│   ├── StoryTitleFineTune/   # Title fine-tuning
│   ├── StoryDescriptionFineTune/  # Description fine-tuning
│   └── StoryDescriptionScoring/   # Description scoring
│
├── Media/                     # Media processing modules
│   ├── VoiceOverGenerator/   # Voice synthesis and audio
│   ├── SubtitleGenerator/    # Subtitle generation
│   ├── VideoGenerator/       # Video assembly
│   ├── FrameInterpolation/   # Frame processing
│   ├── SparseKeyFramesGenerator/  # Keyframe generation
│   ├── FinalizeAudio/        # Audio finalization
│   ├── FinalizeVideo/        # Video finalization
│   └── FinalizeText/         # Text finalization
│
├── Platform/                  # Platform integrations
│   ├── Providers/            # External service providers
│   │   ├── openai_provider.py      # OpenAI LLM
│   │   ├── openai_optimized.py     # Optimized OpenAI
│   │   ├── mock_provider.py        # Mock provider
│   │   ├── youtube_provider.py     # YouTube
│   │   ├── tiktok_provider.py      # TikTok
│   │   ├── instagram_provider.py   # Instagram
│   │   ├── facebook_provider.py    # Facebook
│   │   └── wordpress_provider.py   # WordPress
│   └── Pipeline/             # Pipeline orchestration
│       ├── orchestration/    # Step execution
│       └── scripts/          # Batch scripts
│
├── Utilities/                 # Tools and utilities
│   ├── Tools/                # Publishing and quality tools
│   │   ├── MultiPlatformPublisher.py  # Multi-platform distribution
│   │   ├── VideoQualityChecker.py     # Quality validation
│   │   └── VideoVariantSelector.py    # Variant selection
│   └── Scripts/              # Automation scripts
│       ├── pipeline/         # Pipeline scripts
│       ├── scrapers/         # Content scrapers
│       └── ...              # Various utilities
│
└── Documentation/             # Examples and guides
    └── Examples/             # Usage demonstrations
```

## Import Convention

### For New Code

Always import using the full namespace path from src:

```python
from src.PrismQ.Core.Shared.errors import APIError
from src.PrismQ.Core.Shared.config import settings
from src.PrismQ.Content.IdeaScraper.idea_generation import IdeaAdapter, IdeaGenerator
from src.PrismQ.Content.StoryTitleScoring.title_scoring import TitleScorer
from src.PrismQ.Media.VoiceOverGenerator.voice_recommendation import VoiceRecommender
from src.PrismQ.Platform.Providers import OpenAIProvider, MockLLMProvider
from src.PrismQ.Platform.Pipeline.orchestration.run_step import StepOrchestrator
from src.PrismQ.Utilities.Tools import MultiPlatformPublisher, VideoQualityChecker
from src.PrismQ.Utilities.Scripts import reddit_scraper
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
