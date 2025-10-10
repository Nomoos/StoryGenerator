# Script: Script Viral Scorer

**ID:** `05-script-02-script-scorer`  
**Priority:** P1  
**Effort:** 3-4 hours  
**Status:** ✅ Complete

## Overview

Score script quality across multiple dimensions to assess viral potential and viewer engagement. Evaluates scripts on engagement, clarity, pacing, demographic fit, storytelling quality, and hook strength using LLM-based assessment.

## Dependencies

**Requires:**
- `05-script-01-raw-generation` - Generated scripts to score

**Blocks:**
- `05-script-03-iteration` - Script improvement iterations
- Script refinement workflow

## Acceptance Criteria

- [x] Script scorer class implemented
- [x] Multi-dimensional quality scoring (6 dimensions)
- [x] Weighted overall score calculation
- [x] LLM-based assessment with consistent prompting
- [x] Robust score parsing with fallbacks
- [x] Comprehensive test coverage
- [x] Documentation complete

## Task Details

### Implementation

**Core Module:** `core/script_development.py`

**Key Classes:**
- `ScriptScorer` - Main scoring class
- `ScriptQualityScores` - Data class for storing scores

**Scoring Dimensions:**
1. **Engagement** (25% weight) - How captivating is the content?
2. **Clarity** (15% weight) - How clear is the narrative?
3. **Pacing** (15% weight) - Is pacing appropriate for short-form?
4. **Demographic Fit** (15% weight) - Match with target audience
5. **Storytelling** (20% weight) - Narrative structure quality
6. **Hook Strength** (10% weight) - Opening hook effectiveness

**Overall Score:** Weighted average of all dimensions

### Code Example

```python
from core.script_development import ScriptScorer, Script

# Initialize
scorer = ScriptScorer(llm_provider)

# Score a script
script = Script(...)  # From ScriptGenerator
scores = scorer.score_script(script, detailed=True)

# Access scores
print(f"Engagement: {scores.engagement}")
print(f"Overall Score: {scores.overall_score}")

# Convert to dict
scores_dict = scores.to_dict()
```

### Scoring System

**Scale:** 0-100 for each dimension

**Interpretation:**
- 0-50: Needs significant improvement
- 51-70: Below target, needs refinement
- 71-85: Good quality, minor improvements possible
- 86-100: Excellent quality, viral potential

**Overall Score Formula:**
```
Overall = (Engagement × 0.25) + (Clarity × 0.15) + (Pacing × 0.15) + 
          (Demographic Fit × 0.15) + (Storytelling × 0.20) + (Hook × 0.10)
```

### Testing

```bash
# Run scorer tests
python -m pytest tests/test_script_development.py::TestScriptScorer -v

# Test score parsing
python -m pytest tests/test_script_development.py::TestScriptScorer::test_parse_scores -v
```

**Test Coverage:**
- Scorer initialization
- Script scoring with LLM
- Score parsing from text responses
- Handling missing scores (defaults to 50)
- Overall score calculation
- Quality scores data structure

## Output Format

**ScriptQualityScores Object:**
```python
{
    "engagement": 85.0,
    "clarity": 90.0,
    "pacing": 80.0,
    "demographic_fit": 75.0,
    "storytelling": 82.0,
    "hook_strength": 88.0,
    "overall_score": 83.5  # Calculated
}
```

**Updated Script JSON:**
```json
{
  "script_id": "idea_001",
  "content": "...",
  "quality_scores": {
    "engagement": 85.0,
    "clarity": 90.0,
    "pacing": 80.0,
    "demographic_fit": 75.0,
    "storytelling": 82.0,
    "hook_strength": 88.0,
    "overall_score": 83.5
  }
}
```

## Related Files

**Implementation:**
- `core/script_development.py` - ScriptScorer class (lines 245-365)
- `core/script_development.py` - ScriptQualityScores dataclass (lines 26-62)

**Tests:**
- `tests/test_script_development.py` - TestScriptScorer (lines 190-260)
- `tests/test_script_development.py` - TestScriptQualityScores (lines 55-84)

## Notes

- Uses lower temperature (0.3) for consistent scoring
- Robust parsing handles various LLM response formats
- Defaults to 50.0 if score cannot be parsed
- Detailed feedback option for improvement suggestions
- Scores are used to identify weak areas for iteration

## Next Steps

After completion:
- ✅ Scripts can be scored for quality assessment
- ✅ Ready for iterative improvement workflow
- ✅ Can identify weak dimensions needing refinement
- ✅ Enables data-driven script optimization
