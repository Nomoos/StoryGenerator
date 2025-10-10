#!/usr/bin/env python3
"""
WordPress Draft Post Creation Example

This example demonstrates how to use the WordPressProvider to create
draft posts with story titles and scripts.

Usage:
    # Basic usage with environment variables
    export WORDPRESS_SITE_URL="https://mysite.wordpress.com"
    export WORDPRESS_USERNAME="admin"
    export WORDPRESS_APP_PASSWORD="xxxx xxxx xxxx xxxx"
    python examples/wordpress_integration_example.py

    # Or configure in the script
    python examples/wordpress_integration_example.py --site-url https://mysite.com
"""

import sys
import os
import argparse
from pathlib import Path

# Add providers to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from providers.wordpress_provider import WordPressProvider


def example_basic_usage():
    """Basic example of creating a draft post."""
    print("\n" + "=" * 70)
    print("Example 1: Basic Draft Post Creation")
    print("=" * 70)

    # Initialize WordPress provider
    # Credentials can be set via constructor or environment variables
    provider = WordPressProvider(
        site_url="https://example.wordpress.com",
        username="admin",
        app_password="your_app_password_here"
    )

    # Create a draft post
    result = provider.create_draft_post(
        title="An Amazing Short Story",
        content="Once upon a time, in a digital realm far away, there lived a story generator..."
    )

    if result['success']:
        print(f"✅ Draft post created successfully!")
        print(f"   Post ID: {result['post_id']}")
        print(f"   Post URL: {result['post_url']}")
        print(f"   Edit URL: {result['edit_url']}")
        print(f"   Status: {result['status']}")
    else:
        print(f"❌ Failed to create post: {result['error']}")


def example_with_script_data():
    """Example using script data from StoryGenerator."""
    print("\n" + "=" * 70)
    print("Example 2: Create Draft Post from Script Data")
    print("=" * 70)

    # Sample script data (normally this would come from core.script_development)
    script_data = {
        'title': 'The Mystery of the Forgotten Algorithm',
        'content': """In the depths of an old server room, Sarah discovered something remarkable.
        
A piece of code, written decades ago, still running silently in the background.

It was elegant. Perfect. And completely undocumented.

She traced its origins through layers of legacy systems, following digital breadcrumbs left by a programmer who vanished years ago.

The algorithm predicted market trends with uncanny accuracy. But why was it hidden?

Sarah soon learned some innovations are too powerful to share.

And some secrets are meant to stay buried in the code.""",
        'target_gender': 'women',
        'target_age': '18-23',
        'word_count': 97,
        'estimated_duration': 45.0
    }

    # Initialize provider (using environment variables)
    provider = WordPressProvider()

    # Check authentication
    if not provider.authenticate():
        print("❌ Authentication failed. Please set environment variables:")
        print("   WORDPRESS_SITE_URL")
        print("   WORDPRESS_USERNAME")
        print("   WORDPRESS_APP_PASSWORD")
        return

    # Create draft with metadata
    excerpt = f"A short story for {script_data['target_gender']} aged {script_data['target_age']}"
    
    result = provider.create_draft_post(
        title=script_data['title'],
        content=script_data['content'],
        excerpt=excerpt
    )

    if result['success']:
        print(f"✅ Draft post created from script!")
        print(f"   Post ID: {result['post_id']}")
        print(f"   Edit URL: {result['edit_url']}")
        print(f"\n   You can now:")
        print(f"   1. Review and edit the draft in WordPress")
        print(f"   2. Add images or formatting")
        print(f"   3. Publish when ready")
    else:
        print(f"❌ Failed to create post: {result['error']}")


def example_batch_posts():
    """Example of creating multiple draft posts."""
    print("\n" + "=" * 70)
    print("Example 3: Batch Create Draft Posts")
    print("=" * 70)

    # Sample stories
    stories = [
        {
            'title': 'The Last Message',
            'content': 'In 2095, archaeologists found an old smartphone. It had one unread message...'
        },
        {
            'title': 'Three Seconds',
            'content': 'Time froze for everyone except me. I had three seconds to make a choice...'
        },
        {
            'title': 'The Memory Thief',
            'content': 'She could steal memories with a touch. But every memory she took, she had to keep...'
        }
    ]

    provider = WordPressProvider()

    if not provider.authenticate():
        print("❌ Authentication failed")
        return

    print(f"\nCreating {len(stories)} draft posts...\n")

    for i, story in enumerate(stories, 1):
        print(f"[{i}/{len(stories)}] Creating: {story['title']}")
        
        result = provider.create_draft_post(
            title=story['title'],
            content=story['content']
        )
        
        if result['success']:
            print(f"   ✅ Created (ID: {result['post_id']})")
        else:
            print(f"   ❌ Failed: {result['error']}")

    print(f"\n✅ Batch creation complete!")


def example_update_and_publish():
    """Example of updating a draft and publishing it."""
    print("\n" + "=" * 70)
    print("Example 4: Update Draft and Publish")
    print("=" * 70)

    provider = WordPressProvider()

    if not provider.authenticate():
        print("❌ Authentication failed")
        return

    # Create a draft
    print("\n1. Creating draft post...")
    result = provider.create_draft_post(
        title="Initial Title",
        content="Initial content..."
    )

    if not result['success']:
        print(f"❌ Failed to create draft: {result['error']}")
        return

    post_id = result['post_id']
    print(f"   ✅ Draft created (ID: {post_id})")

    # Update the draft
    print("\n2. Updating draft with improved content...")
    update_result = provider.update_post(
        post_id=post_id,
        title="The Improved Title - Now With Better Content",
        content="This is the improved content after review and editing..."
    )

    if update_result['success']:
        print(f"   ✅ Draft updated")
    else:
        print(f"   ❌ Update failed: {update_result['error']}")
        return

    # Publish the post
    print("\n3. Publishing the post...")
    publish_result = provider.update_post(
        post_id=post_id,
        status='publish'
    )

    if publish_result['success']:
        print(f"   ✅ Post published!")
        print(f"   URL: {publish_result['post_url']}")
    else:
        print(f"   ❌ Publish failed: {publish_result['error']}")


def main():
    """Run all examples."""
    parser = argparse.ArgumentParser(
        description='WordPress Integration Examples',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )

    parser.add_argument(
        '--site-url',
        help='WordPress site URL (overrides WORDPRESS_SITE_URL env var)'
    )
    parser.add_argument(
        '--username',
        help='WordPress username (overrides WORDPRESS_USERNAME env var)'
    )
    parser.add_argument(
        '--app-password',
        help='WordPress application password (overrides WORDPRESS_APP_PASSWORD env var)'
    )
    parser.add_argument(
        '--example',
        type=int,
        choices=[1, 2, 3, 4],
        help='Run specific example (1-4), or all if not specified'
    )

    args = parser.parse_args()

    # Set environment variables if provided
    if args.site_url:
        os.environ['WORDPRESS_SITE_URL'] = args.site_url
    if args.username:
        os.environ['WORDPRESS_USERNAME'] = args.username
    if args.app_password:
        os.environ['WORDPRESS_APP_PASSWORD'] = args.app_password

    print("\n" + "█" * 70)
    print("WordPress Integration - Usage Examples")
    print("█" * 70)

    try:
        if args.example == 1 or not args.example:
            example_basic_usage()
        
        if args.example == 2 or not args.example:
            example_with_script_data()
        
        if args.example == 3 or not args.example:
            example_batch_posts()
        
        if args.example == 4 or not args.example:
            example_update_and_publish()

        print("\n" + "=" * 70)
        print("✅ All examples completed!")
        print("=" * 70)
        print("\nNote: These examples use mock data.")
        print("For real usage, configure your WordPress credentials:")
        print("  - WORDPRESS_SITE_URL: Your WordPress site URL")
        print("  - WORDPRESS_USERNAME: Your WordPress username")
        print("  - WORDPRESS_APP_PASSWORD: Generate from WordPress admin")
        print("\nWordPress Application Password setup:")
        print("  1. Go to: Users → Profile → Application Passwords")
        print("  2. Enter a name (e.g., 'StoryGenerator')")
        print("  3. Click 'Add New Application Password'")
        print("  4. Copy the generated password")

    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
