# Group 3: Audio & Visual Assets

**Focus Areas:**
- Scene planning and shot lists
- Audio production (TTS, normalization)
- Image generation (SDXL keyframes)
- Subtitle generation and timing

**Independence Level:** ⚡ **Parallel Independent** - Works with completed scripts, produces multiple asset types in parallel without internal dependencies

---

## 📋 Current Status

**Progress Hub:** See [PROGRESS.md](./PROGRESS.md) for comprehensive status tracking  
**Current Priority:** See [.NEXT.MD](.NEXT.MD) for the current focus item

**Open Issues:** See [.ISSUES/](.ISSUES/) folder (2 tasks: voice cloning, style consistency)  
**Completed Issues:** See [.DONE/](.DONE/) folder

---

## 🎯 Responsibilities

### Scene Planning
- Beat sheet creation from scripts
- Shot list generation
- Visual prompt engineering
- Scene-to-shot breakdown

### Audio Production
- Text-to-speech generation
- Audio normalization and enhancement
- Voice selection and recommendation
- Audio quality control

### Image Generation
- SDXL keyframe generation
- Visual prompt optimization
- Image quality assessment
- Style consistency validation

### Subtitle Generation
- Forced alignment with audio
- Word-level timing
- Subtitle formatting (SRT)
- Scene-subtitle mapping

---

## 🔄 Pipeline Independence

This group operates in **parallel asset production mode**:
- **Input:** Completed scripts from Group 2
- **Output:** Audio files, keyframe images, and timed subtitles
- **Dependencies:** Scripts from Group 2, infrastructure from Group 1
- **Consumers:** Provides assets to Group 4 for video assembly
- **Parallelization:** Audio, images, and subtitles can be produced simultaneously

---

## 📚 Related Documentation

- [MainProgressHub.md](../../MainProgressHub.md) - Overall progress tracking structure
- [HYBRID_ROADMAP.md](../../docs/roadmaps/HYBRID_ROADMAP.md) - Project roadmap
- [Group 4 Scene Planning](../../issues/resolved/phase-3-implementation/group-4-scene-planning/) - Related completed work
- [Group 7 Image Generation](../../issues/resolved/phase-3-implementation/group-7-image-generation/) - Related completed work

---

## 🔄 Workflow

1. **Pick a task** from `.ISSUES/` or create a new one
2. **Update `.NEXT.MD`** to reflect your current focus
3. **Work on the task** following TDD principles
4. **Update progress** in the child issue file
5. **Complete and move** from `.ISSUES/` to `.DONE/` when finished
6. **Sync roadmap** - Update HYBRID_ROADMAP.md with status changes

---

## 📝 Child Issue Template

Create new issues using the template in [MainProgressHub.md](../../MainProgressHub.md#-child-issue-template).
