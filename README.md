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

## 📄 License

[Add your license here]

---

## 🙏 Acknowledgments

- OpenAI for GPT models
- ElevenLabs for voice generation
- Community contributors

---

**Note**: This repository was recently reorganized to support both C# and Python implementations. The C# version is under development and will become the primary implementation.

**Remember**: Always keep your API keys secure and never commit them to version control!
