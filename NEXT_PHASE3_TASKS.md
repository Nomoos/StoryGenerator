# Next Tasks to Implement from Phase 3

**Status as of:** 2025-01-11 - Post-Cleanup  
**Last Completed:** Groups 1, 2, 4, 6, 7, 8 (partial), 9 + Phase 4 (moved to resolved)  
**Next Priority:** Group 3 (Script Development) - Lowest incomplete group

---

## ✅ Completed Phase 3 Groups (Moved to Resolved)

All completed groups have been moved to `/issues/resolved/phase-3-implementation/` to maintain focus on active work.

### Group 1: Content Pipeline (6 tasks) - P0/P1 ✅
**Location:** `/issues/resolved/p0-content-pipeline/`

Source and process raw content for video ideas.
- Reddit scraper, alternative sources, quality scoring
- Deduplication, ranking, attribution

### Group 2: Idea Generation (7 tasks) - P1 ✅
**Location:** `/issues/resolved/phase-3-implementation/group-2-idea-generation/`

Transform content into video titles and concepts.
- Reddit adaptation, LLM generation, clustering
- Title generation, scoring, voice recommendation, top selection

### Group 4: Scene Planning (3 tasks) - P1 ✅
**Location:** `/issues/resolved/phase-3-implementation/group-4-scene-planning/`

Break scripts into scenes and shots.
- Beat sheet creation, shot lists
- Draft subtitle generation

### Group 6: Subtitle Creation (2 tasks) - P1 ✅
**Location:** `/issues/resolved/phase-3-implementation/group-6-subtitle-creation/`

Create precisely timed subtitles.
- Forced alignment, scene mapping

### Group 7: Image Generation (4 tasks) - P1/P2 ✅
**Location:** `/issues/resolved/phase-3-implementation/group-7-image-generation/`

Generate keyframe images for videos.
- Prompt building, keyframe generation (batch A & B)
- Image selection

### Group 8: Video Production (2 of 3 tasks) - P1/P2 ⚠️
**Location:** `/issues/resolved/phase-3-implementation/group-8-video-production/`

Generate video clips (partial completion).
- ✅ LTX generation, interpolation
- ❌ Variant selection (remains in p1-high)

### Group 9: Post-Production (6 tasks) - P1/P2 ✅
**Location:** `/issues/resolved/phase-3-implementation/group-9-post-production/`

Assemble and enhance final videos.
- Crop/resize, subtitle burning, BGM/SFX
- Concatenation, transitions, color grading

### Phase 4: Pipeline Orchestration (1 task) - P1 ✅
**Location:** `/issues/resolved/phase-4-pipeline-orchestration/`

Complete end-to-end pipeline orchestrator.
- Full pipeline orchestration with state management

**Total Completed:** 30+ tasks from 7 groups (plus Phase 4)

---

## 🎯 RECOMMENDED: Next Groups to Implement (In Priority Order)

### Priority 1: Script Development (Group 3) - NEXT RECOMMENDED ⭐

**Why This is Critical:**
- ✅ Content pipeline is ready (Group 1)
- ✅ Ideas are being generated (Group 2)
- ❌ **BLOCKING:** Scripts are needed for scene planning
- 🔥 **This is the LOWEST numbered incomplete group**
- 🎯 **Blocks entire downstream pipeline**

**Tasks (5):**
1. **05-script-01-raw-generation** (P1) - Generate initial video script
   - Use selected ideas from Group 2
   - Apply storytelling structure
   - Create engaging narrative flow
   - Output: `Generator/scripts/raw/{title_id}.json`

2. **05-script-02-script-scorer** (P1) - Score script quality
   - Evaluate engagement, clarity, pacing
   - Check for storytelling elements
   - Assess target demographic fit
   - Output: Quality scores and metrics

3. **05-script-03-iteration** (P1) - Iteratively improve scripts
   - Multiple refinement passes
   - Address low-scoring areas
   - Optimize for target audience
   - Output: Improved script versions

4. **05-script-04-gpt-improvement** (P1) - GPT-based enhancement
   - Use GPT-4 for creative improvement
   - Enhance engagement and flow
   - Polish dialogue and narration
   - Output: Enhanced script

5. **05-script-05-title-improvement** (P1) - Optimize video title
   - Refine title based on final script
   - Ensure clickability and SEO
   - A/B test variations
   - Output: Final optimized title

**Estimated Effort:** 15-20 hours (3 developers, 2 days)  
**Blocking:** All downstream groups (scenes, audio, video, etc.)  
**Priority Level:** P1 (CRITICAL)

**Location:** `/issues/p1-high/script-development/`

### Priority 2: Audio Production (Group 5) - SECOND PRIORITY

**Why This is Next:**
- ✅ Scripts will be ready (from Group 3)
- ✅ Scene timing is established (from Group 4)
- 🔥 Audio is needed for forced subtitle alignment
- 🔥 Audio duration is required for accurate video timing
- 🎯 **Blocks multiple downstream tasks**

**Tasks (2):**
1. **07-audio-01-tts-generation** (P1) - Generate voiceover using TTS
   - ElevenLabs or OpenAI TTS
   - Select appropriate voice for demographics
   - Generate audio files from scripts
   - Output: `Generator/audio/tts/{gender}/{age}/{title_id}.mp3`

2. **07-audio-02-normalization** (P1) - Normalize audio to -14 LUFS
   - Use pyloudnorm for LUFS normalization
   - YouTube/TikTok standard: -14 LUFS
   - Output: `Generator/audio/normalized/{gender}/{age}/{title_id}.mp3`

**Estimated Effort:** 3-5 hours  
**Dependencies:** Scripts (Group 3) ✅  
**Blocks:** 
- Subtitle Creation (Group 6) - needs audio for forced alignment
- Video Production (Group 8) - needs audio duration for timing
- Post-Production (Group 9) - needs audio for final mix

**Implementation Path:**
```
issues/p1-high/audio-production/
├── 07-audio-01-tts-generation/
└── 07-audio-02-normalization/
```

**Estimated Effort:** 8-10 hours (2 developers, 1 day)  
**Priority Level:** P1 (HIGH)

**Location:** `/issues/p1-high/audio-production/`

### Priority 3: Video Variant Selection (Group 8 remainder)

**Why This is Remaining:**
- ✅ LTX generation and interpolation are complete (moved to resolved)
- ❌ Variant selection quality assessment NOT YET IMPLEMENTED
- 🎯 Would improve video quality but not blocking

**Tasks (1):**
1. **10-video-03-variant-selection** (P2) - Select best video variant
   - Quality metrics for video assessment
   - Motion smoothness and temporal consistency
   - Artifact detection
   - Output: Selected video variant manifest

**Estimated Effort:** 4-5 hours (1 developer, 0.5 day)  
**Priority Level:** P2 (MEDIUM)

**Location:** `/issues/p1-high/video-production/10-video-03-variant-selection/`

### Priority 4: Quality Control (Group 10)

**Tasks (3):**
1. **12-qc-01-device-preview** - Generate preview for different devices
2. **12-qc-02-sync-check** - Verify audio/video sync
3. **12-qc-03-quality-report** - Generate quality metrics report

**Estimated Effort:** 8-10 hours (2 developers, 1 day)  
**Priority Level:** P1 (HIGH)

**Location:** `/issues/p1-high/quality-control/`

### Priority 5: Export & Delivery (Group 11)

**Tasks (3):**
1. **13-export-01-final-encode** - Final video encoding for distribution
2. **13-export-02-thumbnail** - Generate video thumbnail
3. **13-export-03-metadata** - Create metadata files

**Estimated Effort:** 6-8 hours (2 developers, 1 day)  
**Priority Level:** P1 (HIGH)

**Location:** `/issues/p1-high/export-delivery/`

---

## 📊 Implementation Strategy

### Updated Execution Plan

**Wave 1: Script Development (Now - Next 2 days)**
```
Developer Team (3 devs):
├── 05-script-01-raw-generation
├── 05-script-02-script-scorer
├── 05-script-03-iteration
├── 05-script-04-gpt-improvement
└── 05-script-05-title-improvement
```

**Wave 2: Audio Production (After Wave 1 - Next 1 day)**
```
Developer Team (2 devs):
├── 07-audio-01-tts-generation
└── 07-audio-02-normalization
```

**Wave 3: Quality & Export (After Wave 2 - Next 2 days)**
```
Developer Team A (2 devs):
├── 12-qc-01-device-preview
├── 12-qc-02-sync-check
└── 12-qc-03-quality-report

Developer Team B (2 devs):
├── 13-export-01-final-encode
├── 13-export-02-thumbnail
└── 13-export-03-metadata
```

**Optional: Video Variant Selection (Parallel to Wave 3)**
```
Developer (1 dev):
└── 10-video-03-variant-selection
```

---

## 🚀 Immediate Next Action

**START HERE: Script Development (Group 3) - LOWEST INCOMPLETE GROUP**

### Step 1: Review Script Development Issues
```bash
cd /home/runner/work/StoryGenerator/StoryGenerator
cd issues/p1-high/script-development
ls -la
cat 05-script-01-raw-generation/issue.md
cat 05-script-02-script-scorer/issue.md
cat 05-script-03-iteration/issue.md
cat 05-script-04-gpt-improvement/issue.md
cat 05-script-05-title-improvement/issue.md
```

### Step 2: Implement Script Generation
- Choose LLM provider (GPT-4 recommended)
- Implement Python module: `core/script_generation.py`
- Add storytelling structure and templates
- Create tests: `tests/test_script_generation.py`
- Update issue template with implementation details

### Step 3: Implement Script Scoring
- Build quality evaluation metrics
- Implement scoring algorithms
- Add demographic fitting assessment
- Document scoring criteria

### Step 4: Integration
- Test end-to-end: Ideas → Script Generation → Script Scoring
- Verify scripts work with scene planning (Group 4)
- Update pipeline documentation

---

## 📈 Progress Tracking

**Phase 3 Completion Status:**

```
Total Groups: 13
Completed: 7 (54% - Groups 1, 2, 4, 6, 7, 9 + partial 8)
Remaining: 6 (46% - Groups 3, 5, 8 partial, 10, 11, 12)

Total Tasks: 52
Completed: 30 (58%)
Remaining: 22 (42%)

Next Milestone: 65% completion (34 tasks)
Requires: Script Development (5) + Audio Production (2) + remaining tasks
```

**Estimated Timeline:**
- ✅ Week 1-2 Complete: Groups 1, 2, 4, 6, 7, 9 (30 tasks) + Phase 4
- 🎯 Week 3 Target: Group 3 Script Dev (5 tasks) → 35 tasks (67%)
- 🎯 Week 4 Target: Group 5 Audio + Group 8 video + QC (6 tasks) → 41 tasks (79%)
- 🎯 Week 5 Target: Groups 10-11 Export (6 tasks) → 47 tasks (90%)
- 🎯 Week 6 Target: Final polish and distribution → 52 tasks (100%) ✅

---

## 🎯 Success Metrics

After completing Script Development (Group 3), you will have:

✅ End-to-end content-to-script pipeline:
```
Reddit Content → Ideas → Scripts (COMPLETE) → Scenes → Ready for Audio
```

✅ Key outputs ready:
- Generated scripts ready for scene planning
- Script quality scores and iterations
- Optimized titles and narratives
- Complete foundation for audio/video generation

✅ Unblocking multiple downstream tasks:
- Subtitle forced alignment can proceed
- Video production can use accurate timing
- Post-production can mix final audio

---

## 📚 Resources

**Documentation:**
- `docs/PIPELINE_OUTPUT_FILES.md` - Expected output formats
- `docs/PIPELINE_CHECKLIST.md` - Pipeline operation checklist
- `issues/atomic/README.md` - Phase 3 overview

**Examples:**
- `src/CSharp/Examples/VoiceoverGenerationExample.cs` - C# TTS example
- ElevenLabs Python SDK: https://github.com/elevenlabs/elevenlabs-python
- pyloudnorm: https://github.com/csteinmetz1/pyloudnorm

**Current Working Group:**
- `issues/p1-high/audio-production/` - Audio production tasks
- `issues/p1-high/image-generation/` - Image generation tasks (parallel)

---

## ✨ Summary

**What to do next:**
1. ✅ Group 4 (Scene Planning) is complete
2. 🎯 **Implement Group 5 (Audio Production) next** - HIGHEST PRIORITY
3. 🔄 Optionally work on Group 7 (Image Generation) in parallel
4. 📊 Groups 6, 8, 9 wait for audio/images
5. 🎬 Groups 10-13 are final assembly and delivery

**Command to start:**
```bash
cd issues/p1-high/audio-production
# Review and implement tasks in this order:
# 1. 07-audio-01-tts-generation
# 2. 07-audio-02-normalization
```
