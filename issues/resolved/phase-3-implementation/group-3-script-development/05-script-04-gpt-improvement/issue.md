# Script: GPT/Local Improvement (v2+)

**ID:** `05-script-04-gpt-improvement`  
**Priority:** P1  
**Effort:** 3-4 hours  
**Status:** ✅ Complete

## Overview

Enhance scripts using advanced LLM models (GPT-4, Claude, etc.) for final polish. Applies sophisticated improvements to elevate language quality, emotional resonance, and storytelling while maintaining conversational accessibility.

## Dependencies

**Requires:**
- `05-script-03-iteration` - Iteratively improved scripts

**Blocks:**
- Final script production workflow
- Scene planning with polished scripts

## Acceptance Criteria

- [x] Script enhancer class implemented
- [x] Advanced LLM integration
- [x] Language elevation while maintaining tone
- [x] Emotional resonance enhancement
- [x] Rhetorical device integration
- [x] Version tracking and metadata
- [x] Comprehensive test coverage
- [x] Documentation complete

## Task Details

### Implementation

**Core Module:** `core/script_development.py`

**Key Classes:**
- `ScriptEnhancer` - Advanced enhancement with GPT-4+

**Enhancement Goals:**
- Elevate language quality
- Enhance emotional resonance
- Sharpen storytelling and narrative flow
- Strengthen transitions
- Add subtle rhetorical devices
- Maximize viewer retention
- Polish ending for impact

### Code Example

```python
from core.script_development import ScriptEnhancer, Script

# Initialize with advanced model
enhancer = ScriptEnhancer(gpt4_provider)

# Enhance script
script = Script(...)  # From iterator
enhanced = enhancer.enhance_script(script)

print(f"Enhanced to v{enhanced.version}")
print(f"Model: {enhanced.metadata['enhancement_model']}")
```

### Enhancement Process

1. **Analyze Current Script:** Identify areas for elevation
2. **Apply Enhancements:**
   - Elevate language (while staying conversational)
   - Enhance emotional impact
   - Strengthen narrative flow
   - Improve transitions
   - Add rhetorical touches
3. **Preserve Core:** Keep message, length, and tone
4. **Generate Enhanced Version:** Single pass with advanced model

### Testing

```bash
# Run enhancer tests
python -m pytest tests/test_script_development.py::TestScriptEnhancer -v

# Test enhancement workflow
python -m pytest tests/test_script_development.py::TestScriptEnhancer::test_enhance_script -v
```

**Test Coverage:**
- Enhancer initialization
- Script enhancement with GPT-4
- Version increment
- Metadata preservation
- Content transformation

## Output Files

**Enhanced Scripts:**
```
Generator/scripts/
└── gpt_improved/
    └── women/18-23/
        └── idea_001.json  # Enhanced version
```

**Enhanced Script JSON:**
```json
{
  "script_id": "idea_001",
  "version": 4,
  "content": "Enhanced script with elevated language...",
  "quality_scores": {
    "overall_score": 88.5
  },
  "metadata": {
    "enhanced": true,
    "enhancement_model": "gpt-4",
    "iteration": 3,
    "previous_version": 3
  }
}
```

## Enhancement Example

**Before Enhancement (v3, score: 83.1):**
```
Have you ever felt like giving up? Like the world is against you?

Let me tell you about Sarah. She failed her driving test five times. 
Her friends laughed. Her family worried. But Sarah kept going.

On her sixth try, she passed with flying colors. Why? Because she 
learned from every failure.

Your setbacks aren't stopping points. They're stepping stones.
```

**After Enhancement (v4, score: 88.5):**
```
Have you ever felt like giving up? Like every door slams in your face?

Listen to Sarah's journey. She failed her driving test five consecutive times.
Her friends mocked her. Her family lost faith. But Sarah? 
She never stopped believing.

On her sixth attempt, she didn't just pass—she excelled. Her secret?
She transformed each failure into a powerful lesson.

Your setbacks aren't roadblocks. They're stepping stones to greatness.
```

## Related Files

**Implementation:**
- `core/script_development.py` - ScriptEnhancer class (lines 522-602)

**Tests:**
- `tests/test_script_development.py` - TestScriptEnhancer (lines 323-345)

## Notes

- Uses temperature 0.7 for balanced creativity
- Maintains same approximate length
- Preserves core message and storyline
- Elevates without losing accessibility
- Single-pass enhancement (not iterative)
- Typically improves score by 5-10 points
- Marks scripts with `enhanced: true` in metadata

## Next Steps

After completion:
- ✅ Scripts are polished to professional quality
- ✅ Ready for title optimization (`05-script-05`)
- ✅ Can proceed to scene planning
- ✅ Enhanced versions saved separately for comparison
