#!/usr/bin/env python3
"""
Podbean Publishing Script for StoryGenerator

Uploads and publishes podcast episodes to Podbean via API.
Supports immediate and scheduled publishing, with optional artwork.

Usage:
    # Set environment variables and run
    export PODBEAN_CLIENT_ID="your_client_id"
    export PODBEAN_CLIENT_SECRET="your_client_secret"
    export AUDIO_PATH="/path/to/episode.mp3"
    export EP_TITLE="Episode Title"
    export EP_DESC="Episode description"

    python scripts/publish_podbean.py

    # Optional: Schedule publishing
    export EP_PUBLISH_AT="2025-10-12T15:00:00Z"

    # Optional: Add episode artwork
    export EP_ARTWORK_PATH="/path/to/artwork.jpg"
"""

import datetime
import os
import sys

import requests

# Add project root to path for error handling imports
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from PrismQ.Shared.errors import APIError, AuthenticationError, ValidationError


def get_token():
    """Authenticate with Podbean API using OAuth client credentials.

    Returns:
        str: Access token for API requests

    Raises:
        AuthenticationError: If authentication fails
        APIError: If API request fails
    """
    client_id = os.environ.get("PODBEAN_CLIENT_ID")
    client_secret = os.environ.get("PODBEAN_CLIENT_SECRET")

    if not client_id or not client_secret:
        raise AuthenticationError(
            "Missing Podbean credentials",
            details={
                "client_id_set": bool(client_id),
                "client_secret_set": bool(client_secret)
            }
        )

    try:
        r = requests.post(
            "https://api.podbean.com/v1/oauth/token",
            data={
                "grant_type": "client_credentials",
                "client_id": client_id,
                "client_secret": client_secret,
            },
            timeout=30
        )
        r.raise_for_status()
        data = r.json()

        if "access_token" not in data:
            raise AuthenticationError(
                "Invalid response from Podbean OAuth",
                details={"response": data}
            )

        return data["access_token"]

    except requests.exceptions.RequestException as e:
        raise APIError(
            "Failed to authenticate with Podbean",
            details={"error": str(e)},
            original_error=e,
            status_code=getattr(e.response, 'status_code', None) if hasattr(e, 'response') else None
        )


def upload_authorize(token):
    """Get presigned URL for uploading files to Podbean.

    Args:
        token: Podbean API access token

    Returns:
        tuple: (presigned_url, file_key) for upload

    Raises:
        APIError: If API request fails
    """
    try:
        r = requests.get(
            "https://api.podbean.com/v1/files/uploadAuthorize",
            headers={"Authorization": f"Bearer {token}"},
            timeout=30
        )
        r.raise_for_status()
        data = r.json()

        if "presigned_url" not in data or "file_key" not in data:
            raise APIError(
                "Invalid upload authorization response",
                details={"response": data}
            )

        return data["presigned_url"], data["file_key"]

    except requests.exceptions.RequestException as e:
        raise APIError(
            "Failed to get upload authorization",
            details={"error": str(e)},
            original_error=e,
            status_code=getattr(e.response, 'status_code', None) if hasattr(e, 'response') else None
        )


def upload_file(presigned_url, file_path):
    """Upload a file to Podbean using presigned URL.

    Args:
        presigned_url: Presigned URL from upload_authorize
        file_path: Path to file to upload

    Raises:
        ValidationError: If file doesn't exist
        APIError: If upload fails
    """
    if not os.path.exists(file_path):
        raise ValidationError(
            f"File not found: {file_path}",
            details={"path": file_path}
        )

    try:
        with open(file_path, "rb") as f:
            put = requests.put(presigned_url, data=f, timeout=300)
            put.raise_for_status()

    except requests.exceptions.RequestException as e:
        raise APIError(
            f"Failed to upload file: {file_path}",
            details={"error": str(e), "path": file_path},
            original_error=e,
            status_code=getattr(e.response, 'status_code', None) if hasattr(e, 'response') else None
        )


def create_episode(token, *, media_key, title, description, publish_at=None, logo_key=None):
    """Create and publish/schedule a podcast episode on Podbean.

    Args:
        token: Podbean API access token
        media_key: File key from upload
        title: Episode title
        description: Episode description
        publish_at: Optional ISO 8601 UTC timestamp for scheduling (e.g., "2025-10-12T15:00:00Z")
        logo_key: Optional file key for episode artwork

    Returns:
        dict: Episode creation response from API

    Raises:
        ValidationError: If publish_at format is invalid
        APIError: If API request fails
    """
    payload = {
        "title": title,
        "content": description,
        "type": "public",
        "media_key": media_key,
        "status": "publish" if not publish_at else "schedule",
    }

    if publish_at:
        # Expect ISO 8601 (UTC), e.g. 2025-10-12T15:00:00Z
        try:
            if publish_at.endswith("Z"):
                publish_at = publish_at.replace("Z", "+00:00")
            dt = datetime.datetime.fromisoformat(publish_at)
            payload["publish_time"] = str(int(dt.timestamp()))
        except (ValueError, AttributeError) as e:
            raise ValidationError(
                f"Invalid publish_at format: {publish_at}",
                details={
                    "expected": "ISO 8601 UTC (e.g., 2025-10-12T15:00:00Z)",
                    "received": publish_at
                },
                original_error=e
            )

    if logo_key:
        payload["logo_key"] = logo_key

    try:
        r = requests.post(
            "https://api.podbean.com/v1/episodes",
            headers={"Authorization": f"Bearer {token}"},
            data=payload,
            timeout=30
        )
        r.raise_for_status()
        return r.json()

    except requests.exceptions.RequestException as e:
        raise APIError(
            "Failed to create episode",
            details={"error": str(e), "title": title},
            original_error=e,
            status_code=getattr(e.response, 'status_code', None) if hasattr(e, 'response') else None
        )


def upload_artwork(token, artwork_path):
    """Upload episode artwork to Podbean.

    Args:
        token: Podbean API access token
        artwork_path: Path to artwork image file

    Returns:
        str: File key for uploaded artwork

    Raises:
        ValidationError: If artwork file doesn't exist
        APIError: If upload fails
    """
    if not os.path.exists(artwork_path):
        raise ValidationError(
            f"Artwork file not found: {artwork_path}",
            details={"path": artwork_path}
        )

    presigned_url, file_key = upload_authorize(token)
    upload_file(presigned_url, artwork_path)
    return file_key


def main():
    """Main entry point for Podbean publishing script."""
    print("=" * 70)
    print("Podbean Episode Publisher")
    print("=" * 70)

    try:
        # Get environment variables
        audio_path = os.environ.get("AUDIO_PATH")
        ep_title = os.environ.get("EP_TITLE", "New Episode")
        ep_desc = os.environ.get("EP_DESC", "")
        ep_publish = os.environ.get("EP_PUBLISH_AT")
        artwork_path = os.environ.get("EP_ARTWORK_PATH")

        # Validate required inputs
        if not audio_path:
            raise ValidationError(
                "AUDIO_PATH environment variable is required",
                details={"available_vars": [k for k in os.environ if k.startswith("EP_") or k.startswith("PODBEAN_")]}
            )

        print("\nConfiguration:")
        print(f"  Audio file: {audio_path}")
        print(f"  Title: {ep_title}")
        print(f"  Description: {ep_desc[:60]}{'...' if len(ep_desc) > 60 else ''}")

        if ep_publish:
            print(f"  Scheduled for: {ep_publish}")
        else:
            print("  Publishing: Immediately")

        if artwork_path:
            print(f"  Artwork: {artwork_path}")

        print("\n" + "=" * 70)
        print("Authenticating with Podbean...")
        print("=" * 70)

        # Authenticate
        token = get_token()
        print("✅ Authentication successful")

        # Upload audio file
        print("\n" + "=" * 70)
        print("Uploading audio file...")
        print("=" * 70)

        presigned_url, media_key = upload_authorize(token)
        upload_file(presigned_url, audio_path)
        print("✅ Audio uploaded successfully")

        # Upload artwork if provided
        logo_key = None
        if artwork_path and os.path.exists(artwork_path):
            print("\n" + "=" * 70)
            print("Uploading artwork...")
            print("=" * 70)

            logo_key = upload_artwork(token, artwork_path)
            print("✅ Artwork uploaded successfully")

        # Create episode
        print("\n" + "=" * 70)
        print("Creating episode...")
        print("=" * 70)

        result = create_episode(
            token,
            media_key=media_key,
            title=ep_title,
            description=ep_desc,
            publish_at=ep_publish,
            logo_key=logo_key
        )

        permalink = result.get("permalink_url", "")
        episode_id = result.get("episode_id", "")

        print("\n" + "=" * 70)
        print("✅ Episode created successfully!")
        print("=" * 70)

        if permalink:
            print(f"\n🔗 Episode URL: {permalink}")
        if episode_id:
            print(f"📝 Episode ID: {episode_id}")

        if ep_publish:
            print(f"\n⏰ Episode scheduled for: {ep_publish}")
        else:
            print("\n🎉 Episode published immediately!")

        print("\n" + "=" * 70)

        return 0

    except KeyboardInterrupt:
        print("\n\n⚠️  Publishing cancelled by user")
        return 1

    except (ValidationError, AuthenticationError, APIError) as e:
        print(f"\n❌ Error: {e}")
        if hasattr(e, 'details') and e.details:
            print(f"   Details: {e.details}")
        return 1

    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
