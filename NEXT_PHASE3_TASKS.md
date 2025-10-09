# Next Tasks to Implement from Phase 3

**Status as of:** Scene Planning Group Completion  
**Last Completed:** Group 4 - Scene Planning (3 tasks)

---

## ✅ Completed Phase 3 Groups

### Group 1: Content Pipeline (6 tasks) - P0/P1 ✅
Source and process raw content for video ideas.
- Reddit scraper, alternative sources, quality scoring
- Deduplication, ranking, attribution

### Group 2: Idea Generation (7 tasks) - P1 ✅
Transform content into video titles and concepts.
- Reddit adaptation, LLM generation, clustering
- Title generation, scoring, voice recommendation, top selection

### Group 3: Script Development (5 tasks) - P1 ✅
Generate and refine video scripts.
- Raw generation, scoring, iteration
- GPT improvement, title improvement

### Group 4: Scene Planning (3 tasks) - P1 ✅ ← JUST COMPLETED
Break scripts into scenes and shots.
- Beat sheet creation, shot lists
- Draft subtitle generation

**Total Completed:** 21 tasks from 4 groups

---

## 🎯 RECOMMENDED: Next Groups to Implement (In Priority Order)

### Priority 1: Audio Production (Group 5) - NEXT RECOMMENDED

**Why This is Critical:**
- ✅ Scripts are ready (from Group 3)
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

---

### Priority 2: Image Generation (Group 7) - Can Run in Parallel

**Why This is Important:**
- ✅ Scene visual prompts ready (from Group 4)
- ✅ Can run independently while audio is generated
- 🎯 Images needed for video synthesis

**Tasks (4):**
1. **08-images-01-prompt-building** (P1) - Build SDXL prompts from visual descriptions
2. **08-images-02-keyframe-batch-a** (P1) - Generate first batch of keyframes
3. **08-images-03-keyframe-batch-b** (P2) - Generate second batch (variants)
4. **08-images-04-selection** (P2) - Select best images for each scene

**Estimated Effort:** 8-12 hours  
**Dependencies:** Scene Planning (Group 4) ✅  
**Blocks:** Video Production (Group 8)

**Note:** Groups 5 and 7 can be worked on in parallel by different developers.

---

### Priority 3: Video Production (Group 8) - After Audio + Images

**Why Wait:**
- ❌ Requires audio files for timing (from Group 5)
- ❌ Requires keyframe images (from Group 7)
- Must have both before video synthesis

**Tasks (3):**
1. **10-video-01-ltx-generation** (P1) - Generate video clips using LTX
2. **10-video-02-interpolation** (P1) - Interpolate frames for smoothness
3. **10-video-03-variant-selection** (P2) - Select best video variants

**Estimated Effort:** 8-12 hours  
**Dependencies:** Audio (Group 5), Images (Group 7)

---

### Priority 4: Subtitle Creation (Group 6) - After Audio

**Why Wait:**
- ❌ Requires audio files for forced alignment (from Group 5)
- Draft subtitles exist but need precise timing

**Tasks (2):**
1. **11-subtitles-01-forced-alignment** (P1) - Align subtitles with audio using Whisper
2. **11-subtitles-02-scene-mapping** (P1) - Map aligned subtitles to video scenes

**Estimated Effort:** 4-6 hours  
**Dependencies:** Audio (Group 5)

---

### Priority 5: Post-Production (Group 9) - After Video

**Why Wait:**
- ❌ Requires video clips (from Group 8)
- ❌ Requires aligned subtitles (from Group 6)
- Final assembly stage

**Tasks (6):**
1. **09-post-01-crop-resize** (P1) - Crop to 9:16 aspect ratio
2. **09-post-02-subtitle-burn** (P1) - Burn subtitles into video
3. **09-post-03-bgm-sfx** (P1) - Add background music and sound effects
4. **09-post-04-concatenation** (P1) - Concatenate clips into single video
5. **09-post-05-transitions** (P2) - Add transitions between scenes
6. **09-post-06-color-grading** (P2) - Apply color grading

**Estimated Effort:** 10-14 hours  
**Dependencies:** Video (Group 8), Subtitles (Group 6)

---

## 📊 Implementation Strategy

### Parallel Execution Recommended

**Wave 1: Foundation (Now - Next 1-2 days)**
```
Developer Team A (2 devs):
├── 07-audio-01-tts-generation
└── 07-audio-02-normalization

Developer Team B (3 devs):
├── 08-images-01-prompt-building
├── 08-images-02-keyframe-batch-a
├── 08-images-03-keyframe-batch-b
└── 08-images-04-selection
```

**Wave 2: Synthesis (After Wave 1 - Next 2-3 days)**
```
Developer Team A (2 devs):
├── 11-subtitles-01-forced-alignment
└── 11-subtitles-02-scene-mapping

Developer Team B (3 devs):
├── 10-video-01-ltx-generation
├── 10-video-02-interpolation
└── 10-video-03-variant-selection
```

**Wave 3: Assembly (After Wave 2 - Next 2-3 days)**
```
Developer Team (4 devs):
├── 09-post-01-crop-resize
├── 09-post-02-subtitle-burn
├── 09-post-03-bgm-sfx
├── 09-post-04-concatenation
├── 09-post-05-transitions
└── 09-post-06-color-grading
```

**Wave 4: Quality & Delivery (After Wave 3 - Next 1-2 days)**
```
Developer Team (3 devs):
├── Quality Control (3 tasks)
├── Export & Delivery (3 tasks)
└── Distribution (4 tasks - P2)
```

---

## 🚀 Immediate Next Action

**START HERE: Audio Production (Group 5)**

### Step 1: Review Audio Production Issues
```bash
cd /home/runner/work/StoryGenerator/StoryGenerator
cd issues/p1-high/audio-production
ls -la
cat 07-audio-01-tts-generation/issue.md
cat 07-audio-02-normalization/issue.md
```

### Step 2: Implement TTS Generation
- Choose TTS provider (ElevenLabs recommended, OpenAI alternative)
- Implement Python module: `core/audio_generation.py`
- Add voice selection logic based on demographics
- Create tests: `tests/test_audio_generation.py`
- Update issue template with implementation details

### Step 3: Implement Audio Normalization
- Use pyloudnorm library (already in requirements.txt)
- Implement normalization to -14 LUFS (YouTube standard)
- Add tests for LUFS measurement
- Document normalization parameters

### Step 4: Integration
- Test end-to-end: Script → Scene Plan → Audio Generation
- Verify audio files work with forced alignment tools (Whisper)
- Update pipeline documentation

---

## 📈 Progress Tracking

**Phase 3 Completion Status:**

```
Total Groups: 13
Completed: 4 (31%)
Remaining: 9 (69%)

Total Tasks: 52
Completed: 21 (40%)
Remaining: 31 (60%)

Next Milestone: 50% completion (26 tasks)
Requires: Audio Production (2) + Image Generation (4) + Subtitle Creation (2)
```

**Estimated Timeline:**
- Week 1 Complete: Groups 1-4 (21 tasks) ✅
- Week 2 Target: Groups 5-7 (10 tasks) → 31 tasks (60%)
- Week 3 Target: Groups 8-9 (11 tasks) → 42 tasks (81%)
- Week 4 Target: Groups 10-13 (10 tasks) → 52 tasks (100%) ✅

---

## 🎯 Success Metrics

After completing Audio Production (Group 5), you will have:

✅ End-to-end pipeline from content to audio:
```
Reddit Content → Ideas → Scripts → Scenes → Audio Files
```

✅ Key outputs ready:
- Normalized audio files ready for video synthesis
- Audio duration data for precise video timing
- Audio files ready for forced subtitle alignment

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
