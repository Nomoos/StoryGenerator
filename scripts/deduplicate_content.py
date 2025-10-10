#!/usr/bin/env python3
"""
Content Deduplication Script for StoryGenerator

Detects and removes duplicate content from quality-scored stories.
Implements multiple deduplication strategies:
1. Exact ID matching
2. Fuzzy title matching (normalized)
3. Content similarity (text hash)

Outputs:
- Deduplicated content list
- Deduplication report with statistics
"""

import os
import sys
import json
import hashlib
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Set, Tuple
from collections import defaultdict


def normalize_text(text: str) -> str:
    """
    Normalize text for comparison by converting to lowercase and stripping whitespace.

    Args:
        text: Input text to normalize

    Returns:
        Normalized text
    """
    if not text:
        return ""
    return text.lower().strip()


def calculate_content_hash(content: Dict) -> str:
    """
    Calculate a hash of the content for similarity detection.

    Uses first 500 characters of text to detect near-duplicates.
    Note: Does not include title to catch cases where same content has different titles.

    Args:
        content: Content dictionary with text

    Returns:
        SHA256 hash of normalized content
    """
    # Extract text content for hashing
    text = content.get("text", "")

    # Use first 500 chars of text to catch similar stories with slight variations
    text_sample = text[:500] if text else ""

    # Normalize text (case insensitive, strip whitespace)
    normalized = normalize_text(text_sample)

    # Calculate hash
    return hashlib.sha256(normalized.encode("utf-8")).hexdigest()


def deduplicate_content(content_items: List[Dict]) -> Tuple[List[Dict], Dict]:
    """
    Remove duplicate content using multiple strategies.

    Deduplication strategies:
    1. Exact ID match (same content_id)
    2. Fuzzy title match (normalized title)
    3. Content hash match (similar text content)

    When duplicates are found, keeps the highest scoring item.

    Args:
        content_items: List of content dictionaries with scores

    Returns:
        Tuple of (unique_items, report_dict)
    """
    # Sort by score descending to keep best items
    sorted_items = sorted(
        content_items,
        key=lambda x: x.get("viral_score", 0) + x.get("quality_score", 0),
        reverse=True,
    )

    # Tracking sets
    seen_ids: Set[str] = set()
    seen_titles: Set[str] = set()
    seen_hashes: Set[str] = set()

    # Results
    unique_items: List[Dict] = []
    duplicates: Dict[str, List[Dict]] = defaultdict(list)

    # Statistics
    duplicate_by_id = 0
    duplicate_by_title = 0
    duplicate_by_hash = 0

    for item in sorted_items:
        content_id = item.get("content_id", item.get("id", ""))
        title = item.get("title", "")

        is_duplicate = False
        duplicate_reason = None

        # Check 1: Exact ID match
        if content_id and content_id in seen_ids:
            duplicate_by_id += 1
            is_duplicate = True
            duplicate_reason = "exact_id_match"
            duplicates[content_id].append(item)

        # Check 2: Fuzzy title match
        elif title:
            normalized_title = normalize_text(title)
            if normalized_title in seen_titles:
                duplicate_by_title += 1
                is_duplicate = True
                duplicate_reason = "title_match"
                # Find the original for tracking
                for unique_item in unique_items:
                    if normalize_text(unique_item.get("title", "")) == normalized_title:
                        orig_id = unique_item.get("content_id", unique_item.get("id", "unknown"))
                        duplicates[f"title:{orig_id}"].append(item)
                        break

        # Check 3: Content hash match
        if not is_duplicate:
            content_hash = calculate_content_hash(item)
            if content_hash in seen_hashes:
                duplicate_by_hash += 1
                is_duplicate = True
                duplicate_reason = "content_similarity"
                # Find the original for tracking
                for unique_item in unique_items:
                    if calculate_content_hash(unique_item) == content_hash:
                        orig_id = unique_item.get("content_id", unique_item.get("id", "unknown"))
                        duplicates[f"hash:{orig_id}"].append(item)
                        break

        # Add to results if unique
        if not is_duplicate:
            unique_items.append(item)
            if content_id:
                seen_ids.add(content_id)
            if title:
                seen_titles.add(normalize_text(title))
            seen_hashes.add(calculate_content_hash(item))
        else:
            # Add duplicate reason to item for reporting
            item["duplicate_reason"] = duplicate_reason

    # Build report
    report = {
        "timestamp": datetime.now().isoformat(),
        "total_input_items": len(content_items),
        "unique_items": len(unique_items),
        "total_duplicates": len(content_items) - len(unique_items),
        "duplicates_by_type": {
            "exact_id": duplicate_by_id,
            "title_match": duplicate_by_title,
            "content_similarity": duplicate_by_hash,
        },
        "duplicate_groups": len(duplicates),
        "retention_rate": (
            round(len(unique_items) / len(content_items) * 100, 2) if content_items else 0
        ),
    }

    return unique_items, report


def process_segment(gender: str, age_bucket: str, date_str: str = None) -> Dict:
    """
    Process deduplication for a specific segment.

    Args:
        gender: Gender segment (women/men)
        age_bucket: Age bucket (10-13, 14-17, 18-23)
        date_str: Optional date string (YYYY-MM-DD), defaults to today

    Returns:
        Processing results dictionary
    """
    if date_str is None:
        date_str = datetime.now().strftime("%Y-%m-%d")

    # Define paths
    scores_dir = Path(f"src/Generator/scores/{gender}/{age_bucket}")
    input_file = scores_dir / f"content_scores_{date_str}.json"

    # Check if input file exists
    if not input_file.exists():
        print(f"⚠️  Input file not found: {input_file}")
        return {"status": "skipped", "reason": "input_file_not_found", "path": str(input_file)}

    # Load content scores
    try:
        with open(input_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        content_items = data if isinstance(data, list) else data.get("items", [])

        if not content_items:
            print(f"⚠️  No content items found in {input_file}")
            return {"status": "skipped", "reason": "no_content_items"}

        print(f"📥 Loaded {len(content_items)} items from {input_file}")

    except Exception as e:
        print(f"❌ Error loading {input_file}: {e}")
        return {"status": "error", "reason": str(e)}

    # Perform deduplication
    unique_items, dedup_report = deduplicate_content(content_items)

    # Save deduplicated content
    output_file = scores_dir / f"content_deduped_{date_str}.json"
    try:
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(unique_items, f, indent=2, ensure_ascii=False)
        print(f"✅ Saved {len(unique_items)} unique items to {output_file}")
    except Exception as e:
        print(f"❌ Error saving deduplicated content: {e}")
        return {"status": "error", "reason": f"save_failed: {e}"}

    # Save deduplication report
    report_file = scores_dir / f"dedup_report_{date_str}.json"
    try:
        full_report = {
            **dedup_report,
            "segment": gender,
            "age_bucket": age_bucket,
            "date": date_str,
            "input_file": str(input_file),
            "output_file": str(output_file),
            "retained_items": [
                {
                    "content_id": item.get("content_id", item.get("id", "")),
                    "title": item.get("title", "")[:100],
                    "score": item.get("viral_score", 0) + item.get("quality_score", 0),
                }
                for item in unique_items[:20]  # Top 20 for report
            ],
        }

        with open(report_file, "w", encoding="utf-8") as f:
            json.dump(full_report, f, indent=2, ensure_ascii=False)
        print(f"📊 Deduplication report saved to {report_file}")

    except Exception as e:
        print(f"⚠️  Could not save report: {e}")

    return {"status": "success", "segment": f"{gender}/{age_bucket}", **dedup_report}


def main():
    """
    Main entry point for deduplication script.

    Usage:
        python scripts/deduplicate_content.py
        python scripts/deduplicate_content.py --segment women --age 18-23
        python scripts/deduplicate_content.py --date 2025-01-15
    """
    import argparse

    parser = argparse.ArgumentParser(description="Deduplicate content from quality-scored stories")
    parser.add_argument(
        "--segment", choices=["women", "men"], help="Process specific gender segment"
    )
    parser.add_argument(
        "--age", choices=["10-13", "14-17", "18-23"], help="Process specific age bucket"
    )
    parser.add_argument("--date", help="Date string (YYYY-MM-DD), defaults to today")
    parser.add_argument("--all", action="store_true", help="Process all segments")

    args = parser.parse_args()

    print("\n" + "=" * 60)
    print("CONTENT DEDUPLICATION")
    print("=" * 60)

    # Determine segments to process
    if args.segment and args.age:
        segments = [(args.segment, args.age)]
    elif args.all or (not args.segment and not args.age):
        # Process all segments
        segments = [
            ("women", "10-13"),
            ("women", "14-17"),
            ("women", "18-23"),
            ("men", "10-13"),
            ("men", "14-17"),
            ("men", "18-23"),
        ]
    else:
        print("❌ Error: Must specify both --segment and --age, or use --all")
        return 1

    # Process each segment
    results = []
    for gender, age_bucket in segments:
        print(f"\n🎯 Processing {gender}/{age_bucket}...")
        result = process_segment(gender, age_bucket, args.date)
        results.append(result)

        if result["status"] == "success":
            print(f"   ✅ {result['unique_items']} unique / {result['total_input_items']} total")
            print(
                f"   📉 Removed {result['total_duplicates']} duplicates ({100-result['retention_rate']:.1f}%)"
            )

    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)

    successful = [r for r in results if r["status"] == "success"]
    if successful:
        total_input = sum(r.get("total_input_items", 0) for r in successful)
        total_unique = sum(r.get("unique_items", 0) for r in successful)
        total_duplicates = sum(r.get("total_duplicates", 0) for r in successful)

        print(f"✨ Processed {len(successful)} segments")
        print(f"📊 Total: {total_unique} unique / {total_input} input")
        print(f"🗑️  Removed: {total_duplicates} duplicates")
        print(f"📈 Overall retention rate: {total_unique/total_input*100:.1f}%")
    else:
        print("⚠️  No segments processed successfully")

    print("=" * 60 + "\n")

    return 0


if __name__ == "__main__":
    sys.exit(main())
