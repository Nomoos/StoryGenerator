# Frequently Asked Questions (FAQ)

## General Questions

### What is StoryGenerator?

StoryGenerator is an AI-driven video content pipeline that creates engaging short-form vertical videos for TikTok, YouTube Shorts, and Instagram Reels. It automates the process from story idea to final video with voiceovers and subtitles.

### What does the pipeline currently do?

**Currently Implemented**:
- ✅ Story idea generation with metadata
- ✅ AI-generated scripts (~360 words, optimized for engagement)
- ✅ Script revision for voice clarity
- ✅ AI voice synthesis (ElevenLabs)
- ✅ Word-level subtitle generation (WhisperX)
- ✅ Basic video export (audio with static image)

**Coming Soon**:
- 🔄 Shotlist generation (scene breakdown)
- 🔄 SDXL keyframe generation (high-quality images)
- 🔄 Video synthesis (animated scenes)
- 🔄 Dynamic subtitle overlay
- 🔄 Vision guidance for quality control

### How long does it take to generate a video?

**Current pipeline** (script + voice + subtitles):
- ~3-5 minutes per video (with GPU)
- ~5-10 minutes per video (without GPU)

**Full pipeline** (when complete):
- Estimated ~8-15 minutes per video

Time varies based on:
- Script length
- API response times
- GPU availability
- Model sizes used

---

## Technical Questions

### What are the system requirements?

**Minimum**:
- Python 3.8+
- 16GB RAM
- 50GB disk space
- Internet connection for APIs

**Recommended**:
- Python 3.10+
- 32GB RAM
- NVIDIA GPU with 16GB VRAM
- 100GB SSD storage
- Fast internet connection

See [INSTALLATION.md](INSTALLATION.md) for details.

### Do I need a GPU?

**Currently**: No, but recommended for faster subtitle generation (WhisperX).

**Future**: Yes, GPU will be strongly recommended for:
- SDXL image generation
- Video synthesis
- Vision model inference

Without GPU, these stages will be significantly slower or may not work.

### What GPU do I need?

Recommended:
- NVIDIA RTX 3090 (24GB VRAM) or better
- NVIDIA RTX 4080/4090
- NVIDIA A5000/A6000

Minimum for future features:
- NVIDIA RTX 3060 (12GB VRAM)
- NVIDIA RTX 4060 Ti (16GB)

AMD GPUs and Apple Silicon support is not currently planned.

### Can I run this on Mac?

**Currently**: Yes, for CPU-based features:
- Script generation (uses OpenAI API)
- Voice synthesis (uses ElevenLabs API)
- Basic audio processing

**Limitations**:
- WhisperX will be slower on CPU
- Future GPU features (SDXL, video synthesis) won't work
- Better to use cloud GPU instances

### Can I run this on Windows?

Yes! The pipeline supports Windows 10/11. Follow the Windows installation steps in [INSTALLATION.md](INSTALLATION.md).

---

## API and Cost Questions

### What API keys do I need?

**Required**:
1. **OpenAI API key** - for script generation (GPT-4o-mini)
2. **ElevenLabs API key** - for voice synthesis

**Optional** (future):
- HuggingFace token (for some models)

### How much does it cost to generate a video?

**Current costs per video**:

| Service | Usage | Cost |
|---------|-------|------|
| OpenAI GPT-4o-mini | ~800 tokens | ~$0.01 |
| ElevenLabs | ~360 words | ~$0.05-0.15 |
| WhisperX | Local model | Free |
| **Total** | | **~$0.06-0.16** |

**Future costs** (estimated):
- SDXL: Free (local model, uses GPU)
- Video synthesis: Free (local model, uses GPU)
- **Total**: ~$0.06-0.16 per video

Costs vary based on:
- Script length
- Voice quality settings
- Retry/regeneration needs

### Can I use free tiers?

- **OpenAI**: No free tier, but GPT-4o-mini is very affordable
- **ElevenLabs**: Yes! Free tier provides 10,000 characters/month (~28 videos)
- **WhisperX**: Free (open-source, local)

### Are there alternatives to paid APIs?

**For Scripts**:
- Use local LLMs (Llama-3.1, Qwen2.5) - free but needs GPU
- Implementation planned in roadmap

**For Voice**:
- Use Coqui TTS (open-source) - free but lower quality
- Use Microsoft Azure TTS - paid alternative
- Not currently implemented

---

## Usage Questions

### How do I customize the story style?

Edit the `StoryIdea` parameters:

```python
story = StoryIdea(
    story_title="Your Title",
    narrator_gender="female",  # or "male"
    tone="emotional, dark",    # customize tone
    theme="mystery, betrayal", # main themes
    emotional_core="fear, suspense",
    voice_style="tense, dramatic",
    # ... many more options
)
```

See `examples/custom_story_ideas.py` for examples.

### Can I use my own script instead of AI-generated?

Yes! Place your script in:
```
Stories/1_Scripts/Your_Story_Title/Script.txt
```

Then run from revision stage:
```python
reviser = RevisedScriptGenerator()
reviser.Revise(story_idea)
```

### How do I change the voice?

Edit `Generators/GVoice.py`:

```python
voice=Voice(
    voice_id='BZgkqPqms7Kj9ulSkVzn',  # Change this
    style='Creative'
)
```

Find voice IDs at [ElevenLabs Voice Library](https://elevenlabs.io/voice-library).

### Can I generate videos in other languages?

**Currently**: Limited. The pipeline is optimized for English.

**Potential modifications**:
- Change WhisperX language parameter
- Use multilingual voices in ElevenLabs
- Adjust script generation prompts

Full multi-language support is not currently planned but could be added.

### How do I batch process multiple stories?

See `examples/batch_processing.py` for a complete example:

```python
stories = [story1, story2, story3]
for story in stories:
    # Process each story
    process_pipeline(story)
```

---

## Output Questions

### What format are the output videos?

**Currently**: MP3 audio + static image → MP4

**Future**: Full MP4 video with:
- Animated scenes
- Dynamic subtitles
- 1080x1920 resolution (9:16 vertical)
- 24-30 fps

### Where are output files stored?

```
Stories/
├── 0_Ideas/          # Story ideas (JSON)
├── 1_Scripts/        # Generated scripts
├── 2_Revised/        # Revised scripts
├── 3_VoiceOver/      # Audio files
└── 4_Titles/         # Final output with subtitles
```

### Can I customize output resolution?

Not yet. Future versions will support:
- 1080x1920 (9:16 vertical) - default
- 1080x1080 (1:1 square)
- 1920x1080 (16:9 horizontal)

### How do I add background music?

Not currently implemented. Planned in post-production stage. Will allow:
- Background music mixing
- Volume ducking (auto-lower music during voice)
- Music library integration

---

## Development Questions

### Can I contribute to the project?

Yes! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

We welcome:
- Bug fixes
- Feature implementations
- Documentation improvements
- Testing and QA

### What programming skills do I need to contribute?

- **Python** (intermediate to advanced)
- **Machine Learning** basics (for model integration)
- **FFmpeg** knowledge (for video processing)
- **API integration** experience

### What's the development roadmap?

See [PIPELINE.md](PIPELINE.md) for the complete roadmap.

**Priority order**:
1. Environment & model setup improvements
2. Shotlist generation
3. SDXL keyframe generation
4. Video synthesis
5. Post-production enhancements
6. Full pipeline integration

### Why Python? Will there be a C# version?

**Python** is used because:
- Best ML/AI library support
- Fast prototyping
- Strong community

**C# version**: Research phase. Options being considered:
- Python.NET wrapper
- REST API with C# client
- Native C# with ONNX models

See issue template in `docs/CHILD_ISSUES.md`.

---

## Troubleshooting Questions

### Why is my generation failing?

Common causes:
1. **API keys not configured** - Check `.env` file
2. **CUDA not available** - Check GPU setup
3. **Out of memory** - Close other applications
4. **Network issues** - Check internet connection

See [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for detailed solutions.

### Why are subtitles misaligned?

Possible causes:
1. **Script doesn't match audio** - Regenerate voiceover
2. **Audio quality issues** - Check normalization
3. **WhisperX model size too small** - Use "large-v2"

### How do I report a bug?

1. Check [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
2. Search [existing issues](https://github.com/Nomoos/StoryGenerator/issues)
3. Create new issue with:
   - System info
   - Error message
   - Steps to reproduce
   - Expected vs actual behavior

---

## Future Features Questions

### When will SDXL keyframe generation be ready?

Target: 2-3 weeks after initial setup is complete.

Depends on:
- Environment setup completion
- Shotlist generation implementation
- GPU optimization

### Will there be a web interface?

Not currently planned for initial releases. Possible future addition:
- Web UI for story creation
- Progress monitoring
- Output preview

### Will you support other video platforms?

The pipeline is optimized for:
- TikTok (9:16 vertical)
- YouTube Shorts (9:16 vertical)
- Instagram Reels (9:16 vertical)

Future support possible for:
- YouTube (16:9 horizontal)
- Facebook (1:1 square)

### Can I fine-tune the models?

Not officially supported, but possible:
- **SDXL**: Can use LoRA fine-tuning
- **LLMs**: Can use local fine-tuned models
- **Voice**: Can use custom ElevenLabs voices

Documentation for advanced customization may be added later.

---

## Legal and Privacy Questions

### Can I use the generated videos commercially?

Check the terms of service for each API:
- **OpenAI**: Generally allows commercial use
- **ElevenLabs**: Check your plan's terms
- **Generated content**: You own the output

**Disclaimer**: Verify current ToS of each service.

### Are API keys secure?

- Keys stored in `.env` (not committed to Git)
- Never share your `.env` file
- Rotate keys if exposed
- Use API key restrictions where available

### What data is collected?

**This software**:
- Does not collect telemetry
- Does not send data to third parties (except APIs)
- Stores all data locally

**External APIs**:
- OpenAI: Logs prompts (see their policy)
- ElevenLabs: Logs voice requests (see their policy)

---

## Getting Help

### Where can I find more documentation?

- **README.md** - Project overview
- **PIPELINE.md** - Complete pipeline breakdown
- **INSTALLATION.md** - Setup guide
- **QUICKSTART.md** - Get started fast
- **TROUBLESHOOTING.md** - Common issues
- **docs/CHILD_ISSUES.md** - Detailed component specs

### Where can I ask questions?

1. Check this FAQ
2. Check documentation in `docs/`
3. Search [GitHub Issues](https://github.com/Nomoos/StoryGenerator/issues)
4. Create new issue with your question

### Is there a community?

Not yet established. Consider:
- GitHub Discussions (if enabled)
- Discord server (future possibility)

---

*Have a question not answered here? [Create an issue](https://github.com/Nomoos/StoryGenerator/issues) and we'll add it!*

*Last Updated: 2025-10-06*
