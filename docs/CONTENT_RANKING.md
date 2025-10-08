# Content Ranking System - Documentation

## Overview

The content ranking system (`content_ranking.py`) is part of the StoryGenerator pipeline that ranks scored content by viral potential and quality metrics. It takes the output from the quality scorer and deduplication steps and produces a final ranked list of content ready for idea generation.

## Purpose

- **Input**: Scored content and deduplication reports
- **Process**: Filter duplicates, calculate final scores, and rank by viral potential
- **Output**: Ranked content list sorted by score (descending)

## Pipeline Position

```
02-content-03 (Quality Scorer)
        ↓
    content_scores_{date}.json
        ↓
02-content-04 (Deduplication)
        ↓
    dedup_report_{date}.json
        ↓
02-content-05 (Ranking) ← YOU ARE HERE
        ↓
    ranked_content_{date}.json
        ↓
03-ideas-01 (Reddit Adaptation)
```

## Usage

### Process All Segments

```bash
python scripts/content_ranking.py
```

This will process all 6 segments (women/men × 3 age buckets).

### Process Specific Segment

```bash
python scripts/content_ranking.py women 18-23
python scripts/content_ranking.py men 14-17
```

### Custom Base Path

```bash
python scripts/content_ranking.py --base-path /path/to/Generator
```

### Custom Config

```bash
python scripts/content_ranking.py --config /path/to/config.yaml
```

## Input Files

### 1. Content Scores File

**Path**: `Generator/scores/{gender}/{age_bucket}/content_scores_{date}.json`

**Format**:
```json
[
  {
    "id": "content-001",
    "title": "Story Title",
    "source": "r/TrueOffMyChest",
    "novelty": 85,
    "emotional_impact": 90,
    "clarity": 88,
    "replay_value": 82,
    "shareability": 86,
    "quality_score": 87
  }
]
```

**Supported Score Fields**:
- Component scores: `novelty`, `emotional_impact`, `clarity`, `replay_value`, `shareability`
- Pre-calculated: `final_score`, `overall_score`
- Fallback: `quality_score`, `viral_score`, `score`

### 2. Deduplication Report

**Path**: `Generator/scores/{gender}/{age_bucket}/dedup_report_{date}.json`

**Format**:
```json
{
  "duplicates": [
    {
      "id": "content-003",
      "similar_to": "content-001",
      "similarity_score": 0.89
    }
  ],
  "retained_items": ["content-001", "content-002"]
}
```

**Note**: If no dedup report exists, the system will still work and rank all content.

## Output File

**Path**: `Generator/scores/{gender}/{age_bucket}/ranked_content_{date}.json`

**Format**:
```json
{
  "gender": "women",
  "age_bucket": "18-23",
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
      "shareability": 90
      ... (all original fields preserved)
    }
  ]
}
```

## Scoring Algorithm

### Default Weights (from config/scoring.yaml)

```yaml
viral:
  novelty: 0.25      # Unique, surprising content
  emotional: 0.25    # Emotional impact and resonance
  clarity: 0.20      # Clear, easy to understand
  replay: 0.15       # Rewatchability factor
  share: 0.15        # Shareability and virality
```

### Calculation

```
final_score = (
    novelty × 0.25 +
    emotional_impact × 0.25 +
    clarity × 0.20 +
    replay_value × 0.15 +
    shareability × 0.15
)
```

**Example**:
```
Novelty:          85 × 0.25 = 21.25
Emotional Impact: 90 × 0.25 = 22.50
Clarity:          88 × 0.20 = 17.60
Replay Value:     82 × 0.15 = 12.30
Shareability:     87 × 0.15 = 13.05
                               ------
Final Score:                   86.70
```

### Score Thresholds

| Score | Category | Description |
|-------|----------|-------------|
| 85+   | Excellent | Top-tier viral potential |
| 70-84 | Good | Strong candidate for production |
| 55-69 | Acceptable | May need refinement |
| <55   | Poor | Consider alternatives |

## Features

### 1. Duplicate Filtering

Automatically filters out content marked as duplicates in the deduplication report:

```python
# Content marked as duplicate in dedup report
dedup_report = {
    'duplicates': [{'id': 'story-004'}]
}

# Will be excluded from ranking
```

### 2. Flexible Score Formats

Handles multiple input formats:
- Pre-calculated final scores
- Component-based scores
- Fallback scores (quality_score, viral_score)

### 3. Automatic File Discovery

Finds the latest content_scores and dedup_report files automatically:
- Searches by glob pattern (`content_scores_*.json`)
- Sorts by modification time
- Uses most recent file

### 4. Comprehensive Output

Preserves all original content fields plus:
- `rank`: Position in ranking (1, 2, 3, ...)
- `final_score`: Calculated or preserved score

### 5. Summary Statistics

Prints detailed summary after ranking:
- Total items ranked
- Top and bottom scores
- Top 5 items with IDs and scores

## Testing

### Run Tests

```bash
python tests/test_content_ranking.py
```

### Test Coverage

- ✅ Module imports
- ✅ Final score calculation
- ✅ Duplicate ID extraction
- ✅ Content ranking logic
- ✅ File finding
- ✅ End-to-end workflow

**Test Results**: 6/6 tests passing

### Run Examples

```bash
python examples/content_ranking_examples.py
```

Examples demonstrate:
1. Basic content ranking
2. Ranking with duplicate filtering
3. Full end-to-end workflow with file I/O
4. Score calculation explained

## Configuration

### Pipeline Config (config/pipeline.yaml)

Used for general pipeline settings (not ranking-specific).

### Scoring Config (config/scoring.yaml)

```yaml
viral:
  novelty: 0.25
  emotional: 0.25
  clarity: 0.20
  replay: 0.15
  share: 0.15

thresholds:
  excellent: 85
  good: 70
  acceptable: 55
  poor: 40
```

Customize these weights to adjust ranking behavior.

## Integration with Pipeline

### Dependencies

**Requires** (from previous steps):
- `02-content-03` (Quality Scorer): Provides content_scores_{date}.json
- `02-content-04` (Deduplication): Provides dedup_report_{date}.json

**Blocks** (downstream steps):
- `03-ideas-01` (Reddit Adaptation): Uses ranked content to select best stories
- `03-ideas-02` (LLM Generation): Uses top-ranked content as inspiration

### Directory Structure

```
Generator/
└── scores/
    ├── women/
    │   ├── 10-13/
    │   │   ├── content_scores_2025-10-08.json      (input)
    │   │   ├── dedup_report_2025-10-08.json        (input)
    │   │   └── ranked_content_2025-10-08.json      (output)
    │   ├── 14-17/
    │   └── 18-23/
    └── men/
        ├── 10-13/
        ├── 14-17/
        └── 18-23/
```

## Error Handling

### Missing Input Files

```
⚠️  No content_scores files found in Generator/scores/women/18-23
```

**Solution**: Run quality scorer first (02-content-03)

### Missing Dedup Report

```
⚠️  No dedup_report files found in Generator/scores/women/18-23
```

**Note**: Not critical - system will continue without filtering duplicates

### Empty Content

```
⚠️  No content to rank after filtering for women/18-23
```

**Solution**: Check that content_scores file has valid data

## Troubleshooting

### Issue: No files found

**Symptoms**: "No content_scores files found"

**Solutions**:
1. Verify quality scorer has run: `ls Generator/scores/women/18-23/`
2. Check file naming: Files should match `content_scores_*.json`
3. Ensure directory exists: `mkdir -p Generator/scores/women/18-23/`

### Issue: All items filtered as duplicates

**Symptoms**: "No content to rank after filtering"

**Solutions**:
1. Review dedup_report.json - may be too aggressive
2. Check duplicate IDs match content IDs
3. Verify dedup report format is correct

### Issue: Scores are zero

**Symptoms**: All final_score values are 0.00

**Solutions**:
1. Check content_scores file has score fields
2. Verify field names match expected format
3. Ensure component scores exist or fallback scores present

## Performance

### Speed

- Processes ~100 items per second
- Typical runtime for 50 items: <1 second
- File I/O dominates processing time

### Memory

- Loads entire content list into memory
- Typical memory usage: <10 MB per segment
- Scales linearly with content count

### Batch Processing

For all 6 segments (women/men × 3 age buckets):
- Total runtime: ~5-10 seconds
- Depends on content volume per segment

## Best Practices

### 1. Run After Dependencies

Always run quality scorer and deduplication first:

```bash
python scripts/quality_scorer.py      # 02-content-03
python scripts/deduplication.py       # 02-content-04
python scripts/content_ranking.py     # 02-content-05
```

### 2. Verify Output

Check ranked_content_{date}.json after ranking:
- Verify order is correct (highest scores first)
- Check that duplicates were filtered
- Confirm all expected fields are present

### 3. Backup Original Data

Keep copies of content_scores before ranking:
```bash
cp Generator/scores/women/18-23/content_scores_2025-10-08.json \
   Generator/scores/women/18-23/content_scores_2025-10-08.backup.json
```

### 4. Monitor Score Distribution

Review score distribution to ensure quality threshold alignment:
```bash
python scripts/content_ranking.py | grep "Top score"
```

## Future Enhancements

Potential improvements for future versions:

1. **Machine Learning Integration**: Use ML models to predict viral potential
2. **A/B Testing**: Compare ranking algorithms with real engagement data
3. **Dynamic Weights**: Adjust weights based on historical performance
4. **Multi-criteria Ranking**: Support multiple ranking strategies simultaneously
5. **Real-time Updates**: Re-rank as new engagement data arrives
6. **Audience-specific Scoring**: Different weights per segment/age bucket

## See Also

- **Quality Scorer**: `02-content-03-quality-scorer/issue.md`
- **Deduplication**: `02-content-04-deduplication/issue.md`
- **Pipeline Documentation**: `docs/PIPELINE_OUTPUT_FILES.md`
- **Scoring Config**: `config/scoring.yaml`

## Support

For issues or questions:
1. Check test results: `python tests/test_content_ranking.py`
2. Run examples: `python examples/content_ranking_examples.py`
3. Review logs for error messages
4. Verify input file formats match specification

---

**Version**: 1.0  
**Last Updated**: 2025-10-08  
**Status**: Stable
