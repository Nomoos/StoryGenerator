# Scoring: Select Top 5 Titles

**ID:** `04-scoring-03-top-selection`  
**Priority:** P1  
**Effort:** 1-2 hours  
**Status:** ✅ Complete

## Overview

Selects the top 5 titles per segment based on viral scores while ensuring diversity across topics.

## Dependencies

**Requires:**
- `04-scoring-01` - Title scoring

**Blocks:**
- Script Development group (needs selected titles)

## Acceptance Criteria

- [x] TopSelector class implemented
- [x] Top 5 selection per segment
- [x] Topic diversity ensured
- [x] 9 unit tests passing
- [x] Code reviewed and merged

## Implementation

**Module:** `core/pipeline/top_selection.py`
**Class:** `TopSelector`

```python
from core.pipeline.top_selection import TopSelector

selector = TopSelector()
selected = selector.select_top_titles(titles_with_voices, top_n=5, min_score=55)
selector.save_selected_titles(selected, output_dir, gender, age_bucket)
```

**Selection Strategy:**
1. Filter titles below minimum score (default: 55)
2. Sort by score descending
3. First pass: Select one title per topic for diversity
4. Second pass: Fill remaining slots with highest scores
5. Final: Re-sort by score

## Output Files

**File:** `data/selected/{gender}/{age_bucket}/top_5_titles.json`

```json
{
  "segment": {
    "gender": "women",
    "age_bucket": "18-23"
  },
  "total_selected": 5,
  "average_score": 82.3,
  "topics_represented": 4,
  "selected_at": "2024-01-01T12:00:00",
  "titles": [
    {
      "id": "topic_02_title_05",
      "text": "The shocking truth nobody tells you about relationships",
      "score": 92.5,
      "score_tier": "excellent",
      "topic_id": "topic_02",
      "voice_recommendation": {...}
    }
  ]
}
```

## Next Steps

- Script Development group can begin with selected titles
- These titles feed into script generation pipeline
