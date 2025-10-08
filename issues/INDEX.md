# Issues Index - StoryGenerator Pipeline

Complete breakdown of the C# video generation pipeline into manageable, atomic tasks.

## 🎯 Approach

### **Atomic Tasks - Phase-Based (64 Tasks) ⭐ RECOMMENDED**
Parallelizable 1-8 hour tasks organized into 3 phases:

- **Phase 1: Interface** (4 tasks) - Define configs, schemas, and structure
- **Phase 2: Prototype** (3 tasks) - Research and validate C# integrations
- **Phase 3: Implementation** (52 tasks in 13 groups) - Build production pipeline

👉 **[View Atomic Tasks Directory](atomic/README.md)** - Start here for team collaboration

Each phase builds on the previous, ensuring clear dependencies and reduced rework.

> **Note:** The Python-based sequential step issues (step-00 through step-14) have been archived to `obsolete/issues/` as they represent the obsolete Python implementation plan.

## 🎯 C# Implementation Issues

| Type | Name | Status | Priority | Directory |
|------|------|--------|----------|-----------|
| Roadmap | C# Master Roadmap | Active | High | [csharp-master-roadmap/](csharp-master-roadmap/) |
| Phase 3 | Complete Generators | Not Started | P0 | [csharp-phase3-complete-generators/](csharp-phase3-complete-generators/) |
| Phase 4 | Pipeline Orchestration | Planned | P1 | [csharp-phase4-pipeline-orchestration/](csharp-phase4-pipeline-orchestration/) |
| Phase 5 | Video Generators | Planned | P1 | [csharp-video-generators/](csharp-video-generators/) |

For detailed atomic task breakdown, see [atomic/README.md](atomic/README.md).

## 📜 Obsolete Python Issues (Archived)

The Python-based sequential step issues (step-00 through step-14) have been moved to `obsolete/issues/` for historical reference. They represented the original Python implementation plan which is no longer maintained.

To view the archived Python issues:
```bash
cd obsolete/issues/
ls step-*
```

## 🎬 Target Audience Segments

Each step applies to all combinations of:
- **Genders:** women, men
- **Age Buckets:** 10-13, 14-17, 18-23
- **Total Combinations:** 6 (2 × 3)

### Content Scale
- **Titles per segment:** 5 (top-scoring)
- **Total videos:** 30 (5 titles × 6 segments)
- **Shots per video:** 6-10 average
- **Total shots:** ~180-300 across all videos

## 📝 Step Details

### Step 0: Research Prototypes
**Duration:** 1-2 days  
**Deliverables:** Python & C# research stubs  
**Dependencies:** None  

Create proof-of-concept implementations for:
- LLM integration (Ollama, Qwen2.5, Llama3.1)
- ASR (faster-whisper)
- Image generation (SDXL)
- Video generation (LTX-Video)
- Audio normalization (FFmpeg)

[View Issue →](step-00-research/issue.md)

---

### Step 1: Ideas → Topics → Titles
**Duration:** 2-3 days  
**Deliverables:** Ideas, topics, titles per segment  
**Dependencies:** Step 0  

Generate 20+ ideas per segment, cluster into 8+ topics, create 10+ clickable titles.

[View Issue →](step-01-ideas/issue.md)

---

### Step 2: Viral Score (Titles)
**Duration:** 1-2 days  
**Deliverables:** Title scores, voice recommendations, top 5 selections  
**Dependencies:** Step 1  

Score all titles 0-100 using rubric, recommend voices, select top 5 per segment.

[View Issue →](step-02-viral-score/issue.md)

---

### Step 3: Raw Script → Iterate
**Duration:** 3-4 days  
**Deliverables:** Raw scripts (v0), iterated scripts (v1+), scores  
**Dependencies:** Step 2  

Generate scripts from selected titles, score them, iterate until improvement plateaus.

[View Issue →](step-03-raw-script/issue.md)

---

### Step 4: Improve Script (GPT/Local)
**Duration:** 2-3 days  
**Deliverables:** GPT-improved scripts (v2+), final scores  
**Dependencies:** Step 3  

Further improve scripts with focus on clarity, pacing, and hooks.

[View Issue →](step-04-improve-script/issue.md)

---

### Step 5: Improve Title (GPT/Local)
**Duration:** 1-2 days  
**Deliverables:** Title variants, scores, final selections  
**Dependencies:** Step 4  

Generate 5 variants per title, score them, select best performing.

[View Issue →](step-05-improve-title/issue.md)

---

### Step 6: Scene Planning
**Duration:** 2-3 days  
**Deliverables:** Shot definitions, beat-sheets, draft subtitles  
**Dependencies:** Steps 4, 5  

Create detailed scene breakdowns with shots, prompts, and subtitle drafts.

[View Issue →](step-06-scene-planning/issue.md)

---

### Step 7: Voiceover
**Duration:** 2-3 days  
**Deliverables:** TTS audio, normalized audio, metadata  
**Dependencies:** Steps 2, 4  

Generate voiceovers using local TTS, normalize to -14 LUFS.

[View Issue →](step-07-voiceover/issue.md)

---

### Step 8: Subtitle Timing
**Duration:** 1-2 days  
**Deliverables:** Timed SRT files, subtitle-to-shot mappings  
**Dependencies:** Steps 6, 7  

Use faster-whisper for forced alignment, create precise subtitle timing.

[View Issue →](step-08-subtitle-timing/issue.md)

---

### Step 9: Key Images (SDXL)
**Duration:** 3-5 days  
**Deliverables:** Keyframe images (v1, v2), prompts, selections  
**Dependencies:** Step 6  

Generate keyframes using SDXL for each shot, with optional refinement passes.

[View Issue →](step-09-key-images/issue.md)

---

### Step 10: Video Generation
**Duration:** 4-6 days  
**Deliverables:** Video clips (LTX or interpolation), metadata  
**Dependencies:** Steps 6, 9  

Generate video clips using LTX-Video or interpolation, compare methods.

[View Issue →](step-10-video-generation/issue.md)

---

### Step 11: Post-Production
**Duration:** 2-4 days  
**Deliverables:** Draft videos with audio, subtitles, effects  
**Dependencies:** Steps 7, 8, 10  

Assemble all elements: video clips, audio, subtitles, transitions.

[View Issue →](step-11-post-production/issue.md)

---

### Step 12: Quality Checks
**Duration:** 2-3 days  
**Deliverables:** QC reports, issue lists, approval status  
**Dependencies:** Step 11  

Test on devices, verify specs, check quality, generate QC reports.

[View Issue →](step-12-quality-checks/issue.md)

---

### Step 13: Final Export
**Duration:** 1-2 days  
**Deliverables:** Final videos, thumbnails, metadata, platform prep  
**Dependencies:** Step 12  

Export production-ready files with metadata and platform-specific optimization.

[View Issue →](step-13-final-export/issue.md)

---

## 🔧 Configuration Files

All steps reference these configuration files:
- `/config/pipeline.yaml` - Model and pipeline settings
- `/config/scoring.yaml` - Viral scoring rubric
- `/config/schemas/` - JSON schemas for data formats

## 📁 Output Directories

Organized under `/src/Generator/`:
```
Generator/
├── ideas/{gender}/{age}/
├── topics/{gender}/{age}/
├── titles/{gender}/{age}/
├── scores/{gender}/{age}/
├── scripts/raw_local/{gender}/{age}/
├── scripts/iter_local/{gender}/{age}/
├── scripts/gpt_improved/{gender}/{age}/
├── voices/choice/{gender}/{age}/
├── audio/tts/{gender}/{age}/
├── audio/normalized/{gender}/{age}/
├── subtitles/srt/{gender}/{age}/
├── subtitles/timed/{gender}/{age}/
├── scenes/json/{gender}/{age}/
├── images/keyframes_v1/{gender}/{age}/
├── images/keyframes_v2/{gender}/{age}/
├── videos/ltx/{gender}/{age}/
├── videos/interp/{gender}/{age}/
└── final/{gender}/{age}/
```

## ⚡ Quick Start

1. **Start with Step 0:** Set up research prototypes
2. **Follow sequence:** Each step builds on previous steps
3. **Use validation:** Run `@copilot check` after completing each step
4. **Track progress:** Use MicrostepValidator for progress tracking

## 📊 Progress Tracking

Use the MicrostepValidator system:
```python
from Tools.MicrostepValidator import MicrostepValidator

validator = MicrostepValidator()
validator.list_microsteps()

# After completing work
validator.validate_step(step_number, gender, age)
```

## 🎯 Total Timeline

**Estimated Duration:** 30-45 days for complete pipeline (all 30 videos)

**Breakdown:**
- Setup & Research: 1-2 days
- Content Generation (Steps 1-5): 10-14 days
- Production (Steps 6-11): 16-23 days
- QC & Export (Steps 12-13): 3-5 days

## 📚 Documentation

- `/docs/MICROSTEP_VALIDATION.md` - Validation system guide
- `/docs/GENERATOR_STRUCTURE.md` - Folder structure details
- `/docs/PIPELINE.md` - Complete pipeline documentation

## 🤝 Contributing

When working on an issue:
1. Read the issue file thoroughly
2. Follow the checklist
3. Create required artifacts
4. Use MicrostepValidator for tracking
5. Comment `@copilot check` when complete

---

**Last Updated:** 2024-01-01  
**Version:** 1.0  
**Total Issues:** 14
