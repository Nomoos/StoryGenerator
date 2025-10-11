#!/usr/bin/env python3
"""
Content Ranking Module for StoryGenerator

Ranks content by viral potential and quality scores after quality scoring and deduplication.
For each segment/age:
- Reads scored content from content_scores_{date}.json
- Reads deduplication report from dedup_report_{date}.json
- Filters out duplicates
- Ranks content by final score (descending)
- Saves ranked list to Generator/scores/{gender}/{age_bucket}/ranked_content_{date}.json
"""

import os
import json
import yaml
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional
import sys


# Default scoring configuration (fallback if scoring.yaml is not found)
DEFAULT_SCORING_CONFIG = {
    "viral": {
        "novelty": 0.25,
        "emotional": 0.25,
        "clarity": 0.20,
        "replay": 0.15,
        "share": 0.15,
    },
    "thresholds": {
        "excellent": 85,
        "good": 70,
        "acceptable": 55,
        "poor": 40,
    },
}


def load_config(config_path: str = None) -> Dict:
    """
    Load scoring configuration from YAML file.

    Args:
        config_path: Path to scoring.yaml file

    Returns:
        Configuration dictionary with scoring weights
    """
    if config_path is None:
        config_path = Path(__file__).parent.parent / "config" / "scoring.yaml"

    try:
        with open(config_path, "r", encoding="utf-8") as f:
            config = yaml.safe_load(f)
        print(f"✅ Loaded config from {config_path}")
        return config
    except FileNotFoundError:
        print(f"⚠️  Config file not found: {config_path}, using defaults")
        return DEFAULT_SCORING_CONFIG
    except Exception as e:
        print(f"❌ Error loading config: {e}")
        raise


def find_latest_file(directory: Path, pattern: str) -> Optional[Path]:
    """
    Find the latest file matching a pattern in a directory.

    Args:
        directory: Directory to search
        pattern: Glob pattern to match

    Returns:
        Path to latest file or None
    """
    if not directory.exists():
        return None

    matching_files = list(directory.glob(pattern))
    if not matching_files:
        return None

    # Sort by modification time, most recent first
    matching_files.sort(key=lambda p: p.stat().st_mtime, reverse=True)
    return matching_files[0]


def load_scored_content(scores_path: Path, gender: str, age: str) -> Optional[List[Dict]]:
    """
    Load scored content from the quality scorer output.

    Args:
        scores_path: Base path to scores directory
        gender: Target gender (men/women)
        age: Target age range

    Returns:
        List of scored content items or None
    """
    segment_path = scores_path / gender / age

    if not segment_path.exists():
        print(f"⚠️  Scores directory does not exist: {segment_path}")
        return None

    # Find latest content_scores file
    scores_file = find_latest_file(segment_path, "content_scores_*.json")

    if not scores_file:
        print(f"⚠️  No content_scores files found in {segment_path}")
        return None

    print(f"📄 Loading scored content from: {scores_file.name}")

    try:
        with open(scores_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        # Handle different possible formats
        if isinstance(data, list):
            return data
        elif isinstance(data, dict) and "content" in data:
            return data["content"]
        elif isinstance(data, dict) and "items" in data:
            return data["items"]
        else:
            print(f"⚠️  Unexpected data format in {scores_file.name}")
            return None

    except Exception as e:
        print(f"❌ Error loading scored content: {e}")
        return None


def load_dedup_report(scores_path: Path, gender: str, age: str) -> Optional[Dict]:
    """
    Load deduplication report.

    Args:
        scores_path: Base path to scores directory
        gender: Target gender (men/women)
        age: Target age range

    Returns:
        Deduplication report dictionary or None
    """
    segment_path = scores_path / gender / age

    if not segment_path.exists():
        print(f"⚠️  Scores directory does not exist: {segment_path}")
        return None

    # Find latest dedup_report file
    dedup_file = find_latest_file(segment_path, "dedup_report_*.json")

    if not dedup_file:
        print(f"⚠️  No dedup_report files found in {segment_path}")
        # Not having a dedup report is not critical - we can still rank
        return {"duplicates": [], "retained_items": []}

    print(f"📄 Loading dedup report from: {dedup_file.name}")

    try:
        with open(dedup_file, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"❌ Error loading dedup report: {e}")
        return {"duplicates": [], "retained_items": []}


def get_duplicate_ids(dedup_report: Dict) -> set:
    """
    Extract IDs of content marked as duplicates.

    Args:
        dedup_report: Deduplication report dictionary

    Returns:
        Set of content IDs that are duplicates
    """
    duplicate_ids = set()

    # Handle different possible formats
    if "duplicates" in dedup_report:
        duplicates = dedup_report["duplicates"]
        if isinstance(duplicates, list):
            for dup in duplicates:
                if isinstance(dup, dict):
                    # Could be {'id': 'xxx', ...} or {'duplicate_id': 'xxx', ...}
                    if "id" in dup:
                        duplicate_ids.add(dup["id"])
                    elif "duplicate_id" in dup:
                        duplicate_ids.add(dup["duplicate_id"])
                    elif "content_id" in dup:
                        duplicate_ids.add(dup["content_id"])
                elif isinstance(dup, str):
                    duplicate_ids.add(dup)

    return duplicate_ids


def calculate_final_score(item: Dict, config: Dict) -> float:
    """
    Calculate final ranking score for a content item.

    Args:
        item: Content item with scores
        config: Configuration dictionary

    Returns:
        Final score (0-100)
    """
    # Get scoring weights from config
    scoring_config = config.get("viral", {})

    # Default weights if not in config
    weights = {
        "novelty": scoring_config.get("novelty", 0.25),
        "emotional": scoring_config.get("emotional", 0.25),
        "clarity": scoring_config.get("clarity", 0.20),
        "replay": scoring_config.get("replay", 0.15),
        "share": scoring_config.get("share", 0.15),
    }

    # Check if item already has a final score
    if "final_score" in item:
        return item["final_score"]
    if "overall_score" in item:
        return item["overall_score"]

    # Calculate weighted score from component scores
    final_score = 0.0

    # Try different possible score field names
    score_fields = {
        "novelty": ["novelty", "novelty_score"],
        "emotional": ["emotional_impact", "emotional", "emotional_score"],
        "clarity": ["clarity", "clarity_score"],
        "replay": ["replay_value", "replay", "replay_score"],
        "share": ["shareability", "share", "share_score"],
    }

    for metric, possible_fields in score_fields.items():
        value = None
        for field in possible_fields:
            if field in item:
                value = item[field]
                break

        if value is not None:
            final_score += value * weights[metric]

    # If we couldn't calculate from components, try other fields
    if final_score == 0:
        # Try quality_score, viral_score, or score
        if "quality_score" in item:
            final_score = item["quality_score"]
        elif "viral_score" in item:
            final_score = item["viral_score"]
        elif "score" in item:
            final_score = item["score"]

    return final_score


def rank_content(content: List[Dict], dedup_report: Dict, config: Dict) -> List[Dict]:
    """
    Rank content by final score, filtering out duplicates.

    Args:
        content: List of scored content items
        dedup_report: Deduplication report
        config: Configuration dictionary

    Returns:
        Sorted list of ranked content
    """
    print(f"\n🔄 Ranking {len(content)} content items...")

    # Get duplicate IDs
    duplicate_ids = get_duplicate_ids(dedup_report)
    print(f"   Found {len(duplicate_ids)} duplicates to filter out")

    # Filter out duplicates and calculate final scores
    ranked_items = []
    filtered_count = 0

    for item in content:
        # Get content ID (try different possible field names)
        content_id = item.get("id") or item.get("content_id") or item.get("_id")

        # Skip duplicates
        if content_id and content_id in duplicate_ids:
            filtered_count += 1
            continue

        # Calculate final score
        final_score = calculate_final_score(item, config)

        # Create ranked item
        ranked_item = {**item, "final_score": final_score}  # Keep all original fields

        ranked_items.append(ranked_item)

    print(f"   Filtered out {filtered_count} duplicates")
    print(f"   Ranking {len(ranked_items)} unique items...")

    # Sort by final score (descending)
    ranked_items.sort(key=lambda x: x["final_score"], reverse=True)

    # Add rank field
    for i, item in enumerate(ranked_items, start=1):
        item["rank"] = i

    return ranked_items


def save_ranked_content(
    ranked_content: List[Dict], scores_path: Path, gender: str, age: str
) -> Path:
    """
    Save ranked content to JSON file.

    Args:
        ranked_content: List of ranked content items
        scores_path: Base path to scores directory
        gender: Target gender
        age: Target age range

    Returns:
        Path to saved file
    """
    segment_path = scores_path / gender / age
    segment_path.mkdir(parents=True, exist_ok=True)

    # Generate filename with current date
    date_str = datetime.now().strftime("%Y-%m-%d")
    output_file = segment_path / f"ranked_content_{date_str}.json"

    # Prepare output data
    output_data = {
        "gender": gender,
        "age_bucket": age,
        "ranked_at": datetime.now().isoformat(),
        "total_items": len(ranked_content),
        "content": ranked_content,
    }

    # Save to file
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)

    print(f"✅ Saved ranked content to: {output_file}")
    return output_file


def rank_content_for_segment(base_path: Path, gender: str, age: str, config: Dict) -> bool:
    """
    Rank content for a specific segment.

    Args:
        base_path: Base Generator path
        gender: Target gender
        age: Target age range
        config: Configuration dictionary

    Returns:
        True if successful, False otherwise
    """
    print(f"\n{'='*60}")
    print(f"📊 Ranking content for {gender}/{age}")
    print(f"{'='*60}")

    scores_path = base_path / "scores"

    # Load scored content
    content = load_scored_content(scores_path, gender, age)
    if not content:
        print(f"❌ No scored content found for {gender}/{age}")
        return False

    # Load dedup report
    dedup_report = load_dedup_report(scores_path, gender, age)

    # Rank content
    ranked_content = rank_content(content, dedup_report, config)

    if not ranked_content:
        print(f"⚠️  No content to rank after filtering for {gender}/{age}")
        return False

    # Save results
    save_ranked_content(ranked_content, scores_path, gender, age)

    # Print summary
    print(f"\n📈 Ranking Summary:")
    print(f"   Total items ranked: {len(ranked_content)}")
    if ranked_content:
        top_score = ranked_content[0]["final_score"]
        bottom_score = ranked_content[-1]["final_score"]
        print(f"   Top score: {top_score:.2f}")
        print(f"   Bottom score: {bottom_score:.2f}")
        print(f"\n   Top 5 items:")
        for i, item in enumerate(ranked_content[:5], start=1):
            content_id = item.get("id") or item.get("content_id") or f"item_{i}"
            print(f"      {i}. {content_id}: {item['final_score']:.2f}")

    return True


def process_all_segments(base_path: Path = None, config: Dict = None) -> None:
    """
    Process ranking for all segments.

    Args:
        base_path: Base Generator path
        config: Configuration dictionary
    """
    if base_path is None:
        base_path = Path.cwd() / "Generator"

    if config is None:
        config = load_config()

    # Define all segments
    genders = ["women", "men"]
    age_buckets = ["10-13", "14-17", "18-23"]

    print(f"\n🚀 Starting content ranking for all segments...")
    print(f"   Base path: {base_path}")

    success_count = 0
    total_count = 0

    for gender in genders:
        for age in age_buckets:
            total_count += 1
            if rank_content_for_segment(base_path, gender, age, config):
                success_count += 1

    print(f"\n{'='*60}")
    print(f"✅ Ranking complete: {success_count}/{total_count} segments processed")
    print(f"{'='*60}")


def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(description="Rank content by viral potential")
    parser.add_argument("gender", nargs="?", help="Target gender (women/men)")
    parser.add_argument("age", nargs="?", help="Target age bucket (10-13, 14-17, 18-23)")
    parser.add_argument("--base-path", help="Base Generator directory path")
    parser.add_argument("--config", help="Path to config file")

    args = parser.parse_args()

    # Load config
    config = load_config(args.config)

    # Determine base path
    if args.base_path:
        base_path = Path(args.base_path)
    else:
        base_path = Path.cwd() / "Generator"

    if args.gender and args.age:
        # Process specific segment
        print(f"Processing segment: {args.gender}/{args.age}")
        success = rank_content_for_segment(base_path, args.gender, args.age, config)
        sys.exit(0 if success else 1)
    else:
        # Process all segments
        process_all_segments(base_path, config)


if __name__ == "__main__":
    main()
