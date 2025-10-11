# Migration Documentation

This directory contains all documentation related to the PrismQ migration - the transition from the legacy structure to the modular PrismQ architecture.

## 📋 Migration Overview

The PrismQ migration reorganized both Python and C# code into a modular structure with clear separation of concerns.

### Migration Guides

#### Main Guides
- [PrismQ Migration Guide](PRISMQ_MIGRATION.md) - Main migration guide for Python code
- [C# Migration Guide](CSHARP_MIGRATION.md) - C# specific migration strategy
- [Migration Guide (General)](MIGRATION_GUIDE.md) - Active development guide for C# implementation
- [Phase 2C Migration Guide](MIGRATION_GUIDE_PHASE2C.md) - C# code migration from StoryGenerator.Generators

### Implementation Phases

#### Python Migration
- [Phase 2 Implementation](PHASE2_IMPLEMENTATION.md) - Python module migration details
- [Phase 3 Implementation](PHASE3_IMPLEMENTATION.md) - Python migration completion
- [Phase 4 Implementation](PHASE4_IMPLEMENTATION.md) - Final Python cleanup
- [Phase 6 Folder Migration](PHASE6_FOLDER_MIGRATION.md) - Move providers/ and pipeline/ to PrismQ/

#### C# Migration
- [Phase 2 Testing Summary](PHASE2_TESTING_SUMMARY.md) - Phase 2 & testing implementation summary
- [Phase 5 Cleanup](PHASE5_CLEANUP.md) - Remove deprecated C# projects (StoryGenerator.Core, StoryGenerator.Generators)

#### Documentation Migration
- [Documentation Migration](DOCUMENTATION_MIGRATION.md) - Documentation reorganization to PrismQ structure

### Status & Summary

- [PrismQ Migration Status](PRISMQ_MIGRATION_STATUS.md) - Overall migration status report
- [PrismQ Implementation Summary](PRISMQ_IMPLEMENTATION_SUMMARY.md) - Complete implementation summary

## 🎯 Migration Status

### Completed ✅
- Python modules migrated to PrismQ structure
- Python providers migrated to PrismQ.Providers
- Python pipeline migrated to PrismQ.Pipeline
- C# Shared projects created (PrismQ.Shared.Core, Models, Interfaces)
- C# domain projects created and migrated
- Deprecated projects removed (StoryGenerator.Core, StoryGenerator.Generators)
- Documentation reorganized
- All imports updated to use PrismQ namespace
- All tests passing (341 tests)
- Build succeeds with 0 errors

### Current Structure

```
PrismQ/
├── Shared/                    # Shared components
│   ├── PrismQ.Shared.Core/   # Core utilities and services (C#)
│   ├── PrismQ.Shared.Models/ # Shared models (C#)
│   ├── PrismQ.Shared.Interfaces/ # Shared interfaces (C#)
│   ├── interfaces/           # Provider interfaces (Python)
│   ├── cache.py             # Caching utilities
│   ├── config.py            # Configuration management
│   ├── database.py          # Database utilities
│   ├── errors.py            # Custom exceptions
│   ├── logging.py           # Logging utilities
│   └── models.py            # Shared data models
├── IdeaScraper/              # Idea generation
├── StoryGenerator/           # Script development
├── StoryTitleProcessor/      # Title generation
├── StoryTitleScoring/        # Title scoring
├── VoiceOverGenerator/       # Voice generation
├── SubtitleGenerator/        # Subtitle generation
├── VideoGenerator/           # Video generation
├── SceneDescriptions/        # Scene planning
├── Providers/                # External service implementations
│   ├── openai_provider.py   # OpenAI LLM provider
│   ├── mock_provider.py     # Mock provider for testing
│   ├── youtube_provider.py  # YouTube platform provider
│   └── ...                  # Other platform providers
├── Pipeline/                 # Pipeline orchestration
│   ├── orchestration/       # Step orchestration logic
│   └── scripts/             # Batch execution scripts
└── Tools/                    # Video publishing and quality tools
    ├── MultiPlatformPublisher.py  # Multi-platform distribution
    ├── VideoQualityChecker.py     # Video quality validation
    └── VideoVariantSelector.py    # Video variant selection
```

## 📚 Related Documentation

- [Main README](../../README.md) - Project overview
- [C# Documentation](../csharp/) - C# specific documentation
- [Implementation Documentation](../implementation/) - Implementation summaries
- [PrismQ README](../../src/CSharp/PrismQ/README.md) - PrismQ structure details

## 🚀 Quick Links

- [Deprecated Projects](../../DEPRECATED_PROJECTS.md) - List of removed/deprecated projects
- [PrismQ Source](../../src/CSharp/PrismQ/) - PrismQ source code
- [Python PrismQ](../../PrismQ/) - Python PrismQ modules
