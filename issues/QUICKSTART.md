# Issues Quick Start Guide

This guide helps you navigate and use the individual issue files for the StoryGenerator pipeline.

## 📂 What's Been Created

The main issue has been broken down into **14 separate, detailed issue files**, organized by pipeline step:

```
docs/issues/
├── README.md              # Directory overview
├── INDEX.md               # Complete navigation index
├── step-00-research/      # Research prototypes (Python & C#)
├── step-01-ideas/         # Ideas → Topics → Titles generation
├── step-02-viral-score/   # Title scoring and voice selection
├── step-03-raw-script/    # Script generation and iteration
├── step-04-improve-script/# Script improvement (GPT/Local)
├── step-05-improve-title/ # Title variant generation
├── step-06-scene-planning/# Shot planning and beat-sheets
├── step-07-voiceover/     # Audio generation and normalization
├── step-08-subtitle-timing/# Subtitle alignment and timing
├── step-09-key-images/    # SDXL keyframe generation
├── step-10-video-generation/# Video clip generation
├── step-11-post-production/# Assembly and effects
├── step-12-quality-checks/# QC and device testing
└── step-13-final-export/  # Final export and platform prep
```

## 🎯 How to Use These Issues

### 1. Start with the INDEX.md

```bash
cat docs/issues/INDEX.md
```

This provides:
- Overview of all 14 steps
- Dependencies between steps
- Estimated duration per step
- Quick navigation links

### 2. Navigate to a Specific Step

```bash
cd docs/issues/step-01-ideas/
cat issue.md
```

Each issue includes:
- **Status**: Current state (Not Started, In Progress, Complete)
- **Priority**: Importance level (High, Medium, Low)
- **Dependencies**: Which steps must be completed first
- **Overview**: What this step accomplishes
- **Checklist**: Detailed tasks with checkboxes
- **Schemas**: JSON/YAML structure examples
- **Acceptance Criteria**: Definition of "done"
- **Related Files**: Where artifacts should be saved
- **Validation**: How to verify completion

### 3. Work Through the Checklist

Each issue has detailed checklists. For example, Step 1:

```markdown
### 1.1 Ideas Generation
- [ ] Generate **≥20 raw ideas** per segment (markdown list)
- [ ] Save to: `/ideas/{segment}/{age}/YYYYMMDD_ideas.md`
- [ ] Use local LLM (Qwen2.5 or Llama3.1) for generation
- [ ] Ideas should be age-appropriate and gender-relevant
```

### 4. Use MicrostepValidator for Tracking

```python
from Tools.MicrostepValidator import MicrostepValidator

validator = MicrostepValidator()

# Start a step
validator.update_progress(2, "started", "Beginning ideas generation")

# Create artifacts
validator.create_artifact(2, "ideas.md", content, gender="women", age="18-23")

# Mark complete
validator.update_progress(2, "completed", "Generated 20 ideas", 
                         gender="women", age="18-23",
                         artifacts=["ideas.md"])

# Validate
validator.validate_step(2, gender="women", age="18-23")
```

### 5. Comment `@copilot check` When Complete

After finishing a step, comment in your PR or issue:

```
@copilot check
```

This triggers validation and provides feedback on completeness.

## 📋 Pipeline Flow

Follow steps in sequence:

```
0. Research → 1. Ideas → 2. Viral Score → 3. Raw Script → 
4. Improve Script → 5. Improve Title → 6. Scene Planning → 
7. Voiceover → 8. Subtitle Timing → 9. Key Images → 
10. Video Generation → 11. Post-Production → 12. Quality Checks → 
13. Final Export
```

## 🎬 Target Audience

Each step processes all combinations:
- **Genders**: women, men
- **Ages**: 10-13, 14-17, 18-23
- **Total**: 6 combinations
- **Videos**: 30 final (5 titles × 6 combinations)

## 📊 What Each Issue Contains

### Structure
```markdown
# Step N: Title

**Status:** Not Started
**Priority:** High
**Dependencies:** Previous steps

## Overview
Brief description

## Target Audience
Segments and age groups

## Checklist
- [ ] Task 1
- [ ] Task 2

## Schemas
JSON/YAML examples

## Acceptance Criteria
How to verify completion

## Related Files
Paths to artifacts

## Validation
Use @copilot check
```

### Example Paths
- Input: `/scripts/gpt_improved/women/18-23/`
- Output: `/audio/tts/women/18-23/`
- Config: `/config/pipeline.yaml`

## 🔧 Key Configuration Files

All steps reference:
- `/config/pipeline.yaml` - Models, paths, settings
- `/config/scoring.yaml` - Viral scoring rubric
- `/config/schemas/` - JSON schemas

## 📚 Documentation References

Each issue links to:
- `/docs/MICROSTEP_VALIDATION.md` - Validation system
- `/docs/GENERATOR_STRUCTURE.md` - Folder organization
- `/docs/PIPELINE.md` - Pipeline details

## ⚡ Quick Commands

### View all steps
```bash
cat docs/issues/INDEX.md
```

### Work on a specific step
```bash
cd docs/issues/step-01-ideas/
cat issue.md
# Follow the checklist...
```

### Validate your work
```python
python -c "
from Tools.MicrostepValidator import copilot_check_microstep
copilot_check_microstep(2, gender='women', age='18-23')
"
```

### Track progress
```bash
# View progress for a step
cat src/Generator/ideas/women/18-23/progress.md
```

## 📈 Statistics

- **Total Issues**: 14 steps
- **Total Lines**: 2,466 lines of documentation
- **Total Files**: 16 markdown files
- **Coverage**: Complete pipeline from research to export

## 💡 Tips

1. **Read the full issue** before starting work
2. **Check dependencies** - ensure previous steps are complete
3. **Follow the checklist** - it's comprehensive for a reason
4. **Use the schemas** - they show exact format expected
5. **Track with validator** - keeps everything organized
6. **Validate when done** - ensures nothing is missed

## 🤝 Working with @copilot

When you need help:
- Reference the issue: "Based on docs/issues/step-02-viral-score/issue.md..."
- Ask specific questions: "How should I structure the title_score.json?"
- Request validation: "@copilot check"
- Get suggestions: "What's the next step after this?"

## 📝 Example Workflow

```bash
# 1. Check what to work on
cat docs/issues/INDEX.md

# 2. Navigate to step
cd docs/issues/step-02-viral-score/

# 3. Read the full issue
cat issue.md

# 4. Start work
python -c "
from Tools.MicrostepValidator import update_microstep_progress
update_microstep_progress(5, 'started', 'Beginning title scoring')
"

# 5. Follow checklist and create artifacts
# ... do the work ...

# 6. Mark complete
python -c "
from Tools.MicrostepValidator import update_microstep_progress
update_microstep_progress(5, 'completed', 'All titles scored',
                         gender='women', age='18-23',
                         artifacts=['title_scores.json', 'voice_notes.md'])
"

# 7. Validate
python -c "
from Tools.MicrostepValidator import copilot_check_microstep
copilot_check_microstep(5, gender='women', age='18-23')
"

# 8. Comment in PR/issue
# @copilot check
```

## 🎯 Success Criteria

For each step to be complete:
- ✅ All checklist items checked
- ✅ All artifacts created in correct locations
- ✅ MicrostepValidator shows VALID status
- ✅ Acceptance criteria met
- ✅ `@copilot check` passes

## 🚀 Getting Started Now

```bash
# Start with research prototypes
cd docs/issues/step-00-research/
cat issue.md

# Or jump to content generation
cd docs/issues/step-01-ideas/
cat issue.md
```

---

**Remember**: These issues are designed to be **comprehensive** and **self-contained**. Each one has everything you need to complete that step successfully!
