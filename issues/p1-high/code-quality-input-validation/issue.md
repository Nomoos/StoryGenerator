# Code Quality: Add Input Validation

**ID:** `code-quality-input-validation`  
**Priority:** P1 (High)  
**Effort:** 4-5 hours  
**Status:** Not Started

## Overview

Missing input validation throughout the codebase leads to cryptic errors and potential security issues. Add comprehensive validation for all user inputs and API parameters.

## Dependencies

**Requires:** 
- `code-quality-error-handling` - Exception classes should exist

## Acceptance Criteria

- [ ] Validate all function inputs
- [ ] Use Pydantic for data validation
- [ ] Clear error messages for invalid inputs
- [ ] Type hints on all functions
- [ ] Validation tests

## Task Details

### 1. Install Pydantic

```bash
pip install pydantic>=2.5.0
```

### 2. Create Validation Models

```python
from pydantic import BaseModel, Field, validator

class StoryPrompt(BaseModel):
    text: str = Field(..., min_length=10, max_length=10000)
    temperature: float = Field(0.7, ge=0.0, le=2.0)
    max_tokens: int = Field(1000, ge=1, le=4000)
    
    @validator('text')
    def text_not_empty(cls, v):
        if not v.strip():
            raise ValueError('Prompt cannot be empty')
        return v.strip()
```

### 3. Use Validation in Functions

```python
def generate_story(prompt: StoryPrompt) -> str:
    # Pydantic ensures prompt is valid
    return llm.generate(prompt.text, temperature=prompt.temperature)
```

### 4. Path Validation

```python
from pathlib import Path

def validate_path(path: Path, must_exist: bool = False, must_be_writable: bool = True):
    """Validate file path."""
    if must_exist and not path.exists():
        raise ValueError(f"Path does not exist: {path}")
    
    if must_be_writable and not os.access(path.parent, os.W_OK):
        raise ValueError(f"Path not writable: {path}")
    
    return path
```

## Output Files

- `core/validators.py` - Validation utilities
- Updated function signatures with validation
- Tests for validation

## Related Documentation

- See `docs/RESEARCH_AND_IMPROVEMENTS.md` Section 7
- Pydantic docs: https://docs.pydantic.dev/
