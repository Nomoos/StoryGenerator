"""
Manual Video Generation Script

Creates short-form vertical videos (1080×1920) from existing story data.
Integrates audio from GVoice and subtitles from GTitles.

Usage:
    python Generation/Manual/MVideo.py
"""

import os
from Generators.GVideo import VideoGenerator


def manual_video_generation():
    """
    Generate videos for all stories in the TITLES_PATH.
    
    This function:
    1. Creates a VideoGenerator instance
    2. Processes all folders in TITLES_PATH
    3. Creates 1080×1920 portrait videos with subtitles
    """
    print("🎬 Starting Manual Video Generation...")
    print("=" * 60)
    
    # Initialize video generator with default settings
    # - 1080×1920 (portrait/vertical format)
    # - 30 fps
    generator = VideoGenerator(width=1080, height=1920, fps=30)
    
    # Batch create videos for all folders
    # Uses default background image from Resources/baground.jpg
    generator.batch_create_videos()
    
    print("\n" + "=" * 60)
    print("✅ Manual video generation complete!")


if __name__ == "__main__":
    manual_video_generation()
