<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
=======
>>>>>>> master
=======
# StoryGenerator - Complete Pipeline Documentation

A complete pipeline for generating viral social media stories with automated text generation, voice-over, and video production.

## Overview

StoryGenerator automates the creation of short-form vertical videos optimized for TikTok, YouTube Shorts, and Instagram Reels. The pipeline handles everything from idea generation to final video output with thumbnails and metadata.

## Pipeline Architecture

```
1. Ideas Generation (0_Ideas/)
   ↓
2. Script Generation (1_Scripts/)
   ↓
3. Script Revision (2_Revised/)
   ↓
4. Voice Generation (3_VoiceOver/)
   ↓
5. Title Generation (4_Titles/)
   ↓
6. Video Generation (5_Videos/) ← NEW!
   ↓
7. Publishing (Future)
```

## New Features: Video Pipeline Integration (Step 4)

The video pipeline has been fully integrated with the following capabilities:

### ✅ Modular Components

1. **VideoRenderer** - Core video generation
   - Renders videos from audio and images
   - Automatic fallback to solid backgrounds
   - Metadata embedding
   - Thumbnail generation (1080x1920)

2. **SceneComposer** - Scene management
   - Multi-scene composition
   - Scene transitions
   - Automatic text-to-scene splitting

3. **VideoPipeline** - Batch processing
   - Process all stories at once
   - Parallel/sequential processing options
   - Error handling and recovery
   - Comprehensive statistics

### ✅ Error Handling & Fallbacks

- **Image Generation Failure**: Automatically creates solid color background with title text
- **TTS Failure**: Skips story and continues with batch processing
- **Missing Files**: Comprehensive validation before processing
- **Failed Videos**: Cleanup utilities to remove incomplete files

### ✅ Metadata & Thumbnails

- Embeds title, description, artist, and album metadata
- Generates 1080x1920 thumbnails (customizable)
- Saves metadata.json for reference
- Copies script to video folder

### ✅ Batch Processing

- Sequential or parallel processing
- Configurable worker threads
- Skip existing videos automatically
- Force regeneration option

## Installation

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Install FFmpeg

FFmpeg is required for video processing:

**Ubuntu/Debian:**
```bash
sudo apt-get install ffmpeg
```

**MacOS:**
```bash
brew install ffmpeg
```

**Windows:**
Download from [https://ffmpeg.org/download.html](https://ffmpeg.org/download.html)

### 3. Configure Paths

Update `Tools/Utils.py` with your story root path:

```python
STORY_ROOT = "C:\\Users\\YourName\\PROJECTS\\VideoMaking\\StoryGenerator\\Stories"
```

## Usage

### Complete Workflow

#### 1. Generate Ideas
```python
from Generators.GStoryIdeas import StoryIdeaGenerator

generator = StoryIdeaGenerator()
# Generate and save ideas
```

#### 2. Generate Scripts
```python
from Generators.GScript import ScriptGenerator
from Models.StoryIdea import StoryIdea

generator = ScriptGenerator()
idea = StoryIdea.from_file("path/to/idea.json")
generator.generate_from_storyidea(idea)
```

#### 3. Revise Scripts
```python
from Generators.GRevise import RevisedScriptGenerator

generator = RevisedScriptGenerator()
generator.Revise(idea)
```

#### 4. Enhance Scripts (Add Voice Tags)
```python
from Generators.GEnhanceScript import EnhanceScriptGenerator

generator = EnhanceScriptGenerator()
generator.Enhance(folder_name)
```

#### 5. Generate Voice-Overs
```python
from Generators.GVoice import VoiceMaker

maker = VoiceMaker()
maker.generate_audio()
maker.normalize_audio()
```

Or use the manual script:
```bash
python Generation/Manual/MVoice.py
```

#### 6. Generate Videos (NEW!)

**Recommended Method - Full Pipeline:**
```bash
python Generation/Manual/MVideoPipeline.py
```

**Programmatic Usage:**
```python
from Video.VideoPipeline import VideoPipeline

pipeline = VideoPipeline(
    max_workers=2,
    default_resolution=(1080, 1920)
)

# Process all stories
stats = pipeline.batch_process(
    parallel=False,
    force_regenerate=False
)

print(f"Success: {stats['successful']}/{stats['processed']}")
```

**Process Single Story:**
```python
pipeline = VideoPipeline()
success = pipeline.process_story(
    story_folder="My_Story_Name",
    generate_thumbnail=True
)
```

### Manual Processing Scripts

All manual scripts are in `Generation/Manual/`:

- `MIdea.py` - Generate ideas
- `MScript.py` - Generate scripts
- `MRevise.py` - Revise scripts
- `MEnhanceScript.py` - Add voice tags
- `MVoice.py` - Generate voice-overs
- `MVideoPipeline.py` - Generate videos (NEW!)
- `MConvertMP3ToMP4.py` - Legacy converter (now uses VideoRenderer)

## Project Structure

```
StoryGenerator/
├── Models/
│   └── StoryIdea.py              # Story data model
├── Generators/
│   ├── GStoryIdeas.py            # Idea generation
│   ├── GScript.py                # Script generation
│   ├── GRevise.py                # Script revision
│   ├── GEnhanceScript.py         # Voice tag enhancement
│   └── GVoice.py                 # Voice generation
├── Video/                         # NEW: Video pipeline
│   ├── VideoRenderer.py          # Core video rendering
│   ├── SceneComposer.py          # Scene management
│   ├── VideoPipeline.py          # Batch processing
│   └── README.md                 # Detailed video docs
├── Generation/Manual/
│   ├── MVideoPipeline.py         # NEW: Video pipeline script
│   └── ...                       # Other manual scripts
├── Tools/
│   └── Utils.py                  # Utilities and paths
└── Stories/                      # Output directory
    ├── 0_Ideas/
    ├── 1_Scripts/
    ├── 2_Revised/
    ├── 3_VoiceOver/
    ├── 4_Titles/
    └── 5_Videos/                 # NEW: Final videos
```

## Video Pipeline Features

### Resolution Options

Default is 1080x1920 (vertical), but you can customize:

```python
# Square (Instagram)
pipeline = VideoPipeline(default_resolution=(1080, 1080))

# Horizontal (YouTube)
pipeline = VideoPipeline(default_resolution=(1920, 1080))
```

### Parallel Processing

Speed up batch processing with parallel execution:

```python
stats = pipeline.batch_process(
    parallel=True,  # Enable parallel processing
    force_regenerate=False
)
```

**Note**: Parallel processing uses more CPU/memory but is significantly faster for large batches.

### Custom Video Settings

```python
from Video.VideoRenderer import VideoRenderer

renderer = VideoRenderer(
    default_resolution=(1080, 1920),
    default_fps=30,
    default_bitrate="256k"  # Higher quality audio
)
```

### Fallback Behavior

If the background image is missing:
1. Automatically generates a solid color (dark blue-gray) background
2. Adds story title as text overlay (centered, white)
3. Continues video generation without interruption
4. Logs warning about using fallback

### Metadata

Each video includes embedded metadata:
- Title (from StoryIdea)
- Description (generated from story attributes)
- Artist ("Nom")
- Album ("Noms Stories")

Metadata is also saved to `metadata.json` in the video folder for reference.

### Thumbnail Generation

Automatically generates thumbnails:
- Resolution: 1080x1920 (matches video)
- Extracted from video at 0.5 seconds
- Saved as `thumbnail.jpg` in video folder
- Can be customized or regenerated

## Configuration

### API Keys

API keys are required for:
- OpenAI (text generation): `Generators/GScript.py`
- ElevenLabs (voice generation): `Generators/GVoice.py`

**Note**: API keys should be stored securely (e.g., environment variables) in production.

### Story Root Path

Update `STORY_ROOT` in `Tools/Utils.py` to match your local setup:

```python
STORY_ROOT = "C:\\Users\\YourName\\PROJECTS\\VideoMaking\\StoryGenerator\\Stories"
```

### Video Settings

Default settings in `Video/VideoRenderer.py`:
- Resolution: 1080x1920 (vertical)
- FPS: 30
- Video Codec: H.264
- Audio Codec: AAC
- Audio Bitrate: 192k

## Future Enhancements

### Publishing Stage (Not Yet Implemented)

The next step is automated publishing:

1. **Platform APIs**:
   - YouTube Shorts upload
   - TikTok upload (via unofficial APIs)
   - Instagram Reels (via scheduling partners)

2. **Scheduling**:
   - Queue videos for optimal posting times
   - A/B testing with different thumbnails
   - Analytics integration

3. **Automation Considerations**:
   - Many platforms restrict automation
   - May require manual posting or scheduling partners
   - Check platform ToS before automating

### Other Future Features

- Multi-scene video composition with transitions
- Dynamic image generation from text prompts
- Subtitle/caption overlay
- Background music integration
- Video quality presets (draft/final)
- Progress webhooks/notifications

## Troubleshooting

### FFmpeg Not Found
Make sure FFmpeg is installed and in your PATH:
```bash
ffmpeg -version
```

### Empty Videos
Check:
1. Audio file exists and is not empty
2. Audio file has valid duration (use `ffprobe`)
3. Background image path is correct

### Memory Issues
If parallel processing causes memory issues:
```python
# Reduce workers
pipeline = VideoPipeline(max_workers=1)

# Or disable parallel processing
stats = pipeline.batch_process(parallel=False)
```

### Missing Dependencies
Install all required packages:
```bash
pip install -r requirements.txt
```

Check for missing system dependencies:
- FFmpeg
- DejaVu fonts (for fallback text rendering)

## Contributing

When adding new features:
1. Follow existing code structure
2. Add error handling and fallbacks
3. Update documentation
4. Test with edge cases

## License

[Your License Here]

## Credits

- Video pipeline by Copilot AI Assistant
- Story generation using OpenAI GPT models
- Voice generation using ElevenLabs
- Video processing with FFmpeg

---

For detailed video pipeline documentation, see [Video/README.md](Video/README.md)
=======
>>>>>>> origin/master
# StoryGenerator - AI Video Content Pipeline

An AI-driven video content pipeline that integrates ASR, LLM, vision, and generative models to create engaging short-form vertical videos for TikTok, YouTube Shorts, and Instagram Reels.

## 🎯 Project Overview

This project automates the creation of emotional, dramatic vertical stories targeting viewers aged 10-30 in the US, Canada, and Australia. The pipeline transforms story ideas into complete videos with voiceovers, subtitles, and visual content.

## 🏗️ Pipeline Architecture

The complete pipeline consists of 10 major stages:

### Currently Implemented

1. **✅ Story Idea Generation** (`Generators/GStoryIdeas.py`)
   - Generates story concepts with metadata
   - Tracks potential across platforms, regions, age groups, and gender
   
2. **✅ Script Generation** (`Generators/GScript.py`)
   - Uses GPT-4o-mini to generate ~360-word scripts
   - Optimized for spoken content with emotional hooks
   - Natural, conversational language

3. **✅ Script Revision** (`Generators/GRevise.py`)
   - Polishes scripts for AI voice clarity
   - Removes awkward phrasing
   - Optimizes for ElevenLabs voice synthesis

4. **✅ Voice Generation** (`Generators/GVoice.py`)
   - ElevenLabs API integration (eleven_v3 model)
   - LUFS normalization for consistent audio levels
   - Silence trimming and padding

5. **✅ ASR & Subtitles** (`Generators/GTitles.py`)
   - WhisperX for word-level alignment
   - Generates word-by-word SRT files
   - Aligns script to actual audio timing

### Planned Implementation

6. **🔄 Vision Guidance** (Planned)
   - LLaVA-OneVision or Phi-3.5-vision integration
   - Scene understanding and composition guidance
   - Visual consistency validation

7. **🔄 Keyframe Generation** (Planned)
   - SDXL for high-quality image generation
   - Scene-specific prompts from script analysis
   - Visual storytelling alignment

8. **🔄 Video Synthesis** (Planned)
   - LTX-Video or Stable Video Diffusion
   - Smooth transitions between keyframes
   - Synchronized with audio

9. **🔄 Post-Production** (Planned)
   - Subtitle overlay with dynamic styling
   - Audio-visual synchronization
   - Final rendering and format optimization

10. **🔄 One-Click Integration** (Planned)
    - Automated end-to-end pipeline
    - Error handling and recovery
    - Progress tracking and logging

## 📦 Installation

### Prerequisites

- Python 3.8+
- CUDA-capable GPU (recommended for ASR and image generation)
- FFmpeg

### Setup

```bash
# Clone the repository
git clone https://github.com/Nomoos/StoryGenerator.git
cd StoryGenerator

# Install dependencies
pip install -r requirements.txt

# Set up API keys in respective generator files
# - OpenAI API key in Generators/GScript.py and Generators/GRevise.py
# - ElevenLabs API key in Generators/GVoice.py
```

### Additional Dependencies for Full Pipeline

For the complete pipeline implementation, additional packages will be needed:

```bash
# For vision models
pip install transformers accelerate

# For SDXL
pip install diffusers torch torchvision

# For video synthesis
pip install imageio imageio-ffmpeg

# For WhisperX (if not already installed)
pip install whisperx
```

## 🚀 Usage

### Current Workflow

```python
from Models.StoryIdea import StoryIdea
from Generators.GScript import ScriptGenerator
from Generators.GRevise import RevisedScriptGenerator
from Generators.GVoice import VoiceMaker
from Generators.GTitles import TitleGenerator

# 1. Create or load a story idea
idea = StoryIdea(
    story_title="My Amazing Story",
    narrator_gender="female",
    tone="emotional",
    theme="friendship"
)
idea.to_file()

# 2. Generate script
script_gen = ScriptGenerator()
script_gen.generate_from_storyidea(idea)

# 3. Revise script
revise_gen = RevisedScriptGenerator()
revise_gen.Revise(idea)

# 4. Generate voiceover
voice_maker = VoiceMaker()
voice_maker.generate_audio()

# 5. Generate subtitles
title_gen = TitleGenerator()
title_gen.generate_titles()
```

## 📁 Project Structure

```
StoryGenerator/
├── Generators/          # Core pipeline generators
│   ├── GStoryIdeas.py  # Story idea generation
│   ├── GScript.py      # Initial script generation
│   ├── GRevise.py      # Script revision
│   ├── GVoice.py       # Voice synthesis
│   ├── GTitles.py      # Subtitle generation
│   └── GEnhanceScript.py
├── Models/              # Data models
│   └── StoryIdea.py    # Story metadata model
├── Tools/               # Utility functions
│   └── Utils.py        # Path management, file utilities
├── Generation/          # Manual generation scripts
│   └── Manual/         # Individual component tests
└── Stories/            # Output directory (gitignored)
    ├── 0_Ideas/        # Story ideas JSON
    ├── 1_Scripts/      # Generated scripts
    ├── 2_Revised/      # Revised scripts
    ├── 3_VoiceOver/    # Generated audio
    └── 4_Titles/       # Subtitles and final assets
```

## 🔗 Model References

### Currently Used
- **OpenAI GPT-4o-mini**: Script generation and revision
- **ElevenLabs eleven_v3**: Voice synthesis
- **WhisperX large-v2**: ASR and alignment

### Planned Integration
- **faster-whisper large-v3**: [Systran/faster-whisper-large-v3](https://huggingface.co/Systran/faster-whisper-large-v3)
- **Qwen2.5-14B-Instruct**: [unsloth/Qwen2.5-14B-Instruct](https://huggingface.co/unsloth/Qwen2.5-14B-Instruct)
- **Llama-3.1-8B-Instruct**: [meta-llama/Llama-3.1-8B-Instruct](https://huggingface.co/meta-llama/Llama-3.1-8B-Instruct)
- **LLaVA-OneVision**: [docs](https://huggingface.co/docs/transformers/en/model_doc/llava_onevision)
- **Phi-3.5-vision**: [microsoft/Phi-3.5-vision-instruct](https://huggingface.co/microsoft/Phi-3.5-vision-instruct)
- **SDXL**: [docs](https://huggingface.co/docs/diffusers/en/using-diffusers/sdxl)
- **LTX-Video**: [Lightricks/LTX-Video](https://huggingface.co/Lightricks/LTX-Video)
- **Stable Video Diffusion**: [stability.ai](https://stability.ai/stable-video)

## 🎯 Target Audience

- **Age**: 10-30 years old
- **Regions**: US, Canada, Australia
- **Platforms**: TikTok, YouTube Shorts, Instagram Reels
- **Content**: Emotional drama, awkward moments, rebellion, identity, connection

## 📋 Issue Tracking

For detailed component implementation plans, see:
- [PIPELINE.md](PIPELINE.md) - Complete pipeline breakdown
- [docs/CHILD_ISSUES.md](docs/CHILD_ISSUES.md) - Individual component issues

## 🔐 Security Notes

⚠️ **Important**: API keys are currently hardcoded in generator files. For production:
- Use environment variables
- Implement proper secrets management
- Rotate keys regularly
<<<<<<< HEAD
=======
=======
>>>>>>> master
# StoryGenerator

AI-powered story generation pipeline for creating engaging short-form video content for TikTok, YouTube Shorts, and Instagram Reels.

## 🏗️ Repository Structure

This repository contains **two implementations** of the StoryGenerator:

### 📌 **C# Implementation** (Primary/Preferred)
Located in `CSharp/` - Modern, type-safe implementation with better performance and cross-platform support.

### 📌 **Python Implementation** (Legacy/Alternative)
Located in `Python/` - Original implementation, fully functional and maintained.

---

## 🚀 Quick Start

### C# Version (Recommended)
```bash
cd CSharp
# Setup instructions coming soon
```

### Python Version
```bash
cd Python
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
cp ../.env.example .env
# Edit .env with your API keys
```

For detailed setup instructions, see:
- **C#**: [CSharp/README.md](CSharp/README.md) *(coming soon)*
- **Python**: [Python/README.md](Python/README.md)

---

## ⚠️ IMPORTANT: Security Notice

**CRITICAL**: This repository previously had API keys hardcoded in source files. Before using:

1. **All exposed API keys should be considered compromised**
2. Generate new API keys:
   - [OpenAI API Keys](https://platform.openai.com/api-keys)
   - [ElevenLabs API Keys](https://elevenlabs.io/app/settings/api-keys)
3. Set up `.env` file from `.env.example`
4. **Never commit API keys to version control**

See [SECURITY_CHECKLIST.md](SECURITY_CHECKLIST.md) for detailed security procedures.

---

## 📚 Documentation

### Getting Started
- [QUICKSTART.md](QUICKSTART.md) - 15-minute setup guide (Python)
- [INDEX.md](INDEX.md) - Documentation navigation hub

### Technical Documentation
- [ARCHITECTURE.md](ARCHITECTURE.md) - System architecture and design
- [RESEARCH_AND_IMPROVEMENTS.md](RESEARCH_AND_IMPROVEMENTS.md) - Analysis and roadmap

### Security
- [SECURITY_CHECKLIST.md](SECURITY_CHECKLIST.md) - Security procedures and checklist

### Reference
- [SUMMARY.md](SUMMARY.md) - Implementation summary

---

## 🎯 Features

- 🎯 **AI-Powered Story Generation**: Generate viral story ideas using GPT-4
- ✍️ **Script Writing**: Create emotionally engaging scripts optimized for short-form video
- 🎙️ **Voice Enhancement**: Add performance tags for realistic AI voices
- 🔊 **Voice Generation**: Generate high-quality voiceovers using ElevenLabs
- 📊 **Viral Potential Scoring**: Estimate engagement potential across platforms

---

## 📁 Directory Structure

```
StoryGenerator/
│
├── 📁 CSharp/                  # C# Implementation (Primary)
│   ├── Generators/             # Coming soon
│   ├── Models/                 # Coming soon
│   └── README.md               # C# setup guide (coming soon)
│
├── 📁 Python/                  # Python Implementation
│   ├── Generators/             # Core generation modules
│   │   ├── GStoryIdeas.py     # Story idea generation
│   │   ├── GScript.py         # Script generation
│   │   ├── GRevise.py         # Script revision
│   │   ├── GEnhanceScript.py  # Voice tag enhancement
│   │   ├── GVoice.py          # Voice generation
│   │   └── GTitles.py         # Title generation
│   ├── Models/                 # Data models
│   │   └── StoryIdea.py       # Story idea model
│   ├── Tools/                  # Utilities
│   │   └── Utils.py           # Helper functions
│   ├── Generation/             # Manual execution scripts
│   │   └── Manual/            # Entry points
│   ├── requirements.txt        # Python dependencies
│   ├── requirements-dev.txt    # Dev dependencies
│   ├── pyproject.toml         # Python project config
│   └── README.md              # Python-specific documentation
│
├── 📁 Stories/                 # Generated content (gitignored)
│   ├── 0_Ideas/               # Story ideas
│   ├── 1_Scripts/             # Initial scripts
│   ├── 2_Revised/             # Revised scripts
│   └── 3_VoiceOver/           # Audio files
│
├── 📄 Documentation
│   ├── README.md              # This file
│   ├── QUICKSTART.md          # Quick setup guide
│   ├── ARCHITECTURE.md        # Technical architecture
│   ├── RESEARCH_AND_IMPROVEMENTS.md
│   ├── SECURITY_CHECKLIST.md
│   ├── SUMMARY.md
│   └── INDEX.md               # Documentation index
│
└── 📄 Configuration
    ├── .env.example           # Environment template
    └── .gitignore             # Git exclusions
```

---

## 🔧 Which Version Should I Use?

| Feature | C# | Python |
|---------|-----|--------|
| **Status** | 🚧 In Development | ✅ Ready |
| **Performance** | ⚡ Faster | 🐌 Slower |
| **Type Safety** | ✅ Strong typing | ⚠️ Dynamic |
| **Async Support** | ✅ Native | ⚠️ Added complexity |
| **Deployment** | 📦 Single binary | 🐍 Requires interpreter |
| **IDE Support** | ✅ Excellent | ✅ Good |
| **Learning Curve** | 📈 Moderate | 📈 Easy |

**Recommendation**: 
- **For Production**: Wait for C# implementation
- **For Development/Testing**: Use Python implementation now

---

## 💻 Development

### Contributing

Contributions are welcome for both implementations!

**For C# development**:
- Coming soon

**For Python development**:
```bash
cd Python
pip install -r requirements-dev.txt
black .                    # Format code
pylint Generators/         # Lint code
pytest                     # Run tests (when available)
```

---

## 🔄 Migration from Python to C#

Migration guidance will be provided when the C# implementation is complete.

---

## 📈 Roadmap

### C# Implementation
- [ ] Port core generators to C#
- [ ] Implement async/await patterns
- [ ] Add comprehensive unit tests
- [ ] Create CLI interface
- [ ] Build NuGet packages
- [ ] Add web API

### Python Implementation
- [x] Existing functionality
- [ ] Add unit tests
- [ ] Improve error handling
- [ ] Add logging system
- [ ] Create CLI interface

For detailed roadmap, see [RESEARCH_AND_IMPROVEMENTS.md](RESEARCH_AND_IMPROVEMENTS.md).

---

## 📞 Support

- **Documentation**: Check [INDEX.md](INDEX.md) for all documentation
- **Issues**: Open a GitHub issue
- **Security**: See [SECURITY_CHECKLIST.md](SECURITY_CHECKLIST.md)

---
<<<<<<< HEAD
>>>>>>> master
=======
>>>>>>> master

## 📄 License

[Add your license here]

<<<<<<< HEAD
<<<<<<< HEAD
=======
>>>>>>> master
## 🤝 Contributing

[Add contribution guidelines here]

## 📧 Contact

[Add contact information here]
<<<<<<< HEAD
=======
=======
>>>>>>> master
---

## 🙏 Acknowledgments

- OpenAI for GPT models
- ElevenLabs for voice generation
- Community contributors

---

**Note**: This repository was recently reorganized to support both C# and Python implementations. The C# version is under development and will become the primary implementation.

**Remember**: Always keep your API keys secure and never commit them to version control!
<<<<<<< HEAD
<<<<<<< HEAD
>>>>>>> master
=======
=======
>>>>>>> origin/master
>>>>>>> master
