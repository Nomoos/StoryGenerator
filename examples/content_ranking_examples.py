#!/usr/bin/env python3
"""
Content Ranking Examples

Demonstrates how to use the content ranking system with sample data.
"""

import json
import tempfile
from pathlib import Path
from datetime import datetime

# Add parent directory to path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

import content_ranking


def example_1_basic_ranking():
    """Example 1: Basic content ranking with sample data."""
    print("=" * 60)
    print("Example 1: Basic Content Ranking")
    print("=" * 60)

    # Sample scored content
    content = [
        {
            "id": "reddit-001",
            "title": "The Secret Letter That Changed My Life",
            "source": "r/TrueOffMyChest",
            "quality_score": 87,
            "novelty": 85,
            "emotional_impact": 90,
            "clarity": 88,
            "replay_value": 82,
            "shareability": 86,
        },
        {
            "id": "reddit-002",
            "title": "I Discovered My Best Friend's Dark Secret",
            "source": "r/confession",
            "quality_score": 92,
            "novelty": 91,
            "emotional_impact": 94,
            "clarity": 90,
            "replay_value": 88,
            "shareability": 93,
        },
        {
            "id": "twitter-001",
            "title": "A Shocking Family Revelation",
            "source": "Twitter",
            "quality_score": 78,
            "novelty": 75,
            "emotional_impact": 82,
            "clarity": 79,
            "replay_value": 74,
            "shareability": 77,
        },
    ]

    # No duplicates in this example
    dedup_report = {"duplicates": [], "retained_items": ["reddit-001", "reddit-002", "twitter-001"]}

    # Load config
    config = content_ranking.load_config()

    # Rank content
    ranked = content_ranking.rank_content(content, dedup_report, config)

    print(f"\n📊 Ranking Results:")
    print(f"   Total items: {len(ranked)}")
    print("\n   Ranked List:")
    for item in ranked:
        print(f"      Rank {item['rank']}: {item['title']}")
        print(f"         ID: {item['id']}")
        print(f"         Score: {item['final_score']:.2f}")
        print(f"         Source: {item['source']}")
        print()


def example_2_with_duplicates():
    """Example 2: Content ranking with duplicate filtering."""
    print("\n" + "=" * 60)
    print("Example 2: Ranking with Duplicate Filtering")
    print("=" * 60)

    # Sample content with one duplicate
    content = [
        {"id": "story-001", "title": "The Truth About My Parents", "quality_score": 85},
        {"id": "story-002", "title": "A Life-Changing Discovery", "quality_score": 92},
        {"id": "story-003", "title": "The Secret I Kept for Years", "quality_score": 88},
        {
            "id": "story-004",  # This is a duplicate
            "title": "Similar to Story 001",
            "quality_score": 87,
        },
        {"id": "story-005", "title": "The Day Everything Changed", "quality_score": 79},
    ]

    # Dedup report marking story-004 as duplicate
    dedup_report = {
        "duplicates": [
            {
                "id": "story-004",
                "similar_to": "story-001",
                "similarity_score": 0.89,
                "reason": "Similar theme and narrative structure",
            }
        ],
        "retained_items": ["story-001", "story-002", "story-003", "story-005"],
    }

    config = content_ranking.load_config()

    print(f"\n📥 Input: {len(content)} items")
    print(f"   Duplicates to filter: {len(dedup_report['duplicates'])}")

    ranked = content_ranking.rank_content(content, dedup_report, config)

    print(f"\n📊 Ranking Results:")
    print(f"   Items after filtering: {len(ranked)}")
    print("\n   Top 3 Ranked Items:")
    for item in ranked[:3]:
        print(f"      Rank {item['rank']}: {item['title']}")
        print(f"         ID: {item['id']}, Score: {item['final_score']:.2f}")

    print(f"\n   ✓ story-004 was successfully filtered as duplicate")


def example_3_full_workflow():
    """Example 3: Full end-to-end workflow with file I/O."""
    print("\n" + "=" * 60)
    print("Example 3: Full End-to-End Workflow")
    print("=" * 60)

    with tempfile.TemporaryDirectory() as tmpdir:
        base_path = Path(tmpdir) / "Generator"
        scores_path = base_path / "scores" / "women" / "18-23"
        scores_path.mkdir(parents=True, exist_ok=True)

        date_str = datetime.now().strftime("%Y-%m-%d")

        # Create sample scored content
        print("\n📝 Creating sample data files...")

        content_scores = [
            {
                "id": "viral-001",
                "title": "The Letter I Should Never Have Opened",
                "source": "r/TrueOffMyChest",
                "url": "https://reddit.com/r/TrueOffMyChest/abc123",
                "upvotes": 8542,
                "comments": 423,
                "quality_score": 89,
                "novelty": 88,
                "emotional_impact": 92,
                "clarity": 87,
                "replay_value": 85,
                "shareability": 90,
            },
            {
                "id": "viral-002",
                "title": "I Found Out My Sister's Secret",
                "source": "r/relationships",
                "url": "https://reddit.com/r/relationships/def456",
                "upvotes": 12340,
                "comments": 856,
                "quality_score": 94,
                "novelty": 93,
                "emotional_impact": 96,
                "clarity": 92,
                "replay_value": 91,
                "shareability": 95,
            },
            {
                "id": "viral-003",
                "title": "The Truth About My Best Friend",
                "source": "r/confession",
                "url": "https://reddit.com/r/confession/ghi789",
                "upvotes": 6234,
                "comments": 312,
                "quality_score": 82,
                "novelty": 80,
                "emotional_impact": 85,
                "clarity": 83,
                "replay_value": 78,
                "shareability": 82,
            },
        ]

        scores_file = scores_path / f"content_scores_{date_str}.json"
        with open(scores_file, "w") as f:
            json.dump(content_scores, f, indent=2)

        print(f"   ✓ Created: {scores_file.name}")

        # Create dedup report
        dedup_report = {
            "duplicates": [],
            "total_checked": 3,
            "total_unique": 3,
            "similarity_threshold": 0.85,
        }

        dedup_file = scores_path / f"dedup_report_{date_str}.json"
        with open(dedup_file, "w") as f:
            json.dump(dedup_report, f, indent=2)

        print(f"   ✓ Created: {dedup_file.name}")

        # Run ranking
        print(f"\n🔄 Running ranking for women/18-23...")
        config = content_ranking.load_config()
        success = content_ranking.rank_content_for_segment(base_path, "women", "18-23", config)

        if success:
            # Load and display results
            output_file = scores_path / f"ranked_content_{date_str}.json"
            with open(output_file, "r") as f:
                results = json.load(f)

            print(f"\n✅ Ranking Complete!")
            print(f"   Output: {output_file.name}")
            print(f"   Gender: {results['gender']}")
            print(f"   Age Bucket: {results['age_bucket']}")
            print(f"   Total Items: {results['total_items']}")
            print(f"\n   📈 Top Ranked Content:")

            for item in results["content"]:
                print(f"\n      Rank {item['rank']}: {item['title']}")
                print(f"         Score: {item['final_score']:.2f}")
                print(f"         Source: {item['source']}")
                print(
                    f"         Engagement: {item['upvotes']} upvotes, {item['comments']} comments"
                )


def example_4_score_calculation():
    """Example 4: Understanding score calculation."""
    print("\n" + "=" * 60)
    print("Example 4: Score Calculation Explained")
    print("=" * 60)

    config = {
        "viral": {
            "novelty": 0.25,
            "emotional": 0.25,
            "clarity": 0.20,
            "replay": 0.15,
            "share": 0.15,
        }
    }

    item = {
        "id": "example-001",
        "title": "Sample Story Title",
        "novelty": 85,
        "emotional_impact": 90,
        "clarity": 88,
        "replay_value": 82,
        "shareability": 87,
    }

    print("\n📐 Score Calculation:")
    print(f"   Novelty:          {item['novelty']} × 0.25 = {item['novelty'] * 0.25:.2f}")
    print(
        f"   Emotional Impact: {item['emotional_impact']} × 0.25 = {item['emotional_impact'] * 0.25:.2f}"
    )
    print(f"   Clarity:          {item['clarity']} × 0.20 = {item['clarity'] * 0.20:.2f}")
    print(f"   Replay Value:     {item['replay_value']} × 0.15 = {item['replay_value'] * 0.15:.2f}")
    print(f"   Shareability:     {item['shareability']} × 0.15 = {item['shareability'] * 0.15:.2f}")

    final_score = content_ranking.calculate_final_score(item, config)

    print(f"   " + "-" * 50)
    print(f"   Final Score:      {final_score:.2f}")

    print(f"\n   💡 Interpretation:")
    if final_score >= 85:
        print(f"      Excellent - Top-tier viral potential")
    elif final_score >= 70:
        print(f"      Good - Strong candidate for production")
    elif final_score >= 55:
        print(f"      Acceptable - May need refinement")
    else:
        print(f"      Below threshold - Consider alternatives")


def main():
    """Run all examples."""
    print("\n" + "=" * 70)
    print(" " * 15 + "Content Ranking Examples")
    print("=" * 70)

    example_1_basic_ranking()
    example_2_with_duplicates()
    example_3_full_workflow()
    example_4_score_calculation()

    print("\n" + "=" * 70)
    print("Examples complete!")
    print("=" * 70)


if __name__ == "__main__":
    main()
