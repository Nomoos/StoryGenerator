#!/usr/bin/env python3
"""
Example demonstrating the EngagementOptimizer module.

This script shows how to use the research-based video engagement optimization
components integrated from PrismQ.Research.Generator.Video.
"""
import os
import sys

# Add EngagementOptimizer module to path
module_path = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(module_path, 'EngagementOptimizer'))

from config import GenerationConfig
from pipeline import VideoPipeline


def main():
    """Generate example video with optimal engagement settings."""
    
    print("\n" + "=" * 70)
    print("ENGAGEMENT OPTIMIZER - DEMO")
    print("Research-based visual engagement principles for short-form video")
    print("=" * 70 + "\n")
    
    # Create configuration
    config = GenerationConfig(
        output_resolution=(1080, 1920),  # 9:16 vertical format
        fps=30,
        target_duration=27,  # 27 seconds (optimal for retention)
        base_clip_duration=3,
        seed=42,
        cfg_scale=7.0,
    )
    
    # Initialize pipeline
    pipeline = VideoPipeline(config)
    
    # Define captions (synchronized with pattern breaks for maximum impact)
    captions = [
        ("Visual Engagement Principles", 0),
        ("Constant Motion", 120),
        ("High Contrast + Neon", 240),
        ("Pattern Breaks", 360),
        ("Optimized for Watch Time", 480),
        ("Built with PrismQ", 600),
    ]
    
    # Create output directory
    output_dir = os.path.join(os.path.dirname(__file__), "output")
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "engagement_demo.mp4")
    
    # Display configuration
    print("📊 Configuration:")
    print(f"   Resolution: {config.output_resolution[0]}×{config.output_resolution[1]}")
    print(f"   Duration: {config.target_duration}s")
    print(f"   FPS: {config.fps}")
    print(f"   Seed: {config.seed}\n")
    
    # Run pipeline
    pipeline.run_full_pipeline(output_path, captions)
    
    # Summary
    print("\n" + "=" * 70)
    print("✅ DEMO COMPLETE!")
    print("=" * 70)
    print(f"\n📹 Video saved to: {output_path}")
    print(f"\n💡 Key features applied:")
    print(f"   ✓ Constant micro-movement (nothing static >300ms)")
    print(f"   ✓ High contrast with neon accents")
    print(f"   ✓ Pattern breaks every ~1.5s")
    print(f"   ✓ Micro-zoom progression")
    print(f"   ✓ Story captions with fade animations")
    print(f"   ✓ Progress bar with goal-gradient effect")
    print(f"\n📚 Research source:")
    print(f"   https://github.com/PrismQDev/PrismQ.Research.Generator.Video")
    print()


if __name__ == "__main__":
    main()
