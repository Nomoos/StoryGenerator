# PrismQ.Shared

Common C# components used across all PrismQ subprojects.

## Planned Projects

- `PrismQ.Shared.Core` - Core utilities, helpers, extensions ✅ CREATED
- `PrismQ.Shared.Models` - Shared data models and DTOs ✅ CREATED
- `PrismQ.Shared.Interfaces` - Interface definitions ✅ CREATED
- `PrismQ.Shared.Providers` - Provider implementations (Pending)
- `PrismQ.Shared.Data` - Data access layer (Pending)

## Created Projects

### PrismQ.Shared.Core ✅
**Status**: Created and building successfully

**Purpose**: Core utilities and base classes

**Contents**:
- `Result<T>` - Result type for operation outcomes

**Dependencies**:
- Microsoft.Extensions.Logging.Abstractions

### PrismQ.Shared.Models ✅
**Status**: Created and building successfully

**Purpose**: Shared data models and DTOs

**Contents**:
- `AudienceSegment` - Demographic information record

**Dependencies**:
- System.Text.Json

### PrismQ.Shared.Interfaces ✅
**Status**: Created and building successfully

**Purpose**: Interface definitions for providers and services

**Contents**:
- `ILLMProvider` - LLM provider interface

**Dependencies**:
- PrismQ.Shared.Models

## Components to Migrate

From various projects:
- `StoryGenerator.Core` → Split into Core, Models, Interfaces
- `StoryGenerator.Providers` → Shared.Providers
- `StoryGenerator.Data` → Shared.Data
- Models, Interfaces, Utils from all projects

## Namespace Pattern

```csharp
namespace PrismQ.Shared.Core { }
namespace PrismQ.Shared.Models { }
namespace PrismQ.Shared.Interfaces { }
namespace PrismQ.Shared.Providers { }
namespace PrismQ.Shared.Data { }
```

## Status

✅ **Phase 2a Complete** - Initial Shared projects created and building

**Next Steps**:
- Create domain-specific projects (IdeaScraper, StoryGenerator, etc.)
- Migrate code from existing projects
- Update namespaces
