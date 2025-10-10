# Scoring: Title Viral Scorer

**ID:** `04-scoring-01-title-scorer`  
**Priority:** P1  
**Effort:** 4-5 hours  
**Status:** ✅ Complete

## Overview

Scores titles for viral potential using a comprehensive multi-factor rubric. Evaluates titles across 5 dimensions to predict engagement.

## Dependencies

**Requires:**
- `03-ideas-04` - Title generation
- `01-research-01` - Scoring rubric config

**Blocks:**
- `04-scoring-02` - Voice recommendation
- `04-scoring-03` - Top selection

## Acceptance Criteria

- [x] TitleScorer class implemented
- [x] Viral scoring rubric (5 dimensions)
- [x] Scores 0-100 scale
- [x] 12 unit tests passing
- [x] Code reviewed and merged

## Implementation

**Module:** `core/pipeline/title_scoring.py`
**Class:** `TitleScorer`

```python
from core.pipeline.title_scoring import TitleScorer

scorer = TitleScorer(config_path=Path("config/scoring.yaml"))
scored_titles = scorer.score_all_titles(titles_by_topic)
scorer.save_scored_titles(scored_titles, output_dir)
```

**Scoring Dimensions:**
1. **Novelty** (25%) - Uniqueness, surprise, fresh perspectives
2. **Emotional** (25%) - Emotional impact, dramatic language
3. **Clarity** (20%) - Readability, length, word complexity
4. **Replay** (15%) - Rewatchability, reference value
5. **Share** (15%) - Shareability, social triggers

## Output Files

**File:** `data/titles/{gender}/{age_bucket}/titles_scored.json`

```json
{
  "total_titles": 80,
  "average_score": 72.5,
  "titles_by_topic": {
    "topic_01": [
      {
        "id": "topic_01_title_01",
        "text": "Why nobody tells you this shocking truth",
        "score": 85.5,
        "score_breakdown": {
          "novelty": 75,
          "emotional": 90,
          "clarity": 85,
          "replay": 70,
          "share": 80
        },
        "score_tier": "excellent"
      }
    ]
  }
}
```

## Next Steps

- `04-scoring-02` - Add voice recommendations
- `04-scoring-03` - Select top 5 per segment
