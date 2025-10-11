#!/usr/bin/env python3
"""
Standalone Quality Check Script for StoryGenerator Videos

Run quality checks on final videos and generate QC reports.
Can be used to check individual videos or batch process a directory.

Usage:
    # Check a single video
    python scripts/check_video_quality.py /path/to/video.mp4

    # Check all videos in a directory
    python scripts/check_video_quality.py /path/to/directory/

    # Check with custom title ID
    python scripts/check_video_quality.py /path/to/video.mp4 --title-id my_title_001

    # Check without saving report
    python scripts/check_video_quality.py /path/to/video.mp4 --no-save
"""

import os
import sys
import argparse
from pathlib import Path
from glob import glob

# Add src/Python directory to path
sys.path.insert(
    0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src", "Python")
)

from Tools.VideoQualityChecker import VideoQualityChecker


def check_single_video(
    video_path: str, title_id: str = None, save_report: bool = True, output_dir: str = None
):
    """
    Check quality of a single video file.

    Args:
        video_path: Path to video file
        title_id: Optional title ID for the report
        save_report: Whether to save QC report
        output_dir: Directory to save report (defaults to video directory)
    """
    print(f"\n{'='*70}")
    print(f"Checking: {video_path}")
    print(f"{'='*70}")

    if not os.path.exists(video_path):
        print(f"❌ Error: Video file not found: {video_path}")
        return False

    checker = VideoQualityChecker()

    passed, report = checker.check_video_quality(
        video_path, title_id=title_id, save_report=save_report, output_dir=output_dir
    )

    # Print detailed results
    print(f"\n📊 Quality Check Results:")
    print(f"{'─'*70}")
    print(f"Overall Status: {report['overall_status'].upper()}")
    print(f"Quality Score: {report['quality_score']}/100")
    print(f"Checks Passed: {report['checks_passed']}/{report['checks_total']}")
    print(f"Pass Rate: {report['pass_rate']}%")

    print(f"\n📋 Individual Checks:")
    print(f"{'─'*70}")
    for check_name, check_data in report.get("checks", {}).items():
        status_emoji = "✅" if check_data["passed"] else "❌"
        print(f"{status_emoji} {check_data['name']}: {check_data.get('message', 'N/A')}")

        # Print important details
        details = check_data.get("details", {})
        if "size_mb" in details:
            print(f"   └─ Size: {details['size_mb']} MB")
        if "resolution" in details:
            print(f"   └─ Resolution: {details['resolution']}")
        if "video_codec" in details:
            print(f"   └─ Video Codec: {details['video_codec']}")
        if "audio_codec" in details:
            print(f"   └─ Audio Codec: {details['audio_codec']}")
        if "video_bitrate_kbps" in details:
            print(f"   └─ Video Bitrate: {details['video_bitrate_kbps']} kbps")
        if "duration_seconds" in details:
            print(f"   └─ Duration: {details['duration_seconds']}s")

    if save_report and "report_path" in report:
        print(f"\n📄 QC Report saved to: {report['report_path']}")

    return passed


def check_directory(directory_path: str, pattern: str = "*.mp4", save_reports: bool = True):
    """
    Check quality of all videos in a directory.

    Args:
        directory_path: Path to directory
        pattern: File pattern to match (default: *.mp4)
        save_reports: Whether to save QC reports
    """
    print(f"\n{'='*70}")
    print(f"Batch Quality Check: {directory_path}")
    print(f"{'='*70}")

    # Find all video files
    search_pattern = os.path.join(directory_path, "**", pattern)
    video_files = glob(search_pattern, recursive=True)

    if not video_files:
        print(f"⚠️  No video files found matching pattern: {pattern}")
        return

    print(f"\nFound {len(video_files)} video file(s)")

    results = []
    for i, video_path in enumerate(video_files, 1):
        print(f"\n[{i}/{len(video_files)}] Processing: {os.path.basename(video_path)}")

        try:
            passed = check_single_video(video_path, save_report=save_reports)
            results.append((video_path, passed))
        except Exception as e:
            print(f"❌ Error checking {video_path}: {e}")
            results.append((video_path, False))

    # Print summary
    print(f"\n{'='*70}")
    print("Batch Summary")
    print(f"{'='*70}")

    passed_count = sum(1 for _, passed in results if passed)
    total_count = len(results)

    for video_path, passed in results:
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"{status}: {os.path.basename(video_path)}")

    print(f"\n{'─'*70}")
    print(f"Total: {passed_count}/{total_count} videos passed quality checks")

    if passed_count == total_count:
        print("✅ All videos passed quality checks!")
    else:
        print(f"⚠️  {total_count - passed_count} video(s) failed quality checks")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Check video quality and generate QC reports",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Check a single video
  python scripts/check_video_quality.py /path/to/video.mp4
  
  # Check all videos in directory
  python scripts/check_video_quality.py /path/to/directory/
  
  # Check with custom title ID
  python scripts/check_video_quality.py video.mp4 --title-id my_title_001
  
  # Check without saving report
  python scripts/check_video_quality.py video.mp4 --no-save
        """,
    )

    parser.add_argument("path", help="Path to video file or directory")

    parser.add_argument(
        "--title-id", dest="title_id", help="Title ID for the QC report (for single video only)"
    )

    parser.add_argument(
        "--no-save", dest="save_report", action="store_false", help="Do not save QC report to file"
    )

    parser.add_argument(
        "--output-dir",
        dest="output_dir",
        help="Directory to save QC reports (defaults to video directory)",
    )

    parser.add_argument(
        "--pattern", default="*.mp4", help="File pattern for batch processing (default: *.mp4)"
    )

    args = parser.parse_args()

    path = os.path.abspath(args.path)

    if not os.path.exists(path):
        print(f"❌ Error: Path does not exist: {path}")
        return 1

    try:
        if os.path.isfile(path):
            # Check single video
            passed = check_single_video(
                path,
                title_id=args.title_id,
                save_report=args.save_report,
                output_dir=args.output_dir,
            )
            return 0 if passed else 1
        elif os.path.isdir(path):
            # Check directory
            check_directory(path, pattern=args.pattern, save_reports=args.save_report)
            return 0
        else:
            print(f"❌ Error: Invalid path type: {path}")
            return 1

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
