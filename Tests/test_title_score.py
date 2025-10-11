#!/usr/bin/env python3
"""
Tests for title scoring functionality.
"""

import sys
import os
import json
import tempfile
import shutil
from pathlib import Path
from datetime import datetime


def test_imports():
    """Test that title_score module can be imported."""
    print("=" * 60)
    print("TEST: Module Imports")
    print("=" * 60)
    
    try:
        import title_score
        print("✅ title_score module imported successfully")
        return True
    except ImportError as e:
        print(f"❌ Import failed: {e}")
        return False


def test_load_scoring_config():
    """Test loading scoring configuration."""
    print("\n" + "=" * 60)
    print("TEST: Load Scoring Config")
    print("=" * 60)
    
    try:
        import title_score
        config = title_score.load_scoring_config()
        
        # Verify key sections exist
        assert 'title_scoring' in config, "Missing title_scoring section"
        assert 'criteria' in config['title_scoring'], "Missing criteria section"
        assert 'prompt_template' in config, "Missing prompt_template"
        
        print(f"✅ Loaded scoring config with {len(config['title_scoring']['criteria'])} criteria")
        return True
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False


def test_score_title_locally():
    """Test local title scoring functionality."""
    print("\n" + "=" * 60)
    print("TEST: Local Title Scoring")
    print("=" * 60)
    
    try:
        import title_score
        
        config = title_score.load_scoring_config()
        
        # Test various title types
        test_titles = [
            ("Why You Should Never Do This", "women", "18-23"),
            ("5 Ways to Improve Your Life", "men", "25-29"),
            ("The Secret Truth They Don't Want You to Know", "women", "20-24"),
            ("How to Build Your Career in Tech", "men", "24-30"),
            ("A", "women", "10-13"),  # Too short
            ("This is an extremely long title that goes on and on and will definitely be too long for social media platforms", "men", "30-34"),  # Too long
        ]
        
        for title, gender, age in test_titles:
            result = title_score.score_title_locally(title, gender, age, config)
            
            # Verify result structure
            assert 'scores' in result, "Missing scores"
            assert 'overall_score' in result, "Missing overall_score"
            assert 'rationale' in result, "Missing rationale"
            assert 'voice_recommendation' in result, "Missing voice_recommendation"
            
            # Verify score components
            assert 'hook_strength' in result['scores']
            assert 'clarity' in result['scores']
            assert 'relevance' in result['scores']
            assert 'length_format' in result['scores']
            assert 'viral_potential' in result['scores']
            
            # Verify score ranges
            assert 0 <= result['overall_score'] <= 100
            for score in result['scores'].values():
                assert 0 <= score <= 100
            
            # Verify voice recommendation
            assert result['voice_recommendation']['gender'] in ['M', 'F']
            assert len(result['voice_recommendation']['reasoning']) > 0
            
            print(f"  ✓ '{title[:50]}...' scored: {result['overall_score']:.1f}/100")
        
        print("✅ Local scoring works correctly")
        return True
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_voice_recommendation():
    """Test voice recommendation logic."""
    print("\n" + "=" * 60)
    print("TEST: Voice Recommendation")
    print("=" * 60)
    
    try:
        import title_score
        
        test_cases = [
            ("The Mystery of the Ancient Tomb", "women", "20-24", "M"),  # Mystery -> Male
            ("Beauty Tips for Summer", "women", "18-23", "F"),  # Beauty -> Female
            ("Tech Hacks You Need", "men", "25-29", "M"),  # Tech -> Male
            ("How I Changed My Life", "women", "20-24", "F"),  # General women -> Female
            ("How I Changed My Life", "men", "25-29", "M"),  # General men -> Male
        ]
        
        for title, gender, age, expected_voice in test_cases:
            result = title_score.recommend_voice(title, gender, age)
            assert result == expected_voice, f"Expected {expected_voice} for '{title}', got {result}"
            print(f"  ✓ '{title}' -> {result}")
        
        print("✅ Voice recommendations work correctly")
        return True
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_extract_title_from_file():
    """Test extracting titles from different file types."""
    print("\n" + "=" * 60)
    print("TEST: Extract Title from File")
    print("=" * 60)
    
    try:
        import title_score
        
        # Create temporary directory
        with tempfile.TemporaryDirectory() as tmpdir:
            tmppath = Path(tmpdir)
            
            # Test JSON file
            json_file = tmppath / "test.json"
            with open(json_file, 'w') as f:
                json.dump({'title': 'Test Title from JSON'}, f)
            
            title = title_score.extract_title_from_file(json_file)
            assert title == 'Test Title from JSON', f"Expected 'Test Title from JSON', got {title}"
            print("  ✓ Extracted from JSON file")
            
            # Test text file
            txt_file = tmppath / "test.txt"
            with open(txt_file, 'w') as f:
                f.write('Test Title from Text')
            
            title = title_score.extract_title_from_file(txt_file)
            assert title == 'Test Title from Text', f"Expected 'Test Title from Text', got {title}"
            print("  ✓ Extracted from text file")
            
            # Test idea.json file
            idea_dir = tmppath / "some_story"
            idea_dir.mkdir()
            idea_file = idea_dir / "idea.json"
            with open(idea_file, 'w') as f:
                json.dump({'story_title': 'Story Title from Idea'}, f)
            
            title = title_score.extract_title_from_file(idea_file)
            assert title == 'Story Title from Idea', f"Expected 'Story Title from Idea', got {title}"
            print("  ✓ Extracted from idea.json file")
        
        print("✅ Title extraction works correctly")
        return True
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_end_to_end_scoring():
    """Test end-to-end scoring with mock data."""
    print("\n" + "=" * 60)
    print("TEST: End-to-End Scoring")
    print("=" * 60)
    
    try:
        import title_score
        
        # Create temporary directory structure
        with tempfile.TemporaryDirectory() as tmpdir:
            tmppath = Path(tmpdir)
            
            # Create directory structure
            titles_dir = tmppath / "titles" / "women" / "18-23"
            scores_dir = tmppath / "scores"
            voices_dir = tmppath / "voices" / "choice"
            
            titles_dir.mkdir(parents=True)
            
            # Create some test title files
            test_titles = [
                "Why Everyone Is Talking About This",
                "5 Secrets You Need to Know",
                "How I Changed My Life in 30 Days",
                "The Truth About Social Media",
                "What Nobody Tells You About Success"
            ]
            
            for i, title_text in enumerate(test_titles):
                # Create as JSON files
                title_file = titles_dir / f"title_{i+1}.json"
                with open(title_file, 'w') as f:
                    json.dump({'title': title_text}, f)
            
            # Load configs
            config = title_score.load_scoring_config()
            
            # Score titles for this segment
            scored, top = title_score.score_titles_for_segment(
                tmppath / "titles",
                scores_dir,
                voices_dir,
                "women",
                "18-23",
                config
            )
            
            assert scored == len(test_titles), f"Expected {len(test_titles)} scored, got {scored}"
            assert top == min(5, len(test_titles)), f"Expected {min(5, len(test_titles))} top titles, got {top}"
            
            # Verify output files exist
            date_str = datetime.now().strftime("%Y%m%d")
            scores_file = scores_dir / "women" / "18-23" / f"{date_str}_title_scores.json"
            voices_file = voices_dir / "women" / "18-23" / f"{date_str}_voice_notes.md"
            
            assert scores_file.exists(), f"Scores file not created: {scores_file}"
            assert voices_file.exists(), f"Voice notes file not created: {voices_file}"
            
            # Verify scores file content
            with open(scores_file, 'r') as f:
                scores_data = json.load(f)
            
            assert 'metadata' in scores_data
            assert 'scores' in scores_data
            assert len(scores_data['scores']) == len(test_titles)
            
            # Verify voice notes file content
            with open(voices_file, 'r') as f:
                voice_notes = f.read()
            
            assert 'Voice Notes' in voice_notes
            assert 'women' in voice_notes.lower() or 'Women' in voice_notes
            
            print(f"✅ End-to-end test passed: {scored} titles scored, {top} top titles selected")
            print(f"  Scores saved to: {scores_file.name}")
            print(f"  Voice notes saved to: {voices_file.name}")
            return True
            
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def run_all_tests():
    """Run all tests."""
    print("\n" + "🧪" * 30)
    print("RUNNING TITLE SCORING TESTS")
    print("🧪" * 30 + "\n")
    
    tests = [
        ("Module Imports", test_imports),
        ("Load Scoring Config", test_load_scoring_config),
        ("Local Title Scoring", test_score_title_locally),
        ("Voice Recommendation", test_voice_recommendation),
        ("Extract Title from File", test_extract_title_from_file),
        ("End-to-End Scoring", test_end_to_end_scoring),
    ]
    
    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"\n❌ Test '{name}' failed with exception: {e}")
            import traceback
            traceback.print_exc()
            results.append((name, False))
    
    # Print summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{status}: {name}")
    
    print(f"\n{passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 ALL TESTS PASSED! 🎉")
        return 0
    else:
        print("\n⚠️ SOME TESTS FAILED")
        return 1


if __name__ == "__main__":
    sys.exit(run_all_tests())
