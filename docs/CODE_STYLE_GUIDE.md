# Code Style Guide

This document defines the coding standards and style guidelines for the StoryGenerator project.

## Overview

The project enforces consistent code style using automated tools:
- **Black** - Code formatter
- **isort** - Import sorting
- **Flake8** - Linting and style checking
- **mypy** - Static type checking
- **pre-commit** - Automated pre-commit hooks

## Quick Start

### Installation

```bash
# Install development dependencies
pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install
```

### Usage

```bash
# Format code with Black
black src/ tests/

# Sort imports
isort src/ tests/

# Run linting
flake8 src/ tests/

# Run type checking
mypy src/

# Run all pre-commit hooks manually
pre-commit run --all-files
```

## Code Formatting (Black)

### Configuration

Black is configured in `pyproject.toml`:
- **Line length**: 100 characters
- **Target versions**: Python 3.10, 3.11, 3.12
- **Excludes**: `.git`, `.venv`, `build`, `dist`, `obsolete`

### Rules

Black automatically formats code to follow PEP 8 with minimal configuration:

```python
# Good - Black formatted
def process_data(
    items: List[Dict[str, Any]],
    max_items: int = 100,
    validate: bool = True,
) -> List[ProcessedItem]:
    """Process items with validation."""
    results = []
    for item in items[:max_items]:
        if validate and not is_valid(item):
            continue
        results.append(process_item(item))
    return results


# Black will auto-format
def process_data(items:List[Dict[str,Any]],max_items:int=100,validate:bool=True)->List[ProcessedItem]:
    results=[]
    for item in items[:max_items]:
        if validate and not is_valid(item):continue
        results.append(process_item(item))
    return results
```

### Key Points

- **No configuration needed** - Black is opinionated and consistent
- **Automatic formatting** - Run `black .` before committing
- **Line length** - 100 characters (slightly longer for readability)
- **Strings** - Double quotes by default
- **Trailing commas** - Added for multi-line structures

## Import Sorting (isort)

### Configuration

isort is configured to work with Black:
- **Profile**: black
- **Line length**: 100 characters

### Import Order

```python
# Standard library imports
import os
import sys
from pathlib import Path
from typing import List, Dict, Optional

# Third-party imports
import requests
from pydantic import BaseModel, Field

# Local application imports
from core.config import settings
from core.logging import get_logger
from PrismQ.Providers.openai_provider import OpenAIProvider
```

### Rules

1. **Standard library first** - Built-in Python modules
2. **Third-party second** - External packages
3. **Local imports last** - Project modules
4. **Blank lines** - Between import groups
5. **Alphabetical** - Within each group

## Linting (Flake8)

### Configuration

Flake8 is configured in `.flake8`:
- **Max line length**: 100
- **Ignored rules**: E203, W503, E501 (conflicts with Black)
- **Max complexity**: 10

### Common Rules

#### Line Length

```python
# Good - under 100 characters
result = provider.generate_completion(prompt="Hello", temperature=0.7)

# Acceptable - break long lines
result = provider.generate_completion(
    prompt="Hello world, this is a long prompt",
    temperature=0.7,
    max_tokens=1000,
)
```

#### Imports

```python
# Good - specific imports
from typing import List, Dict

# Avoid - wildcard imports
from typing import *  # Flake8 error: F403
```

#### Unused Variables

```python
# Good - use the variable
for item in items:
    process(item)

# Bad - unused variable
for item in items:  # Flake8 error: F841
    pass

# Good - explicit ignore with underscore
for _ in range(10):
    do_something()
```

#### Complexity

```python
# Good - simple function (complexity < 10)
def calculate_total(items):
    return sum(item.price for item in items)

# Bad - too complex (complexity > 10)
def process_complex_logic(data):
    # Multiple nested if/for statements
    # Break into smaller functions
    pass
```

## Type Checking (mypy)

### Configuration

mypy is configured in `pyproject.toml`:
- **Python version**: 3.10
- **Strict mode**: Enabled
- **Enforce type annotations**: Yes

### Type Annotations

#### Function Signatures

```python
# Good - full type annotations
def greet(name: str, age: int) -> str:
    return f"Hello {name}, you are {age}"

# Bad - no type annotations (mypy error)
def greet(name, age):
    return f"Hello {name}, you are {age}"
```

#### Variables

```python
# Good - explicit types
count: int = 0
items: List[str] = []
config: Optional[Dict[str, Any]] = None

# Also good - type inference
count = 0  # inferred as int
items = ["a", "b"]  # inferred as List[str]
```

#### Class Attributes

```python
from typing import ClassVar

class Config:
    """Configuration class."""
    
    # Instance attribute
    api_key: str
    
    # Class attribute
    default_timeout: ClassVar[int] = 30
    
    def __init__(self, api_key: str) -> None:
        self.api_key = api_key
```

#### Return Types

```python
# Good - explicit return type
def get_items() -> List[Item]:
    return [Item(id=1), Item(id=2)]

# Good - None return type
def log_message(message: str) -> None:
    print(message)

# Bad - missing return type (mypy error)
def get_items():
    return [Item(id=1), Item(id=2)]
```

## Naming Conventions

### Files and Modules

```
# Good
user_profile.py
openai_provider.py
test_config.py

# Avoid
UserProfile.py
OpenAIProvider.py
testConfig.py
```

### Classes

```python
# Good - PascalCase
class UserProfile:
    pass

class OpenAIProvider:
    pass

# Avoid
class user_profile:
    pass

class openAI_provider:
    pass
```

### Functions and Variables

```python
# Good - snake_case
def calculate_total_price(items):
    pass

user_count = 10
max_retries = 3

# Avoid - camelCase
def calculateTotalPrice(items):
    pass

userCount = 10
maxRetries = 3
```

### Constants

```python
# Good - UPPER_SNAKE_CASE
MAX_RETRY_COUNT = 5
DEFAULT_TIMEOUT = 30
API_BASE_URL = "https://api.example.com"

# Avoid
max_retry_count = 5
MaxRetryCount = 5
```

### Private Members

```python
class Example:
    def __init__(self):
        self.public_attr = "public"
        self._private_attr = "private"
        self.__very_private = "very private"
    
    def public_method(self):
        pass
    
    def _private_method(self):
        pass
```

## Documentation

### Docstrings

Use Google-style docstrings:

```python
def process_items(
    items: List[Item],
    max_count: int = 100,
    validate: bool = True,
) -> List[ProcessedItem]:
    """Process a list of items with optional validation.
    
    This function processes items in batches and returns the results.
    If validation is enabled, invalid items are skipped.
    
    Args:
        items: List of items to process
        max_count: Maximum number of items to process
        validate: Whether to validate items before processing
        
    Returns:
        List of processed items
        
    Raises:
        ValueError: If max_count is negative
        ProcessingError: If processing fails
        
    Example:
        >>> items = [Item(id=1), Item(id=2)]
        >>> results = process_items(items, max_count=10)
        >>> len(results)
        2
    """
    if max_count < 0:
        raise ValueError("max_count must be non-negative")
    
    results = []
    for item in items[:max_count]:
        if validate and not is_valid(item):
            continue
        results.append(process_item(item))
    return results
```

### Comments

```python
# Good - explain why, not what
# Cache results for 5 minutes to reduce API calls
cached_results = cache.get(key, ttl=300)

# Avoid - redundant comment
# Set the count to 0
count = 0
```

## Best Practices

### 1. Keep Functions Small

```python
# Good - single responsibility
def validate_email(email: str) -> bool:
    return "@" in email and "." in email.split("@")[1]

def send_notification(user: User, message: str) -> None:
    if validate_email(user.email):
        send_email(user.email, message)

# Avoid - doing too much
def validate_and_send(user: User, message: str) -> None:
    # Validation logic
    # Email sending logic
    # Error handling
    # Logging
    pass
```

### 2. Use Type Hints

```python
# Good
def calculate_price(
    base_price: float,
    discount: float = 0.0,
    tax_rate: float = 0.1,
) -> float:
    discounted = base_price * (1 - discount)
    return discounted * (1 + tax_rate)

# Avoid
def calculate_price(base_price, discount=0.0, tax_rate=0.1):
    discounted = base_price * (1 - discount)
    return discounted * (1 + tax_rate)
```

### 3. Use Context Managers

```python
# Good
with open("file.txt") as f:
    data = f.read()

# Good - custom context manager
with database.transaction():
    database.update(record)

# Avoid
f = open("file.txt")
data = f.read()
f.close()
```

### 4. Use List Comprehensions

```python
# Good - readable
squares = [x ** 2 for x in range(10)]
even_squares = [x ** 2 for x in range(10) if x % 2 == 0]

# Avoid - too complex
result = [func(x, y) for x in range(10) if x > 5 for y in range(20) if y < 15]
```

### 5. Use Enums for Constants

```python
from enum import Enum

# Good
class Status(Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETE = "complete"
    ERROR = "error"

# Avoid - magic strings
status = "pending"
if status == "pending":
    process()
```

## Pre-commit Hooks

### Installation

```bash
# Install pre-commit
pip install pre-commit

# Install git hooks
pre-commit install
```

### Usage

Pre-commit hooks run automatically on `git commit`:

```bash
# Commit triggers hooks
git commit -m "Add feature"

# Hooks run:
# - Trailing whitespace check
# - End of file fixer
# - YAML/JSON validation
# - Black formatting
# - isort import sorting
# - Flake8 linting
# - mypy type checking
```

### Manual Run

```bash
# Run all hooks on all files
pre-commit run --all-files

# Run specific hook
pre-commit run black --all-files
pre-commit run flake8 --all-files

# Skip hooks (emergency only)
git commit --no-verify
```

### Configuration

Pre-commit hooks are configured in `.pre-commit-config.yaml`:
- **black** - Code formatting
- **isort** - Import sorting
- **flake8** - Linting
- **mypy** - Type checking
- **trailing-whitespace** - Remove trailing whitespace
- **end-of-file-fixer** - Ensure files end with newline

## CI/CD Integration

### GitHub Actions

Style checks run automatically in CI:

```yaml
- name: Check code style
  run: |
    black --check src/ tests/
    isort --check src/ tests/
    flake8 src/ tests/
    mypy src/
```

### Enforced Checks

Pull requests must pass:
- ✅ Black formatting
- ✅ isort import order
- ✅ Flake8 linting
- ✅ mypy type checking
- ✅ Test coverage >70%

## Troubleshooting

### Black vs Flake8 Conflicts

Some Flake8 rules conflict with Black. These are ignored in `.flake8`:
- `E203` - Whitespace before ':'
- `W503` - Line break before binary operator
- `E501` - Line too long

### Import Sorting Issues

If isort and Black conflict:

```bash
# Run in this order
isort src/ tests/
black src/ tests/
```

### Type Checking Errors

Common mypy errors:

```python
# Error: Missing type annotation
def func(x):  # mypy error
    return x * 2

# Fix: Add type annotations
def func(x: int) -> int:
    return x * 2

# Error: Incompatible types
result: str = 123  # mypy error

# Fix: Use correct type
result: int = 123
```

## Resources

- [Black Documentation](https://black.readthedocs.io/)
- [isort Documentation](https://pycqa.github.io/isort/)
- [Flake8 Documentation](https://flake8.pycqa.org/)
- [mypy Documentation](https://mypy.readthedocs.io/)
- [pre-commit Documentation](https://pre-commit.com/)
- [PEP 8 Style Guide](https://www.python.org/dev/peps/pep-0008/)
- [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html)

## Getting Help

If you have questions about code style:
1. Check this guide
2. Review the tool documentation
3. Run the tools and read error messages
4. Ask in team chat or create an issue
