# Code Quality: Add Comprehensive Error Handling

**ID:** `code-quality-error-handling`  
**Priority:** P1 (High)  
**Effort:** 6-8 hours  
**Status:** Not Started  
**Severity:** MEDIUM

## Overview

The current codebase has insufficient error handling with generic exception catches, no retry logic for API calls, and silent failures. Proper error handling with logging and retry mechanisms is essential for production reliability.

## Current State

### Problems

- ❌ Generic exception catches without proper logging
- ❌ No retry logic for API calls
- ❌ Silent failures in some operations
- ❌ Poor error messages
- ❌ No circuit breaker pattern
- ❌ Errors don't provide actionable information

## Dependencies

**Requires:**
- `architecture-openai-api` - Should update to new API first
- `infrastructure-logging` - Logging should be set up

**Blocks:**
- Production deployment
- Reliable operation

## Acceptance Criteria

### Error Handling
- [ ] Specific exception types for different errors
- [ ] Retry logic with exponential backoff for API calls
- [ ] Proper error logging with context
- [ ] Clear error messages for users
- [ ] Graceful degradation where possible

### API Resilience
- [ ] Automatic retry on rate limits
- [ ] Circuit breaker for repeated failures
- [ ] Timeout handling
- [ ] Network error handling

### Testing
- [ ] Tests for error scenarios
- [ ] Tests for retry logic
- [ ] Tests for timeout handling

## Task Details

### 1. Install Dependencies

```bash
pip install tenacity  # For retry logic
```

Add to `requirements.txt`:
```
tenacity>=8.2.0
```

### 2. Custom Exception Classes

Create `core/exceptions.py`:
```python
class StoryGeneratorError(Exception):
    """Base exception for StoryGenerator."""
    pass

class APIError(StoryGeneratorError):
    """API call failed."""
    pass

class StorageError(StoryGeneratorError):
    """Storage operation failed."""
    pass

class ValidationError(StoryGeneratorError):
    """Input validation failed."""
    pass

class GenerationError(StoryGeneratorError):
    """Content generation failed."""
    pass

class RateLimitError(APIError):
    """API rate limit exceeded."""
    pass
```

### 3. Retry Logic with Tenacity

```python
import logging
from tenacity import (
    retry, 
    stop_after_attempt, 
    wait_exponential,
    retry_if_exception_type,
    before_sleep_log
)
from openai import RateLimitError, APIError as OpenAIAPIError

logger = logging.getLogger(__name__)

class OpenAIProvider:
    @retry(
        retry=retry_if_exception_type((RateLimitError, OpenAIAPIError)),
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10),
        before_sleep=before_sleep_log(logger, logging.WARNING)
    )
    def generate_with_retry(self, messages):
        """Generate with automatic retry on transient errors."""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages
            )
            return response.choices[0].message.content
        
        except RateLimitError as e:
            logger.warning(f"Rate limit exceeded: {e}")
            raise  # Will be retried by tenacity
        
        except OpenAIAPIError as e:
            logger.error(f"OpenAI API error: {e}")
            raise  # Will be retried by tenacity
        
        except Exception as e:
            logger.error(f"Unexpected error: {e}", exc_info=True)
            raise GenerationError(f"Failed to generate content: {e}") from e
```

### 4. Circuit Breaker Pattern

Create `core/circuit_breaker.py`:
```python
from datetime import datetime, timedelta
from enum import Enum
from typing import Callable, Any
import logging

logger = logging.getLogger(__name__)

class CircuitState(Enum):
    CLOSED = "closed"  # Normal operation
    OPEN = "open"      # Failing, reject requests
    HALF_OPEN = "half_open"  # Testing if service recovered

class CircuitBreaker:
    """Circuit breaker to prevent cascading failures."""
    
    def __init__(
        self,
        failure_threshold: int = 5,
        timeout_seconds: int = 60,
        expected_exception: type = Exception
    ):
        self.failure_threshold = failure_threshold
        self.timeout = timedelta(seconds=timeout_seconds)
        self.expected_exception = expected_exception
        
        self.failure_count = 0
        self.last_failure_time = None
        self.state = CircuitState.CLOSED
    
    def call(self, func: Callable, *args, **kwargs) -> Any:
        """Execute function with circuit breaker protection."""
        if self.state == CircuitState.OPEN:
            if datetime.now() - self.last_failure_time > self.timeout:
                self.state = CircuitState.HALF_OPEN
                logger.info("Circuit breaker entering HALF_OPEN state")
            else:
                raise Exception("Circuit breaker is OPEN")
        
        try:
            result = func(*args, **kwargs)
            self._on_success()
            return result
        
        except self.expected_exception as e:
            self._on_failure()
            raise
    
    def _on_success(self):
        """Handle successful call."""
        self.failure_count = 0
        self.state = CircuitState.CLOSED
    
    def _on_failure(self):
        """Handle failed call."""
        self.failure_count += 1
        self.last_failure_time = datetime.now()
        
        if self.failure_count >= self.failure_threshold:
            self.state = CircuitState.OPEN
            logger.error(f"Circuit breaker opened after {self.failure_count} failures")
```

### 5. Timeout Handling

```python
from functools import wraps
import signal

class TimeoutError(Exception):
    pass

def timeout(seconds):
    """Decorator to add timeout to function."""
    def decorator(func):
        def _handle_timeout(signum, frame):
            raise TimeoutError(f"Function {func.__name__} timed out after {seconds}s")
        
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Set alarm
            signal.signal(signal.SIGALRM, _handle_timeout)
            signal.alarm(seconds)
            
            try:
                result = func(*args, **kwargs)
            finally:
                # Cancel alarm
                signal.alarm(0)
            
            return result
        
        return wrapper
    return decorator

# Usage
@timeout(30)
def generate_content(prompt):
    # This will raise TimeoutError if it takes > 30 seconds
    return llm.generate(prompt)
```

### 6. Error Context and Logging

```python
import logging
from contextlib import contextmanager

logger = logging.getLogger(__name__)

@contextmanager
def error_context(operation: str, **context):
    """Context manager for consistent error handling and logging."""
    try:
        logger.info(f"Starting {operation}", extra=context)
        yield
        logger.info(f"Completed {operation}", extra=context)
    
    except Exception as e:
        logger.error(
            f"Error in {operation}: {e}",
            extra=context,
            exc_info=True
        )
        raise

# Usage
with error_context("idea_generation", segment="men_18-23"):
    ideas = generator.generate(prompt)
```

### 7. Validation with Clear Errors

```python
def validate_prompt(prompt: str) -> str:
    """Validate and sanitize prompt."""
    if not prompt:
        raise ValidationError("Prompt cannot be empty")
    
    if len(prompt) > 10000:
        raise ValidationError(f"Prompt too long: {len(prompt)} characters (max 10000)")
    
    if not prompt.strip():
        raise ValidationError("Prompt contains only whitespace")
    
    return prompt.strip()

def validate_output_path(path: Path) -> Path:
    """Validate output path is writable."""
    if path.exists() and not path.is_file():
        raise ValidationError(f"Path exists but is not a file: {path}")
    
    if not os.access(path.parent, os.W_OK):
        raise ValidationError(f"Cannot write to directory: {path.parent}")
    
    return path
```

### 8. Testing Error Handling

Create `tests/test_error_handling.py`:
```python
import pytest
from unittest.mock import Mock, patch
from core.exceptions import APIError, RateLimitError
from providers.openai_provider import OpenAIProvider

def test_retry_on_rate_limit():
    """Test automatic retry on rate limit."""
    provider = OpenAIProvider(api_key="test")
    
    # Mock to fail twice, then succeed
    with patch.object(provider.client.chat.completions, 'create') as mock:
        from openai import RateLimitError as OpenAIRateLimit
        mock.side_effect = [
            OpenAIRateLimit("Rate limit"),
            OpenAIRateLimit("Rate limit"),
            Mock(choices=[Mock(message=Mock(content="Success"))])
        ]
        
        result = provider.generate_with_retry([{"role": "user", "content": "test"}])
        assert result == "Success"
        assert mock.call_count == 3

def test_circuit_breaker_opens():
    """Test circuit breaker opens after failures."""
    cb = CircuitBreaker(failure_threshold=3)
    
    def failing_func():
        raise Exception("Fail")
    
    # Cause 3 failures
    for _ in range(3):
        with pytest.raises(Exception):
            cb.call(failing_func)
    
    # Circuit should be open
    assert cb.state == CircuitState.OPEN
    
    # Next call should be rejected
    with pytest.raises(Exception, match="Circuit breaker is OPEN"):
        cb.call(failing_func)
```

## Output Files

- `core/exceptions.py` - Custom exception classes
- `core/circuit_breaker.py` - Circuit breaker implementation
- Updated provider files with retry logic
- `tests/test_error_handling.py` - Error handling tests

## Related Files

All generator and provider files

## Notes

- 🔄 Always use retry with exponential backoff for API calls
- 📝 Log errors with context for debugging
- 🛡️ Use circuit breaker to prevent cascading failures
- ⏱️ Add timeouts to prevent hanging
- ✅ Validate inputs early

## Next Steps

After completion:
- Reliable API calls with retry
- Better error messages
- Protected against cascading failures
- Production-ready error handling

## Related Documentation

- See `docs/RESEARCH_AND_IMPROVEMENTS.md` Section 5
- Tenacity docs: https://tenacity.readthedocs.io/
