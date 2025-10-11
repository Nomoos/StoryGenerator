#!/usr/bin/env python3
"""
Example: Using the Batch Exporter to export multiple videos at once.
"""

import os
import sys

# Add src/Python directory to path
sys.path.insert(
    0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src", "Python")
)

from Models.StoryIdea import StoryIdea
from Tools.BatchExporter import BatchExporter
from Tools.Utils import TITLES_PATH, sanitize_filename


def create_sample_stories():
    """Create sample story ideas for demonstration."""
    stories = [
        StoryIdea(
            story_title="The Unexpected Journey",
            narrator_gender="F",
            tone="adventurous",
            theme="self-discovery",
            goal="Inspire viewers to take risks",
            potencial={"age_groups": {"20_25": 85}},
        ),
        StoryIdea(
            story_title="A Lesson in Patience",
            narrator_gender="M",
            tone="reflective",
            theme="wisdom",
            goal="Share life lessons",
            potencial={"age_groups": {"25_30": 90}},
        ),
        StoryIdea(
            story_title="The Power of Friendship",
            narrator_gender="F",
            tone="heartwarming",
            theme="relationships",
            goal="Celebrate human connections",
            potencial={"age_groups": {"18_23": 88}},
        ),
    ]
    return stories


def example_sequential_batch():
    """Example: Sequential batch export."""
    print("\n" + "=" * 60)
    print("Example 1: Sequential Batch Export")
    print("=" * 60 + "\n")

    # Create sample stories
    stories = create_sample_stories()

    # Get video paths (in real usage, these would be actual video files)
    video_paths = [
        os.path.join(TITLES_PATH, sanitize_filename(story.story_title), "final_video.mp4")
        for story in stories
    ]

    # Initialize batch exporter
    exporter = BatchExporter(max_workers=1)

    print("📦 Starting sequential batch export...")
    print(f"   Processing {len(stories)} videos one at a time\n")

    # Note: In real usage, make sure the video files exist
    # This is just a demonstration of the API
    print("⚠️  Note: This example requires actual video files to exist.")
    print("   Create videos first using the video pipeline.\n")


def example_parallel_batch():
    """Example: Parallel batch export."""
    print("\n" + "=" * 60)
    print("Example 2: Parallel Batch Export")
    print("=" * 60 + "\n")

    stories = create_sample_stories()
    video_paths = [
        os.path.join(TITLES_PATH, sanitize_filename(story.story_title), "final_video.mp4")
        for story in stories
    ]

    # Initialize with multiple workers for parallel processing
    exporter = BatchExporter(max_workers=4)

    print("📦 Starting parallel batch export...")
    print(f"   Processing {len(stories)} videos with 4 workers\n")

    # Export with custom callback for progress
    def progress_callback(current, total, title):
        print(f"   [{current}/{total}] Processing: {title}")

    print("⚠️  Note: This example requires actual video files to exist.")


def example_batch_with_options():
    """Example: Batch export with custom options."""
    print("\n" + "=" * 60)
    print("Example 3: Batch Export with Custom Options")
    print("=" * 60 + "\n")

    stories = create_sample_stories()
    video_paths = [
        os.path.join(TITLES_PATH, sanitize_filename(story.story_title), "final_video.mp4")
        for story in stories
    ]

    exporter = BatchExporter(max_workers=2)

    print("📦 Batch export with custom settings:")
    print("   - Generate thumbnails: Yes")
    print("   - Generate metadata: Yes")
    print("   - Parallel processing: Yes")
    print("   - Progress tracking: Enabled\n")


def example_retry_failed():
    """Example: Retry failed exports."""
    print("\n" + "=" * 60)
    print("Example 4: Retry Failed Exports")
    print("=" * 60 + "\n")

    print("If a batch export had failures, you can retry them:")
    print()
    print("```python")
    print("# Previous batch results")
    print("previous_results = exporter.export_batch(stories, videos)")
    print()
    print("# Retry failed exports")
    print("retry_results = exporter.retry_failed(")
    print("    previous_results, stories, videos")
    print(")")
    print("```")


def example_batch_summary():
    """Example: Understanding batch export results."""
    print("\n" + "=" * 60)
    print("Example 5: Batch Export Results")
    print("=" * 60 + "\n")

    print("Batch export returns detailed results:")
    print()
    print("Summary Structure:")
    print("  - total: Total number of videos processed")
    print("  - successful: Number of successful exports")
    print("  - failed: Number of failed exports")
    print("  - duration_seconds: Total time taken")
    print("  - avg_time_per_video: Average processing time")
    print("  - results: Detailed results for each video")
    print()
    print("Each video result includes:")
    print("  - title: Story title")
    print("  - title_id: Unique identifier")
    print("  - success: Boolean success status")
    print("  - duration: Processing time")
    print("  - video_path: Path to exported video")
    print("  - thumbnail_path: Path to thumbnail")
    print("  - metadata_path: Path to metadata JSON")
    print("  - error: Error message (if failed)")


def main():
    """Run all examples."""
    print("\n" + "=" * 60)
    print("BATCH EXPORTER - USAGE EXAMPLES")
    print("=" * 60)

    example_sequential_batch()
    example_parallel_batch()
    example_batch_with_options()
    example_retry_failed()
    example_batch_summary()

    print("\n" + "=" * 60)
    print("📚 Additional Information")
    print("=" * 60)
    print()
    print("Benefits of Batch Export:")
    print("  ✅ Process multiple videos efficiently")
    print("  ✅ Parallel processing for faster completion")
    print("  ✅ Automatic error handling and recovery")
    print("  ✅ Progress tracking and reporting")
    print("  ✅ Integration with export registry")
    print()
    print("Best Practices:")
    print("  1. Use parallel processing for large batches (4-8 workers)")
    print("  2. Monitor progress with callback functions")
    print("  3. Retry failed exports after fixing issues")
    print("  4. Check batch summary for detailed statistics")
    print()
    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()
