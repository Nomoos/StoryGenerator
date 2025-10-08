# Architecture: Decouple Components and Refactor

**ID:** `architecture-decoupling`  
**Priority:** P1 (High)  
**Effort:** 12-16 hours  
**Status:** Not Started  
**Severity:** MEDIUM

## Overview

The current codebase has tight coupling between components, with generators directly depending on file system operations. This makes the code difficult to test, hard to maintain, and prevents swapping implementations. A proper architecture with clear separation of concerns is needed.

## Current State

### Problems

- ❌ Generators directly depend on file system operations
- ❌ No clear separation of concerns
- ❌ Difficult to unit test (can't mock dependencies)
- ❌ Hard to swap implementations
- ❌ Business logic mixed with infrastructure code
- ❌ No dependency injection

## Dependencies

**Requires:**
- `security-file-paths` - Path handling should be fixed first

**Blocks:**
- Comprehensive unit testing
- Mock testing
- Alternative storage implementations

## Acceptance Criteria

### Architecture
- [ ] Define clear interfaces for providers
- [ ] Separate core logic from infrastructure
- [ ] Implement dependency injection
- [ ] Create abstract base classes for extensibility
- [ ] Follow SOLID principles

### Code Organization
- [ ] Reorganize into `core/`, `providers/`, `generators/` structure
- [ ] Move interfaces to `core/interfaces/`
- [ ] Move models to `core/models/`
- [ ] Implement concrete providers in `providers/`

### Testing
- [ ] All components can be unit tested in isolation
- [ ] Mock implementations for testing
- [ ] Integration tests for full workflows

### Documentation
- [ ] Architecture diagram
- [ ] Component interaction documentation
- [ ] Interface documentation

## Task Details

### 1. Proposed Architecture

```
StoryGenerator/
├── core/
│   ├── __init__.py
│   ├── interfaces/
│   │   ├── __init__.py
│   │   ├── llm_provider.py          # Abstract LLM provider
│   │   ├── storage_provider.py      # Abstract storage
│   │   ├── voice_provider.py        # Abstract TTS
│   │   └── image_provider.py        # Abstract image generation
│   └── models/
│       ├── __init__.py
│       ├── story_idea.py
│       ├── script.py
│       └── voice_config.py
│
├── providers/
│   ├── __init__.py
│   ├── openai_provider.py           # OpenAI implementation
│   ├── elevenlabs_provider.py       # ElevenLabs implementation
│   ├── file_storage.py              # File system storage
│   └── mock_provider.py             # Mock for testing
│
├── generators/
│   ├── __init__.py
│   ├── idea_generator.py
│   ├── script_generator.py
│   ├── revision_generator.py
│   └── voice_generator.py
│
├── config/
│   ├── __init__.py
│   └── settings.py
│
└── tests/
    ├── unit/
    └── integration/
```

### 2. Define Interfaces

Create `core/interfaces/llm_provider.py`:
```python
from abc import ABC, abstractmethod
from typing import List, Dict, Optional

class ILLMProvider(ABC):
    """Interface for Large Language Model providers."""
    
    @abstractmethod
    def generate_completion(
        self,
        prompt: str,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None
    ) -> str:
        """Generate text completion from prompt."""
        pass
    
    @abstractmethod
    def generate_chat(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: Optional[int] = None
    ) -> str:
        """Generate response from chat messages."""
        pass
```

Create `core/interfaces/storage_provider.py`:
```python
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Optional

class IStorageProvider(ABC):
    """Interface for storage providers."""
    
    @abstractmethod
    def save_json(self, path: Path, data: dict) -> None:
        """Save data as JSON."""
        pass
    
    @abstractmethod
    def load_json(self, path: Path) -> dict:
        """Load JSON data."""
        pass
    
    @abstractmethod
    def save_text(self, path: Path, text: str) -> None:
        """Save text file."""
        pass
    
    @abstractmethod
    def load_text(self, path: Path) -> str:
        """Load text file."""
        pass
    
    @abstractmethod
    def exists(self, path: Path) -> bool:
        """Check if file exists."""
        pass
    
    @abstractmethod
    def list_files(self, directory: Path, pattern: str = "*") -> List[Path]:
        """List files in directory matching pattern."""
        pass
```

Create `core/interfaces/voice_provider.py`:
```python
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Optional

class IVoiceProvider(ABC):
    """Interface for text-to-speech providers."""
    
    @abstractmethod
    def generate_audio(
        self,
        text: str,
        voice_id: str,
        output_path: Path,
        model_id: Optional[str] = None
    ) -> Path:
        """Generate audio from text."""
        pass
    
    @abstractmethod
    def list_voices(self) -> List[Dict[str, Any]]:
        """List available voices."""
        pass
```

### 3. Implement Concrete Providers

Create `providers/openai_provider.py`:
```python
from core.interfaces.llm_provider import ILLMProvider
from openai import OpenAI
import os
from typing import List, Dict, Optional

class OpenAIProvider(ILLMProvider):
    """OpenAI implementation of LLM provider."""
    
    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-4o-mini"):
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        if not self.api_key:
            raise ValueError("OpenAI API key required")
        
        self.model = model
        self.client = OpenAI(api_key=self.api_key)
    
    def generate_completion(self, prompt: str, temperature: float = 0.7, 
                          max_tokens: Optional[int] = None) -> str:
        messages = [{"role": "user", "content": prompt}]
        return self.generate_chat(messages, temperature, max_tokens)
    
    def generate_chat(self, messages: List[Dict[str, str]], 
                     temperature: float = 0.7,
                     max_tokens: Optional[int] = None) -> str:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens
        )
        return response.choices[0].message.content
```

Create `providers/file_storage.py`:
```python
from core.interfaces.storage_provider import IStorageProvider
from pathlib import Path
import json
from typing import List

class FileStorageProvider(IStorageProvider):
    """File system implementation of storage provider."""
    
    def save_json(self, path: Path, data: dict) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    def load_json(self, path: Path) -> dict:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def save_text(self, path: Path, text: str) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(text)
    
    def load_text(self, path: Path) -> str:
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
    
    def exists(self, path: Path) -> bool:
        return path.exists()
    
    def list_files(self, directory: Path, pattern: str = "*") -> List[Path]:
        if not directory.exists():
            return []
        return list(directory.glob(pattern))
```

### 4. Refactor Generators to Use Interfaces

**Before:**
```python
class IdeaGenerator:
    def generate(self, prompt: str):
        # Direct OpenAI call
        response = openai.ChatCompletion.create(...)
        
        # Direct file write
        with open("C:\\...\\output.json", 'w') as f:
            json.dump(data, f)
```

**After:**
```python
from core.interfaces.llm_provider import ILLMProvider
from core.interfaces.storage_provider import IStorageProvider

class IdeaGenerator:
    """Generate story ideas using LLM."""
    
    def __init__(self, llm: ILLMProvider, storage: IStorageProvider):
        """
        Initialize idea generator.
        
        Args:
            llm: LLM provider for generating ideas
            storage: Storage provider for saving results
        """
        self.llm = llm
        self.storage = storage
    
    def generate(self, prompt: str, output_path: Path) -> dict:
        """Generate ideas and save to storage."""
        # Use injected LLM provider
        response = self.llm.generate_completion(prompt)
        
        # Parse and structure response
        ideas = self._parse_ideas(response)
        
        # Use injected storage provider
        self.storage.save_json(output_path, ideas)
        
        return ideas
```

### 5. Dependency Injection Container

Create `config/container.py`:
```python
from providers.openai_provider import OpenAIProvider
from providers.elevenlabs_provider import ElevenLabsProvider
from providers.file_storage import FileStorageProvider
from generators.idea_generator import IdeaGenerator
from generators.script_generator import ScriptGenerator

class Container:
    """Dependency injection container."""
    
    def __init__(self):
        # Providers
        self._llm_provider = None
        self._storage_provider = None
        self._voice_provider = None
        
        # Generators
        self._idea_generator = None
        self._script_generator = None
    
    @property
    def llm_provider(self):
        if self._llm_provider is None:
            self._llm_provider = OpenAIProvider()
        return self._llm_provider
    
    @property
    def storage_provider(self):
        if self._storage_provider is None:
            self._storage_provider = FileStorageProvider()
        return self._storage_provider
    
    @property
    def voice_provider(self):
        if self._voice_provider is None:
            self._voice_provider = ElevenLabsProvider()
        return self._voice_provider
    
    @property
    def idea_generator(self):
        if self._idea_generator is None:
            self._idea_generator = IdeaGenerator(
                llm=self.llm_provider,
                storage=self.storage_provider
            )
        return self._idea_generator
    
    @property
    def script_generator(self):
        if self._script_generator is None:
            self._script_generator = ScriptGenerator(
                llm=self.llm_provider,
                storage=self.storage_provider
            )
        return self._script_generator
```

### 6. Usage Example

```python
from config.container import Container

# Create container
container = Container()

# Get generator with dependencies injected
idea_gen = container.idea_generator

# Use generator
ideas = idea_gen.generate(
    prompt="Generate story ideas about...",
    output_path=Path("./output/ideas.json")
)
```

### 7. Mock for Testing

Create `providers/mock_provider.py`:
```python
from core.interfaces.llm_provider import ILLMProvider

class MockLLMProvider(ILLMProvider):
    """Mock LLM provider for testing."""
    
    def __init__(self, responses: List[str] = None):
        self.responses = responses or ["Mock response"]
        self.call_count = 0
    
    def generate_completion(self, prompt: str, **kwargs) -> str:
        response = self.responses[self.call_count % len(self.responses)]
        self.call_count += 1
        return response
    
    def generate_chat(self, messages: List[Dict], **kwargs) -> str:
        return self.generate_completion("", **kwargs)
```

### 8. Unit Testing Example

```python
import pytest
from generators.idea_generator import IdeaGenerator
from providers.mock_provider import MockLLMProvider
from providers.file_storage import FileStorageProvider

def test_idea_generator(tmp_path):
    """Test idea generator with mocked dependencies."""
    # Setup mocks
    mock_llm = MockLLMProvider(responses=["Test idea 1", "Test idea 2"])
    storage = FileStorageProvider()
    
    # Create generator with injected dependencies
    generator = IdeaGenerator(llm=mock_llm, storage=storage)
    
    # Test generation
    output_path = tmp_path / "ideas.json"
    result = generator.generate("Test prompt", output_path)
    
    # Verify
    assert output_path.exists()
    assert mock_llm.call_count == 1
```

## Output Files

- `core/interfaces/llm_provider.py`
- `core/interfaces/storage_provider.py`
- `core/interfaces/voice_provider.py`
- `core/models/` - Domain models
- `providers/openai_provider.py`
- `providers/elevenlabs_provider.py`
- `providers/file_storage.py`
- `providers/mock_provider.py`
- `config/container.py`
- Updated generator files
- Architecture diagram

## Related Files

All generator files need to be refactored

## Notes

- 🏗️ Follow SOLID principles (especially Dependency Inversion)
- 🧪 Makes unit testing much easier
- 🔄 Easy to swap implementations
- 📦 Better code organization
- 🎯 Clear separation of concerns

## Next Steps

After completion:
- Easy to unit test all components
- Can mock dependencies for testing
- Easy to add alternative implementations
- Better maintainability
- Reduced coupling

## Related Documentation

- See `docs/RESEARCH_AND_IMPROVEMENTS.md` Section 4
- SOLID principles: https://en.wikipedia.org/wiki/SOLID
