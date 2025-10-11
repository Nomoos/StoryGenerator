"""PrismQ - Story Generation Framework

A modular, pipeline-based framework for automated story generation,
media processing, and multi-platform distribution.

This package is organized into logical groups following the content pipeline:

**Pipeline Stages (Sequential):**
1. Pipeline/01_IdeaGeneration - Idea scraping and generation
2. Pipeline/02_TextGeneration - Story, title, and scene generation
3. Pipeline/03_AudioGeneration - Voice-over and subtitle generation
4. Pipeline/04_ImageGeneration - Keyframe and image generation
5. Pipeline/05_VideoGeneration - Video assembly and finalization

**Infrastructure:**
- Infrastructure/Core - Shared utilities and configuration
- Infrastructure/Platform - External service integrations
- Infrastructure/Utilities - Tools, scripts, and automation

**Resources:**
- Resources/Assets - Media assets
- Resources/Data - Runtime data
- Resources/Configuration - Configuration files

**Development:**
- Development/Tests - Test suite
- Development/Examples - Usage examples
- Development/Documentation - Project documentation

**Projects:**
- Projects/CSharp - C# implementation
- Projects/Research - Research documents
- Projects/Issues - Issue tracking
- Projects/Podcasts - Podcast content

Example usage:
    from PrismQ.Pipeline.01_IdeaGeneration.IdeaScraper.idea_generation import IdeaGenerator
    from PrismQ.Infrastructure.Core.Shared.config import settings
    from PrismQ.Infrastructure.Platform.Providers import OpenAIProvider
"""

__version__ = "1.0.0"
