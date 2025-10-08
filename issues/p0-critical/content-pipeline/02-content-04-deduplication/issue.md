# Content: Story Deduplication

**ID:** `02-content-04-deduplication`  
**Priority:** P1  
**Effort:** 2-3 hours  
**Status:** ✅ Complete

## Overview

Detects and removes duplicate content from quality-scored stories using multiple deduplication strategies:
1. **Exact ID matching** - Same content_id from different sources
2. **Fuzzy title matching** - Normalized title comparison (case-insensitive)
3. **Content similarity** - Hash-based detection of similar text content

When duplicates are found, the system keeps the highest scoring item and removes lower-scoring duplicates.

## Dependencies

**Requires:**
- `02-content-01` - Reddit scraper (provides content)
- `02-content-02` - Alternative sources (provides content)
- `02-content-03` - Quality scorer (provides scored content)

**Blocks:**
- `02-content-05` - Ranking (needs deduplicated content)

## Acceptance Criteria

- [x] Script reads quality-scored content from `Generator/scores/{gender}/{age_bucket}/`
- [x] Implements multiple deduplication strategies (ID, title, content hash)
- [x] Keeps highest scoring duplicate when conflicts found
- [x] Outputs deduplicated content to JSON file
- [x] Generates deduplication report with statistics
- [x] Documentation updated
- [x] Tests passing (9/9 tests)
- [x] Code reviewed and merged

## Task Details

### Implementation

The deduplication script is located at `scripts/deduplicate_content.py` and provides:

#### Core Functions:
- `normalize_text(text)` - Normalize text for comparison (lowercase, strip whitespace)
- `calculate_content_hash(content)` - Generate hash from text content for similarity detection
- `deduplicate_content(items)` - Apply deduplication strategies and return unique items
- `process_segment(gender, age_bucket, date)` - Process a specific demographic segment

#### Deduplication Strategy:
1. **Sort by score** - Process highest scoring items first
2. **Check exact ID** - Skip if content_id already seen
3. **Check title match** - Skip if normalized title already seen
4. **Check content hash** - Skip if text content hash already seen
5. **Add to unique set** - If all checks pass, item is unique

#### Output Files:
- `content_deduped_{date}.json` - Deduplicated content list
- `dedup_report_{date}.json` - Statistics and duplicate information

### Testing

```bash
# Run comprehensive test suite
python tests/test_deduplication.py

# Process single segment
python scripts/deduplicate_content.py --segment women --age 18-23

# Process all segments
python scripts/deduplicate_content.py --all

# Process with specific date
python scripts/deduplicate_content.py --all --date 2025-01-15
```

### Example Usage

```bash
# Process all demographic segments
cd /home/runner/work/StoryGenerator/StoryGenerator
python scripts/deduplicate_content.py --all

# Output:
# 🎯 Processing women/10-13...
#    ✅ 45 unique / 50 total
#    📉 Removed 5 duplicates (10.0%)
# ...
# ✨ Processed 6 segments
# 📊 Total: 280 unique / 300 input
# 🗑️  Removed: 20 duplicates
```

## Output Files

**Location:** `Generator/scores/{gender}/{age_bucket}/`

### 1. Deduplicated Content (`content_deduped_{date}.json`)
```json
[
  {
    "content_id": "story_001",
    "title": "Amazing Discovery",
    "text": "Full story text...",
    "viral_score": 85,
    "quality_score": 75,
    "novelty": 80,
    "emotional_impact": 90,
    ...
  }
]
```

### 2. Deduplication Report (`dedup_report_{date}.json`)
```json
{
  "timestamp": "2025-01-15T10:30:00",
  "segment": "women",
  "age_bucket": "18-23",
  "date": "2025-01-15",
  "total_input_items": 100,
  "unique_items": 87,
  "total_duplicates": 13,
  "duplicates_by_type": {
    "exact_id": 5,
    "title_match": 6,
    "content_similarity": 2
  },
  "duplicate_groups": 13,
  "retention_rate": 87.0,
  "input_file": "Generator/scores/women/18-23/content_scores_2025-01-15.json",
  "output_file": "Generator/scores/women/18-23/content_deduped_2025-01-15.json",
  "retained_items": [
    {
      "content_id": "story_001",
      "title": "Top story title...",
      "score": 160
    }
  ]
}
```

## Related Files

- `scripts/deduplicate_content.py` - Main deduplication script
- `tests/test_deduplication.py` - Comprehensive test suite (9 tests)
- `docs/PIPELINE_OUTPUT_FILES.md` - Output file documentation

## Notes

### Deduplication Strategies Explained:

1. **Exact ID Match**: Catches exact duplicates from the same source with identical IDs
2. **Fuzzy Title Match**: Catches near-duplicates with same/similar titles (case-insensitive)
3. **Content Similarity**: Catches stories with different titles but similar content using hash of first 500 characters

### Design Decisions:

- **Sort by score first**: Ensures highest quality duplicate is always kept
- **Multiple strategies**: Catches different types of duplicates (exact, near-exact, similar)
- **Hash-based similarity**: Uses first 500 chars to balance accuracy vs. performance
- **Detailed reporting**: Provides breakdown by duplicate type for analysis

### Performance:

- Memory efficient: Processes items sequentially
- Fast hash-based lookups: O(1) duplicate checking
- Scales well: Tested with hundreds of items per segment

## Next Steps

After completion:
- `02-content-05`: Ranking can use deduplicated content
- `03-ideas-01`: Idea generation has cleaner input
- Quality improvement: No duplicate stories in final output
