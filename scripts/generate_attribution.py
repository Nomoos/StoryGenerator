#!/usr/bin/env python3
"""
Source Attribution Generator for StoryGenerator

Extracts and stores attribution metadata for scraped content.
Ensures proper source tracking and attribution for compliance and transparency.

This script processes scraped content and generates attribution files
containing source information, author details, and usage rights.
"""

import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional
import argparse


def determine_license(source_type: str, subreddit: Optional[str] = None) -> str:
    """
    Determine the license type based on source and content type.
    
    Args:
        source_type: Type of source (e.g., 'reddit', 'twitter', 'quora')
        subreddit: Name of the subreddit (for Reddit sources)
    
    Returns:
        License information string
    """
    if source_type.lower() == "reddit":
        # Reddit content is subject to Reddit's User Agreement and Content Policy
        return "Reddit User Agreement - Fair Use for Transformative Works"
    elif source_type.lower() == "twitter":
        return "Twitter Terms of Service - Fair Use"
    elif source_type.lower() == "quora":
        return "Quora Terms of Service - Fair Use"
    else:
        return "Fair Use - Transformative Work"


def determine_usage_rights(source_type: str) -> str:
    """
    Determine usage rights based on source type and content policy.
    
    Args:
        source_type: Type of source (e.g., 'reddit', 'twitter', 'quora')
    
    Returns:
        Usage rights description
    """
    if source_type.lower() == "reddit":
        return "Transformative use for creative storytelling. Original attribution preserved."
    elif source_type.lower() == "twitter":
        return "Transformative use under fair use doctrine. Original source credited."
    else:
        return "Transformative use for educational and entertainment purposes."


def create_attribution_metadata(
    content_id: str,
    source_url: str,
    author: str,
    source_type: str = "reddit",
    subreddit: Optional[str] = None,
    scraped_date: Optional[str] = None,
    additional_metadata: Optional[Dict] = None
) -> Dict:
    """
    Create attribution metadata for a piece of content.
    
    Args:
        content_id: Unique identifier for the content
        source_url: Full URL to the original content
        author: Author/creator of the original content
        source_type: Type of source (default: 'reddit')
        subreddit: Subreddit name (for Reddit sources)
        scraped_date: ISO-8601 formatted date when content was scraped
        additional_metadata: Optional additional metadata to include
    
    Returns:
        Dictionary containing attribution metadata
    """
    if scraped_date is None:
        scraped_date = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    
    attribution = {
        "content_id": content_id,
        "source_url": source_url,
        "author": author,
        "source_type": source_type,
        "license": determine_license(source_type, subreddit),
        "date_scraped": scraped_date,
        "usage_rights": determine_usage_rights(source_type),
        "attribution_generated": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    }
    
    # Add subreddit for Reddit sources
    if subreddit:
        attribution["subreddit"] = subreddit
    
    # Include any additional metadata
    if additional_metadata:
        attribution["additional_info"] = additional_metadata
    
    return attribution


def save_attribution_file(
    attribution_data: Dict,
    output_dir: Path,
    content_id: str
) -> Path:
    """
    Save attribution metadata to a JSON file.
    
    Args:
        attribution_data: Attribution metadata dictionary
        output_dir: Directory where attribution file should be saved
        content_id: Unique identifier for the content
    
    Returns:
        Path to the saved attribution file
    """
    # Ensure output directory exists
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Create filename
    filename = f"attribution_{content_id}.json"
    filepath = output_dir / filename
    
    # Save to file
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(attribution_data, f, indent=2, ensure_ascii=False)
    
    return filepath


def process_reddit_story(
    story: Dict,
    gender: str,
    age_bucket: str,
    base_output_dir: Path
) -> Path:
    """
    Process a Reddit story and generate its attribution file.
    
    Args:
        story: Dictionary containing story data (from scraper output)
        gender: Target gender segment ('women' or 'men')
        age_bucket: Target age bucket ('10-13', '14-17', '18-23')
        base_output_dir: Base directory for output files
    
    Returns:
        Path to the created attribution file
    """
    content_id = story.get("id")
    source_url = story.get("url")
    author = story.get("author", "[deleted]")
    subreddit = story.get("subreddit", "").replace("r/", "")
    scraped_date = story.get("created_utc") or story.get("scraped_at")
    
    # Extract additional useful metadata
    additional_metadata = {
        "title": story.get("title"),
        "upvotes": story.get("upvotes"),
        "num_comments": story.get("num_comments"),
        "awards": story.get("awards", 0)
    }
    
    # Create attribution metadata
    attribution = create_attribution_metadata(
        content_id=content_id,
        source_url=source_url,
        author=author,
        source_type="reddit",
        subreddit=subreddit,
        scraped_date=scraped_date,
        additional_metadata=additional_metadata
    )
    
    # Determine output directory
    output_dir = base_output_dir / "sources" / "reddit" / gender / age_bucket
    
    # Save attribution file
    filepath = save_attribution_file(attribution, output_dir, content_id)
    
    return filepath


def process_scraped_content_file(
    input_file: Path,
    base_output_dir: Path,
    verbose: bool = False
) -> List[Path]:
    """
    Process a scraped content JSON file and generate attribution files.
    
    Args:
        input_file: Path to the scraped content JSON file
        base_output_dir: Base directory for output files
        verbose: Whether to print verbose output
    
    Returns:
        List of paths to created attribution files
    """
    if verbose:
        print(f"📖 Reading: {input_file}")
    
    # Load scraped content
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Extract metadata
    gender = data.get("segment")
    age_bucket = data.get("age_bucket")
    stories = data.get("stories", [])
    
    if verbose:
        print(f"   Segment: {gender}/{age_bucket}")
        print(f"   Stories: {len(stories)}")
    
    created_files = []
    
    # Process each story
    for story in stories:
        try:
            filepath = process_reddit_story(story, gender, age_bucket, base_output_dir)
            created_files.append(filepath)
            
            if verbose:
                print(f"   ✅ Created: {filepath.name}")
        except Exception as e:
            content_id = story.get("id", "unknown")
            print(f"   ⚠️  Error processing story {content_id}: {e}")
    
    return created_files


def process_directory(
    input_dir: Path,
    base_output_dir: Path,
    pattern: str = "*.json",
    verbose: bool = False
) -> int:
    """
    Process all scraped content files in a directory.
    
    Args:
        input_dir: Directory containing scraped content files
        base_output_dir: Base directory for output files
        pattern: File pattern to match (default: '*.json')
        verbose: Whether to print verbose output
    
    Returns:
        Total number of attribution files created
    """
    total_created = 0
    
    # Find all matching files
    json_files = list(input_dir.rglob(pattern))
    
    if verbose:
        print(f"🔍 Found {len(json_files)} files matching '{pattern}'\n")
    
    for json_file in json_files:
        try:
            created_files = process_scraped_content_file(
                json_file,
                base_output_dir,
                verbose=verbose
            )
            total_created += len(created_files)
        except Exception as e:
            print(f"❌ Error processing {json_file}: {e}")
    
    return total_created


def main():
    """Main entry point for the attribution generator."""
    parser = argparse.ArgumentParser(
        description="Generate attribution metadata for scraped content"
    )
    parser.add_argument(
        "input",
        type=str,
        help="Input file or directory containing scraped content"
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default="src/Generator",
        help="Base output directory (default: src/Generator)"
    )
    parser.add_argument(
        "--pattern",
        type=str,
        default="reddit_scraped_*.json",
        help="File pattern for directory processing (default: reddit_scraped_*.json)"
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable verbose output"
    )
    
    args = parser.parse_args()
    
    # Resolve paths
    input_path = Path(args.input).resolve()
    output_dir = Path(args.output_dir).resolve()
    
    print("=" * 60)
    print("Source Attribution Generator")
    print("=" * 60)
    print(f"Input:  {input_path}")
    print(f"Output: {output_dir}")
    print("=" * 60)
    print()
    
    # Process input
    if input_path.is_file():
        created_files = process_scraped_content_file(
            input_path,
            output_dir,
            verbose=args.verbose
        )
        total_created = len(created_files)
    elif input_path.is_dir():
        total_created = process_directory(
            input_path,
            output_dir,
            pattern=args.pattern,
            verbose=args.verbose
        )
    else:
        print(f"❌ Error: Input path does not exist: {input_path}")
        return 1
    
    print()
    print("=" * 60)
    print(f"✅ Successfully created {total_created} attribution files")
    print("=" * 60)
    
    return 0


if __name__ == "__main__":
    exit(main())
