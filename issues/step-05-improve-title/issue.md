# Step 5: Improve Title by GPT (or Local)

**Status:** Not Started  
**Priority:** Medium  
**Dependencies:** Step 4 (Final Scripts Selected)

## Overview

Generate multiple title variants for each selected title, score them, and choose the best performing version.

## Target Audience
- Segments: `women/{age}` and `men/{age}`
- Age buckets: `10-13`, `14-17`, `18-23`
- Apply to top 5 titles per segment/age

## Checklist

### 5.1 Generate Title Variants
- [ ] Generate **5 variants** per selected title
- [ ] Use GPT or local LLM for variant generation
- [ ] Variants should maintain core concept while improving clickability
- [ ] Consider A/B testing principles

### 5.2 Score All Variants
- [ ] Score all variants using `title_score.py` from Step 2
- [ ] Apply same rubric: novelty, emotional, clarity, replay, share
- [ ] Compare with original title score

### 5.3 Select Best Variant
- [ ] Choose best scoring variant per title
- [ ] Save to: `/titles/{segment}/{age}/{title_id}_improved.json`
- [ ] Update title/slug registry if changed
- [ ] Document improvement rationale

## JSON Schema

### Improved Title (`{title_id}_improved.json`)
```json
{
  "original_title_id": "uuid",
  "segment": "women|men",
  "age_bucket": "10-13|14-17|18-23",
  "original_title": "Original Title Text",
  "original_score": 78,
  "variants": [
    {
      "variant_id": "var-001",
      "title": "Variant Title 1",
      "score_total": 85,
      "scores": {
        "novelty": 20,
        "emotional": 22,
        "clarity": 18,
        "replay": 13,
        "share": 12
      },
      "rationale": "Explanation..."
    }
  ],
  "selected_variant": "var-003",
  "final_title": "Best Variant Title",
  "improvement": "+7 points",
  "updated_at": "2024-01-01T12:00:00Z"
}
```

## Variant Generation Guidelines

### What to Vary
- **Length:** Shorter vs longer versions
- **Question vs Statement:** "Did you know?" vs "The truth about..."
- **Emotional Words:** Vary intensity and type
- **Numbers:** Add/remove specific numbers or statistics
- **Mystery Level:** More/less explicit about content

### What to Preserve
- Core topic and message
- Age-appropriateness
- Segment relevance
- Brand voice consistency

## Acceptance Criteria

- [ ] 5 variants generated per title (total: 150 variants)
- [ ] All variants scored using title scoring rubric
- [ ] Best variant selected per title (30 selections)
- [ ] Improved title JSON files saved for all titles
- [ ] Registry updated with new titles (if changed)
- [ ] Improvement documented (before/after comparison)

## Title Registry Update

If title changes:
- [ ] Update title reference in script metadata
- [ ] Update voice notes if needed
- [ ] Maintain link to original title_id
- [ ] Track version history

## Related Files

- `/titles/{segment}/{age}/` - Titles directory
- `/scores/{segment}/{age}/` - Title scores
- `/scripts/title_score.py` - Scoring implementation
- `/config/scoring.yaml` - Scoring rubric

## Microstep Validation

Use the MicrostepValidator for tracking:
- Step 4: titles

Comment `@copilot check` when title improvement is complete.

## Notes

- Generate variants that test different viral hooks
- A/B testing principles: test one variable at a time when possible
- Keep variants that test significantly different approaches
- Total variants: 150 (5 per title × 30 titles)
- Document why selected variant performs better
