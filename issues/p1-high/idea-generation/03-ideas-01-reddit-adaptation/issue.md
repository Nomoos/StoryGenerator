# Ideas: Adapt Reddit Stories

**ID:** `03-ideas-01-reddit-adaptation`  
**Priority:** P1  
**Effort:** 4-5 hours  
**Status:** ✅ Complete

## Overview

Adapts Reddit stories from the content pipeline into structured video ideas suitable for specific audience segments. Uses LLM to transform raw Reddit content into engaging video concepts.

## Dependencies

**Requires:**
- `02-content-05` - Content ranking/quality control
- `01-research-01` - Research and segmentation
- OpenAI API or compatible LLM

**Blocks:**
- `03-ideas-03` - Topic clustering (needs ideas as input)

## Acceptance Criteria

- [x] IdeaAdapter class implemented
- [x] Reddit story adaptation logic working
- [x] Ideas saved to JSON format
- [x] Unit tests passing (9 tests)
- [x] Code reviewed and merged

## Task Details

### Implementation

**Module:** `core/pipeline/idea_generation.py`

**Class:** `IdeaAdapter`

The IdeaAdapter takes Reddit stories and adapts them into video ideas using LLM prompts:

```python
from core.pipeline.idea_generation import IdeaAdapter
from providers.openai_provider import OpenAIProvider

# Initialize
llm = OpenAIProvider(model="gpt-4o-mini")
adapter = IdeaAdapter(llm)

# Adapt single story
story = {
    "id": "abc123",
    "title": "My crazy experience at work",
    "selftext": "Story content...",
    "score": 1500,
    "subreddit": "tifu"
}

idea = adapter.adapt_story(story, gender="women", age_bucket="18-23")

# Adapt multiple stories
ideas = adapter.adapt_stories(stories, "women", "18-23")

# Save to file
adapter.save_ideas(ideas, Path("data/ideas/women/18-23"))
```

**Key Features:**
- LLM-based story adaptation for target audience
- Preserves source attribution and metadata
- JSON output format
- Batch processing support

### Testing

```bash
# Run unit tests
pytest tests/pipeline/test_idea_generation.py::TestIdeaAdapter -v

# Test with mock provider
python -m scripts.pipeline.generate_ideas --gender women --age 18-23 --mock
```

## Output Files

**Directory:** `data/ideas/{gender}/{age_bucket}/`

**File:** `reddit_adapted.json`

```json
[
  {
    "id": "reddit_abc123",
    "source": "reddit_adapted",
    "original_title": "My crazy experience at work",
    "original_url": "https://reddit.com/r/tifu/abc123",
    "content": "Adapted video idea content here...",
    "target_gender": "women",
    "target_age": "18-23",
    "adapted_at": "2024-01-01T12:00:00",
    "metadata": {
      "score": 1500,
      "subreddit": "tifu"
    }
  }
]
```

## Related Files

- `core/pipeline/idea_generation.py` - Main implementation
- `tests/pipeline/test_idea_generation.py` - Unit tests
- `scripts/pipeline/generate_ideas.py` - Pipeline orchestration
- `docs/PIPELINE_OUTPUT_FILES.md` - Output documentation

## Notes

- Requires active LLM provider (OpenAI API key)
- Can use mock provider for testing
- Respects rate limits with retry logic
- Maintains source attribution for content compliance

## Next Steps

After completion:
- `03-ideas-03` - Topic clustering can proceed
- Ideas will be merged with LLM-generated ideas
