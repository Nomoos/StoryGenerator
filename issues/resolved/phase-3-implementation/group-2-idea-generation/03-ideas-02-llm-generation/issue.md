# Ideas: LLM Original Ideas

**ID:** `03-ideas-02-llm-generation`  
**Priority:** P1  
**Effort:** 3-4 hours  
**Status:** ✅ Complete

## Overview

Generates original story ideas using LLM without relying on external content sources. Creates fresh, creative video concepts tailored to specific audience segments.

## Dependencies

**Requires:**
- `01-research-01` - Research and audience segmentation
- OpenAI API or compatible LLM

**Blocks:**
- `03-ideas-03` - Topic clustering (needs ideas as input)

## Acceptance Criteria

- [x] IdeaGenerator class implemented
- [x] LLM prompt templates for idea generation
- [x] Ideas saved to JSON format
- [x] Unit tests passing (9 tests)
- [x] Code reviewed and merged

## Task Details

### Implementation

**Module:** `core/pipeline/idea_generation.py`

**Class:** `IdeaGenerator`

Generates original ideas using creative LLM prompts:

```python
from core.pipeline.idea_generation import IdeaGenerator
from providers.openai_provider import OpenAIProvider

# Initialize
llm = OpenAIProvider(model="gpt-4o-mini")
generator = IdeaGenerator(llm)

# Generate ideas
ideas = generator.generate_ideas(
    gender="women",
    age_bucket="18-23",
    count=20
)

# Save to file
generator.save_ideas(ideas, Path("data/ideas/women/18-23"))
```

**Key Features:**
- Higher temperature (0.8) for creative generation
- Structured prompt for viral video concepts
- Automatic parsing of numbered lists
- Metadata tracking (model, timestamp)

**Prompt Strategy:**
- Target audience context (gender, age)
- Viral content requirements
- Short-form format (30-60 seconds)
- Relatable scenarios and emotions

### Testing

```bash
# Run unit tests
pytest tests/pipeline/test_idea_generation.py::TestIdeaGenerator -v

# Generate ideas with mock provider
python -m scripts.pipeline.generate_ideas --gender women --age 18-23 --mock --ideas-count 20
```

## Output Files

**Directory:** `data/ideas/{gender}/{age_bucket}/`

**File:** `llm_generated.json`

```json
[
  {
    "id": "llm_001",
    "source": "llm_generated",
    "content": "A young professional discovers her coworkers have been secretly helping her succeed...",
    "target_gender": "women",
    "target_age": "18-23",
    "generated_at": "2024-01-01T12:00:00",
    "metadata": {
      "model": "gpt-4o-mini"
    }
  }
]
```

**Merged File:** `all_ideas.json`

Combines Reddit-adapted and LLM-generated ideas:

```json
{
  "total_count": 35,
  "adapted_count": 15,
  "generated_count": 20,
  "merged_at": "2024-01-01T12:00:00",
  "ideas": [...]
}
```

## Related Files

- `core/pipeline/idea_generation.py` - Main implementation
- `tests/pipeline/test_idea_generation.py` - Unit tests
- `scripts/pipeline/generate_ideas.py` - Pipeline orchestration
- `docs/PIPELINE_OUTPUT_FILES.md` - Output documentation

## Notes

- Uses higher temperature (0.8) for creativity vs. adaptation (0.7)
- Automatically parses numbered lists from LLM output
- Robust to various response formats
- Can generate 20+ ideas per segment

## Next Steps

After completion:
- Ideas merged with Reddit-adapted ideas in `all_ideas.json`
- `03-ideas-03` - Topic clustering can proceed with combined ideas
