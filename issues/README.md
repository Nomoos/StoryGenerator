# Issues Directory

This directory contains issue tracking for the C# implementation of StoryGenerator.

## 🎯 Organization Approach

### **Atomic Tasks - Phase-Based (64 Tasks) ⭐ RECOMMENDED**
Organized into 3 phases: **Interface → Prototype → Implementation**

Parallelizable 1-8 hour tasks optimized for team collaboration. Multiple developers can work simultaneously within each phase.

👉 **[Start with Atomic Tasks](atomic/README.md)** for faster completion

#### Phase Structure:
- **Phase 1: Interface** (4 tasks) - Define configs and structure
- **Phase 2: Prototype** (3 tasks) - Research and validate C# integrations  
- **Phase 3: Implementation** (52 tasks) - Build production pipeline

Each phase builds on the previous, ensuring clear dependencies and incremental value delivery.

> **Note:** The Python-based sequential step issues (step-00 through step-14) have been moved to `obsolete/issues/` as the C# implementation is now the primary codebase.

---

## Directory Structure

```
issues/
├── README.md (this file)
├── INDEX.md (index of all issues)
├── QUICKSTART.md (usage guide)
│
├── atomic/ ⭐ C# Implementation: 64 tasks in 3 phases
│   ├── README.md (phase-based workflow guide)
│   ├── phase-1-interface/ (4 tasks - configs & structure)
│   ├── phase-2-prototype/ (3 tasks - C# research & validation)
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
├── csharp-master-roadmap/         # C# Implementation Master Roadmap
├── csharp-phase3-complete-generators/  # C# Phase 3 Tasks
├── csharp-phase4-pipeline-orchestration/  # C# Phase 4 Tasks
└── csharp-video-generators/       # C# Video Generation Tasks
```

**Obsolete Issues** (Python-based sequential steps) are now in `obsolete/issues/step-XX/`

## Usage

### For C# Development (Atomic/Phase-Based) ⭐
1. **Review** [atomic/README.md](atomic/README.md) for phase-based workflow
2. **Start with Phase 1** (Interface) - Define structure and configs
3. **Then Phase 2** (Prototype) - Validate C# integrations
4. **Finally Phase 3** (Implementation) - Build production pipeline
5. Comment `@copilot check` when completing tasks

### For Historical Reference (Python Steps)
Python-based sequential step issues have been moved to `obsolete/issues/step-XX/` for historical reference only. They are no longer actively maintained.
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
