#!/usr/bin/env python3
"""
Example: Using the Title Scoring System

This example demonstrates how to use title_score.py to evaluate video titles.
"""

import sys
import json
from pathlib import Path

# Add parent directory to path to import title_score
sys.path.insert(0, str(Path(__file__).parent.parent))

from title_score import (
    load_scoring_config,
    score_title_locally,
    recommend_voice,
    generate_voice_reasoning,
)


def example_score_single_title():
    """Example 1: Score a single title."""
    print("=" * 60)
    print("Example 1: Score a Single Title")
    print("=" * 60)

    # Load configuration
    config = load_scoring_config()

    # Score a title
    title = "5 Secrets Nobody Tells You About Success"
    gender = "women"
    age = "20-24"

    result = score_title_locally(title, gender, age, config)

    print(f"\nTitle: {title}")
    print(f"Target: {gender}, {age}")
    print(f"\nOverall Score: {result['overall_score']:.1f}/100")
    print(f"Rationale: {result['rationale']}")
    print(f"\nVoice Recommendation: {result['voice_recommendation']['gender']}")
    print(f"Reasoning: {result['voice_recommendation']['reasoning']}")

    print("\nDetailed Scores:")
    for criterion, score in result["scores"].items():
        print(f"  {criterion.replace('_', ' ').title()}: {score}/100")


def example_voice_recommendation():
    """Example 2: Get voice recommendations for different titles."""
    print("\n" + "=" * 60)
    print("Example 2: Voice Recommendations")
    print("=" * 60)

    test_cases = [
        ("The Mystery of the Ancient Code", "women", "18-23"),
        ("10 Beauty Tips for Glowing Skin", "women", "18-23"),
        ("Tech Hacks Every Developer Needs", "men", "25-29"),
        ("How I Built My Dream Career", "women", "25-29"),
        ("The Dark Secret They're Hiding", "men", "20-24"),
    ]

    for title, gender, age in test_cases:
        voice = recommend_voice(title, gender, age)
        reasoning = generate_voice_reasoning(title, gender, age, voice)
        print(f"\nTitle: {title}")
        print(f"Target: {gender}, {age}")
        print(f"Voice: {voice} - {reasoning}")


def example_batch_scoring():
    """Example 3: Score multiple titles and rank them."""
    print("\n" + "=" * 60)
    print("Example 3: Batch Scoring and Ranking")
    print("=" * 60)

    config = load_scoring_config()

    titles = [
        "Why Everyone Is Talking About This",
        "This Changed My Life Forever",
        "The Truth Nobody Wants You to Know",
        "5 Simple Tricks That Actually Work",
        "You Won't Believe What Happened Next",
    ]

    gender = "women"
    age = "18-23"

    results = []
    for title in titles:
        result = score_title_locally(title, gender, age, config)
        results.append({"title": title, "score": result["overall_score"]})

    # Sort by score (descending)
    results.sort(key=lambda x: x["score"], reverse=True)

    print(f"\nRanked titles for {gender}, {age}:\n")
    for i, item in enumerate(results, 1):
        print(f"{i}. {item['title']}")
        print(f"   Score: {item['score']:.1f}/100\n")


def example_score_analysis():
    """Example 4: Analyze scoring patterns."""
    print("\n" + "=" * 60)
    print("Example 4: Scoring Pattern Analysis")
    print("=" * 60)

    config = load_scoring_config()

    # Test different title characteristics
    test_titles = {
        "With Question": "Why Do We Dream at Night?",
        "With Numbers": "7 Ways to Improve Your Life",
        "Emotional Words": "The Shocking Truth They Don't Want You to Know",
        "How-To Format": "How to Build Your First Business",
        "Personal Story": "How I Changed My Life in 30 Days",
        "Generic": "An Interesting Story",
    }

    gender = "women"
    age = "20-24"

    for label, title in test_titles.items():
        result = score_title_locally(title, gender, age, config)
        print(f'\n{label}: "{title}"')
        print(f"  Overall: {result['overall_score']:.1f}/100")
        print(f"  Hook: {result['scores']['hook_strength']}")
        print(f"  Clarity: {result['scores']['clarity']}")
        print(f"  Viral: {result['scores']['viral_potential']}")


def main():
    """Run all examples."""
    print("\n" + "🎬" * 30)
    print("TITLE SCORING SYSTEM - EXAMPLES")
    print("🎬" * 30 + "\n")

    try:
        example_score_single_title()
        example_voice_recommendation()
        example_batch_scoring()
        example_score_analysis()

        print("\n" + "=" * 60)
        print("✅ All examples completed successfully!")
        print("=" * 60)

    except Exception as e:
        print(f"\n❌ Error running examples: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    main()
