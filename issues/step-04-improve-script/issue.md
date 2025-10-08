# Step 4: Improve Script by GPT (or Local Substitute)

**Status:** Not Started  
**Priority:** High  
**Dependencies:** Step 3 (Iterated Scripts v1+)

## Overview

Further improve scripts using GPT (or local substitute) focusing on clarity, pacing, and hooks. Continue iteration until scores plateau.

## Target Audience
- Segments: `women/{age}` and `men/{age}`
- Age buckets: `10-13`, `14-17`, `18-23`
- Apply to top 5 titles per segment/age

## Configuration Note

> If strictly local, set `models.llm: qwen2_5_14b` in `/config/pipeline.yaml` and still name the output directory "gpt_improved".

## Checklist

### 4.1 GPT/Local Improvement
- [ ] Improve best script from Step 3 (clarity, pacing, hooks)
- [ ] Focus on:
  - **Clarity:** Clear and concise messaging
  - **Pacing:** Proper rhythm and timing
  - **Hooks:** Strong opening and retention points
- [ ] Save to: `/scripts/gpt_improved/{segment}/{age}/{title_id}_v2.md`

### 4.2 Score Improved Version
- [ ] Score v2 script using `script_score.py`
- [ ] Save to: `/scores/{segment}/{age}/{title_id}_script_v2_score.json`
- [ ] Compare with previous version scores

### 4.3 Additional Iterations (If Needed)
- [ ] If v2 < v1, iterate again (v3, v4)
- [ ] Continue until improvement plateaus (< 5% gain)
- [ ] Track all versions for comparison
- [ ] Select final best version

## Improvement Focus Areas

### Clarity
- Remove ambiguity
- Simplify complex concepts
- Use age-appropriate language
- Ensure message is clear

### Pacing
- Balance information density
- Vary sentence length
- Add natural pauses
- Match target video length (45-60 sec)

### Hooks
- Strengthen opening (first 3 seconds)
- Add mid-script retention hooks
- Compelling conclusion/CTA
- Maintain engagement throughout

## Acceptance Criteria

- [ ] GPT-improved scripts (v2) exist for all titles
- [ ] All v2 scripts have been scored
- [ ] v2 scores compared with v1 scores
- [ ] Additional iterations (v3, v4) if v2 didn't improve
- [ ] Final best version documented per title
- [ ] Score progression tracked (v0 → v1 → v2 → v3...)

## Version Selection Logic

```
IF score_v2 >= score_v1:
    best_version = v2
    continue to v3 if improvement > 5%
ELSE:
    iterate to v3
    IF score_v3 < score_v2:
        best_version = highest scoring version
        STOP iteration
```

## Related Files

- `/scripts/gpt_improved/{segment}/{age}/` - GPT-improved scripts
- `/scores/{segment}/{age}/` - All script scores
- `/config/pipeline.yaml` - LLM configuration

## Microstep Validation

Use the MicrostepValidator for tracking:
- Step 8: scripts_gpt

Comment `@copilot check` when improvement is complete.

## Notes

- Model options: GPT-4, GPT-3.5-turbo, or Qwen2.5-14B locally
- Keep all versions for quality analysis
- Document which version was selected as final
- Total scripts to improve: 30 (5 titles × 6 combinations)
