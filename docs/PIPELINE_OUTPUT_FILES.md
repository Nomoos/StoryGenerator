# Pipeline Output Files Reference

This document describes all files created by each pipeline operation, including paths, formats, and purposes.

## File Naming Convention

All files follow this pattern:
```
{operation}/{gender}/{age_bucket}/{filename}
```

Where:
- **gender**: `women` or `men`
- **age_bucket**: `10-13`, `14-17`, or `18-23`
- **filename**: Operation-specific naming

---

## Phase 1: Content Pipeline

### 02-content-01: Reddit Scraper
**Output Directory**: `Generator/sources/reddit/{gender}/{age_bucket}/`
**Files Created**:
- `reddit_post_{id}.json` - Raw Reddit post data
  - Contains: title, selftext, score, num_comments, created_utc, url, subreddit
  - Format: JSON
  - Example: `reddit_post_abc123.json`

### 02-content-02: Alternative Sources
**Output Directory**: `Generator/sources/{quora|twitter}/{gender}/{age_bucket}/`
**Files Created**:
- `quora_question_{id}.json` - Quora question and answers
- `twitter_thread_{id}.json` - Twitter thread data

### 02-content-03: Quality Scorer
**Output Directory**: `Generator/scores/{gender}/{age_bucket}/`
**Files Created**:
- `content_scores_{date}.json` - Quality scores for all content
  - Contains: content_id, viral_score, novelty, emotional_impact, clarity, replay_value, shareability
  - Format: JSON with array of scored items
  - Example: `content_scores_2025-01-01.json`

### 02-content-04: Deduplication
**Output Directory**: `Generator/scores/{gender}/{age_bucket}/`
**Files Created**:
- `dedup_report_{date}.json` - Deduplication report
  - Contains: duplicates found, similarity scores, retained items
  - Format: JSON

### 02-content-05: Ranking
**Output Directory**: `Generator/scores/{gender}/{age_bucket}/`
**Files Created**:
- `ranked_content_{date}.json` - Ranked list of content by score
  - Contains: Sorted array of content with final scores
  - Format: JSON

### 02-content-06: Attribution
**Output Directory**: `Generator/sources/reddit/{gender}/{age_bucket}/`
**Files Created**:
- `attribution_{content_id}.json` - Attribution metadata
  - Contains: source_url, author, license, date_scraped, usage_rights

---

## Phase 2: Idea Generation

### 03-ideas-01: Reddit Adaptation
**Output Directory**: `Generator/ideas/{gender}/{age_bucket}/`
**Files Created**:
- `idea_{id}_adapted.txt` - Adapted story idea from Reddit content
  - Contains: Story concept adapted from source content
  - Format: Plain text
  - Example: `idea_001_adapted.txt`

### 03-ideas-02: LLM Generation
**Output Directory**: `Generator/ideas/{gender}/{age_bucket}/`
**Files Created**:
- `idea_{id}_generated.txt` - LLM-generated original story idea
  - Contains: Original story concept from LLM
  - Format: Plain text
  - Example: `idea_002_generated.txt`

### 03-ideas-03: Clustering
**Output Directory**: `Generator/ideas/{gender}/{age_bucket}/`
**Files Created**:
- `clusters_{date}.json` - Idea clusters
  - Contains: Cluster IDs, member ideas, cluster themes
  - Format: JSON

### 03-ideas-04: Title Generation
**Output Directory**: `Generator/titles/{gender}/{age_bucket}/`
**Files Created**:
- `titles_{idea_id}.json` - Generated title variants for an idea
  - Contains: Array of title options with metadata
  - Format: JSON
  - Example: `titles_001.json`

### 04-scoring-01: Title Scorer
**Output Directory**: `Generator/titles/{gender}/{age_bucket}/`
**Files Created**:
- `title_scores_{idea_id}.json` - Title scores
  - Contains: Title variants with viral scores
  - Format: JSON

### 04-scoring-02: Voice Recommendation
**Output Directory**: `Generator/voices/choice/{gender}/{age_bucket}/`
**Files Created**:
- `voice_rec_{idea_id}.json` - Voice recommendation
  - Contains: Recommended voice style, pitch, speed, emotion
  - Format: JSON

### 04-scoring-03: Top Selection
**Output Directory**: `Generator/topics/{gender}/{age_bucket}/`
**Files Created**:
- `selected_topics_{date}.json` - Top-selected topics for production
  - Contains: Final selected topics with all metadata
  - Format: JSON

---

## Phase 3: Script Development

### 05-script-01: Raw Generation
**Output Directory**: `Generator/scripts/raw_local/{gender}/{age_bucket}/`
**Files Created**:
- `script_{topic_id}_v1.txt` - Raw script first draft
  - Contains: Script text with basic structure
  - Format: Plain text
  - Example: `script_001_v1.txt`

### 05-script-02: Script Scorer
**Output Directory**: `Generator/scores/{gender}/{age_bucket}/`
**Files Created**:
- `script_score_{topic_id}_v1.json` - Script quality score
  - Contains: Hook score, pacing, narrative_arc, resolution, overall_score
  - Format: JSON

### 05-script-03: Iteration
**Output Directory**: `Generator/scripts/iter_local/{gender}/{age_bucket}/`
**Files Created**:
- `script_{topic_id}_v2.txt` - Iterated script (second draft)
- `script_{topic_id}_v3.txt` - Further iterations if needed
  - Contains: Improved script based on scoring feedback
  - Format: Plain text

### 05-script-04: GPT Improvement
**Output Directory**: `Generator/scripts/gpt_improved/{gender}/{age_bucket}/`
**Files Created**:
- `script_{topic_id}_final.txt` - GPT-enhanced final script
  - Contains: Polished, publication-ready script
  - Format: Plain text
  - Example: `script_001_final.txt`

### 05-script-05: Title Improvement
**Output Directory**: `Generator/titles/{gender}/{age_bucket}/`
**Files Created**:
- `title_{topic_id}_final.txt` - Final optimized title
  - Contains: Refined title matching final script
  - Format: Plain text

---

## Phase 4: Scene Planning

### 06-scenes-01: Beat Sheet
**Output Directory**: `Generator/scenes/json/{gender}/{age_bucket}/`
**Files Created**:
- `beats_{topic_id}.json` - Story beat sheet with timing
  - Contains: Scene beats, duration, emotional arc, pacing
  - Format: JSON
  - Example: `beats_001.json`

### 06-scenes-02: Shot List
**Output Directory**: `Generator/scenes/json/{gender}/{age_bucket}/`
**Files Created**:
- `shotlist_{topic_id}.json` - Detailed shot list
  - Contains: Array of shots with timing, description, camera angles
  - Format: JSON
  - Example: `shotlist_001.json`

### 06-scenes-03: Draft Subtitles
**Output Directory**: `Generator/subtitles/srt/{gender}/{age_bucket}/`
**Files Created**:
- `subs_{topic_id}_draft.srt` - Draft subtitle file
  - Contains: Subtitle timing and text (rough timing)
  - Format: SRT
  - Example: `subs_001_draft.srt`

---

## Phase 5: Audio Production

### 07-audio-01: TTS Generation
**Output Directory**: `Generator/audio/tts/{gender}/{age_bucket}/`
**Files Created**:
- `voiceover_{topic_id}.wav` - Generated voiceover audio
  - Contains: Speech audio from TTS engine
  - Format: WAV (48kHz, 16-bit, mono)
  - Duration: 30-60 seconds
  - Size: ~5-10 MB
  - Example: `voiceover_001.wav`

### 07-audio-02: Normalization
**Output Directory**: `Generator/audio/normalized/{gender}/{age_bucket}/`
**Files Created**:
- `voiceover_{topic_id}_normalized.wav` - Normalized audio for YouTube
  - Contains: Audio normalized to -14 LUFS
  - Format: WAV (48kHz, 16-bit, mono)
  - Loudness: -14 LUFS ± 0.5
  - True Peak: < -1.0 dBTP
  - Example: `voiceover_001_normalized.wav`
- `normalization_report_{topic_id}.json` - Normalization metrics
  - Contains: Input LUFS, output LUFS, true peak, LRA

---

## Phase 6: Subtitle Creation

### 08-subtitles-01: Forced Alignment
**Output Directory**: `Generator/subtitles/srt/{gender}/{age_bucket}/`
**Files Created**:
- `subs_{topic_id}_aligned.srt` - Precisely aligned subtitles
  - Contains: Word-level aligned subtitle timing
  - Format: SRT with accurate timestamps (±50ms)
  - Example: `subs_001_aligned.srt`
- `alignment_{topic_id}.json` - Alignment metadata
  - Contains: Word timestamps, confidence scores

### 08-subtitles-02: Scene Mapping
**Output Directory**: `Generator/subtitles/timed/{gender}/{age_bucket}/`
**Files Created**:
- `subs_{topic_id}_final.srt` - Final scene-mapped subtitles
  - Contains: Subtitles mapped to video scenes
  - Format: SRT
  - Example: `subs_001_final.srt`
- `subtitle_scenes_{topic_id}.json` - Scene mapping data
  - Contains: Subtitle-to-scene relationships

---

## Phase 7: Image Generation

### 09-images-01: Prompt Builder
**Output Directory**: `Generator/scenes/json/{gender}/{age_bucket}/`
**Files Created**:
- `prompts_{topic_id}.json` - Image generation prompts
  - Contains: SDXL prompts for each scene/shot
  - Format: JSON with array of prompts
  - Example: `prompts_001.json`

### 09-images-02: Keyframe Gen A
**Output Directory**: `Generator/images/keyframes_v1/{gender}/{age_bucket}/`
**Files Created**:
- `keyframe_{topic_id}_shot{N}_v1.png` - First variant keyframes
  - Contains: Generated keyframe image (SDXL)
  - Format: PNG
  - Resolution: 1024x1024 or 1024x1792
  - Size: ~2-5 MB per image
  - Example: `keyframe_001_shot001_v1.png`

### 09-images-03: Keyframe Gen B
**Output Directory**: `Generator/images/keyframes_v2/{gender}/{age_bucket}/`
**Files Created**:
- `keyframe_{topic_id}_shot{N}_v2.png` - Second variant keyframes
  - Contains: Alternative keyframe image (different seed)
  - Format: PNG
  - Resolution: 1024x1024 or 1024x1792
  - Example: `keyframe_001_shot001_v2.png`

### 09-images-04: Selection
**Output Directory**: `Generator/images/keyframes_v1/{gender}/{age_bucket}/` or `keyframes_v2/`
**Files Created**:
- `selection_{topic_id}.json` - Selected keyframes
  - Contains: List of selected keyframes (v1 or v2) for each shot
  - Format: JSON

---

## Phase 8: Video Production

### 10-video-01: LTX Generation
**Output Directory**: `Generator/videos/ltx/{gender}/{age_bucket}/`
**Files Created**:
- `video_{topic_id}_shot{N}.mp4` - LTX-generated video clip
  - Contains: AI-generated video from keyframe
  - Format: MP4 (H.264)
  - Resolution: 1080x1920 (9:16)
  - Frame Rate: 30 fps
  - Duration: 2-5 seconds per shot
  - Size: ~10-30 MB per clip
  - Example: `video_001_shot001.mp4`

### 10-video-02: Interpolation
**Output Directory**: `Generator/videos/interp/{gender}/{age_bucket}/`
**Files Created**:
- `video_{topic_id}_shot{N}_interp.mp4` - Interpolated smooth video
  - Contains: Frame-interpolated video for smoother motion
  - Format: MP4 (H.264)
  - Resolution: 1080x1920
  - Frame Rate: 60 fps (if interpolated)
  - Example: `video_001_shot001_interp.mp4`

### 10-video-03: Variant Selection
**Output Directory**: `Generator/videos/ltx/{gender}/{age_bucket}/`
**Files Created**:
- `variants_{topic_id}.json` - Selected video variants
  - Contains: List of chosen video clips (ltx or interp)
  - Format: JSON

---

## Phase 9: Post-Production

### 11-post-01: Crop & Resize
**Output Directory**: `Generator/final/{gender}/{age_bucket}/temp/`
**Files Created**:
- `video_{topic_id}_cropped.mp4` - Cropped 9:16 video
  - Contains: Video cropped to vertical format
  - Format: MP4 (H.264)
  - Resolution: 1080x1920 (exact)
  - Safe margins: Top 8%, Bottom 10%
  - Example: `video_001_cropped.mp4`

### 11-post-02: Subtitle Burn
**Output Directory**: `Generator/final/{gender}/{age_bucket}/temp/`
**Files Created**:
- `video_{topic_id}_subtitled.mp4` - Video with burned subtitles
  - Contains: Video with hardcoded subtitles
  - Format: MP4 (H.264)
  - Resolution: 1080x1920
  - Example: `video_001_subtitled.mp4`

### 11-post-03: BGM & SFX
**Output Directory**: `Generator/final/{gender}/{age_bucket}/temp/`
**Files Created**:
- `video_{topic_id}_audio_mixed.mp4` - Video with background music and SFX
  - Contains: Video with voiceover + BGM + sound effects
  - Format: MP4 (H.264)
  - Audio: -14 LUFS (normalized)
  - Example: `video_001_audio_mixed.mp4`

### 11-post-04: Concatenation
**Output Directory**: `Generator/final/{gender}/{age_bucket}/temp/`
**Files Created**:
- `video_{topic_id}_concatenated.mp4` - All shots concatenated
  - Contains: Single video with all scenes joined
  - Format: MP4 (H.264)
  - Duration: 30-60 seconds
  - Example: `video_001_concatenated.mp4`

### 11-post-05: Transitions
**Output Directory**: `Generator/final/{gender}/{age_bucket}/temp/`
**Files Created**:
- `video_{topic_id}_transitions.mp4` - Video with scene transitions
  - Contains: Video with fade/dissolve transitions between scenes
  - Format: MP4 (H.264)
  - Example: `video_001_transitions.mp4`

### 11-post-06: Color Grading
**Output Directory**: `Generator/final/{gender}/{age_bucket}/temp/`
**Files Created**:
- `video_{topic_id}_graded.mp4` - Color-graded video
  - Contains: Video with applied color LUT
  - Format: MP4 (H.264)
  - Example: `video_001_graded.mp4`

---

## Phase 10: Quality Control

### 12-qc-01: Device Preview
**Output Directory**: `Generator/final/{gender}/{age_bucket}/`
**Files Created**:
- `preview_report_{topic_id}.json` - Device preview report
  - Contains: Screenshots from various device previews
  - Format: JSON + PNG screenshots

### 12-qc-02: Sync Check
**Output Directory**: `Generator/final/{gender}/{age_bucket}/`
**Files Created**:
- `sync_report_{topic_id}.json` - Audio/video sync analysis
  - Contains: Sync offset measurements, frame drops
  - Format: JSON

### 12-qc-03: Quality Report
**Output Directory**: `Generator/final/{gender}/{age_bucket}/`
**Files Created**:
- `quality_report_{topic_id}.json` - Comprehensive quality assessment
  - Contains: Technical metrics, quality scores, issues found
  - Format: JSON

---

## Phase 11: Export & Delivery

### 13-export-01: Final Encode
**Output Directory**: `Generator/final/{gender}/{age_bucket}/`
**Files Created**:
- `video_{topic_id}_final.mp4` - **FINAL DELIVERABLE VIDEO**
  - Contains: Publication-ready video
  - Format: MP4 (H.264, High Profile)
  - Resolution: 1080x1920 (9:16 vertical)
  - Frame Rate: 30 fps
  - Video Bitrate: 8-12 Mbps (CRF 23)
  - Audio: AAC, 48kHz, stereo, -14 LUFS
  - Duration: 30-60 seconds
  - Size: ~30-80 MB
  - Example: `video_001_final.mp4`

### 13-export-02: Thumbnail
**Output Directory**: `Generator/final/{gender}/{age_bucket}/`
**Files Created**:
- `thumbnail_{topic_id}.jpg` - Video thumbnail
  - Contains: Eye-catching thumbnail image
  - Format: JPEG
  - Resolution: 1920x1080 (16:9 for YouTube)
  - Size: < 2 MB
  - Example: `thumbnail_001.jpg`

### 13-export-03: Metadata
**Output Directory**: `Generator/final/{gender}/{age_bucket}/`
**Files Created**:
- `metadata_{topic_id}.json` - Video metadata
  - Contains: Title, description, tags, category, attribution
  - Format: JSON
  - Example: `metadata_001.json`

---

## Phase 12: Distribution

### 14-dist-01: YouTube Upload
**Output Directory**: `Generator/final/{gender}/{age_bucket}/`
**Files Created**:
- `youtube_upload_{topic_id}.json` - Upload result
  - Contains: Video ID, upload timestamp, URL, status
  - Format: JSON

### 14-dist-02: TikTok Upload
**Output Directory**: `Generator/final/{gender}/{age_bucket}/`
**Files Created**:
- `tiktok_upload_{topic_id}.json` - Upload result
  - Contains: Video ID, upload timestamp, URL, status
  - Format: JSON

### 14-dist-03: Instagram Upload
**Output Directory**: `Generator/final/{gender}/{age_bucket}/`
**Files Created**:
- `instagram_upload_{topic_id}.json` - Upload result
  - Contains: Media ID, upload timestamp, URL, status
  - Format: JSON

### 14-dist-04: Facebook Upload
**Output Directory**: `Generator/final/{gender}/{age_bucket}/`
**Files Created**:
- `facebook_upload_{topic_id}.json` - Upload result
  - Contains: Video ID, upload timestamp, URL, status
  - Format: JSON

---

## Phase 13: Analytics

### 15-analytics-01: Collection
**Output Directory**: `Generator/final/{gender}/{age_bucket}/`
**Files Created**:
- `analytics_{topic_id}_{date}.json` - Analytics snapshot
  - Contains: Views, likes, comments, shares, watch time
  - Format: JSON
  - Updated: Daily

### 15-analytics-02: Monetization
**Output Directory**: `Generator/final/{gender}/{age_bucket}/`
**Files Created**:
- `monetization_{topic_id}_{date}.json` - Revenue data
  - Contains: Ad revenue, RPM, CPM
  - Format: JSON

### 15-analytics-03: Performance
**Output Directory**: `Generator/final/{gender}/{age_bucket}/`
**Files Created**:
- `performance_{topic_id}_{date}.json` - Performance metrics
  - Contains: CTR, average view duration, engagement rate
  - Format: JSON

### 15-analytics-04: Optimization
**Output Directory**: `Generator/final/{gender}/{age_bucket}/`
**Files Created**:
- `optimization_{topic_id}.json` - Recommendations
  - Contains: Insights and suggestions for improvement
  - Format: JSON

---

## Summary of Key Output Files

### Most Important Files (Per Video)

1. **Final Video**: `Generator/final/{gender}/{age_bucket}/video_{topic_id}_final.mp4`
2. **Voiceover (Normalized)**: `Generator/audio/normalized/{gender}/{age_bucket}/voiceover_{topic_id}_normalized.wav`
3. **Final Subtitles**: `Generator/subtitles/timed/{gender}/{age_bucket}/subs_{topic_id}_final.srt`
4. **Thumbnail**: `Generator/final/{gender}/{age_bucket}/thumbnail_{topic_id}.jpg`
5. **Metadata**: `Generator/final/{gender}/{age_bucket}/metadata_{topic_id}.json`

### File Size Estimates (Per Video)

- **Raw Assets**: ~100-200 MB
  - Audio: ~10-20 MB
  - Images: ~30-60 MB (10-15 keyframes × ~3-5 MB each)
  - Video clips: ~50-120 MB (10-15 clips × ~5-10 MB each)
- **Working Files**: ~150-300 MB
  - Post-production temp files
- **Final Deliverables**: ~30-80 MB
  - Final video: ~30-80 MB
  - Thumbnail: < 2 MB
  - Metadata/JSON: < 1 MB

### Total Storage (Per Video): ~280-580 MB

### Archive Recommendations

After distribution and initial analytics period (30 days):
- **Keep**: Final video, metadata, analytics
- **Archive to cold storage**: Raw assets, intermediate files
- **Delete**: Temporary post-production files

---

**Document Version**: 1.0
**Last Updated**: 2025-01-01
**Configuration**: `config/pipeline.yaml`
**Folder Structure**: `docs/GENERATOR_STRUCTURE.md`
