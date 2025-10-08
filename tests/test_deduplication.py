#!/usr/bin/env python3
"""
Test suite for content deduplication functionality.

Tests various deduplication strategies and edge cases.
"""

import os
import sys
import json
import tempfile
import shutil
from pathlib import Path

# Add scripts directory to path to import deduplication module
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'scripts'))

from deduplicate_content import (
    normalize_text,
    calculate_content_hash,
    deduplicate_content,
    process_segment
)


def test_normalize_text():
    """Test text normalization."""
    print("\n" + "="*60)
    print("Test 1: Text Normalization")
    print("="*60)
    
    # Test cases
    tests = [
        ("Hello World", "hello world"),
        ("  Spaces  ", "spaces"),
        ("UPPERCASE", "uppercase"),
        ("MiXeD CaSe", "mixed case"),
        ("", ""),
    ]
    
    all_passed = True
    for input_text, expected in tests:
        result = normalize_text(input_text)
        if result == expected:
            print(f"   ✅ '{input_text}' -> '{result}'")
        else:
            print(f"   ❌ '{input_text}' -> '{result}' (expected '{expected}')")
            all_passed = False
    
    return all_passed


def test_content_hash():
    """Test content hash calculation."""
    print("\n" + "="*60)
    print("Test 2: Content Hash Calculation")
    print("="*60)
    
    # Test 1: Same content produces same hash
    content1 = {"title": "Test Story", "text": "This is a test story"}
    content2 = {"title": "Test Story", "text": "This is a test story"}
    
    hash1 = calculate_content_hash(content1)
    hash2 = calculate_content_hash(content2)
    
    if hash1 == hash2:
        print("   ✅ Identical content produces same hash")
    else:
        print("   ❌ Identical content produced different hashes")
        return False
    
    # Test 2: Different content produces different hash
    content3 = {"title": "Different Story", "text": "This is different"}
    hash3 = calculate_content_hash(content3)
    
    if hash1 != hash3:
        print("   ✅ Different content produces different hash")
    else:
        print("   ❌ Different content produced same hash")
        return False
    
    # Test 3: Different titles, same content produces same hash
    content4 = {"title": "Another Title", "text": "This is a test story"}
    hash4 = calculate_content_hash(content4)
    
    if hash1 == hash4:
        print("   ✅ Same content with different title produces same hash")
    else:
        print("   ❌ Should produce same hash for same content with different title")
        return False
    
    # Test 4: Case insensitive (normalized)
    content5 = {"title": "Different", "text": "THIS IS A TEST STORY"}
    hash5 = calculate_content_hash(content5)
    
    if hash1 == hash5:
        print("   ✅ Hash is case-insensitive")
    else:
        print("   ❌ Hash should be case-insensitive")
        return False
    
    return True


def test_exact_id_deduplication():
    """Test deduplication by exact ID match."""
    print("\n" + "="*60)
    print("Test 3: Exact ID Deduplication")
    print("="*60)
    
    content_items = [
        {
            "content_id": "story_001",
            "title": "First Story",
            "text": "Content of first story",
            "viral_score": 80,
            "quality_score": 70
        },
        {
            "content_id": "story_001",  # Duplicate ID
            "title": "First Story Modified",
            "text": "Modified content",
            "viral_score": 60,  # Lower score
            "quality_score": 50
        },
        {
            "content_id": "story_002",
            "title": "Second Story",
            "text": "Content of second story",
            "viral_score": 75,
            "quality_score": 65
        }
    ]
    
    unique_items, report = deduplicate_content(content_items)
    
    # Should keep 2 unique items
    if len(unique_items) == 2:
        print(f"   ✅ Correct number of unique items: {len(unique_items)}")
    else:
        print(f"   ❌ Expected 2 unique items, got {len(unique_items)}")
        return False
    
    # Should remove 1 duplicate
    if report["total_duplicates"] == 1:
        print(f"   ✅ Detected {report['total_duplicates']} duplicate")
    else:
        print(f"   ❌ Expected 1 duplicate, got {report['total_duplicates']}")
        return False
    
    # Should keep the higher scoring item
    kept_story = [item for item in unique_items if item["content_id"] == "story_001"][0]
    if kept_story["viral_score"] == 80:
        print("   ✅ Kept higher scoring duplicate")
    else:
        print("   ❌ Should keep higher scoring duplicate")
        return False
    
    return True


def test_title_deduplication():
    """Test deduplication by fuzzy title match."""
    print("\n" + "="*60)
    print("Test 4: Title Deduplication")
    print("="*60)
    
    content_items = [
        {
            "content_id": "story_001",
            "title": "Amazing Discovery",
            "text": "First version of text",
            "viral_score": 85,
            "quality_score": 75
        },
        {
            "content_id": "story_002",
            "title": "AMAZING DISCOVERY",  # Same title, different case
            "text": "Different text content",
            "viral_score": 70,
            "quality_score": 60
        },
        {
            "content_id": "story_003",
            "title": "Unique Story",
            "text": "Completely different",
            "viral_score": 80,
            "quality_score": 70
        }
    ]
    
    unique_items, report = deduplicate_content(content_items)
    
    # Should keep 2 unique items
    if len(unique_items) == 2:
        print(f"   ✅ Detected title duplicate: {len(unique_items)} unique items")
    else:
        print(f"   ❌ Expected 2 unique items, got {len(unique_items)}")
        return False
    
    # Check duplicate was by title
    if report["duplicates_by_type"]["title_match"] >= 1:
        print(f"   ✅ Detected title match: {report['duplicates_by_type']['title_match']} duplicates")
    else:
        print(f"   ❌ Should detect title match duplicate")
        return False
    
    return True


def test_content_similarity_deduplication():
    """Test deduplication by content similarity."""
    print("\n" + "="*60)
    print("Test 5: Content Similarity Deduplication")
    print("="*60)
    
    long_text = "This is a long story about something interesting. " * 20
    
    content_items = [
        {
            "content_id": "story_001",
            "title": "Story One",
            "text": long_text,
            "viral_score": 90,
            "quality_score": 80
        },
        {
            "content_id": "story_002",
            "title": "Story Two",  # Different title
            "text": long_text,  # Same content
            "viral_score": 75,
            "quality_score": 65
        },
        {
            "content_id": "story_003",
            "title": "Story Three",
            "text": "Completely different content here",
            "viral_score": 85,
            "quality_score": 75
        }
    ]
    
    unique_items, report = deduplicate_content(content_items)
    
    # Should keep 2 unique items
    if len(unique_items) == 2:
        print(f"   ✅ Detected content similarity: {len(unique_items)} unique items")
    else:
        print(f"   ❌ Expected 2 unique items, got {len(unique_items)}")
        return False
    
    # Should keep highest scoring
    if unique_items[0]["viral_score"] + unique_items[0]["quality_score"] >= \
       unique_items[1]["viral_score"] + unique_items[1]["quality_score"]:
        print("   ✅ Kept higher scoring items")
    else:
        print("   ❌ Should keep higher scoring items")
        return False
    
    return True


def test_empty_input():
    """Test handling of empty input."""
    print("\n" + "="*60)
    print("Test 6: Empty Input Handling")
    print("="*60)
    
    content_items = []
    unique_items, report = deduplicate_content(content_items)
    
    if len(unique_items) == 0 and report["total_duplicates"] == 0:
        print("   ✅ Handles empty input correctly")
        return True
    else:
        print("   ❌ Should handle empty input")
        return False


def test_no_duplicates():
    """Test when all items are unique."""
    print("\n" + "="*60)
    print("Test 7: No Duplicates")
    print("="*60)
    
    content_items = [
        {
            "content_id": f"story_{i:03d}",
            "title": f"Unique Story {i}",
            "text": f"Unique content {i}" * 10,
            "viral_score": 70 + i,
            "quality_score": 60 + i
        }
        for i in range(5)
    ]
    
    unique_items, report = deduplicate_content(content_items)
    
    if len(unique_items) == 5 and report["total_duplicates"] == 0:
        print(f"   ✅ All 5 items retained, no false positives")
        print(f"   ✅ Retention rate: {report['retention_rate']}%")
        return True
    else:
        print(f"   ❌ Expected 5 unique items, got {len(unique_items)}")
        return False


def test_integration_with_filesystem():
    """Test integration with file system operations."""
    print("\n" + "="*60)
    print("Test 8: Filesystem Integration")
    print("="*60)
    
    # Create temporary directory structure
    with tempfile.TemporaryDirectory() as tmpdir:
        # Setup directory structure
        scores_dir = Path(tmpdir) / "src" / "Generator" / "scores" / "women" / "18-23"
        scores_dir.mkdir(parents=True, exist_ok=True)
        
        # Create test input file
        test_date = "2025-01-15"
        input_file = scores_dir / f"content_scores_{test_date}.json"
        
        test_data = [
            {
                "content_id": "test_001",
                "title": "Test Story",
                "text": "Test content",
                "viral_score": 80,
                "quality_score": 70
            },
            {
                "content_id": "test_001",  # Duplicate
                "title": "Test Story Duplicate",
                "text": "Different content",
                "viral_score": 60,
                "quality_score": 50
            },
            {
                "content_id": "test_002",
                "title": "Another Story",
                "text": "More content",
                "viral_score": 85,
                "quality_score": 75
            }
        ]
        
        with open(input_file, 'w') as f:
            json.dump(test_data, f)
        
        # Change to temp directory
        original_dir = os.getcwd()
        try:
            os.chdir(tmpdir)
            
            # Run process_segment
            result = process_segment("women", "18-23", test_date)
            
            if result["status"] == "success":
                print(f"   ✅ Process completed successfully")
            else:
                print(f"   ❌ Process failed: {result.get('reason', 'unknown')}")
                return False
            
            # Check output files exist
            output_file = scores_dir / f"content_deduped_{test_date}.json"
            report_file = scores_dir / f"dedup_report_{test_date}.json"
            
            if output_file.exists():
                print(f"   ✅ Output file created: {output_file.name}")
                
                # Verify output content
                with open(output_file, 'r') as f:
                    output_data = json.load(f)
                
                if len(output_data) == 2:
                    print(f"   ✅ Output contains correct number of items: {len(output_data)}")
                else:
                    print(f"   ❌ Expected 2 items, got {len(output_data)}")
                    return False
            else:
                print(f"   ❌ Output file not created")
                return False
            
            if report_file.exists():
                print(f"   ✅ Report file created: {report_file.name}")
                
                # Verify report structure
                with open(report_file, 'r') as f:
                    report = json.load(f)
                
                required_fields = [
                    "timestamp", "total_input_items", "unique_items",
                    "total_duplicates", "duplicates_by_type", "retention_rate"
                ]
                
                missing_fields = [f for f in required_fields if f not in report]
                if not missing_fields:
                    print(f"   ✅ Report has all required fields")
                else:
                    print(f"   ❌ Missing fields in report: {missing_fields}")
                    return False
            else:
                print(f"   ❌ Report file not created")
                return False
            
        finally:
            os.chdir(original_dir)
    
    return True


def test_report_structure():
    """Test deduplication report structure."""
    print("\n" + "="*60)
    print("Test 9: Report Structure")
    print("="*60)
    
    content_items = [
        {
            "content_id": "story_001",
            "title": "Story",
            "text": "Content",
            "viral_score": 80,
            "quality_score": 70
        }
    ]
    
    unique_items, report = deduplicate_content(content_items)
    
    # Check required fields
    required_fields = [
        "timestamp",
        "total_input_items",
        "unique_items",
        "total_duplicates",
        "duplicates_by_type",
        "retention_rate"
    ]
    
    missing_fields = [f for f in required_fields if f not in report]
    
    if not missing_fields:
        print(f"   ✅ Report has all required fields")
    else:
        print(f"   ❌ Missing fields: {missing_fields}")
        return False
    
    # Check duplicates_by_type structure
    expected_types = ["exact_id", "title_match", "content_similarity"]
    missing_types = [t for t in expected_types if t not in report["duplicates_by_type"]]
    
    if not missing_types:
        print(f"   ✅ Duplicates breakdown by type present")
    else:
        print(f"   ❌ Missing duplicate types: {missing_types}")
        return False
    
    # Check retention rate is percentage
    if 0 <= report["retention_rate"] <= 100:
        print(f"   ✅ Retention rate is valid: {report['retention_rate']}%")
    else:
        print(f"   ❌ Invalid retention rate: {report['retention_rate']}")
        return False
    
    return True


def main():
    """Run all tests."""
    print("\n" + "="*80)
    print("CONTENT DEDUPLICATION - COMPREHENSIVE TESTS")
    print("="*80)
    
    results = []
    
    # Run all tests
    results.append(("Text Normalization", test_normalize_text()))
    results.append(("Content Hash", test_content_hash()))
    results.append(("Exact ID Deduplication", test_exact_id_deduplication()))
    results.append(("Title Deduplication", test_title_deduplication()))
    results.append(("Content Similarity", test_content_similarity_deduplication()))
    results.append(("Empty Input", test_empty_input()))
    results.append(("No Duplicates", test_no_duplicates()))
    results.append(("Filesystem Integration", test_integration_with_filesystem()))
    results.append(("Report Structure", test_report_structure()))
    
    # Print summary
    print("\n" + "="*80)
    print("TEST SUMMARY")
    print("="*80)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {test_name}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed!")
    else:
        print(f"\n⚠️  {total - passed} test(s) failed")
    
    print("="*80 + "\n")
    
    return passed == total


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
