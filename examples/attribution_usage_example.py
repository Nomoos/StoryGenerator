#!/usr/bin/env python3
"""
Example usage of the source attribution system.

This script demonstrates how to use the attribution generator
programmatically to create attribution metadata for content.
"""

import sys
import json
import tempfile
from pathlib import Path

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from generate_attribution import (
    create_attribution_metadata,
    save_attribution_file,
    process_reddit_story,
    process_scraped_content_file,
)


def example_1_basic_attribution():
    """Example 1: Create basic attribution metadata."""
    print("\n" + "=" * 60)
    print("Example 1: Basic Attribution Metadata")
    print("=" * 60)

    attribution = create_attribution_metadata(
        content_id="abc123",
        source_url="https://reddit.com/r/relationships/comments/abc123",
        author="throwaway_user",
        source_type="reddit",
        subreddit="relationships",
    )

    print("\nGenerated attribution metadata:")
    print(json.dumps(attribution, indent=2))


def example_2_with_additional_info():
    """Example 2: Create attribution with additional metadata."""
    print("\n" + "=" * 60)
    print("Example 2: Attribution with Additional Info")
    print("=" * 60)

    additional_info = {
        "title": "Need relationship advice",
        "upvotes": 1250,
        "num_comments": 340,
        "awards": 5,
    }

    attribution = create_attribution_metadata(
        content_id="def456",
        source_url="https://reddit.com/r/dating_advice/comments/def456",
        author="advice_seeker",
        source_type="reddit",
        subreddit="dating_advice",
        scraped_date="2024-01-15T10:30:00Z",
        additional_metadata=additional_info,
    )

    print("\nGenerated attribution with additional info:")
    print(json.dumps(attribution, indent=2))


def example_3_save_to_file():
    """Example 3: Save attribution to file."""
    print("\n" + "=" * 60)
    print("Example 3: Save Attribution to File")
    print("=" * 60)

    attribution = create_attribution_metadata(
        content_id="ghi789",
        source_url="https://reddit.com/r/AmItheAsshole/comments/ghi789",
        author="confused_person",
        source_type="reddit",
        subreddit="AmItheAsshole",
    )

    # Save to temporary directory
    output_dir = Path(tempfile.gettempdir()) / "attribution_example"
    filepath = save_attribution_file(attribution, output_dir, "ghi789")

    print(f"\n✅ Attribution saved to: {filepath}")
    print(f"\nFile contents:")
    with open(filepath, "r") as f:
        print(f.read())


def example_4_process_reddit_story():
    """Example 4: Process a complete Reddit story."""
    print("\n" + "=" * 60)
    print("Example 4: Process Reddit Story")
    print("=" * 60)

    # Sample Reddit story data (as would come from scraper)
    story = {
        "id": "jkl012",
        "title": "Update: She said yes!",
        "text": "Following up on my previous post...",
        "url": "https://reddit.com/r/relationships/comments/jkl012",
        "upvotes": 2500,
        "num_comments": 450,
        "created_utc": "2024-01-20T14:30:00Z",
        "subreddit": "r/relationships",
        "author": "happy_guy_123",
        "awards": 12,
        "is_self": True,
    }

    output_dir = Path(tempfile.gettempdir()) / "attribution_example"
    filepath = process_reddit_story(story, "men", "18-23", output_dir)

    print(f"\n✅ Processed story and created: {filepath}")
    print(f"\nFile contents:")
    with open(filepath, "r") as f:
        content = json.load(f)
        print(json.dumps(content, indent=2))


def example_5_batch_processing():
    """Example 5: Batch process multiple stories."""
    print("\n" + "=" * 60)
    print("Example 5: Batch Processing")
    print("=" * 60)

    # Sample scraped data file
    scraped_data = {
        "segment": "women",
        "age_bucket": "14-17",
        "subreddits": ["r/teenagers", "r/TrueOffMyChest"],
        "total_scraped": 2,
        "selected": 2,
        "scraped_at": "2024-01-21T10:00:00Z",
        "stories": [
            {
                "id": "story1",
                "title": "Story 1",
                "url": "https://reddit.com/r/teenagers/comments/story1",
                "author": "teen_user1",
                "upvotes": 500,
                "num_comments": 100,
                "created_utc": "2024-01-20T15:00:00Z",
                "subreddit": "r/teenagers",
                "awards": 1,
            },
            {
                "id": "story2",
                "title": "Story 2",
                "url": "https://reddit.com/r/TrueOffMyChest/comments/story2",
                "author": "user2",
                "upvotes": 750,
                "num_comments": 150,
                "created_utc": "2024-01-21T09:00:00Z",
                "subreddit": "r/TrueOffMyChest",
                "awards": 3,
            },
        ],
    }

    # Save to temporary file
    temp_dir = Path(tempfile.gettempdir())
    input_file = temp_dir / "batch_example.json"
    with open(input_file, "w") as f:
        json.dump(scraped_data, f)

    # Process the file
    output_dir = temp_dir / "attribution_example"
    created_files = process_scraped_content_file(input_file, output_dir, verbose=True)

    print(f"\n✅ Created {len(created_files)} attribution files:")
    for filepath in created_files:
        print(f"   - {filepath.name}")


def main():
    """Run all examples."""
    print("=" * 60)
    print("SOURCE ATTRIBUTION SYSTEM - USAGE EXAMPLES")
    print("=" * 60)

    # Run each example
    example_1_basic_attribution()
    example_2_with_additional_info()
    example_3_save_to_file()
    example_4_process_reddit_story()
    example_5_batch_processing()

    print("\n" + "=" * 60)
    print("✅ All examples completed successfully!")
    print("=" * 60)
    print("\nFor more information, see:")
    print("  - issues/p0-critical/content-pipeline/02-content-06-attribution/README.md")
    print("  - scripts/generate_attribution.py --help")
    print("  - tests/test_attribution.py")
    print()


if __name__ == "__main__":
    main()
