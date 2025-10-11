#!/usr/bin/env python3
"""
Title Improvement Examples

Demonstrates how to use the title improvement system to generate
and score improved title variants.
"""

import sys
from pathlib import Path

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

import title_improve
import title_score


def example_1_improve_single_title():
    """Example 1: Improve a single title with the system."""
    print("=" * 70)
    print("EXAMPLE 1: Improve a Single Title")
    print("=" * 70)

    # Original title
    original_title = "10 Tips for Success"
    segment = "women"
    age = "18-23"

    print(f"\nOriginal Title: {original_title}")
    print(f"Target Audience: {segment}, {age}")

    # Load configurations
    llm_config = title_improve.load_llm_config()
    scoring_config_path = Path(__file__).parent.parent / "data" / "config" / "scoring.yaml"
    scoring_config = title_score.load_scoring_config(str(scoring_config_path))

    # Generate variants
    print(f"\nGenerating {5} title variants...")
    variants = title_improve.generate_title_variants(
        original_title, segment, age, llm_config, count=5
    )

    print(f"Generated Variants:")
    for i, variant in enumerate(variants, 1):
        print(f"  {i}. {variant}")

    # Score and select best
    print(f"\nScoring all variants...")
    best_title, best_score, all_scores = title_improve.score_and_select_best_variant(
        original_title, variants, segment, age, scoring_config
    )

    print(f"\n🏆 Best Title: {best_title}")
    print(f"   Score: {best_score['overall_score']:.1f}/100")

    if best_score["is_original"]:
        print("   (Original title was already best!)")
    else:
        improvement = (
            (best_score["overall_score"] - all_scores[0]["overall_score"])
            / all_scores[0]["overall_score"]
            * 100
        )
        print(f"   Improvement: {improvement:+.1f}%")


def example_2_batch_analysis():
    """Example 2: Analyze improvement potential across multiple titles."""
    print("\n\n" + "=" * 70)
    print("EXAMPLE 2: Batch Analysis of Titles")
    print("=" * 70)

    titles = [
        "Simple Life Hacks",
        "Career Advice for Young Professionals",
        "Relationship Tips",
        "5 Ways to Stay Motivated",
        "The Truth About Social Media",
    ]

    segment = "women"
    age = "18-23"

    # Load configs
    llm_config = title_improve.load_llm_config()
    scoring_config_path = Path(__file__).parent.parent / "data" / "config" / "scoring.yaml"
    scoring_config = title_score.load_scoring_config(str(scoring_config_path))

    print(f"\nAnalyzing {len(titles)} titles for {segment}/{age}...")

    results = []
    for title in titles:
        # Generate variants
        variants = title_improve.generate_title_variants(title, segment, age, llm_config, count=3)

        # Score them
        best_title, best_score, all_scores = title_improve.score_and_select_best_variant(
            title, variants, segment, age, scoring_config
        )

        improvement = 0
        if all_scores[0]["overall_score"] > 0:
            improvement = (
                (best_score["overall_score"] - all_scores[0]["overall_score"])
                / all_scores[0]["overall_score"]
                * 100
            )

        results.append(
            {
                "original": title,
                "best": best_title,
                "original_score": all_scores[0]["overall_score"],
                "best_score": best_score["overall_score"],
                "improvement": improvement,
                "is_changed": not best_score["is_original"],
            }
        )

    # Print summary
    print("\n" + "-" * 70)
    print("Results Summary:")
    print("-" * 70)
    print(f"{'Original':<35} {'Score':<8} {'Improved':<8} {'Change'}")
    print("-" * 70)

    for r in results:
        change_icon = "✓" if r["is_changed"] else "–"
        print(
            f"{r['original']:<35} {r['original_score']:>6.1f}  {r['best_score']:>6.1f}  {change_icon:>5}"
        )

    print("-" * 70)
    avg_improvement = sum(r["improvement"] for r in results) / len(results)
    changed_count = sum(1 for r in results if r["is_changed"])
    print(f"\nAverage improvement: {avg_improvement:+.1f}%")
    print(f"Titles improved: {changed_count}/{len(results)}")


def example_3_compare_strategies():
    """Example 3: Compare different variant generation strategies."""
    print("\n\n" + "=" * 70)
    print("EXAMPLE 3: Compare Variant Generation Strategies")
    print("=" * 70)

    original_title = "How to Be More Productive"
    segment = "men"
    age = "24-30"

    print(f"\nOriginal Title: {original_title}")
    print(f"Target Audience: {segment}, {age}")

    # Load scoring config
    scoring_config_path = Path(__file__).parent.parent / "data" / "config" / "scoring.yaml"
    scoring_config = title_score.load_scoring_config(str(scoring_config_path))

    # Score original
    original_score = title_score.score_title_locally(original_title, segment, age, scoring_config)
    print(f"\nOriginal Score: {original_score['overall_score']:.1f}/100")

    # Strategy 1: Local rule-based
    print("\n--- Strategy 1: Local Rule-Based ---")
    local_variants = title_improve.generate_title_variants_local(
        original_title, segment, age, count=5
    )

    for i, variant in enumerate(local_variants, 1):
        score = title_score.score_title_locally(variant, segment, age, scoring_config)
        improvement = (
            (score["overall_score"] - original_score["overall_score"])
            / original_score["overall_score"]
            * 100
        )
        print(f"{i}. {variant}")
        print(f"   Score: {score['overall_score']:.1f}/100 ({improvement:+.1f}%)")


def example_4_registry_tracking():
    """Example 4: Demonstrate registry tracking."""
    print("\n\n" + "=" * 70)
    print("EXAMPLE 4: Title Registry Tracking")
    print("=" * 70)

    # Check if registry exists
    registry_path = Path(__file__).parent.parent / "data" / "titles" / "title_registry.json"

    if registry_path.exists():
        import json

        with open(registry_path, "r") as f:
            registry = json.load(f)

        print(f"\nRegistry Status:")
        print(f"  Total titles tracked: {registry['metadata']['total_titles']}")
        print(f"  Last updated: {registry['metadata']['updated_at']}")

        # Count changes
        changed = sum(1 for t in registry["titles"].values() if t["is_changed"])
        unchanged = len(registry["titles"]) - changed

        print(f"\nTitle Changes:")
        print(f"  Improved: {changed}")
        print(f"  Kept original: {unchanged}")

        if registry["titles"]:
            print(f"\nRecent Improvements:")
            # Sort by improvement percentage
            sorted_titles = sorted(
                registry["titles"].items(), key=lambda x: x[1]["improvement_pct"], reverse=True
            )

            for key, data in sorted_titles[:5]:
                if data["is_changed"]:
                    print(f"\n  {data['segment']}/{data['age']}/{data['title_id']}")
                    print(f"    Original: {data['original_title']}")
                    print(f"    Improved: {data['improved_title']}")
                    print(f"    Slug: {data['slug']}")
                    print(
                        f"    Score: {data['original_score']:.1f} → {data['improved_score']:.1f} ({data['improvement_pct']:+.1f}%)"
                    )
    else:
        print("\n⚠️  No registry found yet. Run title_improve.py to create one.")


def main():
    """Run all examples."""
    print("\n" + "=" * 70)
    print("TITLE IMPROVEMENT EXAMPLES")
    print("=" * 70)

    try:
        example_1_improve_single_title()
        example_2_batch_analysis()
        example_3_compare_strategies()
        example_4_registry_tracking()

        print("\n" + "=" * 70)
        print("✅ All examples completed successfully!")
        print("=" * 70)

    except Exception as e:
        print(f"\n❌ Error running examples: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    main()
