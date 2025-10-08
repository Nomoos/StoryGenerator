# Step 3: Raw Script (Local) → Score → Iterate

**Status:** Not Started  
**Priority:** High  
**Dependencies:** Step 2 (Viral Score - Top Titles Selected)

## Overview

Generate raw scripts using local LLM from selected titles, score them for viral potential, and iteratively improve based on feedback.

## Target Audience
- Segments: `women/{age}` and `men/{age}`
- Age buckets: `10-13`, `14-17`, `18-23`
- Apply to top 5 titles per segment/age

## Checklist

### 3.1 Raw Script Generation (Local LLM)
- [ ] Use chosen titles from Step 2 → generate **raw script**
- [ ] Use Qwen2.5-14B or Llama3.1-8B for generation
- [ ] Save to: `/scripts/raw_local/{segment}/{age}/{title_id}.md`
- [ ] Scripts should be 45-60 seconds when spoken
- [ ] Include narrative structure: hook, build, climax, resolution

### 3.2 Viral Score (Script v0)
- [ ] Implement `script_score.py` using same rubric + narrative cohesion
- [ ] Score each raw script (v0) 0-100
- [ ] Save to: `/scores/{segment}/{age}/{title_id}_script_v0_score.json`
- [ ] Include detailed feedback for improvement

### 3.3 Iterate Script (Local)
- [ ] Apply feedback → generate **iterated script v1**
- [ ] Save to: `/scripts/iter_local/{segment}/{age}/{title_id}_v1.md`
- [ ] Score v1 → save to: `/scores/{segment}/{age}/{title_id}_script_v1_score.json`
- [ ] Continue iteration if score improves (v2, v3, etc.)
- [ ] Stop when improvement plateaus (< 5% gain)

## JSON Schema

### Script Score (`{title_id}_script_v{N}_score.json`)
```json
{
  "title_id": "uuid",
  "script_version": "v0|v1|v2|...",
  "segment": "women|men",
  "age_bucket": "10-13|14-17|18-23",
  "score_total": 78,
  "scores": {
    "novelty": 18,
    "emotional": 21,
    "clarity": 16,
    "replay": 12,
    "share": 11,
    "narrative_cohesion": 15
  },
  "feedback": "Detailed suggestions for improvement",
  "rationale": "Explanation of scores",
  "scored_at": "2024-01-01T12:00:00Z"
}
```

## Script Format

Each script should include:
- **Title:** From Step 2
- **Target:** Segment/Age
- **Word Count:** ~150-200 words (45-60 sec at normal pace)
- **Structure:**
  - Hook (5-10 sec): Grab attention
  - Build (20-30 sec): Develop story/information
  - Climax (10-15 sec): Peak moment
  - Resolution (5-10 sec): Conclusion/CTA

## Scoring Criteria

Beyond title scoring, add:
- **Narrative Cohesion:** 0-20 points
  - Flow and pacing
  - Story structure
  - Character consistency (if applicable)

## Acceptance Criteria

- [ ] `script_score.py` exists and is functional
- [ ] Raw scripts (v0) exist for all top 5 titles per segment/age (30 total)
- [ ] All v0 scripts have been scored
- [ ] Iterated scripts (v1+) exist with improved scores
- [ ] Score files track progression (v0 → v1 → v2...)
- [ ] Iteration stops when improvements plateau
- [ ] Final best version identified per title

## Related Files

- `/scripts/raw_local/{segment}/{age}/` - Raw scripts directory
- `/scripts/iter_local/{segment}/{age}/` - Iterated scripts directory
- `/scores/{segment}/{age}/` - Script scores directory
- `/config/scoring.yaml` - Scoring rubric
- `/scripts/script_score.py` - Script scoring implementation

## Microstep Validation

Use the MicrostepValidator for tracking:
- Step 6: scripts_raw
- Step 7: scripts_iter

Comment `@copilot check` when iteration is complete.

## Notes

- Total scripts: 30 (5 titles × 6 segment/age combinations)
- Keep iteration history for analysis
- Focus on viral potential metrics
