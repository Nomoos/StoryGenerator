# StoryGenerator

AI-powered story generation pipeline for creating engaging short-form video content for TikTok, YouTube Shorts, and Instagram Reels.

## ⚠️ IMPORTANT: Security Notice

**CRITICAL**: Before using this project, you must set up proper API key management.

### Current Issues

This repository previously had API keys hardcoded in source files (now removed). If you cloned this repository before the security fix:

1. **All exposed API keys should be considered compromised**
2. Revoke any API keys that may have been exposed
3. Generate new API keys from your providers:
   - [OpenAI API Keys](https://platform.openai.com/api-keys)
   - [ElevenLabs API Keys](https://elevenlabs.io/app/settings/api-keys)

## Features

- 🎯 **AI-Powered Story Generation**: Generate viral story ideas using GPT-4
- ✍️ **Script Writing**: Create emotionally engaging scripts optimized for short-form video
- 🎙️ **Voice Enhancement**: Add performance tags for realistic AI voices
- 🔊 **Voice Generation**: Generate high-quality voiceovers using ElevenLabs
- 📊 **Viral Potential Scoring**: Estimate engagement potential across platforms and demographics

## Installation

### Prerequisites

- Python 3.12 or higher
- OpenAI API key
- ElevenLabs API key (for voice generation)

### Setup

1. **Clone the repository**
```bash
git clone https://github.com/Nomoos/StoryGenerator.git
cd StoryGenerator
```

2. **Create and activate virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables**
```bash
cp .env.example .env
```

5. **Edit `.env` file with your API keys**
```bash
OPENAI_API_KEY=your_actual_openai_key_here
ELEVENLABS_API_KEY=your_actual_elevenlabs_key_here
```

⚠️ **NEVER commit your `.env` file to version control!**

## Project Structure

```
StoryGenerator/
├── Generators/          # Core generation modules
│   ├── GStoryIdeas.py  # Story idea generation
│   ├── GScript.py      # Script generation
│   ├── GRevise.py      # Script revision
│   ├── GEnhanceScript.py # Add voice tags
│   └── GVoice.py       # Voice generation
├── Models/              # Data models
│   └── StoryIdea.py    # Story idea model
├── Tools/               # Utilities
│   └── Utils.py        # Helper functions
├── Generation/          # Manual generation scripts
│   └── Manual/         # Entry points for manual workflows
└── Stories/            # Generated content (gitignored)
    ├── 0_Ideas/        # Generated story ideas
    ├── 1_Scripts/      # Initial scripts
    ├── 2_Revised/      # Revised scripts
    └── 3_VoiceOver/    # Generated audio
```

## Usage

### Generate Story Ideas

```python
from Generators.GStoryIdeas import StoryIdeasGenerator

generator = StoryIdeasGenerator()
ideas = generator.generate_ideas(
    topic="falling for someone who gives mixed signals",
    count=5,
    tone="awkward, romantic, relatable",
    theme="first love, quiet sadness, learning to let go"
)

for idea in ideas:
    print(f"Title: {idea.story_title}")
    print(f"Potential: {idea.potencial['overall']}")
```

### Generate Script from Idea

```python
from Generators.GScript import ScriptGenerator
from Models.StoryIdea import StoryIdea

# Load an idea
idea = StoryIdea.from_file("Stories/0_Ideas/your_story_idea.json")

# Generate script
generator = ScriptGenerator()
generator.generate_from_storyidea(idea)
```

### Revise Script

```python
from Generators.GRevise import RevisedScriptGenerator

reviser = RevisedScriptGenerator()
reviser.Revise(idea)
```

### Add Voice Tags

```python
from Generators.GEnhanceScript import EnhanceScriptGenerator

enhancer = EnhanceScriptGenerator()
enhancer.Enhance(folder_name)
```

### Generate Voiceover

```python
from Generators.GVoice import VoiceMaker

voice_maker = VoiceMaker()
voice_maker.generate_audio()
```

## Pipeline Workflow

The typical story generation pipeline:

1. **Idea Generation** → `GStoryIdeas.py`
   - Input: Topic, tone, theme
   - Output: JSON files with story ideas in `Stories/0_Ideas/`

2. **Script Writing** → `GScript.py`
   - Input: Story idea
   - Output: Initial script in `Stories/1_Scripts/`

3. **Script Revision** → `GRevise.py`
   - Input: Initial script
   - Output: Revised script in `Stories/2_Revised/`

4. **Voice Enhancement** → `GEnhanceScript.py`
   - Input: Revised script
   - Output: Script with ElevenLabs tags

5. **Voice Generation** → `GVoice.py`
   - Input: Enhanced script
   - Output: MP3 voiceover in `Stories/3_VoiceOver/`

## Configuration

Key configuration options in `.env`:

- `DEFAULT_MODEL`: OpenAI model to use (default: gpt-4o-mini)
- `TEMPERATURE`: Creativity level for generation (0.0-1.0)
- `VOICE_ID`: ElevenLabs voice ID
- `VOICE_MODEL`: ElevenLabs model version
- `STORY_ROOT`: Root directory for generated content

## Development

### Running Tests

```bash
pip install -r requirements-dev.txt
pytest
```

### Code Formatting

```bash
black .
isort .
```

### Linting

```bash
pylint Generators/
flake8
```

## Known Issues & Limitations

See [RESEARCH_AND_IMPROVEMENTS.md](RESEARCH_AND_IMPROVEMENTS.md) for a comprehensive analysis of current issues and planned improvements.

### Current Limitations

1. **API Costs**: Each generation incurs OpenAI and ElevenLabs API costs
2. **Rate Limits**: Subject to API provider rate limits
3. **Platform-Specific Paths**: Some paths may need adjustment for different OS
4. **No Retry Logic**: API failures are not automatically retried
5. **Limited Error Handling**: Some edge cases may not be handled gracefully

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines

- Follow PEP 8 style guide
- Add tests for new features
- Update documentation
- Never commit API keys or sensitive data

## Security

### Reporting Security Issues

If you discover a security vulnerability, please email [security contact] instead of using the issue tracker.

### Security Best Practices

- Never commit API keys
- Use environment variables for secrets
- Regularly rotate API keys
- Review the `.gitignore` file
- Use `git-secrets` or similar tools to prevent accidental commits

## License

[Add your license here]

## Acknowledgments

- OpenAI for GPT models
- ElevenLabs for voice generation
- Community contributors

## Support

For questions, issues, or feature requests:
- Open an issue on GitHub
- Check existing documentation
- Review [RESEARCH_AND_IMPROVEMENTS.md](RESEARCH_AND_IMPROVEMENTS.md)

## Roadmap

See [RESEARCH_AND_IMPROVEMENTS.md](RESEARCH_AND_IMPROVEMENTS.md) for detailed roadmap including:

- ✅ Security improvements
- 🔄 Architecture refactoring
- 📝 Testing infrastructure
- 🚀 Performance optimizations
- 📚 Enhanced documentation

## Version History

- **Current**: Initial public release with security improvements
- See commit history for detailed changes

---

**Remember**: Always keep your API keys secure and never commit them to version control!
