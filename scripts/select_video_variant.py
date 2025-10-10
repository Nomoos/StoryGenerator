#!/usr/bin/env python3
"""
Standalone Video Variant Selection Script for StoryGenerator

Select the best video variant from multiple generated options.
Can be used for individual shots or batch processing.

Usage:
    # Select best from multiple variants
    python scripts/select_video_variant.py variant1.mp4 variant2.mp4 variant3.mp4
    
    # Select with shot ID
    python scripts/select_video_variant.py --shot-id shot_001 variant1.mp4 variant2.mp4
    
    # Manual override (select variant by index)
    python scripts/select_video_variant.py --manual 1 variant1.mp4 variant2.mp4 variant3.mp4
    
    # Batch process from JSON config
    python scripts/select_video_variant.py --batch variants_config.json
"""

import os
import sys
import json
import argparse
from pathlib import Path

# Add src/Python directory to path
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'src', 'Python'))

from Tools.VideoVariantSelector import VideoVariantSelector


def select_single_shot(
    variants: list,
    shot_id: str = None,
    manual_override: int = None,
    output_dir: str = None,
    save_report: bool = True
):
    """
    Select best variant for a single shot.
    
    Args:
        variants: List of video variant paths
        shot_id: Optional shot ID
        manual_override: Manual selection index
        output_dir: Output directory for report
        save_report: Whether to save report
    """
    print(f"\n{'='*70}")
    print(f"Video Variant Selection")
    if shot_id:
        print(f"Shot ID: {shot_id}")
    print(f"{'='*70}")
    
    print(f"\nAnalyzing {len(variants)} variant(s):")
    for i, variant in enumerate(variants):
        exists = "✓" if os.path.exists(variant) else "✗"
        print(f"  [{i}] {exists} {variant}")
    
    selector = VideoVariantSelector()
    
    try:
        selected_path, report = selector.select_best_variant(
            video_variants=variants,
            shot_id=shot_id,
            save_report=save_report,
            output_dir=output_dir,
            manual_override=manual_override
        )
        
        # Print results
        print(f"\n{'─'*70}")
        print("Selection Results")
        print(f"{'─'*70}")
        
        if report.get('manual_override'):
            print(f"🔧 Manual Override: Selected variant {report['selected_index']}")
        else:
            score = report['selected_score']
            print(f"🎯 Automated Selection: Variant {report['selected_index']}")
            print(f"\n   Quality Metrics:")
            print(f"   ├─ Overall Score: {score['overall_score']}/100")
            print(f"   ├─ Motion Smoothness: {score['motion_smoothness']:.2f}")
            print(f"   ├─ Temporal Consistency: {score['temporal_consistency']:.2f}")
            print(f"   └─ Artifact Ratio: {score['artifact_ratio']:.2f}")
            
            print(f"\n   Quality Checks:")
            checks = score['quality_checks']
            for check_name, passed in checks.items():
                status = "✅" if passed else "❌"
                print(f"   {status} {check_name.replace('_', ' ').title()}")
        
        print(f"\n✅ Selected: {selected_path}")
        print(f"   Reason: {report['selection_reason']}")
        
        if save_report and 'report_path' in report:
            print(f"\n📄 Selection report saved: {report['report_path']}")
        
        return 0
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1


def batch_select(config_path: str, output_dir: str = None, save_reports: bool = True):
    """
    Batch select variants from JSON config.
    
    Config format:
    {
        "shot_001": ["variant1.mp4", "variant2.mp4"],
        "shot_002": ["variant1.mp4", "variant2.mp4"]
    }
    
    Args:
        config_path: Path to JSON config file
        output_dir: Output directory for reports
        save_reports: Whether to save reports
    """
    print(f"\n{'='*70}")
    print(f"Batch Video Variant Selection")
    print(f"{'='*70}")
    
    # Load config
    try:
        with open(config_path, 'r') as f:
            variant_groups = json.load(f)
    except Exception as e:
        print(f"❌ Error loading config: {e}")
        return 1
    
    print(f"\nLoaded config: {config_path}")
    print(f"Found {len(variant_groups)} shot(s)")
    
    selector = VideoVariantSelector()
    
    try:
        results = selector.batch_select_variants(
            variant_groups=variant_groups,
            output_dir=output_dir,
            save_reports=save_reports
        )
        
        # Save batch results
        if save_reports:
            batch_report_path = os.path.join(
                output_dir or os.path.dirname(config_path),
                "batch_variant_selection.json"
            )
            
            batch_report = {
                'config_path': config_path,
                'total_shots': len(variant_groups),
                'successful_selections': len(results),
                'selections': {
                    shot_id: {
                        'selected_path': selected_path,
                        'overall_score': report['selected_score']['overall_score'] if report['selected_score'] else None
                    }
                    for shot_id, (selected_path, report) in results.items()
                }
            }
            
            os.makedirs(os.path.dirname(batch_report_path), exist_ok=True)
            with open(batch_report_path, 'w') as f:
                json.dump(batch_report, f, indent=2)
            
            print(f"\n📄 Batch report saved: {batch_report_path}")
        
        return 0
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Select best video variant from multiple options",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Select best from 3 variants
  python scripts/select_video_variant.py variant1.mp4 variant2.mp4 variant3.mp4
  
  # Select with shot ID
  python scripts/select_video_variant.py --shot-id shot_001 v1.mp4 v2.mp4
  
  # Manual override (select variant 1)
  python scripts/select_video_variant.py --manual 1 v1.mp4 v2.mp4 v3.mp4
  
  # Batch process from JSON config
  python scripts/select_video_variant.py --batch variants.json
  
  # Custom output directory
  python scripts/select_video_variant.py --output-dir /path/to/reports v1.mp4 v2.mp4
        """
    )
    
    parser.add_argument(
        'variants',
        nargs='*',
        help='Paths to video variant files'
    )
    
    parser.add_argument(
        '--shot-id',
        dest='shot_id',
        help='Shot ID for the selection report'
    )
    
    parser.add_argument(
        '--manual',
        dest='manual_override',
        type=int,
        help='Manual selection index (0-based) to override automatic selection'
    )
    
    parser.add_argument(
        '--no-save',
        dest='save_report',
        action='store_false',
        help='Do not save selection report to file'
    )
    
    parser.add_argument(
        '--output-dir',
        dest='output_dir',
        help='Directory to save selection reports'
    )
    
    parser.add_argument(
        '--batch',
        dest='batch_config',
        help='Batch process from JSON config file'
    )
    
    args = parser.parse_args()
    
    try:
        if args.batch_config:
            # Batch mode
            if not os.path.exists(args.batch_config):
                print(f"❌ Error: Config file not found: {args.batch_config}")
                return 1
            
            return batch_select(
                config_path=args.batch_config,
                output_dir=args.output_dir,
                save_reports=args.save_report
            )
        else:
            # Single shot mode
            if not args.variants:
                parser.print_help()
                print("\n❌ Error: No video variants provided")
                return 1
            
            if len(args.variants) < 2:
                print("⚠️  Warning: Only one variant provided. Selection requires at least 2 variants.")
                print(f"Using the single variant: {args.variants[0]}")
                return 0
            
            return select_single_shot(
                variants=args.variants,
                shot_id=args.shot_id,
                manual_override=args.manual_override,
                output_dir=args.output_dir,
                save_report=args.save_report
            )
            
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted by user")
        return 130
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
