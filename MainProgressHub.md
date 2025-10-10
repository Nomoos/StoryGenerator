# 📣 Main Progress Hub — Parallel Phases (Roadmap-Synced)

**Purpose**  
This document defines the **single source of truth** structure for StoryGenerator progress across **all phases**. It describes how each working group tracks **unfinished child issues** from their `./.ISSUES` folder, highlights their **current focus** from `.NEXT.MD`, and keeps `docs/roadmaps/HYBRID_ROADMAP.md` in sync.

---

## 🔗 Scope & Directives

- **Roadmap is canonical:** Any change in status **must** be reflected in `docs/roadmaps/HYBRID_ROADMAP.md` in the same update cycle.  
- **Per-group ownership:** Each group controls its own `.NEXT.MD`, `.ISSUES/` (open tasks), and `.DONE/` (completed tasks).  
- **Hub aggregates only:** This hub structure allows listing **current focus**, **unfinished work**, **risks**, and **links**.

---

## 🧩 Working Groups & Folders

Each group directory contains:
- `.NEXT.MD` — the **single, current focus** item (one-pager summary + links).
- `.ISSUES/` — **unfinished** child issues (one markdown file per task).
- `.DONE/` — **completed** child issues (moved here upon completion).

```
issues/
  group_1/
    README.md
    .NEXT.MD
    .ISSUES/
      <child-issue>.md
      <child-issue-2>.md
    .DONE/
      <completed-issue>.md
  group_2/
    README.md
    .NEXT.MD
    .ISSUES/
    .DONE/
  group_3/
    README.md
    .NEXT.MD
    .ISSUES/
    .DONE/
  group_4/
    README.md
    .NEXT.MD
    .ISSUES/
    .DONE/
```

> **Rule of one:** `.NEXT.MD` points to exactly **one** priority item at a time. Everything else stays in `.ISSUES/` until picked up.

---

## 📅 Reporting Cadence

- **When work starts or priorities change:** Update `.NEXT.MD`.  
- **When a task is finished:** Move its file from `.ISSUES/` → `.DONE/` (same filename).  
- **Hub refresh:** Edit the GitHub issue to reflect the new **Next** and **Unfinished** lists, then sync the roadmap.  
- **Commit message convention:**  
  ```bash
  git commit -m "roadmap(sync): group_<N> <status-change>"
  ```

---

## 📋 Child Issue Template

Each child issue in `.ISSUES/` should follow this structure:

```markdown
# [Issue Title]

**Group:** group_<N>  
**Priority:** P0/P1/P2  
**Status:** 🔄 In Progress | 📋 Not Started  
**Estimated Effort:** X hours  

## Description
[Clear description of the task]

## Acceptance Criteria
- [ ] Criterion 1
- [ ] Criterion 2
- [ ] Criterion 3

## Dependencies
- Link to related issues or prerequisite work

## Implementation Notes
[Technical details, approach, or considerations]

## Links
- Related roadmap section: [HYBRID_ROADMAP.md](../docs/roadmaps/HYBRID_ROADMAP.md)
```

---

## 🎯 Working Group Assignments

### Group 1: Foundation & Infrastructure
**Focus Areas:**
- Core pipeline orchestration
- Configuration management
- Error handling and retry logic
- Performance monitoring

### Group 2: Content & Ideas
**Focus Areas:**
- Content collection and sourcing
- Idea generation
- Script development and iteration
- Quality scoring

### Group 3: Media Production
**Focus Areas:**
- Audio production (TTS, normalization)
- Image generation (SDXL keyframes)
- Video synthesis (LTX-Video)
- Scene planning

### Group 4: Post-Production & Distribution
**Focus Areas:**
- Subtitle creation and timing
- Post-production effects
- Quality control
- Export and delivery
- Platform distribution

---

## 🔄 Workflow

### 1. Starting New Work
1. Create child issue file in `.ISSUES/` following the template
2. Update `.NEXT.MD` if this becomes the current priority
3. Link to relevant roadmap section

### 2. Tracking Progress
1. Update child issue file with progress notes
2. Keep `.NEXT.MD` in sync with current focus
3. Update `HYBRID_ROADMAP.md` if status changes

### 3. Completing Work
1. Mark all acceptance criteria as complete
2. Move file from `.ISSUES/` → `.DONE/`
3. Update `.NEXT.MD` to next priority
4. Update `HYBRID_ROADMAP.md` with completion status
5. Commit with proper message format

---

## 📊 Status Aggregation

The Main Progress Hub GitHub issue should aggregate:

### Current Focus (from each .NEXT.MD)
- **Group 1:** [Current focus item]
- **Group 2:** [Current focus item]
- **Group 3:** [Current focus item]
- **Group 4:** [Current focus item]

### Unfinished Work (from each .ISSUES/)
Count of open issues per group

### Risks & Blockers
Any issues blocking progress

### Quick Links
- [Hybrid Roadmap](docs/roadmaps/HYBRID_ROADMAP.md)
- [Issues Index](issues/INDEX.md)
- [Phase Organization](issues/atomic/PHASE_ORGANIZATION.md)

---

## 🛠️ Maintenance

- **Daily:** Update `.NEXT.MD` as priorities shift
- **Weekly:** Review `.ISSUES/` counts and redistribute if needed
- **On Completion:** Move completed issues to `.DONE/` immediately
- **On Status Change:** Update both group files and `HYBRID_ROADMAP.md` together

---

## 📚 Related Documents

- [HYBRID_ROADMAP.md](docs/roadmaps/HYBRID_ROADMAP.md) - Single source of truth for project status
- [Issues README](issues/README.md) - Overall issues organization
- [INDEX.md](issues/INDEX.md) - Issue index and step details
- [PHASE_ORGANIZATION.md](issues/atomic/PHASE_ORGANIZATION.md) - Phase-based organization guide
