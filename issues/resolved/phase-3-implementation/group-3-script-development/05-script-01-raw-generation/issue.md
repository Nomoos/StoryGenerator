# Script: Raw Generation (v0)

**ID:** `05-script-01-raw-generation`  
**Priority:** P1  
**Effort:** 4-5 hours  
**Status:** ✅ Complete

## Overview

Generate initial video scripts (v0) from video ideas using LLM. Takes structured video ideas from the Idea Generation group and creates engaging, short-form video scripts suitable for platforms like TikTok and YouTube Shorts.

## Dependencies

**Requires:**
- `04-scoring-03-top-selection` - Top 5 video ideas per demographic segment
- Idea Generation group output - Structured video ideas with metadata

**Blocks:**
- `05-script-02-script-scorer` - Script quality scoring
- Scene Planning group - Beat sheet generation

## Acceptance Criteria

- [x] Script generator class implemented
- [x] LLM integration for script generation
- [x] Target duration support (30-60 seconds)
- [x] Multiple style options (engaging, dramatic, educational)
- [x] Proper output directory structure
- [x] Comprehensive test coverage (24 tests passing)
- [x] Documentation complete

## Task Details

### Implementation

**Core Module:** `core/script_development.py`

**Key Classes:**
- `ScriptGenerator` - Main script generation class
- `Script` - Data class representing a script with metadata

**Features:**
- LLM-based script generation with customizable prompts
- Target word count calculation based on duration
- Automatic cleaning of generated content (removes markdown, stage directions)
- Word count and duration estimation
- JSON output format
- Demographic targeting (gender, age)

### Code Example

```python
from core.script_development import ScriptGenerator
from core.interfaces.llm_provider import OpenAIProvider

# Initialize
llm = OpenAIProvider(api_key="...", model="gpt-4")
generator = ScriptGenerator(llm, output_root="Generator/scripts")

# Generate script
idea = {
    'id': 'idea_001',
    'content': 'A story about overcoming adversity',
    'title': 'Never Give Up',
    'target_gender': 'women',
    'target_age': '18-23'
}

script = generator.generate_script(
    idea=idea,
    target_duration=45.0,
    style='engaging'
)

# Save
output_path = generator.save_script(script, version_label="v0")
```

### Testing

```bash
# Run tests
python -m pytest tests/test_script_development.py::TestScriptGenerator -v

# Test specific functionality
python -m pytest tests/test_script_development.py::TestScriptGenerator::test_generate_script -v
```

**Test Coverage:**
- Generator initialization
- Script generation with various parameters
- Content cleaning (markdown, stage directions)
- Script saving to file system
- JSON serialization

## Output Files

**Structure:**
```
Generator/scripts/
├── v0/
│   ├── women/
│   │   ├── 18-23/
│   │   │   ├── idea_001.json
│   │   │   └── idea_002.json
│   │   └── 24-29/
│   └── men/
└── v1/  # Future iterations
```

**JSON Schema:**
```json
{
  "script_id": "idea_001",
  "content": "Script narration text...",
  "title": "Video Title",
  "target_gender": "women",
  "target_age": "18-23",
  "version": 0,
  "word_count": 125,
  "estimated_duration": 50.0,
  "generated_at": "2025-01-11T10:30:00",
  "metadata": {
    "source_idea_id": "idea_001",
    "generation_style": "engaging",
    "target_duration": 45.0
  }
}
```

## Related Files

**Implementation:**
- `core/script_development.py` - Main implementation (lines 94-243)
- `core/interfaces/llm_provider.py` - LLM provider interface

**Tests:**
- `tests/test_script_development.py` - Comprehensive test suite
  - TestScriptGenerator class (lines 130-188)

**Dependencies:**
- Idea Generation outputs in `Generator/ideas/`

## Notes

- Uses 150 words per minute speaking rate for duration estimation
- Supports multiple generation styles (engaging, dramatic, educational)
- Automatically cleans markdown and stage directions from LLM output
- Second-person perspective ("you") for better engagement
- Strong hooks required in first 3 seconds

## Next Steps

After completion:
- ✅ Scripts are ready for quality scoring (`05-script-02`)
- ✅ Can proceed with script iteration and improvement
- ✅ Foundation for scene planning once scripts are refined
