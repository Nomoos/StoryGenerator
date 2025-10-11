# Architecture Documentation

## Overview

The StoryGenerator project has implemented a modern, maintainable architecture following SOLID principles and best practices. This document describes the architecture patterns, components, and design decisions.

## Architecture Principles

### 1. Dependency Inversion Principle (DIP)

High-level modules (application logic) depend on abstractions (interfaces), not on low-level modules (concrete implementations).

```
┌─────────────────────┐
│  Application Logic  │
└──────────┬──────────┘
           │ depends on
           ▼
┌─────────────────────┐
│   ILLMProvider      │  (Interface)
└──────────┬──────────┘
           │ implemented by
           ▼
┌─────────────────────┐
│  OpenAIProvider     │  (Concrete Implementation)
└─────────────────────┘
```

### 2. Open/Closed Principle (OCP)

The system is open for extension but closed for modification. New providers can be added without changing existing code.

### 3. Single Responsibility Principle (SRP)

Each component has a single, well-defined responsibility:
- **Interfaces**: Define contracts
- **Providers**: Implement external service integrations
- **Tests**: Verify behavior
- **Documentation**: Guide users

## Architecture Diagram

```
StoryGenerator/
│
├── core/                           # Core abstractions and business logic
│   ├── interfaces/                 # Abstract interfaces (contracts)
│   │   ├── llm_provider.py        # ILLMProvider, IAsyncLLMProvider
│   │   ├── storage_provider.py    # [Future] IStorageProvider
│   │   └── voice_provider.py      # [Future] IVoiceProvider
│   │
│   └── models/                     # [Future] Domain models
│       ├── story_idea.py
│       ├── script.py
│       └── voice_config.py
│
├── PrismQ/Providers/                      # Concrete implementations
│   ├── openai_provider.py         # OpenAI LLM implementation
│   ├── mock_provider.py           # Mock for testing
│   ├── elevenlabs_provider.py     # [Future] Voice synthesis
│   └── file_storage.py            # [Future] File operations
│
├── tests/                          # Test suite
│   └── test_openai_provider.py    # Provider tests (26 tests)
│
├── examples/                       # Usage examples
│   └── provider_architecture_example.py
│
└── docs/                           # Documentation
    ├── MIGRATION_GUIDE.md         # Migration from old API
    └── ARCHITECTURE.md            # This file
```

## Component Details

### Core Interfaces

#### ILLMProvider
Abstract interface for synchronous Language Model providers.

**Methods:**
- `generate_completion(prompt, **kwargs) -> str`: Single prompt completion
- `generate_chat(messages, **kwargs) -> str`: Chat-based completion
- `model_name: str`: Property returning model name

**Benefits:**
- Consistent API across all LLM providers
- Easy to swap implementations
- Mockable for testing
- Type-safe with proper hints

#### IAsyncLLMProvider
Async variant of ILLMProvider for high-throughput applications.

### Provider Implementations

#### OpenAIProvider
Production-ready OpenAI implementation with:
- ✅ Automatic retry logic (3 attempts)
- ✅ Exponential backoff (4-10 seconds)
- ✅ Comprehensive error handling
- ✅ Rate limit management
- ✅ Detailed logging
- ✅ Type hints throughout

```python
from PrismQ.Providers import OpenAIProvider

provider = OpenAIProvider(model="gpt-4o-mini")
result = provider.generate_completion("Your prompt")
```

#### MockLLMProvider
Testing-focused implementation with:
- ✅ No API calls required
- ✅ Predictable, deterministic responses
- ✅ Call tracking for verification
- ✅ Fast test execution

```python
from PrismQ.Providers import MockLLMProvider

provider = MockLLMProvider(response="Test response")
result = provider.generate_completion("Any prompt")
assert result == "Test response"
assert provider.call_count == 1
```

## Design Patterns

### 1. Strategy Pattern

The provider architecture implements the Strategy pattern, allowing algorithms (LLM providers) to be selected at runtime.

```python
def generate_content(provider: ILLMProvider, topic: str) -> str:
    """Strategy: accepts any provider implementation."""
    return provider.generate_completion(f"Write about {topic}")

# Strategy 1: OpenAI
openai_provider = OpenAIProvider()
result = generate_content(openai_provider, "AI")

# Strategy 2: Mock (for testing)
mock_provider = MockLLMProvider(response="Test content")
result = generate_content(mock_provider, "AI")
```

### 2. Decorator Pattern (Retry Logic)

The `@retry` decorator wraps methods to add retry behavior without modifying core logic.

```python
@retry(
    retry=retry_if_exception_type((RateLimitError, APIConnectionError)),
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=4, max=10),
)
def chat_completion(self, messages, **kwargs):
    # Core logic here
    pass
```

## Error Handling Architecture

### Retry Strategy

```
API Call
   │
   ├─ Success ────────────────────────► Return Result
   │
   └─ RateLimitError or ConnectionError
         │
         ├─ Attempt 1 ─► Wait 4s ─► Retry
         │
         ├─ Attempt 2 ─► Wait 8s ─► Retry
         │
         └─ Attempt 3 ─► Wait 10s ─► Retry
               │
               ├─ Success ─────────► Return Result
               │
               └─ Still Fails ─────► Raise RetryError
```

### Error Hierarchy

```
Exception
   │
   ├─ OpenAIError                  # Base OpenAI exception
   │    ├─ APIError                # API errors
   │    ├─ RateLimitError         # Rate limiting (retryable)
   │    └─ APIConnectionError      # Network errors (retryable)
   │
   └─ tenacity.RetryError          # Max retries exceeded
```

## Best Practices

### 1. Always Use Interfaces

```python
# Good: Depends on interface
def process(provider: ILLMProvider):
    return provider.generate_completion("prompt")

# Bad: Depends on concrete implementation
def process(provider: OpenAIProvider):
    return provider.generate_completion("prompt")
```

### 2. Use Mock Providers for Testing

```python
# Good: Fast, reliable tests
def test_feature():
    provider = MockLLMProvider(response="Expected")
    result = feature(provider)
    assert result == "Expected"

# Bad: Slow, unreliable tests
def test_feature():
    provider = OpenAIProvider()  # Makes real API calls!
    result = feature(provider)
```

## References

- [SOLID Principles](https://en.wikipedia.org/wiki/SOLID)
- [OpenAI Python SDK](https://github.com/openai/openai-python)
- [Tenacity Retry Library](https://tenacity.readthedocs.io/)
- [Python Type Hints](https://docs.python.org/3/library/typing.html)
