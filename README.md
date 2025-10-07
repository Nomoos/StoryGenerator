
# StoryGenerator - AI Video Content Pipeline

An AI-driven video content pipeline that integrates ASR, LLM, vision, and generative models to create engaging short-form vertical videos for TikTok, YouTube Shorts, and Instagram Reels.

## 🎯 Project Overview

This project automates the creation of emotional, dramatic vertical stories targeting viewers aged 10-30 in the US, Canada, and Australia. The pipeline transforms story ideas into complete videos with voiceovers, subtitles, and visual content.

## 📚 Documentation

- **[README.md](README.md)** (this file) - Overview and quick start
- **[docs/MODELS.md](docs/MODELS.md)** - Comprehensive model documentation with Hugging Face references
- **[docs/EXAMPLES.md](docs/EXAMPLES.md)** - Input/output examples for all pipeline stages
- **[docs/PIPELINE.md](docs/PIPELINE.md)** - Detailed pipeline breakdown and technical specifications
- **[docs/CHILD_ISSUES.md](docs/CHILD_ISSUES.md)** - Issue tracking and task templates
- **[docs/INSTALLATION.md](docs/INSTALLATION.md)** - Detailed setup instructions
- **[docs/TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md)** - Common issues and solutions
- **[docs/TITLE_IMPROVEMENT.md](docs/TITLE_IMPROVEMENT.md)** - Title variant generation and improvement guide
- **[docs/TITLE_SCORING.md](docs/TITLE_SCORING.md)** - Title scoring system documentation

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

3. **✅ Script Improvement** (C# Implementation - `src/CSharp/Tools/`)
   - Iteratively improves scripts using GPT or local LLM (qwen2.5_14b)
   - Scores scripts on 8 rubric criteria (Hook, Plot, Dialogue, etc.)
   - Generates improved versions (v2, v3, v4) until quality plateaus
   - Saves to `data/gpt_improved/{segment}/{age}/{title_id}_v*.md`
   - **[Quick Start Guide](docs/SCRIPT_IMPROVEMENT_QUICKSTART.md)**

3.5. **✅ Title Improvement** (`scripts/title_improve.py`)
   - Generates 5 improved title variants using GPT or local LLM
   - Scores each variant using viral potential rubric
   - Automatically selects best-performing title
   - Saves to `data/titles/{segment}/{age}/{title_id}_improved.json`
   - Maintains centralized title registry with slugs and change tracking
   - **[Title Improvement Guide](docs/TITLE_IMPROVEMENT.md)**

4. **✅ Script Revision** (`Generators/GRevise.py`)
   - Polishes scripts for AI voice clarity
   - Removes awkward phrasing
   - Optimizes for ElevenLabs voice synthesis

5. **✅ Voice Generation** (`Generators/GVoice.py`)
   - ElevenLabs API integration (eleven_v3 model)
   - LUFS normalization for consistent audio levels
   - Silence trimming and padding

6. **✅ ASR & Subtitles** (`Generators/GTitles.py`)
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

### Quick Start Example

```python
from Models.StoryIdea import StoryIdea
from Generators.GScript import ScriptGenerator
from Generators.GRevise import RevisedScriptGenerator
from Generators.GVoice import VoiceMaker
from Generators.GTitles import TitleGenerator

# 1. Create a story idea
idea = StoryIdea(
    story_title="The Unexpected Friend",
    narrator_gender="female",
    tone="emotional, heartwarming",
    theme="friendship, acceptance"
)
idea.to_file()

# 2. Generate script
script_gen = ScriptGenerator(model="gpt-4o-mini")
script_gen.generate_from_storyidea(idea)

# 3. Revise script for voice clarity
revise_gen = RevisedScriptGenerator(model="gpt-4o-mini")
revise_gen.Revise(idea)

# 4. Generate voiceover
voice_maker = VoiceMaker()
voice_maker.generate_audio()

# 5. Generate word-level subtitles
title_gen = TitleGenerator(model_size="large-v2")
title_gen.generate_titles()
```

### Example Scripts

The `examples/` directory contains ready-to-run demonstration scripts:

- **[basic_pipeline.py](examples/basic_pipeline.py)** - Complete walkthrough of the current pipeline
- **[batch_processing.py](examples/batch_processing.py)** - Process multiple stories in batch
- **[custom_story_ideas.py](examples/custom_story_ideas.py)** - Create custom story variations

Run an example:
```bash
python examples/basic_pipeline.py
```

### Input/Output Examples

For detailed examples of inputs and outputs at each pipeline stage, including:
- Story idea JSON format
- Script generation examples
- Voice generation specifications
- Subtitle SRT format
- Planned: Shotlist JSON, keyframe images, final videos

📖 **See [docs/EXAMPLES.md](docs/EXAMPLES.md) for comprehensive input/output examples**

## 📁 Project Structure

The project follows a clean, organized structure:

```
StoryGenerator/
├── src/                    # Source code
│   ├── Python/            # Python implementation
│   │   ├── Generators/   # Core pipeline generators
│   │   │   ├── GStoryIdeas.py  # Story idea generation
│   │   │   ├── GScript.py      # Initial script generation
│   │   │   ├── GRevise.py      # Script revision
│   │   │   ├── GVoice.py       # Voice synthesis
│   │   │   └── GTitles.py      # Subtitle generation
│   │   ├── Models/       # Data models
│   │   │   └── StoryIdea.py    # Story metadata model
│   │   └── Tools/        # Utility functions
│   │       └── Utils.py  # Path management, file utilities
│   ├── CSharp/            # C# implementation
│   │   ├── Generators/   # Video effects, compositing
│   │   ├── Tools/        # Script improvement, FFmpeg
│   │   └── Models/       # C# data models
│   ├── Generator/         # Legacy generator code
│   └── research/          # Research prototypes and experiments
├── tests/                 # Test files
├── scripts/               # Utility scripts and automation
├── docs/                  # Documentation
├── examples/              # Example scripts and demos
├── data/                  # Generated content and data files
│   ├── Stories/          # Story outputs (0_Ideas, 1_Scripts, etc.)
│   ├── config/           # Configuration files
│   ├── prompts/          # LLM prompts
│   └── ...               # Other data directories
├── assets/                # Media assets
│   ├── audio/            # Audio files
│   ├── images/           # Image assets
│   ├── videos/           # Video files
│   └── scenes/           # Scene data
├── README.md              # This file
├── QUICKSTART.md          # Quick start guide
└── requirements.txt       # Python dependencies
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
  - [OpenAI Platform Docs](https://platform.openai.com/docs/models/gpt-4o-mini)
  - Cost: $0.150 / 1M input tokens, $0.600 / 1M output tokens

- **ElevenLabs eleven_v3**: Voice synthesis
  - [ElevenLabs API Docs](https://elevenlabs.io/docs/api-reference/text-to-speech)
  - High-quality, natural-sounding voices

- **WhisperX large-v2**: ASR and word-level alignment
  - [openai/whisper-large-v2](https://huggingface.co/openai/whisper-large-v2)
  - [WhisperX GitHub](https://github.com/m-bain/whisperX)

### Planned Integration

- **faster-whisper large-v3**: [Systran/faster-whisper-large-v3](https://huggingface.co/Systran/faster-whisper-large-v3)
  - 4x faster inference, lower memory footprint
  
- **Qwen2.5-14B-Instruct**: [Qwen/Qwen2.5-14B-Instruct](https://huggingface.co/Qwen/Qwen2.5-14B-Instruct)
  - Local LLM alternative for script generation
  
- **Llama-3.1-8B-Instruct**: [meta-llama/Llama-3.1-8B-Instruct](https://huggingface.co/meta-llama/Llama-3.1-8B-Instruct)
  - Lower VRAM alternative (16GB vs 28GB)
  
- **LLaVA-OneVision**: [Hugging Face Docs](https://huggingface.co/docs/transformers/en/model_doc/llava_onevision)
  - Vision-language model for scene validation
  
- **Phi-3.5-vision**: [microsoft/Phi-3.5-vision-instruct](https://huggingface.co/microsoft/Phi-3.5-vision-instruct)
  - Lightweight vision model (4B params, 8GB VRAM)
  
- **Stable Diffusion XL (SDXL)**: [Hugging Face Diffusers Docs](https://huggingface.co/docs/diffusers/en/using-diffusers/sdxl)
  - High-quality keyframe generation (1024x1024)
  
- **LTX-Video**: [Lightricks/LTX-Video](https://huggingface.co/Lightricks/LTX-Video)
  - Video generation from keyframes
  
- **Stable Video Diffusion**: [Stability AI](https://stability.ai/stable-video)
  - Image-to-video conversion with smooth motion

📖 **For detailed model documentation, specifications, and usage examples, see [docs/MODELS.md](docs/MODELS.md)**

## 🎯 Target Audience

- **Age**: 10-30 years old
- **Regions**: US, Canada, Australia
- **Platforms**: TikTok, YouTube Shorts, Instagram Reels
- **Content**: Emotional drama, awkward moments, rebellion, identity, connection

## 📋 Issue Tracking

This project uses a structured issue tracking system to manage the implementation of all pipeline components.

### Documentation

- **[ISSUE_TRACKING.md](ISSUE_TRACKING.md)** - Issue tracking system overview and workflow
- **[docs/CHILD_ISSUES.md](docs/CHILD_ISSUES.md)** - Complete issue templates for all 10 pipeline stages
- **[PIPELINE.md](PIPELINE.md)** - Technical breakdown with implementation status
- **[.github/ISSUE_TEMPLATE/](.github/ISSUE_TEMPLATE/)** - GitHub issue templates (use when creating issues)

### 10 Major Pipeline Stages

1. ✅ **Environment & Model Setup** - Configuration and model management
2. ✅ **ASR Enhancement** - Speech recognition with WhisperX (upgrade to faster-whisper planned)
3. 🔄 **Shotlist Generation** - LLM-based scene planning (planned)
4. 🔄 **Vision Guidance** - Optional scene validation with vision models (planned)
5. 🔄 **SDXL Keyframe Generation** - High-quality image generation (planned)
6. 🔄 **Video Synthesis** - LTX-Video or SVD integration (planned)
7. 🔄 **Post-Production** - Subtitle overlay and final rendering (planned)
8. 🔄 **Pipeline Integration** - One-click end-to-end automation (planned)
9. 🔄 **C# Implementation** - Research and migration (planned)
10. 🔄 **Documentation** - Comprehensive guides and examples (in progress)

### Current Implementation Status

**✅ Completed (Stages 1-5 of current pipeline)**:
- Story idea generation with viral potential scoring
- GPT-4o-mini script generation (~360 words, emotional hooks)
- Script revision optimized for AI voice synthesis
- ElevenLabs voice generation with LUFS normalization
- WhisperX word-level subtitle generation and alignment

**🔄 In Progress**:
- Documentation enhancement
- Model references and citations
- Input/output examples

**📋 Planned**:
- Shotlist generation using local LLMs
- SDXL keyframe generation
- Video synthesis with LTX-Video/SVD
- Complete automation pipeline

### Creating Issues

**To create a new child issue**:
1. Go to the [Issues tab](https://github.com/Nomoos/StoryGenerator/issues)
2. Click "New Issue"
3. Select the appropriate stage template (Stage 1-10)
4. Fill in any additional context
5. Submit the issue

Each template includes:
- Clear description and scope
- Requirements (Must/Should/Nice to have)
- Detailed subtasks
- Success criteria
- Dependencies and references

For detailed information on the issue tracking workflow, see [ISSUE_TRACKING.md](ISSUE_TRACKING.md).

## 🔐 Security Notes

⚠️ **Important**: API keys are currently hardcoded in generator files. For production:
- Use environment variables
- Implement proper secrets management
- Rotate keys regularly

---

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

## 🤝 Contributing

[Add contribution guidelines here]

## 📧 Contact

[Add contact information here]

---

## 🙏 Acknowledgments

- OpenAI for GPT models
- ElevenLabs for voice generation
- Community contributors

---

**Note**: This repository was recently reorganized to support both C# and Python implementations. The C# version is under development and will become the primary implementation.

**Remember**: Always keep your API keys secure and never commit them to version control!
