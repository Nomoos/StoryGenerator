# Architecture: Decouple Components

**Group:** group_1  
**Priority:** P1 (High)  
**Status:** 📋 Not Started  
**Estimated Effort:** 6-8 hours  

## Description

Refactor tightly coupled components into modular, testable units with clear interfaces. Implement dependency injection and interface-based design.

## Acceptance Criteria

- [ ] Define clear interfaces for core components
- [ ] Implement dependency injection container
- [ ] Refactor generators to use interfaces
- [ ] Remove circular dependencies
- [ ] Document component architecture
- [ ] Unit tests with mocked dependencies

## Dependencies

- Requires: `code-quality-input-validation` (for interface definitions)
- Install: `dependency-injector>=4.41.0` (optional DI container)

## Implementation Notes

Create `core/interfaces.py`:

```python
from abc import ABC, abstractmethod
from typing import List, Dict, Any

class ILLMProvider(ABC):
    @abstractmethod
    def generate(self, prompt: str, **kwargs) -> str:
        pass

class ITTSProvider(ABC):
    @abstractmethod
    def synthesize(self, text: str, voice: str) -> bytes:
        pass

class IGenerator(ABC):
    @abstractmethod
    def generate(self, input_data: Dict[str, Any]) -> Any:
        pass
```

Refactor generators to accept dependencies:

```python
class IdeaGenerator:
    def __init__(self, llm_provider: ILLMProvider, logger: Logger):
        self.llm = llm_provider
        self.logger = logger
    
    def generate(self, content: str) -> StoryIdea:
        # Implementation uses injected dependencies
        pass
```

## Links

- Related: [docs/RESEARCH_AND_IMPROVEMENTS.md](../../../docs/RESEARCH_AND_IMPROVEMENTS.md) Section 8
- Related roadmap: [HYBRID_ROADMAP.md](../../../docs/roadmaps/HYBRID_ROADMAP.md)
