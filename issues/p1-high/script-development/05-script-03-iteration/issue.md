# Script: Local Iteration (v1)

**ID:** `05-script-03-iteration`  
**Priority:** P1  
**Effort:** 4-5 hours  
**Status:** ✅ Complete

## Overview

Iteratively improve scripts based on quality scores until target score is reached or improvement plateaus. Identifies weak dimensions, generates improved versions, and tracks progress through multiple iterations.

## Dependencies

**Requires:**
- `05-script-02-script-scorer` - Quality scoring system
- Generated scripts from `05-script-01`

**Blocks:**
- `05-script-04-gpt-improvement` - GPT-based enhancement
- High-quality script production workflow

## Acceptance Criteria

- [x] Script iterator class implemented
- [x] Weakness identification algorithm
- [x] Iterative improvement loop with target score
- [x] Plateau detection (stop if no improvement)
- [x] Version tracking for all iterations
- [x] Metadata preservation across versions
- [x] Comprehensive test coverage
- [x] Documentation complete

## Task Details

### Implementation

**Core Module:** `core/script_development.py`

**Key Classes:**
- `ScriptIterator` - Manages iterative improvement
- Supporting: `ScriptScorer` for re-scoring

**Features:**
- Automatic weakness identification (scores < 70)
- Targeted improvements for weakest dimensions
- Configurable target score and max iterations
- Plateau detection (stops if no improvement)
- Version history tracking
- Performance delta reporting

### Code Example

```python
from core.script_development import ScriptIterator, Script

# Initialize
iterator = ScriptIterator(llm_provider)

# Iteratively improve
script = Script(...)  # From ScriptGenerator
versions = iterator.improve_script(
    script=script,
    max_iterations=3,
    target_score=80.0
)

# Analyze results
print(f"Total versions: {len(versions)}")
for i, version in enumerate(versions):
    if version.quality_scores:
        print(f"v{i}: {version.quality_scores.overall_score:.1f}")
```

### Iteration Algorithm

1. **Score Initial Version** (if not already scored)
2. **Check Target:** Stop if target score reached
3. **Identify Weaknesses:** Find dimensions < 70
4. **Generate Improvement:** Focus on top 3 weaknesses
5. **Score New Version:** Evaluate improved script
6. **Check Progress:** Stop if no improvement
7. **Repeat:** Until target reached or max iterations

**Stopping Conditions:**
- Target score achieved
- Max iterations reached
- No improvement detected
- No weaknesses remaining

### Testing

```bash
# Run iterator tests
python -m pytest tests/test_script_development.py::TestScriptIterator -v

# Test weakness identification
python -m pytest tests/test_script_development.py::TestScriptIterator::test_identify_weaknesses -v
```

**Test Coverage:**
- Iterator initialization
- Weakness identification logic
- Single iteration improvement
- Multi-iteration workflow
- Plateau detection
- Version tracking

## Output Files

**Versioned Scripts:**
```
Generator/scripts/
├── v0/
│   └── women/18-23/idea_001.json  # Initial
├── v1/
│   └── women/18-23/idea_001.json  # Iteration 1
├── v2/
│   └── women/18-23/idea_001.json  # Iteration 2
└── v3/
    └── women/18-23/idea_001.json  # Iteration 3
```

**Version Metadata:**
```json
{
  "script_id": "idea_001",
  "version": 2,
  "content": "...",
  "quality_scores": {
    "overall_score": 82.5
  },
  "metadata": {
    "iteration": 2,
    "weaknesses_addressed": ["pacing", "hook_strength"],
    "previous_score": 75.0
  }
}
```

## Iteration Example

**Initial (v0):**
- Engagement: 70, Clarity: 65, Pacing: 60
- Overall: 68.5

**After Iteration 1 (v1):**
- Engagement: 78, Clarity: 75, Pacing: 72
- Overall: 76.2 (+7.7)

**After Iteration 2 (v2):**
- Engagement: 85, Clarity: 82, Pacing: 80
- Overall: 83.1 (+6.9)

**Result:** Target 80.0 exceeded, stop iterating

## Related Files

**Implementation:**
- `core/script_development.py` - ScriptIterator class (lines 367-520)

**Tests:**
- `tests/test_script_development.py` - TestScriptIterator (lines 262-321)

## Notes

- Focuses on top 3 weaknesses per iteration
- Uses same LLM for consistency
- Preserves all version history
- Logs improvement deltas for monitoring
- Typically converges in 2-3 iterations
- Prevents infinite loops with plateau detection

## Next Steps

After completion:
- ✅ Scripts are iteratively refined to target quality
- ✅ Ready for GPT-4 enhancement (`05-script-04`)
- ✅ Version history available for analysis
- ✅ Weak dimensions systematically addressed
