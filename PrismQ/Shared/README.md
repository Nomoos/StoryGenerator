# Shared

Common utilities, interfaces, and models used across all subprojects.

## Purpose

Provides shared functionality that multiple subprojects depend on:
- Configuration management
- Error definitions
- Logging utilities
- Provider interfaces
- Data models
- Caching
- Retry logic
- Validation

## Structure

- **interfaces/** - Provider interfaces (LLM, Platform, Storage, Voice)
- **cache.py** - Caching utilities
- **config.py** - Configuration management
- **database.py** - Database utilities
- **errors.py** - Custom exceptions
- **logging.py** - Logging setup and utilities
- **models.py** - Shared data models
- **platform_comparison.py** - Platform comparison utilities
- **retry.py** - Retry decorators and utilities
- **validation.py** - Validation functions

## Usage

### Common Imports

```python
# Errors and exceptions
from PrismQ.Shared.errors import APIError, ValidationError, RateLimitError

# Logging
from PrismQ.Shared.logging import get_logger, setup_logging
logger = get_logger(__name__)

# Configuration
from PrismQ.Shared.config import settings

# Provider interfaces
from PrismQ.Shared.interfaces.llm_provider import ILLMProvider
from PrismQ.Shared.interfaces.platform_provider import IPlatformProvider
from PrismQ.Shared.interfaces.storage_provider import IStorageProvider
from PrismQ.Shared.interfaces.voice_provider import IVoiceProvider
```

## Design Principle

Everything in `Shared/` should be:
- Stateless or configuration-driven
- Reusable across multiple subprojects
- Well-documented and tested
- Free of subproject-specific logic
