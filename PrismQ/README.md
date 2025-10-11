# PrismQ - Modular Story Generation Framework

PrismQ is the new modular architecture for the StoryGenerator project, organizing functionality into independent, well-defined subprojects.

## Directory Structure

```
PrismQ/
├─ Shared/                     # Common utilities and interfaces
│  ├─ interfaces/              # Provider interfaces (LLM, Platform, etc.)
│  ├─ cache.py                 # Caching utilities
│  ├─ config.py                # Configuration management
│  ├─ database.py              # Database utilities
│  ├─ errors.py                # Custom exceptions
│  ├─ logging.py               # Logging utilities
│  ├─ models.py                # Shared data models
│  ├─ retry.py                 # Retry logic
│  └─ validation.py            # Validation utilities
│
├─ IdeaScraper/                # Idea scraping and generation
│  ├─ idea_generation.py       # Generate ideas from various sources
│  ├─ topic_clustering.py      # Cluster ideas into topics
│  └─ scripts/                 # Utility scripts
│
├─ StoryTitleProcessor/        # Process ideas into story titles
│  └─ title_generation.py      # Generate title variants
│
├─ StoryTitleScoring/          # Evaluate and score story titles
│  ├─ title_scoring.py         # Score titles for viral potential
│  └─ top_selection.py         # Select top-scoring titles
│
├─ StoryTitleFineTune/         # Fine-tune title generation (placeholder)
│
├─ StoryGenerator/             # Generate stories from ideas
│  ├─ script_development.py    # Script generation and iteration
│  └─ style_consistency.py     # Style checking and consistency
│
├─ StoryDescriptionScoring/    # Evaluate and score descriptions (placeholder)
│
├─ StoryDescriptionFineTune/   # Fine-tune description generation (placeholder)
│
├─ FinalizeText/               # Finalize text output (placeholder)
│
├─ VoiceOverGenerator/         # Generate audio voiceover
│  ├─ audio_production.py      # TTS generation and normalization
│  ├─ voice_cloning.py         # Voice cloning utilities
│  └─ voice_recommendation.py  # Recommend voices for content
│
├─ FinalizeAudio/              # Finalize audio output (placeholder)
│
├─ SubtitleGenerator/          # Generate subtitles (placeholder)
│
├─ SceneDescriptions/          # Build scene descriptions
│  └─ scene_planning.py        # Scene and shot planning
│
├─ SparseKeyFramesGenerator/   # Generate sparse keyframes (placeholder)
│
├─ FrameInterpolation/         # Frame interpolation (placeholder)
│
├─ VideoGenerator/             # Generate video from frames (placeholder)
│
├─ FinalizeVideo/              # Finalize video output (placeholder)
│
├─ DescriptionGenerator/       # Generate metadata descriptions (placeholder)
│
├─ TagsGenerator/              # Generate tags (placeholder)
│
├─ Providers/                  # External service provider implementations
│  ├─ openai_provider.py       # OpenAI LLM provider
│  ├─ mock_provider.py         # Mock provider for testing
│  ├─ youtube_provider.py      # YouTube platform provider
│  ├─ tiktok_provider.py       # TikTok platform provider
│  ├─ instagram_provider.py    # Instagram platform provider
│  ├─ facebook_provider.py     # Facebook platform provider
│  └─ wordpress_provider.py    # WordPress publishing provider
│
└─ Pipeline/                   # Pipeline orchestration and execution
   ├─ orchestration/           # Pipeline step orchestration
   │  ├─ run_step.py           # Step execution logic
   │  └─ story_db.py           # Story database management
   └─ scripts/                 # Pipeline batch scripts
      └─ *.bat                 # Windows batch files for pipeline steps
```

## Import Convention

### For New Code

Always import directly from PrismQ subprojects:

```python
from PrismQ.Shared.errors import APIError
from PrismQ.IdeaScraper.idea_generation import IdeaAdapter, IdeaGenerator
from PrismQ.StoryTitleScoring.title_scoring import TitleScorer
from PrismQ.VoiceOverGenerator.voice_recommendation import VoiceRecommender
from PrismQ.Providers import OpenAIProvider, MockLLMProvider
from PrismQ.Pipeline.orchestration.run_step import StepOrchestrator
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
