#!/usr/bin/env python3
"""
Example demonstration of VideoQualityChecker

This script demonstrates how the quality checker works and what
kind of reports it generates, even without a real video file.
"""

import os
import sys
import json
from datetime import datetime

# Add src/Python directory to path
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'src', 'Python'))

from Tools.VideoQualityChecker import VideoQualityChecker


def create_mock_qc_report():
    """Create a mock QC report to demonstrate the structure."""
    return {
        "video_path": "/final/men/25-34/my_story_title_qc.mp4",
        "title_id": "my_story_title",
        "checked_at": datetime.now().isoformat(),
        "checks": {
            "file_properties": {
                "name": "File Properties",
                "passed": True,
                "details": {
                    "file_exists": True,
                    "size_bytes": 15728640,
                    "size_mb": 15.0
                },
                "message": "File exists (15.0 MB)"
            },
            "codec_format": {
                "name": "Codec & Format",
                "passed": True,
                "details": {
                    "format": "mov,mp4,m4a,3gp,3g2,mj2",
                    "format_long": "QuickTime / MOV",
                    "video_codec": "h264",
                    "pixel_format": "yuv420p",
                    "audio_codec": "aac"
                },
                "message": "Using recommended codec: h264"
            },
            "resolution_legibility": {
                "name": "Resolution & Legibility",
                "passed": True,
                "details": {
                    "width": 1080,
                    "height": 1920,
                    "resolution": "1080x1920",
                    "aspect_ratio": 0.56,
                    "fps": 30.0,
                    "fps_status": "good"
                },
                "message": "Perfect resolution: 1080x1920"
            },
            "bitrate": {
                "name": "Bitrate Analysis",
                "passed": True,
                "details": {
                    "overall_bitrate_bps": 2097152,
                    "overall_bitrate_kbps": 2097.15,
                    "video_bitrate_bps": 1900544,
                    "video_bitrate_kbps": 1900.54,
                    "audio_bitrate_bps": 196608,
                    "audio_bitrate_kbps": 192.0
                },
                "message": "Good video bitrate: 1900.54 kbps"
            },
            "file_size": {
                "name": "File Size",
                "passed": True,
                "details": {
                    "size_bytes": 15728640,
                    "size_mb": 15.0,
                    "min_size_mb": 1.0,
                    "max_size_mb": 100.0
                },
                "message": "File size acceptable: 15.0 MB"
            },
            "av_sync": {
                "name": "Audio/Video Sync",
                "passed": True,
                "details": {
                    "video_duration": 60.05,
                    "audio_duration": 60.03,
                    "format_duration": 60.05,
                    "sync_difference": 0.02
                },
                "message": "Audio/video in sync (diff: 0.02s)"
            },
            "duration": {
                "name": "Duration",
                "passed": True,
                "details": {
                    "duration_seconds": 60.05,
                    "duration_formatted": "1m 0s",
                    "min_duration": 5,
                    "max_duration": 180
                },
                "message": "Duration acceptable: 60.05s"
            }
        },
        "overall_status": "passed",
        "checks_passed": 7,
        "checks_total": 7,
        "pass_rate": 100.0,
        "quality_score": 100,
        "report_path": "/final/men/25-34/my_story_title_qc.json"
    }


def create_mock_failed_report():
    """Create a mock QC report with failures to demonstrate issues."""
    return {
        "video_path": "/final/women/18-24/low_quality_video.mp4",
        "title_id": "low_quality_video",
        "checked_at": datetime.now().isoformat(),
        "checks": {
            "file_properties": {
                "name": "File Properties",
                "passed": True,
                "details": {
                    "file_exists": True,
                    "size_bytes": 524288,
                    "size_mb": 0.5
                },
                "message": "File exists (0.5 MB)"
            },
            "codec_format": {
                "name": "Codec & Format",
                "passed": False,
                "details": {
                    "format": "avi",
                    "video_codec": "mjpeg",
                    "audio_codec": "pcm_s16le"
                },
                "message": "Non-standard codec: mjpeg (expected h264)"
            },
            "resolution_legibility": {
                "name": "Resolution & Legibility",
                "passed": False,
                "details": {
                    "width": 640,
                    "height": 480,
                    "resolution": "640x480",
                    "aspect_ratio": 1.33,
                    "fps": 15.0,
                    "fps_status": "low",
                    "fps_warning": "Low frame rate: 15 fps"
                },
                "message": "Low resolution: 640x480 (expected 1080x1920)"
            },
            "bitrate": {
                "name": "Bitrate Analysis",
                "passed": False,
                "details": {
                    "overall_bitrate_bps": 768000,
                    "overall_bitrate_kbps": 768.0,
                    "video_bitrate_bps": 640000,
                    "video_bitrate_kbps": 640.0,
                    "audio_bitrate_bps": 128000,
                    "audio_bitrate_kbps": 128.0
                },
                "message": "Low video bitrate: 640.0 kbps (min: 2000 kbps)"
            },
            "file_size": {
                "name": "File Size",
                "passed": False,
                "details": {
                    "size_bytes": 524288,
                    "size_mb": 0.5,
                    "min_size_mb": 1.0,
                    "max_size_mb": 100.0
                },
                "message": "File too small: 0.5 MB (min: 1.0 MB)"
            },
            "av_sync": {
                "name": "Audio/Video Sync",
                "passed": False,
                "details": {
                    "video_duration": 58.5,
                    "audio_duration": 60.0,
                    "format_duration": 60.0,
                    "sync_difference": 1.5
                },
                "message": "Audio/video out of sync (diff: 1.5s)"
            },
            "duration": {
                "name": "Duration",
                "passed": True,
                "details": {
                    "duration_seconds": 60.0,
                    "duration_formatted": "1m 0s",
                    "min_duration": 5,
                    "max_duration": 180
                },
                "message": "Duration acceptable: 60.0s"
            }
        },
        "overall_status": "failed",
        "checks_passed": 2,
        "checks_total": 7,
        "pass_rate": 28.6,
        "quality_score": 42,
        "report_path": "/final/women/18-24/low_quality_video_qc.json"
    }


def print_qc_report(report: dict, title: str):
    """Print a formatted QC report."""
    print(f"\n{'='*70}")
    print(f"{title}")
    print(f"{'='*70}")
    
    print(f"\nVideo: {report['video_path']}")
    print(f"Title ID: {report['title_id']}")
    print(f"Checked: {report['checked_at']}")
    
    print(f"\n📊 Overall Results:")
    print(f"{'─'*70}")
    status_emoji = "✅" if report['overall_status'] == 'passed' else "❌"
    print(f"{status_emoji} Status: {report['overall_status'].upper()}")
    print(f"   Quality Score: {report['quality_score']}/100")
    print(f"   Checks Passed: {report['checks_passed']}/{report['checks_total']}")
    print(f"   Pass Rate: {report['pass_rate']}%")
    
    print(f"\n📋 Individual Checks:")
    print(f"{'─'*70}")
    
    for check_name, check_data in report['checks'].items():
        status = "✅" if check_data['passed'] else "❌"
        print(f"{status} {check_data['name']}")
        print(f"   {check_data['message']}")
        
        # Show key details
        details = check_data['details']
        if 'size_mb' in details:
            print(f"   └─ File Size: {details['size_mb']} MB")
        if 'resolution' in details:
            print(f"   └─ Resolution: {details['resolution']}")
        if 'video_codec' in details:
            print(f"   └─ Codec: {details['video_codec']}")
        if 'video_bitrate_kbps' in details:
            print(f"   └─ Bitrate: {details['video_bitrate_kbps']} kbps")
        if 'duration_seconds' in details:
            print(f"   └─ Duration: {details['duration_seconds']}s")
        
        print()
    
    if 'report_path' in report:
        print(f"📄 QC Report: {report['report_path']}")


def demonstrate_quality_checker():
    """Demonstrate the quality checker functionality."""
    print("\n" + "="*70)
    print("VideoQualityChecker Demonstration")
    print("="*70)
    
    print("\nThis demonstration shows how the VideoQualityChecker analyzes videos")
    print("and generates comprehensive quality control reports.")
    
    print("\n" + "─"*70)
    print("Quality Checks Performed:")
    print("─"*70)
    
    checks = [
        "1. File Properties - Verifies file exists and has valid size",
        "2. Codec & Format - Checks for recommended H.264 video codec",
        "3. Resolution & Legibility - Validates 1080x1920 vertical format",
        "4. Bitrate Analysis - Ensures sufficient video/audio quality",
        "5. File Size - Validates reasonable file size for duration",
        "6. A/V Sync - Checks audio/video synchronization",
        "7. Duration - Validates video length is within acceptable range"
    ]
    
    for check in checks:
        print(f"   {check}")
    
    # Show example of perfect video
    print("\n" + "="*70)
    print("Example 1: High-Quality Video (Perfect Score)")
    print("="*70)
    
    perfect_report = create_mock_qc_report()
    print_qc_report(perfect_report, "Quality Report")
    
    # Show example JSON structure
    print(f"\n{'─'*70}")
    print("Sample QC Report JSON Structure:")
    print(f"{'─'*70}")
    print(json.dumps(perfect_report, indent=2)[:500] + "...")
    
    # Show example of problematic video
    print("\n\n" + "="*70)
    print("Example 2: Low-Quality Video (Issues Detected)")
    print("="*70)
    
    failed_report = create_mock_failed_report()
    print_qc_report(failed_report, "Quality Report")
    
    # Show how to use it
    print("\n" + "="*70)
    print("How to Use the Quality Checker")
    print("="*70)
    
    usage_examples = """
1. Automatic Quality Check (Integrated with VideoCompositor):
   
   from Generators.GVideoCompositor import VideoCompositor
   
   compositor = VideoCompositor(perform_quality_check=True)
   video_path = compositor.compose_final_video(story_idea)
   # Quality check runs automatically and saves QC report
   
2. Manual Quality Check (Standalone Script):
   
   # Check a single video
   python scripts/check_video_quality.py /path/to/video.mp4
   
   # Check all videos in a directory
   python scripts/check_video_quality.py /final/men/25-34/
   
   # Check with custom title ID
   python scripts/check_video_quality.py video.mp4 --title-id my_title_001
   
3. Programmatic Usage:
   
   from Tools.VideoQualityChecker import VideoQualityChecker
   
   checker = VideoQualityChecker()
   passed, report = checker.check_video_quality(
       video_path="/path/to/video.mp4",
       title_id="my_title",
       save_report=True
   )
   
   print(f"Quality Score: {report['quality_score']}/100")
   print(f"Checks Passed: {report['checks_passed']}/{report['checks_total']}")
"""
    
    print(usage_examples)
    
    # Show QC report file location
    print("="*70)
    print("QC Report File Location")
    print("="*70)
    
    print("""
Quality check reports are saved as JSON files with the naming pattern:
    {title_id}_qc.json

Default locations:
    - Same directory as the video file
    - /final/{segment}/{age}/{title_id}_qc.json (for organized content)
    
The report contains:
    - Timestamp of quality check
    - Individual check results with pass/fail status
    - Detailed metrics (codec, bitrate, resolution, etc.)
    - Overall quality score (0-100)
    - Recommendations for improvements
""")
    
    print("="*70)
    print("✅ Demonstration Complete")
    print("="*70)
    print("\nThe quality checker is now integrated into the video pipeline!")
    print("All final videos will be automatically checked for quality issues.")


if __name__ == "__main__":
    try:
        demonstrate_quality_checker()
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted by user")
        sys.exit(130)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
