# PrismQ Migration Guide

This guide helps you migrate code from the old `core/` structure to the new `PrismQ/` modular architecture.

## Overview

The repository has been reorganized into independent subprojects under the `PrismQ/` namespace. This provides:
- Better separation of concerns
- Easier maintenance and testing
- Foundation for future modular packaging
- Clear ownership of functionality

## Quick Reference

### Module Mapping

| Old Location | New Location | Purpose |
|-------------|--------------|---------|
| `core/errors.py` | `PrismQ/Shared/errors.py` | Custom exceptions |
| `core/config.py` | `PrismQ/Shared/config.py` | Configuration management |
| `core/models.py` | `PrismQ/Shared/models.py` | Data models |
| `core/logging.py` | `PrismQ/Shared/logging.py` | Logging utilities |
| `core/cache.py` | `PrismQ/Shared/cache.py` | Caching utilities |
| `core/retry.py` | `PrismQ/Shared/retry.py` | Retry logic |
| `core/validation.py` | `PrismQ/Shared/validation.py` | Validation utilities |
| `core/database.py` | `PrismQ/Shared/database.py` | Database utilities |
| `core/interfaces/` | `PrismQ/Shared/interfaces/` | Provider interfaces |
| `core/pipeline/idea_generation.py` | `PrismQ/IdeaScraper/idea_generation.py` | Idea generation |
| `core/pipeline/topic_clustering.py` | `PrismQ/IdeaScraper/topic_clustering.py` | Topic clustering |
| `core/pipeline/title_generation.py` | `PrismQ/StoryTitleProcessor/title_generation.py` | Title generation |
| `core/pipeline/title_scoring.py` | `PrismQ/StoryTitleScoring/title_scoring.py` | Title scoring |
| `core/pipeline/top_selection.py` | `PrismQ/StoryTitleScoring/top_selection.py` | Top title selection |
| `core/pipeline/voice_recommendation.py` | `PrismQ/VoiceOverGenerator/voice_recommendation.py` | Voice recommendation |
| `core/pipeline/voice_cloning.py` | `PrismQ/VoiceOverGenerator/voice_cloning.py` | Voice cloning |
| `core/script_development.py` | `PrismQ/StoryGenerator/script_development.py` | Script development |
| `core/pipeline/style_consistency.py` | `PrismQ/StoryGenerator/style_consistency.py` | Style checking |
| `core/audio_production.py` | `PrismQ/VoiceOverGenerator/audio_production.py` | Audio production |
| `core/scene_planning.py` | `PrismQ/SceneDescriptions/scene_planning.py` | Scene planning |

## Migration Steps

### Step 1: Update Imports

**Old Code:**
```python
from core.errors import APIError
from core.pipeline.idea_generation import IdeaAdapter
from core.pipeline.title_scoring import TitleScorer
```

**New Code:**
```python
from PrismQ.Shared.errors import APIError
from PrismQ.IdeaScraper.idea_generation import IdeaAdapter
from PrismQ.StoryTitleScoring.title_scoring import TitleScorer
```

### Step 2: Update Interface Imports

**Old Code:**
```python
from core.interfaces.llm_provider import ILLMProvider
from core.interfaces.platform_provider import PlatformType
```

**New Code:**
```python
from PrismQ.Shared.interfaces.llm_provider import ILLMProvider
from PrismQ.Shared.interfaces.platform_provider import PlatformType
```

### Step 3: Run Tests

After updating imports, run your tests to ensure everything works:

```bash
python -m pytest tests/
```

### Step 4: Update Documentation

Update any documentation that references the old structure.

## Backward Compatibility

During the transition period, the old `core/` imports continue to work through a compatibility layer:

```python
# This still works (redirects to PrismQ automatically)
from core.errors import APIError

# But new code should use:
from PrismQ.Shared.errors import APIError
```

The compatibility layer will be removed in a future release once all code has been migrated.

## Common Patterns

### Pattern 1: Shared Utilities

Anything that multiple subprojects need goes in `PrismQ/Shared/`:
- Error classes
- Configuration
- Logging
- Data models
- Interfaces

### Pattern 2: Subproject-Specific Code

Code specific to a pipeline stage goes in its subproject:
- Idea generation → `PrismQ/IdeaScraper/`
- Title processing → `PrismQ/StoryTitleProcessor/`
- Script development → `PrismQ/StoryGenerator/`
- Audio production → `PrismQ/VoiceOverGenerator/`

### Pattern 3: Cross-Subproject Dependencies

When one subproject needs another, import directly:

```python
# In PrismQ/StoryGenerator/script_development.py
from PrismQ.Shared.interfaces.llm_provider import ILLMProvider
from PrismQ.Shared.errors import ValidationError
```

## Benefits

After migration, you'll get:

1. **Clearer Structure**: Easy to find where functionality lives
2. **Better Testing**: Test subprojects in isolation
3. **Easier Maintenance**: Changes don't ripple across the codebase
4. **Future Packaging**: Can package subprojects separately if needed
5. **Better Documentation**: Each subproject can have its own docs

## Need Help?

- Check `PrismQ/README.md` for the full structure
- Look at migrated test files in `tests/pipeline/` for examples
- Create an issue if you encounter problems

## Timeline

- ✅ **Phase 1**: Python code migration (complete)
- ✅ **Phase 2**: C# code migration (structure and shared projects complete)
  - ✅ Structure created (19 subproject directories)
  - ✅ Documentation complete
  - ✅ Shared projects created (Core, Models, Interfaces)
- ✅ **Phase 3**: Update all tests to use PrismQ imports (complete - 35 files updated)
- ✅ **Phase 4**: Remove Python backward compatibility layer (complete - 24 files removed)
- ✅ **Phase 5**: Remove deprecated C# projects (complete - 2 projects removed)

**Status**: 🎉 All phases complete! Migration finished and all deprecated projects cleaned up.
