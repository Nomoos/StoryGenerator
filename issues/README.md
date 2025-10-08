# Issues Directory

This directory contains issue tracking for the C# implementation of StoryGenerator, organized by priority and status for optimal workflow management.

## 🎯 Organization by Priority & Status

Issues are organized following **best practices** and **test-driven development (TDD)** principles:

### ✅ Resolved Issues
**Location:** `resolved/`

Completed tasks with ✅ Complete status. Moved here to keep active issues focused on current work.
- **Phase 1:** 3/3 tasks complete (Interface & setup)
- **Phase 2:** 3/3 tasks complete (C# prototypes)

👉 **[View Resolved Issues](resolved/README.md)**

### 🔴 P0 - Critical Priority
**Location:** `p0-critical/`

**Must complete immediately.** Blockers for other work. Focus all resources here first.
- C# Phase 3 generator completion
- Content pipeline foundation (Reddit scraper)

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
| ✅ Resolved | Complete | 6 tasks | ~30 hours (done) |
| 🔴 P0 Critical | Active | 8 tasks | 20-30 hours |
| 🟡 P1 High | Next | 42 tasks | 120-200 hours |
| 🟢 P2 Medium | Planned | 9 tasks | 60-80 hours |
| **Total** | | **65 tasks** | **200-310 hours** |

> **Note:** The Python-based sequential step issues (step-00 through step-14) have been moved to `obsolete/issues/` as the C# implementation is now the primary codebase.

---

## Directory Structure

```
issues/
├── README.md (this file)
├── INDEX.md (issue index)
├── QUICKSTART.md (getting started guide)
│
├── resolved/ ✅ Completed issues (6 tasks)
│   ├── phase-1-interface/ (Setup complete)
│   └── phase-2-prototype/ (Prototypes complete)
│
├── p0-critical/ 🔴 Critical priority (8 tasks, ~20-30 hours)
│   ├── csharp-phase3-complete-generators/
│   └── content-pipeline/
│
├── p1-high/ 🟡 High priority (42 tasks, ~120-200 hours)
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
├── p2-medium/ 🟢 Medium priority (9 tasks, ~60-80 hours)
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
