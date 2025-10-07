#!/usr/bin/env python3
"""
Test script for VideoQualityChecker

Tests the quality checker functionality without requiring a full video pipeline.
"""

import os
import sys
import json
import tempfile
from pathlib import Path

# Add src/Python directory to path
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'src', 'Python'))

from Tools.VideoQualityChecker import VideoQualityChecker


def test_quality_checker_basic():
    """Test basic VideoQualityChecker functionality."""
    print("\n" + "="*60)
    print("Testing VideoQualityChecker - Basic Functionality")
    print("="*60)
    
    checker = VideoQualityChecker()
    
    # Test 1: Non-existent file
    print("\n1. Testing with non-existent file...")
    passed, report = checker.check_video_quality(
        "/tmp/nonexistent_video.mp4",
        title_id="test_001",
        save_report=False
    )
    
    if not passed and report['overall_status'] == 'failed':
        print("   ✅ Correctly rejected non-existent file")
        print(f"   Failure reason: {report.get('failure_reason', 'N/A')}")
    else:
        print("   ❌ Should have failed for non-existent file")
        return False
    
    # Test 2: Check report structure
    print("\n2. Testing report structure...")
    required_fields = ['video_path', 'title_id', 'checked_at', 'checks', 'overall_status']
    missing_fields = [f for f in required_fields if f not in report]
    
    if not missing_fields:
        print("   ✅ Report has all required fields")
        print(f"   Fields: {', '.join(required_fields)}")
    else:
        print(f"   ❌ Missing fields: {', '.join(missing_fields)}")
        return False
    
    # Test 3: Check individual tests structure
    print("\n3. Testing individual check structure...")
    required_check_fields = ['name', 'passed', 'details']
    
    if 'checks' in report and report['checks']:
        first_check = list(report['checks'].values())[0]
        missing_check_fields = [f for f in required_check_fields if f not in first_check]
        
        if not missing_check_fields:
            print("   ✅ Check structure is valid")
            print(f"   Total checks: {len(report['checks'])}")
        else:
            print(f"   ❌ Missing check fields: {', '.join(missing_check_fields)}")
            return False
    else:
        print("   ⚠️  No checks in report (expected for failed file check)")
    
    # Test 4: Scoring system
    print("\n4. Testing scoring system...")
    if 'quality_score' in report:
        score = report['quality_score']
        if 0 <= score <= 100:
            print(f"   ✅ Valid quality score: {score}/100")
        else:
            print(f"   ❌ Invalid score range: {score}")
            return False
    else:
        print("   ⚠️  No quality score in report")
    
    print("\n✅ Basic functionality tests passed!")
    return True


def test_quality_checker_with_sample_video():
    """Test with a sample video if available."""
    print("\n" + "="*60)
    print("Testing VideoQualityChecker - Sample Video (if available)")
    print("="*60)
    
    # Try to find a sample video in the repository
    sample_paths = [
        "/home/runner/work/StoryGenerator/StoryGenerator/data/Stories/4_Titles/*/final_video.mp4",
        "/home/runner/work/StoryGenerator/StoryGenerator/src/Generator/final/*/*/*.mp4"
    ]
    
    sample_video = None
    from glob import glob
    
    for pattern in sample_paths:
        matches = glob(pattern)
        if matches:
            sample_video = matches[0]
            break
    
    if not sample_video:
        print("\n⚠️  No sample video found in repository")
        print("   Skipping sample video tests")
        return True
    
    print(f"\n1. Testing with sample video: {sample_video}")
    
    checker = VideoQualityChecker()
    
    with tempfile.TemporaryDirectory() as tmpdir:
        passed, report = checker.check_video_quality(
            sample_video,
            title_id="sample_test",
            save_report=True,
            output_dir=tmpdir
        )
        
        print(f"\n   Overall Status: {report['overall_status']}")
        print(f"   Quality Score: {report['quality_score']}/100")
        print(f"   Checks Passed: {report['checks_passed']}/{report['checks_total']}")
        
        # Print check results
        print("\n   Check Results:")
        for check_name, check_data in report['checks'].items():
            status = "✅" if check_data['passed'] else "❌"
            print(f"   {status} {check_data['name']}: {check_data.get('message', 'N/A')}")
        
        # Verify report was saved
        report_path = report.get('report_path', '')
        if os.path.exists(report_path):
            print(f"\n   ✅ QC report saved to: {report_path}")
            
            # Load and verify JSON is valid
            with open(report_path, 'r') as f:
                loaded_report = json.load(f)
            print(f"   ✅ QC report is valid JSON ({len(json.dumps(loaded_report))} bytes)")
        else:
            print(f"\n   ❌ QC report not saved")
            return False
    
    print("\n✅ Sample video tests passed!")
    return True


def test_quality_thresholds():
    """Test quality threshold checks."""
    print("\n" + "="*60)
    print("Testing VideoQualityChecker - Quality Thresholds")
    print("="*60)
    
    checker = VideoQualityChecker()
    
    # Test threshold values
    print("\n1. Checking quality thresholds...")
    thresholds = {
        "MIN_VIDEO_SIZE_MB": checker.MIN_VIDEO_SIZE_MB,
        "MAX_VIDEO_SIZE_MB": checker.MAX_VIDEO_SIZE_MB,
        "TARGET_RESOLUTION": checker.TARGET_RESOLUTION,
        "MIN_BITRATE_KBPS": checker.MIN_BITRATE_KBPS,
        "TARGET_BITRATE_KBPS": checker.TARGET_BITRATE_KBPS,
        "MIN_AUDIO_BITRATE_KBPS": checker.MIN_AUDIO_BITRATE_KBPS,
        "MIN_DURATION_SECONDS": checker.MIN_DURATION_SECONDS,
        "MAX_DURATION_SECONDS": checker.MAX_DURATION_SECONDS
    }
    
    print("   Configured thresholds:")
    for name, value in thresholds.items():
        print(f"   - {name}: {value}")
    
    # Verify thresholds are reasonable
    if (checker.MIN_VIDEO_SIZE_MB < checker.MAX_VIDEO_SIZE_MB and
        checker.TARGET_RESOLUTION[0] > 0 and
        checker.TARGET_RESOLUTION[1] > 0 and
        checker.MIN_BITRATE_KBPS < checker.TARGET_BITRATE_KBPS and
        checker.MIN_DURATION_SECONDS < checker.MAX_DURATION_SECONDS):
        print("\n   ✅ All thresholds are valid")
    else:
        print("\n   ❌ Some thresholds are invalid")
        return False
    
    print("\n✅ Threshold tests passed!")
    return True


def run_all_tests():
    """Run all tests."""
    print("\n" + "="*60)
    print("VideoQualityChecker Test Suite")
    print("="*60)
    
    tests = [
        ("Basic Functionality", test_quality_checker_basic),
        ("Quality Thresholds", test_quality_thresholds),
        ("Sample Video", test_quality_checker_with_sample_video)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"\n❌ Test '{test_name}' failed with exception: {e}")
            import traceback
            traceback.print_exc()
            results.append((test_name, False))
    
    # Summary
    print("\n" + "="*60)
    print("Test Summary")
    print("="*60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{status}: {test_name}")
    
    print("\n" + "="*60)
    print(f"Total: {passed}/{total} tests passed")
    
    if passed == total:
        print("✅ All tests passed!")
        return 0
    else:
        print("❌ Some tests failed")
        return 1


if __name__ == "__main__":
    sys.exit(run_all_tests())
