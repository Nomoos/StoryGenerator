# Pipeline Stage Modular Architecture

## Overview

The PrismQ pipeline has been restructured to support **fully independent, modular repositories** for each pipeline stage. Each stage has:

1. **Clear Input/Output Contracts** - Defined through typed data classes
2. **Independent Testing** - Can be tested without dependencies on other stages
3. **No Cross-Imports** - Stages only depend on shared infrastructure interfaces
4. **Versioned Interfaces** - Each stage has a version for compatibility tracking

## Pipeline Stages

The content creation pipeline consists of 5 sequential stages:

```
01_IdeaGeneration → 02_TextGeneration → 03_AudioGeneration → 04_ImageGeneration → 05_VideoGeneration
```

### Stage 01: Idea Generation

**Input:** `IdeaGenerationInput`
- `target_gender`: Target audience gender
- `target_age`: Target age bucket
- `idea_count`: Number of ideas to generate
- `source_stories`: Optional source stories to adapt

**Output:** `IdeaGenerationOutput`
- `ideas`: List of `IdeaItem` objects
- `total_count`: Total number of ideas
- `adapted_count`: Number of adapted ideas
- `generated_count`: Number of LLM-generated ideas

### Stage 02: Text Generation

**Input:** `TextGenerationInput`
- `idea`: The `IdeaItem` to develop
- `generate_title`: Whether to generate title
- `generate_description`: Whether to generate description
- `generate_tags`: Whether to generate tags
- `generate_scenes`: Whether to generate scene descriptions

**Output:** `TextGenerationOutput`
- `content`: `TextContent` object with story, title, description, tags, scenes
- `quality_score`: Quality score (0-100)

### Stage 03: Audio Generation

**Input:** `AudioGenerationInput`
- `text_content`: `TextContent` from previous stage
- `voice_id`: Voice identifier
- `generate_subtitles`: Whether to generate subtitles
- `audio_format`: Desired format (mp3, wav, etc.)

**Output:** `AudioGenerationOutput`
- `audio`: `AudioContent` object with file path, duration, subtitles

### Stage 04: Image Generation

**Input:** `ImageGenerationInput`
- `text_content`: `TextContent` from text generation
- `audio_content`: Optional `AudioContent` for timing
- `keyframe_count`: Number of keyframes to generate
- `image_style`: Style for generation

**Output:** `ImageGenerationOutput`
- `keyframes`: List of `KeyFrame` objects with images and timestamps

### Stage 05: Video Generation

**Input:** `VideoGenerationInput`
- `text_content`: `TextContent` from text generation
- `audio_content`: `AudioContent` from audio generation
- `keyframes`: List of `KeyFrame` from image generation
- `video_format`: Desired format (mp4, webm, etc.)
- `resolution`: Video resolution
- `fps`: Frames per second

**Output:** `VideoGenerationOutput`
- `video`: `VideoContent` object with file path, duration, metadata

## Implementing a Pipeline Stage

### Step 1: Import Base Classes

```python
from PrismQ.Infrastructure.Core.Shared.interfaces import (
    BasePipelineStage,
    IdeaGenerationInput,
    IdeaGenerationOutput,
    IdeaItem,
)
```

### Step 2: Implement the Stage

```python
class IdeaGenerationStage(BasePipelineStage[IdeaGenerationInput, IdeaGenerationOutput]):
    """Stage 01: Idea Generation."""
    
    def __init__(self, llm_provider):
        super().__init__(
            stage_name="IdeaGeneration",
            stage_id="01_idea_generation",
            version="1.0.0"
        )
        self.llm_provider = llm_provider
    
    async def _execute_impl(self, input_data: IdeaGenerationInput) -> IdeaGenerationOutput:
        """Generate ideas based on input parameters."""
        # Implementation here
        ideas = []
        # ... generate ideas ...
        
        return IdeaGenerationOutput(
            ideas=ideas,
            total_count=len(ideas),
            adapted_count=0,
            generated_count=len(ideas),
        )
    
    async def validate_input(self, input_data: IdeaGenerationInput) -> bool:
        """Validate input parameters."""
        if not input_data.target_gender or not input_data.target_age:
            return False
        if input_data.idea_count <= 0:
            return False
        return True
```

### Step 3: Use the Stage

```python
# Create the stage
stage = IdeaGenerationStage(llm_provider=my_llm_provider)

# Prepare input
input_data = IdeaGenerationInput(
    target_gender="women",
    target_age="18-23",
    idea_count=20
)

# Execute
result = await stage.execute(input_data)

# Access output
ideas = result.data.ideas
metadata = result.metadata
print(f"Generated {len(ideas)} ideas in {metadata.execution_time_ms}ms")
```

## Testing a Stage

Stages can be tested independently using the contracts:

```python
import pytest
from unittest.mock import Mock
from datetime import datetime

@pytest.mark.asyncio
async def test_idea_generation_stage():
    """Test idea generation stage in isolation."""
    
    # Mock dependencies
    mock_llm = Mock()
    mock_llm.generate_completion.return_value = "Test idea content"
    
    # Create stage
    stage = IdeaGenerationStage(llm_provider=mock_llm)
    
    # Create input
    input_data = IdeaGenerationInput(
        target_gender="women",
        target_age="18-23",
        idea_count=1
    )
    
    # Execute stage
    result = await stage.execute(input_data)
    
    # Verify output contract
    assert result.data.total_count == 1
    assert len(result.data.ideas) == 1
    assert result.metadata.status == StageStatus.COMPLETED
    assert result.metadata.stage_name == "IdeaGeneration"
```

## Benefits of Modular Structure

### 1. Independent Development
- Each stage can be developed in its own repository
- Teams can work on different stages simultaneously
- Changes to one stage don't affect others

### 2. Clear Contracts
- Input/output types are explicitly defined
- No ambiguity about data flow
- IDE autocomplete and type checking work properly

### 3. Easy Testing
- Stages can be tested with mocked inputs
- No need to run entire pipeline for testing
- Unit tests are fast and focused

### 4. Versioning
- Each stage has its own version
- Compatibility can be tracked
- Easy to rollback individual stages

### 5. No Cross-Dependencies
- Stages only depend on shared interfaces
- Circular dependencies are impossible
- Import graph is clean and predictable

## Migration Guide

To migrate existing code to the modular structure:

### Before (Tightly Coupled)
```python
# Cross-stage imports (BAD)
from PrismQ.IdeaScraper.idea_generation import IdeaGenerator
from PrismQ.StoryTitleProcessor.title_generation import TitleGenerator
from PrismQ.VoiceOverGenerator.voice_recommendation import VoiceRecommender

# Stages directly calling each other
ideas = idea_generator.generate_ideas(gender, age)
titles = title_generator.generate_titles(ideas)  # Direct coupling!
voice = voice_recommender.recommend(titles)
```

### After (Modular)
```python
# Only import contracts and interfaces (GOOD)
from PrismQ.Infrastructure.Core.Shared.interfaces import (
    IdeaGenerationInput,
    TextGenerationInput,
    AudioGenerationInput,
)

# Stages communicate through contracts
idea_input = IdeaGenerationInput(target_gender="women", target_age="18-23")
idea_result = await idea_stage.execute(idea_input)

# Pass output as input to next stage
text_input = TextGenerationInput(idea=idea_result.data.ideas[0])
text_result = await text_stage.execute(text_input)

# Chain continues with clear contracts
audio_input = AudioGenerationInput(text_content=text_result.data.content)
audio_result = await audio_stage.execute(audio_input)
```

## Stage Development Checklist

When developing a new stage:

- [ ] Define input contract (dataclass)
- [ ] Define output contract (dataclass)
- [ ] Implement `IPipelineStage` interface
- [ ] Add input validation
- [ ] Add unit tests with mocked dependencies
- [ ] Document the stage in this README
- [ ] Add JSON schemas for input/output
- [ ] Version the stage implementation

## Directory Structure

```
PrismQ/
├── Infrastructure/
│   └── Core/
│       └── Shared/
│           └── interfaces/
│               ├── pipeline_stage.py      # Base interfaces
│               ├── stage_contracts.py     # I/O contracts
│               ├── llm_provider.py        # LLM interface
│               └── __init__.py            # Exports
│
├── Pipeline/
│   ├── 01_IdeaGeneration/
│   │   └── README.md                      # Stage-specific docs
│   ├── 02_TextGeneration/
│   │   └── README.md
│   ├── 03_AudioGeneration/
│   │   └── README.md
│   ├── 04_ImageGeneration/
│   │   └── README.md
│   └── 05_VideoGeneration/
│       └── README.md
```

## Future: Separate Repositories

Each stage can eventually be moved to its own repository:

```
github.com/org/prismq-stage-01-idea-generation
github.com/org/prismq-stage-02-text-generation
github.com/org/prismq-stage-03-audio-generation
github.com/org/prismq-stage-04-image-generation
github.com/org/prismq-stage-05-video-generation
```

Each repository would:
- Implement the stage interface
- Depend on `prismq-core` for contracts
- Have its own tests, CI/CD
- Version independently
- Be deployed/used independently
