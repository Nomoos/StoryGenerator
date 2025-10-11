#!/usr/bin/env python3
"""
Test for final video export functionality.
Tests the export to /final/{segment}/{age}/{title_id}.mp4 structure.
"""

import os
import sys
import json
import tempfile
import shutil
from pathlib import Path

# Add src/Python directory to path
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'src', 'Python'))

from Models.StoryIdea import StoryIdea
from Tools.Utils import (
    get_segment_from_gender,
    get_age_group_from_potencial,
    generate_title_id,
    get_final_export_path
)


def test_segment_from_gender():
    """Test gender to segment conversion."""
    print("\n" + "="*60)
    print("Testing segment extraction from gender")
    print("="*60)
    
    test_cases = [
        ('F', 'women'),
        ('Female', 'women'),
        ('woman', 'women'),
        ('M', 'men'),
        ('Male', 'men'),
        ('man', 'men'),
        ('', 'women'),  # Default
        (None, 'women'),  # Default
    ]
    
    all_passed = True
    for gender, expected in test_cases:
        result = get_segment_from_gender(gender)
        status = "✅" if result == expected else "❌"
        print(f"  {status} Gender '{gender}' -> '{result}' (expected '{expected}')")
        if result != expected:
            all_passed = False
    
    return all_passed


def test_age_group_extraction():
    """Test age group extraction from potencial."""
    print("\n" + "="*60)
    print("Testing age group extraction")
    print("="*60)
    
    # Test case 1: Valid potencial with clear winner
    potencial1 = {
        "age_groups": {
            "10_15": 20,
            "15_20": 30,
            "20_25": 80,  # Highest
            "25_30": 40,
            "30_50": 10,
            "50_70": 5
        }
    }
    result1 = get_age_group_from_potencial(potencial1)
    print(f"  Test 1: {result1} (expected '18-23') {'✅' if result1 == '18-23' else '❌'}")
    
    # Test case 2: Empty potencial
    result2 = get_age_group_from_potencial({})
    print(f"  Test 2: {result2} (expected '18-23' default) {'✅' if result2 == '18-23' else '❌'}")
    
    # Test case 3: None potencial
    result3 = get_age_group_from_potencial(None)
    print(f"  Test 3: {result3} (expected '18-23' default) {'✅' if result3 == '18-23' else '❌'}")
    
    return result1 == '18-23' and result2 == '18-23' and result3 == '18-23'


def test_title_id_generation():
    """Test title ID generation."""
    print("\n" + "="*60)
    print("Testing title ID generation")
    print("="*60)
    
    # Test consistency
    title = "My Amazing Story"
    id1 = generate_title_id(title)
    id2 = generate_title_id(title)
    
    print(f"  Test 1: ID length = {len(id1)} (expected 8) {'✅' if len(id1) == 8 else '❌'}")
    print(f"  Test 2: Consistency {id1} == {id2} {'✅' if id1 == id2 else '❌'}")
    
    # Test uniqueness
    title2 = "Another Story"
    id3 = generate_title_id(title2)
    print(f"  Test 3: Uniqueness {id1} != {id3} {'✅' if id1 != id3 else '❌'}")
    
    return len(id1) == 8 and id1 == id2 and id1 != id3


def test_export_path_generation():
    """Test export path generation."""
    print("\n" + "="*60)
    print("Testing export path generation")
    print("="*60)
    
    story_title = "Test Story"
    segment = "women"
    age_group = "18-23"
    filename = "test123.mp4"
    
    path = get_final_export_path(story_title, segment, age_group, filename)
    print(f"  Generated path: {path}")
    
    # Check path components
    checks = [
        ('/data/final/' in path or '\\data\\final\\' in path, "Contains /data/final/"),
        (segment in path, f"Contains segment '{segment}'"),
        (age_group in path, f"Contains age group '{age_group}'"),
        (filename in path, f"Contains filename '{filename}'"),
    ]
    
    all_passed = True
    for check, description in checks:
        status = "✅" if check else "❌"
        print(f"  {status} {description}")
        if not check:
            all_passed = False
    
    return all_passed


def test_story_idea_integration():
    """Test integration with StoryIdea object."""
    print("\n" + "="*60)
    print("Testing StoryIdea integration")
    print("="*60)
    
    # Create a test StoryIdea
    story = StoryIdea(
        story_title="Test Integration Story",
        narrator_gender="F",
        tone="dramatic",
        theme="adventure",
        potencial={
            "age_groups": {
                "10_15": 10,
                "15_20": 20,
                "20_25": 90,  # Target age
                "25_30": 30,
                "30_50": 15,
                "50_70": 5
            }
        }
    )
    
    # Extract information
    segment = get_segment_from_gender(story.narrator_gender)
    age_group = get_age_group_from_potencial(story.potencial)
    title_id = generate_title_id(story.story_title)
    
    print(f"  Story Title: {story.story_title}")
    print(f"  Segment: {segment} (expected 'women') {'✅' if segment == 'women' else '❌'}")
    print(f"  Age Group: {age_group} (expected '18-23') {'✅' if age_group == '18-23' else '❌'}")
    print(f"  Title ID: {title_id} (8 chars) {'✅' if len(title_id) == 8 else '❌'}")
    
    # Test export path generation
    video_path = get_final_export_path(story.story_title, segment, age_group, f"{title_id}.mp4")
    print(f"  Video path: {video_path}")
    
    return segment == 'women' and age_group == '18-23' and len(title_id) == 8


def main():
    """Run all tests."""
    print("\n" + "="*60)
    print("FINAL EXPORT - FUNCTIONALITY TESTS")
    print("="*60)
    
    results = []
    
    # Run tests
    results.append(("Segment from Gender", test_segment_from_gender()))
    results.append(("Age Group Extraction", test_age_group_extraction()))
    results.append(("Title ID Generation", test_title_id_generation()))
    results.append(("Export Path Generation", test_export_path_generation()))
    results.append(("StoryIdea Integration", test_story_idea_integration()))
    
    # Print summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {test_name}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    print("="*60 + "\n")
    
    return passed == total


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
