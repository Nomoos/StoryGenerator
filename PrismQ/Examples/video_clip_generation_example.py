#!/usr/bin/env python3
"""
Example: Generate video clips using the VideoClipGenerator.

This script demonstrates how to use the video clip generation module
to create clips from shots using either LTX-Video or frame interpolation.
"""

import os
import sys
from pathlib import Path

# Add src path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src" / "research" / "python"))

from generate_video_clips import VideoClipGenerator


def example_ltx_generation():
    """Example: Generate clips using LTX-Video."""
    print("\n" + "=" * 60)
    print("Example 1: LTX-Video Generation")
    print("=" * 60)

    # Initialize generator for LTX mode
    generator = VideoClipGenerator(use_ltx=True, fps=30, device="cpu")  # Use "cuda" for GPU

    # Define shots for LTX generation
    shots = [
        {
            "image_path": "examples/keyframes/shot_000.png",
            "motion": "slow zoom in",
            "intensity": 0.3,
            "duration": 10.0,
        },
        {
            "image_path": "examples/keyframes/shot_001.png",
            "motion": "pan right",
            "intensity": 0.5,
            "duration": 12.0,
        },
    ]

    print(f"Generating {len(shots)} clips using LTX-Video...")

    # Note: This won't actually generate videos without valid image files
    # and the LTX models installed. This is just to demonstrate the API.

    try:
        clip_paths = generator.generate_clips_for_story(
            shots=shots,
            segment="tech",
            age="18-23",
            title_id="example_story_ltx",
            base_output_dir="videos",
        )

        print(f"\n✅ Would generate {len(clip_paths)} clips")
        print(f"   Output directory: videos/ltx/tech/18-23/example_story_ltx/")
    except Exception as e:
        print(f"⚠️  Note: Actual generation requires valid images and models")
        print(f"   This is just an API demonstration")

    finally:
        generator.cleanup()


def example_interpolation_generation():
    """Example: Generate clips using frame interpolation."""
    print("\n" + "=" * 60)
    print("Example 2: Frame Interpolation Generation")
    print("=" * 60)

    # Initialize generator for interpolation mode
    generator = VideoClipGenerator(use_ltx=False, fps=30, device="cpu")

    # Define shots with keyframes for interpolation
    shots = [
        {
            "keyframes": [
                "examples/keyframes/shot_002_kf1.png",
                "examples/keyframes/shot_002_kf2.png",
                "examples/keyframes/shot_002_kf3.png",
            ],
            "duration": 15.0,
        },
        {
            "keyframes": [
                "examples/keyframes/shot_003_kf1.png",
                "examples/keyframes/shot_003_kf2.png",
            ],
            "duration": 10.0,
        },
    ]

    print(f"Generating {len(shots)} clips using frame interpolation...")

    try:
        clip_paths = generator.generate_clips_for_story(
            shots=shots,
            segment="lifestyle",
            age="24-30",
            title_id="example_story_interp",
            base_output_dir="videos",
        )

        print(f"\n✅ Would generate {len(clip_paths)} clips")
        print(f"   Output directory: videos/interp/lifestyle/24-30/example_story_interp/")
    except Exception as e:
        print(f"⚠️  Note: Actual generation requires valid images and FFmpeg")
        print(f"   This is just an API demonstration")

    finally:
        generator.cleanup()


def example_config_based_generation():
    """Example: Use configuration file to determine generation method."""
    print("\n" + "=" * 60)
    print("Example 3: Configuration-Based Generation")
    print("=" * 60)

    # Initialize generator without specifying method
    # It will use the default from pipeline.yaml
    generator = VideoClipGenerator(config_path="data/config/pipeline.yaml", fps=30)

    # Check which method is being used
    if generator.use_ltx:
        print(f"✅ Using LTX-Video (from config: switches.use_ltx=true)")
    else:
        print(f"✅ Using Frame Interpolation (from config: switches.use_ltx=false)")

    generator.cleanup()


def example_single_shot():
    """Example: Generate a single shot clip."""
    print("\n" + "=" * 60)
    print("Example 4: Single Shot Generation")
    print("=" * 60)

    generator = VideoClipGenerator(use_ltx=True, fps=24, device="cpu")

    shot = {
        "image_path": "examples/keyframes/shot_004.png",
        "motion": "zoom in",
        "intensity": 0.4,
        "duration": 10.0,
    }

    output_path = "videos/ltx/demo/18-23/single_shot/shot_0.mp4"

    print(f"Generating single shot clip...")
    print(f"  Output: {output_path}")

    try:
        clip_path = generator.generate_shot_clip(
            shot=shot, output_path=output_path, duration=10.0, seed=42
        )
        print(f"✅ Would generate: {clip_path}")
    except Exception as e:
        print(f"⚠️  Note: Requires valid image file and models")

    generator.cleanup()


def main():
    """Run all examples."""
    print("\n" + "=" * 60)
    print("Video Clip Generation - Usage Examples")
    print("=" * 60)
    print("\nThese examples demonstrate the API usage.")
    print("Actual video generation requires:")
    print("  - Valid keyframe images")
    print("  - LTX-Video models (for Variant A)")
    print("  - FFmpeg + interpolation models (for Variant B)")
    print("  - GPU with sufficient VRAM (recommended)")

    # Run examples
    example_ltx_generation()
    example_interpolation_generation()
    example_config_based_generation()
    example_single_shot()

    print("\n" + "=" * 60)
    print("Examples Complete")
    print("=" * 60)
    print("\nFor real video generation, see:")
    print("  - docs/VIDEO_CLIP_GENERATION.md")
    print("  - examples/video_clips/example_shots.yaml")
    print("\nTo generate from command line:")
    print("  python src/research/python/generate_video_clips.py --help")


if __name__ == "__main__":
    main()
