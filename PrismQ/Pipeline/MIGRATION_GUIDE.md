# Migration Guide: From Tightly Coupled to Modular Architecture

## Overview

This guide helps you migrate existing pipeline code from the tightly coupled architecture to the new modular architecture with clear input/output contracts.

## Why Migrate?

### Current Problems (Tightly Coupled)
- ❌ Stages directly import and call each other
- ❌ Circular dependencies between modules
- ❌ Cannot test stages in isolation
- ❌ Cannot develop stages independently
- ❌ Cannot version/deploy stages separately
- ❌ Difficult to understand data flow

### Benefits of Modular Architecture
- ✅ Each stage is independently testable
- ✅ Clear input/output contracts
- ✅ No cross-stage dependencies
- ✅ Stages can be developed in separate repos
- ✅ Easy to version and deploy independently
- ✅ Clean separation of concerns

## Migration Steps

### Step 1: Understand the New Architecture

The new architecture uses:
1. **Base Interface**: `IPipelineStage[TInput, TOutput]`
2. **Stage Contracts**: Data classes for input/output (e.g., `IdeaGenerationInput`, `IdeaGenerationOutput`)
3. **Base Implementation**: `BasePipelineStage` with common functionality

### Step 2: Identify Cross-Stage Imports (Anti-Pattern)

**Before (Bad - Cross-stage imports):**
```python
# In 01_IdeaGeneration/scripts/generate_ideas.py
from PrismQ.IdeaScraper.idea_generation import IdeaGenerator
from PrismQ.StoryTitleProcessor.title_generation import TitleGenerator  # BAD!
from PrismQ.VoiceOverGenerator.voice_recommendation import VoiceRecommender  # BAD!

# Stages calling each other directly
ideas = idea_generator.generate_ideas(gender, age)
titles = title_generator.generate_titles(ideas)  # Direct coupling!
```

**After (Good - Contract-based):**
```python
# Only import contracts and interfaces
from PrismQ.Infrastructure.Core.Shared.interfaces import (
    IdeaGenerationInput,
    IdeaGenerationOutput,
    TextGenerationInput,
    IPipelineStage,
)

# Stages communicate through contracts
idea_result = await idea_stage.execute(IdeaGenerationInput(...))
text_input = TextGenerationInput(idea=idea_result.data.ideas[0])
text_result = await text_stage.execute(text_input)
```

### Step 3: Refactor Stage Implementation

#### Example: Migrating Idea Generation Stage

**Before (Old Implementation):**
```python
# PrismQ/Pipeline/01_IdeaGeneration/IdeaScraper/idea_generation.py
from PrismQ.Shared.interfaces.llm_provider import ILLMProvider  # Old path

class IdeaGenerator:
    def __init__(self, llm_provider: ILLMProvider):
        self.llm = llm_provider
    
    def generate_ideas(self, gender: str, age: str, count: int = 20):
        # Returns plain dict/list
        prompt = f"Generate ideas for {gender} aged {age}"
        response = self.llm.generate_completion(prompt)
        # ... parsing logic ...
        return ideas  # Untyped list
```

**After (New Implementation):**
```python
# PrismQ/Pipeline/01_IdeaGeneration/stage.py
from PrismQ.Infrastructure.Core.Shared.interfaces import (
    BasePipelineStage,
    IdeaGenerationInput,
    IdeaGenerationOutput,
    IdeaItem,
    ILLMProvider,
)

class IdeaGenerationStage(BasePipelineStage[IdeaGenerationInput, IdeaGenerationOutput]):
    def __init__(self, llm_provider: ILLMProvider):
        super().__init__(
            stage_name="IdeaGeneration",
            stage_id="01_idea_generation",
            version="1.0.0"
        )
        self.llm_provider = llm_provider
    
    async def _execute_impl(self, input_data: IdeaGenerationInput) -> IdeaGenerationOutput:
        # Type-safe input and output
        ideas = []
        # ... generation logic using input_data.target_gender, input_data.target_age ...
        
        return IdeaGenerationOutput(
            ideas=ideas,
            total_count=len(ideas),
            adapted_count=0,
            generated_count=len(ideas)
        )
    
    async def validate_input(self, input_data: IdeaGenerationInput) -> bool:
        # Input validation
        valid_genders = ['women', 'men', 'all', 'non-binary']
        return input_data.target_gender in valid_genders
```

### Step 4: Update Scripts/Orchestration

**Before (Direct coupling):**
```python
# scripts/generate_ideas.py
from PrismQ.IdeaScraper.idea_generation import IdeaGenerator
from PrismQ.StoryTitleProcessor.title_generation import TitleGenerator

# Direct instantiation and chaining
llm = MockLLMProvider()
idea_gen = IdeaGenerator(llm)
title_gen = TitleGenerator(llm)

ideas = idea_gen.generate_ideas("women", "18-23")
titles = title_gen.generate_titles(ideas)  # Tight coupling
```

**After (Contract-based orchestration):**
```python
# scripts/run_pipeline.py
from PrismQ.Infrastructure.Core.Shared.interfaces import (
    IdeaGenerationInput,
    TextGenerationInput,
)
from PrismQ.Development.Examples.pipeline_orchestrator import PipelineOrchestrator

# Dependency injection - stages are independent
from stage_01 import IdeaGenerationStage
from stage_02 import TextGenerationStage

llm = MockLLMProvider()
idea_stage = IdeaGenerationStage(llm)
text_stage = TextGenerationStage(llm)

orchestrator = PipelineOrchestrator(
    idea_stage=idea_stage,
    text_stage=text_stage
)

# Run with clear contracts
result = await orchestrator.run_full_pipeline(
    target_gender="women",
    target_age="18-23"
)
```

### Step 5: Update Tests

**Before (Coupled tests):**
```python
# Test depends on other stages
def test_idea_generation():
    from PrismQ.IdeaScraper.idea_generation import IdeaGenerator
    
    gen = IdeaGenerator(mock_llm)
    ideas = gen.generate_ideas("women", "18-23")
    
    # Untyped assertions
    assert len(ideas) > 0
    assert "content" in ideas[0]
```

**After (Independent contract tests):**
```python
# Test only the contract, not implementation
@pytest.mark.asyncio
async def test_idea_generation_stage():
    from PrismQ.Infrastructure.Core.Shared.interfaces import (
        IdeaGenerationInput,
        IdeaGenerationOutput,
        StageStatus,
    )
    
    mock_llm = Mock()
    mock_llm.generate_completion.return_value = "Test idea"
    
    stage = IdeaGenerationStage(llm_provider=mock_llm)
    
    input_data = IdeaGenerationInput(
        target_gender="women",
        target_age="18-23",
        idea_count=1
    )
    
    result = await stage.execute(input_data)
    
    # Type-safe assertions on contract
    assert isinstance(result.data, IdeaGenerationOutput)
    assert result.data.total_count >= 1
    assert result.metadata.status == StageStatus.COMPLETED
```

## Common Migration Patterns

### Pattern 1: Remove Direct Stage Calls

**Before:**
```python
# In Stage 01 calling Stage 02 directly (BAD)
from PrismQ.StoryTitleProcessor.title_generation import TitleGenerator

ideas = self.generate_ideas(...)
title_generator = TitleGenerator(self.llm)
titles = title_generator.generate_titles(ideas)  # Cross-stage call
```

**After:**
```python
# Stages don't call each other (GOOD)
# Return output, let orchestrator handle chaining

return IdeaGenerationOutput(
    ideas=ideas,
    total_count=len(ideas),
    # ... other fields
)

# Orchestrator handles the chaining
idea_result = await idea_stage.execute(idea_input)
text_input = TextGenerationInput(idea=idea_result.data.ideas[0])
text_result = await text_stage.execute(text_input)
```

### Pattern 2: Replace Untyped Dicts with Contracts

**Before:**
```python
def generate_ideas(...) -> list[dict]:
    return [
        {
            "id": "001",
            "content": "...",
            "metadata": {...}
        }
    ]
```

**After:**
```python
async def _execute_impl(self, input_data: IdeaGenerationInput) -> IdeaGenerationOutput:
    ideas = [
        IdeaItem(
            id="001",
            content="...",
            source="llm_generated",
            target_gender=input_data.target_gender,
            target_age=input_data.target_age,
            created_at=datetime.now(),
            metadata={...}
        )
    ]
    
    return IdeaGenerationOutput(
        ideas=ideas,
        total_count=len(ideas),
        adapted_count=0,
        generated_count=len(ideas)
    )
```

### Pattern 3: Dependency Injection Over Direct Imports

**Before:**
```python
# Stage creates its own dependencies
from PrismQ.Providers.openai_provider import OpenAIProvider

class IdeaGenerator:
    def __init__(self):
        self.llm = OpenAIProvider()  # Hard-coded dependency
```

**After:**
```python
# Dependencies injected through constructor
class IdeaGenerationStage(BasePipelineStage[...]):
    def __init__(self, llm_provider: ILLMProvider):
        super().__init__(...)
        self.llm_provider = llm_provider  # Injected, testable
```

## Checklist for Each Stage

When migrating a stage, ensure:

- [ ] Remove all cross-stage imports (imports from other pipeline stages)
- [ ] Only import from `Infrastructure/Core/Shared/interfaces`
- [ ] Implement `IPipelineStage[TInput, TOutput]` interface
- [ ] Use stage-specific input/output contracts (e.g., `IdeaGenerationInput/Output`)
- [ ] Add input validation in `validate_input()` method
- [ ] Inject dependencies through constructor (no hard-coded dependencies)
- [ ] Update tests to use contracts and mock dependencies
- [ ] Document the stage's contract in its README

## Verifying Migration Success

### 1. Import Graph Should Be Clean

Run this to check for cross-stage imports:
```bash
# Should find NO results (all cross-imports removed)
grep -r "from PrismQ.Pipeline.0[1-5]" PrismQ/Pipeline/*/
```

### 2. Tests Should Pass in Isolation

Each stage's tests should run without needing other stages:
```bash
pytest PrismQ/Development/Tests/pipeline/test_stage_01_*.py
pytest PrismQ/Development/Tests/pipeline/test_stage_02_*.py
```

### 3. Stages Should Be Independently Deployable

Each stage should:
- Have its own `stage.py` with the implementation
- Only depend on `prismq-core` (interfaces/contracts)
- Have a `requirements.txt` with minimal dependencies
- Have its own tests and documentation

## Future: Separate Repositories

Once migration is complete, each stage can move to its own repository:

```
prismq-core/                          # Shared contracts/interfaces
├── interfaces/
│   ├── pipeline_stage.py
│   ├── stage_contracts.py
│   └── provider_interfaces.py

prismq-stage-01-idea-generation/      # Stage 01
├── src/
│   └── stage.py
├── tests/
├── requirements.txt                   # Only depends on prismq-core
└── README.md

prismq-stage-02-text-generation/      # Stage 02
├── src/
│   └── stage.py
├── tests/
├── requirements.txt                   # Only depends on prismq-core
└── README.md

# ... and so on for other stages
```

## Getting Help

- See `PrismQ/Pipeline/MODULAR_ARCHITECTURE.md` for architecture overview
- See `PrismQ/Pipeline/01_IdeaGeneration/README.md` for stage-specific docs
- See `PrismQ/Development/Examples/` for working examples
- Run example: `python PrismQ/Development/Examples/pipeline_orchestrator.py`
