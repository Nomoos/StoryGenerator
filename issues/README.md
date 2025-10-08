# Issues Directory

This directory contains individual issue files organized by pipeline steps. Each step has been broken down into **separate, manageable issues** with two organization approaches.

## 🎯 Choose Your Approach

### Option 1: Sequential Steps (15 Large Issues)
Traditional step-by-step breakdown. Each step is comprehensive and covers multiple tasks.

### Option 2: **Atomic Tasks - Phase-Based (64 Tasks) ⭐ RECOMMENDED**
Organized into 3 phases: **Interface → Prototype → Implementation**

Parallelizable 1-8 hour tasks optimized for team collaboration. Multiple developers can work simultaneously within each phase.

👉 **[Start with Atomic Tasks](atomic/README.md)** for faster completion

#### Phase Structure:
- **Phase 1: Interface** (4 tasks) - Define configs and structure
- **Phase 2: Prototype** (8 tasks) - Research and validate integrations  
- **Phase 3: Implementation** (52 tasks) - Build production pipeline

Each phase builds on the previous, ensuring clear dependencies and incremental value delivery.

---

## Directory Structure

```
issues/
├── README.md (this file)
├── INDEX.md (index of all issues)
├── QUICKSTART.md (usage guide)
│
├── atomic/ ⭐ NEW: 64 tasks in 3 phases (Interface → Prototype → Implementation)
│   ├── README.md (phase-based workflow guide)
│   ├── phase-1-interface/ (4 tasks - configs & structure)
│   ├── phase-2-prototype/ (8 tasks - research & validation)
│   └── phase-3-implementation/ (52 tasks in 13 groups)
│       ├── content-pipeline/
│       ├── idea-generation/
│       ├── script-development/
│       ├── scene-planning/
│       ├── audio-production/
│       ├── subtitle-creation/
│       ├── image-generation/
│       ├── video-production/
│       ├── post-production/
│       ├── quality-control/
│       ├── export-delivery/
│       ├── distribution/
│       └── analytics/
│
├── step-00-research/      # Research Prototypes (Local Only)
├── step-01-ideas/         # Ideas → Topics → Titles
├── step-02-viral-score/   # Viral Score (Titles)
├── step-03-raw-script/    # Raw Script → Score → Iterate
├── step-04-improve-script/# Improve Script by GPT/Local
├── step-05-improve-title/ # Improve Title by GPT/Local
├── step-06-scene-planning/# Scene Planning
├── step-07-voiceover/     # Voiceover
├── step-08-subtitle-timing/# Subtitle Timing
├── step-09-key-images/    # Key Images per Scene (SDXL)
├── step-10-video-generation/# Video Generation
├── step-11-post-production/# Post-Production
├── step-12-quality-checks/# Quality Checks
├── step-13-final-export/  # Final Export
└── step-14-distribution-analytics/ # Platform Distribution & Analytics
```

## Usage

### For Solo Developers (Sequential)
1. Navigate to the specific step directory you want to work on
2. Read the issue file(s) in that directory
3. Follow the checklist and acceptance criteria
4. Comment `@copilot check` in the issue when you complete a task

### For Teams (Atomic/Phase-Based) ⭐
1. **Review** [atomic/README.md](atomic/README.md) for phase-based workflow
2. **Start with Phase 1** (Interface) - Define structure and configs
3. **Move to Phase 2** (Prototype) - Validate all integrations
4. **Execute Phase 3** (Implementation) - Build production pipeline in 13 groups
5. **Track** progress using MicrostepValidator per task
6. **Complete** pipeline 5-10x faster than sequential with proper phasing

## Phase-Based Execution Benefits

- **Clear progression**: Interface → Prototype → Implementation
- **Reduced rework**: Validate before building full implementation
- **Better coordination**: Teams work within logical phase boundaries
- **10 developers**: Complete in ~11-17 days (vs 4-6 weeks sequential)
- **20 developers**: Complete in ~7-11 days with full parallelization
- **Granular progress**: Track 64 atomic completions across 3 phases
- **Resource optimization**: Match task difficulty to developer skills within each phase
- **Flexible scheduling**: Pause/resume entire phases or individual groups independently

## Related Documentation

- `/docs/MICROSTEP_VALIDATION.md` - Microstep validation system
- `/docs/GENERATOR_STRUCTURE.md` - Generator folder structure
- `/docs/PIPELINE.md` - Complete pipeline documentation
- `atomic/README.md` - Parallel workflow guide
