# Ideas: Generate Titles

**ID:** `03-ideas-04-title-generation`  
**Priority:** P1  
**Effort:** 3-4 hours  
**Status:** ✅ Complete

## Overview

Generates multiple title variants for each topic using LLM creativity. Creates engaging, viral-ready titles optimized for short-form video content.

## Dependencies

**Requires:**
- `03-ideas-03` - Topic clustering

**Blocks:**
- `04-scoring-01` - Title scoring (needs titles)

## Acceptance Criteria

- [x] TitleGenerator class implemented  
- [x] Multiple title variants per topic (10+)
- [x] Titles saved to JSON format
- [x] Code reviewed and merged

## Implementation

**Module:** `core/pipeline/title_generation.py`
**Class:** `TitleGenerator`

```python
from core.pipeline.title_generation import TitleGenerator

generator = TitleGenerator(llm_provider)
titles_by_topic = generator.generate_all_titles(topics, titles_per_topic=10)
generator.save_titles(titles_by_topic, output_dir)
```

**Features:**
- High temperature (0.85) for creative diversity
- Viral title techniques (questions, numbers, emotions)
- 10+ variants per topic
- Length validation (20-100 chars)

## Output Files

**File:** `data/titles/{gender}/{age_bucket}/titles_raw.json`

```json
{
  "total_titles": 80,
  "total_topics": 8,
  "generated_at": "2024-01-01T12:00:00",
  "titles_by_topic": {
    "topic_01": [
      {
        "id": "topic_01_title_01",
        "topic_id": "topic_01",
        "text": "Why nobody tells you this shocking truth about relationships",
        "length": 60
      }
    ]
  }
}
```

## Next Steps

- `04-scoring-01` - Score titles for viral potential
