# C# Code Migration to PrismQ Structure

## Overview

This document outlines the C# code migration to the PrismQ structure, adapting the Python migration approach to C# conventions and project structure.

## Migration Approach

Unlike Python's file-based module system, C# uses projects (`.csproj`) and assemblies. Therefore, the migration strategy differs:

### Python vs C# Structure

**Python Approach:**
- Move `.py` files to new directories
- Update imports
- Create `__init__.py` files

**C# Approach:**
- Create new projects under PrismQ directories
- Use project references
- Update namespaces gradually
- Maintain solution structure

## Project Mapping

### Current Structure → PrismQ Structure

| Current Project/Component | New PrismQ Location | Notes |
|--------------------------|---------------------|-------|
| `StoryGenerator.Core` | Split into multiple | Core utilities → Shared, Domain logic → specific subprojects |
| `StoryGenerator.Generators/IdeaGenerator` | `PrismQ.IdeaScraper` | Idea generation |
| `StoryGenerator.Generators/TitleGenerator` | `PrismQ.StoryTitleProcessor` | Title generation |
| `StoryGenerator.Generators/TopicGenerator` | `PrismQ.IdeaScraper` | Topic clustering |
| `StoryGenerator.Generators/ScriptGenerator` | `PrismQ.StoryGenerator` | Script development |
| `StoryGenerator.Generators/VoiceGenerator` | `PrismQ.VoiceOverGenerator` | Voice generation |
| `StoryGenerator.Generators/SubtitleGenerator` | `PrismQ.SubtitleGenerator` | Subtitle generation |
| `StoryGenerator.Generators/SceneBeatsGenerator` | `PrismQ.SceneDescriptions` | Scene planning |
| `StoryGenerator.Generators/VideoSynthesizer` | `PrismQ.VideoGenerator` | Video generation |
| `StoryGenerator.Pipeline` | Keep or distribute | Pipeline orchestration |
| `StoryGenerator.Providers` | `PrismQ.Shared` | Provider interfaces and implementations |
| `StoryGenerator.Data` | `PrismQ.Shared` | Data access layer |
| Models, Interfaces, Utils | `PrismQ.Shared` | Shared components |

## Implementation Phases

### Phase 1: Structure and Documentation ✅
- [x] Create PrismQ directory structure
- [x] Create C# PrismQ README
- [x] Document migration strategy

### Phase 2: Shared Components (Next)
- [ ] Create `PrismQ.Shared.Core` project
- [ ] Create `PrismQ.Shared.Models` project
- [ ] Create `PrismQ.Shared.Interfaces` project
- [ ] Move core models and interfaces

### Phase 3: Domain Projects
- [ ] Create domain-specific projects in subproject folders
- [ ] Move generator classes to appropriate projects
- [ ] Update namespaces

### Phase 4: Integration
- [ ] Update solution file
- [ ] Update project references
- [ ] Verify builds
- [ ] Update examples

### Phase 5: Testing
- [ ] Run all tests
- [ ] Fix any broken references
- [ ] Update test projects if needed

## Namespace Migration

### Before
```csharp
namespace StoryGenerator.Core.Models;
namespace StoryGenerator.Generators;
namespace StoryGenerator.Providers;
```

### After
```csharp
namespace PrismQ.Shared.Models;
namespace PrismQ.IdeaScraper.Generators;
namespace PrismQ.Shared.Providers;
```

## Project Reference Pattern

New projects should reference Shared components:

```xml
<ItemGroup>
  <ProjectReference Include="..\Shared\PrismQ.Shared.Core\PrismQ.Shared.Core.csproj" />
  <ProjectReference Include="..\Shared\PrismQ.Shared.Models\PrismQ.Shared.Models.csproj" />
</ItemGroup>
```

## Backward Compatibility

During transition:

1. **Keep Original Projects**: Don't delete original projects immediately
2. **Use Type Forwarding**: Forward types from old to new assemblies
3. **Gradual Migration**: Migrate one subproject at a time
4. **Test Frequently**: Ensure builds and tests pass after each change

### Type Forwarding Example

In old assembly:
```csharp
[assembly: TypeForwardedTo(typeof(PrismQ.Shared.Models.StoryIdea))]
```

This allows existing code to continue using old namespace while types live in new assembly.

## Benefits of C# PrismQ Structure

1. **Clear Boundaries**: Each project has distinct responsibilities
2. **Independent Versioning**: Can version components separately
3. **NuGet Packages**: Can publish subprojects as NuGet packages
4. **Dependency Management**: Clear project dependencies
5. **Parallel Development**: Teams can work on different subprojects
6. **Testing**: Can test subprojects in isolation

## Notes

### C#-Specific Considerations

- **Solution File**: Will need to add new projects to `StoryGenerator.sln`
- **Build Order**: Project dependencies determine build order
- **Assembly Names**: Follow pattern `PrismQ.{Subproject}.{Component}`
- **NuGet Packages**: Shared packages needed by multiple subprojects
- **Target Framework**: Use .NET 9.0 to match existing projects

### Incremental Approach

The C# migration is more complex than Python due to:
- Compiled nature (need working builds)
- Project references and dependencies
- Namespace changes affect all consumers
- Solution file maintenance

Therefore, we take an **incremental, tested approach**:
1. Create new structure alongside existing
2. Move components gradually
3. Maintain backward compatibility
4. Test after each change
5. Eventually deprecate old structure

## Current Status

- ✅ Phase 1 Complete: Structure and documentation created
- 🔄 Phase 2 In Progress: Ready to create Shared projects
- ⏳ Phase 3-5: Pending

## Next Steps

1. Create `PrismQ.Shared.Core` project with core utilities
2. Create `PrismQ.Shared.Models` project with data models
3. Create `PrismQ.Shared.Interfaces` project with interfaces
4. Update solution file to include new projects
5. Begin moving code to new projects

## Questions?

See the main PrismQ documentation or create an issue for questions about the C# migration.
