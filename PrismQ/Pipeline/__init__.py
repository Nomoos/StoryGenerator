"""PrismQ.Pipeline - Content Creation Pipeline

Sequential pipeline stages from idea to final video:
1. 01_IdeaGeneration - Idea scraping and generation
2. 02_TextGeneration - Story, title, and scene generation
3. 03_AudioGeneration - Voice-over and subtitle generation
4. 04_ImageGeneration - Keyframe and image generation
5. 05_VideoGeneration - Video assembly and finalization

## Modular Architecture

Each stage is fully independent with clear input/output contracts.
See MODULAR_ARCHITECTURE.md for details.

Key files:
- MODULAR_ARCHITECTURE.md - Architecture overview
- MIGRATION_GUIDE.md - How to migrate existing code
- IMPLEMENTATION_STATUS.md - Current status and roadmap
- 01_IdeaGeneration/README.md - Stage 01 documentation
- 02_TextGeneration/README.md - Stage 02 documentation
- ... (and so on for each stage)
"""

__all__ = []
