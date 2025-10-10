#!/usr/bin/env python3
"""
Tests for VideoVariantSelector

Tests the variant selection functionality without requiring real video files.
"""

import os
import sys
import json
import tempfile
from pathlib import Path

# Add src/Python directory to path
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'src', 'Python'))

from Tools.VideoVariantSelector import VideoVariantSelector


def test_basic_functionality():
    """Test basic VideoVariantSelector functionality."""
    print("\n" + "="*60)
    print("TEST: VideoVariantSelector - Basic Functionality")
    print("="*60)
    
    try:
        selector = VideoVariantSelector()
        
        # Test 1: Initialization
        print("\n1. Testing initialization...")
        assert selector is not None
        assert hasattr(selector, 'select_best_variant')
        assert hasattr(selector, 'batch_select_variants')
        print("   ✅ Selector initialized successfully")
        
        # Test 2: Empty variants list
        print("\n2. Testing empty variants list...")
        try:
            selector.select_best_variant([], save_report=False)
            print("   ❌ Should have raised ValueError for empty list")
            return False
        except ValueError as e:
            print(f"   ✅ Correctly raised ValueError: {e}")
        
        # Test 3: Manual override with valid index
        print("\n3. Testing manual override...")
        with tempfile.NamedTemporaryFile(suffix='.mp4', delete=False) as tmp:
            tmp_path = tmp.name
            tmp.write(b'fake video data')
        
        try:
            variants = [tmp_path]
            selected, report = selector.select_best_variant(
                variants,
                shot_id="test_shot",
                save_report=False,
                manual_override=0
            )
            
            assert selected == tmp_path
            assert report['manual_override'] == True
            assert report['selected_index'] == 0
            print("   ✅ Manual override working correctly")
        finally:
            os.unlink(tmp_path)
        
        # Test 4: Manual override with invalid index
        print("\n4. Testing invalid manual override...")
        try:
            selector.select_best_variant(
                ['variant1.mp4', 'variant2.mp4'],
                save_report=False,
                manual_override=5
            )
            print("   ❌ Should have raised ValueError for invalid index")
            return False
        except ValueError as e:
            print(f"   ✅ Correctly raised ValueError: {e}")
        
        print("\n" + "="*60)
        print("✅ All basic functionality tests passed")
        print("="*60)
        return True
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_quality_metrics():
    """Test quality metric calculations."""
    print("\n" + "="*60)
    print("TEST: Quality Metrics Calculation")
    print("="*60)
    
    try:
        selector = VideoVariantSelector()
        
        # Test overall score calculation
        print("\n1. Testing overall score calculation...")
        
        test_cases = [
            (1.0, 1.0, 0.0, 100.0),  # Perfect quality
            (0.8, 0.8, 0.1, 83.0),   # Good quality
            (0.6, 0.7, 0.2, 69.5),   # Acceptable quality (adjusted)
            (0.3, 0.4, 0.5, 39.5),   # Poor quality (adjusted)
        ]
        
        for motion, temporal, artifacts, expected in test_cases:
            score = selector._calculate_overall_score(motion, temporal, artifacts)
            # Allow small floating point differences
            assert abs(score - expected) < 1.0, f"Expected ~{expected}, got {score}"
            print(f"   ✅ Motion={motion}, Temporal={temporal}, Artifacts={artifacts} → Score={score}")
        
        print("\n" + "="*60)
        print("✅ All quality metrics tests passed")
        print("="*60)
        return True
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_report_structure():
    """Test selection report structure."""
    print("\n" + "="*60)
    print("TEST: Selection Report Structure")
    print("="*60)
    
    try:
        selector = VideoVariantSelector()
        
        # Create temporary video files
        tmp_files = []
        for i in range(2):
            tmp = tempfile.NamedTemporaryFile(suffix='.mp4', delete=False)
            tmp.write(b'fake video data ' * 100)
            tmp.close()
            tmp_files.append(tmp.name)
        
        try:
            # Test report structure
            print("\n1. Testing report structure with manual override...")
            selected, report = selector.select_best_variant(
                tmp_files,
                shot_id="test_shot_001",
                save_report=False,
                manual_override=0
            )
            
            # Check required fields
            required_fields = [
                'shot_id',
                'selected_at',
                'total_variants',
                'analyzed_variants',
                'selected_variant',
                'selected_index',
                'selection_reason',
                'manual_override'
            ]
            
            missing = [f for f in required_fields if f not in report]
            assert not missing, f"Missing fields: {missing}"
            print(f"   ✅ Report has all required fields")
            
            # Check field values
            assert report['shot_id'] == 'test_shot_001'
            assert report['total_variants'] == 2
            assert report['selected_index'] == 0
            assert report['manual_override'] == True
            print(f"   ✅ Report field values correct")
            
            # Test JSON serialization
            print("\n2. Testing JSON serialization...")
            json_str = json.dumps(report, indent=2)
            assert len(json_str) > 0
            deserialized = json.loads(json_str)
            assert deserialized['shot_id'] == report['shot_id']
            print(f"   ✅ Report serializes to JSON correctly")
            
            print("\n" + "="*60)
            print("✅ All report structure tests passed")
            print("="*60)
            return True
            
        finally:
            # Cleanup
            for tmp_file in tmp_files:
                os.unlink(tmp_file)
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_batch_selection():
    """Test batch variant selection."""
    print("\n" + "="*60)
    print("TEST: Batch Variant Selection")
    print("="*60)
    
    try:
        selector = VideoVariantSelector()
        
        # Create temporary video files
        print("\n1. Creating test video files...")
        tmp_files = []
        for i in range(4):
            tmp = tempfile.NamedTemporaryFile(suffix='.mp4', delete=False)
            tmp.write(b'fake video data ' * 100)
            tmp.close()
            tmp_files.append(tmp.name)
        
        try:
            # Create variant groups
            variant_groups = {
                'shot_001': [tmp_files[0], tmp_files[1]],
                'shot_002': [tmp_files[2], tmp_files[3]]
            }
            
            print(f"   ✅ Created {len(tmp_files)} test videos")
            
            # Test batch selection
            print("\n2. Testing batch selection...")
            results = selector.batch_select_variants(
                variant_groups,
                save_reports=False
            )
            
            assert len(results) == 2, f"Expected 2 results, got {len(results)}"
            assert 'shot_001' in results
            assert 'shot_002' in results
            
            for shot_id, (selected_path, report) in results.items():
                assert os.path.exists(selected_path)
                assert report['shot_id'] == shot_id
                print(f"   ✅ {shot_id}: Selected {os.path.basename(selected_path)}")
            
            print("\n" + "="*60)
            print("✅ All batch selection tests passed")
            print("="*60)
            return True
            
        finally:
            # Cleanup
            for tmp_file in tmp_files:
                if os.path.exists(tmp_file):
                    os.unlink(tmp_file)
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def run_all_tests():
    """Run all tests."""
    print("\n" + "="*70)
    print("VideoVariantSelector Test Suite")
    print("="*70)
    
    tests = [
        ("Basic Functionality", test_basic_functionality),
        ("Quality Metrics", test_quality_metrics),
        ("Report Structure", test_report_structure),
        ("Batch Selection", test_batch_selection)
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n{'='*70}")
        print(f"Running: {test_name}")
        print(f"{'='*70}")
        
        try:
            passed = test_func()
            results.append((test_name, passed))
        except Exception as e:
            print(f"❌ {test_name} failed with exception: {e}")
            results.append((test_name, False))
    
    # Print summary
    print("\n" + "="*70)
    print("Test Summary")
    print("="*70)
    
    for test_name, passed in results:
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"{status}: {test_name}")
    
    passed_count = sum(1 for _, passed in results if passed)
    total_count = len(results)
    
    print(f"\n{'─'*70}")
    print(f"Total: {passed_count}/{total_count} tests passed")
    
    if passed_count == total_count:
        print("✅ All tests passed!")
        return True
    else:
        print(f"❌ {total_count - passed_count} test(s) failed")
        return False


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
