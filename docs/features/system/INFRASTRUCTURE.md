# Infrastructure Documentation

## Overview

This document covers the infrastructure components of the StoryGenerator project:
- Configuration Management
- Logging System
- Testing Infrastructure

## Configuration Management

### Features

- **Type-safe Configuration**: Using pydantic-settings for validation
- **Environment Variables**: Load from `.env` files and environment
- **Path Management**: Automatic directory creation
- **Validation**: Built-in validation for all settings
- **Dev/Prod Configs**: Support for different environments

### Usage

```python
from PrismQ.Shared.config import settings

# Access configuration (settings is already a singleton)
api_key = settings.openai_api_key
model = settings.default_model
story_path = settings.story_root
```

### Configuration Options

| Setting | Type | Default | Description |
|---------|------|---------|-------------|
| `openai_api_key` | str | "" | OpenAI API key |
| `elevenlabs_api_key` | str | "" | ElevenLabs API key |
| `huggingface_token` | str | None | HuggingFace token (optional) |
| `reddit_client_id` | str | None | Reddit client ID (optional) |
| `reddit_client_secret` | str | None | Reddit client secret (optional) |
| `default_model` | str | "gpt-4o-mini" | Default OpenAI model |
| `temperature` | float | 0.9 | Model temperature (0.0-2.0) |
| `max_tokens` | int | 4000 | Maximum tokens |
| `story_root` | Path | "./Stories" | Story storage directory |
| `log_dir` | Path | "./logs" | Log files directory |
| `cache_dir` | Path | "./cache" | Cache directory |
| `voice_id` | str | "BZgkqPqms7Kj9ulSkVzn" | ElevenLabs voice ID |
| `voice_model` | str | "eleven_v3" | ElevenLabs voice model |
| `voice_style` | str | "Creative" | ElevenLabs voice style |
| `log_level` | str | "INFO" | Logging level |
| `enable_cache` | bool | True | Enable caching |
| `max_retries` | int | 3 | Max API retry attempts |
| `cuda_visible_devices` | str | None | GPU device ID(s) |
| `debug` | bool | False | Debug mode |

### Environment Variables

Create a `.env` file in the project root:

```bash
# API Keys
OPENAI_API_KEY=sk-your-key-here
ELEVENLABS_API_KEY=sk-your-key-here

# Model Settings
DEFAULT_MODEL=gpt-4o-mini
TEMPERATURE=0.9
MAX_TOKENS=4000

# Paths
STORY_ROOT=./Stories
LOG_DIR=./logs
CACHE_DIR=./cache

# Logging
LOG_LEVEL=INFO

# Performance
ENABLE_CACHE=true
MAX_RETRIES=3
```

### Testing Configuration

For testing, use the `isolated_config` fixture:

```python
def test_with_config(isolated_config):
    """Test with isolated configuration."""
    settings = get_settings()
    assert settings.story_root.exists()
```

## Logging System

### Features

- **Structured Logging**: Consistent format across application
- **Multiple Handlers**: Console and file output
- **Log Levels**: DEBUG, INFO, WARNING, ERROR, CRITICAL
- **JSON Format**: For production log parsing
- **Request ID Tracking**: For distributed tracing
- **Context Managers**: Add contextual information

### Usage

#### Basic Logging

```python
from PrismQ.Shared.logging import setup_logging, get_logger

# Setup logging (typically in main)
setup_logging(level="INFO")

# Get logger in your module
logger = get_logger(__name__)

# Log messages
logger.debug("Detailed debug information")
logger.info("Informational message")
logger.warning("Warning message")
logger.error("Error occurred", exc_info=True)
logger.critical("Critical issue")
```

#### JSON Logging (Production)

```python
from PrismQ.Shared.logging import setup_logging

# Setup with JSON format for production
setup_logging(
    level="INFO",
    json_format=True,
    console_output=True,
    file_output=True
)
```

#### Contextual Logging

```python
from PrismQ.Shared.logging import get_logger, LoggerContext

logger = get_logger(__name__)

with LoggerContext(logger, request_id="req-123", user_id="user-456"):
    logger.info("Processing request")
    # All logs in this context include request_id and user_id
```

#### Request ID Tracking

```python
setup_logging(
    level="INFO",
    request_id="unique-request-id"
)
```

### Log Levels

- **DEBUG**: Detailed diagnostic information
- **INFO**: General informational messages
- **WARNING**: Warning messages (potential issues)
- **ERROR**: Error messages (failures)
- **CRITICAL**: Critical issues (system failures)

### Log Files

Logs are written to:
- **Console**: Human-readable format
- **File**: `logs/app.log` (human-readable or JSON)

### Configuration

Control logging behavior via environment variables:

```bash
LOG_LEVEL=DEBUG  # Set log level
LOG_DIR=./logs   # Set log directory
```

## Testing Infrastructure

### Running Tests

```bash
# Install test dependencies
pip install -r requirements-dev.txt

# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html --cov-report=term-missing

# Run specific test file
pytest tests/infrastructure/test_config.py

# Run infrastructure tests only
pytest tests/infrastructure/

# Run tests in parallel (faster)
pytest -n auto

# Run with specific markers
pytest -m unit
pytest -m "not slow"
```

### Test Structure

```
tests/
├── conftest.py              # Shared fixtures
├── infrastructure/          # Infrastructure tests
│   ├── test_config.py      # Configuration tests
│   └── test_logging.py     # Logging tests
├── unit/                    # Unit tests
├── integration/             # Integration tests
└── ...
```

### Fixtures Available

#### Standard Fixtures

- `temp_dir`: Temporary directory with cleanup
- `sample_json_file`: Sample JSON file for testing
- `sample_text_file`: Sample text file for testing
- `mock_environment_variables`: Mock environment variables
- `captured_logs`: Capture log output

#### Infrastructure Fixtures

- `mock_openai_client`: Mock OpenAI API client
- `mock_elevenlabs_client`: Mock ElevenLabs API client
- `isolated_config`: Isolated configuration for testing

### Writing Tests

```python
import pytest

class TestMyFeature:
    """Test suite for MyFeature."""
    
    def test_basic_functionality(self):
        """Test basic case."""
        # Arrange
        input_data = "test"
        
        # Act
        result = my_function(input_data)
        
        # Assert
        assert result == "expected"
    
    @pytest.mark.parametrize("input,expected", [
        ("a", "A"),
        ("b", "B"),
    ])
    def test_parameterized(self, input, expected):
        """Test multiple cases."""
        assert my_function(input) == expected
```

### Test Markers

- `@pytest.mark.unit`: Unit test
- `@pytest.mark.integration`: Integration test
- `@pytest.mark.slow`: Slow running test
- `@pytest.mark.requires_api`: Requires API access
- `@pytest.mark.requires_gpu`: Requires GPU

### Coverage Requirements

- **Minimum Coverage**: 70%
- **Target Coverage**: 80%+
- **Infrastructure Coverage**: 98%+

### Mock Providers

Use mock fixtures to avoid real API calls:

```python
def test_with_openai(mock_openai_client):
    """Test OpenAI integration."""
    # Mock already configured with test response
    response = mock_openai_client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": "test"}]
    )
    assert response.choices[0].message.content == "Test response"
```

## Best Practices

### Configuration

1. **Use Environment Variables**: Don't hardcode secrets
2. **Validate Early**: Let pydantic catch configuration errors at startup
3. **Use Defaults**: Provide sensible defaults for non-critical settings
4. **Document Settings**: Add descriptions to all configuration fields
5. **Test Isolation**: Use `isolated_config` fixture in tests

### Logging

1. **Use Appropriate Levels**: DEBUG for details, INFO for normal, WARNING for issues
2. **Include Context**: Add relevant information to log messages
3. **Avoid Secrets**: Never log API keys or sensitive data
4. **Structure Logs**: Use key-value pairs for better parsing
5. **Exception Logging**: Use `exc_info=True` for error logs

### Testing

1. **Write Tests First**: Follow TDD principles
2. **Test Edge Cases**: Consider boundary conditions
3. **Use Fixtures**: Reuse test setup with fixtures
4. **Mock External Calls**: Don't hit real APIs in tests
5. **Maintain Coverage**: Keep coverage above 70%
6. **Fast Tests**: Keep unit tests fast (<1s each)
7. **Clear Names**: Use descriptive test names

## Troubleshooting

### Configuration Issues

**Problem**: Configuration not loading

```bash
# Check .env file exists
ls -la .env

# Verify environment variables
echo $OPENAI_API_KEY

# Test configuration
python -c "from PrismQ.Shared.config import settings; print(settings.openai_api_key)"
```

### Logging Issues

**Problem**: Logs not appearing

```bash
# Check log directory
ls -la logs/

# Verify log level
echo $LOG_LEVEL

# Test logging
python -c "from PrismQ.Shared.logging import setup_logging, get_logger; setup_logging(); get_logger('test').info('Test')"
```

### Testing Issues

**Problem**: Tests failing

```bash
# Verbose output
pytest -vv tests/infrastructure/

# Show print statements
pytest -s tests/infrastructure/

# Debug mode
pytest --pdb tests/infrastructure/

# Coverage details
pytest --cov=src --cov-report=term-missing
```

## See Also

- [TDD Guide](TDD_GUIDE.md)
- [Testing README](../tests/README.md)
- [Issue Templates](../issues/p1-high/)
