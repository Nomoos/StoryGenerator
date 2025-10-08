# Phase-Based Issue Organization - Visual Guide

## Overview

This document provides a visual representation of the reorganized atomic issues structure. All 63 tasks are organized into 3 phases following the principle: **Interface → Prototype → Implementation**.

## 🎯 Three-Phase Model

```
┌─────────────────────────────────────────────────────────────────┐
│                     PHASE 1: INTERFACE                          │
│                    (Define the "what")                          │
│                                                                 │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│  │ Repo         │  │ Config       │  │ C#           │         │
│  │ Structure    │→ │ Files        │→ │ Projects     │         │
│  └──────────────┘  └──────────────┘  └──────────────┘         │
│                                                                 │
│  3 tasks • 1-2 days • 2-3 developers                           │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                    PHASE 2: PROTOTYPE                           │
│                   (Validate the "how")                          │
│                                                                 │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐          │
│  │ Ollama  │  │ Whisper │  │ FFmpeg  │  │ SDXL/   │          │
│  │ Client  │  │ Client  │  │ Client  │  │ LTX     │          │
│  └─────────┘  └─────────┘  └─────────┘  └─────────┘          │
│  Python + C# implementations in parallel                       │
│                                                                 │
│  8 tasks • 2-3 days • 4-8 developers                           │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                 PHASE 3: IMPLEMENTATION                         │
│                  (Build the real thing)                         │
│                                                                 │
│  13 Groups • 52 Tasks • 8-12 days • 10-20 developers           │
│                                                                 │
│  See detailed breakdown below                                  │
└─────────────────────────────────────────────────────────────────┘
```

## 📊 Phase 3: Implementation Groups

### Content Flow Diagram

```
┌──────────────────────────────────────────────────────────────────────────┐
│                        CONTENT PIPELINE (6 tasks)                        │
│  Reddit → Alt Sources → Quality Score → Dedup → Rank → Attribution     │
└──────────────────────────────────────────────────────────────────────────┘
                                    ↓
┌──────────────────────────────────────────────────────────────────────────┐
│                       IDEA GENERATION (7 tasks)                          │
│  Adapt Stories → Generate Ideas → Cluster → Titles →                   │
│  Score Titles → Voice Rec → Select Top 5                               │
└──────────────────────────────────────────────────────────────────────────┘
                                    ↓
┌──────────────────────────────────────────────────────────────────────────┐
│                      SCRIPT DEVELOPMENT (5 tasks)                        │
│  Generate Raw → Score → Iterate → GPT Improve → Title Improve          │
└──────────────────────────────────────────────────────────────────────────┘
                                    ↓
              ┌─────────────────────┴─────────────────────┐
              ↓                                           ↓
┌──────────────────────────────┐          ┌──────────────────────────────┐
│   SCENE PLANNING (3 tasks)   │          │  AUDIO PRODUCTION (2 tasks)  │
│  Beat Sheet → Shot List →    │          │  TTS Gen → Normalization     │
│  Draft Subtitles             │          └──────────────────────────────┘
└──────────────────────────────┘                         ↓
              ↓                                           ↓
┌──────────────────────────────┐          ┌──────────────────────────────┐
│  IMAGE GENERATION (4 tasks)  │          │ SUBTITLE CREATION (2 tasks)  │
│  Prompts → KeyframesA/B →    │          │  Forced Align → Scene Map    │
│  Selection                   │          └──────────────────────────────┘
└──────────────────────────────┘
              ↓
┌──────────────────────────────┐
│  VIDEO PRODUCTION (3 tasks)  │
│  LTX Gen → Interpolation →   │
│  Variant Selection           │
└──────────────────────────────┘
              ↓
┌─────────────────────────────────────────────────┐
│           POST-PRODUCTION (6 tasks)             │
│  Crop → Burn Subs → BGM/SFX → Concat →         │
│  Transitions → Color Grade                      │
└─────────────────────────────────────────────────┘
              ↓
┌──────────────────────────────┐
│   QUALITY CONTROL (3 tasks)  │
│  Device Preview → Sync →     │
│  QC Report                   │
└──────────────────────────────┘
              ↓
┌──────────────────────────────┐
│   EXPORT & DELIVERY (3 tasks)│
│  Final Encode → Thumbnail →  │
│  Metadata                    │
└──────────────────────────────┘
              ↓
┌──────────────────────────────┐
│     DISTRIBUTION (4 tasks)   │
│  YouTube → TikTok →          │
│  Instagram → Facebook        │
└──────────────────────────────┘
              ↓
┌──────────────────────────────┐
│       ANALYTICS (4 tasks)    │
│  Collection → Monetization → │
│  Performance → Optimization  │
└──────────────────────────────┘
```

## 📈 Task Distribution

### By Phase
```
Phase 1: ███ 3 tasks (5%)
Phase 2: ████████ 8 tasks (13%)
Phase 3: ████████████████████████████████████████████████████ 52 tasks (82%)
```

### By Priority
```
P0 (Critical): ███████████████ 15 tasks (23%)
P1 (Core):     ██████████████████████████████████ 35 tasks (55%)
P2 (Enhanced): ██████████████ 14 tasks (22%)
```

### By Phase 3 Groups
```
Content Pipeline:    ██████ 6 tasks
Idea Generation:     ███████ 7 tasks
Script Development:  █████ 5 tasks
Scene Planning:      ███ 3 tasks
Audio Production:    ██ 2 tasks
Subtitle Creation:   ██ 2 tasks
Image Generation:    ████ 4 tasks
Video Production:    ███ 3 tasks
Post-Production:     ██████ 6 tasks
Quality Control:     ███ 3 tasks
Export & Delivery:   ███ 3 tasks
Distribution:        ████ 4 tasks
Analytics:           ████ 4 tasks
```

## 🚀 Execution Timeline (20 Developers)

```
Week 1
├── Days 1-2: Phase 1 + Phase 2 (parallel)
│   ├── Team A (4 devs): Phase 1 Interface
│   └── Team B (8 devs): Phase 2 Prototype (parallel)
│
└── Days 3-7: Phase 3 Wave 1 + 2
    ├── Team A (6 devs): Content Pipeline + Idea Generation
    ├── Team B (6 devs): Script Dev + Scene Planning
    └── Team C (8 devs): Audio + Subtitle + Image Gen

Week 2
├── Days 8-10: Phase 3 Wave 3
│   ├── Team A (8 devs): Video Production + Post-Production
│   └── Team B (6 devs): Quality Control + Export
│
└── Days 11-12: Phase 3 Wave 4
    ├── Team A (8 devs): Distribution
    └── Team B (6 devs): Analytics + Documentation
```

## 🎯 Dependencies Between Phases

```
┌─────────────┐
│  Phase 1    │  ← No dependencies (starting point)
│ Interface   │
└─────────────┘
      │
      └──────────────┐
                     ↓
              ┌─────────────┐
              │  Phase 2    │  ← Requires: Phase 1 complete
              │ Prototype   │     (needs config files, env)
              └─────────────┘
                     │
                     └──────────────┐
                                    ↓
                             ┌─────────────────┐
                             │    Phase 3      │  ← Requires: Phase 1 + 2
                             │ Implementation  │     (needs structure + patterns)
                             └─────────────────┘
```

## 📁 Directory Structure

```
issues/atomic/
│
├── phase-1-interface/                    [3 tasks]
│   ├── README.md                         (Phase guide)
│   ├── 00-setup-01-repo-structure/
│   ├── 00-setup-02-config-files/
│   └── 00-setup-04-csharp-projects/
│
├── phase-2-prototype/                    [8 tasks]
│   ├── README.md                         (Phase guide)
│   ├── 01-research-01-ollama-client/
│   ├── 01-research-02-whisper-client/
│   ├── 01-research-03-ffmpeg-client/
│   ├── 01-research-04-sdxl-client/
│   ├── 01-research-05-ltx-client/
│   ├── 01-research-06-csharp-ollama/
│   ├── 01-research-07-csharp-whisper/
│   └── 01-research-08-csharp-ffmpeg/
│
└── phase-3-implementation/               [52 tasks in 13 groups]
    ├── README.md                         (Phase guide)
    │
    ├── content-pipeline/                 [6 tasks]
    │   ├── README.md
    │   └── 02-content-*/ (6 tasks)
    │
    ├── idea-generation/                  [7 tasks]
    │   ├── README.md
    │   ├── 03-ideas-*/ (4 tasks)
    │   └── 04-scoring-*/ (3 tasks)
    │
    ├── script-development/               [5 tasks]
    │   ├── README.md
    │   └── 05-script-*/ (5 tasks)
    │
    ├── scene-planning/                   [3 tasks]
    │   ├── README.md
    │   └── 06-scenes-*/ (3 tasks)
    │
    ├── audio-production/                 [2 tasks]
    │   ├── README.md
    │   └── 07-audio-*/ (2 tasks)
    │
    ├── subtitle-creation/                [2 tasks]
    │   ├── README.md
    │   └── 08-subtitles-*/ (2 tasks)
    │
    ├── image-generation/                 [4 tasks]
    │   ├── README.md
    │   └── 09-images-*/ (4 tasks)
    │
    ├── video-production/                 [3 tasks]
    │   ├── README.md
    │   └── 10-video-*/ (3 tasks)
    │
    ├── post-production/                  [6 tasks]
    │   ├── README.md
    │   └── 11-post-*/ (6 tasks)
    │
    ├── quality-control/                  [3 tasks]
    │   ├── README.md
    │   └── 12-qc-*/ (3 tasks)
    │
    ├── export-delivery/                  [3 tasks]
    │   ├── README.md
    │   └── 13-export-*/ (3 tasks)
    │
    ├── distribution/                     [4 tasks]
    │   ├── README.md
    │   └── 14-dist-*/ (4 tasks)
    │
    └── analytics/                        [4 tasks]
        ├── README.md
        └── 15-analytics-*/ (4 tasks)
```

## 🎓 Key Benefits

### 1. Clear Progression
- **Interface first**: Define before implementing
- **Prototype second**: Validate before building
- **Implementation last**: Build with confidence

### 2. Reduced Rework
- Catch integration issues early in prototypes
- Fix config problems before implementation
- Validate patterns before scale

### 3. Better Coordination
- Teams work within logical phase boundaries
- Clear handoffs between phases
- Parallel work within each phase

### 4. Incremental Value
- Phase 1: Working dev environment
- Phase 2: Validated integrations
- Phase 3: Production pipeline

## 📚 Documentation Map

```
atomic/
├── README.md                             ← Start here (overview)
│
├── phase-1-interface/
│   └── README.md                         ← Phase 1 guide
│
├── phase-2-prototype/
│   └── README.md                         ← Phase 2 guide
│
├── phase-3-implementation/
│   ├── README.md                         ← Phase 3 overview
│   │
│   ├── content-pipeline/README.md        ← Group guides
│   ├── idea-generation/README.md
│   ├── script-development/README.md
│   ├── ... (10 more group READMEs)
│   │
│   └── {group}/{task}/issue.md          ← Individual task details
```

## 🔄 Migration Notes

### From Old Structure
- Task IDs remain unchanged (e.g., `02-content-01-reddit-scraper`)
- All issue.md files preserved without modification
- Only directory organization changed
- Update references to point to new paths

### Path Changes
```
Old: issues/atomic/02-content-01-reddit-scraper/issue.md
New: issues/atomic/phase-3-implementation/content-pipeline/02-content-01-reddit-scraper/issue.md
```

## 📞 Quick Reference

### Starting a New Project?
1. Read `atomic/README.md` for overview
2. Review `phase-1-interface/README.md` for first steps
3. Assign Phase 1 tasks to team
4. Complete Phase 1 before moving to Phase 2

### Already Started?
1. Map your current work to the new structure
2. Complete current phase before moving forward
3. Update any documentation references
4. Use new paths for future work

### Need Help?
- Each phase has a detailed README.md
- Each group has task-specific guidance
- Individual tasks have acceptance criteria
- All original issue.md files are preserved

---

**Last Updated:** 2025-01-01  
**Structure Version:** 2.0 (Phase-Based)  
**Total Issues:** 63 (3 + 8 + 52)
