# P1-High Priority: 5 Parallel Task Groups

> **⚠️ NOTE:** This planning document is now outdated. Most P1 tasks have been completed. Configuration management and logging have been enhanced with the orchestration foundation. See [HYBRID_ROADMAP.md](../../roadmaps/HYBRID_ROADMAP.md) for current status.

After P0 completion, these 5 groups can be worked on in parallel to accelerate development.

---

## 🔧 Group 1: Infrastructure Foundation (Priority: Start First)
**Status:** Mostly Complete (configuration and logging enhanced with orchestration)  
**Dependencies:** None - can start immediately  
**Why First:** Enables testing and quality control for all other work

### Tasks (3):
1. **infrastructure-testing** (8-10 hours)
   - Set up pytest framework
   - Create test templates
   - Configure test runners

2. **infrastructure-configuration** (4-6 hours)
   - Implement config management system
   - YAML/JSON configuration loading
   - Environment-specific configs

3. **infrastructure-logging** (3-4 hours)
   - Structured logging system
   - Log levels and formatting
   - Log rotation and storage

### Commands to Run:
```bash
# Navigate to infrastructure issues
cd issues/p1-high/

# Task 1: Testing Infrastructure
cd infrastructure-testing
cat issue.md
# Follow checklist in issue.md

# Task 2: Configuration Management
cd ../infrastructure-configuration
cat issue.md
# Follow checklist in issue.md

# Task 3: Logging System
cd ../infrastructure-logging
cat issue.md
# Follow checklist in issue.md

# Verify implementation
pytest tests/infrastructure/
python -m pytest tests/test_config.py
python -m pytest tests/test_logging.py
```

---

## 🏗️ Group 2: Architecture & Code Quality (Priority: Start First)
**Total Effort:** 25-36 hours  
**Dependencies:** None - can start immediately  
**Why Important:** Improves codebase maintainability and prevents technical debt

### Tasks (5):
1. **architecture-openai-api** (2-3 hours)
   - Update to OpenAI SDK v1.0+
   - Migrate deprecated API calls

2. **architecture-decoupling** (12-16 hours)
   - Decouple components
   - Implement dependency injection
   - Improve testability

3. **code-quality-error-handling** (6-8 hours)
   - Comprehensive error handling
   - Retry logic and circuit breakers
   - Error recovery strategies

4. **code-quality-code-style** (3-4 hours)
   - Set up Black formatter
   - Configure flake8 linter
   - Standardize code style

5. **code-quality-input-validation** (4-5 hours)
   - Implement Pydantic models
   - Input validation
   - Type checking

### Commands to Run:
```bash
cd issues/p1-high/

# Task 1: OpenAI API Update
cd architecture-openai-api
cat issue.md
pip install --upgrade openai
# Follow migration guide in issue

# Task 2: Architecture Decoupling
cd ../architecture-decoupling
cat issue.md
# Follow refactoring checklist

# Task 3: Error Handling
cd ../code-quality-error-handling
cat issue.md
# Implement error handling patterns

# Task 4: Code Style
cd ../code-quality-code-style
cat issue.md
pip install black flake8 isort
black --check src/
flake8 src/
isort --check-only src/

# Task 5: Input Validation
cd ../code-quality-input-validation
cat issue.md
pip install pydantic
# Implement validation models

# Verify all changes
pytest tests/architecture/
pytest tests/code_quality/
black src/
flake8 src/
```

---

## 📝 Group 3: Content Generation Pipeline (Priority: After Group 1)
**Total Effort:** 35-45 hours  
**Dependencies:** Infrastructure (Group 1) recommended  
**Focus:** Story ideas, topics, titles, and scoring

### Tasks (7 from idea-generation/):
1. Reddit story adaptation
2. LLM-based idea generation
3. Topic clustering
4. Title generation
5. Title viral scoring
6. Voice recommendation
7. Top selection

### Commands to Run:
```bash
cd issues/p1-high/idea-generation/

# View all idea generation tasks
ls -la
cat README.md

# Task 1-7: Follow each issue sequentially
for issue in */issue.md; do
  echo "=== Processing $issue ==="
  cat "$issue"
  # Implement according to issue specs
done

# Run idea generation pipeline
cd ../../..
python -m src.scripts.generate_ideas --gender women --age 18-23

# Verify outputs
ls -la data/Generator/ideas/women/18-23/
ls -la data/Generator/topics/women/18-23/
ls -la data/Generator/titles/women/18-23/
ls -la data/Generator/scores/women/18-23/

# Run tests
pytest tests/PrismQ/Pipeline/test_idea_generation.py
```

---

## 🎬 Group 4: Script & Scene Development (Priority: After Group 3)
**Total Effort:** 30-40 hours  
**Dependencies:** Content Generation (Group 3) must complete first  
**Focus:** Scripts, scenes, and audio preparation

### Tasks (10):
**Script Development (5 tasks):**
1. Raw script generation
2. Script scoring
3. Iterative improvement
4. GPT-based enhancement
5. Title optimization

**Scene Planning (3 tasks):**
6. Beat sheet creation
7. Shot list generation
8. Draft subtitle preparation

**Audio Production (2 tasks):**
9. TTS generation
10. Audio normalization

### Commands to Run:
```bash
cd issues/p1-high/

# Script Development Tasks (1-5)
cd script-development/
cat README.md
ls -la

for issue in */issue.md; do
  echo "=== Script Task: $issue ==="
  cat "$issue"
done

# Scene Planning Tasks (6-8)
cd ../scene-planning/
cat README.md

for issue in */issue.md; do
  echo "=== Scene Task: $issue ==="
  cat "$issue"
done

# Audio Production Tasks (9-10)
cd ../audio-production/
cat README.md

for issue in */issue.md; do
  echo "=== Audio Task: $issue ==="
  cat "$issue"
done

# Run script development pipeline
cd ../../..
python -m src.scripts.generate_scripts --title "Top Title 1" --gender women --age 18-23

# Run scene planning
python -m src.scripts.plan_scenes --script-id script_001

# Run audio production
python -m src.scripts.generate_audio --script-id script_001

# Verify outputs
ls -la data/Generator/scripts/*/women/18-23/
ls -la data/Generator/scenes/json/women/18-23/
ls -la data/Generator/audio/*/women/18-23/

# Run tests
pytest tests/PrismQ/Pipeline/test_script_development.py
pytest tests/PrismQ/Pipeline/test_scene_planning.py
pytest tests/PrismQ/Pipeline/test_audio_production.py
```

---

## 🎨 Group 5: Visual & Final Production (Priority: After Group 4)
**Total Effort:** 45-60 hours  
**Dependencies:** Script & Scene Development (Group 4) must complete first  
**Focus:** Images, videos, post-production, quality control

### Tasks (18):
**Subtitle Creation (2 tasks):**
1. Forced alignment with Whisper
2. Scene-to-subtitle mapping

**Image Generation (4 tasks):**
3. Prompt builder
4. Keyframe generation (Batch A)
5. Keyframe generation (Batch B)
6. Selection and quality assessment

**Video Production (3 tasks):**
7. LTX-Video generation
8. Frame interpolation
9. Variant selection

**Post-Production (6 tasks):**
10. Crop and resize
11. Subtitle burn-in
12. Background music/SFX
13. Concatenation
14. Transitions
15. Color grading

**Quality Control (3 tasks):**
16. Automated quality checks
17. Device testing
18. QC report generation

### Commands to Run:
```bash
cd issues/p1-high/

# Subtitle Creation (1-2)
cd subtitle-creation/
cat README.md

for issue in */issue.md; do
  echo "=== Subtitle Task: $issue ==="
  cat "$issue"
done

python -m src.scripts.align_subtitles --audio-id audio_001

# Image Generation (3-6)
cd ../image-generation/
cat README.md

for issue in */issue.md; do
  echo "=== Image Task: $issue ==="
  cat "$issue"
done

python -m src.scripts.generate_keyframes --scene-id scene_001

# Video Production (7-9)
cd ../video-production/
cat README.md

for issue in */issue.md; do
  echo "=== Video Task: $issue ==="
  cat "$issue"
done

python -m src.scripts.generate_video --keyframes keyframes_001

# Post-Production (10-15)
cd ../post-production/
cat README.md

for issue in */issue.md; do
  echo "=== Post-Production Task: $issue ==="
  cat "$issue"
done

python -m src.scripts.post_process --video-id video_001

# Quality Control (16-18)
cd ../quality-control/
cat README.md

for issue in */issue.md; do
  echo "=== QC Task: $issue ==="
  cat "$issue"
done

python -m src.scripts.quality_check --video-id video_001

# Verify final outputs
ls -la data/Generator/subtitles/*/women/18-23/
ls -la data/Generator/images/*/women/18-23/
ls -la data/Generator/videos/*/women/18-23/
ls -la data/Generator/final/women/18-23/

# Run comprehensive tests
pytest tests/PrismQ/Pipeline/test_subtitle_creation.py
pytest tests/PrismQ/Pipeline/test_image_generation.py
pytest tests/PrismQ/Pipeline/test_video_production.py
pytest tests/PrismQ/Pipeline/test_post_production.py
pytest tests/PrismQ/Pipeline/test_quality_control.py
```

---

## 📊 Parallel Execution Summary

### Optimal Parallelization Strategy:

```
┌─────────────────────────────────────────────────────────────┐
│ Timeline View                                               │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│ Week 1-2:  ┌──────────────┐  ┌─────────────────────────┐  │
│            │ Group 1:     │  │ Group 2:                │  │
│            │ Infrastructure│  │ Architecture & Quality  │  │
│            └──────────────┘  └─────────────────────────┘  │
│            (15-20 hours)      (25-36 hours)              │
│                 ↓                      ↓                   │
│ Week 3-4:       └──────────┬──────────┘                   │
│                            ↓                               │
│                ┌─────────────────────────┐                │
│                │ Group 3:                │                │
│                │ Content Generation      │                │
│                └─────────────────────────┘                │
│                (35-45 hours)                              │
│                            ↓                               │
│ Week 5-6:      ┌─────────────────────────┐                │
│                │ Group 4:                │                │
│                │ Script & Scene Dev      │                │
│                └─────────────────────────┘                │
│                (30-40 hours)                              │
│                            ↓                               │
│ Week 7-9:      ┌─────────────────────────┐                │
│                │ Group 5:                │                │
│                │ Visual & Final Prod     │                │
│                └─────────────────────────┘                │
│                (45-60 hours)                              │
└─────────────────────────────────────────────────────────────┘
```

### Quick Start Commands by Group:

#### Start All Groups (in separate terminals/sessions):

```bash
# Terminal 1: Infrastructure (Group 1)
cd issues/p1-high/infrastructure-testing && cat issue.md

# Terminal 2: Architecture (Group 2)
cd issues/p1-high/architecture-openai-api && cat issue.md

# Wait for Group 1 & 2 to complete, then:

# Terminal 3: Content Generation (Group 3)
cd issues/p1-high/idea-generation && cat README.md

# Wait for Group 3 to complete, then:

# Terminal 4: Script Development (Group 4)
cd issues/p1-high/script-development && cat README.md

# Wait for Group 4 to complete, then:

# Terminal 5: Visual Production (Group 5)
cd issues/p1-high/image-generation && cat README.md
```

### Testing Commands for Each Group:

```bash
# After Group 1 (Infrastructure)
pytest tests/infrastructure/

# After Group 2 (Architecture & Quality)
pytest tests/architecture/
pytest tests/code_quality/
black --check src/
flake8 src/

# After Group 3 (Content Generation)
pytest tests/PrismQ/Pipeline/test_idea_generation.py
pytest tests/PrismQ/Pipeline/test_topic_clustering.py
pytest tests/PrismQ/Pipeline/test_title_generation.py

# After Group 4 (Script & Scene)
pytest tests/PrismQ/Pipeline/test_script_development.py
pytest tests/PrismQ/Pipeline/test_scene_planning.py
pytest tests/PrismQ/Pipeline/test_audio_production.py

# After Group 5 (Visual & Final)
pytest tests/PrismQ/Pipeline/test_subtitle_creation.py
pytest tests/PrismQ/Pipeline/test_image_generation.py
pytest tests/PrismQ/Pipeline/test_video_production.py
pytest tests/PrismQ/Pipeline/test_post_production.py
pytest tests/PrismQ/Pipeline/test_quality_control.py

# Full pipeline test (after all groups)
pytest tests/PrismQ/Pipeline/test_full_pipeline.py
```

---

## 🎯 Task Assignment Recommendations

### For Solo Developer:
1. Complete Group 1 first (foundation)
2. Complete Group 2 (improves all future work)
3. Then proceed Groups 3 → 4 → 5 sequentially

### For 2-Person Team:
- **Person A:** Groups 1 & 3 & 5 (infrastructure + content + visual)
- **Person B:** Groups 2 & 4 (architecture + scripts)

### For 3-Person Team:
- **Person A:** Group 1 + Group 2 (foundation)
- **Person B:** Group 3 (content generation)
- **Person C:** Group 4 → Group 5 (production pipeline)

### For 5-Person Team (Maximum Parallelization):
- **Person A:** Group 1 - Infrastructure
- **Person B:** Group 2 - Architecture & Quality
- **Person C:** Group 3 - Content Generation (starts after A)
- **Person D:** Group 4 - Script & Scene Dev (starts after C)
- **Person E:** Group 5 - Visual Production (starts after D)

---

## 📋 Progress Tracking Commands

```bash
# Check overall progress
grep -r "Status:" issues/p1-high/*/issue.md | grep -v "NOT STARTED"

# Generate progress report
python scripts/generate_progress_report.py --priority P1

# List completed tasks
find issues/p1-high -name "issue.md" -exec grep -l "Status: COMPLETE" {} \;

# Count remaining tasks
find issues/p1-high -name "issue.md" -exec grep -l "Status: NOT STARTED" {} \; | wc -l

# Estimate remaining effort
python scripts/estimate_remaining_effort.py --priority P1
```

---

**Total Estimated Effort:** 150-200 hours  
**Optimal Timeline:** 8-10 weeks (with 2-3 developers working in parallel)  
**Dependencies Enforced:** Groups 3→4→5 must be sequential, Groups 1&2 can be parallel
