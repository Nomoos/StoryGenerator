# Group 3 — Progress & Coordination Hub

This document tracks all unfinished tasks, current priorities, and blockers for **Group 3** (Audio/Visual) development in StoryGenerator.

**Last Updated:** 2025-10-10

---

## 📅 Update Checklist

- [x] `.NEXT.MD` is up to date
- [x] Unfinished tasks listed below
- [x] Blockers/risks noted
- [x] Roadmap synced

---

## Current Focus (`.NEXT.MD`)

**Task:** Audio Production: Voice Cloning System  
**Priority:** P1 (High)  
**Estimated Effort:** 8-10 hours  
**Status:** 📋 Not Started

### Description

Implement voice cloning system to create custom voices for different audience segments using Coqui TTS. This enables creation of multiple voice profiles per age/gender segment with quality validation and A/B testing framework.

### Key Features
- Voice cloning from reference samples (5-10 minutes of audio)
- Multiple voice profiles per age/gender segment
- Voice quality validation
- Voice embedding storage and reuse
- TTS generation with cloned voices
- A/B testing framework for voice variants

**Full Details:** [.ISSUES/audio-voice-cloning.md](.ISSUES/audio-voice-cloning.md)

---

## Unfinished Tasks

### 1. Audio Production: Voice Cloning System
- **Priority:** P1 (High)
- **Effort:** 8-10 hours
- **Status:** 📋 Not Started
- **Dependencies:** 
  - Coqui TTS (TTS>=0.20.0)
  - Audio production infrastructure from Group 3
  - CUDA/GPU for training (recommended)
- **File:** [.ISSUES/audio-voice-cloning.md](.ISSUES/audio-voice-cloning.md)

**Acceptance Criteria:**
- [ ] Voice cloning from reference samples (5-10 minutes of audio)
- [ ] Multiple voice profiles per age/gender segment
- [ ] Voice quality validation
- [ ] Voice embedding storage and reuse
- [ ] TTS generation with cloned voices
- [ ] A/B testing framework for voice variants
- [ ] Unit tests with sample voices

### 2. Image Generation: Style Consistency System
- **Priority:** P1 (High)
- **Effort:** 6-8 hours
- **Status:** 📋 Not Started
- **Dependencies:**
  - diffusers>=0.25.0, ip-adapter>=1.0.0
  - SDXL infrastructure from Group 3
  - GPU with 12GB+ VRAM
- **File:** [.ISSUES/image-style-consistency.md](.ISSUES/image-style-consistency.md)

**Acceptance Criteria:**
- [ ] Style reference image selection/creation
- [ ] Style transfer to all keyframes
- [ ] Visual coherence scoring across frames
- [ ] Color palette consistency
- [ ] Character/object consistency across frames
- [ ] Style library for different video types
- [ ] Unit tests for style consistency

---

## Blockers/Risks

### Current Blockers
- **None** - Both tasks are ready to start

### Potential Risks
1. **GPU Requirements:**
   - Voice cloning: CUDA/GPU recommended for optimal training
   - Style consistency: Requires GPU with 12GB+ VRAM
   - **Mitigation:** Both can work with CPU but performance will be slower

2. **Dependencies:**
   - Voice cloning requires audio production infrastructure
   - Style consistency requires SDXL infrastructure
   - **Mitigation:** Core infrastructure appears to be in place from resolved tasks

3. **Integration Complexity:**
   - Both features need to integrate with existing pipeline
   - Voice profiles and style libraries need management system
   - **Mitigation:** Follow established patterns from resolved groups

### Technical Dependencies
- ✅ Scripts from Group 2 (completed)
- ✅ Foundation infrastructure from Group 1
- ⚠️ Audio production infrastructure (partial - basic TTS exists, cloning is enhancement)
- ⚠️ Image generation infrastructure (partial - basic SDXL exists, style consistency is enhancement)

---

## Links

### Internal References
- **Hub:** [MainProgressHub.md](../../MainProgressHub.md)
- **Group README:** [README.md](./README.md)
- **Current Focus:** [.NEXT.MD](./.NEXT.MD)
- **Roadmap:** [docs/roadmaps/HYBRID_ROADMAP.md](../../docs/roadmaps/HYBRID_ROADMAP.md)

### Related Work
- **Audio Production (Resolved):** [group-5-audio-production](../resolved/phase-3-implementation/group-5-audio-production/)
- **Image Generation (Resolved):** [group-7-image-generation](../resolved/phase-3-implementation/group-7-image-generation/)
- **Scene Planning (Resolved):** [group-4-scene-planning](../resolved/phase-3-implementation/group-4-scene-planning/)
- **C# Voice Implementation:** [src/CSharp/VOICEOVER_README.md](../../src/CSharp/VOICEOVER_README.md)

### Documentation
- **Pipeline Overview:** [docs/PIPELINE.md](../../docs/PIPELINE.md)
- **Generator Structure:** [docs/GENERATOR_STRUCTURE.md](../../docs/GENERATOR_STRUCTURE.md)
- **Microstep Validation:** [docs/MICROSTEP_VALIDATION.md](../../docs/MICROSTEP_VALIDATION.md)

---

## Timeline & Effort

**Total Effort:** 14-18 hours  
**Tasks:** 2  
**Priority:** P1 (High)

**Suggested Sequence:**
1. Voice Cloning (8-10h) - Audio enhancement
2. Style Consistency (6-8h) - Visual enhancement

**Parallelization:** These tasks can be worked on independently by different developers if team capacity allows.

---

## Group 3 Responsibilities

Group 3 focuses on **Audio & Visual Assets** production:

### Audio Production
- ✅ Text-to-speech generation (basic - completed)
- ⏳ Voice cloning and custom voices (enhancement - current)
- ✅ Audio normalization and enhancement (completed)
- ✅ Voice selection and recommendation (completed)

### Image Generation
- ✅ SDXL keyframe generation (basic - completed)
- ⏳ Style consistency validation (enhancement - current)
- ✅ Visual prompt optimization (completed)
- ✅ Image quality assessment (completed)

### Scene Planning
- ✅ Beat sheet creation from scripts (completed)
- ✅ Shot list generation (completed)
- ✅ Scene-to-shot breakdown (completed)

### Subtitle Generation
- ✅ Forced alignment with audio (completed)
- ✅ Word-level timing (completed)
- ✅ Subtitle formatting (SRT) (completed)

**Current Status:** Core functionality complete, working on enhancement features (voice cloning and style consistency).

---

## Next Steps

1. **Voice Cloning (Current Priority)**
   - Set up Coqui TTS development environment
   - Implement `VoiceCloner` class
   - Create voice profile management system
   - Develop quality validation framework
   - Build A/B testing infrastructure
   - Write comprehensive tests
   - Document API and usage

2. **Style Consistency (Next)**
   - Set up IP-Adapter and diffusers
   - Implement `StyleConsistencyManager` class
   - Create style reference generation system
   - Develop coherence scoring metrics
   - Build style library management
   - Write comprehensive tests
   - Document API and usage

3. **Post-Completion**
   - Update roadmap with completion status
   - Move completed tasks to `.DONE/`
   - Update `.NEXT.MD` for next priorities
   - Integrate with main pipeline
   - Update documentation

---

## Contributing

When working on Group 3 tasks:

1. **Pick a task** from `.ISSUES/`
2. **Update `.NEXT.MD`** to reflect your focus
3. **Follow TDD principles** - tests first
4. **Update progress** in the task file regularly
5. **Move to `.DONE/`** when complete
6. **Sync roadmap** - Update HYBRID_ROADMAP.md

Use feature branches: `feature/group3-{task-name}`

---

**For questions or blockers:** Create an issue or contact the maintainer.
