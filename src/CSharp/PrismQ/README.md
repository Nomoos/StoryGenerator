# PrismQ C# Projects

This directory contains the C# implementation of the PrismQ modular architecture, mirroring the Python structure.

## Structure

Each subproject directory contains C# projects (`.csproj`) organized by functionality:

### Active Subprojects

- **Shared/** - Common utilities, models, interfaces, and core functionality
  - `PrismQ.Shared.Core` - Core utilities and base classes
  - `PrismQ.Shared.Models` - Data models and DTOs
  - `PrismQ.Shared.Interfaces` - Interface definitions

- **IdeaScraper/** - Idea generation and topic clustering
  - Related to `StoryGenerator.Generators` (IdeaGenerator, TopicGenerator, TitleGenerator)

- **StoryTitleProcessor/** - Title generation and processing
  - Related to `StoryGenerator.Generators` (TitleGenerator)

- **StoryTitleScoring/** - Title evaluation and scoring

- **StoryGenerator/** - Script generation and development
  - Related to `StoryGenerator.Generators` (ScriptGenerator, RevisionGenerator, EnhancementGenerator)

- **VoiceOverGenerator/** - Voice generation and audio production
  - Related to `StoryGenerator.Generators` (VoiceGenerator)

- **SceneDescriptions/** - Scene planning and beat generation
  - Related to `StoryGenerator.Generators` (SceneBeatsGenerator)

- **SubtitleGenerator/** - Subtitle generation
  - Related to `StoryGenerator.Generators` (SubtitleGenerator)

- **VideoGenerator/** - Video synthesis
  - Related to `StoryGenerator.Generators` (KeyframeVideoSynthesizer, LTXVideoSynthesizer)

### Placeholder Subprojects

The following directories are placeholders for future C# implementation:
- StoryTitleFineTune
- StoryDescriptionScoring
- StoryDescriptionFineTune
- FinalizeText
- FinalizeAudio
- FinalizeVideo
- FrameInterpolation
- SparseKeyFramesGenerator
- DescriptionGenerator
- TagsGenerator

## Migration Strategy

### Phase 1: Structure Creation ✅ COMPLETE
- [x] Create PrismQ directory structure (19 subprojects)
- [x] Create README and documentation
- [x] Document C# migration approach
- [x] Create subproject READMEs for active components

### Phase 2a: Shared Projects Creation ✅ COMPLETE
- [x] Create PrismQ.Shared.Core project
- [x] Create PrismQ.Shared.Models project
- [x] Create PrismQ.Shared.Interfaces project
- [x] Add projects to solution
- [x] Verify builds successfully

### Phase 2b: Project Organization (Next Steps)
- Move existing C# projects into appropriate PrismQ subprojects
- Update namespaces to use PrismQ prefix
- Update project references

### Phase 3: Refactor Core Projects
- Split StoryGenerator.Core into Shared components
- Reorganize models and interfaces
- Update dependencies

### Phase 4: Update References
- Update solution file
- Update all project references
- Ensure builds work correctly

## Namespace Convention

All C# projects under PrismQ should use the namespace pattern:
```csharp
namespace PrismQ.{Subproject}.{Component}
{
    // Example: namespace PrismQ.IdeaScraper.Generators
    // Example: namespace PrismQ.Shared.Models
}
```

## Backward Compatibility

During migration, we maintain backward compatibility by:
1. Keeping original projects in place initially
2. Creating project references instead of moving immediately
3. Gradual namespace migration
4. Type forwarding where needed

## Related Documentation

- See `/PrismQ/README.md` for Python structure
- See `/docs/migration/PRISMQ_MIGRATION.md` for migration guide
- See `/PRISMQ_IMPLEMENTATION_SUMMARY.md` for Python implementation details
