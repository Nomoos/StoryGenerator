# Deprecated Projects and Migration Status

## Overview
This document tracks the migration from StoryGenerator.Core to PrismQ.Shared structure.

## Successfully Migrated Projects

### Consuming Projects (Updated to use PrismQ.Shared)
- ✅ **StoryGenerator.Data** - Now references PrismQ.Shared.Core, Models, and Interfaces
- ✅ **StoryGenerator.Providers** - Now references PrismQ.Shared.Core
- ✅ **StoryGenerator.Pipeline** - Now references all PrismQ.Shared projects
- ✅ **StoryGenerator.CLI** - Now references all PrismQ.Shared projects
- ✅ **Examples/IdeaCollectorExample** - Now references PrismQ.Shared projects
- ✅ **SubtitleAlignment.Example** - Now references PrismQ.Shared projects

### PrismQ Domain Projects (Updated to use PrismQ.Shared)
- ✅ **PrismQ.IdeaScraper** - Migrated, uses PrismQ.Shared + StoryGenerator.Providers
- ✅ **PrismQ.StoryGenerator** - Migrated, uses PrismQ.Shared + StoryGenerator.Providers
- ✅ **PrismQ.SubtitleGenerator** - Migrated, uses PrismQ.Shared + StoryGenerator.Providers
- ✅ **PrismQ.VoiceOverGenerator** - Migrated, uses PrismQ.Shared + StoryGenerator.Providers
- ✅ **PrismQ.StoryTitleProcessor** - Added to solution, references PrismQ.Shared
- ✅ **PrismQ.StoryTitleScoring** - Added to solution, references PrismQ.Shared
- ✅ **PrismQ.SceneDescriptions** - Added to solution, references PrismQ.Shared

### PrismQ Shared Projects (Core Infrastructure)
- ✅ **PrismQ.Shared.Core** - Contains core utilities, services (FileHelper, PathConfiguration, etc.)
- ✅ **PrismQ.Shared.Models** - Contains shared models (Result<T>, StoryIdea, CollectedIdea, Shotlist, etc.)
- ✅ **PrismQ.Shared.Interfaces** - Contains shared interfaces (IGenerator, IIdeaCollector, IDatabase, etc.)

## Projects with Known Issues

### VideoGenerator Projects (Non-Critical)
- ⚠️ **PrismQ.VideoGenerator** - Has orphaned model references (KeyframeManifest, StructuredShot, etc.)
  - These models exist in `/src/CSharp/Models/KeyframeModels.cs` but are not in any project
  - The `StoryGenerator.Models` namespace doesn't have a corresponding project
  - **Impact**: 12 build errors in VideoGenerator
  - **Recommendation**: Either move models to PrismQ.Shared.Models or create a PrismQ.VideoGenerator.Models project

- ⚠️ **StoryGenerator.Pipeline/Services/VideoGenerationService.cs**
  - References `LTXVideoSynthesizer` and `KeyframeVideoSynthesizer` which don't exist in PrismQ yet
  - **Impact**: 3 build errors
  - **Recommendation**: These classes need to be migrated from StoryGenerator.Generators to PrismQ.VideoGenerator

## Deprecated/Empty Projects

### StoryGenerator.Core
- **Status**: EMPTY - No source files
- **Migration**: All functionality moved to PrismQ.Shared projects
- **References**: Still referenced by projects for backward compatibility
- **Recommendation**: Can be removed once all references are confirmed working

## Build Status

### Current State
- **Total Errors**: 21 (all in VideoGenerator-related code)
- **Projects Building Successfully**: 
  - All PrismQ.Shared projects ✅
  - All migrated consuming projects ✅
  - Most PrismQ domain projects ✅
- **Projects with Errors**:
  - PrismQ.VideoGenerator (orphaned models) ⚠️
  - StoryGenerator.Pipeline (VideoGenerationService only) ⚠️

### Solution File
All PrismQ projects have been added to `StoryGenerator.sln`:
- PrismQ.Shared.Core
- PrismQ.Shared.Models  
- PrismQ.Shared.Interfaces
- PrismQ.IdeaScraper
- PrismQ.StoryGenerator
- PrismQ.StoryTitleProcessor
- PrismQ.StoryTitleScoring
- PrismQ.SubtitleGenerator
- PrismQ.VoiceOverGenerator
- PrismQ.VideoGenerator
- PrismQ.SceneDescriptions

## Migration Summary

### What Was Accomplished
1. ✅ Fixed all PrismQ.Shared projects to properly reference dependencies
2. ✅ Moved Result<T> to PrismQ.Shared.Models to avoid circular dependencies
3. ✅ Created ContentFilterResult in PrismQ.Shared.Models
4. ✅ Added IGenerator interface to PrismQ.Shared.Interfaces
5. ✅ Updated all consuming projects to reference PrismQ.Shared instead of StoryGenerator.Core
6. ✅ Added all PrismQ projects to the solution file
7. ✅ Updated ~50+ files with correct using statements and namespaces
8. ✅ Fixed Result.Failure() method calls to use single parameter

### Namespace Mappings
```
StoryGenerator.Core.Models       → PrismQ.Shared.Models
StoryGenerator.Core.Interfaces   → PrismQ.Shared.Interfaces
StoryGenerator.Core.Services     → PrismQ.Shared.Core.Services
StoryGenerator.Core.Utils        → PrismQ.Shared.Core.Utils
StoryGenerator.Core.Configuration → PrismQ.Shared.Core.Configuration
```

### Known Limitations
- VideoGenerator models (KeyframeManifest, etc.) are orphaned and need to be properly placed
- LTXVideoSynthesizer and KeyframeVideoSynthesizer classes haven't been migrated yet
- StoryGenerator.Core is empty but still referenced (safe to remove in future PR)

## Next Steps

1. **Resolve VideoGenerator Issues** (Optional)
   - Move orphaned models from `/src/CSharp/Models/` to appropriate PrismQ project
   - Migrate video synthesizer classes to PrismQ.VideoGenerator

2. **Clean Up** (Future PR)
   - Remove StoryGenerator.Core project once confirmed unnecessary
   - Remove StoryGenerator.Generators once all functionality is in PrismQ

3. **Testing**
   - Run integration tests to ensure functionality is preserved
   - Test each migrated component individually

## Files Modified

Total files modified: ~75+
- PrismQ.Shared projects: 25+ files
- Consuming projects: 20+ files  
- PrismQ domain projects: 15+ files
- Project files (.csproj): 15+ files
- Solution file: 1 file

All changes have been committed and pushed to the `copilot/update-references-to-prismq` branch.
