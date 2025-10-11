# PrismQ Modular Pipeline Architecture - Quick Start

## 🎯 Goal

Transform PrismQ pipeline stages into fully independent, modular components that can be:
- Developed in separate repositories
- Tested independently
- Versioned separately
- Deployed as microservices

## 📊 Architecture Diagram

### Before: Tightly Coupled Architecture
```
┌─────────────────────────────────────────────────────────────────┐
│                      Tightly Coupled Pipeline                     │
│                                                                   │
│  ┌──────────────┐    ┌──────────────┐    ┌─────────────────┐   │
│  │   Stage 01   │───>│   Stage 02   │───>│    Stage 03     │   │
│  │     Idea     │<───│     Text     │<───│     Audio       │   │
│  │  Generation  │    │  Generation  │    │   Generation    │   │
│  └──────────────┘    └──────────────┘    └─────────────────┘   │
│         │                    │                      │            │
│         └────────────────────┴──────────────────────┘            │
│                    Cross-imports everywhere ❌                    │
│              (Circular dependencies, hard to test)               │
└─────────────────────────────────────────────────────────────────┘
```

### After: Modular Architecture with Contracts
```
┌─────────────────────────────────────────────────────────────────┐
│                     Modular Pipeline Architecture                 │
│                                                                   │
│  ┌──────────────┐  [IdeaOutput]  ┌──────────────────────────┐   │
│  │   Stage 01   │───────────────>│                          │   │
│  │     Idea     │                │                          │   │
│  │  Generation  │                │      Orchestrator        │   │
│  └──────────────┘                │    (Coordinates flow)    │   │
│         ↓                         │                          │   │
│   Only depends on                │                          │   │
│   ILLMProvider ✅                 │                          │   │
│                                   │                          │   │
│  ┌──────────────┐  [TextOutput]  │                          │   │
│  │   Stage 02   │───────────────>│                          │   │
│  │     Text     │                │                          │   │
│  │  Generation  │                └──────────────────────────┘   │
│  └──────────────┘                             │                  │
│         ↓                                     │                  │
│   Only depends on                             ↓                  │
│   ILLMProvider ✅                     [VideoOutput]              │
│                                                                   │
│  Each stage:                                                     │
│  ✅ Independent                                                  │
│  ✅ Testable in isolation                                       │
│  ✅ Clear contracts                                             │
│  ✅ No cross-dependencies                                       │
└─────────────────────────────────────────────────────────────────┘
```

## 🔑 Key Concepts

### 1. Pipeline Stage Interface
Every stage implements:
```python
IPipelineStage[TInput, TOutput]
    ├── stage_name: str
    ├── stage_id: str
    ├── stage_version: str
    ├── execute(input: TInput) -> StageResult[TOutput]
    └── validate_input(input: TInput) -> bool
```

### 2. Stage Contracts (Data Classes)
Clear input/output types for each stage:
```
Stage 01: IdeaGenerationInput  -> IdeaGenerationOutput
Stage 02: TextGenerationInput  -> TextGenerationOutput
Stage 03: AudioGenerationInput -> AudioGenerationOutput
Stage 04: ImageGenerationInput -> ImageGenerationOutput
Stage 05: VideoGenerationInput -> VideoGenerationOutput
```

### 3. No Cross-Dependencies
```
✅ GOOD:
PrismQ/Pipeline/01_IdeaGeneration/
    ├── stage.py
    │   └── from PrismQ.Infrastructure.Core.Shared.interfaces import (
    │           IPipelineStage, ILLMProvider, IdeaGenerationInput, ...
    │       )
    └── tests/
        └── test_stage.py (mocked dependencies)

❌ BAD:
PrismQ/Pipeline/01_IdeaGeneration/
    └── script.py
        └── from PrismQ.Pipeline.02_TextGeneration import TitleGenerator
            (Cross-stage import! Creates coupling)
```

## 🚀 Quick Start

### 1. Create a New Stage (5 Steps)

```python
# Step 1: Import base and contracts
from PrismQ.Infrastructure.Core.Shared.interfaces import (
    BasePipelineStage,
    IdeaGenerationInput,
    IdeaGenerationOutput,
    ILLMProvider,
)

# Step 2: Implement the stage
class IdeaGenerationStage(BasePipelineStage[IdeaGenerationInput, IdeaGenerationOutput]):
    def __init__(self, llm_provider: ILLMProvider):
        super().__init__(
            stage_name="IdeaGeneration",
            stage_id="01_idea_generation",
            version="1.0.0"
        )
        self.llm = llm_provider
    
    # Step 3: Implement execution logic
    async def _execute_impl(self, input_data: IdeaGenerationInput) -> IdeaGenerationOutput:
        # Your logic here
        ideas = []
        # ... generate ideas ...
        return IdeaGenerationOutput(ideas=ideas, ...)
    
    # Step 4: Implement validation
    async def validate_input(self, input_data: IdeaGenerationInput) -> bool:
        return input_data.target_gender in ['women', 'men', 'all']

# Step 5: Use the stage
stage = IdeaGenerationStage(llm_provider=my_llm)
result = await stage.execute(IdeaGenerationInput(...))
```

### 2. Chain Stages Together

```python
from PrismQ.Development.Examples.pipeline_orchestrator import PipelineOrchestrator

# Create independent stages
idea_stage = IdeaGenerationStage(llm)
text_stage = TextGenerationStage(llm)
audio_stage = AudioGenerationStage(voice_provider)

# Orchestrator chains them via contracts
orchestrator = PipelineOrchestrator(
    idea_stage=idea_stage,
    text_stage=text_stage,
    audio_stage=audio_stage
)

# Run the pipeline
result = await orchestrator.run_full_pipeline(
    target_gender="women",
    target_age="18-23"
)
```

### 3. Test Stages Independently

```python
@pytest.mark.asyncio
async def test_idea_stage():
    # Mock dependencies
    mock_llm = Mock()
    mock_llm.generate_completion.return_value = "Test idea"
    
    # Create stage
    stage = IdeaGenerationStage(llm_provider=mock_llm)
    
    # Test with contract
    input_data = IdeaGenerationInput(
        target_gender="women",
        target_age="18-23"
    )
    
    result = await stage.execute(input_data)
    
    # Verify contract
    assert result.data.total_count > 0
    assert result.metadata.status == StageStatus.COMPLETED
```

## 📁 File Structure

```
PrismQ/
├── Infrastructure/Core/Shared/interfaces/
│   ├── pipeline_stage.py          # Base interfaces
│   ├── stage_contracts.py         # Input/output contracts
│   ├── llm_provider.py           # Provider interfaces
│   └── __init__.py               # Exports all
│
├── Pipeline/
│   ├── MODULAR_ARCHITECTURE.md   # ⭐ Architecture overview
│   ├── MIGRATION_GUIDE.md        # ⭐ How to migrate code
│   ├── IMPLEMENTATION_STATUS.md  # ⭐ Current status
│   │
│   ├── 01_IdeaGeneration/
│   │   ├── README.md             # Stage docs
│   │   └── stage.py              # Implementation (future)
│   │
│   ├── 02_TextGeneration/
│   │   ├── README.md
│   │   └── stage.py              # (future)
│   │
│   └── ... (03, 04, 05)
│
└── Development/
    ├── Examples/
    │   ├── stage_01_idea_generation.py    # ⭐ Full example
    │   └── pipeline_orchestrator.py       # ⭐ Chaining example
    │
    └── Tests/pipeline/
        └── test_stage_contracts.py        # ⭐ Contract tests
```

## 📚 Essential Reading

1. **Start Here:**
   - `PrismQ/Pipeline/MODULAR_ARCHITECTURE.md` - Understand the architecture

2. **Learn by Example:**
   - `PrismQ/Development/Examples/stage_01_idea_generation.py` - Full implementation
   - `PrismQ/Development/Examples/pipeline_orchestrator.py` - Stage chaining

3. **Migrate Existing Code:**
   - `PrismQ/Pipeline/MIGRATION_GUIDE.md` - Step-by-step guide

4. **Check Progress:**
   - `PrismQ/Pipeline/IMPLEMENTATION_STATUS.md` - What's done, what's next

## 🧪 Try It Out

### Run the Example Pipeline
```bash
cd /home/runner/work/StoryGenerator/StoryGenerator
PYTHONPATH=. python PrismQ/Development/Examples/pipeline_orchestrator.py
```

Expected output:
```
============================================================
Pipeline Orchestrator - Full Pipeline Execution
============================================================
Stage 01: Generating ideas...
✓ Generated 1 ideas in 100ms
...
Stage 05: Assembling video...
✓ Generated video in 3000ms
============================================================
Pipeline Complete!
============================================================
```

### Run the Tests
```bash
PYTHONPATH=. python -m pytest PrismQ/Development/Tests/pipeline/test_stage_contracts.py -v
```

### Check Your Code
```bash
# Find cross-stage imports (should be none)
grep -r "from PrismQ.Pipeline.0[1-5]" PrismQ/Pipeline/*/
```

## ✨ Benefits Summary

| Aspect | Before (Coupled) | After (Modular) |
|--------|-----------------|-----------------|
| **Testing** | Must run entire pipeline | Test each stage independently |
| **Development** | Changes affect all stages | Develop stages in isolation |
| **Dependencies** | Circular imports | Clean, one-way flow |
| **Deployment** | Monolithic | Can deploy stages separately |
| **Versioning** | All-or-nothing | Independent versioning |
| **Repositories** | Single repo | Can split into multiple repos |
| **Understanding** | Complex flow | Clear contracts |

## 🎓 Learning Path

1. **Understand the Problem** (5 min)
   - Read this file
   - See the "Before/After" diagrams

2. **Learn the Architecture** (15 min)
   - Read `MODULAR_ARCHITECTURE.md`
   - Understand contracts and interfaces

3. **See It in Action** (10 min)
   - Run `pipeline_orchestrator.py`
   - Review `stage_01_idea_generation.py`

4. **Migrate Your Code** (varies)
   - Follow `MIGRATION_GUIDE.md`
   - One stage at a time

5. **Test & Verify** (ongoing)
   - Write contract-based tests
   - Check for cross-imports

## 🔗 Related Files

- **Interfaces:** `PrismQ/Infrastructure/Core/Shared/interfaces/`
- **Contracts:** `PrismQ/Infrastructure/Core/Shared/interfaces/stage_contracts.py`
- **Examples:** `PrismQ/Development/Examples/`
- **Tests:** `PrismQ/Development/Tests/pipeline/test_stage_contracts.py`
- **Stage Docs:** `PrismQ/Pipeline/01_IdeaGeneration/README.md` (and 02, 03, 04, 05)

## 💡 Key Takeaway

> Each pipeline stage is now a **fully independent module** with:
> - ✅ Clear input/output contracts (typed data classes)
> - ✅ No dependencies on other stages
> - ✅ Complete testability in isolation
> - ✅ Ability to be developed in separate repositories

This enables true modular development where teams can work on different stages simultaneously without conflicts or coupling.
