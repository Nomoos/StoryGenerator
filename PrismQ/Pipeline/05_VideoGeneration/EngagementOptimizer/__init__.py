"""
EngagementOptimizer - Research-based video engagement optimization.

This module implements visual engagement principles from PrismQ.Research.Generator.Video
for maximizing watch time on short-form vertical video platforms (TikTok, Reels, Shorts).

Key Features:
- Constant Motion: Nothing remains static for >300ms
- High Contrast + Saturated Accents: Bright "neon" edges over dark midtones
- Pattern + Surprise: Smooth flow with periodic pattern breaks
- Enhanced Overlays: Story captions + progress bar optimized for retention

Research Repository: https://github.com/PrismQDev/PrismQ.Research.Generator.Video
"""

from .config import GenerationConfig
from .visual_style import VisualStyle
from .motion import MotionEffects
from .overlay import Overlay
from .generator import VideoGenerator
from .pipeline import VideoPipeline

__all__ = [
    'GenerationConfig',
    'VisualStyle',
    'MotionEffects',
    'Overlay',
    'VideoGenerator',
    'VideoPipeline',
]
