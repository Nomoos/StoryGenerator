# Python Development Guidelines - PEP Adoption

This document outlines the Python Enhancement Proposals (PEPs) adopted for the StoryGenerator project to ensure modern, maintainable, and type-safe Python code.

## Adopted PEPs

### PEP 484 – Type Hints
**Status:** ✅ Adopted  
**Python Version:** 3.5+  
**Impact:** All functions and methods now include type annotations

Type hints improve code clarity, enable better IDE support, and catch errors early through static type checking.

**Example:**
```python
def process_story(title: str, content: str, max_length: int = 1000) -> dict[str, str]:
    """Process a story and return metadata."""
    return {"title": title, "summary": content[:max_length]}
```

**Configuration:**
- `mypy` enabled with strict type checking
- `disallow_untyped_defs = true` enforces type annotations on all functions

### PEP 604 – Union Types with `|` Syntax
**Status:** ✅ Adopted  
**Python Version:** 3.10+  
**Impact:** Modern union type syntax replaces `typing.Union`

The `|` operator provides cleaner, more readable type unions.

**Before:**
```python
from typing import Union, Optional
def get_value() -> Union[str, int, None]:
    pass
```

**After:**
```python
def get_value() -> str | int | None:
    pass
```

**Benefits:**
- More concise and readable
- Aligns with mathematical set notation
- No imports needed for basic unions

### PEP 585 – Type Hinting Generics in Standard Collections
**Status:** ✅ Adopted  
**Python Version:** 3.9+  
**Impact:** Use built-in collection types for type hints

Standard collection types (`list`, `dict`, `set`, `tuple`) can be used directly in type hints without importing from `typing`.

**Before:**
```python
from typing import List, Dict, Tuple
def process(items: List[str]) -> Dict[str, int]:
    pass
```

**After:**
```python
def process(items: list[str]) -> dict[str, int]:
    pass
```

### PEP 612 – Parameter Specification Variables
**Status:** ✅ Adopted  
**Python Version:** 3.10+  
**Impact:** Better typing for decorators and higher-order functions

`ParamSpec` enables precise type hints for functions that wrap other functions.

**Example:**
```python
from typing import ParamSpec, TypeVar, Callable

P = ParamSpec('P')
R = TypeVar('R')

def log_calls(func: Callable[P, R]) -> Callable[P, R]:
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        print(f"Calling {func.__name__}")
        return func(*args, **kwargs)
    return wrapper
```

### PEP 618 – Optional Length-Checking in `zip`
**Status:** ✅ Adopted  
**Python Version:** 3.10+  
**Impact:** Safer iteration over multiple sequences

The `strict=True` parameter in `zip()` ensures all iterables have the same length.

**Example:**
```python
# Raises ValueError if lists have different lengths
for title, content in zip(titles, contents, strict=True):
    process_story(title, content)
```

### PEP 621 – Project Metadata in `pyproject.toml`
**Status:** ✅ Adopted  
**Python Version:** All  
**Impact:** Standardized project configuration

All project metadata is now in `pyproject.toml` following PEP 621 standard format.

**Key sections:**
- `[project]` - Name, version, description, dependencies
- `[project.optional-dependencies]` - Development dependencies
- `[project.urls]` - Homepage, documentation, repository links
- `[build-system]` - Build configuration

### PEP 668 – Externally Managed Environments
**Status:** ✅ Recognized  
**Python Version:** 3.11+  
**Impact:** Prevents accidental system package modifications

Modern Python installations use externally managed environments. Always use virtual environments:

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -e ".[dev]"
```

### PEP 525 – Asynchronous Generators
**Status:** ✅ Adopted  
**Python Version:** 3.6+  
**Impact:** Async iteration support

Used in async pipeline stages for streaming data processing.

**Example:**
```python
async def fetch_stories() -> AsyncGenerator[dict[str, str], None]:
    """Stream stories from API."""
    async for story in api_client.stream():
        yield story
```

### PEP 530 – Asynchronous Comprehensions
**Status:** ✅ Adopted  
**Python Version:** 3.6+  
**Impact:** Cleaner async collection building

**Example:**
```python
# Async list comprehension
stories = [story async for story in fetch_stories()]

# Async dict comprehension
story_map = {story['id']: story async for story in fetch_stories()}
```

### PEP 567 – Context Variables
**Status:** ✅ Adopted  
**Python Version:** 3.7+  
**Impact:** Better async context management

Context variables provide thread-safe and async-safe storage.

**Example:**
```python
import contextvars

request_id: contextvars.ContextVar[str] = contextvars.ContextVar('request_id')

async def process_request(id: str) -> None:
    request_id.set(id)
    # Context is preserved across async calls
    await do_work()
```

### PEP 659 – Specialized Adaptive Interpreter
**Status:** ✅ Recognized  
**Python Version:** 3.11+  
**Impact:** Automatic performance improvements

Python 3.11+ includes an adaptive interpreter that specializes bytecode based on runtime behavior. No code changes needed - just run on Python 3.11+.

**Performance gains:**
- 10-60% faster than Python 3.10
- Especially beneficial for loops and type-consistent code
- Works best with type hints

## Type Checking Configuration

### mypy
Strict type checking is enabled in `pyproject.toml`:

```toml
[tool.mypy]
python_version = "3.10"
disallow_untyped_defs = true
disallow_incomplete_defs = true
check_untyped_defs = true
no_implicit_optional = true
warn_redundant_casts = true
warn_unused_ignores = true
warn_no_return = true
warn_unreachable = true
strict_equality = true
```

### Running Type Checks

```bash
# Install mypy if not already installed
pip install mypy

# Check all Python files
mypy scripts/ examples/

# Check specific file
mypy scripts/reddit_scraper.py
```

## Best Practices

### 1. Always Use Type Hints
Every public function and method should have type annotations:

```python
def process_video(
    input_path: str,
    output_path: str,
    quality: int = 1080,
    fps: int = 30
) -> dict[str, str | int]:
    """Process video file with specified settings."""
    ...
```

### 2. Use Modern Type Syntax
- Use `list[str]` instead of `List[str]`
- Use `dict[str, int]` instead of `Dict[str, int]`
- Use `X | Y` instead of `Union[X, Y]`
- Use `X | None` instead of `Optional[X]`

### 3. Document Complex Types
For complex types, consider using `TypeAlias`:

```python
from typing import TypeAlias

StoryMetadata: TypeAlias = dict[str, str | int | list[str]]

def get_metadata() -> StoryMetadata:
    return {"title": "Story", "duration": 120, "tags": ["action"]}
```

### 4. Use Protocols for Duck Typing
Instead of abstract base classes, use `Protocol` for structural subtyping:

```python
from typing import Protocol

class Processable(Protocol):
    def process(self) -> str: ...

def handle(obj: Processable) -> None:
    result = obj.process()
```

### 5. Type Narrow with `TypeGuard`
For runtime type checking:

```python
from typing import TypeGuard

def is_string_list(val: list[object]) -> TypeGuard[list[str]]:
    return all(isinstance(x, str) for x in val)
```

## Migration Guide

### Step 1: Update Imports
Replace old-style imports:
```python
# Old
from typing import List, Dict, Optional, Union

# New
# No imports needed for basic types
```

### Step 2: Update Type Annotations
```python
# Old
def func(items: List[str]) -> Optional[Dict[str, int]]:
    ...

# New
def func(items: list[str]) -> dict[str, int] | None:
    ...
```

### Step 3: Add Missing Annotations
Add type hints to all unannotated functions:
```python
# Before
def calculate(x, y):
    return x + y

# After
def calculate(x: float, y: float) -> float:
    return x + y
```

### Step 4: Run Type Checker
```bash
mypy scripts/ examples/
```

### Step 5: Fix Type Errors
Address any type errors reported by mypy.

## References

- [PEP 484 – Type Hints](https://peps.python.org/pep-0484/)
- [PEP 585 – Type Hinting Generics](https://peps.python.org/pep-0585/)
- [PEP 604 – Union Operators](https://peps.python.org/pep-0604/)
- [PEP 612 – Parameter Specification](https://peps.python.org/pep-0612/)
- [PEP 618 – zip strict](https://peps.python.org/pep-0618/)
- [PEP 621 – Project Metadata](https://peps.python.org/pep-0621/)
- [PEP 668 – Externally Managed Environments](https://peps.python.org/pep-0668/)
- [PEP 525 – Async Generators](https://peps.python.org/pep-0525/)
- [PEP 530 – Async Comprehensions](https://peps.python.org/pep-0530/)
- [PEP 567 – Context Variables](https://peps.python.org/pep-0567/)
- [PEP 659 – Specialized Interpreter](https://peps.python.org/pep-0659/)
- [mypy Documentation](https://mypy.readthedocs.io/)

## Status

- ✅ PEP 621 metadata format implemented
- ✅ Modern type syntax adopted (PEP 585, 604)
- ✅ Type checking enabled with mypy
- ✅ Documentation created
- 🔄 Type annotations being added to all functions (in progress)

---

**Last Updated:** 2025-10-10  
**Python Version:** 3.10+  
**Type Checker:** mypy 1.8+
