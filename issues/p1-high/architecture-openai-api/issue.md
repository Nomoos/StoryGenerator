# Architecture: Update Deprecated OpenAI API Usage

**ID:** `architecture-openai-api`  
**Priority:** P1 (High)  
**Effort:** 2-3 hours  
**Status:** Not Started  
**Severity:** MEDIUM

## Overview

The codebase uses the deprecated OpenAI API format (`openai.ChatCompletion.create`). OpenAI has released a new SDK with a cleaner, more maintainable API. Updating to the new format ensures future compatibility and access to new features.

## Current State

### Deprecated API Usage

```python
response = openai.ChatCompletion.create(
    model=self.model,
    messages=messages
)
```

### Problems

- ❌ Uses deprecated OpenAI SDK methods
- ❌ Will break with future SDK updates
- ❌ Missing access to new features
- ❌ Inconsistent error handling
- ❌ Technical debt accumulation

## Dependencies

**Requires:**
- `security-api-keys` - API keys must be in environment variables first

**Blocks:**
- None (but recommended before expanding AI features)

## Acceptance Criteria

### Code Updates
- [ ] Update to latest OpenAI SDK (v1.0+)
- [ ] Replace all `openai.ChatCompletion.create` calls
- [ ] Replace all `openai.Completion.create` calls
- [ ] Use new client-based API
- [ ] Update error handling for new exception types

### Testing
- [ ] All existing tests pass with new API
- [ ] Test error handling with new exceptions
- [ ] Verify API responses match expected format
- [ ] Test rate limiting behavior

### Documentation
- [ ] Update code comments with new API usage
- [ ] Document migration in MIGRATION_GUIDE.md
- [ ] Update README with SDK version requirements

## Task Details

### 1. Update Requirements

```bash
# requirements.txt
openai>=1.0.0  # Update from older version
```

Install:
```bash
pip install --upgrade openai
```

### 2. Create OpenAI Client Wrapper

Create `providers/openai_provider.py`:

```python
import os
from openai import OpenAI, AsyncOpenAI
from typing import List, Dict, Optional
import logging

logger = logging.getLogger(__name__)

class OpenAIProvider:
    """Wrapper for OpenAI API using new SDK."""
    
    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-4o-mini"):
        """
        Initialize OpenAI provider.
        
        Args:
            api_key: OpenAI API key (defaults to OPENAI_API_KEY env var)
            model: Model to use for completions
        """
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        if not self.api_key:
            raise ValueError("OpenAI API key is required")
        
        self.model = model
        self.client = OpenAI(api_key=self.api_key)
    
    def chat_completion(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: Optional[int] = None
    ) -> str:
        """
        Generate chat completion.
        
        Args:
            messages: List of message dicts with 'role' and 'content'
            temperature: Sampling temperature (0-2)
            max_tokens: Maximum tokens in response
        
        Returns:
            Generated text content
        """
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens
            )
            return response.choices[0].message.content
        
        except Exception as e:
            logger.error(f"OpenAI API error: {e}")
            raise

class AsyncOpenAIProvider:
    """Async wrapper for OpenAI API."""
    
    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-4o-mini"):
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        if not self.api_key:
            raise ValueError("OpenAI API key is required")
        
        self.model = model
        self.client = AsyncOpenAI(api_key=self.api_key)
    
    async def chat_completion(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: Optional[int] = None
    ) -> str:
        """Async chat completion."""
        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens
            )
            return response.choices[0].message.content
        
        except Exception as e:
            logger.error(f"OpenAI API error: {e}")
            raise
```

### 3. Update Generator Files

**Before (Deprecated):**
```python
import openai

openai.api_key = "sk-..."  # Hardcoded

response = openai.ChatCompletion.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "user", "content": prompt}
    ]
)
result = response.choices[0].message.content
```

**After (New API):**
```python
from providers.openai_provider import OpenAIProvider

provider = OpenAIProvider(model="gpt-4o-mini")

messages = [
    {"role": "user", "content": prompt}
]
result = provider.chat_completion(messages)
```

### Files to Update

1. `Generators/GStoryIdeas.py`
2. `Generators/GScript.py`
3. `Generators/GRevise.py`
4. `Generators/GEnhanceScript.py`
5. Any other files using OpenAI API

### 4. Update Error Handling

**Old exceptions:**
```python
try:
    response = openai.ChatCompletion.create(...)
except openai.error.RateLimitError:
    # Handle rate limit
except openai.error.APIError:
    # Handle API error
```

**New exceptions:**
```python
from openai import OpenAIError, RateLimitError, APIError

try:
    result = provider.chat_completion(...)
except RateLimitError as e:
    logger.warning(f"Rate limit hit: {e}")
    # Handle rate limit with retry
except APIError as e:
    logger.error(f"API error: {e}")
    raise
except OpenAIError as e:
    logger.error(f"OpenAI error: {e}")
    raise
```

### 5. Add Retry Logic

```python
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

class OpenAIProvider:
    @retry(
        retry=retry_if_exception_type(RateLimitError),
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10)
    )
    def chat_completion(self, messages: List[Dict[str, str]], **kwargs) -> str:
        """Chat completion with automatic retry on rate limits."""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                **kwargs
            )
            return response.choices[0].message.content
        except RateLimitError:
            logger.warning("Rate limit hit, retrying...")
            raise  # Will be retried by tenacity
```

### 6. Testing

Create `tests/test_openai_provider.py`:
```python
import pytest
from unittest.mock import Mock, patch
from providers.openai_provider import OpenAIProvider

@pytest.fixture
def provider():
    return OpenAIProvider(api_key="test-key", model="gpt-4o-mini")

def test_provider_initialization(provider):
    """Test provider initializes correctly."""
    assert provider.model == "gpt-4o-mini"
    assert provider.client is not None

def test_chat_completion_success(provider):
    """Test successful chat completion."""
    with patch.object(provider.client.chat.completions, 'create') as mock_create:
        # Mock response
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "Test response"
        mock_create.return_value = mock_response
        
        messages = [{"role": "user", "content": "Test prompt"}]
        result = provider.chat_completion(messages)
        
        assert result == "Test response"
        mock_create.assert_called_once()

def test_chat_completion_error(provider):
    """Test error handling."""
    with patch.object(provider.client.chat.completions, 'create') as mock_create:
        from openai import APIError
        mock_create.side_effect = APIError("Test error")
        
        messages = [{"role": "user", "content": "Test"}]
        with pytest.raises(APIError):
            provider.chat_completion(messages)
```

Run tests:
```bash
python -m pytest tests/test_openai_provider.py -v
```

## Output Files

- New `providers/openai_provider.py` - OpenAI client wrapper
- Updated generator files - Using new API
- New `tests/test_openai_provider.py` - Provider tests
- Updated `requirements.txt` - OpenAI SDK v1.0+
- Updated `docs/MIGRATION_GUIDE.md` - API migration notes

## Related Files

- `Generators/GStoryIdeas.py`
- `Generators/GScript.py`
- `Generators/GRevise.py`
- `Generators/GEnhanceScript.py`
- `requirements.txt`

## Migration Checklist

- [ ] Update OpenAI SDK to v1.0+
- [ ] Create OpenAIProvider wrapper
- [ ] Update GStoryIdeas.py
- [ ] Update GScript.py
- [ ] Update GRevise.py
- [ ] Update GEnhanceScript.py
- [ ] Update error handling
- [ ] Add retry logic
- [ ] Write tests
- [ ] Run all tests
- [ ] Update documentation

## Notes

- 📦 OpenAI SDK v1.0+ is a breaking change from previous versions
- 🔄 New API uses client-based pattern (more Pythonic)
- ⚡ Better async support in new SDK
- 🔧 Improved error handling with specific exception types
- 📝 Better type hints and IDE support

## Benefits of Update

- ✅ Future-proof code
- ✅ Access to new features
- ✅ Better error handling
- ✅ Improved async support
- ✅ Better type hints
- ✅ Active SDK maintenance

## Next Steps

After completion:
- All OpenAI API calls use new SDK
- Better error handling and retry logic
- Ready for new OpenAI features
- Reduced technical debt

## Related Documentation

- See `docs/RESEARCH_AND_IMPROVEMENTS.md` Section 3
- OpenAI SDK migration guide: https://github.com/openai/openai-python/discussions/742
- OpenAI SDK documentation: https://platform.openai.com/docs/api-reference
