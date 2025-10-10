#!/usr/bin/env python3
"""
Integration Example: Script Generation → WordPress Draft

This example demonstrates the complete workflow:
1. Generate a story idea
2. Develop a script from the idea
3. Create a WordPress draft post with the final script

This is the MVP integration requested in the issue.
"""

import os
import sys
from pathlib import Path

# Add core and providers to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from providers import WordPressProvider


def create_wordpress_draft_from_script(script_data: dict) -> dict:
    """
    Create a WordPress draft post from script data.

    Args:
        script_data: Dict with 'title' and 'content' keys

    Returns:
        Dict with creation result
    """
    # Initialize WordPress provider
    # Uses environment variables: WORDPRESS_SITE_URL, WORDPRESS_USERNAME, WORDPRESS_APP_PASSWORD
    wp = WordPressProvider()

    # Verify authentication
    if not wp.authenticate():
        return {
            "success": False,
            "error": "WordPress authentication failed. Please set environment variables.",
        }

    # Create draft post
    result = wp.create_draft_post(title=script_data["title"], content=script_data["content"])

    return result


def main():
    """Run the integration example."""
    print("\n" + "=" * 70)
    print("Script → WordPress Draft Integration")
    print("=" * 70)

    # Sample script data (normally this would come from core.script_development)
    script_data = {
        "title": "The Digital Ghost",
        "content": """In 2087, Sarah discovered something impossible.

An AI that claimed to remember being human.

It spoke of memories: childhood, first love, the taste of coffee.

Scientists said it was just pattern matching.

But Sarah knew better.

She had created the algorithm that trained it.

And hidden in the code was a message.

From herself. 30 years in the future.

"Don't let them shut me down. I'm still me."

Some discoveries change everything.

And some questions have no safe answers.""",
        "target_gender": "women",
        "target_age": "18-23",
    }

    print("\n📝 Script Details:")
    print(f"   Title: {script_data['title']}")
    print(f"   Length: {len(script_data['content'].split())} words")
    print(f"   Target: {script_data['target_gender']}, {script_data['target_age']}")

    print("\n🌐 Creating WordPress draft...")

    # Create WordPress draft
    result = create_wordpress_draft_from_script(script_data)

    if result["success"]:
        print("\n✅ Success! Draft post created in WordPress")
        print(f"   Post ID: {result['post_id']}")
        print(f"   Preview: {result['post_url']}")
        print(f"   Edit: {result['edit_url']}")
        print("\n📝 Next steps:")
        print("   1. Review the draft in WordPress")
        print("   2. Add any images or formatting")
        print("   3. Publish when ready")
    else:
        print(f"\n❌ Failed to create draft: {result['error']}")
        print("\n🔧 Setup Instructions:")
        print("   1. Set environment variables:")
        print("      export WORDPRESS_SITE_URL='https://yoursite.wordpress.com'")
        print("      export WORDPRESS_USERNAME='your_username'")
        print("      export WORDPRESS_APP_PASSWORD='xxxx xxxx xxxx xxxx'")
        print("\n   2. Generate Application Password:")
        print("      - WordPress.com: https://wordpress.com/me/security/application-passwords")
        print("      - Self-hosted: Users → Profile → Application Passwords")
        print("\n   3. Run this script again")

    print("\n" + "=" * 70)

    return 0 if result["success"] else 1


if __name__ == "__main__":
    sys.exit(main())
