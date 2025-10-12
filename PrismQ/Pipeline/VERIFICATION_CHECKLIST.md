# Modular Architecture Verification Checklist

Use this checklist to verify that a pipeline stage is correctly implemented according to the modular architecture.

## ✅ Stage Independence Checklist

### 1. Interface Implementation
- [ ] Stage implements `IPipelineStage[TInput, TOutput]` or extends `BasePipelineStage`
- [ ] Has `stage_name` property defined
- [ ] Has `stage_id` property defined (format: `0X_stage_name`)
- [ ] Has `stage_version` property defined (semantic versioning)
- [ ] Implements `execute()` method or `_execute_impl()` for BasePipelineStage
- [ ] Implements `validate_input()` method

### 2. Input/Output Contracts
- [ ] Uses typed input contract (e.g., `IdeaGenerationInput`)
- [ ] Uses typed output contract (e.g., `IdeaGenerationOutput`)
- [ ] Input contract has all required fields
- [ ] Output contract has all required fields
- [ ] No use of raw dicts or untyped data structures

### 3. Dependencies
- [ ] Only imports from `PrismQ.Infrastructure.Core.Shared.interfaces`
- [ ] Does NOT import from other pipeline stages (`PrismQ.Pipeline.01_*`, etc.)
- [ ] Dependencies are injected via constructor
- [ ] No hard-coded provider instances
- [ ] Provider interfaces are used (e.g., `ILLMProvider`, not `OpenAIProvider`)

### 4. Testing
- [ ] Has unit tests
- [ ] Tests use mocked dependencies
- [ ] Tests verify input contract
- [ ] Tests verify output contract
- [ ] Tests verify metadata is populated
- [ ] Tests run independently without other stages
- [ ] All tests pass

### 5. Documentation
- [ ] Has README.md in stage directory
- [ ] README documents input contract
- [ ] README documents output contract
- [ ] README shows example usage
- [ ] README shows testing example
- [ ] README lists dependencies

## 🔍 Verification Commands

### Check for Cross-Stage Imports
```bash
# Should return ZERO results
grep -r "from PrismQ.Pipeline.0[1-5]" PrismQ/Pipeline/01_IdeaGeneration/ | wc -l
```

### Check for Hard-Coded Providers
```bash
# Should return ZERO results
grep -r "OpenAIProvider()" PrismQ/Pipeline/01_IdeaGeneration/ | wc -l
grep -r "ElevenLabsProvider()" PrismQ/Pipeline/03_AudioGeneration/ | wc -l
```

### Run Stage Tests in Isolation
```bash
# Should pass without needing other stages
PYTHONPATH=. python -m pytest PrismQ/Development/Tests/pipeline/test_stage_01_*.py
```

### Verify Contracts Work
```bash
# Should successfully import and create instances
PYTHONPATH=. python -c "
from PrismQ.Infrastructure.Core.Shared.interfaces import (
    IdeaGenerationInput,
    IdeaGenerationOutput
)
input_data = IdeaGenerationInput(target_gender='women', target_age='18-23')
print('✓ Contracts work correctly')
"
```

## 📊 Stage Maturity Levels

### Level 1: Basic Implementation ⭐
- [ ] Implements `IPipelineStage` interface
- [ ] Uses typed contracts for input/output
- [ ] Has basic tests

### Level 2: Independent ⭐⭐
- [ ] Level 1 requirements met
- [ ] No cross-stage imports
- [ ] Dependencies injected
- [ ] Tests use mocked dependencies
- [ ] Can run tests in isolation

### Level 3: Production Ready ⭐⭐⭐
- [ ] Level 2 requirements met
- [ ] Comprehensive test coverage (>80%)
- [ ] Input validation with error messages
- [ ] Complete documentation
- [ ] JSON schema for input/output
- [ ] Performance tests
- [ ] Error handling

### Level 4: Repository Ready ⭐⭐⭐⭐
- [ ] Level 3 requirements met
- [ ] Can be extracted to separate repository
- [ ] Has own `requirements.txt` (only depends on `prismq-core`)
- [ ] Has CI/CD configuration
- [ ] Versioned releases
- [ ] API documentation
- [ ] Example implementations

## 🚨 Common Anti-Patterns to Avoid

### ❌ Direct Stage Coupling
```python
# BAD - importing from another stage
from PrismQ.Pipeline.02_TextGeneration.StoryTitleProcessor import TitleGenerator

# GOOD - using contracts
from PrismQ.Infrastructure.Core.Shared.interfaces import TextGenerationInput
```

### ❌ Hard-Coded Dependencies
```python
# BAD - creating provider directly
class IdeaStage:
    def __init__(self):
        self.llm = OpenAIProvider()

# GOOD - dependency injection
class IdeaStage:
    def __init__(self, llm_provider: ILLMProvider):
        self.llm_provider = llm_provider
```

### ❌ Untyped Contracts
```python
# BAD - returning plain dict
def execute(self, input_data: dict) -> dict:
    return {"ideas": [...]}

# GOOD - using typed contracts
async def execute(self, input_data: IdeaGenerationInput) -> StageResult[IdeaGenerationOutput]:
    return StageResult(data=IdeaGenerationOutput(...))
```

### ❌ Stage Calling Stage
```python
# BAD - one stage directly calling another
class IdeaStage:
    def generate(self):
        ideas = self.generate_ideas()
        text_gen = TextGenerationStage()
        return text_gen.generate(ideas)  # Direct coupling!

# GOOD - let orchestrator handle chaining
class IdeaStage:
    async def _execute_impl(self, input_data):
        ideas = self.generate_ideas()
        return IdeaGenerationOutput(ideas=ideas)
```

## 📈 Progress Tracking

Use this section to track migration progress:

### Stage 01: Idea Generation
- [ ] Interface implementation
- [ ] Input/output contracts
- [ ] No cross-dependencies
- [ ] Independent tests
- [ ] Documentation
- **Status:** Not Started / In Progress / Complete

### Stage 02: Text Generation
- [ ] Interface implementation
- [ ] Input/output contracts
- [ ] No cross-dependencies
- [ ] Independent tests
- [ ] Documentation
- **Status:** Not Started / In Progress / Complete

### Stage 03: Audio Generation
- [ ] Interface implementation
- [ ] Input/output contracts
- [ ] No cross-dependencies
- [ ] Independent tests
- [ ] Documentation
- **Status:** Not Started / In Progress / Complete

### Stage 04: Image Generation
- [ ] Interface implementation
- [ ] Input/output contracts
- [ ] No cross-dependencies
- [ ] Independent tests
- [ ] Documentation
- **Status:** Not Started / In Progress / Complete

### Stage 05: Video Generation
- [ ] Interface implementation
- [ ] Input/output contracts
- [ ] No cross-dependencies
- [ ] Independent tests
- [ ] Documentation
- **Status:** Not Started / In Progress / Complete

## 🎯 Definition of Done

A stage is considered "modular" when:

1. ✅ All items in "Stage Independence Checklist" are checked
2. ✅ All verification commands pass
3. ✅ Reaches at least "Level 2: Independent" maturity
4. ✅ No anti-patterns present
5. ✅ Can be tested without any other stage
6. ✅ Only depends on shared infrastructure interfaces

## 📝 Review Process

Before merging stage implementation:

1. **Self-Review:** Go through this checklist yourself
2. **Automated Checks:** Run all verification commands
3. **Peer Review:** Have another developer verify
4. **Integration Test:** Run stage in full pipeline
5. **Documentation Review:** Ensure README is complete

## 🔗 Related Resources

- **Architecture:** `PrismQ/Pipeline/MODULAR_ARCHITECTURE.md`
- **Migration:** `PrismQ/Pipeline/MIGRATION_GUIDE.md`
- **Status:** `PrismQ/Pipeline/IMPLEMENTATION_STATUS.md`
- **Examples:** `PrismQ/Development/Examples/`
- **Tests:** `PrismQ/Development/Tests/pipeline/test_stage_contracts.py`
