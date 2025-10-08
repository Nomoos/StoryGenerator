# Atomic Issues - Parallel Execution

This directory contains **62 atomic, independently executable issues** that can be worked on in parallel.

## Structure

Each atomic issue is a self-contained task that can be completed by a single person in 1-8 hours.

```
atomic/
├── 00-setup-01-repo-structure/        # P0 - Setup repo folders
├── 00-setup-02-config-files/          # P0 - Create YAML configs
├── 00-setup-03-python-env/            # P0 - Python environment setup
├── 00-setup-04-csharp-projects/       # P0 - C# project structure
├── 01-research-01-ollama-client/      # P0 - Ollama LLM client
├── 01-research-02-whisper-client/     # P0 - Whisper ASR client
├── 01-research-03-ffmpeg-client/      # P0 - FFmpeg media client
├── 01-research-04-sdxl-client/        # P1 - SDXL image client
├── 01-research-05-ltx-client/         # P1 - LTX video client
├── 02-content-01-reddit-scraper/      # P0 - Reddit story mining
├── 02-content-02-alt-sources/         # P1 - Alternative sources
├── 02-content-03-quality-scorer/      # P1 - Story quality assessment
├── 03-ideas-01-reddit-adaptation/     # P1 - Adapt Reddit stories
├── 03-ideas-02-llm-generation/        # P1 - Generate original ideas
├── 03-ideas-03-clustering/            # P1 - Cluster ideas into topics
├── 03-ideas-04-title-generation/      # P1 - Generate titles from topics
├── 04-scoring-01-title-scorer/        # P1 - Score titles for viral potential
├── 04-scoring-02-voice-recommendation/# P1 - Recommend voice (F/M)
├── 04-scoring-03-top-selection/       # P1 - Select top 5 titles
├── 05-script-01-raw-generation/       # P1 - Generate raw scripts
├── 05-script-02-script-scorer/        # P1 - Score scripts
├── 05-script-03-iteration/            # P1 - Iterate scripts locally
├── 05-script-04-gpt-improvement/      # P1 - Improve with GPT/local
├── 05-script-05-title-improvement/    # P1 - Improve titles
├── 06-scenes-01-beat-sheet/           # P1 - Create beat sheets
├── 06-scenes-02-shotlist/             # P1 - Generate shot lists
├── 06-scenes-03-draft-subtitles/      # P1 - Draft subtitle lines
├── 07-audio-01-tts-generation/        # P1 - Generate voiceover
├── 07-audio-02-normalization/         # P1 - Normalize audio LUFS
├── 08-subtitles-01-forced-alignment/  # P1 - Time subtitles to audio
├

://08-subtitles-02-scene-mapping/      # P1 - Map subtitles to shots
├── 09-images-01-prompt-builder/       # P1 - Build SDXL prompts
├── 09-images-02-keyframe-gen-a/       # P1 - Generate keyframes batch A
├── 09-images-03-keyframe-gen-b/       # P2 - Generate keyframes batch B
├── 09-images-04-selection/            # P2 - Select best keyframes
├── 10-video-01-ltx-generation/        # P1 - Generate LTX video clips
├── 10-video-02-interpolation/         # P2 - Interpolate keyframes
├── 10-video-03-variant-selection/     # P2 - Choose video variant
├── 11-post-01-crop-resize/            # P1 - Crop to 9:16
├── 11-post-02-subtitle-burn/          # P1 - Burn/soft subtitles
├── 11-post-03-bgm-sfx/                # P2 - Add background music/SFX
├── 11-post-04-concatenation/          # P1 - Concatenate shots
├── 11-post-05-transitions/            # P2 - Add transitions
├── 12-qc-01-device-preview/           # P1 - Test on devices
├── 12-qc-02-sync-check/               # P1 - Check subtitle sync
├── 12-qc-03-quality-report/           # P1 - Generate QC report
├── 13-export-01-final-encode/         # P1 - Export final video
├── 13-export-02-thumbnail/            # P1 - Generate thumbnail
├── 13-export-03-metadata/             # P1 - Create metadata JSON
├── 14-dist-01-youtube-upload/         # P2 - Upload to YouTube
├── 14-dist-02-tiktok-upload/          # P2 - Upload to TikTok
├── 14-dist-03-instagram-upload/       # P2 - Upload to Instagram
├── 14-dist-04-facebook-upload/        # P2 - Upload to Facebook
├── 15-analytics-01-collection/        # P2 - Collect analytics
├── 15-analytics-02-monetization/      # P2 - Track revenue
├── 15-analytics-03-performance/       # P2 - Evaluate performance
└── 15-analytics-04-optimization/      # P2 - Generate recommendations
```

## Priority Levels

- **P0 (Critical Path)**: Must complete first, ~15 tasks
- **P1 (Core Pipeline)**: Main content pipeline, ~30 tasks
- **P2 (Distribution)**: Publishing and analytics, ~17 tasks

## Parallel Execution Waves

### Wave 1: Foundation (P0 - 7-10 tasks can run in parallel)
1. Setup tasks (00-setup-*)
2. Research prototypes (01-research-*)
3. Reddit scraper (02-content-01)

**Estimated time**: 1-2 days with 10 developers

### Wave 2: Content Pipeline (P1 - 15-20 tasks can run in parallel)
1. Content collection (02-content-*)
2. Ideas & titles (03-ideas-*, 04-scoring-*)
3. Scripts (05-script-*)
4. Scenes & audio (06-scenes-*, 07-audio-*)
5. Images & video (09-images-*, 10-video-*)

**Estimated time**: 3-5 days with 20 developers

### Wave 3: Production & Distribution (P1/P2 - 10-15 tasks can run in parallel)
1. Subtitles (08-subtitles-*)
2. Post-production (11-post-*)
3. QC & export (12-qc-*, 13-export-*)
4. Distribution & analytics (14-dist-*, 15-analytics-*)

**Estimated time**: 2-3 days with 15 developers

## Task Dependencies

Each issue file includes:
- **Dependencies**: Which tasks must complete first
- **Blocks**: Which tasks are waiting on this one
- **Effort**: Estimated hours (1-8)
- **Priority**: P0, P1, or P2
- **Acceptance Criteria**: Clear definition of done

## Usage

1. **Review the dependency graph** in `../INDEX.md`
2. **Assign tasks** based on team skills and availability
3. **Start with P0 tasks** in parallel
4. **Progress to P1** as P0 completes
5. **Finish with P2** distribution tasks
6. **Track progress** using MicrostepValidator per task

## Example: Parallel Team of 10

**Day 1:**
- Dev 1-2: Setup tasks (00-setup-*)
- Dev 3-4: Ollama + Whisper clients (01-research-01, 01-research-02)
- Dev 5-6: FFmpeg + SDXL clients (01-research-03, 01-research-04)
- Dev 7-8: Reddit scraper (02-content-01)
- Dev 9-10: Quality scorer (02-content-03)

**Day 2-3:**
- Dev 1-2: Ideas generation (03-ideas-*)
- Dev 3-4: Title scoring (04-scoring-*)
- Dev 5-6: Script generation (05-script-*)
- Dev 7-8: Audio pipeline (07-audio-*)
- Dev 9-10: Image generation (09-images-*)

**Day 4:**
- Dev 1-3: Video generation (10-video-*)
- Dev 4-6: Post-production (11-post-*)
- Dev 7-9: QC & Export (12-qc-*, 13-export-*)
- Dev 10: Documentation

**Result**: Complete pipeline in 4-5 days vs 4-6 weeks sequentially!

## Notes

- Each task is designed for **1 person, 1-8 hours**
- Tasks with shared dependencies should coordinate
- Use feature branches: `feature/atomic-{task-id}`
- Daily standups to sync on blockers
- MicrostepValidator tracks granular progress

See individual `issue.md` files for detailed requirements.
