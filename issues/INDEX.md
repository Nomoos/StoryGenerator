# Issues Index - StoryGenerator Pipeline

Complete breakdown of the video generation pipeline into manageable, step-by-step issues.

## Overview

This index organizes the entire StoryGenerator pipeline (from ideation to final export) into 14 distinct steps. Each step has its own directory with a detailed issue file.

## 🎯 Quick Navigation

| Step | Name | Status | Priority | Directory |
|------|------|--------|----------|-----------|
| 0 | Research Prototypes | Not Started | High | [step-00-research/](step-00-research/) |
| 1 | Ideas → Topics → Titles | Not Started | High | [step-01-ideas/](step-01-ideas/) |
| 2 | Viral Score (Titles) | Not Started | High | [step-02-viral-score/](step-02-viral-score/) |
| 3 | Raw Script → Iterate | Not Started | High | [step-03-raw-script/](step-03-raw-script/) |
| 4 | Improve Script (GPT/Local) | Not Started | High | [step-04-improve-script/](step-04-improve-script/) |
| 5 | Improve Title (GPT/Local) | Not Started | Medium | [step-05-improve-title/](step-05-improve-title/) |
| 6 | Scene Planning | Not Started | High | [step-06-scene-planning/](step-06-scene-planning/) |
| 7 | Voiceover | Not Started | High | [step-07-voiceover/](step-07-voiceover/) |
| 8 | Subtitle Timing | Not Started | High | [step-08-subtitle-timing/](step-08-subtitle-timing/) |
| 9 | Key Images (SDXL) | Not Started | High | [step-09-key-images/](step-09-key-images/) |
| 10 | Video Generation | Not Started | High | [step-10-video-generation/](step-10-video-generation/) |
| 11 | Post-Production | Not Started | High | [step-11-post-production/](step-11-post-production/) |
| 12 | Quality Checks | Not Started | High | [step-12-quality-checks/](step-12-quality-checks/) |
| 13 | Final Export | Not Started | High | [step-13-final-export/](step-13-final-export/) |
| 14 | Platform Distribution & Analytics | Not Started | Medium | [step-14-distribution-analytics/](step-14-distribution-analytics/) |

## 📊 Pipeline Flow

```
Step 0: Research Prototypes (Setup)
    ↓
Step 1: Ideas → Topics → Titles (Content Generation)
    ↓
Step 2: Viral Score (Title Selection)
    ↓
Step 3: Raw Script → Iterate (Script v0, v1)
    ↓
Step 4: Improve Script (Script v2+)
    ↓
Step 5: Improve Title (Title Variants)
    ↓
Step 6: Scene Planning (Shots + Draft Subtitles)
    ↓
Step 7: Voiceover (Audio Generation + Normalization)
    ↓
Step 8: Subtitle Timing (Forced Alignment)
    ↓
Step 9: Key Images (SDXL Keyframes)
    ↓
Step 10: Video Generation (LTX/Interpolation)
    ↓
Step 11: Post-Production (Assembly + Effects)
    ↓
Step 12: Quality Checks (QC Reports)
    ↓
Step 13: Final Export (Platform-Ready Files)
    ↓
Step 14: Platform Distribution & Analytics (Upload + Performance Tracking)
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
