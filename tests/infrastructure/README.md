# Infrastructure Tests

This directory contains tests for the infrastructure components of StoryGenerator.

## Test Coverage

### Configuration Tests (`test_config.py`)

Tests the pydantic-settings based configuration management system:

- **Default Values** (4 tests)
  - Model settings defaults
  - Path defaults
  - Log level defaults
  - Performance settings defaults

- **Validation** (6 tests)
  - Valid log levels
  - Case-insensitive log levels
  - Invalid log level error handling
  - Temperature range validation (0.0-2.0)
  - Max tokens positive validation
  - Max retries positive validation

- **Environment Variables** (3 tests)
  - Environment variable override
  - Optional environment variables
  - Boolean environment variables

- **Path Creation** (1 test)
  - Automatic directory creation

- **Singleton Pattern** (2 tests)
  - Singleton instance management
  - Settings reload functionality

- **Integration** (1 test)
  - Complete configuration workflow

**Coverage**: 100% (47/47 statements)

### Logging Tests (`test_logging.py`)

Tests the structured logging system:

- **Setup** (5 tests)
  - Default logging setup
  - Custom log level
  - Console-only output
  - File-only output
  - Log directory creation

- **Output** (3 tests)
  - Writing to log file
  - Multiple log levels
  - Log level filtering

- **JSON Format** (1 test)
  - JSON formatted logs

- **Logger Access** (3 tests)
  - Getting logger instance
  - Logger with custom name
  - Multiple logger instances

- **Context** (2 tests)
  - Logger context usage
  - Factory restoration

- **Integration** (2 tests)
  - Complete logging workflow
  - Request ID tracking

**Coverage**: 96.77% (60/62 statements)

## Running Tests

```bash
# Run all infrastructure tests
pytest tests/infrastructure/

# Run specific test file
pytest tests/infrastructure/test_config.py
pytest tests/infrastructure/test_logging.py

# Run with coverage
pytest tests/infrastructure/ --cov=src/Python/config --cov=src/Python/logging

# Run with verbose output
pytest tests/infrastructure/ -v

# Run specific test class
pytest tests/infrastructure/test_config.py::TestSettingsValidation

# Run specific test
pytest tests/infrastructure/test_config.py::TestSettingsValidation::test_log_level_validation_valid
```

## Test Structure

```
tests/infrastructure/
├── __init__.py                # Package initialization
├── test_config.py             # Configuration management tests
└── test_logging.py            # Logging system tests
```

## Fixtures Used

### From `tests/conftest.py`

- `temp_dir`: Temporary directory with cleanup
- `monkeypatch`: Pytest fixture for environment variable mocking
- `tmp_path`: Pytest fixture for temporary paths
- `caplog`: Pytest fixture for log capturing
- `mocker`: Pytest-mock fixture for creating mocks

### Custom Fixtures

Tests use inline fixtures and pytest's built-in fixtures for isolated testing.

## Test Markers

Infrastructure tests are automatically marked as:
- `integration`: Tests in infrastructure directory

Use markers to filter tests:

```bash
# Run only integration tests
pytest -m integration

# Run only unit tests
pytest -m unit

# Skip slow tests
pytest -m "not slow"
```

## Writing New Infrastructure Tests

Follow this template:

```python
import pytest
from PrismQ.Shared.config import Settings

class TestNewFeature:
    """Test suite for new feature."""
    
    def test_basic_case(self):
        """Test basic functionality."""
        # Arrange
        settings = Settings()
        
        # Act
        result = settings.some_method()
        
        # Assert
        assert result == expected_value
    
    def test_error_case(self):
        """Test error handling."""
        with pytest.raises(ValueError, match="expected error"):
            Settings(invalid_param="bad")
```

## Best Practices

1. **Test Isolation**: Use `tmp_path` and `monkeypatch` for isolated tests
2. **Clear Names**: Test names should describe what is being tested
3. **AAA Pattern**: Arrange, Act, Assert structure
4. **One Assertion**: Test one thing at a time
5. **Edge Cases**: Test boundary conditions
6. **Error Handling**: Test both success and failure cases
7. **Fast Tests**: Keep tests fast (<1s each)
8. **No External Dependencies**: Mock all external services

## Coverage Goals

- **Minimum**: 70% (project requirement)
- **Target**: 80%+ (recommended)
- **Infrastructure**: 95%+ (critical code)

Current infrastructure coverage: **98.17%**

## Troubleshooting

### Tests Failing

```bash
# Run with full traceback
pytest tests/infrastructure/ --tb=long

# Run with print statements visible
pytest tests/infrastructure/ -s

# Run with debugging on failure
pytest tests/infrastructure/ --pdb
```

### Coverage Too Low

```bash
# See what's not covered
pytest tests/infrastructure/ --cov=src/Python --cov-report=term-missing

# Generate HTML coverage report
pytest tests/infrastructure/ --cov=src/Python --cov-report=html
open htmlcov/index.html
```

### Import Errors

```bash
# Verify Python path includes project root
python -c "import sys; print('\n'.join(sys.path))"

# Try importing directly
python -c "from PrismQ.Shared.config import settings; print(get_settings())"
```

## See Also

- [Infrastructure Documentation](../../docs/INFRASTRUCTURE.md)
- [Test README](../README.md)
- [TDD Guide](../../docs/TDD_GUIDE.md)
