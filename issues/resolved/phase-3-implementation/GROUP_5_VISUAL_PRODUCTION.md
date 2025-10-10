# Group 5: Visual & Final Production

**Phase:** 3 - Implementation  
**Total Tasks:** 18  
**Priority:** P1 (after Group 4 completion)  
**Duration:** 45-60 hours (5-7 days)  
**Team Size:** 8-10 developers  
**Status:** NOT STARTED

## Overview

Group 5 represents the final phase of the video generation pipeline, transforming scripts and audio into polished, distribution-ready videos. This group encompasses subtitle alignment, image generation, video synthesis, post-production effects, and comprehensive quality control.

**Key Components:**
- **Subtitle Creation:** Precise word-level alignment and scene mapping
- **Image Generation:** AI-powered keyframe generation with SDXL
- **Video Production:** Frame-to-video synthesis with LTX-Video
- **Post-Production:** Assembly, effects, and finalization
- **Quality Control:** Comprehensive validation before delivery

## Dependencies

**Requires (Group 4 completion):**
- Script Development group (finalized scripts)
- Scene Planning group (beat sheets, shot lists)
- Audio Production group (normalized voiceovers)

**Blocks:**
- Export & Delivery group (needs QC-approved videos)
- Distribution pipeline

## Task Categories

### 1. Subtitle Creation (2 tasks, 6-8 hours)

**Purpose:** Generate precisely timed subtitles and map them to video scenes

**Tasks:**
1. ✅ `08-subtitles-01-forced-alignment` (P1, 4-5h) - Word-level alignment with Whisper
2. ✅ `08-subtitles-02-scene-mapping` (P1, 2-3h) - Map subtitle timings to shots

**Implementation Status:**
- C# implementation complete: `StoryGenerator.Core.Services.SubtitleAligner`
- Interface: `ISubtitleAligner`
- Example: `SubtitleAlignment.Example`

**Outputs:**
```
Generator/subtitles/
├── timed/{gender}/{age}/{title_id}.srt
├── timed/{gender}/{age}/{title_id}.vtt
└── mapped/{gender}/{age}/{title_id}_subs_to_shots.json
```

---

### 2. Image Generation (4 tasks, 15-19 hours)

**Purpose:** Generate high-quality keyframes for each video shot using SDXL

**Tasks:**
1. `09-images-01-prompt-builder` (P1, 3-4h) - Build SDXL prompts from shot descriptions
2. `09-images-02-keyframe-gen-a` (P1, 5-6h) - Generate keyframes batch A (shots 1-N/2)
3. `09-images-03-keyframe-gen-b` (P2, 5-6h) - Generate keyframes batch B (shots N/2+1-N)
4. `09-images-04-selection` (P2, 2-3h) - Select best keyframe variants per shot

**Implementation Status:**
- C# implementation complete: `Generators.KeyframeGenerationService`
- Interface: `IKeyframeGenerationService`
- Example: `Examples.KeyframeGenerationExample`

**Key Features:**
- Multi-variant generation (3-5 per shot)
- LoRA support for style consistency
- Quality-based selection
- Batch processing for efficiency

**Outputs:**
```
Generator/images/
├── prompts/{gender}/{age}/{title_id}_prompts.json
├── keyframes/{gender}/{age}/{title_id}/shot_{n}/
│   ├── variant_1.png
│   ├── variant_2.png
│   └── variant_3.png
└── selected/{gender}/{age}/{title_id}/shot_{n}_selected.png
```

---

### 3. Video Production (3 tasks, 15-20 hours)

**Purpose:** Synthesize video clips from keyframes using AI-powered generation

**Tasks:**
1. `10-video-01-ltx-generation` (P1, 6-8h) - Generate video clips with LTX-Video
2. `10-video-02-interpolation` (P2, 5-7h) - Frame interpolation (RIFE/FILM)
3. `10-video-03-variant-selection` (P2, 4-5h) - Select best video variant per shot

**Implementation Status:**
- C# implementation complete: `Generators.LTXVideoSynthesizer`
- Interface: `IVideoSynthesizer`
- Factory: `IVideoSynthesizerFactory`
- Alternative: `KeyframeVideoSynthesizer` (interpolation-based)

**Key Features:**
- Multiple synthesis strategies (LTX-Video, interpolation)
- Variant generation and selection
- Duration control (3-5 seconds per shot)
- Quality assessment

**Outputs:**
```
Generator/videos/
├── ltx/{gender}/{age}/{title_id}/shot_{n}/
│   ├── variant_1.mp4
│   ├── variant_2.mp4
│   └── variant_3.mp4
├── interpolated/{gender}/{age}/{title_id}/shot_{n}/
│   └── interpolated.mp4
└── selected/{gender}/{age}/{title_id}/shot_{n}_selected.mp4
```

---

### 4. Post-Production (6 tasks, 10-15 hours)

**Purpose:** Assemble and enhance video clips into polished final output

**Tasks:**
1. `11-post-01-crop-resize` (P1, 2-3h) - Crop to 9:16 aspect ratio for mobile
2. `11-post-02-subtitle-burn` (P1, 2-3h) - Burn or soft-code subtitles
3. `11-post-03-bgm-sfx` (P2, 2-3h) - Add background music and sound effects
4. `11-post-04-concatenation` (P1, 1-2h) - Concatenate all scene clips
5. `11-post-05-transitions` (P2, 1-2h) - Add transitions between scenes
6. `11-post-06-color-grading` (P2, 2-3h) - Apply color grading and filters

**Implementation Status:**
- C# implementation complete: `Tools.VideoPostProducer`
- Interface: `IVideoPostProducer`
- Example: `Examples.VideoPostProductionExample`

**Key Features:**
- Intelligent cropping (face detection, safe zones)
- Multiple subtitle styles
- Audio ducking for background music
- Smooth transitions (fade, dissolve, wipe)
- Color grading presets

**Outputs:**
```
Generator/post/
├── cropped/{gender}/{age}/{title_id}_cropped.mp4
├── with_subs/{gender}/{age}/{title_id}_subs.mp4
├── with_audio/{gender}/{age}/{title_id}_audio.mp4
└── final_draft/{gender}/{age}/{title_id}_final.mp4
```

---

### 5. Quality Control (3 tasks, 6-8 hours)

**Purpose:** Validate video quality and ensure distribution readiness

**Tasks:**
1. `12-qc-01-device-preview` (P1, 2-3h) - Generate device-specific previews
2. `12-qc-02-sync-check` (P1, 2-3h) - Verify audio-subtitle synchronization
3. `12-qc-03-quality-report` (P1, 2-3h) - Generate comprehensive QC report

**Key Checks:**
- A/V synchronization (±50ms tolerance)
- Subtitle readability (contrast, timing)
- Audio levels (LUFS -14.0 ±1.0)
- Video quality (bitrate, resolution, artifacts)
- Device compatibility (iOS, Android)
- Safe zone compliance (text visibility)

**Outputs:**
```
Generator/qc/
├── device_tests/{gender}/{age}/{title_id}/
│   ├── iphone_preview.mp4
│   └── android_preview.mp4
├── sync_reports/{gender}/{age}/{title_id}_sync_report.json
└── quality_reports/{gender}/{age}/{title_id}_qc_report.json
```

---

## Execution Strategy

### Parallel Execution Plan

```
Week 1 (Days 1-2): Subtitle Creation + Image Generation Setup
├── Team A (2 devs): Subtitle alignment integration and testing
├── Team B (3 devs): Prompt builder + Keyframe generation batch A
└── Team C (2 devs): Keyframe generation batch B setup

Week 1 (Days 3-4): Video Production + Post-Production Setup
├── Team A (2 devs): LTX-Video integration
├── Team B (3 devs): Frame interpolation + Variant selection
└── Team C (3 devs): Post-production pipeline (crop, subtitles, concat)

Week 2 (Days 5-6): Post-Production Completion + QC
├── Team A (2 devs): Background music + Transitions + Color grading
├── Team B (3 devs): Quality control implementation
└── Team C (3 devs): Integration testing and pipeline orchestration

Week 2 (Day 7): Final Testing & Documentation
└── All Teams: End-to-end testing, documentation, code review
```

### Critical Path

```
Subtitle Creation (6-8h)
    ↓
Image Generation (15-19h)
    ↓
Video Production (15-20h)
    ↓
Post-Production (10-15h)
    ↓
Quality Control (6-8h)
```

**Total Sequential Time:** 52-70 hours  
**With Parallelization:** 45-60 hours (5-7 days with proper team coordination)

---

## Success Criteria

### Subtitle Creation
- [x] C# implementation complete and tested
- [ ] Word-level timestamps accurate to ±50ms
- [ ] SRT and VTT formats generated
- [ ] Shot mapping JSON created
- [ ] Integration tests passing

### Image Generation
- [x] C# implementation complete and tested
- [ ] SDXL prompts generated from shot descriptions
- [ ] 3-5 keyframe variants per shot
- [ ] Quality selection algorithm implemented
- [ ] Batch processing optimized
- [ ] Output manifests generated

### Video Production
- [x] C# implementation complete and tested
- [ ] LTX-Video integration functional
- [ ] Frame interpolation working (alternative method)
- [ ] Variant selection automated
- [ ] 3-5 second clips per shot
- [ ] Smooth motion and quality

### Post-Production
- [x] C# implementation complete and tested
- [ ] 9:16 aspect ratio cropping accurate
- [ ] Subtitle burn-in with safe zones
- [ ] Background music with ducking
- [ ] Scene concatenation seamless
- [ ] Transitions smooth and professional
- [ ] Color grading applied

### Quality Control
- [ ] Device previews generated
- [ ] A/V sync verified (±50ms)
- [ ] Audio levels validated (-14.0 LUFS ±1.0)
- [ ] Video quality metrics checked
- [ ] QC report generated
- [ ] Pass/fail criteria enforced

### Integration
- [ ] Full pipeline runs end-to-end
- [ ] All intermediate files preserved
- [ ] Error handling robust
- [ ] Progress tracking implemented
- [ ] Performance benchmarks met

---

## Quick Start

### Prerequisites

```bash
# C# Implementation (recommended)
cd src/CSharp
dotnet restore
dotnet build

# Python services (Whisper, SDXL, LTX-Video)
pip install -r requirements.txt

# FFmpeg for video processing
# Install from https://ffmpeg.org/
```

### Running Individual Stages

```bash
# 1. Subtitle Alignment
cd src/CSharp/SubtitleAlignment.Example
dotnet run -- path/to/audio.mp3 women 18-23 story_001

# 2. Keyframe Generation
cd src/CSharp/Examples
dotnet run --project KeyframeGenerationExample.csproj

# 3. Video Synthesis
cd src/CSharp/Examples
dotnet run --project VideoSynthesisExample.csproj

# 4. Post-Production
cd src/CSharp/Examples
dotnet run --project VideoPostProductionExample.csproj
```

### Running Full Pipeline

```bash
# Python orchestration (to be implemented)
python -m scripts.pipeline.run_group5 \
  --title-id story_001 \
  --gender women \
  --age 18-23 \
  --script-path data/Generator/scripts/women/18-23/story_001.txt \
  --audio-path data/Generator/audio/women/18-23/story_001.wav

# Expected outputs:
# - Subtitles: data/Generator/subtitles/timed/women/18-23/story_001.srt
# - Images: data/Generator/images/selected/women/18-23/story_001/
# - Videos: data/Generator/videos/selected/women/18-23/story_001/
# - Final: data/Generator/post/final_draft/women/18-23/story_001_final.mp4
# - QC Report: data/Generator/qc/quality_reports/women/18-23/story_001_qc_report.json
```

---

## Testing Strategy

### Unit Tests

```bash
# C# unit tests
cd src/CSharp
dotnet test

# Python unit tests (when implemented)
pytest tests/pipeline/test_subtitle_creation.py
pytest tests/pipeline/test_image_generation.py
pytest tests/pipeline/test_video_production.py
pytest tests/pipeline/test_post_production.py
pytest tests/pipeline/test_quality_control.py
```

### Integration Tests

```bash
# Test full pipeline with sample data
pytest tests/integration/test_group5_pipeline.py -v

# Test individual stages
pytest tests/integration/test_subtitle_stage.py
pytest tests/integration/test_image_stage.py
pytest tests/integration/test_video_stage.py
pytest tests/integration/test_post_stage.py
pytest tests/integration/test_qc_stage.py
```

### Performance Benchmarks

**Target Performance:**
- Subtitle alignment: < 30 seconds per minute of audio
- Keyframe generation: < 60 seconds per shot (SDXL)
- Video synthesis: < 120 seconds per shot (LTX-Video)
- Post-production: < 60 seconds per final video
- Quality control: < 30 seconds per video

**Total Pipeline:** < 30 minutes for a 60-second video

---

## Implementation Notes

### Existing C# Implementation

Group 5 benefits from substantial existing C# implementation:

✅ **Subtitle Creation:** Fully implemented
- `StoryGenerator.Core.Services.SubtitleAligner`
- Uses faster-whisper for word-level alignment
- Supports SRT and VTT formats
- Shot mapping included

✅ **Image Generation:** Fully implemented
- `Generators.KeyframeGenerationService`
- SDXL integration complete
- Multi-variant generation
- Quality-based selection

✅ **Video Production:** Fully implemented
- `Generators.LTXVideoSynthesizer`
- `Generators.KeyframeVideoSynthesizer`
- Multiple synthesis strategies
- Variant management

✅ **Post-Production:** Fully implemented
- `Tools.VideoPostProducer`
- Complete FFmpeg integration
- Cropping, subtitles, concatenation
- Transitions and color grading

❌ **Quality Control:** Not yet implemented
- Need to implement QC validation
- Device preview generation
- Sync checking
- Quality metrics and reporting

### What Needs to Be Done

1. **Python Pipeline Orchestration**
   - Create `scripts/pipeline/run_group5.py`
   - Integrate C# tools via subprocess
   - Add progress tracking and logging

2. **Quality Control Implementation**
   - Device preview generation
   - A/V sync verification
   - Quality metrics collection
   - Report generation

3. **Integration Testing**
   - End-to-end pipeline tests
   - Performance benchmarking
   - Error handling validation

4. **Documentation Updates**
   - Update all 18 issue.md files
   - Create user guides
   - Add troubleshooting docs

---

## Related Documentation

- [P1_PARALLEL_TASK_GROUPS.md](../../P1_PARALLEL_TASK_GROUPS.md) - Overview of all P1 groups
- [PIPELINE_ORCHESTRATION.md](../../docs/PIPELINE_ORCHESTRATION.md) - Complete pipeline architecture
- [SUBTITLE_ALIGNMENT.md](../../src/CSharp/SUBTITLE_ALIGNMENT.md) - Subtitle creation details
- [KEYFRAME_GENERATION_README.md](../../src/CSharp/KEYFRAME_GENERATION_README.md) - Image generation guide
- [POST_PRODUCTION_CSHARP.md](../../src/CSharp/POST_PRODUCTION_CSHARP.md) - Post-production implementation

---

## Next Steps After Completion

After Group 5 is complete:
1. **Export & Delivery** - Final video packaging and upload
2. **Distribution** - Platform-specific delivery (YouTube, TikTok, Instagram)
3. **Analytics** - Performance tracking and optimization
4. **Iteration** - Content improvement based on performance data

---

## Issues & Support

For issues or questions about Group 5 implementation:
1. Check individual task issue.md files in subdirectories
2. Review C# implementation guides in `src/CSharp/`
3. Review Python examples in `examples/`
4. Open a GitHub issue with `[Group 5]` tag

---

## Version History

**v1.0.0** (Current)
- Initial comprehensive group documentation
- Detailed task breakdown
- Execution strategy defined
- Success criteria established
