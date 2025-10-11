# Configuration Management System

This document describes the centralized configuration management system for the StoryGenerator application.

## Overview

The configuration system uses Pydantic Settings to provide type-safe, validated configuration with support for environment variables and `.env` files.

## Quick Start

```python
from core.config import settings

# Access configuration values
print(settings.openai_api_key)
print(settings.log_level)
print(settings.story_root)
```

## Configuration Sources

Configuration is loaded in the following order of precedence:

1. **Environment variables** (highest priority)
2. **`.env` file** in the project root
3. **Default values** (lowest priority)

## Configuration Categories

### API Keys

```python
settings.openai_api_key         # OpenAI API key
settings.elevenlabs_api_key     # ElevenLabs API key
settings.reddit_client_id       # Reddit API client ID
settings.reddit_client_secret   # Reddit API client secret
settings.reddit_user_agent      # Reddit API user agent
settings.huggingface_token      # HuggingFace token
```

### Paths

All paths are automatically created if they don't exist.

```python
settings.story_root     # Root directory for stories
settings.data_root      # Root directory for data
settings.cache_dir      # Directory for cached data
settings.logs_dir       # Directory for log files
```

### Logging

```python
settings.log_level      # DEBUG, INFO, WARNING, ERROR, CRITICAL
settings.log_format     # json or text
settings.log_to_file    # Whether to write logs to file
```

### Performance

```python
settings.max_workers        # Maximum worker threads (1-32)
settings.retry_attempts     # Retry attempts for failed operations (1-10)
settings.timeout            # Request timeout in seconds (1-300)
```

### Model Settings

```python
settings.default_model      # Default OpenAI model (e.g., gpt-4o-mini)
settings.temperature        # Model temperature (0.0-2.0)
settings.max_tokens         # Maximum tokens (1-128000)
```

### Voice Settings

```python
settings.voice_id                 # ElevenLabs voice ID
settings.voice_stability          # Voice stability (0.0-1.0)
settings.voice_similarity_boost   # Voice similarity boost (0.0-1.0)
```

### Environment

```python
settings.environment    # development, production, or test
settings.debug          # Enable debug mode
```

## Environment Variables

All settings can be configured via environment variables. Variable names are case-insensitive.

Example `.env` file:

```bash
# API Keys
OPENAI_API_KEY=sk-your-key-here
ELEVENLABS_API_KEY=el-your-key-here
REDDIT_CLIENT_ID=your-reddit-client-id
REDDIT_CLIENT_SECRET=your-reddit-secret

# Paths
STORY_ROOT=./Stories
DATA_ROOT=./data
CACHE_DIR=./cache
LOGS_DIR=./logs

# Logging
LOG_LEVEL=INFO
LOG_FORMAT=text
LOG_TO_FILE=true

# Performance
MAX_WORKERS=4
RETRY_ATTEMPTS=3
TIMEOUT=30

# Model Settings
DEFAULT_MODEL=gpt-4o-mini
TEMPERATURE=0.9
MAX_TOKENS=4000

# Voice Settings
VOICE_ID=BZgkqPqms7Kj9ulSkVzn
VOICE_STABILITY=0.5
VOICE_SIMILARITY_BOOST=0.75

# Environment
ENVIRONMENT=development
DEBUG=false
```

## Validation

The configuration system automatically validates all settings:

- **Log Level**: Must be one of DEBUG, INFO, WARNING, ERROR, CRITICAL
- **Temperature**: Must be between 0.0 and 2.0
- **Max Workers**: Must be between 1 and 32
- **Retry Attempts**: Must be between 1 and 10
- **Timeout**: Must be between 1 and 300 seconds
- **Max Tokens**: Must be between 1 and 128000
- **Voice Settings**: Must be between 0.0 and 1.0

Invalid values will raise a `ValidationError` with a clear error message.

## Helper Methods

```python
# Get numeric log level for Python logging
log_level_int = settings.get_log_level_int()

# Check environment
if settings.is_production():
    # Production-specific code
    pass

if settings.is_development():
    # Development-specific code
    pass

if settings.is_test():
    # Test-specific code
    pass
```

## Usage in Code

### Basic Usage

```python
from core.config import settings

# Use in your code
api_key = settings.openai_api_key
model = settings.default_model
```

### Dependency Injection

```python
from core.config import get_settings

def my_function(config=None):
    if config is None:
        config = get_settings()
    
    # Use config
    print(config.log_level)
```

### Testing

```python
from core.config import Settings

def test_my_feature():
    # Create test settings
    test_settings = Settings(
        openai_api_key="test-key",
        log_level="DEBUG",
        environment="test"
    )
    
    # Use in tests
    assert test_settings.is_test()
```

## Directory Creation

All configured paths are automatically created when settings are loaded:

```python
from core.config import settings

# These directories are guaranteed to exist
assert settings.story_root.exists()
assert settings.data_root.exists()
assert settings.cache_dir.exists()
assert settings.logs_dir.exists()
```

## Best Practices

1. **Never hardcode API keys** - Always use environment variables
2. **Use .env for local development** - Keep .env in .gitignore
3. **Use environment-specific settings** - Set ENVIRONMENT variable appropriately
4. **Validate on startup** - Settings are validated when loaded
5. **Use the singleton** - Import and use the global `settings` instance
6. **Document required settings** - Make it clear which settings are required

## Troubleshooting

### Missing Required Settings

If required API keys are missing, the application will start but API calls will fail. Set appropriate environment variables or add them to your `.env` file.

### Invalid Values

If you provide invalid configuration values, you'll see a clear error message:

```
ValidationError: 1 validation error for Settings
log_level
  log_level must be one of ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'], got 'INVALID'
```

### Path Issues

If directories cannot be created (e.g., permission issues), a warning will be logged but the application will continue. Check file permissions if you see these warnings.

## See Also

- [Pydantic Settings Documentation](https://docs.pydantic.dev/latest/concepts/pydantic_settings/)
- [.env.example](../../.env.example) - Template for environment variables
- [tests/test_core_config.py](../../tests/test_core_config.py) - Test suite
