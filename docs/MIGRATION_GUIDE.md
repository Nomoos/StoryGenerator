# OpenAI API Migration Guide

## Overview

This guide documents the migration from the deprecated OpenAI API (pre-v1.0) to the new OpenAI SDK (v1.0+) and the introduction of the provider architecture pattern.

## Changes Made

### 1. OpenAI SDK Update

**Before (Deprecated API):**
```python
import openai

openai.api_key = "sk-..."  # Hardcoded or from env

response = openai.ChatCompletion.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "user", "content": prompt}
    ]
)
result = response.choices[0].message.content
```

**After (New SDK v1.0+):**
```python
from openai import OpenAI

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "user", "content": prompt}
    ]
)
result = response.choices[0].message.content
```

### 2. Provider Architecture Pattern

We've introduced a provider architecture pattern that decouples the application from specific LLM implementations. This makes it easy to:
- Swap between different LLM providers
- Mock providers for testing
- Add retry logic and error handling in one place
- Follow SOLID principles (Dependency Inversion)

**Using the Provider (Recommended):**
```python
from providers import OpenAIProvider

# Initialize provider (reads from OPENAI_API_KEY env var)
provider = OpenAIProvider(model="gpt-4o-mini")

# Simple completion
result = provider.generate_completion("Your prompt here")

# Chat completion
messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Hello!"}
]
result = provider.generate_chat(messages)

# With custom parameters
result = provider.generate_chat(
    messages,
    temperature=0.9,
    max_tokens=1000
)
```

**Async Usage:**
```python
from providers import AsyncOpenAIProvider

provider = AsyncOpenAIProvider(model="gpt-4o-mini")

# Async completion
result = await provider.generate_completion("Your prompt here")

# Async chat
result = await provider.generate_chat(messages)
```

### 3. Interface-Based Design

All providers implement the `ILLMProvider` interface, which defines a standard contract:

```python
from core.interfaces.llm_provider import ILLMProvider
from providers import OpenAIProvider, MockLLMProvider

def generate_story(provider: ILLMProvider, topic: str) -> str:
    """Generate a story using any LLM provider."""
    prompt = f"Write a short story about {topic}"
    return provider.generate_completion(prompt)

# Use with OpenAI
openai_provider = OpenAIProvider()
story = generate_story(openai_provider, "a robot")

# Use with mock for testing
mock_provider = MockLLMProvider(response="Test story")
story = generate_story(mock_provider, "a robot")
```

## Key Features

### Automatic Retry Logic

The OpenAI provider includes automatic retry logic for rate limits and connection errors:
- 3 retry attempts
- Exponential backoff (4-10 seconds)
- Retries on `RateLimitError` and `APIConnectionError`

### Comprehensive Error Handling

```python
from openai import RateLimitError, APIError
from providers import OpenAIProvider

provider = OpenAIProvider()

try:
    result = provider.generate_completion("prompt")
except RateLimitError as e:
    # Rate limit exceeded after retries
    print(f"Rate limited: {e}")
except APIError as e:
    # API error from OpenAI
    print(f"API error: {e}")
```

### Logging

All provider operations are logged:
- INFO: Initialization
- DEBUG: API calls and responses
- WARNING: Retries
- ERROR: Failures

```python
import logging

# Enable debug logging to see all provider operations
logging.basicConfig(level=logging.DEBUG)
```

## Testing

### Unit Tests with Mock Provider

```python
from providers import MockLLMProvider

def test_story_generation():
    # Use mock provider for testing
    provider = MockLLMProvider(response="Test story content")
    
    result = generate_story(provider, "robots")
    
    assert result == "Test story content"
    assert provider.call_count == 1
    assert "robots" in provider.last_prompt
```

### Integration Tests

```python
import pytest
from providers import OpenAIProvider

@pytest.mark.slow
@pytest.mark.skipif(
    "OPENAI_API_KEY" not in os.environ,
    reason="OPENAI_API_KEY not set"
)
def test_real_api_call():
    provider = OpenAIProvider()
    result = provider.generate_completion("Say 'test'")
    assert isinstance(result, str)
    assert len(result) > 0
```

## Migration Checklist

For migrating existing code to use the new provider pattern:

- [ ] Install OpenAI SDK v1.0+ (`pip install --upgrade openai>=1.0.0`)
- [ ] Install retry library (`pip install tenacity`)
- [ ] Update imports from `import openai` to `from providers import OpenAIProvider`
- [ ] Replace `openai.ChatCompletion.create()` with `provider.generate_chat()`
- [ ] Replace `openai.Completion.create()` with `provider.generate_completion()`
- [ ] Update error handling for new exception types
- [ ] Update tests to use `MockLLMProvider`
- [ ] Verify environment variable `OPENAI_API_KEY` is set
- [ ] Run tests to verify migration

## Environment Setup

Ensure you have the OpenAI API key set in your environment:

```bash
# .env file
OPENAI_API_KEY=sk-your-key-here

# Or export in shell
export OPENAI_API_KEY=sk-your-key-here
```

## Benefits of Migration

✅ **Future-proof**: Uses the latest OpenAI SDK with ongoing support  
✅ **Better error handling**: Automatic retry logic and comprehensive error catching  
✅ **Easier testing**: Mock providers eliminate need for API calls in tests  
✅ **Decoupled**: Easy to swap between different LLM providers  
✅ **Type hints**: Better IDE support and type checking  
✅ **Logging**: Built-in logging for debugging and monitoring  
✅ **SOLID principles**: Clean architecture following best practices

## Example: Complete Migration

**Before:**
```python
# old_code.py
import openai

openai.api_key = os.getenv('OPENAI_API_KEY')

def generate_story_idea(topic: str) -> str:
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": f"Generate a story idea about {topic}"}
        ]
    )
    return response.choices[0].message.content
```

**After:**
```python
# new_code.py
from providers import OpenAIProvider
from core.interfaces.llm_provider import ILLMProvider

class StoryGenerator:
    def __init__(self, llm_provider: ILLMProvider):
        self.llm = llm_provider
    
    def generate_story_idea(self, topic: str) -> str:
        prompt = f"Generate a story idea about {topic}"
        return self.llm.generate_completion(prompt)

# Production usage
generator = StoryGenerator(OpenAIProvider(model="gpt-4o-mini"))
idea = generator.generate_story_idea("robots")

# Testing
from providers import MockLLMProvider

mock_provider = MockLLMProvider(response="Test story idea")
test_generator = StoryGenerator(mock_provider)
test_idea = test_generator.generate_story_idea("robots")
assert test_idea == "Test story idea"
```

## Support

For issues or questions:
1. Check the [OpenAI Python SDK documentation](https://github.com/openai/openai-python)
2. Review the provider source code in `providers/openai_provider.py`
3. Check the tests in `tests/test_openai_provider.py` for examples
4. Consult the interface definitions in `core/interfaces/llm_provider.py`

## Version Information

- **OpenAI SDK**: v1.50.2+
- **Python**: 3.10+
- **Tenacity** (retry library): Latest
