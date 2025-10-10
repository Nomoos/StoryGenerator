# Content Deduplication

Detects and removes duplicate stories from quality-scored content using multiple strategies.

## Overview

The deduplication system prevents duplicate content from entering the pipeline by using three detection strategies:

1. **Exact ID Matching** - Catches identical content from the same source
2. **Fuzzy Title Matching** - Catches near-duplicates with similar titles (case-insensitive)
3. **Content Similarity** - Catches stories with different titles but similar content

When duplicates are found, the **highest scoring item is always kept**.

## Quick Start

```bash
# Process all demographic segments
python scripts/deduplicate_content.py --all

# Process specific segment
python scripts/deduplicate_content.py --segment women --age 18-23

# Process with specific date
python scripts/deduplicate_content.py --all --date 2025-01-15
```

## Usage

### Command Line Options

```bash
python scripts/deduplicate_content.py [options]

Options:
  --segment {women,men}        Process specific gender segment
  --age {10-13,14-17,18-23}   Process specific age bucket
  --date YYYY-MM-DD           Date string (defaults to today)
  --all                       Process all segments
  -h, --help                  Show help message
```

### Examples

```bash
# Process all segments for today
python scripts/deduplicate_content.py --all

# Process women 18-23 segment
python scripts/deduplicate_content.py --segment women --age 18-23

# Process specific date
python scripts/deduplicate_content.py --segment men --age 14-17 --date 2025-01-15

# Full pipeline usage
# 1. Scrape content
python scripts/reddit_scraper.py --all

# 2. Score content
python scripts/quality_scorer.py --all

# 3. Deduplicate
python scripts/deduplicate_content.py --all

# 4. Rank and continue...
```

## Input Files

**Location:** `Generator/scores/{gender}/{age_bucket}/`

**Expected file:** `content_scores_{date}.json`

Example structure:
```json
[
  {
    "content_id": "story_001",
    "title": "Story Title",
    "text": "Full story text...",
    "source": "r/relationships",
    "viral_score": 85,
    "quality_score": 78,
    "novelty": 70,
    "emotional_impact": 95,
    ...
  }
]
```

## Output Files

### 1. Deduplicated Content

**File:** `content_deduped_{date}.json`
**Format:** JSON array of unique content items

Contains only unique stories, sorted by combined score (viral_score + quality_score).

### 2. Deduplication Report

**File:** `dedup_report_{date}.json`
**Format:** JSON object with statistics

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
  "retention_rate": 87.0,
  "retained_items": [
    {"content_id": "story_001", "title": "Top story...", "score": 160}
  ]
}
```

## Deduplication Strategies

### 1. Exact ID Match

Detects stories with identical `content_id` from the same source.

**Example:**
```json
// Original
{"content_id": "reddit_001", "title": "Story", "viral_score": 85}

// Duplicate (removed)
{"content_id": "reddit_001", "title": "Story Update", "viral_score": 70}
```

### 2. Fuzzy Title Match

Detects stories with the same normalized title (case-insensitive, whitespace-stripped).

**Example:**
```json
// Original
{"content_id": "001", "title": "My Best Friend Betrayed Me", "score": 85}

// Duplicate (removed)
{"content_id": "002", "title": "my best friend betrayed me", "score": 65}
```

### 3. Content Similarity

Detects stories with similar text content (first 500 characters) even if titles differ.

**Example:**
```json
// Original
{"title": "Lost 100 Pounds", "text": "After years of struggling...", "score": 88}

// Duplicate (removed)
{"title": "Weight Loss Success", "text": "After years of struggling...", "score": 75}
```

## How It Works

1. **Load** - Reads quality-scored content from input file
2. **Sort** - Sorts by score descending (keeps highest quality)
3. **Check** - For each item, checks against three duplicate strategies
4. **Keep** - If unique, adds to output; if duplicate, skips
5. **Save** - Writes deduplicated content and report to files

## Performance

- **Memory efficient**: Processes items sequentially
- **Fast lookups**: O(1) duplicate checking using hash sets
- **Scalable**: Tested with hundreds of items per segment
- **Safe**: Original input files are never modified

## Testing

```bash
# Run comprehensive test suite (9 tests)
python tests/test_deduplication.py

# Expected output:
# ✅ PASS: Text Normalization
# ✅ PASS: Content Hash
# ✅ PASS: Exact ID Deduplication
# ✅ PASS: Title Deduplication
# ✅ PASS: Content Similarity
# ✅ PASS: Empty Input
# ✅ PASS: No Duplicates
# ✅ PASS: Filesystem Integration
# ✅ PASS: Report Structure
# Total: 9/9 tests passed
```

## Integration with Pipeline

### Position in Pipeline

```
Content Scraping → Quality Scoring → [DEDUPLICATION] → Ranking → Idea Generation
```

### Dependencies

**Requires:**
- `02-content-01` - Reddit scraper (content source)
- `02-content-02` - Alternative sources (content source)
- `02-content-03` - Quality scorer (scored content)

**Blocks:**
- `02-content-05` - Ranking (needs deduplicated content)

### File Flow

```
Input:  Generator/scores/{gender}/{age}/content_scores_{date}.json
Output: Generator/scores/{gender}/{age}/content_deduped_{date}.json
        Generator/scores/{gender}/{age}/dedup_report_{date}.json
```

## Configuration

No configuration file needed. The script uses:
- **Hash sample size**: First 500 characters of text
- **Sort order**: Combined `viral_score + quality_score`
- **Keep strategy**: Highest scoring duplicate

## Troubleshooting

### No input file found

```bash
⚠️  Input file not found: Generator/scores/women/18-23/content_scores_2025-01-15.json
```

**Solution:** Ensure quality scoring has been run first:
```bash
python scripts/quality_scorer.py --segment women --age 18-23
```

### No content items

```bash
⚠️  No content items found in input file
```

**Solution:** Check that input file contains a valid JSON array or object with "items" key.

### Empty output

If all items are removed as duplicates, check:
1. Are you running multiple times on same date?
2. Is input file correct?
3. Check dedup_report for details on what was removed

## Implementation Details

### Core Functions

- `normalize_text(text)` - Normalize for comparison
- `calculate_content_hash(content)` - Generate similarity hash
- `deduplicate_content(items)` - Apply all strategies
- `process_segment(gender, age, date)` - Process one segment

### Code Location

- **Script:** `scripts/deduplicate_content.py` (363 lines)
- **Tests:** `tests/test_deduplication.py` (9 comprehensive tests)
- **Docs:** `issues/p0-critical/content-pipeline/02-content-04-deduplication/issue.md`

## Related Documentation

- [Pipeline Output Files](../../docs/PIPELINE_OUTPUT_FILES.md)
- [Content Pipeline README](../../issues/p0-critical/content-pipeline/README.md)
- [Issue Details](../../issues/p0-critical/content-pipeline/02-content-04-deduplication/issue.md)

## Example Output

```bash
$ python scripts/deduplicate_content.py --segment women --age 18-23 --date 2025-01-15

============================================================
CONTENT DEDUPLICATION
============================================================

🎯 Processing women/18-23...
📥 Loaded 7 items from src/Generator/scores/women/18-23/content_scores_2025-01-15.json
✅ Saved 4 unique items to src/Generator/scores/women/18-23/content_deduped_2025-01-15.json
📊 Deduplication report saved to src/Generator/scores/women/18-23/dedup_report_2025-01-15.json
   ✅ 4 unique / 7 total
   📉 Removed 3 duplicates (42.9%)

============================================================
SUMMARY
============================================================
✨ Processed 1 segments
📊 Total: 4 unique / 7 input
🗑️  Removed: 3 duplicates
📈 Overall retention rate: 57.1%
============================================================
```

## License

Part of the StoryGenerator project.
