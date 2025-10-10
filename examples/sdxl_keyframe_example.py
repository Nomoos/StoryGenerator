#!/usr/bin/env python3
"""
Example: SDXL Keyframe Generation

Demonstrates how to use the SDXL-based keyframe generator to create
high-quality 1080x1920 keyframes for vertical video.
"""

import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from Python.Generators.GKeyframeGenerator import KeyframeGenerator
from Python.Models.StoryIdea import StoryIdea


def example_basic_generation():
    """
    Example 1: Basic keyframe generation with SDXL
    """
    print("=" * 70)
    print("Example 1: Basic SDXL Keyframe Generation")
    print("=" * 70)

    # Load an existing story (you need to have a story generated first)
    # Replace with your actual story title
    story_title = "The Unexpected Friend"  # Example story

    try:
        # Try to load story idea
        story_idea = StoryIdea.from_file(story_title)
    except FileNotFoundError:
        print(f"❌ Story '{story_title}' not found.")
        print("   Please generate a story first using the basic pipeline.")
        return

    print(f"\n📖 Loaded story: {story_idea.story_title}")

    # Initialize SDXL keyframe generator
    print("\n🎨 Initializing SDXL keyframe generator...")
    generator = KeyframeGenerator(
        use_refiner=True,  # Use refiner for maximum quality
        style_preset="cinematic",  # Cinematic style
    )

    # Generate keyframes
    print("\n🎬 Generating keyframes...")
    scenes = generator.generate_keyframes(story_idea)

    print(f"\n✅ Generated keyframes for {len(scenes)} scenes")

    # Show summary
    print("\n📊 Keyframe Summary:")
    total_keyframes = sum(len(scene.keyframes) for scene in scenes if hasattr(scene, "keyframes"))
    print(f"   Total keyframes: {total_keyframes}")

    # Cleanup
    generator.cleanup()


def example_fast_generation():
    """
    Example 2: Fast generation without refiner (for testing or low VRAM)
    """
    print("\n" + "=" * 70)
    print("Example 2: Fast Generation (No Refiner)")
    print("=" * 70)

    story_title = "The Unexpected Friend"  # Example story

    try:
        story_idea = StoryIdea.from_file(story_title)
    except FileNotFoundError:
        print(f"❌ Story '{story_title}' not found.")
        return

    print(f"\n📖 Loaded story: {story_idea.story_title}")

    # Initialize without refiner for faster generation
    print("\n🎨 Initializing SDXL (fast mode)...")
    generator = KeyframeGenerator(
        use_refiner=False,  # Disable refiner
        num_inference_steps=30,  # Fewer steps
        style_preset="photorealistic",
    )

    print("\n🎬 Generating keyframes (fast mode)...")
    scenes = generator.generate_keyframes(story_idea)

    print(f"\n✅ Generated keyframes for {len(scenes)} scenes (fast mode)")

    # Cleanup
    generator.cleanup()


def example_style_comparison():
    """
    Example 3: Generate same scene with different styles
    """
    print("\n" + "=" * 70)
    print("Example 3: Style Comparison")
    print("=" * 70)

    # For this example, we'll show how to apply different styles
    # (actual generation would require loading a story)

    print("\n🎨 Available styles:")
    styles = ["cinematic", "photorealistic", "dramatic", "soft", "vibrant", "moody"]

    for i, style in enumerate(styles, 1):
        print(f"   {i}. {style}")

    print("\n💡 To use different styles:")
    print("   generator = KeyframeGenerator(style_preset='cinematic')")
    print("   # or")
    print("   generator.apply_style_preset('dramatic')")


def main():
    """Main function to run examples"""
    print("🎬 SDXL Keyframe Generation Examples")
    print("=" * 70)

    print("\n⚠️  Note: These examples require:")
    print("   - A GPU with 12GB+ VRAM (or use fast mode)")
    print("   - An existing story with scene descriptions")
    print("   - SDXL models will be downloaded on first run (~13GB)")

    # Check for GPU
    try:
        import torch

        has_gpu = torch.cuda.is_available()
        print(f"\n🖥️  GPU Available: {'Yes ✅' if has_gpu else 'No ❌ (will use CPU - slower)'}")
        if has_gpu:
            print(f"   GPU: {torch.cuda.get_device_name(0)}")
            print(f"   VRAM: {torch.cuda.get_device_properties(0).total_memory / 1e9:.1f} GB")
    except ImportError:
        print("\n⚠️  PyTorch not installed. Please run: pip install -r requirements.txt")
        return

    # Run examples
    print("\n" + "=" * 70)
    print("Choose an example to run:")
    print("  1. Basic generation (with refiner)")
    print("  2. Fast generation (no refiner)")
    print("  3. Style comparison (info only)")
    print("  0. Exit")

    try:
        choice = input("\nEnter choice (0-3): ").strip()

        if choice == "1":
            example_basic_generation()
        elif choice == "2":
            example_fast_generation()
        elif choice == "3":
            example_style_comparison()
        elif choice == "0":
            print("\n👋 Goodbye!")
        else:
            print("\n❌ Invalid choice")

    except KeyboardInterrupt:
        print("\n\n👋 Interrupted by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    main()
