# Issues Quick Start Guide

**Last Updated:** 2025-10-10 (Verification Update)  
**Status:** ⚠️ Implementation complete, testing needed

This guide helps you navigate and use the individual issue files for the StoryGenerator pipeline.

## ⚠️ Current Status (2025-10-10)

**Environment Verified:**
- ✅ Python 3.12.3 installed
- ✅ .NET 9.0.305 installed
- ❌ Build errors present (24 nullable reference issues in Research project)

**Implementation:**
- ✅ Steps 00-13: Code complete
- ❌ Step 14: Not started (P2/Phase 4)
- ⚠️ Testing: All steps need verification with sample data

**Documentation:**
- ✅ [VERIFICATION_REPORT.md](../VERIFICATION_REPORT.md) - Comprehensive findings
- ✅ [POST_ROADMAP_TRACKER.md](../POST_ROADMAP_TRACKER.md) - Production workflow
- ✅ [PIPELINE_STATUS.md](../obsolete/issues/PIPELINE_STATUS.md) - Quick status
- ⚠️ Step READMEs: 2 of 15 complete

**See [VERIFICATION_REPORT.md](../VERIFICATION_REPORT.md) for complete details.**

---

## 📂 What's Been Created

The main issue has been broken down into **15 separate, detailed issue files**, organized by pipeline step:

**Note:** Step folders are currently in `obsolete/issues/` directory structure.

```
obsolete/issues/
├── STEP_README_TEMPLATE.md     # Template for step documentation
├── PIPELINE_STATUS.md          # Quick status reference
├── step-00-research/           # Research prototypes (Python & C#)
│   ├── issue.md
│   └── README.md ✅
├── step-01-ideas/              # Ideas → Topics → Titles generation  
│   ├── issue.md
│   └── README.md ✅
├── step-02-viral-score/        # Title scoring and voice selection
│   └── issue.md
├── step-03-raw-script/         # Script generation and iteration
│   └── issue.md
├── step-04-improve-script/     # Script improvement (GPT/Local)
│   └── issue.md
├── step-05-improve-title/      # Title variant generation
│   └── issue.md
├── step-06-scene-planning/     # Shot planning and beat-sheets
│   └── issue.md
├── step-07-voiceover/          # Audio generation and normalization
│   └── issue.md
├── step-08-subtitle-timing/    # Subtitle alignment and timing
│   └── issue.md
├── step-09-key-images/         # SDXL keyframe generation
│   └── issue.md
├── step-10-video-generation/   # Video clip generation
│   └── issue.md
├── step-11-post-production/    # Assembly and effects
│   └── issue.md
├── step-12-quality-checks/     # QC and device testing
│   └── issue.md
├── step-13-final-export/       # Final export and platform prep
│   └── issue.md
└── step-14-distribution-analytics/  # Distribution & analytics (P2 - not started)
    └── issue.md
```

**Documentation Progress:**
- ✅ Steps 00-01: Complete READMEs with usage examples
- ⚠️ Steps 02-14: Use issue.md until READMEs created

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
# Navigate to step folder
cd obsolete/issues/step-01-ideas/

# Read detailed requirements
cat issue.md

# Read usage guide (if README exists)
cat README.md
```

**Steps with Complete Documentation:**
- ✅ [Step 00: Research](../obsolete/issues/step-00-research/README.md)
- ✅ [Step 01: Ideas](../obsolete/issues/step-01-ideas/README.md)

Each step includes:
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
- ✅ MicrostepValidator shows VALID status (if using Python validator)
- ✅ Acceptance criteria met
- ✅ `@copilot check` passes (if using validation)

## 🔧 Environment Setup

### Check Your Environment

```bash
# Verify Python version (need 3.10+)
python3 --version
# Should show: Python 3.12.3 or higher

# Verify .NET version (need 9.0)
dotnet --version
# Should show: 9.0.305 or higher

# Check if repository builds
cd /path/to/StoryGenerator
dotnet build src/CSharp/StoryGenerator.sln
# ⚠️ Currently has 24 build errors in Research project
```

### Known Issues

**Build Errors (as of 2025-10-10):**
- Location: `src/CSharp/StoryGenerator.Research/`
- Issue: 24 nullable reference type errors
- Impact: Blocks testing of research prototypes
- Files: OllamaClient.cs, WhisperClient.cs, FFmpegClient.cs, Orchestrator.cs
- Status: ❌ Needs fixing

**Workaround:** Most pipeline steps don't depend on Research project and will build successfully.

## 🚀 Actual Working Commands (2025-10-10)

### Build the Solution (Excluding Research)

```bash
# Build main pipeline (works)
dotnet build src/CSharp/StoryGenerator.CLI/StoryGenerator.CLI.csproj

# Run CLI to see available commands
dotnet run --project src/CSharp/StoryGenerator.CLI
```

### Run Tests

```bash
# Run C# tests (works)
dotnet test src/CSharp/StoryGenerator.Tests/

# Run specific test category
dotnet test --filter "Category=IdeaGeneration"

# Python tests (if available)
cd /path/to/StoryGenerator
pytest tests/
```

### Execute Pipeline Steps

**Note:** These commands are examples based on the implementation. Actual CLI may differ - verify with `dotnet run --project src/CSharp/StoryGenerator.CLI -- --help`

```bash
# Step 01: Generate ideas (example)
dotnet run --project src/CSharp/StoryGenerator.CLI -- ideas generate \
  --segment women \
  --age 18-23 \
  --count 20

# Step 03: Generate script (example)
dotnet run --project src/CSharp/StoryGenerator.CLI -- script generate \
  --input ideas.json \
  --output script.txt

# Python scripts (direct execution)
python3 src/scripts/whisper_asr.py --input audio.wav --output transcription.json
python3 src/scripts/sdxl_generation.py --prompt "A beautiful landscape" --output image.png
python3 src/scripts/ltx_synthesis.py --frames frames.json --output video.mp4
```

### Verify Step Implementation

```bash
# Check if a step's code exists
ls -la src/CSharp/StoryGenerator.Pipeline/Stages/

# Check Python implementations
ls -la core/PrismQ/Pipeline/
ls -la src/scripts/

# View step documentation
cat obsolete/issues/step-01-ideas/README.md
```

## 📚 Documentation Resources

### Verification Reports
- [VERIFICATION_REPORT.md](../VERIFICATION_REPORT.md) - Complete verification findings
- [POST_ROADMAP_TRACKER.md](../POST_ROADMAP_TRACKER.md) - Production/distribution workflow  
- [PIPELINE_STATUS.md](../obsolete/issues/PIPELINE_STATUS.md) - Quick status reference

### Implementation Guides
- [HYBRID_ROADMAP.md](../docs/roadmaps/HYBRID_ROADMAP.md) - Project roadmap with verification status
- [PIPELINE_GUIDE.md](../src/CSharp/PIPELINE_GUIDE.md) - C# pipeline architecture
- [CLI_USAGE.md](../src/CSharp/CLI_USAGE.md) - CLI usage guide (if exists)

### Step Documentation
- [Step 00: Research](../obsolete/issues/step-00-research/README.md) ✅ Complete
- [Step 01: Ideas](../obsolete/issues/step-01-ideas/README.md) ✅ Complete
- Steps 02-14: Use issue.md files until READMEs created

## 🚀 Getting Started Now

### For New Users

```bash
# 1. Clone and navigate to repository
git clone https://github.com/Nomoos/StoryGenerator.git
cd StoryGenerator

# 2. Check environment
python3 --version  # Need 3.10+
dotnet --version   # Need 9.0+

# 3. Install dependencies
pip install -r requirements.txt
dotnet restore src/CSharp/StoryGenerator.sln

# 4. Try building (expect Research errors)
dotnet build src/CSharp/StoryGenerator.CLI/

# 5. Read verification report
cat VERIFICATION_REPORT.md

# 6. Pick a step to work on
cd obsolete/issues/step-01-ideas/
cat README.md
```

### For Contributors

```bash
# 1. Read verification status
cat VERIFICATION_REPORT.md
cat obsolete/issues/PIPELINE_STATUS.md

# 2. Pick a step needing documentation
# Steps 02-14 need READMEs

# 3. Copy template
cp obsolete/issues/STEP_README_TEMPLATE.md \
   obsolete/issues/step-XX-name/README.md

# 4. Fill in details following Step 00 and 01 examples
# See: obsolete/issues/step-00-research/README.md
# See: obsolete/issues/step-01-ideas/README.md

# 5. Test your documentation
# Follow your own README to verify it works
```

---

**Remember**: These issues are designed to be **comprehensive** and **self-contained**. Each one has everything you need to complete that step successfully!
