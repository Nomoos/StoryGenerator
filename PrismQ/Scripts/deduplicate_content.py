#!/usr/bin/env python3
"""
Content Deduplication Script for StoryGenerator (Enhanced v2.0)

Detects and removes duplicate content from quality-scored stories.
Implements multiple deduplication strategies:
1. Exact ID matching
2. Fuzzy title matching (normalized)
3. Content similarity (text hash)
4. Advanced fuzzy matching (Levenshtein distance) - NEW
5. Semantic similarity (sentence embeddings) - NEW

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
from typing import List, Dict, Set, Tuple, Optional
from collections import defaultdict

# Enhanced deduplication dependencies
try:
    from fuzzywuzzy import fuzz
    FUZZY_AVAILABLE = True
except ImportError:
    FUZZY_AVAILABLE = False
    print("⚠️  fuzzywuzzy not available. Install with: pip install fuzzywuzzy python-Levenshtein")

try:
    from sentence_transformers import SentenceTransformer, util
    import torch
    SEMANTIC_AVAILABLE = True
except ImportError:
    SEMANTIC_AVAILABLE = False
    torch = None  # Define as None for type hints
    SentenceTransformer = None
    print("⚠️  sentence-transformers not available. Install with: pip install sentence-transformers")


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


def check_fuzzy_duplicate(text: str, seen_texts: List[Tuple[str, str]], threshold: int = 85) -> Tuple[bool, float, str]:
    """
    Check if text is a fuzzy duplicate using Levenshtein distance.
    
    Args:
        text: Text to check
        seen_texts: List of (text, id) tuples already seen
        threshold: Similarity threshold (0-100), default 85
    
    Returns:
        Tuple of (is_duplicate, similarity_score, matched_id)
    """
    if not FUZZY_AVAILABLE or not text:
        return False, 0.0, ""
    
    for seen_text, seen_id in seen_texts:
        # Use token_sort_ratio for word-order independence
        similarity = fuzz.token_sort_ratio(text.lower(), seen_text.lower())
        
        if similarity >= threshold:
            return True, similarity, seen_id
    
    return False, 0.0, ""


def check_semantic_duplicate(
    text: str, 
    seen_embeddings: List[Tuple], 
    model: Optional,
    threshold: float = 0.90
) -> Tuple[bool, float, str]:
    """
    Check if text is semantically similar using sentence embeddings.
    
    Args:
        text: Text to check
        seen_embeddings: List of (embedding, id) tuples already seen
        model: SentenceTransformer model for encoding
        threshold: Similarity threshold (0-1), default 0.90
    
    Returns:
        Tuple of (is_duplicate, similarity_score, matched_id)
    """
    if not SEMANTIC_AVAILABLE or not model or not text or not seen_embeddings:
        return False, 0.0, ""
    
    try:
        # Encode new text (use first 500 chars for performance)
        text_sample = text[:500]
        new_embedding = model.encode(text_sample, convert_to_tensor=True, show_progress_bar=False)
        
        # Compare with all seen embeddings
        for seen_embedding, seen_id in seen_embeddings:
            similarity = util.cos_sim(new_embedding, seen_embedding).item()
            
            if similarity >= threshold:
                return True, similarity, seen_id
        
        return False, 0.0, ""
    
    except Exception as e:
        print(f"⚠️  Semantic check error: {e}")
        return False, 0.0, ""


def deduplicate_content(
    content_items: List[Dict],
    use_fuzzy: bool = True,
    use_semantic: bool = True,
    fuzzy_threshold: int = 85,
    semantic_threshold: float = 0.90,
    semantic_model_name: str = "all-MiniLM-L6-v2"
) -> Tuple[List[Dict], Dict]:
    """
    Remove duplicate content using multiple strategies (enhanced v2.0).

    Deduplication strategies:
    1. Exact ID match (same content_id)
    2. Fuzzy title match (normalized title)
    3. Content hash match (similar text content)
    4. Advanced fuzzy matching (Levenshtein distance) - NEW
    5. Semantic similarity (sentence embeddings) - NEW

    When duplicates are found, keeps the highest scoring item.

    Args:
        content_items: List of content dictionaries with scores
        use_fuzzy: Enable advanced fuzzy matching (requires fuzzywuzzy)
        use_semantic: Enable semantic similarity (requires sentence-transformers)
        fuzzy_threshold: Similarity threshold for fuzzy matching (0-100)
        semantic_threshold: Similarity threshold for semantic matching (0-1)
        semantic_model_name: Model name for sentence-transformers

    Returns:
        Tuple of (unique_items, report_dict)
    """
    # Load semantic model if enabled
    semantic_model = None
    if use_semantic and SEMANTIC_AVAILABLE:
        try:
            print(f"📥 Loading semantic model: {semantic_model_name}...")
            semantic_model = SentenceTransformer(semantic_model_name)
            print(f"✅ Semantic model loaded")
        except Exception as e:
            print(f"⚠️  Could not load semantic model: {e}")
            use_semantic = False
    
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
    
    # Enhanced tracking for fuzzy and semantic matching
    seen_title_texts: List[Tuple[str, str]] = []  # (title_text, id)
    seen_content_texts: List[Tuple[str, str]] = []  # (content_text, id)
    seen_embeddings: List[Tuple] = []  # (embedding, id)

    # Results
    unique_items: List[Dict] = []
    duplicates: Dict[str, List[Dict]] = defaultdict(list)

    # Statistics
    duplicate_by_id = 0
    duplicate_by_title = 0
    duplicate_by_hash = 0
    duplicate_by_fuzzy_title = 0
    duplicate_by_fuzzy_content = 0
    duplicate_by_semantic = 0

    for item in sorted_items:
        content_id = item.get("content_id", item.get("id", ""))
        title = item.get("title", "")
        text = item.get("text", "")

        is_duplicate = False
        duplicate_reason = None
        similarity_score = 0.0

        # Check 1: Exact ID match
        if content_id and content_id in seen_ids:
            duplicate_by_id += 1
            is_duplicate = True
            duplicate_reason = "exact_id_match"
            similarity_score = 1.0
            duplicates[content_id].append(item)

        # Check 2: Fuzzy title match (normalized)
        elif title:
            normalized_title = normalize_text(title)
            if normalized_title in seen_titles:
                duplicate_by_title += 1
                is_duplicate = True
                duplicate_reason = "title_match"
                similarity_score = 1.0
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
                similarity_score = 1.0
                # Find the original for tracking
                for unique_item in unique_items:
                    if calculate_content_hash(unique_item) == content_hash:
                        orig_id = unique_item.get("content_id", unique_item.get("id", "unknown"))
                        duplicates[f"hash:{orig_id}"].append(item)
                        break

        # Check 4: Advanced fuzzy title matching (NEW)
        if not is_duplicate and use_fuzzy and FUZZY_AVAILABLE and title:
            is_fuzzy_dup, fuzzy_sim, matched_id = check_fuzzy_duplicate(
                title, seen_title_texts, fuzzy_threshold
            )
            if is_fuzzy_dup:
                duplicate_by_fuzzy_title += 1
                is_duplicate = True
                duplicate_reason = "fuzzy_title_match"
                similarity_score = fuzzy_sim / 100.0
                duplicates[f"fuzzy_title:{matched_id}"].append(item)

        # Check 5: Advanced fuzzy content matching (NEW)
        if not is_duplicate and use_fuzzy and FUZZY_AVAILABLE and text:
            is_fuzzy_dup, fuzzy_sim, matched_id = check_fuzzy_duplicate(
                text[:500], seen_content_texts, fuzzy_threshold
            )
            if is_fuzzy_dup:
                duplicate_by_fuzzy_content += 1
                is_duplicate = True
                duplicate_reason = "fuzzy_content_match"
                similarity_score = fuzzy_sim / 100.0
                duplicates[f"fuzzy_content:{matched_id}"].append(item)

        # Check 6: Semantic similarity matching (NEW)
        if not is_duplicate and use_semantic and semantic_model and text:
            is_sem_dup, sem_sim, matched_id = check_semantic_duplicate(
                text, seen_embeddings, semantic_model, semantic_threshold
            )
            if is_sem_dup:
                duplicate_by_semantic += 1
                is_duplicate = True
                duplicate_reason = "semantic_similarity"
                similarity_score = sem_sim
                duplicates[f"semantic:{matched_id}"].append(item)

        # Add to results if unique
        if not is_duplicate:
            unique_items.append(item)
            if content_id:
                seen_ids.add(content_id)
            if title:
                seen_titles.add(normalize_text(title))
                if use_fuzzy and FUZZY_AVAILABLE:
                    seen_title_texts.append((title, content_id or f"item_{len(unique_items)}"))
            seen_hashes.add(calculate_content_hash(item))
            
            if text:
                if use_fuzzy and FUZZY_AVAILABLE:
                    seen_content_texts.append((text[:500], content_id or f"item_{len(unique_items)}"))
                
                if use_semantic and semantic_model:
                    try:
                        embedding = semantic_model.encode(
                            text[:500], 
                            convert_to_tensor=True,
                            show_progress_bar=False
                        )
                        seen_embeddings.append((embedding, content_id or f"item_{len(unique_items)}"))
                    except Exception as e:
                        print(f"⚠️  Could not create embedding: {e}")
        else:
            # Add duplicate reason and similarity to item for reporting
            item["duplicate_reason"] = duplicate_reason
            item["similarity_score"] = similarity_score

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
            "fuzzy_title_match": duplicate_by_fuzzy_title,
            "fuzzy_content_match": duplicate_by_fuzzy_content,
            "semantic_similarity": duplicate_by_semantic,
        },
        "duplicate_groups": len(duplicates),
        "retention_rate": (
            round(len(unique_items) / len(content_items) * 100, 2) if content_items else 0
        ),
        "features_used": {
            "fuzzy_matching": use_fuzzy and FUZZY_AVAILABLE,
            "semantic_matching": use_semantic and SEMANTIC_AVAILABLE,
            "fuzzy_threshold": fuzzy_threshold if use_fuzzy else None,
            "semantic_threshold": semantic_threshold if use_semantic else None,
            "semantic_model": semantic_model_name if use_semantic and semantic_model else None,
        },
    }

    return unique_items, report


def process_segment(
    gender: str, 
    age_bucket: str, 
    date_str: str = None,
    use_fuzzy: bool = True,
    use_semantic: bool = True,
    fuzzy_threshold: int = 85,
    semantic_threshold: float = 0.90
) -> Dict:
    """
    Process deduplication for a specific segment (enhanced v2.0).

    Args:
        gender: Gender segment (women/men)
        age_bucket: Age bucket (10-13, 14-17, 18-23)
        date_str: Optional date string (YYYY-MM-DD), defaults to today
        use_fuzzy: Enable advanced fuzzy matching
        use_semantic: Enable semantic similarity detection
        fuzzy_threshold: Similarity threshold for fuzzy matching (0-100)
        semantic_threshold: Similarity threshold for semantic matching (0-1)

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
    unique_items, dedup_report = deduplicate_content(
        content_items,
        use_fuzzy=use_fuzzy,
        use_semantic=use_semantic,
        fuzzy_threshold=fuzzy_threshold,
        semantic_threshold=semantic_threshold
    )

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
    Main entry point for deduplication script (enhanced v2.0).

    Usage:
        python scripts/deduplicate_content.py
        python scripts/deduplicate_content.py --segment women --age 18-23
        python scripts/deduplicate_content.py --date 2025-01-15
        python scripts/deduplicate_content.py --no-fuzzy --no-semantic  # Basic mode only
        python scripts/deduplicate_content.py --fuzzy-threshold 90 --semantic-threshold 0.85
    """
    import argparse

    parser = argparse.ArgumentParser(
        description="Deduplicate content from quality-scored stories (Enhanced v2.0)"
    )
    parser.add_argument(
        "--segment", choices=["women", "men"], help="Process specific gender segment"
    )
    parser.add_argument(
        "--age", choices=["10-13", "14-17", "18-23"], help="Process specific age bucket"
    )
    parser.add_argument("--date", help="Date string (YYYY-MM-DD), defaults to today")
    parser.add_argument("--all", action="store_true", help="Process all segments")
    
    # Enhanced features
    parser.add_argument(
        "--no-fuzzy", action="store_true", 
        help="Disable advanced fuzzy matching (Levenshtein distance)"
    )
    parser.add_argument(
        "--no-semantic", action="store_true",
        help="Disable semantic similarity detection (embeddings)"
    )
    parser.add_argument(
        "--fuzzy-threshold", type=int, default=85,
        help="Fuzzy matching similarity threshold (0-100, default: 85)"
    )
    parser.add_argument(
        "--semantic-threshold", type=float, default=0.90,
        help="Semantic similarity threshold (0-1, default: 0.90)"
    )

    args = parser.parse_args()

    print("\n" + "=" * 60)
    print("CONTENT DEDUPLICATION (Enhanced v2.0)")
    print("=" * 60)
    
    # Show configuration
    print(f"\n📋 Configuration:")
    print(f"   Fuzzy matching: {'✅ Enabled' if not args.no_fuzzy and FUZZY_AVAILABLE else '❌ Disabled'}")
    if not args.no_fuzzy and FUZZY_AVAILABLE:
        print(f"   Fuzzy threshold: {args.fuzzy_threshold}%")
    print(f"   Semantic matching: {'✅ Enabled' if not args.no_semantic and SEMANTIC_AVAILABLE else '❌ Disabled'}")
    if not args.no_semantic and SEMANTIC_AVAILABLE:
        print(f"   Semantic threshold: {args.semantic_threshold}")
    print()

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
        result = process_segment(
            gender, 
            age_bucket, 
            args.date,
            use_fuzzy=not args.no_fuzzy,
            use_semantic=not args.no_semantic,
            fuzzy_threshold=args.fuzzy_threshold,
            semantic_threshold=args.semantic_threshold
        )
        results.append(result)

        if result["status"] == "success":
            print(f"   ✅ {result['unique_items']} unique / {result['total_input_items']} total")
            print(
                f"   📉 Removed {result['total_duplicates']} duplicates ({100-result['retention_rate']:.1f}%)"
            )
            
            # Show breakdown by duplicate type
            dup_types = result.get('duplicates_by_type', {})
            if any(dup_types.values()):
                print(f"   📊 Breakdown:")
                for dup_type, count in dup_types.items():
                    if count > 0:
                        print(f"      - {dup_type}: {count}")

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
