#!/usr/bin/env python3
"""
Standalone Multi-Platform Video Publishing Script for StoryGenerator

Publish videos to YouTube, TikTok, Instagram, and Facebook with a single command.

Usage:
    # Publish to YouTube only
    python scripts/publish_video.py video.mp4 --platforms youtube --title "My Video"

    # Publish to multiple platforms
    python scripts/publish_video.py video.mp4 \\
        --platforms youtube tiktok instagram \\
        --title "Amazing Story" \\
        --description "Check out this incredible story!" \\
        --tags shorts viral ai story

    # Schedule upload
    python scripts/publish_video.py video.mp4 \\
        --platforms youtube \\
        --title "Scheduled Video" \\
        --schedule "2025-10-11 10:00:00"

    # Publish with custom metadata per platform
    python scripts/publish_video.py video.mp4 \\
        --platforms youtube instagram \\
        --metadata-file metadata.json
"""

import os
import sys
import json
import argparse
from pathlib import Path
from datetime import datetime

# Add src/Python directory to path - but do it carefully to avoid shadowing std library
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
src_python = os.path.join(project_root, "src", "Python")
if src_python not in sys.path:
    sys.path.append(src_python)

from Tools.MultiPlatformPublisher import (
    MultiPlatformPublisher,
    Platform,
    PlatformMetadata,
    UploadStatus
)


def load_metadata_from_file(metadata_file: str) -> dict:
    """Load metadata from JSON file."""
    with open(metadata_file, 'r', encoding='utf-8') as f:
        return json.load(f)


def publish_single_video(
    video_path: str,
    platforms: list,
    title: str = None,
    description: str = None,
    tags: list = None,
    privacy: str = 'public',
    thumbnail: str = None,
    metadata_file: str = None,
    output_dir: str = None,
    credentials_dir: str = None,
    schedule: str = None
):
    """
    Publish a single video to selected platforms.
    
    Args:
        video_path: Path to video file
        platforms: List of platform names
        title: Video title
        description: Video description
        tags: List of tags
        privacy: Privacy setting (public/unlisted/private)
        thumbnail: Path to thumbnail image
        metadata_file: JSON file with platform-specific metadata
        output_dir: Directory to save reports
        credentials_dir: Directory with credentials
        schedule: Scheduled time (format: YYYY-MM-DD HH:MM:SS)
    """
    print(f"\n{'='*70}")
    print(f"Multi-Platform Video Publisher")
    print(f"{'='*70}")
    
    # Convert platform names to enum
    platform_enums = [Platform(p) for p in platforms]
    
    # Initialize publisher
    publisher = MultiPlatformPublisher(
        output_dir=output_dir,
        credentials_dir=credentials_dir,
        enable_platforms=platform_enums
    )
    
    # Prepare metadata
    if metadata_file:
        # Load from file
        metadata = load_metadata_from_file(metadata_file)
        # Convert dicts to PlatformMetadata objects
        for key, value in metadata.items():
            if isinstance(value, dict):
                metadata[key] = PlatformMetadata(**value)
    else:
        # Use command-line arguments
        metadata = {}
        for platform in platform_enums:
            metadata[platform.value] = PlatformMetadata(
                title=title or Path(video_path).stem,
                description=description or '',
                tags=tags or [],
                privacy=privacy,
                thumbnail_path=thumbnail
            )
    
    print(f"\nVideo: {video_path}")
    print(f"Platforms: {', '.join(p.value for p in platform_enums)}")
    
    if title:
        print(f"Title: {title}")
    if description:
        print(f"Description: {description[:60]}{'...' if len(description) > 60 else ''}")
    if tags:
        print(f"Tags: {', '.join(tags)}")
    print(f"Privacy: {privacy}")
    
    # Check if scheduling
    if schedule:
        try:
            scheduled_time = datetime.strptime(schedule, "%Y-%m-%d %H:%M:%S")
            print(f"\n⏰ Scheduling upload for: {scheduled_time}")
            
            task = publisher.schedule_upload(
                video_path=video_path,
                metadata=metadata,
                platforms=platform_enums,
                scheduled_time=scheduled_time
            )
            
            print(f"✓ Upload scheduled successfully")
            print(f"\nTo process scheduled uploads, run:")
            print(f"  python scripts/publish_video.py --process-queue")
            
            return
            
        except ValueError as e:
            print(f"❌ Invalid date format: {e}")
            print(f"Use format: YYYY-MM-DD HH:MM:SS")
            return
    
    # Publish immediately
    print(f"\n{'='*70}")
    print(f"Uploading...")
    print(f"{'='*70}\n")
    
    results = publisher.publish_to_all(
        video_path=video_path,
        metadata=metadata,
        platforms=platform_enums,
        save_report=True
    )
    
    # Display results
    print(f"\n{'='*70}")
    print(f"Upload Results")
    print(f"{'='*70}\n")
    
    for result in results:
        status_icon = "✅" if result.status == UploadStatus.SUCCESS else "❌"
        print(f"{status_icon} {result.platform.value.upper()}")
        
        if result.status == UploadStatus.SUCCESS:
            print(f"   URL: {result.url}")
            print(f"   Video ID: {result.video_id}")
            if result.message:
                print(f"   Message: {result.message}")
        else:
            print(f"   ❌ Error: {result.error}")
        print()
    
    # Summary
    success_count = sum(1 for r in results if r.status == UploadStatus.SUCCESS)
    failed_count = len(results) - success_count
    
    print(f"{'='*70}")
    print(f"Summary: {success_count} succeeded, {failed_count} failed")
    print(f"{'='*70}\n")
    
    return success_count == len(results)


def process_upload_queue(output_dir: str = None, credentials_dir: str = None, dry_run: bool = False):
    """Process scheduled uploads in the queue."""
    print(f"\n{'='*70}")
    print(f"Processing Upload Queue")
    print(f"{'='*70}\n")
    
    publisher = MultiPlatformPublisher(
        output_dir=output_dir,
        credentials_dir=credentials_dir
    )
    
    if not publisher.upload_queue:
        print("No pending uploads in queue")
        return
    
    print(f"Found {len(publisher.upload_queue)} pending upload(s)")
    
    if dry_run:
        print("\n[DRY RUN MODE - No actual uploads will be performed]\n")
    
    processed = publisher.process_queue(dry_run=dry_run)
    
    print(f"\nProcessed {len(processed)} upload(s)")
    
    for task in processed:
        status_icon = "✅" if task.status == UploadStatus.SUCCESS else "❌"
        print(f"{status_icon} {task.video_path}")
        print(f"   Platforms: {', '.join(p.value for p in task.platforms)}")
        print(f"   Status: {task.status.value}")
        print()


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Publish videos to multiple platforms',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    
    # Main arguments
    parser.add_argument(
        'video_path',
        nargs='?',
        help='Path to video file'
    )
    
    parser.add_argument(
        '--platforms',
        nargs='+',
        choices=['youtube', 'tiktok', 'instagram', 'facebook'],
        help='Platforms to publish to'
    )
    
    parser.add_argument(
        '--title',
        help='Video title'
    )
    
    parser.add_argument(
        '--description',
        help='Video description'
    )
    
    parser.add_argument(
        '--tags',
        nargs='+',
        help='Video tags'
    )
    
    parser.add_argument(
        '--privacy',
        choices=['public', 'unlisted', 'private'],
        default='public',
        help='Privacy setting (default: public)'
    )
    
    parser.add_argument(
        '--thumbnail',
        help='Path to thumbnail image'
    )
    
    parser.add_argument(
        '--metadata-file',
        help='JSON file with platform-specific metadata'
    )
    
    parser.add_argument(
        '--schedule',
        help='Schedule upload for later (format: YYYY-MM-DD HH:MM:SS)'
    )
    
    # Queue processing
    parser.add_argument(
        '--process-queue',
        action='store_true',
        help='Process scheduled uploads in queue'
    )
    
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Simulate queue processing without uploading'
    )
    
    # Configuration
    parser.add_argument(
        '--output-dir',
        help='Directory to save upload reports'
    )
    
    parser.add_argument(
        '--credentials-dir',
        help='Directory containing platform credentials'
    )
    
    args = parser.parse_args()
    
    try:
        # Check if processing queue
        if args.process_queue:
            process_upload_queue(
                output_dir=args.output_dir,
                credentials_dir=args.credentials_dir,
                dry_run=args.dry_run
            )
            return 0
        
        # Otherwise, publishing a video
        if not args.video_path:
            parser.error("video_path is required when not using --process-queue")
        
        if not args.platforms and not args.metadata_file:
            parser.error("--platforms is required when not using --metadata-file")
        
        if not args.title and not args.metadata_file:
            parser.error("--title is required when not using --metadata-file")
        
        # Check video exists
        if not os.path.exists(args.video_path):
            print(f"❌ Error: Video file not found: {args.video_path}")
            return 1
        
        # Publish video
        success = publish_single_video(
            video_path=args.video_path,
            platforms=args.platforms or [],
            title=args.title,
            description=args.description,
            tags=args.tags,
            privacy=args.privacy,
            thumbnail=args.thumbnail,
            metadata_file=args.metadata_file,
            output_dir=args.output_dir,
            credentials_dir=args.credentials_dir,
            schedule=args.schedule
        )
        
        return 0 if success else 1
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Upload cancelled by user")
        return 1
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    exit(main())
