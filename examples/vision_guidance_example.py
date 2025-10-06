#!/usr/bin/env python3
"""
Example usage of Vision Guidance utilities.
Demonstrates how to use GVision for image quality assessment and validation.
"""

import os
import sys
from pathlib import Path

# Add Python directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "Python"))
# Add project root for config
sys.path.insert(0, str(Path(__file__).parent.parent))

from Generators.GVision import GVision
from Tools.VisionUtils import (
    check_gpu_available,
    estimate_vram_usage,
    find_keyframe_images
)


def example_basic_usage():
    """Example: Basic initialization and model info."""
    print("="*60)
    print("Example 1: Basic Initialization")
    print("="*60)
    
    # Check GPU availability
    gpu_available, device_name = check_gpu_available()
    print(f"\nDevice: {device_name}")
    
    # Initialize generator (without loading model)
    generator = GVision(model_name="phi-3.5-vision", load_model=False)
    
    print("\nSupported models:")
    for name in GVision.SUPPORTED_MODELS.keys():
        vram = estimate_vram_usage(name)
        print(f"  - {name}: {vram} VRAM")
    
    print("\n✅ Generator initialized successfully")
    print("Note: Model will be loaded on first use\n")


def example_caption_generation():
    """Example: Generate captions for images (requires model)."""
    print("="*60)
    print("Example 2: Caption Generation")
    print("="*60)
    
    print("\nThis example requires transformers library and model download")
    print("To run this example:")
    print("1. Install transformers: pip install transformers")
    print("2. Ensure you have sufficient RAM/VRAM")
    print("3. First run will download the model (~3-8GB)")
    
    print("\nExample code:")
    print("""
    from Python.Generators.GVision import GVision
    
    # Initialize with model loading
    generator = GVision(model_name="phi-3.5-vision", load_model=True)
    
    # Generate caption for an image
    caption = generator.generate_caption("path/to/image.jpg")
    print(f"Caption: {caption.caption}")
    print(f"Model: {caption.model_used}")
    """)


def example_quality_assessment():
    """Example: Assess image quality (requires model)."""
    print("="*60)
    print("Example 3: Quality Assessment")
    print("="*60)
    
    print("\nThis example requires transformers library")
    
    print("\nExample code:")
    print("""
    from Python.Generators.GVision import GVision
    
    # Initialize generator
    generator = GVision(model_name="phi-3.5-vision", load_model=True)
    
    # Assess image quality
    quality = generator.assess_quality("path/to/image.jpg")
    
    print(f"Overall Quality: {quality.overall_quality}/10")
    print(f"Composition: {quality.composition}/10")
    print(f"Lighting: {quality.lighting}/10")
    print(f"Average: {quality.average_score():.1f}/10")
    print(f"Artifacts Detected: {quality.artifacts_detected}")
    print(f"Reasoning: {quality.reasoning}")
    """)


def example_consistency_check():
    """Example: Check consistency between images (requires model)."""
    print("="*60)
    print("Example 4: Consistency Check")
    print("="*60)
    
    print("\nThis example requires transformers library")
    
    print("\nExample code:")
    print("""
    from Python.Generators.GVision import GVision
    
    # Initialize generator
    generator = GVision(model_name="phi-3.5-vision", load_model=True)
    
    # Check consistency between consecutive frames
    consistency = generator.check_consistency(
        "path/to/scene1.jpg",
        "path/to/scene2.jpg"
    )
    
    print(f"Character Consistency: {consistency.character_consistency}/10")
    print(f"Style Consistency: {consistency.style_consistency}/10")
    print(f"Visual Continuity: {consistency.visual_continuity}/10")
    print(f"Average: {consistency.average_score():.1f}/10")
    
    if consistency.inconsistencies:
        print("Inconsistencies found:")
        for issue in consistency.inconsistencies:
            print(f"  - {issue}")
    """)


def example_storyboard_validation():
    """Example: Validate entire storyboard (requires model)."""
    print("="*60)
    print("Example 5: Storyboard Validation")
    print("="*60)
    
    print("\nThis example requires transformers library")
    
    print("\nExample code:")
    print("""
    from Python.Generators.GVision import GVision
    from Python.Tools.VisionUtils import find_keyframe_images
    
    # Find all keyframe images in a story folder
    image_paths = find_keyframe_images("path/to/story_folder")
    
    # Initialize generator
    generator = GVision(model_name="phi-3.5-vision", load_model=True)
    
    # Validate entire storyboard
    validation = generator.validate_storyboard(
        image_paths,
        check_consistency=True,
        quality_threshold=6.0,
        consistency_threshold=6.0
    )
    
    print(f"Story: {validation.story_name}")
    print(f"Scenes: {validation.scene_count}")
    print(f"Avg Quality: {validation.overall_quality_avg:.1f}/10")
    print(f"Avg Consistency: {validation.overall_consistency_avg:.1f}/10")
    print(f"Validation Passed: {validation.validation_passed}")
    
    if validation.recommendations:
        print("\\nRecommendations:")
        for rec in validation.recommendations:
            print(f"  - {rec}")
    
    # Save validation results
    import json
    with open("validation_results.json", "w") as f:
        json.dump(validation.to_dict(), f, indent=2)
    
    # Clean up resources
    generator.cleanup()
    """)


def example_integration_with_pipeline():
    """Example: Integration with video pipeline."""
    print("="*60)
    print("Example 6: Pipeline Integration")
    print("="*60)
    
    print("\nIntegrating vision guidance with keyframe generation:")
    
    print("\nExample code:")
    print("""
    from Python.Generators.GVision import GVision
    from Python.Generators.GKeyframeGenerator import KeyframeGenerator
    
    # Initialize both generators
    vision_gen = GVision(model_name="phi-3.5-vision", load_model=True)
    keyframe_gen = KeyframeGenerator()
    
    # Generate keyframe
    keyframe_path = "generated_keyframe.jpg"
    keyframe_gen.generate_scene_keyframe(scene, output_path=keyframe_path)
    
    # Validate generated keyframe
    result = vision_gen.validate_image(
        keyframe_path,
        check_quality=True,
        quality_threshold=7.0
    )
    
    if result.quality_score.average_score() < 7.0:
        print("Quality too low, regenerating...")
        # Regenerate with adjusted parameters
        keyframe_gen.generate_scene_keyframe(
            scene,
            output_path=keyframe_path,
            num_inference_steps=50  # Higher steps for better quality
        )
    
    # Clean up
    vision_gen.cleanup()
    """)


def main():
    """Run all examples."""
    print("\n" + "="*60)
    print("VISION GUIDANCE - USAGE EXAMPLES")
    print("="*60 + "\n")
    
    example_basic_usage()
    example_caption_generation()
    example_quality_assessment()
    example_consistency_check()
    example_storyboard_validation()
    example_integration_with_pipeline()
    
    print("\n" + "="*60)
    print("For more information, see:")
    print("  - PIPELINE.md (Section 4: Vision Guidance)")
    print("  - docs/CHILD_ISSUES.md (Vision Guidance Integration)")
    print("  - tests/test_vision.py (Working examples)")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()
