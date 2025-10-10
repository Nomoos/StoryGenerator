"""
# Error Handling & Retry Logic Guide

This guide covers the error handling patterns and retry logic used in StoryGenerator.

## Table of Contents

- [Quick Start](#quick-start)
- [Exception Hierarchy](#exception-hierarchy)
- [Retry Logic](#retry-logic)
- [Circuit Breaker Pattern](#circuit-breaker-pattern)
- [Best Practices](#best-practices)
- [Examples](#examples)
- [Integration](#integration)
- [Troubleshooting](#troubleshooting)

## Quick Start

### Basic Error Handling

```python
from core.errors import APIError, ValidationError
from core.retry import retry_api_call

# Raise custom exceptions
if not api_key:
    raise ValidationError("API key is required", details={"field": "api_key"})

# Use retry decorator for API calls
@retry_api_call(max_attempts=3)
def call_openai_api(prompt: str):
    response = openai.Completion.create(prompt=prompt)
    if not response:
        raise APIError("OpenAI API returned empty response")
    return response
```

### Circuit Breaker for Failing Services

```python
from core.retry import with_circuit_breaker

@with_circuit_breaker(failure_threshold=5, recovery_timeout=60)
def call_external_service():
    response = requests.get("https://service.example.com/api")
    return response.json()
```

## Exception Hierarchy

All custom exceptions inherit from `StoryGeneratorError`:

### Base Exception

**`StoryGeneratorError`** - Base exception for all errors
- Attributes: `message`, `details`, `original_error`
- Methods: `to_dict()`, `__str__()`

```python
from core.errors import StoryGeneratorError

error = StoryGeneratorError(
    "Operation failed",
    details={"operation": "script_generation", "item_id": "123"},
    original_error=original_exception
)

# Convert to dict for logging
error_dict = error.to_dict()
# {
#     "error_type": "StoryGeneratorError",
#     "message": "Operation failed",
#     "details": {"operation": "script_generation", "item_id": "123"},
#     "original_error": "..."
# }
```

### Input/Output Errors

**`ValidationError`** - Input validation failures
```python
from core.errors import ValidationError

raise ValidationError(
    "Invalid input format",
    details={"field": "email", "value": "invalid", "reason": "missing @"}
)
```

### API Errors

**`APIError`** - External API call failures
- Additional attributes: `status_code`, `retry_after`

```python
from core.errors import APIError

raise APIError(
    "OpenAI API request failed",
    status_code=503,
    retry_after=30,
    details={"endpoint": "/v1/completions"}
)
```

**`RateLimitError`** - Rate limit exceeded (extends APIError)
```python
from core.errors import RateLimitError

raise RateLimitError(
    "OpenAI rate limit exceeded",
    retry_after=120,
    status_code=429
)
```

**`AuthenticationError`** - Authentication/authorization failures (extends APIError)
```python
from core.errors import AuthenticationError

raise AuthenticationError(
    "Invalid API key",
    status_code=401,
    details={"provider": "openai"}
)
```

**`TimeoutError`** - Operation timeouts
```python
from core.errors import TimeoutError

raise TimeoutError(
    "API call timed out after 30s",
    details={"timeout": 30, "endpoint": "/v1/completions"}
)
```

### Processing Errors

**`ProcessingError`** - Pipeline processing failures
- Additional attributes: `stage`, `item_id`

```python
from core.errors import ProcessingError

raise ProcessingError(
    "Script generation failed",
    stage="script_generation",
    item_id="story-123",
    details={"reason": "insufficient context"}
)
```

### Configuration Errors

**`ConfigurationError`** - Configuration issues
```python
from core.errors import ConfigurationError

raise ConfigurationError(
    "Missing required configuration",
    details={"missing_keys": ["OPENAI_API_KEY", "STORY_ROOT"]}
)
```

**`ResourceError`** - Resource unavailability
```python
from core.errors import ResourceError

raise ResourceError(
    "Failed to create output directory",
    details={"path": "/data/output", "reason": "permission denied"}
)
```

## Retry Logic

### Retry with Backoff Decorator

The `retry_with_backoff` decorator provides exponential backoff for transient failures:

```python
from core.retry import retry_with_backoff
from core.errors import APIError

@retry_with_backoff(
    max_attempts=5,           # Maximum retry attempts
    initial_delay=1.0,        # Initial delay in seconds
    max_delay=60.0,           # Maximum delay cap
    exponential_base=2.0,     # Exponential multiplier
    exceptions=(APIError,),   # Exceptions to retry on
)
def call_api():
    response = requests.get("https://api.example.com")
    if not response.ok:
        raise APIError(f"API error: {response.status_code}", status_code=response.status_code)
    return response.json()
```

**Backoff Schedule:**
- Attempt 1: Call immediately
- Attempt 2: Wait 1s (1.0 * 2^0)
- Attempt 3: Wait 2s (1.0 * 2^1)
- Attempt 4: Wait 4s (1.0 * 2^2)
- Attempt 5: Wait 8s (1.0 * 2^3)

**Rate Limit Handling:**
When `RateLimitError` is raised with `retry_after`, the decorator respects it:

```python
@retry_with_backoff(max_attempts=3, initial_delay=1.0)
def rate_limited_call():
    response = requests.get("https://api.example.com")
    if response.status_code == 429:
        retry_after = int(response.headers.get("Retry-After", 60))
        raise RateLimitError("Rate limited", retry_after=retry_after)
    return response.json()
# Will wait the full retry_after time instead of exponential backoff
```

### Retry API Call Convenience Decorator

For standard API calls, use the simplified `retry_api_call` decorator:

```python
from core.retry import retry_api_call

@retry_api_call(max_attempts=3, initial_delay=1.0, max_delay=10.0)
def get_completion(prompt: str):
    response = openai.Completion.create(
        engine="gpt-4",
        prompt=prompt,
        max_tokens=100
    )
    return response

# Automatically retries on APIError, RateLimitError, TimeoutError
```

### Retry Callback

Execute custom logic on each retry:

```python
def log_retry(exc, attempt):
    logger.warning(f"Retry {attempt} due to {exc}")

@retry_with_backoff(
    max_attempts=3,
    initial_delay=1.0,
    on_retry=log_retry
)
def api_call():
    # ...
    pass
```

### Retry Context Manager

For more control, use the `RetryContext` context manager:

```python
from core.retry import RetryContext

while True:
    with RetryContext(max_attempts=3, initial_delay=1.0) as retry:
        response = requests.get("https://api.example.com")
        
        if response.status_code == 429:
            retry.should_retry()  # Mark for retry
            continue
        
        if not response.ok:
            raise APIError(f"API error: {response.status_code}")
        
        data = response.json()
        break  # Success, exit retry loop

# Use data here
```

## Circuit Breaker Pattern

Circuit breakers prevent repeated calls to failing services:

### Circuit Breaker States

1. **CLOSED** (Normal): All calls pass through
2. **OPEN** (Failing): Calls fail immediately without attempting
3. **HALF_OPEN** (Testing): Test call to check if service recovered

### Using the Circuit Breaker

```python
from core.retry import with_circuit_breaker, CircuitBreaker

@with_circuit_breaker(
    failure_threshold=5,      # Open after 5 failures
    recovery_timeout=60,      # Test recovery after 60s
    expected_exception=APIError,  # Count these as failures
)
def call_unstable_service():
    response = requests.get("https://unstable-service.com")
    if not response.ok:
        raise APIError(f"Service error: {response.status_code}")
    return response.json()
```

**How it works:**
1. Service starts working normally (CLOSED)
2. After 5 consecutive failures, circuit opens (OPEN)
3. For next 60 seconds, all calls fail immediately
4. After 60 seconds, circuit half-opens (HALF_OPEN)
5. Next call is attempted
   - If successful: Circuit closes, back to normal
   - If failed: Circuit reopens for another 60 seconds

### Manual Circuit Breaker

For more control, use the CircuitBreaker class directly:

```python
from core.retry import CircuitBreaker

cb = CircuitBreaker(failure_threshold=3, recovery_timeout=30)

def my_function():
    response = requests.get("https://service.com")
    return response.json()

try:
    result = cb.call(my_function)
except Exception as e:
    print(f"Call failed or circuit is open: {e}")
```

## Best Practices

### 1. Use Appropriate Exception Types

```python
# Good: Specific exception with details
raise ValidationError(
    "Invalid story ID format",
    details={"id": story_id, "expected": "alphanumeric"}
)

# Bad: Generic exception
raise Exception("Invalid ID")
```

### 2. Include Context in Errors

```python
# Good: Rich context for debugging
raise ProcessingError(
    "Failed to generate script",
    stage="script_generation",
    item_id=story.id,
    details={
        "story_title": story.title,
        "attempt": 3,
        "reason": "timeout"
    }
)

# Bad: Minimal information
raise ProcessingError("Failed")
```

### 3. Wrap External Errors

```python
# Good: Wrap and preserve original error
try:
    response = openai.Completion.create(prompt=prompt)
except openai.error.APIError as e:
    raise APIError(
        "OpenAI API call failed",
        original_error=e,
        details={"prompt_length": len(prompt)}
    )

# Bad: Lose original error context
except openai.error.APIError:
    raise APIError("API failed")
```

### 4. Combine Retry and Circuit Breaker

```python
# For critical external services, use both
@with_circuit_breaker(failure_threshold=5)
@retry_with_backoff(max_attempts=3)
def critical_api_call():
    # Retry individual failures
    # Circuit breaker prevents cascade failures
    return api.call()
```

### 5. Log Errors Appropriately

```python
from core.logging import get_logger

logger = get_logger(__name__)

try:
    result = process_story(story)
except ProcessingError as e:
    logger.error(
        "Story processing failed",
        extra=e.to_dict()  # Log structured error data
    )
    raise
```

## Examples

### Example 1: OpenAI API Call with Full Error Handling

```python
from core.errors import APIError, RateLimitError, AuthenticationError
from core.retry import retry_with_backoff, with_circuit_breaker
from core.logging import get_logger

logger = get_logger(__name__)

@with_circuit_breaker(failure_threshold=5, recovery_timeout=120)
@retry_with_backoff(max_attempts=3, initial_delay=2.0, max_delay=30.0)
def generate_completion(prompt: str, max_tokens: int = 100) -> str:
    """Generate completion with robust error handling."""
    try:
        response = openai.Completion.create(
            engine="gpt-4",
            prompt=prompt,
            max_tokens=max_tokens,
            timeout=30
        )
        return response.choices[0].text
    
    except openai.error.RateLimitError as e:
        retry_after = 60  # Default retry time
        raise RateLimitError(
            "OpenAI rate limit exceeded",
            retry_after=retry_after,
            original_error=e
        )
    
    except openai.error.AuthenticationError as e:
        raise AuthenticationError(
            "OpenAI authentication failed - check API key",
            status_code=401,
            original_error=e
        )
    
    except openai.error.Timeout as e:
        raise APIError(
            "OpenAI request timed out",
            details={"timeout": 30},
            original_error=e
        )
    
    except openai.error.APIError as e:
        raise APIError(
            "OpenAI API error",
            original_error=e,
            details={"prompt_length": len(prompt)}
        )
```

### Example 2: Processing Pipeline with Error Handling

```python
from core.errors import ProcessingError, ValidationError
from core.logging import get_logger, log_context

logger = get_logger(__name__)

def process_story_pipeline(story_id: str) -> dict:
    """Process story through pipeline with error handling."""
    with log_context(story_id=story_id, stage="pipeline"):
        try:
            # Validate input
            story = get_story(story_id)
            if not story:
                raise ValidationError(
                    "Story not found",
                    details={"story_id": story_id}
                )
            
            # Generate script
            try:
                script = generate_script(story)
            except Exception as e:
                raise ProcessingError(
                    "Script generation failed",
                    stage="script_generation",
                    item_id=story_id,
                    original_error=e
                )
            
            # Generate audio
            try:
                audio = generate_audio(script)
            except Exception as e:
                raise ProcessingError(
                    "Audio generation failed",
                    stage="audio_generation",
                    item_id=story_id,
                    original_error=e,
                    details={"script_length": len(script)}
                )
            
            logger.info(f"Successfully processed story {story_id}")
            return {"script": script, "audio": audio}
        
        except ProcessingError as e:
            logger.error(
                "Pipeline processing failed",
                extra=e.to_dict()
            )
            raise
```

### Example 3: Graceful Degradation

```python
from core.errors import APIError
from core.retry import retry_api_call

@retry_api_call(max_attempts=2)
def get_enhanced_title(title: str) -> str:
    """Get enhanced title from API with fallback."""
    try:
        response = openai.Completion.create(
            prompt=f"Improve this title: {title}",
            max_tokens=50
        )
        return response.choices[0].text.strip()
    except APIError as e:
        logger.warning(
            f"Failed to enhance title, using original",
            extra={"error": str(e)}
        )
        # Graceful degradation: return original title
        return title
```

## Integration

### With Configuration System

```python
from core.config import settings
from core.errors import ConfigurationError

def validate_configuration():
    """Validate required configuration."""
    if not settings.openai_api_key:
        raise ConfigurationError(
            "OpenAI API key not configured",
            details={"required_env_var": "OPENAI_API_KEY"}
        )
    
    if not settings.story_root.exists():
        raise ConfigurationError(
            "Story root directory does not exist",
            details={"path": str(settings.story_root)}
        )
```

### With Logging System

```python
from core.logging import get_logger
from core.errors import StoryGeneratorError

logger = get_logger(__name__)

try:
    result = risky_operation()
except StoryGeneratorError as e:
    # Log structured error data
    logger.error(
        "Operation failed",
        extra=e.to_dict()
    )
    raise
```

### With Validation System

```python
from core.validation import validate_input
from core.models import StoryIdea
from core.errors import ValidationError as CoreValidationError
from pydantic import ValidationError as PydanticValidationError

@validate_input(idea=StoryIdea)
def process_idea(idea: StoryIdea):
    try:
        # Processing logic
        pass
    except PydanticValidationError as e:
        # Convert Pydantic error to our ValidationError
        raise CoreValidationError(
            "Input validation failed",
            details={"errors": e.errors()},
            original_error=e
        )
```

## Troubleshooting

### Issue: Too Many Retries

**Problem:** Functions retry too many times, causing slow failures.

**Solution:** Reduce `max_attempts` or increase `initial_delay`:
```python
@retry_with_backoff(max_attempts=2, initial_delay=5.0)
def quick_fail_api_call():
    # ...
```

### Issue: Circuit Breaker Opens Too Quickly

**Problem:** Circuit breaker opens after few transient errors.

**Solution:** Increase `failure_threshold`:
```python
@with_circuit_breaker(failure_threshold=10, recovery_timeout=60)
def tolerant_service_call():
    # ...
```

### Issue: Not Catching Specific Errors

**Problem:** Retry catching wrong exception types.

**Solution:** Specify exact exceptions:
```python
@retry_with_backoff(
    max_attempts=3,
    exceptions=(APIError, RateLimitError)  # Only retry these
)
def specific_retry():
    # ...
```

### Issue: Lost Error Context

**Problem:** Error context lost when wrapping exceptions.

**Solution:** Always include `original_error`:
```python
try:
    external_call()
except ExternalError as e:
    raise APIError(
        "External call failed",
        original_error=e,  # Preserve original
        details={"context": "..."}
    )
```

## Additional Resources

- [Core Configuration](CONFIG_README.md)
- [Logging System](LOGGING_README.md)
- [Testing Guide](../tests/TESTING_GUIDE.md)
- [tenacity library docs](https://tenacity.readthedocs.io/)
"""
