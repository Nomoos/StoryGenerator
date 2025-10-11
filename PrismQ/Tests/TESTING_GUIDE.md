# Testing Guide

This document provides comprehensive guidelines for testing in the StoryGenerator project.

## Overview

The project uses **pytest** as its testing framework with comprehensive coverage reporting, fixtures, and mocking capabilities.

## Quick Start

```bash
# Run all tests
pytest

# Run with coverage report
pytest --cov

# Run specific test file
pytest tests/test_config.py

# Run specific test function
pytest tests/test_config.py::TestSettings::test_default_values

# Run tests matching a pattern
pytest -k "config"

# Run tests with specific marker
pytest -m unit
pytest -m integration
pytest -m "not slow"
```

## Test Organization

### Directory Structure

```
tests/
├── conftest.py              # Shared fixtures and configuration
├── mocks/                   # Mock providers for testing
│   ├── __init__.py
│   ├── mock_openai_provider.py
│   └── mock_elevenlabs_provider.py
├── infrastructure/          # Infrastructure tests
│   ├── test_config.py
│   └── test_logging.py
├── PrismQ/Pipeline/                # Pipeline tests
└── test_*.py               # Top-level test modules
```

### Test Markers

Tests are categorized using pytest markers:

- `@pytest.mark.unit` - Unit tests (fast, isolated)
- `@pytest.mark.integration` - Integration tests (slower, may use external services)
- `@pytest.mark.slow` - Slow-running tests
- `@pytest.mark.requires_api` - Tests requiring API access
- `@pytest.mark.requires_gpu` - Tests requiring GPU

**Example:**

```python
@pytest.mark.unit
def test_configuration_defaults():
    # Fast unit test
    pass

@pytest.mark.integration
@pytest.mark.requires_api
def test_openai_integration():
    # Integration test requiring API key
    pass
```

## Writing Tests

### Test Structure

Follow the **Arrange-Act-Assert** pattern:

```python
def test_example():
    # Arrange - Set up test data and conditions
    config = Settings(log_level="DEBUG")
    
    # Act - Perform the action being tested
    result = config.get_log_level_int()
    
    # Assert - Verify the results
    assert result == logging.DEBUG
```

### Naming Conventions

- Test files: `test_*.py`
- Test classes: `Test*`
- Test functions: `test_*`

**Examples:**

```python
# Good names
def test_config_loads_from_environment()
def test_logger_creates_log_file()
def test_openai_provider_handles_rate_limit()

# Avoid vague names
def test_config()
def test_logger()
def test_api()
```

### Test Classes

Group related tests in classes:

```python
class TestConfiguration:
    """Test configuration management."""
    
    def test_default_values(self):
        """Test that default values are set correctly."""
        settings = Settings()
        assert settings.log_level == "INFO"
    
    def test_environment_override(self, monkeypatch):
        """Test that environment variables override defaults."""
        monkeypatch.setenv("LOG_LEVEL", "DEBUG")
        settings = Settings()
        assert settings.log_level == "DEBUG"
```

## Fixtures

### Using Built-in Fixtures

```python
def test_with_temp_directory(temp_dir):
    """Use temp_dir fixture from conftest.py."""
    file_path = temp_dir / "test.txt"
    file_path.write_text("content")
    assert file_path.exists()

def test_with_mock_openai(mock_openai_client):
    """Use mock_openai_client fixture."""
    response = mock_openai_client.chat.completions.create(...)
    assert response is not None
```

### Creating Custom Fixtures

```python
import pytest

@pytest.fixture
def sample_story():
    """Provide a sample story for testing."""
    return {
        "title": "Test Story",
        "content": "Once upon a time...",
        "metadata": {"author": "Test Author"}
    }

def test_story_processing(sample_story):
    """Test using custom fixture."""
    assert sample_story["title"] == "Test Story"
```

### Fixture Scopes

```python
@pytest.fixture(scope="function")  # Default - runs for each test
def function_fixture():
    pass

@pytest.fixture(scope="module")  # Runs once per module
def module_fixture():
    pass

@pytest.fixture(scope="session")  # Runs once per test session
def session_fixture():
    pass
```

## Mocking

### Using Mock Providers

```python
from tests.mocks.mock_openai_provider import MockOpenAIProvider, create_mock_provider

def test_with_mock_provider():
    """Test using mock OpenAI provider."""
    # Create provider with custom responses
    provider = create_mock_provider(["Response 1", "Response 2"])
    
    # Use provider
    result1 = provider.generate_chat([{"role": "user", "content": "Hello"}])
    result2 = provider.generate_chat([{"role": "user", "content": "Hi"}])
    
    assert result1 == "Response 1"
    assert result2 == "Response 2"
    assert provider.call_count == 2
```

### Using pytest-mock

```python
def test_with_mocker(mocker):
    """Test using pytest-mock."""
    # Mock a function
    mock_function = mocker.patch('module.function_name')
    mock_function.return_value = "mocked result"
    
    # Call code that uses the mocked function
    result = module.function_name()
    
    assert result == "mocked result"
    mock_function.assert_called_once()
```

### Patching Environment Variables

```python
def test_with_env_vars(monkeypatch):
    """Test with environment variables."""
    monkeypatch.setenv("API_KEY", "test-key")
    monkeypatch.setenv("DEBUG", "true")
    
    # Test code that reads environment variables
    assert os.getenv("API_KEY") == "test-key"
```

## Test Coverage

### Running Coverage

```bash
# Run tests with coverage
pytest --cov

# Generate HTML coverage report
pytest --cov --cov-report=html

# Open HTML report
open htmlcov/index.html
```

### Coverage Configuration

Coverage is configured in `pyproject.toml`:

- **Minimum coverage**: 70%
- **Source**: `src/` directory
- **Omitted**: tests, `__init__.py` files, obsolete code

### Writing Testable Code

Make code more testable by:

1. **Use dependency injection**:
```python
# Good - testable
def process_data(provider, data):
    return provider.transform(data)

# Bad - hard to test
def process_data(data):
    provider = RealProvider()  # Hard-coded dependency
    return provider.transform(data)
```

2. **Keep functions small and focused**:
```python
# Good - each function does one thing
def validate_input(data):
    if not data:
        raise ValueError("Data cannot be empty")

def process_data(data):
    validate_input(data)
    return transform(data)
```

3. **Avoid side effects**:
```python
# Good - pure function
def calculate_total(items):
    return sum(item.price for item in items)

# Bad - side effect
total = 0
def calculate_total(items):
    global total
    total = sum(item.price for item in items)
```

## Testing Best Practices

### 1. Test One Thing at a Time

```python
# Good - tests one aspect
def test_config_loads_log_level():
    settings = Settings(log_level="DEBUG")
    assert settings.log_level == "DEBUG"

def test_config_validates_log_level():
    with pytest.raises(ValueError):
        Settings(log_level="INVALID")

# Avoid - tests multiple things
def test_config():
    settings = Settings(log_level="DEBUG")
    assert settings.log_level == "DEBUG"
    with pytest.raises(ValueError):
        Settings(log_level="INVALID")
    # ... more assertions
```

### 2. Use Descriptive Test Names

```python
# Good
def test_logger_creates_file_in_specified_directory()
def test_config_raises_error_when_path_invalid()

# Avoid
def test_logger()
def test_config_error()
```

### 3. Keep Tests Independent

```python
# Good - each test is independent
def test_create_user():
    user = create_user("test@example.com")
    assert user.email == "test@example.com"

def test_delete_user():
    user = create_user("test@example.com")
    delete_user(user.id)
    assert get_user(user.id) is None

# Avoid - tests depend on each other
user_id = None

def test_create_user():
    global user_id
    user = create_user("test@example.com")
    user_id = user.id
    assert user.email == "test@example.com"

def test_delete_user():
    global user_id
    delete_user(user_id)  # Depends on previous test
```

### 4. Test Edge Cases

```python
def test_function_with_various_inputs():
    # Normal case
    assert calculate(10, 5) == 15
    
    # Edge cases
    assert calculate(0, 0) == 0
    assert calculate(-5, 5) == 0
    assert calculate(1000000, 1) == 1000001
    
    # Error cases
    with pytest.raises(TypeError):
        calculate("invalid", 5)
```

### 5. Use Parameterized Tests

```python
import pytest

@pytest.mark.parametrize("input,expected", [
    (0, 0),
    (1, 1),
    (2, 4),
    (3, 9),
    (-2, 4),
])
def test_square(input, expected):
    assert square(input) == expected
```

## Integration Testing

### Testing with Mock APIs

```python
from tests.mocks.mock_openai_provider import MockOpenAIProvider

@pytest.mark.integration
def test_script_generation_flow():
    """Test complete script generation flow with mocked API."""
    # Setup
    provider = MockOpenAIProvider()
    provider.set_response("Generated script content")
    
    # Test
    generator = ScriptGenerator(provider)
    script = generator.generate("Story about robots")
    
    # Verify
    assert "Generated script content" in script
    assert provider.call_count == 1
```

### Testing with Real APIs

```python
import os
import pytest

@pytest.mark.integration
@pytest.mark.requires_api
def test_real_openai_api():
    """Test with real OpenAI API (requires API key)."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        pytest.skip("OPENAI_API_KEY not set")
    
    provider = OpenAIProvider(api_key)
    response = provider.generate_chat([
        {"role": "user", "content": "Say 'test successful'"}
    ])
    
    assert "test" in response.lower()
```

## Continuous Integration

### GitHub Actions

The project uses GitHub Actions for CI. Tests run automatically on:
- Every push to `main`
- Every pull request
- Scheduled runs (daily)

### Local Pre-commit Checks

Before committing, run:

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov

# Run linting
black src/ tests/
flake8 src/ tests/
```

## Troubleshooting

### Tests Fail Locally But Pass in CI

1. Check Python version matches CI (3.10+)
2. Ensure all dependencies are installed: `pip install -e ".[dev]"`
3. Clear pytest cache: `pytest --cache-clear`

### Import Errors

If you see import errors:

```bash
# Install package in editable mode
pip install -e .

# Or add project root to PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
```

### Slow Tests

```bash
# Run only fast tests
pytest -m "not slow"

# Run with verbose output to see which tests are slow
pytest -v --durations=10
```

### Coverage Not Tracking

```bash
# Clear coverage data
rm -rf .coverage htmlcov/

# Run with coverage
pytest --cov --cov-report=html
```

## Resources

- [pytest Documentation](https://docs.pytest.org/)
- [pytest-cov Documentation](https://pytest-cov.readthedocs.io/)
- [pytest-mock Documentation](https://pytest-mock.readthedocs.io/)
- [Testing Best Practices](https://docs.python-guide.org/writing/tests/)

## Examples

### Complete Test File Example

```python
"""Tests for configuration management."""

import os
import pytest
from pathlib import Path

from core.config import Settings, get_settings


class TestSettings:
    """Test Settings class."""
    
    def test_default_values(self):
        """Test default configuration values."""
        settings = Settings()
        assert settings.log_level == "INFO"
        assert settings.max_workers == 4
    
    def test_env_override(self, monkeypatch):
        """Test environment variable override."""
        monkeypatch.setenv("LOG_LEVEL", "DEBUG")
        settings = Settings()
        assert settings.log_level == "DEBUG"
    
    @pytest.mark.parametrize("level", ["DEBUG", "INFO", "WARNING", "ERROR"])
    def test_log_levels(self, level):
        """Test various log levels."""
        settings = Settings(log_level=level)
        assert settings.log_level == level
    
    def test_invalid_log_level(self):
        """Test invalid log level raises error."""
        with pytest.raises(ValueError):
            Settings(log_level="INVALID")
    
    def test_path_creation(self, tmp_path):
        """Test directory creation."""
        story_root = tmp_path / "stories"
        settings = Settings(story_root=story_root)
        assert story_root.exists()


@pytest.mark.integration
class TestSettingsIntegration:
    """Integration tests for settings."""
    
    def test_complete_workflow(self, isolated_config):
        """Test complete configuration workflow."""
        settings = get_settings()
        assert settings.story_root.exists()
        assert settings.log_dir.exists()
```

## Getting Help

If you have questions about testing:
1. Check this guide
2. Review existing tests in the `tests/` directory
3. Consult the [pytest documentation](https://docs.pytest.org/)
4. Ask in team chat or create an issue
