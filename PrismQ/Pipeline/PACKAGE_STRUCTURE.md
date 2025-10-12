# Package Structure for Modular Architecture

## Current Monolithic Structure
```
PrismQ/
└── Pipeline/
    ├── 01_IdeaGeneration/
    │   └── IdeaScraper/
    │       ├── idea_generation.py
    │       ├── topic_clustering.py
    │       └── scripts/
    │           └── generate_ideas.py  # ❌ Has cross-imports
    │
    ├── 02_TextGeneration/
    │   ├── StoryGenerator/
    │   ├── StoryTitleProcessor/       # ❌ Imported by Stage 01
    │   ├── StoryTitleScoring/         # ❌ Imported by Stage 01
    │   └── ...
    │
    └── ... (other stages with similar coupling)
```

## Target Modular Structure
```
PrismQ/
├── Infrastructure/
│   └── Core/
│       └── Shared/
│           └── interfaces/
│               ├── pipeline_stage.py      # ✅ Base interfaces
│               ├── stage_contracts.py     # ✅ I/O contracts
│               ├── llm_provider.py        # ✅ Provider interfaces
│               └── __init__.py            # ✅ Exports all
│
└── Pipeline/
    ├── 01_IdeaGeneration/
    │   ├── README.md                      # ✅ Stage documentation
    │   ├── stage.py                       # ✅ Stage implementation
    │   ├── __init__.py
    │   └── tests/
    │       └── test_stage.py              # ✅ Independent tests
    │
    ├── 02_TextGeneration/
    │   ├── README.md
    │   ├── stage.py
    │   ├── __init__.py
    │   └── tests/
    │       └── test_stage.py
    │
    ├── 03_AudioGeneration/
    │   ├── README.md
    │   ├── stage.py
    │   ├── __init__.py
    │   └── tests/
    │       └── test_stage.py
    │
    ├── 04_ImageGeneration/
    │   ├── README.md
    │   ├── stage.py
    │   ├── __init__.py
    │   └── tests/
    │       └── test_stage.py
    │
    ├── 05_VideoGeneration/
    │   ├── README.md
    │   ├── stage.py
    │   ├── __init__.py
    │   └── tests/
    │       └── test_stage.py
    │
    ├── MODULAR_ARCHITECTURE.md            # ✅ Architecture overview
    ├── MIGRATION_GUIDE.md                 # ✅ How to migrate
    ├── IMPLEMENTATION_STATUS.md           # ✅ Current status
    ├── VERIFICATION_CHECKLIST.md          # ✅ Verification steps
    └── README_MODULAR.md                  # ✅ Quick start guide
```

## Future: Separate Repositories

Once fully migrated, each stage can be its own repository:

### Repository: prismq-core
```
prismq-core/
├── prismq_core/
│   ├── __init__.py
│   ├── interfaces/
│   │   ├── pipeline_stage.py
│   │   ├── stage_contracts.py
│   │   ├── llm_provider.py
│   │   ├── voice_provider.py
│   │   └── storage_provider.py
│   └── utils/
│       └── validation.py
├── tests/
├── setup.py
└── README.md

# Install: pip install prismq-core
```

### Repository: prismq-stage-01-idea-generation
```
prismq-stage-01-idea-generation/
├── prismq_idea_generation/
│   ├── __init__.py
│   └── stage.py
├── tests/
│   └── test_stage.py
├── examples/
│   └── example_usage.py
├── requirements.txt
│   └── prismq-core>=1.0.0      # Only dependency
├── setup.py
└── README.md

# Install: pip install prismq-stage-01-idea-generation
```

### Repository: prismq-stage-02-text-generation
```
prismq-stage-02-text-generation/
├── prismq_text_generation/
│   ├── __init__.py
│   └── stage.py
├── tests/
├── requirements.txt
│   └── prismq-core>=1.0.0
├── setup.py
└── README.md

# Install: pip install prismq-stage-02-text-generation
```

... and so on for stages 03, 04, 05

### Repository: prismq-pipeline-orchestrator
```
prismq-pipeline-orchestrator/
├── prismq_orchestrator/
│   ├── __init__.py
│   └── orchestrator.py
├── tests/
├── requirements.txt
│   ├── prismq-core>=1.0.0
│   ├── prismq-stage-01-idea-generation>=1.0.0
│   ├── prismq-stage-02-text-generation>=1.0.0
│   ├── prismq-stage-03-audio-generation>=1.0.0
│   ├── prismq-stage-04-image-generation>=1.0.0
│   └── prismq-stage-05-video-generation>=1.0.0
├── setup.py
└── README.md

# Install: pip install prismq-pipeline-orchestrator
```

## Import Patterns

### ❌ Old Pattern (Coupled)
```python
# In Stage 01
from PrismQ.Pipeline.02_TextGeneration.StoryTitleProcessor import TitleGenerator
from PrismQ.Pipeline.03_AudioGeneration.VoiceOverGenerator import VoiceRecommender

# Creates coupling, circular dependencies
```

### ✅ New Pattern (Modular - Current Monorepo)
```python
# In Stage 01
from PrismQ.Infrastructure.Core.Shared.interfaces import (
    BasePipelineStage,
    IdeaGenerationInput,
    IdeaGenerationOutput,
    ILLMProvider,
)

# Only imports from shared infrastructure
```

### ✅ Future Pattern (Separate Repositories)
```python
# In prismq-stage-01-idea-generation
from prismq_core.interfaces import (
    BasePipelineStage,
    IdeaGenerationInput,
    IdeaGenerationOutput,
    ILLMProvider,
)

# Still only imports from core, but from separate package
```

## Dependency Graph

### Current (Coupled)
```
Stage 01 ←→ Stage 02 ←→ Stage 03
    ↓           ↓           ↓
  [Circular dependencies, hard to manage]
```

### Target (Modular)
```
Stage 01 → prismq-core
Stage 02 → prismq-core
Stage 03 → prismq-core
Stage 04 → prismq-core
Stage 05 → prismq-core

Orchestrator → prismq-core
            → Stage 01
            → Stage 02
            → Stage 03
            → Stage 04
            → Stage 05
```

## File Count Comparison

### Before
- Many files across scattered modules
- Unclear ownership and boundaries
- Duplicate functionality

### After
Each stage has:
- 1 `stage.py` (implementation)
- 1 `README.md` (documentation)
- 1+ test files
- Clean, minimal structure

## Migration Path

1. **Phase 1 (Current):** ✅ DONE
   - Create interfaces and contracts
   - Create documentation
   - Create examples

2. **Phase 2:** In Progress
   - Refactor Stage 01 to use new architecture
   - Refactor Stage 02 to use new architecture
   - Refactor stages 03, 04, 05
   - Remove cross-imports

3. **Phase 3:** Future
   - Extract `prismq-core` package
   - Move each stage to separate repository
   - Publish packages to PyPI
   - Version independently

## Benefits Summary

| Aspect | Before | After |
|--------|--------|-------|
| **Files per stage** | 10-20+ scattered | 2-3 focused files |
| **Dependencies** | Circular | Clean, one-way |
| **Testing** | Integration only | Unit tests per stage |
| **Development** | Monolithic | Independent modules |
| **Versioning** | All-or-nothing | Per-stage versioning |
| **Deployment** | Single deployment | Microservices ready |
