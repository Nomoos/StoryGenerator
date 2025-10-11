# Story Generator Pipeline Checklist

This checklist tracks all pipeline operations from content sourcing to final distribution. Check off each step as you complete it for a story video.

## Story Information

- **Story ID**: `_______________________`
- **Target Audience**: `_______________________` (e.g., women/10-13)
- **Start Date**: `_______________________`
- **Completion Date**: `_______________________`

---

## Phase 1: Content Pipeline (6 operations)

### Content Sourcing
- [ ] **Reddit Scraper** - Scrape potential stories from Reddit
- [ ] **Alternative Sources** - Scrape from Quora, Twitter, other sources
- [ ] **Quality Scorer** - Score content quality and viral potential
- [ ] **Deduplication** - Remove duplicate or similar content
- [ ] **Ranking** - Rank content by viral score
- [ ] **Attribution** - Track and store content attribution data

---

## Phase 2: Idea Generation (7 operations)

### Idea Development
- [ ] **Reddit Adaptation** - Adapt Reddit content into story ideas
- [ ] **LLM Generation** - Generate original story ideas using LLM
- [ ] **Clustering** - Cluster similar ideas together
- [ ] **Title Generation** - Generate compelling titles

### Idea Scoring
- [ ] **Title Scorer** - Score titles for viral potential
- [ ] **Voice Recommendation** - Recommend voice style for story
- [ ] **Top Selection** - Select top-scoring ideas for production

---

## Phase 3: Script Development (5 operations)

### Script Creation
- [ ] **Raw Generation** - Generate raw script from idea
- [ ] **Script Scorer** - Score script quality
- [ ] **Iteration** - Iterate and improve script based on score
- [ ] **GPT Improvement** - Use GPT to enhance script quality
- [ ] **Title Improvement** - Refine title based on final script

---

## Phase 4: Scene Planning (3 operations)

### Scene Breakdown
- [ ] **Beat Sheet** - Create story beat sheet with timing
- [ ] **Shot List** - Generate detailed shot list for each scene
- [ ] **Draft Subtitles** - Create draft subtitle timing

---

## Phase 5: Audio Production (2 operations)

### Voiceover Creation
- [ ] **TTS Generation** - Generate voiceover using text-to-speech
- [ ] **Normalization** - Normalize audio to -14 LUFS for YouTube

---

## Phase 6: Subtitle Creation (2 operations)

### Subtitle Timing
- [ ] **Forced Alignment** - Align words with audio timestamps
- [ ] **Scene Mapping** - Map subtitles to video scenes

---

## Phase 7: Image Generation (4 operations)

### Keyframe Creation
- [ ] **Prompt Builder** - Build image prompts from script
- [ ] **Keyframe Gen A** - Generate first set of keyframes
- [ ] **Keyframe Gen B** - Generate second set of keyframes (variation)
- [ ] **Selection** - Select best keyframes for each scene

---

## Phase 8: Video Production (3 operations)

### Video Synthesis
- [ ] **LTX Generation** - Generate video clips using LTX Video
- [ ] **Interpolation** - Interpolate frames for smooth motion
- [ ] **Variant Selection** - Select best video variants

---

## Phase 9: Post-Production (6 operations)

### Video Enhancement
- [ ] **Crop & Resize** - Crop to 9:16 aspect ratio (1080x1920)
- [ ] **Subtitle Burn** - Burn subtitles into video
- [ ] **BGM & SFX** - Add background music and sound effects
- [ ] **Concatenation** - Concatenate all clips into single video
- [ ] **Transitions** - Add transitions between scenes
- [ ] **Color Grading** - Apply color grading for visual consistency

---

## Phase 10: Quality Control (3 operations)

### Quality Validation
- [ ] **Device Preview** - Preview on mobile devices
- [ ] **Sync Check** - Verify audio/video/subtitle sync
- [ ] **Quality Report** - Generate quality assessment report

---

## Phase 11: Export & Delivery (3 operations)

### Final Output
- [ ] **Final Encode** - Encode final video for distribution
- [ ] **Thumbnail** - Generate eye-catching thumbnail
- [ ] **Metadata** - Prepare metadata (title, description, tags)

---

## Phase 12: Distribution (4 operations)

### Platform Upload
- [ ] **YouTube Upload** - Upload to YouTube with metadata
- [ ] **TikTok Upload** - Upload to TikTok
- [ ] **Instagram Upload** - Upload to Instagram Reels
- [ ] **Facebook Upload** - Upload to Facebook

---

## Phase 13: Analytics (4 operations)

### Performance Tracking
- [ ] **Collection** - Collect view/engagement analytics
- [ ] **Monetization** - Track revenue and monetization data
- [ ] **Performance** - Analyze video performance metrics
- [ ] **Optimization** - Generate recommendations for next video

---

## Summary

**Total Operations**: 52
- **Completed**: `_______` / 52
- **Success Rate**: `_______%`
- **Time Taken**: `_______` hours

## Notes

```
Add any notes, issues encountered, or learnings from this pipeline run:

```

---

**Checklist Version**: 1.0
**Last Updated**: 2025-01-01
**Pipeline Configuration**: `config/pipeline.yaml`
