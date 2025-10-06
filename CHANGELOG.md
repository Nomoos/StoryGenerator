# Changelog

All notable changes to the StoryGenerator project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Planned
- Shotlist generation from scripts
- SDXL keyframe generation
- Video synthesis with LTX-Video/Stable Video Diffusion
- Vision guidance integration
- Dynamic subtitle overlay
- One-click pipeline orchestration
- Enhanced post-production features
- C# implementation research

## [0.2.0] - 2025-10-06

### Added
- Comprehensive documentation suite
  - README.md with project overview
  - PIPELINE.md with detailed component breakdown
  - INSTALLATION.md with setup instructions
  - QUICKSTART.md for fast onboarding
  - TROUBLESHOOTING.md with common issues
  - FAQ.md with frequently asked questions
  - CHILD_ISSUES.md with 10 detailed issue templates
- Example scripts
  - basic_pipeline.py - Simple end-to-end example
  - batch_processing.py - Process multiple stories
  - custom_story_ideas.py - Create custom stories
- Environment configuration
  - .env.example template for API keys
  - Updated .gitignore with proper exclusions

### Changed
- Improved project structure documentation
- Enhanced security recommendations for API keys

## [0.1.0] - 2025-01-06 (Initial)

### Added
- Story idea generation with metadata
  - StoryIdea model with comprehensive parameters
  - Potential scoring across platforms, regions, age groups
- Script generation
  - GPT-4o-mini integration
  - ~360 word optimized scripts
  - Emotional hook optimization
- Script revision
  - Voice-optimized rewrites
  - Natural rhythm enhancement
- Voice synthesis
  - ElevenLabs API integration
  - LUFS normalization
  - Silence trimming
- ASR & Subtitle generation
  - WhisperX integration
  - Word-level timestamp alignment
  - SRT file generation
- Basic utilities
  - File management
  - Path handling
  - MP3 to MP4 conversion (with static image)

### Project Structure
- `Generators/` - Core pipeline generators
  - GStoryIdeas.py - Story idea generation
  - GScript.py - Script generation
  - GRevise.py - Script revision
  - GVoice.py - Voice synthesis
  - GTitles.py - Subtitle generation
- `Models/` - Data models
  - StoryIdea.py - Story metadata
- `Tools/` - Utility functions
  - Utils.py - File and path utilities
- `Generation/Manual/` - Manual test scripts

---

## Version Guidelines

### Version Numbers
- **Major version** (X.0.0): Breaking changes, major feature additions
- **Minor version** (0.X.0): New features, non-breaking changes
- **Patch version** (0.0.X): Bug fixes, minor improvements

### Categories
- **Added**: New features
- **Changed**: Changes to existing functionality
- **Deprecated**: Features marked for removal
- **Removed**: Removed features
- **Fixed**: Bug fixes
- **Security**: Security improvements

---

## Roadmap

### Version 0.3.0 (Planned)
- [ ] Environment setup improvements
- [ ] API key management system
- [ ] Model caching optimization
- [ ] GPU optimization
- [ ] Enhanced ASR with faster-whisper v3

### Version 0.4.0 (Planned)
- [ ] Shotlist generation
- [ ] Scene breakdown from scripts
- [ ] Alternative LLM support (Qwen2.5, Llama-3.1)

### Version 0.5.0 (Planned)
- [ ] SDXL keyframe generation
- [ ] Character consistency system
- [ ] Style presets
- [ ] ControlNet integration

### Version 0.6.0 (Planned)
- [ ] Video synthesis (LTX-Video or SVD)
- [ ] Motion control
- [ ] Scene transitions

### Version 0.7.0 (Planned)
- [ ] Enhanced post-production
- [ ] Dynamic subtitle overlay
- [ ] Background music mixing
- [ ] Multi-format export

### Version 0.8.0 (Planned)
- [ ] Vision guidance integration
- [ ] Quality validation
- [ ] Consistency checking

### Version 1.0.0 (Planned)
- [ ] Full pipeline integration
- [ ] One-click execution
- [ ] CLI interface
- [ ] Configuration management
- [ ] Error recovery
- [ ] Complete documentation

### Future Versions
- [ ] Web interface
- [ ] C# implementation
- [ ] Multi-language support
- [ ] Advanced customization
- [ ] Cloud deployment support

---

[Unreleased]: https://github.com/Nomoos/StoryGenerator/compare/v0.2.0...HEAD
[0.2.0]: https://github.com/Nomoos/StoryGenerator/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/Nomoos/StoryGenerator/releases/tag/v0.1.0
