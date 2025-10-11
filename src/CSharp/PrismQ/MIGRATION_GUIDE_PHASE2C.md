# C# Code Migration Guide - Phase 2c

## Current Status

✅ **Complete:**
- Phase 1: PrismQ directory structure created
- Phase 2a: Shared projects created (Core, Models, Interfaces)
- Phase 2b: Domain project files (.csproj) created for all subprojects

⏳ **Next Steps:**
- Phase 2c: Migrate actual C# code files from StoryGenerator.Generators

## Phase 2c: Code Migration Steps

### Step 1: IdeaScraper Migration

**Files to Move:**
- `src/CSharp/StoryGenerator.Generators/IdeaGenerator.cs` → `src/CSharp/PrismQ/IdeaScraper/`
- `src/CSharp/StoryGenerator.Generators/IIdeaGenerator.cs` → `src/CSharp/PrismQ/IdeaScraper/`

**Namespace Update:**
```csharp
// Before
namespace StoryGenerator.Generators;

// After
namespace PrismQ.IdeaScraper;
```

**Dependencies to Update:**
- Change `using StoryGenerator.Core.Models;` → `using PrismQ.Shared.Models;`
- Change `using StoryGenerator.Core.Services;` → `using PrismQ.Shared.Core.Services;`

### Step 2: StoryGenerator Migration

**Files to Move:**
- `src/CSharp/StoryGenerator.Generators/ScriptGenerator.cs` → `src/CSharp/PrismQ/StoryGenerator/`
- `src/CSharp/StoryGenerator.Generators/IScriptGenerator.cs` → `src/CSharp/PrismQ/StoryGenerator/`
- `src/CSharp/StoryGenerator.Generators/RevisionGenerator.cs` → `src/CSharp/PrismQ/StoryGenerator/`
- `src/CSharp/StoryGenerator.Generators/IRevisionGenerator.cs` → `src/CSharp/PrismQ/StoryGenerator/`
- `src/CSharp/StoryGenerator.Generators/EnhancementGenerator.cs` → `src/CSharp/PrismQ/StoryGenerator/`
- `src/CSharp/StoryGenerator.Generators/IEnhancementGenerator.cs` → `src/CSharp/PrismQ/StoryGenerator/`

**Namespace Update:**
```csharp
// Before
namespace StoryGenerator.Generators;

// After
namespace PrismQ.StoryGenerator;
```

### Step 3: VoiceOverGenerator Migration

**Files to Move:**
- `src/CSharp/StoryGenerator.Generators/VoiceGenerator.cs` → `src/CSharp/PrismQ/VoiceOverGenerator/`
- `src/CSharp/StoryGenerator.Generators/IVoiceGenerator.cs` → `src/CSharp/PrismQ/VoiceOverGenerator/`

**Namespace Update:**
```csharp
// Before
namespace StoryGenerator.Generators;

// After
namespace PrismQ.VoiceOverGenerator;
```

### Step 4: SubtitleGenerator Migration

**Files to Move:**
- `src/CSharp/StoryGenerator.Generators/SubtitleGenerator.cs` → `src/CSharp/PrismQ/SubtitleGenerator/`
- `src/CSharp/StoryGenerator.Generators/ISubtitleGenerator.cs` → `src/CSharp/PrismQ/SubtitleGenerator/`

**Namespace Update:**
```csharp
// Before
namespace StoryGenerator.Generators;

// After
namespace PrismQ.SubtitleGenerator;
```

### Step 5: VideoGenerator Migration

**Files to Move:**
- `src/CSharp/StoryGenerator.Generators/KeyframeVideoSynthesizer.cs` → `src/CSharp/PrismQ/VideoGenerator/`
- `src/CSharp/StoryGenerator.Generators/LTXVideoSynthesizer.cs` → `src/CSharp/PrismQ/VideoGenerator/`
- `src/CSharp/StoryGenerator.Generators/IVideoSynthesizer.cs` → `src/CSharp/PrismQ/VideoGenerator/`
- `src/CSharp/StoryGenerator.Generators/VideoSynthesisBase.cs` → `src/CSharp/PrismQ/VideoGenerator/`

**Namespace Update:**
```csharp
// Before
namespace StoryGenerator.Generators;

// After
namespace PrismQ.VideoGenerator;
```

### Step 6: SceneDescriptions Migration

**Files from loose Generators folder:**
- `src/CSharp/Generators/SceneBeatsGenerator.cs` → `src/CSharp/PrismQ/SceneDescriptions/`
- `src/CSharp/Generators/SimpleSceneBeatsGenerator.cs` → `src/CSharp/PrismQ/SceneDescriptions/`

**Namespace Update:**
```csharp
// Update namespace to
namespace PrismQ.SceneDescriptions;
```

### Step 7: Update Solution File

Add the new PrismQ projects to `StoryGenerator.sln`:

```bash
dotnet sln StoryGenerator.sln add src/CSharp/PrismQ/IdeaScraper/PrismQ.IdeaScraper.csproj
dotnet sln StoryGenerator.sln add src/CSharp/PrismQ/StoryTitleProcessor/PrismQ.StoryTitleProcessor.csproj
dotnet sln StoryGenerator.sln add src/CSharp/PrismQ/StoryTitleScoring/PrismQ.StoryTitleScoring.csproj
dotnet sln StoryGenerator.sln add src/CSharp/PrismQ/StoryGenerator/PrismQ.StoryGenerator.csproj
dotnet sln StoryGenerator.sln add src/CSharp/PrismQ/VoiceOverGenerator/PrismQ.VoiceOverGenerator.csproj
dotnet sln StoryGenerator.sln add src/CSharp/PrismQ/SceneDescriptions/PrismQ.SceneDescriptions.csproj
dotnet sln StoryGenerator.sln add src/CSharp/PrismQ/SubtitleGenerator/PrismQ.SubtitleGenerator.csproj
dotnet sln StoryGenerator.sln add src/CSharp/PrismQ/VideoGenerator/PrismQ.VideoGenerator.csproj
```

### Step 8: Update Project References

Update projects that reference `StoryGenerator.Generators` to reference the new PrismQ projects:

**Examples:**
- Update `Examples/` projects
- Update `Tests/` projects
- Update `StoryGenerator.CLI/` project

### Step 9: Add Missing Dependencies

The PrismQ projects will need additional dependencies beyond Shared projects. Update each .csproj as needed:

```xml
<ItemGroup>
  <!-- For OpenAI access -->
  <PackageReference Include="Azure.AI.OpenAI" Version="..." />
  
  <!-- For logging -->
  <PackageReference Include="Microsoft.Extensions.Logging.Abstractions" Version="..." />
  
  <!-- Add other packages as needed -->
</ItemGroup>
```

### Step 10: Build and Test

```bash
# Build solution
dotnet build StoryGenerator.sln

# Run tests
dotnet test StoryGenerator.sln

# Fix any errors
```

### Step 11: Backward Compatibility (Optional)

To maintain backward compatibility temporarily, you can use **Type Forwarding**:

In the old `StoryGenerator.Generators` assembly, add:

```csharp
using System.Runtime.CompilerServices;

[assembly: TypeForwardedTo(typeof(PrismQ.IdeaScraper.IdeaGenerator))]
[assembly: TypeForwardedTo(typeof(PrismQ.StoryGenerator.ScriptGenerator))]
// ... etc for all moved types
```

This allows existing code to continue using old namespaces while types actually live in new assemblies.

## Common Issues and Solutions

### Issue 1: Missing Dependencies

**Error:** `The type or namespace name 'X' could not be found`

**Solution:** 
- Add missing NuGet packages to the new PrismQ project
- Add project references to required PrismQ.Shared projects

### Issue 2: Circular Dependencies

**Error:** Build fails due to circular references

**Solution:**
- Extract shared interfaces to PrismQ.Shared.Interfaces
- Ensure dependencies flow in one direction only

### Issue 3: Build Order

**Error:** Projects build in wrong order

**Solution:**
- Ensure project references are correct
- MSBuild automatically determines build order from references

## Testing Checklist

After migration:

- [ ] Solution builds without errors
- [ ] All existing tests pass
- [ ] Examples compile and run
- [ ] CLI application works
- [ ] No warnings about deprecated namespaces (if type forwarding used)

## Rollback Plan

If migration fails:
1. The old `StoryGenerator.Generators` project still exists
2. Simply remove new PrismQ projects from solution
3. Revert any changed references back to old project
4. Old code continues to work

## Next Phase

After Phase 2c is complete:
- **Phase 3**: Refactor StoryGenerator.Core into Shared components
- **Phase 4**: Update all project references across the solution
- **Phase 5**: Remove old projects and clean up

## Questions?

See:
- `/docs/migration/PRISMQ_MIGRATION.md` for overall migration guide
- `/src/CSharp/PrismQ/README.md` for C# PrismQ structure
- Create an issue for specific migration questions
