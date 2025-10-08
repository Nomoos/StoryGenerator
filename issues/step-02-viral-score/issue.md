# Step 2: Viral Score (Titles)

**Status:** Not Started  
**Priority:** High  
**Dependencies:** Step 1 (Ideas → Topics → Titles)

## Overview

Score each title for viral potential using local LLM and the rubric from `/config/scoring.yaml`. Recommend voice (F/M) per segment and select top 5 titles.

## Target Audience
- Segments: `women/{age}` and `men/{age}`
- Age buckets: `10-13`, `14-17`, `18-23`

## Checklist

### 2.1 Title Scoring Implementation
- [ ] Implement `title_score.py` using local LLM rubric per `/config/scoring.yaml`
- [ ] Score each title 0-100 with detailed rationale
- [ ] Include scores for: novelty, emotional, clarity, replay, share
- [ ] Recommend **voice (F/M)** per segment based on content

### 2.2 Score All Titles
- [ ] Score all titles from Step 1 for each segment/age combination
- [ ] Save JSON to: `/scores/{segment}/{age}/YYYYMMDD_title_scores.json`
- [ ] Include metadata: segment, age_bucket, scored timestamp

### 2.3 Select Top Titles
- [ ] Select top **N=5 titles** per segment/age based on scores
- [ ] Write voice recommendation notes to: `/voices/choice/{segment}/{age}/YYYYMMDD_voice_notes.md`
- [ ] Document why each voice was recommended

## JSON Schema

### Title Score (`YYYYMMDD_title_scores.json`)
```json
{
  "title_id": "uuid",
  "segment": "women|men",
  "age_bucket": "10-13|14-17|18-23",
  "score_total": 85,
  "scores": {
    "novelty": 20,
    "emotional": 22,
    "clarity": 18,
    "replay": 13,
    "share": 12
  },
  "voice_recommendation": "female|male",
  "rationale": "Detailed explanation of scores and voice choice"
}
```

### Voice Notes Format (`YYYYMMDD_voice_notes.md`)
```markdown
# Voice Selection Notes - {segment}/{age}

Date: YYYY-MM-DD

## Top 5 Selected Titles

### 1. [Title Name] (Score: 85/100)
- **Voice Recommended:** Female/Male
- **Rationale:** Emotional narrative suits female voice...
- **Title ID:** uuid

### 2. [Title Name] (Score: 82/100)
...
```

## Scoring Rubric Weights

From `/config/scoring.yaml`:
- **Novelty:** 0.25 (25%)
- **Emotional:** 0.25 (25%)
- **Clarity:** 0.20 (20%)
- **Replay:** 0.15 (15%)
- **Share:** 0.15 (15%)

**Total:** 100 points maximum

## Acceptance Criteria

- [ ] `title_score.py` script exists and is functional
- [ ] Title score JSON files exist for all segment/age combinations
- [ ] All titles from Step 1 have been scored
- [ ] Voice notes markdown files exist for all segment/age combinations
- [ ] Top 5 titles selected per segment/age with clear rationale
- [ ] Voice recommendations are justified and documented

## Related Files

- `/scores/{segment}/{age}/` - Scores directory
- `/voices/choice/{segment}/{age}/` - Voice selection notes
- `/config/scoring.yaml` - Scoring rubric configuration
- `/scripts/title_score.py` - Title scoring implementation

## Microstep Validation

Use the MicrostepValidator for tracking:
- Step 5: scores
- Step 9: voice_choice

Comment `@copilot check` when all scoring is complete.

## Notes

- Use local LLM (Qwen2.5-14B or Llama 3.1 8B) for scoring
- Voice recommendations should consider target audience demographics
- Total combinations: 6 (2 genders × 3 age buckets)
