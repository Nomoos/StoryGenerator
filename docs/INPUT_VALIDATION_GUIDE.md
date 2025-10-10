# Input Validation System

This document describes the comprehensive input validation system for StoryGenerator using Pydantic models and validation decorators.

## Overview

The input validation system provides:
- **Type-safe data models** using Pydantic
- **Automatic validation** with clear error messages
- **Validation decorators** for functions
- **Schema documentation** with examples
- **Comprehensive test coverage** (62 tests)

## Quick Start

### Basic Usage

```python
from core.models import StoryIdea, ScriptConfig
from core.validation import validate_input, validate_dict

# Validate a dictionary manually
data = {
    "id": "story-123",
    "content": "This is a story about...",
    "target_gender": "women",
    "target_age": "18-23",
    "source": "reddit"
}

idea = validate_dict(data, StoryIdea)
print(idea.content)  # Type-safe access
```

### Using Decorators

```python
from core.validation import validate_input, validate_output
from core.models import StoryIdea, APIResponse

@validate_input(idea=StoryIdea)
def process_story(idea):
    """Process a story idea."""
    return f"Processing: {idea.content}"

@validate_output(APIResponse)
def get_response():
    """Get an API response."""
    return {"success": True, "data": {"key": "value"}}
```

## Data Models

### Core Models

#### StoryIdea

Represents a story idea for video generation.

```python
from core.models import StoryIdea

idea = StoryIdea(
    id="unique-id-123",
    content="This is the story content...",
    target_gender="women",  # or "men"
    target_age="18-23",  # or "10-13", "14-17"
    source="reddit",  # or "instagram", "tiktok", "manual", "generated"
    score=85.5,  # Optional: 0-100
    metadata={"author": "user123"}  # Optional
)
```

**Validation Rules:**
- `id`: 1-100 characters, alphanumeric + hyphens + underscores
- `content`: 10-5000 characters, cannot be empty/whitespace
- `target_gender`: Must be "women" or "men"
- `target_age`: Must be "10-13", "14-17", or "18-23"
- `source`: Must be valid ContentSource enum
- `score`: 0.0-100.0 (default: 0.0)

#### ScriptConfig

Configuration for script generation.

```python
from core.models import ScriptConfig

config = ScriptConfig(
    min_words=350,  # 100-1000
    max_words=370,  # 100-1000, must be > min_words
    temperature=0.7,  # 0.0-1.0
    max_tokens=2000,  # 100-10000
    model="gpt-4"
)
```

**Validation Rules:**
- `min_words`: 100-1000
- `max_words`: 100-1000, must be greater than min_words
- `temperature`: 0.0-1.0
- `max_tokens`: 100-10000
- `model`: 1-100 characters

#### TitleConfig

Configuration for title generation.

```python
from core.models import TitleConfig

config = TitleConfig(
    count=10,  # 1-100
    min_length=20,  # 10-200
    max_length=100,  # 10-200, must be > min_length
    require_emoji=False,
    temperature=0.8  # 0.0-1.0
)
```

#### AudioConfig

Configuration for audio generation with ElevenLabs.

```python
from core.models import AudioConfig

config = AudioConfig(
    voice_id="voice-id-123",
    stability=0.5,  # 0.0-1.0
    similarity_boost=0.75,  # 0.0-1.0
    style=0.0,  # 0.0-1.0
    use_speaker_boost=True
)
```

#### ImageConfig

Configuration for image generation with Stable Diffusion.

```python
from core.models import ImageConfig

config = ImageConfig(
    width=1024,  # 256-2048, must be multiple of 8
    height=1024,  # 256-2048, must be multiple of 8
    steps=30,  # 10-100
    guidance_scale=7.5,  # 1.0-20.0
    negative_prompt="blurry, low quality",
    seed=42  # Optional: 0 to 2^32-1
)
```

#### VideoConfig

Configuration for video generation.

```python
from core.models import VideoConfig

config = VideoConfig(
    fps=30,  # 1-60
    duration=60.0,  # 1.0-300.0 seconds
    resolution="1080p",  # "720p", "1080p", or "4k"
    codec="libx264",
    bitrate="5M"
)
```

#### APIResponse

Generic API response wrapper.

```python
from core.models import APIResponse

# Success response
response = APIResponse(
    success=True,
    data={"result": "processed"},
    metadata={"timestamp": "2025-10-10"}
)

# Error response
response = APIResponse(
    success=False,
    error="Something went wrong",
    metadata={"error_code": "E001"}
)
```

**Validation Rules:**
- Must provide `error` when `success=False`
- Cannot provide `error` when `success=True`

#### BatchRequest

Request for batch processing.

```python
from core.models import BatchRequest

request = BatchRequest(
    items=[1, 2, 3, 4, 5],
    batch_size=10,  # 1-100
    parallel=True,
    max_workers=4  # 1-32
)
```

**Validation Rules:**
- `items`: Cannot be empty
- `max_workers`: Must be 1 when `parallel=False`

## Validation Decorators

### @validate_input

Validates function inputs against Pydantic models.

```python
from core.validation import validate_input
from core.models import StoryIdea, ScriptConfig

@validate_input(idea=StoryIdea, config=ScriptConfig)
def generate_script(idea, config):
    """Generate a script from an idea."""
    return f"Script for {idea.id}: {config.min_words}-{config.max_words} words"

# Call with dictionaries
result = generate_script(
    idea={"id": "test", "content": "Story...", ...},
    config={"min_words": 300, "max_words": 400}
)

# Or call with model instances
idea = StoryIdea(...)
config = ScriptConfig(...)
result = generate_script(idea=idea, config=config)
```

### @validate_output

Validates function outputs against a Pydantic model.

```python
from core.validation import validate_output
from core.models import APIResponse

@validate_output(APIResponse)
def process_data():
    """Process data and return API response."""
    return {
        "success": True,
        "data": {"processed": True}
    }

# Returns APIResponse instance
response = process_data()
assert isinstance(response, APIResponse)
```

### @validate_call

Combines input and output validation.

```python
from core.validation import validate_call
from core.models import StoryIdea

@validate_call(idea=StoryIdea)
def process_idea(idea):
    """Process an idea."""
    return {
        "success": True,
        "data": {"content": idea.content}
    }
```

## Validation Utilities

### validate_dict

Manually validate a dictionary.

```python
from core.validation import validate_dict
from core.models import StoryIdea

data = {"id": "test", "content": "Story...", ...}
idea = validate_dict(data, StoryIdea)
```

### get_validation_errors

Get formatted validation errors.

```python
from core.validation import get_validation_errors
from core.models import StoryIdea

data = {"id": "test", "content": "X"}  # Too short
errors = get_validation_errors(data, StoryIdea)
print(errors)
# Output:
# Validation error for StoryIdea:
# - content: String should have at least 10 characters
```

### is_valid

Check if data is valid without raising exceptions.

```python
from core.validation import is_valid
from core.models import StoryIdea

data = {"id": "test", "content": "Valid content...", ...}
if is_valid(data, StoryIdea):
    print("Data is valid!")
else:
    print("Data is invalid")
```

## Error Handling

### Validation Errors

```python
from pydantic import ValidationError
from core.models import StoryIdea

try:
    idea = StoryIdea(
        id="test",
        content="Short",  # Too short
        target_gender="women",
        target_age="18-23",
        source="reddit"
    )
except ValidationError as e:
    print(f"Validation failed: {e}")
    # Access structured error data
    for error in e.errors():
        field = ".".join(str(loc) for loc in error["loc"])
        message = error["msg"]
        print(f"- {field}: {message}")
```

### Custom Error Messages

Models include custom validators with clear error messages:

```python
@field_validator("content")
@classmethod
def validate_content(cls, v: str) -> str:
    """Validate content is not empty after stripping whitespace."""
    if not v.strip():
        raise ValueError("Content cannot be empty or only whitespace")
    return v.strip()
```

## Testing

### Running Tests

```bash
# Run validation tests
pytest tests/test_core_models.py tests/test_core_validation.py -v

# Run with coverage
pytest tests/test_core_models.py tests/test_core_validation.py --cov=core
```

### Test Coverage

- **62 tests** covering all models and validation utilities
- **Models**: 44 tests for all data models
- **Validation**: 18 tests for decorators and utilities
- **Coverage**: All validation rules and error cases

### Example Tests

```python
def test_story_idea_validation():
    """Test StoryIdea validation."""
    # Valid data
    idea = StoryIdea(
        id="test",
        content="Valid story content",
        target_gender="women",
        target_age="18-23",
        source="reddit"
    )
    assert idea.content == "Valid story content"
    
    # Invalid data
    with pytest.raises(ValidationError):
        StoryIdea(
            id="test",
            content="X",  # Too short
            target_gender="women",
            target_age="18-23",
            source="reddit"
        )
```

## Best Practices

### 1. Always Validate User Input

```python
@validate_input(idea=StoryIdea)
def process_user_input(idea):
    """Always validate input from users/APIs."""
    pass
```

### 2. Use Type Hints

```python
from typing import Dict
from core.models import StoryIdea

def process_idea(idea: StoryIdea) -> Dict[str, str]:
    """Use type hints for clarity."""
    return {"content": idea.content}
```

### 3. Validate at Boundaries

Validate data at system boundaries (API endpoints, file I/O, database):

```python
@app.post("/process")
@validate_input(idea=StoryIdea)
def process_endpoint(idea):
    """Validate at API boundaries."""
    pass
```

### 4. Provide Clear Error Messages

```python
from core.validation import get_validation_errors

data = get_user_input()
errors = get_validation_errors(data, StoryIdea)
if errors:
    return {"error": errors}
```

### 5. Use Enums for Fixed Values

```python
from core.models import TargetGender, TargetAge

# Type-safe access to valid values
gender = TargetGender.WOMEN
age = TargetAge.AGE_18_23
```

## Integration Examples

### With FastAPI

```python
from fastapi import FastAPI
from core.models import StoryIdea, APIResponse

app = FastAPI()

@app.post("/story", response_model=APIResponse)
async def create_story(idea: StoryIdea):
    """FastAPI automatically validates with Pydantic."""
    return APIResponse(
        success=True,
        data={"id": idea.id, "content": idea.content}
    )
```

### With Flask

```python
from flask import Flask, request
from core.models import StoryIdea
from core.validation import validate_dict, get_validation_errors

app = Flask(__name__)

@app.route("/story", methods=["POST"])
def create_story():
    """Validate manually in Flask."""
    data = request.get_json()
    
    errors = get_validation_errors(data, StoryIdea)
    if errors:
        return {"error": errors}, 400
    
    idea = validate_dict(data, StoryIdea)
    return {"success": True, "id": idea.id}
```

### With Database

```python
from core.models import StoryIdea
from core.validation import validate_dict

def save_idea(data: dict):
    """Validate before saving to database."""
    idea = validate_dict(data, StoryIdea)
    
    # Save to database
    db.insert({
        "id": idea.id,
        "content": idea.content,
        "target_gender": idea.target_gender.value,
        ...
    })
```

## Troubleshooting

### Common Issues

#### 1. ValidationError: String should have at least X characters

**Problem:** Content or field is too short.

**Solution:** Ensure content meets minimum length requirements.

```python
# Wrong
content = "Short"  # Less than 10 characters

# Right
content = "This is a longer content that meets the minimum requirement"
```

#### 2. ValidationError: Input should be 'women' or 'men'

**Problem:** Invalid enum value.

**Solution:** Use valid enum values or the enum directly.

```python
# Wrong
target_gender = "female"

# Right
target_gender = "women"
# Or
from core.models import TargetGender
target_gender = TargetGender.WOMEN
```

#### 3. ValidationError: max_words must be greater than min_words

**Problem:** Logical constraint violated.

**Solution:** Ensure max is actually greater than min.

```python
# Wrong
config = ScriptConfig(min_words=400, max_words=300)

# Right
config = ScriptConfig(min_words=300, max_words=400)
```

#### 4. Parameter not found in function signature

**Problem:** Decorator references parameter that doesn't exist.

**Solution:** Match decorator parameter names to function parameters.

```python
# Wrong
@validate_input(story=StoryIdea)
def process_idea(idea):  # Parameter name mismatch
    pass

# Right
@validate_input(idea=StoryIdea)
def process_idea(idea):
    pass
```

## Resources

- [Pydantic Documentation](https://docs.pydantic.dev/)
- [Pydantic Validators](https://docs.pydantic.dev/latest/concepts/validators/)
- [Type Hints Guide](https://docs.python.org/3/library/typing.html)
- [core/models.py](../core/models.py) - Model definitions
- [core/validation.py](../core/validation.py) - Validation utilities
- [tests/test_core_models.py](../tests/test_core_models.py) - Model tests
- [tests/test_core_validation.py](../tests/test_core_validation.py) - Validation tests
