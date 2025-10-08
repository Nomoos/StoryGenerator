# Issues Directory

This directory contains individual issue files organized by pipeline steps. Each step has been broken down into **separate, manageable issues** with two organization approaches.

## 🎯 Choose Your Approach

### Option 1: Sequential Steps (15 Large Issues)
Traditional step-by-step breakdown. Each step is comprehensive and covers multiple tasks.

### Option 2: **Atomic Tasks (64 Independent Issues) ⭐ RECOMMENDED**
Parallelizable 1-8 hour tasks optimized for team collaboration. Multiple developers can work simultaneously.

👉 **[Start with Atomic Tasks](atomic/README.md)** for faster completion

---

## Directory Structure

```
issues/
├── README.md (this file)
├── INDEX.md (index of all issues)
├── QUICKSTART.md (usage guide)
│
├── atomic/ ⭐ NEW: 64 parallelizable tasks
│   ├── README.md (parallel workflow guide)
│   ├── 00-setup-01-repo-structure/
│   ├── 00-setup-02-config-files/
│   ├── 01-research-01-ollama-client/
│   ├── 02-content-01-reddit-scraper/
│   ├── ... (59 more atomic tasks)
│   └── 15-analytics-04-optimization/
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

### For Teams (Atomic/Parallel) ⭐
1. **Review** [atomic/README.md](atomic/README.md) for parallel workflow
2. **Assign** tasks from different priority waves to team members
3. **Execute** tasks in parallel (P0 → P1 → P2)
4. **Track** progress using MicrostepValidator per task
5. **Complete** pipeline 5-10x faster than sequential

## Parallel Execution Benefits

- **10 developers**: Complete in ~4-5 days (vs 4-6 weeks sequential)
- **Clear dependencies**: Know exactly what can run in parallel
- **Granular progress**: Track 64 atomic completions instead of 15
- **Resource optimization**: Match task difficulty to developer skills
- **Flexible scheduling**: Pause/resume individual tasks independently

## Related Documentation

- `/docs/MICROSTEP_VALIDATION.md` - Microstep validation system
- `/docs/GENERATOR_STRUCTURE.md` - Generator folder structure
- `/docs/PIPELINE.md` - Complete pipeline documentation
- `atomic/README.md` - Parallel workflow guide
