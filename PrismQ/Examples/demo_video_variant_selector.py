#!/usr/bin/env python3
"""
Example demonstration of VideoVariantSelector

Shows how to use the variant selector in different scenarios.
"""

import os
import sys
import json
from pathlib import Path

# Add src/Python directory to path
sys.path.insert(
    0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src", "Python")
)

from Tools.VideoVariantSelector import VideoVariantSelector


def example_single_selection():
    """Example: Select best variant from a list."""
    print("\n" + "=" * 70)
    print("Example 1: Single Shot Variant Selection")
    print("=" * 70)

    print(
        """
Scenario: You have 3 video variants for shot_001:
- variant_ltx.mp4 (generated with LTX-Video)
- variant_interp.mp4 (generated with frame interpolation)
- variant_stable.mp4 (generated with stable diffusion video)
    """
    )

    # In a real scenario, these would be actual video files
    variants = [
        "Generator/videos/ltx/shot_001/variant_ltx.mp4",
        "Generator/videos/interpolated/shot_001/variant_interp.mp4",
        "Generator/videos/stable/shot_001/variant_stable.mp4",
    ]

    print("Code:")
    print(
        """
    from Tools.VideoVariantSelector import VideoVariantSelector
    
    selector = VideoVariantSelector()
    
    selected, report = selector.select_best_variant(
        video_variants=variants,
        shot_id='shot_001',
        save_report=True
    )
    
    print(f"Selected: {selected}")
    print(f"Quality Score: {report['selected_score']['overall_score']}/100")
    print(f"Reason: {report['selection_reason']}")
    """
    )

    print("\nExpected Output:")
    print(
        """
    Selected: Generator/videos/ltx/shot_001/variant_ltx.mp4
    Quality Score: 87.5/100
    Reason: Selected for: high overall quality, smooth motion, minimal artifacts
    
    📄 Report saved: Generator/videos/ltx/shot_001/shot_001_variant_selection.json
    """
    )


def example_manual_override():
    """Example: Manually override automatic selection."""
    print("\n" + "=" * 70)
    print("Example 2: Manual Override")
    print("=" * 70)

    print(
        """
Scenario: The automatic selection picked variant 1, but you prefer 
the artistic style of variant 2 for creative reasons.
    """
    )

    print("Code:")
    print(
        """
    from Tools.VideoVariantSelector import VideoVariantSelector
    
    selector = VideoVariantSelector()
    
    # Use manual_override parameter to select variant 2 (index 1)
    selected, report = selector.select_best_variant(
        video_variants=variants,
        shot_id='shot_001',
        manual_override=1,  # Select second variant (0-indexed)
        save_report=True
    )
    
    print(f"Selected: {selected}")
    print(f"Override: {report['manual_override']}")
    """
    )

    print("\nExpected Output:")
    print(
        """
    Selected: Generator/videos/interpolated/shot_001/variant_interp.mp4
    Override: True
    Reason: Manual override: User selected variant 1
    """
    )


def example_batch_processing():
    """Example: Process multiple shots at once."""
    print("\n" + "=" * 70)
    print("Example 3: Batch Processing")
    print("=" * 70)

    print(
        """
Scenario: You have multiple shots, each with 2-3 variants, and want
to process them all at once.
    """
    )

    print("Step 1: Create batch config JSON file:")
    print(
        """
    # variants_config.json
    {
      "shot_001": [
        "Generator/videos/ltx/shot_001/variant_ltx.mp4",
        "Generator/videos/interpolated/shot_001/variant_interp.mp4"
      ],
      "shot_002": [
        "Generator/videos/ltx/shot_002/variant_ltx.mp4",
        "Generator/videos/interpolated/shot_002/variant_interp.mp4"
      ],
      "shot_003": [
        "Generator/videos/ltx/shot_003/variant_ltx.mp4",
        "Generator/videos/interpolated/shot_003/variant_interp.mp4",
        "Generator/videos/stable/shot_003/variant_stable.mp4"
      ]
    }
    """
    )

    print("\nStep 2: Run batch selection (CLI):")
    print(
        """
    python scripts/select_video_variant.py --batch variants_config.json
    """
    )

    print("\nStep 2 (Alternative): Run batch selection (Python API):")
    print(
        """
    from Tools.VideoVariantSelector import VideoVariantSelector
    import json
    
    # Load config
    with open('variants_config.json', 'r') as f:
        variant_groups = json.load(f)
    
    selector = VideoVariantSelector()
    results = selector.batch_select_variants(
        variant_groups=variant_groups,
        save_reports=True
    )
    
    # Print results
    for shot_id, (selected_path, report) in results.items():
        score = report['selected_score']['overall_score']
        print(f"{shot_id}: {selected_path} (score: {score}/100)")
    """
    )

    print("\nExpected Output:")
    print(
        """
    ======================================================================
    Batch Variant Selection: 3 shots
    ======================================================================
    
    Processing shot: shot_001 (2 variants)
      ✅ Selected: variant_ltx.mp4
         Score: 85.2/100
         Selected for: high overall quality, smooth motion
    
    Processing shot: shot_002 (2 variants)
      ✅ Selected: variant_interp.mp4
         Score: 88.7/100
         Selected for: high overall quality, consistent frames, minimal artifacts
    
    Processing shot: shot_003 (3 variants)
      ✅ Selected: variant_ltx.mp4
         Score: 91.3/100
         Selected for: excellent overall quality, smooth motion, minimal artifacts
    
    ======================================================================
    Batch Selection Complete: 3/3 shots processed
    ======================================================================
    
    📄 Batch report saved: batch_variant_selection.json
    """
    )


def example_custom_thresholds():
    """Example: Customize quality thresholds."""
    print("\n" + "=" * 70)
    print("Example 4: Custom Quality Thresholds")
    print("=" * 70)

    print(
        """
Scenario: You have stricter quality requirements and want to adjust
the minimum acceptable thresholds.
    """
    )

    print("Code:")
    print(
        """
    from Tools.VideoVariantSelector import VideoVariantSelector
    
    selector = VideoVariantSelector()
    
    # Customize thresholds (default values shown)
    selector.MIN_MOTION_SCORE = 0.7      # Increase from 0.6
    selector.MIN_TEMPORAL_SCORE = 0.8    # Increase from 0.7
    selector.MAX_ARTIFACT_RATIO = 0.10   # Decrease from 0.15
    selector.MIN_OVERALL_SCORE = 70      # Increase from 60
    
    selected, report = selector.select_best_variant(
        video_variants=variants,
        shot_id='shot_001',
        save_report=True
    )
    
    # Check if selected variant meets custom thresholds
    score = report['selected_score']
    checks = score['quality_checks']
    
    if all(checks.values()):
        print(f"✅ Selected variant meets all custom quality thresholds")
    else:
        print(f"⚠️ Selected variant has quality issues:")
        for check, passed in checks.items():
            if not passed:
                print(f"  - {check}: FAILED")
    """
    )


def example_report_analysis():
    """Example: Analyze selection report."""
    print("\n" + "=" * 70)
    print("Example 5: Analyzing Selection Reports")
    print("=" * 70)

    print(
        """
Scenario: After batch processing, you want to review which shots had
lower quality scores and may need attention.
    """
    )

    print("Code:")
    print(
        """
    import json
    from pathlib import Path
    
    # Load batch report
    with open('batch_variant_selection.json', 'r') as f:
        batch_report = json.load(f)
    
    # Analyze quality scores
    low_quality_shots = []
    
    for shot_id, selection_data in batch_report['selections'].items():
        score = selection_data.get('overall_score')
        
        if score and score < 80:
            low_quality_shots.append((shot_id, score))
    
    # Print results
    if low_quality_shots:
        print(f"Found {len(low_quality_shots)} shot(s) with quality < 80:")
        for shot_id, score in sorted(low_quality_shots, key=lambda x: x[1]):
            print(f"  ⚠️ {shot_id}: {score}/100")
    else:
        print("✅ All shots have quality score >= 80")
    
    # Load individual report for detailed analysis
    report_path = f"shot_001_variant_selection.json"
    with open(report_path, 'r') as f:
        report = json.load(f)
    
    # Check individual metrics
    score = report['selected_score']
    print(f"\\nDetailed metrics for shot_001:")
    print(f"  Motion Smoothness: {score['motion_smoothness']:.2f}")
    print(f"  Temporal Consistency: {score['temporal_consistency']:.2f}")
    print(f"  Artifact Ratio: {score['artifact_ratio']:.2f}")
    print(f"  Overall Score: {score['overall_score']}/100")
    """
    )


def main():
    """Run all examples."""
    print("\n" + "=" * 70)
    print("VideoVariantSelector Usage Examples")
    print("=" * 70)

    print(
        """
This demonstration shows various ways to use the VideoVariantSelector
for selecting the best video variant from multiple generation methods.
    """
    )

    examples = [
        example_single_selection,
        example_manual_override,
        example_batch_processing,
        example_custom_thresholds,
        example_report_analysis,
    ]

    for example in examples:
        example()

    print("\n" + "=" * 70)
    print("Additional Resources")
    print("=" * 70)
    print(
        """
Documentation:
  - Implementation Summary: issues/resolved/video-production/GROUP_8_VIDEO_VARIANT_SELECTION_SUMMARY.md
  - Source Code: src/Python/Tools/VideoVariantSelector.py
  - CLI Tool: scripts/select_video_variant.py
  - Tests: tests/test_video_variant_selector.py

Quick Start:
  # Simple selection
  python scripts/select_video_variant.py variant1.mp4 variant2.mp4
  
  # Get help
  python scripts/select_video_variant.py --help
  
  # Run tests
  python tests/test_video_variant_selector.py
    """
    )

    print("\n" + "=" * 70)
    print("✅ Examples Complete")
    print("=" * 70)


if __name__ == "__main__":
    main()
