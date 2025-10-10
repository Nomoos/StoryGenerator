# Script: Title Improvement

**ID:** `05-script-05-title-improvement`  
**Priority:** P1  
**Effort:** 2-3 hours  
**Status:** ✅ Complete

## Overview

Generate multiple optimized title variants for video scripts. Creates titles optimized for clickability, SEO, and platform algorithms using various proven formulas and styles.

## Dependencies

**Requires:**
- `05-script-04-gpt-improvement` - Enhanced scripts
- Final script content for context

**Blocks:**
- Video publishing workflow
- Thumbnail creation (uses titles)

## Acceptance Criteria

- [x] Title optimizer class implemented
- [x] Multiple variant generation (5+ per script)
- [x] Various title styles supported
- [x] Rationale for each variant
- [x] Character limit validation (60 chars)
- [x] Comprehensive test coverage
- [x] Documentation complete

## Task Details

### Implementation

**Core Module:** `core/script_development.py`

**Key Classes:**
- `TitleOptimizer` - Generates title variants

**Title Styles:**
1. **Curiosity Gap** - "What Happens When..."
2. **How-To/Value** - "How I Discovered..."
3. **Shocking/Controversial** - "Nobody Talks About..."
4. **Listicle/Number** - "3 Secrets About..."
5. **Personal Story** - "I Tried... and This Happened"

### Code Example

```python
from core.script_development import TitleOptimizer, Script

# Initialize
optimizer = TitleOptimizer(llm_provider)

# Generate variants
script = Script(...)  # Enhanced script
variants = optimizer.generate_title_variants(
    script=script,
    num_variants=5
)

# Review variants
for variant in variants:
    print(f"{variant['style']}: {variant['title']}")
    print(f"  Rationale: {variant['rationale']}\n")
```

### Title Generation Process

1. **Analyze Script:** Extract key themes and hooks
2. **Generate Variants:** Create 5+ titles in different styles
3. **Optimize for Platforms:**
   - Under 60 characters for optimal display
   - Keywords for SEO
   - Emotional triggers for engagement
4. **Provide Rationale:** Explain why each title works

### Testing

```bash
# Run optimizer tests
python -m pytest tests/test_script_development.py::TestTitleOptimizer -v

# Test variant generation
python -m pytest tests/test_script_development.py::TestTitleOptimizer::test_generate_title_variants -v
```

**Test Coverage:**
- Optimizer initialization
- Title variant generation
- Multiple style coverage
- Response parsing
- Rationale extraction

## Output Files

**Title Variants JSON:**
```
Generator/titles/improved/
└── women/18-23/
    └── idea_001_titles.json
```

**JSON Structure:**
```json
{
  "script_id": "idea_001",
  "original_title": "Never Give Up",
  "variants": [
    {
      "title": "What Happens When You Fail 5 Times?",
      "style": "Curiosity Gap",
      "rationale": "Creates intrigue and promises revelation"
    },
    {
      "title": "How I Turned 5 Failures Into Success",
      "style": "How-To/Value",
      "rationale": "Offers transformation story and actionable value"
    },
    {
      "title": "Nobody Talks About Failing This Much",
      "style": "Shocking/Controversial",
      "rationale": "Breaks taboo, creates curiosity"
    },
    {
      "title": "3 Lessons From Failing 5 Times",
      "style": "Listicle/Number",
      "rationale": "Specific promise, easy to digest"
    },
    {
      "title": "I Failed 5 Times and Here's What Happened",
      "style": "Personal Story",
      "rationale": "Authentic, relatable personal journey"
    }
  ],
  "generated_at": "2025-01-11T10:45:00"
}
```

## Title Examples

**Original:** "Overcoming Adversity"

**Optimized Variants:**
1. **Curiosity:** "What Nobody Tells You About Failure"
2. **How-To:** "How I Transformed 5 Failures Into Success"
3. **Shocking:** "Why Failing Is Better Than You Think"
4. **Number:** "5 Times I Failed Before I Succeeded"
5. **Personal:** "I Failed More Than Anyone—Here's Why"

## Title Best Practices

**Do:**
- Keep under 60 characters
- Use emotional triggers
- Promise value or revelation
- Be specific when possible
- Use numbers and lists
- Create curiosity gaps
- Be authentic

**Avoid:**
- Clickbait without substance
- ALL CAPS (unless strategic)
- Misleading promises
- Generic phrasing
- Overly long titles

## Related Files

**Implementation:**
- `core/script_development.py` - TitleOptimizer class (lines 604-711)

**Tests:**
- `tests/test_script_development.py` - TestTitleOptimizer (lines 347-391)

## Notes

- Uses high temperature (0.9) for creativity
- Generates diverse style coverage
- Includes rationale for each variant
- Platform-optimized (60 char limit)
- Can be A/B tested for performance
- Should align with script content
- Consider SEO keywords for YouTube

## Next Steps

After completion:
- ✅ Multiple title options ready for A/B testing
- ✅ Scripts and titles ready for scene planning
- ✅ Can select best-performing title variant
- ✅ Complete script development pipeline finished
