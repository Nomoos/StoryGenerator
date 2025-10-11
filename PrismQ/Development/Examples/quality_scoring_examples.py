#!/usr/bin/env python3
"""
Example: Using the Content Quality Scorer

Demonstrates how to use the quality scoring system to assess content.
"""

import sys
import json
from pathlib import Path

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from process_quality import calculate_score, assess_content_quality, load_scoring_config


def example_score_ideas():
    """Example 1: Score different quality ideas."""
    print("=" * 60)
    print("Example 1: Scoring Ideas")
    print("=" * 60)

    ideas = [
        {
            "title": "The Secret Nobody Tells You About Success",
            "synopsis": "A shocking revelation that changes everything you thought you knew",
            "hook": "What if the key to success was hiding in plain sight?",
            "themes": ["mystery", "revelation", "success", "truth"],
        },
        {
            "title": "A Story About Things",
            "synopsis": "Some things happen",
            "hook": "This is a story",
        },
        {
            "title": "The Amazing Discovery That Will Blow Your Mind",
            "synopsis": "Scientists have uncovered something incredible that could change the world forever",
            "hook": "Are you ready to learn the truth?",
            "themes": ["science", "discovery", "mystery", "innovation", "future"],
        },
    ]

    for i, idea in enumerate(ideas, 1):
        score = calculate_score(idea)
        print(f"\nIdea {i}: {idea['title']}")
        print(f"Score: {score:.1f}/100")

        if score >= 85:
            print("Quality: ⭐ Excellent")
        elif score >= 70:
            print("Quality: ✅ Good")
        elif score >= 55:
            print("Quality: ⚠️  Acceptable (needs improvement)")
        else:
            print("Quality: ❌ Poor (needs rework)")


def example_detailed_metrics():
    """Example 2: Get detailed metric breakdown."""
    print("\n" + "=" * 60)
    print("Example 2: Detailed Metrics")
    print("=" * 60)

    content = {
        "title": "Why Everyone Keeps Making The Same Mistakes",
        "description": "This shocking truth reveals the hidden patterns in human behavior that nobody talks about",
        "themes": ["psychology", "behavior", "truth", "society"],
        "keywords": ["mistakes", "patterns", "human", "hidden"],
    }

    # Get individual metrics
    metrics = assess_content_quality(content, "topic")

    print(f"\nContent: {content['title']}")
    print("\n📊 Metric Breakdown:")
    print(f"  Novelty:     {metrics['novelty']:.1f}/100  (uniqueness & surprise)")
    print(f"  Emotional:   {metrics['emotional']:.1f}/100  (emotional impact)")
    print(f"  Clarity:     {metrics['clarity']:.1f}/100  (understandability)")
    print(f"  Replay:      {metrics['replay']:.1f}/100  (rewatchability)")
    print(f"  Share:       {metrics['share']:.1f}/100  (viral potential)")

    # Calculate weighted score using the same function the system uses
    final_score = calculate_score(content)
    print(f"\n🎯 Final Score: {final_score:.1f}/100")


def example_compare_titles():
    """Example 3: Compare different title styles."""
    print("\n" + "=" * 60)
    print("Example 3: Comparing Title Styles")
    print("=" * 60)

    titles = [
        {"title": "5 Secrets Nobody Tells You About Success", "style": "List + Secret"},
        {"title": "Why Do We Keep Making The Same Mistakes?", "style": "Question"},
        {"title": "The Truth They Don't Want You To Know", "style": "Conspiracy"},
        {"title": "How I Changed My Life Forever", "style": "Personal"},
        {"title": "A Guide to Better Living", "style": "Generic"},
    ]

    results = []
    for title_data in titles:
        score = calculate_score({"title": title_data["title"]})
        results.append({"title": title_data["title"], "style": title_data["style"], "score": score})

    # Sort by score
    results.sort(key=lambda x: x["score"], reverse=True)

    print("\n🏆 Title Rankings (by viral potential):\n")
    for i, result in enumerate(results, 1):
        print(f"{i}. {result['title']}")
        print(f"   Style: {result['style']} | Score: {result['score']:.1f}/100\n")


def example_batch_scoring():
    """Example 4: Batch score multiple content files."""
    print("\n" + "=" * 60)
    print("Example 4: Batch Scoring")
    print("=" * 60)

    # Simulate multiple content items
    content_batch = [
        {
            "id": "001",
            "title": "The Mystery of the Ancient Code",
            "synopsis": "Coders discover a hidden algorithm in old files",
            "themes": ["technology", "mystery"],
        },
        {
            "id": "002",
            "title": "Space Adventures",
            "synopsis": "Exploring the solar system",
            "themes": ["space"],
        },
        {
            "id": "003",
            "title": "The Secret Truth Everyone Needs to Know",
            "synopsis": "A shocking revelation that will change everything",
            "themes": ["truth", "revelation", "mystery"],
        },
        {"id": "004", "title": "Test", "synopsis": "Test content"},
    ]

    print("\n📊 Scoring Results:\n")

    excellent = []
    good = []
    acceptable = []
    poor = []

    for content in content_batch:
        score = calculate_score(content)

        if score >= 85:
            excellent.append((content["id"], score))
            status = "⭐ Excellent"
        elif score >= 70:
            good.append((content["id"], score))
            status = "✅ Good"
        elif score >= 55:
            acceptable.append((content["id"], score))
            status = "⚠️  Acceptable"
        else:
            poor.append((content["id"], score))
            status = "❌ Poor"

        print(f"[{content['id']}] {content['title']}")
        print(f"       Score: {score:.1f}/100 - {status}\n")

    print("\n" + "=" * 60)
    print("Summary:")
    print(f"  ⭐ Excellent: {len(excellent)}")
    print(f"  ✅ Good: {len(good)}")
    print(f"  ⚠️  Acceptable: {len(acceptable)}")
    print(f"  ❌ Poor: {len(poor)}")
    print(f"  Total: {len(content_batch)}")


def example_custom_weights():
    """Example 5: Using custom scoring weights."""
    print("\n" + "=" * 60)
    print("Example 5: Custom Scoring Weights")
    print("=" * 60)

    content = {
        "title": "The Amazing Discovery",
        "synopsis": "A scientist makes a breakthrough",
        "themes": ["science", "discovery"],
    }

    # Default weights
    config_default = load_scoring_config()
    score_default = calculate_score(content, config_default)

    print(f"\nContent: {content['title']}")
    print(f"\nDefault Score: {score_default:.1f}/100")
    print("Weights:", config_default.get("viral", {}))

    # Custom weights (emphasize shareability)
    config_custom = {
        "viral": {
            "novelty": 0.15,
            "emotional": 0.20,
            "clarity": 0.15,
            "replay": 0.10,
            "share": 0.40,  # Increased shareability weight
        }
    }
    score_custom = calculate_score(content, config_custom)

    print(f"\nCustom Score (share-focused): {score_custom:.1f}/100")
    print("Weights:", config_custom["viral"])
    print(f"\nDifference: {abs(score_default - score_custom):.1f} points")


def main():
    """Run all examples."""
    print("\n" + "=" * 60)
    print("Content Quality Scoring Examples")
    print("=" * 60)
    print()

    example_score_ideas()
    example_detailed_metrics()
    example_compare_titles()
    example_batch_scoring()
    example_custom_weights()

    print("\n" + "=" * 60)
    print("Examples Complete!")
    print("=" * 60)
    print("\nFor more information, see docs/QUALITY_SCORING.md")
    print()


if __name__ == "__main__":
    main()
