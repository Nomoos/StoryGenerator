#!/usr/bin/env python3
"""
Test script for Content Quality Scorer

Tests the quality assessment functionality for different content types.
"""

import os
import sys
import json
from pathlib import Path

# Add scripts directory to path
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'scripts'))

from process_quality import (
    calculate_score, 
    assess_content_quality,
    assess_novelty,
    assess_emotional_impact,
    assess_clarity,
    assess_replay_value,
    assess_shareability,
    load_scoring_config
)


def test_score_idea():
    """Test scoring for idea content."""
    print("\n" + "="*60)
    print("Testing Content Quality Scorer - Idea Content")
    print("="*60)
    
    # High quality idea
    high_quality_idea = {
        "idea_id": "test_001",
        "title": "The Secret Truth Nobody Wants You to Know",
        "synopsis": "A shocking discovery reveals the hidden mysteries behind everyday life that will change how you see the world forever",
        "hook": "What if everything you believed was actually a carefully constructed lie?",
        "themes": ["mystery", "revelation", "truth", "conspiracy", "discovery"],
        "genre": "thriller"
    }
    
    score = calculate_score(high_quality_idea)
    print(f"\n✅ High Quality Idea Score: {score:.2f}/100")
    
    if score >= 70:
        print("   Correctly identified as high quality")
    else:
        print("   ❌ Should be high quality")
        return False
    
    # Low quality idea
    low_quality_idea = {
        "title": "Test"
    }
    
    score = calculate_score(low_quality_idea)
    print(f"\n✅ Low Quality Idea Score: {score:.2f}/100")
    
    if score < 50:
        print("   Correctly identified as low quality")
    else:
        print("   ❌ Should be low quality")
        return False
    
    return True


def test_score_topic():
    """Test scoring for topic content."""
    print("\n" + "="*60)
    print("Testing Content Quality Scorer - Topic Content")
    print("="*60)
    
    # Good quality topic
    topic = {
        "topic_id": "test_002",
        "category": "science",
        "title": "Amazing Space Discovery That Will Blow Your Mind",
        "description": "Scientists have uncovered a mysterious signal from deep space that could reveal the secrets of the universe and change everything we know",
        "keywords": ["space", "discovery", "science", "mystery", "universe"]
    }
    
    score = calculate_score(topic)
    print(f"\n✅ Topic Score: {score:.2f}/100")
    
    if 55 <= score <= 90:
        print("   Score in expected range")
    else:
        print("   ⚠️ Score outside expected range")
    
    return True


def test_score_title():
    """Test scoring for title content."""
    print("\n" + "="*60)
    print("Testing Content Quality Scorer - Title Content")
    print("="*60)
    
    # High viral potential title
    viral_title = {
        "title": "5 Secrets Nobody Tells You About Success That Will Change Your Life"
    }
    
    score = calculate_score(viral_title)
    print(f"\n✅ Viral Title Score: {score:.2f}/100")
    
    # Question-based title
    question_title = {
        "title": "Why Do We Keep Making The Same Mistakes? The Truth Revealed"
    }
    
    score2 = calculate_score(question_title)
    print(f"✅ Question Title Score: {score2:.2f}/100")
    
    # Generic title
    generic_title = {
        "title": "A Story About Things"
    }
    
    score3 = calculate_score(generic_title)
    print(f"✅ Generic Title Score: {score3:.2f}/100")
    
    if score > score3 and score2 > score3:
        print("\n   Correctly ranked titles by quality")
        return True
    else:
        print("\n   ❌ Title ranking incorrect")
        return False


def test_individual_metrics():
    """Test individual quality metrics."""
    print("\n" + "="*60)
    print("Testing Individual Quality Metrics")
    print("="*60)
    
    content_data = {
        "title": "The Amazing Secret Truth About Everything",
        "description": "This shocking revelation will change how you see the world. Everyone needs to know this hidden truth that nobody talks about.",
        "themes": ["mystery", "truth", "revelation", "society"]
    }
    
    scores = assess_content_quality(content_data, "topic")
    
    print("\n📊 Individual Metric Scores:")
    print(f"   Novelty:     {scores['novelty']:.1f}/100")
    print(f"   Emotional:   {scores['emotional']:.1f}/100")
    print(f"   Clarity:     {scores['clarity']:.1f}/100")
    print(f"   Replay:      {scores['replay']:.1f}/100")
    print(f"   Share:       {scores['share']:.1f}/100")
    
    # Check that all scores are in valid range
    for metric, score in scores.items():
        if not (0 <= score <= 100):
            print(f"\n   ❌ {metric} score out of range: {score}")
            return False
    
    print("\n✅ All metrics in valid range (0-100)")
    return True


def test_scoring_config():
    """Test scoring configuration loading."""
    print("\n" + "="*60)
    print("Testing Scoring Configuration")
    print("="*60)
    
    config = load_scoring_config()
    
    # Check viral weights
    if "viral" in config:
        viral = config["viral"]
        print(f"\n✅ Viral weights loaded:")
        for metric, weight in viral.items():
            print(f"   {metric}: {weight}")
        
        # Check that weights sum to approximately 1.0
        total = sum(viral.values())
        if 0.95 <= total <= 1.05:
            print(f"\n✅ Weights sum to {total:.2f} (valid)")
        else:
            print(f"\n⚠️ Weights sum to {total:.2f} (should be ~1.0)")
    else:
        print("   ⚠️ Using default weights")
    
    # Check thresholds
    if "thresholds" in config:
        thresholds = config["thresholds"]
        print(f"\n✅ Quality thresholds:")
        for level, score in thresholds.items():
            print(f"   {level}: {score}")
    
    return True


def test_content_type_detection():
    """Test automatic content type detection."""
    print("\n" + "="*60)
    print("Testing Content Type Detection")
    print("="*60)
    
    # Test idea detection
    idea = {"idea_id": "001", "synopsis": "test"}
    scores = assess_content_quality(idea)
    print("\n✅ Idea type detected and scored")
    
    # Test topic detection
    topic = {"topic_id": "002", "category": "test", "keywords": ["a", "b"]}
    scores = assess_content_quality(topic)
    print("✅ Topic type detected and scored")
    
    # Test title detection
    title = {"title": "Test Title"}
    scores = assess_content_quality(title)
    print("✅ Title type detected and scored")
    
    return True


def run_all_tests():
    """Run all tests."""
    print("\n" + "="*60)
    print("Content Quality Scorer Test Suite")
    print("="*60)
    
    tests = [
        ("Idea Scoring", test_score_idea),
        ("Topic Scoring", test_score_topic),
        ("Title Scoring", test_score_title),
        ("Individual Metrics", test_individual_metrics),
        ("Scoring Config", test_scoring_config),
        ("Content Type Detection", test_content_type_detection)
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
    
    print(f"\n{'='*60}")
    print(f"Total: {passed}/{total} tests passed")
    print(f"{'='*60}\n")
    
    return 0 if passed == total else 1


if __name__ == "__main__":
    sys.exit(run_all_tests())
