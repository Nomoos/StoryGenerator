# Issues Directory

This directory contains issue tracking for the C# implementation of StoryGenerator, organized by priority and status for optimal workflow management.

## 🎯 Organization by Priority & Status

Issues are organized following **best practices** and **test-driven development (TDD)** principles:

### ✅ Resolved Issues
**Location:** `resolved/`

Completed tasks with ✅ Complete status. Moved here to keep active issues focused on current work.
- **Phase 1:** 3/3 tasks complete (Interface & setup)
- **Phase 2:** 3/3 tasks complete (C# prototypes)
- **P0 Security:** 2/2 tasks complete (Security fixes)
- **P0 C# Phase 3:** 1/1 task complete (Generator implementation)
- **P0 Content Pipeline:** 5/6 tasks complete (Content sourcing)

👉 **[View Resolved Issues](resolved/README.md)**

### 🔴 P0 - Critical Priority
**Location:** `p0-critical/`

**Nearly complete.** Only 1 task remaining (quality scorer).
- ⏳ Content quality assessment (Not Started)

**Completed (moved to resolved/):**
- ✅ Security fixes (2 tasks)
- ✅ C# Phase 3 generator completion
- ✅ Content pipeline foundation (5 tasks)

👉 **[View P0 Critical Issues](p0-critical/README.md)**

### 🟡 P1 - High Priority
**Location:** `p1-high/`

**Next in queue.** Core pipeline implementation tasks. Start after P0 completion.
- Pipeline orchestration
- 41 implementation tasks across 10 groups
- Idea generation → Scripts → Scenes → Audio → Video → Export

👉 **[View P1 High Priority Issues](p1-high/README.md)**

### 🟢 P2 - Medium Priority
**Location:** `p2-medium/`

**Future work.** Publishing, analytics, and optimization. Begin after core pipeline works.
- Platform distribution (YouTube, TikTok, Instagram, Facebook)
- Analytics and performance tracking
- Advanced video features

👉 **[View P2 Medium Priority Issues](p2-medium/README.md)**

## 📊 Status Overview

| Priority | Status | Task Count | Estimated Effort |
|----------|--------|------------|------------------|
| ✅ Resolved | Complete | 14 tasks | ~60 hours (done) |
| 🔴 P0 Critical | Nearly Done | 1 task | 2-3 hours |
| 🟡 P1 High | Next | 50 tasks | 160-250 hours |
| 🟢 P2 Medium | Planned | 16 tasks | 110-135 hours |
| **Total** | | **81 tasks** | **272-388 hours** |

> **Note:** The Python-based sequential step issues (step-00 through step-14) have been moved to `obsolete/issues/` as the C# implementation is now the primary codebase.

---

## Directory Structure

```
issues/
├── README.md (this file)
├── INDEX.md (issue index)
├── QUICKSTART.md (getting started guide)
│
├── resolved/ ✅ Completed issues (14 tasks)
│   ├── phase-1-interface/ (Setup complete)
│   ├── phase-2-prototype/ (Prototypes complete)
│   ├── p0-security/ (Security fixes complete)
│   ├── p0-csharp-phase3/ (Generator implementation complete)
│   └── p0-content-pipeline/ (5/6 content tasks complete)
│
├── p0-critical/ 🔴 Critical priority (1 task, ~2-3 hours)
│   └── content-pipeline/
│       └── 02-content-03-quality-scorer/ (Not Started)
│
├── p1-high/ 🟡 High priority (50 tasks, ~160-250 hours)
│   ├── csharp-phase4-pipeline-orchestration/
│   ├── idea-generation/
│   ├── script-development/
│   ├── scene-planning/
│   ├── audio-production/
│   ├── subtitle-creation/
│   ├── image-generation/
│   ├── video-production/
│   ├── post-production/
│   ├── quality-control/
│   └── export-delivery/
│
├── p2-medium/ 🟢 Medium priority (16 tasks, ~110-135 hours)
│   ├── csharp-video-generators/
│   ├── distribution/
│   └── analytics/
│
├── atomic/ (Legacy phase organization - kept for reference)
│   ├── README.md
│   ├── phase-1-interface/ (empty - moved to resolved/)
│   └── phase-2-prototype/ (empty - moved to resolved/)
│
└── csharp-master-roadmap/ (Overall project roadmap)
```

**Priority-Based Organization:** Issues are now organized by priority (P0, P1, P2) rather than phase, enabling better focus on critical path items and supporting test-driven development practices.

## Usage

### Priority-Based Development Workflow

#### 1. Start with P0 - Critical Priority 🔴
```bash
cd issues/p0-critical/
# Review README.md for overview
# Pick a task and follow TDD practices
```

**Focus:** Complete ALL P0 tasks before moving to P1. These are blockers.

#### 2. Move to P1 - High Priority 🟡
```bash
cd issues/p1-high/
# Review task groups
# Many tasks can be parallelized
```

**Focus:** Core pipeline implementation. Can work on multiple groups simultaneously.

#### 3. Tackle P2 - Medium Priority 🟢
```bash
cd issues/p2-medium/
# Platform distribution
# Analytics and optimization
```

**Focus:** Publishing and analytics features after core pipeline works.

### Test-Driven Development (TDD) Workflow

For each task:
1. **Read acceptance criteria** in issue.md
2. **Write tests first** (Red phase)
   ```bash
   # Create test file
   # Define expected behavior
   # Run tests - they should fail
   ```
3. **Implement minimal code** (Green phase)
   ```bash
   # Write just enough code to pass tests
   # Keep it simple
   ```
4. **Refactor and improve** (Refactor phase)
   ```bash
   # Clean up code
   # Improve design
   # Tests still pass
   ```
5. **Document and review**
   ```bash
   # Add XML documentation
   # Submit for peer review
   ```

### Resolved Issues (Historical Reference)

For completed work and examples:
```bash
cd issues/resolved/
# View completed implementations
# Use as reference for similar tasks
```
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
