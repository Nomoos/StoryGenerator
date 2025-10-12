# Stage 02: Text Generation

## Purpose

Transform video ideas into complete text content including story scripts, titles, descriptions, tags, and scene descriptions.

## Independence

This stage is **fully independent** and can be developed, tested, and deployed separately.

## Input Contract

```python
@dataclass
class TextGenerationInput:
    idea: IdeaItem                  # Idea from Stage 01
    generate_title: bool = True     # Generate title?
    generate_description: bool = True
    generate_tags: bool = True
    generate_scenes: bool = True
    additional_params: dict = field(default_factory=dict)
```

## Output Contract

```python
@dataclass
class TextGenerationOutput:
    content: TextContent            # Generated text content
    quality_score: float | None     # Quality score (0-100)
    metadata: dict = field(default_factory=dict)

@dataclass
class TextContent:
    story_script: str               # Main narrative script
    title: str | None               # Generated title
    description: str | None         # Video description
    tags: list[str]                 # Tags for discoverability
    scenes: list[dict]              # Scene descriptions
    metadata: dict = field(default_factory=dict)
```

## Dependencies

- ✅ `IPipelineStage`, `ILLMProvider` from shared interfaces
- ✅ `IdeaItem` from stage contracts (data structure only)
- ❌ NO imports from other pipeline stage implementations

## Usage Example

```python
from PrismQ.Infrastructure.Core.Shared.interfaces import (
    TextGenerationInput,
    TextGenerationOutput,
    IdeaItem,
)

# Input from Stage 01
idea = IdeaItem(
    id="llm_001",
    content="A story about overcoming challenges",
    source="llm_generated",
    target_gender="women",
    target_age="18-23",
    created_at=datetime.now()
)

# Create input for Stage 02
input_data = TextGenerationInput(
    idea=idea,
    generate_title=True,
    generate_description=True,
    generate_tags=True,
    generate_scenes=True
)

# Execute stage
result = await text_stage.execute(input_data)

# Access output
content = result.data.content
print(f"Title: {content.title}")
print(f"Script: {content.story_script}")
print(f"Tags: {', '.join(content.tags)}")
```

## Input JSON Example

```json
{
  "idea": {
    "id": "llm_001",
    "content": "A compelling story about personal growth",
    "source": "llm_generated",
    "target_gender": "women",
    "target_age": "18-23",
    "created_at": "2024-01-15T10:30:00"
  },
  "generate_title": true,
  "generate_description": true,
  "generate_tags": true,
  "generate_scenes": true
}
```

## Output JSON Example

```json
{
  "content": {
    "story_script": "In the heart of the city, a young woman discovers...",
    "title": "Journey to Self-Discovery",
    "description": "A powerful story about finding your true self...",
    "tags": ["inspiration", "personal-growth", "self-discovery", "women"],
    "scenes": [
      {
        "timestamp": 0,
        "description": "Opening scene showing city skyline",
        "duration": 5
      },
      {
        "timestamp": 5,
        "description": "Main character introduction",
        "duration": 10
      }
    ]
  },
  "quality_score": 87.5,
  "metadata": {
    "word_count": 450,
    "reading_time_seconds": 180
  }
}
```

## Testing

```python
@pytest.mark.asyncio
async def test_text_generation():
    """Test text generation stage independently."""
    
    mock_llm = Mock()
    mock_llm.generate_completion.side_effect = [
        "Test Story Script",
        "Test Title",
        "Test Description",
        "inspiration, growth, women"
    ]
    
    stage = TextGenerationStage(llm_provider=mock_llm)
    
    idea = IdeaItem(
        id="test_001",
        content="Test idea",
        source="test",
        target_gender="women",
        target_age="18-23",
        created_at=datetime.now()
    )
    
    input_data = TextGenerationInput(idea=idea)
    result = await stage.execute(input_data)
    
    assert result.data.content.story_script == "Test Story Script"
    assert result.data.content.title == "Test Title"
    assert len(result.data.content.tags) > 0
```

## Repository Structure (When Independent)

```
prismq-stage-02-text-generation/
├── src/
│   ├── stage.py              # Main stage implementation
│   ├── script_generator.py   # Script generation
│   ├── title_generator.py    # Title generation
│   ├── tag_generator.py      # Tag generation
│   └── scene_planner.py      # Scene planning
├── tests/
│   └── test_stage.py
├── requirements.txt
│   └── prismq-core>=1.0.0    # Only dependency
└── README.md
```
