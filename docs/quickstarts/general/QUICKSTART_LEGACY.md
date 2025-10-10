# Quick Start Guide

Get started with StoryGenerator in 5 minutes!

## Prerequisites

- Python 3.8+
- OpenAI API key
- ElevenLabs API key
- FFmpeg installed

## Installation

```bash
# 1. Clone the repository
git clone https://github.com/Nomoos/StoryGenerator.git
cd StoryGenerator

# 2. Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure API keys
cp .env.example .env
# Edit .env and add your API keys
```

## Your First Video

### Option 1: Using the Example Script

```bash
# Run the basic pipeline example
python examples/basic_pipeline.py
```

This will:
1. ✅ Create a story idea
2. ✅ Generate a script (~360 words)
3. ✅ Revise the script for voice clarity
4. ✅ Generate voiceover with ElevenLabs
5. ✅ Create word-level subtitles with WhisperX

**Output**: Check `Stories/4_Titles/The_Unexpected_Friend/`

### Option 2: Step-by-Step (Interactive)

#### Step 1: Create a Story Idea

```python
from Models.StoryIdea import StoryIdea

story = StoryIdea(
    story_title="My First Story",
    narrator_gender="female",
    tone="emotional",
    theme="friendship"
)
story.to_file()
```

#### Step 2: Generate Script

```python
from Generators.GScript import ScriptGenerator

script_gen = ScriptGenerator()
script_gen.generate_from_storyidea(story)
```

#### Step 3: Revise Script

```python
from Generators.GRevise import RevisedScriptGenerator

reviser = RevisedScriptGenerator()
reviser.Revise(story)
```

#### Step 4: Generate Voice

```python
from Generators.GVoice import VoiceMaker

voice = VoiceMaker()
voice.generate_audio()
```

#### Step 5: Generate Subtitles

```python
from Generators.GTitles import TitleGenerator

titles = TitleGenerator()
titles.generate_titles()
```

## Understanding the Output

After running the pipeline, you'll find:

```
Stories/
└── 4_Titles/
    └── My_First_Story/
        ├── idea.json                      # Story metadata
        ├── Revised.txt                    # Final script
        ├── voiceover_normalized.mp3       # Audio file
        └── Subtitles_Word_By_Word.txt     # SRT subtitles
```

## What Each File Contains

### `idea.json`
Story metadata including title, theme, tone, and potential scores.

### `Revised.txt`
The polished script optimized for AI voice synthesis.

### `voiceover_normalized.mp3`
Audio narration with normalized volume levels (LUFS -14.0).

### `Subtitles_Word_By_Word.txt`
SRT subtitle file with word-level timestamps for each word.

## Customizing Your Story

Edit the story parameters to create different styles:

```python
story = StoryIdea(
    story_title="Dark Mystery",
    narrator_gender="male",
    tone="suspenseful, dark",
    theme="mystery, betrayal",
    narrator_type="first-person",
    emotional_core="fear, distrust, revelation",
    twist_type="unexpected betrayal",
    voice_style="tense, cautious, dramatic",
    locations="abandoned warehouse, dark alley"
)
```

## Common Issues

### "API key not found"
- Make sure `.env` file exists in project root
- Check that API keys are correctly formatted (no quotes)

### "CUDA not available"
- Install PyTorch with CUDA: `pip install torch --index-url https://download.pytorch.org/whl/cu118`
- Verify GPU: `nvidia-smi`

### "FFmpeg not found"
- Ubuntu: `sudo apt install ffmpeg`
- macOS: `brew install ffmpeg`
- Windows: Download from ffmpeg.org

## Next Steps

Now that you've created your first video:

1. **Explore Examples**: Check `examples/` directory for more scripts
2. **Read Full Guide**: See [USAGE.md](docs/USAGE.md) for detailed usage
3. **Customize**: See [CONFIGURATION.md](docs/CONFIGURATION.md) for options
4. **Contribute**: See [CONTRIBUTING.md](docs/CONTRIBUTING.md) to help improve

## Current Limitations

The pipeline currently generates:
- ✅ Scripts
- ✅ Voiceovers
- ✅ Subtitles
- ⚠️ Static images with audio (basic video)

**Coming Soon**:
- 🔄 SDXL keyframe generation
- 🔄 Video synthesis with LTX-Video/SVD
- 🔄 Dynamic subtitle overlay
- 🔄 Shotlist generation
- 🔄 Vision guidance

See [PIPELINE.md](PIPELINE.md) for the complete roadmap.

## Getting Help

- **Documentation**: Check `docs/` directory
- **Troubleshooting**: See [TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md)
- **Issues**: [GitHub Issues](https://github.com/Nomoos/StoryGenerator/issues)
- **Examples**: See `examples/` directory

## Video Tutorial

Coming soon!

---

**Total Time to First Video**: ~5-10 minutes (depending on API response time)

Happy storytelling! 🎬✨
