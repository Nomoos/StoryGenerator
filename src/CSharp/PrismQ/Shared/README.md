# PrismQ.Shared

Common C# components used across all PrismQ subprojects.

## Planned Projects

- `PrismQ.Shared.Core` - Core utilities, helpers, extensions
- `PrismQ.Shared.Models` - Shared data models and DTOs
- `PrismQ.Shared.Interfaces` - Interface definitions
- `PrismQ.Shared.Providers` - Provider implementations
- `PrismQ.Shared.Data` - Data access layer

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

⏳ Pending - Structure created, awaiting implementation
