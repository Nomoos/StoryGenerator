"""
Configuration module for StoryGenerator.

This module contains configuration files for various components:
- sdxl_config: SDXL keyframe generation settings
- vision_prompts: Prompts for vision model quality assessment
"""

from . import sdxl_config
from . import vision_prompts

__all__ = ['sdxl_config', 'vision_prompts']
