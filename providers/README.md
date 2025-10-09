# Providers Package

This package contains concrete implementations of service provider interfaces for the StoryGenerator application.

## Overview

The provider architecture pattern decouples the application from specific service implementations, making it easy to:
- Swap between different service providers
- Mock services for testing
- Add retry logic and error handling centrally
- Follow SOLID principles (especially Dependency Inversion)

## Available Providers

### LLM Providers

#### OpenAIProvider
Synchronous OpenAI API implementation using the new SDK (v1.0+).

```python
from providers import OpenAIProvider

provider = OpenAIProvider(model="gpt-4o-mini")
result = provider.generate_completion("Your prompt here")
```

Features:
- Automatic retry with exponential backoff (3 attempts)
- Comprehensive error handling
- Rate limit management
- Detailed logging

#### AsyncOpenAIProvider
Asynchronous OpenAI API implementation for high-throughput applications.

```python
from providers import AsyncOpenAIProvider

provider = AsyncOpenAIProvider(model="gpt-4o-mini")
result = await provider.generate_completion("Your prompt here")
```

#### MockLLMProvider
Mock provider for testing without making actual API calls.

```python
from providers import MockLLMProvider

provider = MockLLMProvider(response="Test response")
result = provider.generate_completion("Any prompt")
# result == "Test response"
```

Features:
- No API calls required
- Tracks call count and last inputs
- Perfect for unit testing

## Usage Examples

### Basic Usage

```python
from providers import OpenAIProvider

# Initialize with environment variable OPENAI_API_KEY
provider = OpenAIProvider(model="gpt-4o-mini")

# Simple completion
response = provider.generate_completion("Write a haiku about coding")

# Chat completion
messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Hello!"}
]
response = provider.generate_chat(messages, temperature=0.8)
```

### Interface-Based Design

```python
from core.interfaces.llm_provider import ILLMProvider
from providers import OpenAIProvider, MockLLMProvider

def generate_content(provider: ILLMProvider, topic: str) -> str:
    """Works with any LLM provider."""
    return provider.generate_completion(f"Write about {topic}")

# Production
prod_provider = OpenAIProvider()
result = generate_content(prod_provider, "AI")

# Testing
test_provider = MockLLMProvider(response="Test content")
result = generate_content(test_provider, "AI")
```

### Error Handling

```python
from openai import RateLimitError, APIError
from providers import OpenAIProvider

provider = OpenAIProvider()

try:
    result = provider.generate_completion("prompt")
except RateLimitError:
    # Rate limit exceeded after retries
    print("Rate limited - try again later")
except APIError as e:
    # API error from OpenAI
    print(f"API error: {e}")
```

## Configuration

### Environment Variables

```bash
# Required for OpenAI providers
OPENAI_API_KEY=sk-your-key-here

# Optional: default model
DEFAULT_MODEL=gpt-4o-mini
```

### Logging

Enable debug logging to see provider operations:

```python
import logging

logging.basicConfig(level=logging.DEBUG)
```

## Testing

### Unit Tests

Use `MockLLMProvider` for fast, reliable unit tests:

```python
from providers import MockLLMProvider

def test_story_generation():
    provider = MockLLMProvider(response="A test story")
    
    result = generate_story(provider, "robots")
    
    assert result == "A test story"
    assert provider.call_count == 1
```

### Integration Tests

Mark integration tests that require API keys:

```python
import pytest
from providers import OpenAIProvider

@pytest.mark.slow
@pytest.mark.skipif(
    "OPENAI_API_KEY" not in os.environ,
    reason="OPENAI_API_KEY not set"
)
def test_real_api():
    provider = OpenAIProvider()
    result = provider.generate_completion("test")
    assert isinstance(result, str)
```

## Architecture

```
providers/
├── __init__.py              # Package exports
├── openai_provider.py       # OpenAI implementation
├── mock_provider.py         # Mock for testing
└── README.md               # This file

core/interfaces/
└── llm_provider.py         # ILLMProvider interface
```

## Adding New Providers

To add a new provider:

1. Create a new file in `providers/`
2. Implement the `ILLMProvider` or `IAsyncLLMProvider` interface
3. Add error handling and retry logic as needed
4. Export from `__init__.py`
5. Add tests
6. Update documentation

Example:

```python
from core.interfaces.llm_provider import ILLMProvider

class MyProvider(ILLMProvider):
    @property
    def model_name(self) -> str:
        return "my-model"
    
    def generate_completion(self, prompt: str, **kwargs) -> str:
        # Implementation here
        pass
    
    def generate_chat(self, messages: List[Dict], **kwargs) -> str:
        # Implementation here
        pass
```

## See Also

- [Migration Guide](../docs/MIGRATION_GUIDE.md) - Full migration documentation
- [Examples](../examples/provider_architecture_example.py) - Working examples
- [Tests](../tests/test_openai_provider.py) - Test examples
- [Interface Definition](../core/interfaces/llm_provider.py) - Interface contracts
