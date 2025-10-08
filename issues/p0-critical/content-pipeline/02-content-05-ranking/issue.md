# Content: Story Ranking & Selection

**ID:** `02-content-05-ranking`  
**Priority:** P1  
**Effort:** 2-3 hours  
**Status:** Complete

## Overview

This task implements the content ranking system that takes scored content from the quality scorer and deduplication report, then produces a ranked list of content sorted by viral potential. The ranking system filters out duplicates and assigns final scores based on multiple quality metrics.

## Dependencies

**Requires:**
- `02-content-03`
- `02-content-04`

**Blocks:**
- [Tasks that depend on this one]

## Acceptance Criteria

- [x] Ranking script created and working
- [x] Can read scored content from content_scores_{date}.json
- [x] Can read dedup report from dedup_report_{date}.json
- [x] Filters out duplicate content based on dedup report
- [x] Calculates final scores using weighted metrics
- [x] Sorts content by score (descending order)
- [x] Outputs ranked_content_{date}.json to correct directory
- [x] Supports processing individual segments or all segments
- [x] Tests passing (6/6 tests pass)
- [x] Documentation updated

## Task Details

### Implementation

**Script:** `scripts/content_ranking.py`

The ranking system:
1. Reads scored content from `Generator/scores/{gender}/{age_bucket}/content_scores_{date}.json`
2. Reads deduplication report from `Generator/scores/{gender}/{age_bucket}/dedup_report_{date}.json`
3. Filters out content marked as duplicates
4. Calculates final scores using weighted metrics:
   - Novelty (25%)
   - Emotional Impact (25%)
   - Clarity (20%)
   - Replay Value (15%)
   - Shareability (15%)
5. Sorts content by final score (descending)
6. Adds rank field to each item
7. Saves to `Generator/scores/{gender}/{age_bucket}/ranked_content_{date}.json`

**Example Usage:**

```bash
# Process all segments
python scripts/content_ranking.py

# Process specific segment
python scripts/content_ranking.py women 18-23

# Specify custom base path
python scripts/content_ranking.py --base-path /path/to/Generator
```

**Score Calculation:**

The system supports multiple score formats:
- Component scores (novelty, emotional_impact, clarity, etc.)
- Pre-calculated final_score or overall_score
- Fallback to quality_score or viral_score

### Testing

```bash
# Run all tests
python tests/test_content_ranking.py

# Tests include:
# - Module imports
# - Final score calculation
# - Duplicate ID extraction
# - Content ranking logic
# - File finding
# - End-to-end workflow
```

**Test Results:** 6/6 tests passing

## Output Files

**Output Directory**: `Generator/scores/{gender}/{age_bucket}/`

**File Created**: `ranked_content_{date}.json`

**Format:**
```json
{
  "gender": "women|men",
  "age_bucket": "10-13|14-17|18-23",
  "ranked_at": "2025-10-08T12:00:00",
  "total_items": 50,
  "content": [
    {
      "rank": 1,
      "id": "content-001",
      "title": "The Secret That Changed Everything",
      "final_score": 92.5,
      "novelty": 90,
      "emotional_impact": 93,
      "clarity": 91,
      "replay_value": 92,
      "shareability": 90,
      ... (all original fields preserved)
    }
  ]
}
```

## Related Files

- **Implementation:** `scripts/content_ranking.py`
- **Tests:** `tests/test_content_ranking.py`
- **Config:** `config/pipeline.yaml`, `config/scoring.yaml`
- **Documentation:** `docs/PIPELINE_OUTPUT_FILES.md`

## Notes

- The ranking system is flexible and handles multiple input formats
- Supports both component-based scoring and pre-calculated scores
- Automatically finds the latest content_scores and dedup_report files
- Can process all segments at once or individual segments
- Preserves all original content fields in the output
- Provides detailed summary statistics after ranking
- Works seamlessly with data from 02-content-03 (quality scorer) and 02-content-04 (deduplication)

## Next Steps

After completion:
- **03-ideas-01** (Reddit Adaptation): Can use ranked content to select best stories for adaptation
- **03-ideas-02** (LLM Generation): Can use top-ranked content as inspiration
- **04-scoring-01** (Title Scoring): Will use similar ranking approach for titles
