#!/usr/bin/env python3
"""
Multi-Platform Publisher for StoryGenerator

Orchestrates video uploads across multiple platforms including YouTube, TikTok,
Instagram, and Facebook. Provides unified interface for publishing videos with
platform-specific optimizations, scheduling, error handling, and tracking.
"""

import os
import json
from pathlib import Path
from typing import Dict, List, Optional, Any, Union
from datetime import datetime
from enum import Enum
from dataclasses import dataclass, asdict


# Simple logger class to avoid import issues
class SimpleLogger:
    def info(self, msg): print(f"[INFO] {msg}")
    def warning(self, msg): print(f"[WARNING] {msg}")
    def error(self, msg, exc_info=False): print(f"[ERROR] {msg}")

logger = SimpleLogger()


class Platform(Enum):
    """Supported video platforms."""
    YOUTUBE = "youtube"
    TIKTOK = "tiktok"
    INSTAGRAM = "instagram"
    FACEBOOK = "facebook"


class UploadStatus(Enum):
    """Upload status states."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    SUCCESS = "success"
    FAILED = "failed"
    SCHEDULED = "scheduled"


@dataclass
class PlatformMetadata:
    """Metadata for a specific platform."""
    title: Optional[str] = None
    description: Optional[str] = None
    caption: Optional[str] = None
    tags: Optional[List[str]] = None
    category: Optional[str] = None
    thumbnail_path: Optional[str] = None
    privacy: Optional[str] = "public"  # public, unlisted, private
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary, excluding None values."""
        return {k: v for k, v in asdict(self).items() if v is not None}


@dataclass
class UploadTask:
    """Represents a video upload task."""
    video_path: str
    platforms: List[Platform]
    metadata: Dict[Platform, PlatformMetadata]
    scheduled_time: Optional[datetime] = None
    status: UploadStatus = UploadStatus.PENDING
    results: Optional[List[Dict[str, Any]]] = None
    error: Optional[str] = None
    created_at: datetime = None
    completed_at: Optional[datetime] = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()


@dataclass
class UploadResult:
    """Result of an upload operation."""
    platform: Platform
    status: UploadStatus
    video_id: Optional[str] = None
    url: Optional[str] = None
    message: Optional[str] = None
    error: Optional[str] = None
    uploaded_at: datetime = None
    
    def __post_init__(self):
        if self.uploaded_at is None and self.status == UploadStatus.SUCCESS:
            self.uploaded_at = datetime.now()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        result = asdict(self)
        result['platform'] = self.platform.value
        result['status'] = self.status.value
        if self.uploaded_at:
            result['uploaded_at'] = self.uploaded_at.isoformat()
        return result


class MultiPlatformPublisher:
    """
    Multi-platform video publisher.
    
    Orchestrates video uploads across YouTube, TikTok, Instagram, and Facebook
    using existing platform provider implementations. Provides:
    - Unified upload interface
    - Platform-specific optimization
    - Scheduling and queue management
    - Error handling and retry logic
    - Upload tracking and reporting
    """
    
    def __init__(
        self,
        output_dir: Optional[str] = None,
        credentials_dir: Optional[str] = None,
        enable_platforms: Optional[List[Platform]] = None
    ):
        """
        Initialize multi-platform publisher.
        
        Args:
            output_dir: Directory to save upload logs and reports
            credentials_dir: Directory containing platform credentials
            enable_platforms: List of platforms to enable (default: all)
        """
        self.output_dir = Path(output_dir) if output_dir else Path("data/distribution")
        self.credentials_dir = Path(credentials_dir) if credentials_dir else Path("credentials")
        self.enable_platforms = enable_platforms or list(Platform)
        
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Upload queue and history
        self.upload_queue: List[UploadTask] = []
        self.upload_history: List[UploadTask] = []
        
        # Platform clients (lazy initialization)
        self._youtube = None
        self._tiktok = None
        self._instagram = None
        self._facebook = None
        
        # Initialize platform availability
        self._check_platform_availability()
    
    def _check_platform_availability(self):
        """Check which platforms are available based on dependencies."""
        self.available_platforms = {}
        
        # Check YouTube
        try:
            from PrismQ.Providers import YouTubeUploader
            self.available_platforms[Platform.YOUTUBE] = True
        except ImportError:
            logger.warning("YouTube provider not available (missing dependencies)")
            self.available_platforms[Platform.YOUTUBE] = False
        
        # Check TikTok
        try:
            from PrismQ.Providers import TikTokUploader
            self.available_platforms[Platform.TIKTOK] = True
        except ImportError:
            logger.warning("TikTok provider not available (missing dependencies)")
            self.available_platforms[Platform.TIKTOK] = False
        
        # Check Instagram
        try:
            from PrismQ.Providers import InstagramUploader
            self.available_platforms[Platform.INSTAGRAM] = True
        except ImportError:
            logger.warning("Instagram provider not available (missing dependencies)")
            self.available_platforms[Platform.INSTAGRAM] = False
        
        # Check Facebook
        try:
            from PrismQ.Providers import FacebookUploader
            self.available_platforms[Platform.FACEBOOK] = True
        except ImportError:
            logger.warning("Facebook provider not available (missing dependencies)")
            self.available_platforms[Platform.FACEBOOK] = False
    
    def _get_youtube_client(self):
        """Get or initialize YouTube client."""
        if self._youtube is None and self.available_platforms.get(Platform.YOUTUBE):
            try:
                from PrismQ.Providers import YouTubeUploader
                credentials_path = self.credentials_dir / "youtube_client_secret.json"
                token_path = self.credentials_dir / "youtube_token.json"
                
                self._youtube = YouTubeUploader(
                    credentials_path=str(credentials_path),
                    token_path=str(token_path)
                )
                logger.info("YouTube client initialized")
            except Exception as e:
                logger.error(f"Failed to initialize YouTube client: {e}")
                self._youtube = None
        
        return self._youtube
    
    def _get_tiktok_client(self):
        """Get or initialize TikTok client."""
        if self._tiktok is None and self.available_platforms.get(Platform.TIKTOK):
            try:
                from PrismQ.Providers import TikTokUploader
                credentials_path = self.credentials_dir / "tiktok_credentials.json"
                
                self._tiktok = TikTokUploader(
                    credentials_path=str(credentials_path)
                )
                logger.info("TikTok client initialized")
            except Exception as e:
                logger.error(f"Failed to initialize TikTok client: {e}")
                self._tiktok = None
        
        return self._tiktok
    
    def _get_instagram_client(self):
        """Get or initialize Instagram client."""
        if self._instagram is None and self.available_platforms.get(Platform.INSTAGRAM):
            try:
                from PrismQ.Providers import InstagramUploader
                credentials_path = self.credentials_dir / "instagram_credentials.json"
                
                self._instagram = InstagramUploader(
                    credentials_path=str(credentials_path)
                )
                logger.info("Instagram client initialized")
            except Exception as e:
                logger.error(f"Failed to initialize Instagram client: {e}")
                self._instagram = None
        
        return self._instagram
    
    def _get_facebook_client(self):
        """Get or initialize Facebook client."""
        if self._facebook is None and self.available_platforms.get(Platform.FACEBOOK):
            try:
                from PrismQ.Providers import FacebookUploader
                credentials_path = self.credentials_dir / "facebook_credentials.json"
                
                self._facebook = FacebookUploader(
                    credentials_path=str(credentials_path)
                )
                logger.info("Facebook client initialized")
            except Exception as e:
                logger.error(f"Failed to initialize Facebook client: {e}")
                self._facebook = None
        
        return self._facebook
    
    def publish_to_platform(
        self,
        platform: Platform,
        video_path: str,
        metadata: PlatformMetadata
    ) -> UploadResult:
        """
        Upload video to a specific platform.
        
        Args:
            platform: Target platform
            video_path: Path to video file
            metadata: Platform-specific metadata
        
        Returns:
            UploadResult with upload status and details
        """
        video_path = Path(video_path)
        
        if not video_path.exists():
            return UploadResult(
                platform=platform,
                status=UploadStatus.FAILED,
                error=f"Video file not found: {video_path}"
            )
        
        if platform not in self.enable_platforms:
            return UploadResult(
                platform=platform,
                status=UploadStatus.FAILED,
                error=f"Platform {platform.value} is not enabled"
            )
        
        if not self.available_platforms.get(platform):
            return UploadResult(
                platform=platform,
                status=UploadStatus.FAILED,
                error=f"Platform {platform.value} dependencies not available"
            )
        
        try:
            if platform == Platform.YOUTUBE:
                return self._upload_to_youtube(video_path, metadata)
            elif platform == Platform.TIKTOK:
                return self._upload_to_tiktok(video_path, metadata)
            elif platform == Platform.INSTAGRAM:
                return self._upload_to_instagram(video_path, metadata)
            elif platform == Platform.FACEBOOK:
                return self._upload_to_facebook(video_path, metadata)
            else:
                return UploadResult(
                    platform=platform,
                    status=UploadStatus.FAILED,
                    error=f"Unsupported platform: {platform.value}"
                )
        
        except Exception as e:
            logger.error(f"Failed to upload to {platform.value}: {e}", exc_info=True)
            return UploadResult(
                platform=platform,
                status=UploadStatus.FAILED,
                error=str(e)
            )
    
    def _upload_to_youtube(
        self,
        video_path: Path,
        metadata: PlatformMetadata
    ) -> UploadResult:
        """Upload video to YouTube."""
        client = self._get_youtube_client()
        
        if client is None:
            return UploadResult(
                platform=Platform.YOUTUBE,
                status=UploadStatus.FAILED,
                error="YouTube client not initialized"
            )
        
        # Authenticate if needed
        if not client.authenticate():
            return UploadResult(
                platform=Platform.YOUTUBE,
                status=UploadStatus.FAILED,
                error="YouTube authentication failed"
            )
        
        # Prepare metadata for YouTube
        from PrismQ.Shared.interfaces.platform_provider import VideoMetadata, PrivacyStatus
        
        privacy_map = {
            "public": PrivacyStatus.PUBLIC,
            "unlisted": PrivacyStatus.UNLISTED,
            "private": PrivacyStatus.PRIVATE
        }
        
        video_metadata = VideoMetadata(
            title=metadata.title or "Untitled Video",
            description=metadata.description or "",
            tags=metadata.tags or [],
            privacy_status=privacy_map.get(metadata.privacy, PrivacyStatus.PUBLIC),
            category_id=metadata.category or "24"  # Entertainment
        )
        
        # Upload video
        result = client.upload_video(str(video_path), video_metadata)
        
        # Upload thumbnail if provided
        if metadata.thumbnail_path and Path(metadata.thumbnail_path).exists():
            try:
                client.upload_thumbnail(result.video_id, metadata.thumbnail_path)
            except Exception as e:
                logger.warning(f"Failed to upload thumbnail: {e}")
        
        return UploadResult(
            platform=Platform.YOUTUBE,
            status=UploadStatus.SUCCESS if result.success else UploadStatus.FAILED,
            video_id=result.video_id,
            url=result.url,
            message=result.message,
            error=result.error if not result.success else None
        )
    
    def _upload_to_tiktok(
        self,
        video_path: Path,
        metadata: PlatformMetadata
    ) -> UploadResult:
        """Upload video to TikTok."""
        client = self._get_tiktok_client()
        
        if client is None:
            return UploadResult(
                platform=Platform.TIKTOK,
                status=UploadStatus.FAILED,
                error="TikTok client not initialized"
            )
        
        # Authenticate if needed
        if not client.authenticate():
            return UploadResult(
                platform=Platform.TIKTOK,
                status=UploadStatus.FAILED,
                error="TikTok authentication failed"
            )
        
        # Prepare metadata for TikTok
        from PrismQ.Shared.interfaces.platform_provider import VideoMetadata, PrivacyStatus
        
        privacy_map = {
            "public": PrivacyStatus.PUBLIC,
            "unlisted": PrivacyStatus.UNLISTED,
            "private": PrivacyStatus.PRIVATE
        }
        
        video_metadata = VideoMetadata(
            title=metadata.caption or metadata.title or "",
            description=metadata.description or "",
            tags=metadata.tags or [],
            privacy_status=privacy_map.get(metadata.privacy, PrivacyStatus.PUBLIC)
        )
        
        # Upload video
        result = client.upload_video(str(video_path), video_metadata)
        
        return UploadResult(
            platform=Platform.TIKTOK,
            status=UploadStatus.SUCCESS if result.success else UploadStatus.FAILED,
            video_id=result.video_id,
            url=result.url,
            message=result.message,
            error=result.error if not result.success else None
        )
    
    def _upload_to_instagram(
        self,
        video_path: Path,
        metadata: PlatformMetadata
    ) -> UploadResult:
        """Upload Reel to Instagram."""
        client = self._get_instagram_client()
        
        if client is None:
            return UploadResult(
                platform=Platform.INSTAGRAM,
                status=UploadStatus.FAILED,
                error="Instagram client not initialized"
            )
        
        # Authenticate if needed
        if not client.authenticate():
            return UploadResult(
                platform=Platform.INSTAGRAM,
                status=UploadStatus.FAILED,
                error="Instagram authentication failed"
            )
        
        # Prepare metadata for Instagram
        from PrismQ.Shared.interfaces.platform_provider import VideoMetadata
        
        video_metadata = VideoMetadata(
            title=metadata.caption or metadata.title or "",
            description=metadata.description or "",
            tags=metadata.tags or []
        )
        
        # Upload video (Reel)
        result = client.upload_video(str(video_path), video_metadata)
        
        return UploadResult(
            platform=Platform.INSTAGRAM,
            status=UploadStatus.SUCCESS if result.success else UploadStatus.FAILED,
            video_id=result.video_id,
            url=result.url,
            message=result.message,
            error=result.error if not result.success else None
        )
    
    def _upload_to_facebook(
        self,
        video_path: Path,
        metadata: PlatformMetadata
    ) -> UploadResult:
        """Upload video to Facebook."""
        client = self._get_facebook_client()
        
        if client is None:
            return UploadResult(
                platform=Platform.FACEBOOK,
                status=UploadStatus.FAILED,
                error="Facebook client not initialized"
            )
        
        # Authenticate if needed
        if not client.authenticate():
            return UploadResult(
                platform=Platform.FACEBOOK,
                status=UploadStatus.FAILED,
                error="Facebook authentication failed"
            )
        
        # Prepare metadata for Facebook
        from PrismQ.Shared.interfaces.platform_provider import VideoMetadata, PrivacyStatus
        
        privacy_map = {
            "public": PrivacyStatus.PUBLIC,
            "unlisted": PrivacyStatus.UNLISTED,
            "private": PrivacyStatus.PRIVATE
        }
        
        video_metadata = VideoMetadata(
            title=metadata.title or "Untitled Video",
            description=metadata.description or "",
            tags=metadata.tags or [],
            privacy_status=privacy_map.get(metadata.privacy, PrivacyStatus.PUBLIC)
        )
        
        # Upload video
        result = client.upload_video(str(video_path), video_metadata)
        
        return UploadResult(
            platform=Platform.FACEBOOK,
            status=UploadStatus.SUCCESS if result.success else UploadStatus.FAILED,
            video_id=result.video_id,
            url=result.url,
            message=result.message,
            error=result.error if not result.success else None
        )
    
    def publish_to_all(
        self,
        video_path: str,
        metadata: Dict[str, Union[PlatformMetadata, Dict[str, Any]]],
        platforms: Optional[List[Platform]] = None,
        save_report: bool = True
    ) -> List[UploadResult]:
        """
        Publish video to multiple platforms.
        
        Args:
            video_path: Path to video file
            metadata: Dictionary mapping platform names to PlatformMetadata objects
                     or dictionaries with metadata
            platforms: List of platforms to publish to (default: all enabled)
            save_report: Whether to save upload report
        
        Returns:
            List of UploadResult objects for each platform
        """
        platforms = platforms or self.enable_platforms
        results = []
        
        for platform in platforms:
            # Get metadata for this platform
            platform_key = platform.value
            platform_metadata = metadata.get(platform_key)
            
            if platform_metadata is None:
                # Try with Platform enum as key
                platform_metadata = metadata.get(platform)
            
            if platform_metadata is None:
                logger.warning(f"No metadata provided for {platform.value}, skipping")
                continue
            
            # Convert dict to PlatformMetadata if needed
            if isinstance(platform_metadata, dict):
                platform_metadata = PlatformMetadata(**platform_metadata)
            
            # Upload to platform
            result = self.publish_to_platform(platform, video_path, platform_metadata)
            results.append(result)
            
            # Log result
            if result.status == UploadStatus.SUCCESS:
                logger.info(f"✓ Uploaded to {platform.value}: {result.url}")
            else:
                logger.error(f"✗ Failed to upload to {platform.value}: {result.error}")
        
        # Save report if requested
        if save_report:
            self._save_upload_report(video_path, results)
        
        return results
    
    def schedule_upload(
        self,
        video_path: str,
        metadata: Dict[str, PlatformMetadata],
        platforms: List[Platform],
        scheduled_time: datetime
    ) -> UploadTask:
        """
        Schedule a video upload for later.
        
        Args:
            video_path: Path to video file
            metadata: Platform-specific metadata
            platforms: List of platforms to publish to
            scheduled_time: When to publish
        
        Returns:
            UploadTask object representing the scheduled upload
        """
        task = UploadTask(
            video_path=video_path,
            platforms=platforms,
            metadata=metadata,
            scheduled_time=scheduled_time,
            status=UploadStatus.SCHEDULED
        )
        
        self.upload_queue.append(task)
        logger.info(f"Scheduled upload for {scheduled_time}: {video_path}")
        
        return task
    
    def process_queue(self, dry_run: bool = False) -> List[UploadTask]:
        """
        Process pending uploads in the queue.
        
        Args:
            dry_run: If True, don't actually upload, just simulate
        
        Returns:
            List of processed UploadTask objects
        """
        processed = []
        now = datetime.now()
        
        for task in self.upload_queue[:]:
            # Check if task is ready to process
            if task.status == UploadStatus.SCHEDULED:
                if task.scheduled_time and task.scheduled_time > now:
                    continue  # Not yet time
            
            if task.status not in [UploadStatus.PENDING, UploadStatus.SCHEDULED]:
                continue  # Already processed or in progress
            
            # Process task
            task.status = UploadStatus.IN_PROGRESS
            
            if not dry_run:
                results = self.publish_to_all(
                    task.video_path,
                    task.metadata,
                    task.platforms
                )
                
                # Update task
                task.results = [r.to_dict() for r in results]
                task.status = UploadStatus.SUCCESS if all(
                    r.status == UploadStatus.SUCCESS for r in results
                ) else UploadStatus.FAILED
            else:
                task.status = UploadStatus.SUCCESS
                logger.info(f"[DRY RUN] Would upload: {task.video_path}")
            
            task.completed_at = datetime.now()
            
            # Move to history
            self.upload_queue.remove(task)
            self.upload_history.append(task)
            processed.append(task)
        
        return processed
    
    def _save_upload_report(
        self,
        video_path: str,
        results: List[UploadResult]
    ):
        """Save upload report to JSON file."""
        video_name = Path(video_path).stem
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_name = f"{video_name}_{timestamp}_upload.json"
        report_path = self.output_dir / report_name
        
        report = {
            'video_path': str(video_path),
            'uploaded_at': datetime.now().isoformat(),
            'platforms': [r.to_dict() for r in results],
            'summary': {
                'total': len(results),
                'success': sum(1 for r in results if r.status == UploadStatus.SUCCESS),
                'failed': sum(1 for r in results if r.status == UploadStatus.FAILED)
            }
        }
        
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Upload report saved: {report_path}")
    
    def get_upload_history(
        self,
        platform: Optional[Platform] = None,
        limit: Optional[int] = None
    ) -> List[UploadTask]:
        """
        Get upload history.
        
        Args:
            platform: Filter by platform
            limit: Maximum number of results
        
        Returns:
            List of UploadTask objects from history
        """
        history = self.upload_history
        
        if platform:
            history = [
                task for task in history
                if platform in task.platforms
            ]
        
        if limit:
            history = history[-limit:]
        
        return history


def main():
    """Command-line interface for multi-platform publisher."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Publish videos to multiple platforms'
    )
    parser.add_argument(
        'video_path',
        help='Path to video file'
    )
    parser.add_argument(
        '--platforms',
        nargs='+',
        choices=['youtube', 'tiktok', 'instagram', 'facebook'],
        default=['youtube'],
        help='Platforms to publish to'
    )
    parser.add_argument(
        '--title',
        required=True,
        help='Video title'
    )
    parser.add_argument(
        '--description',
        default='',
        help='Video description'
    )
    parser.add_argument(
        '--tags',
        nargs='+',
        default=[],
        help='Video tags'
    )
    parser.add_argument(
        '--privacy',
        choices=['public', 'unlisted', 'private'],
        default='public',
        help='Privacy setting'
    )
    parser.add_argument(
        '--output-dir',
        help='Directory to save reports'
    )
    parser.add_argument(
        '--credentials-dir',
        help='Directory containing platform credentials'
    )
    
    args = parser.parse_args()
    
    # Parse platforms
    platforms = [Platform(p) for p in args.platforms]
    
    # Create publisher
    publisher = MultiPlatformPublisher(
        output_dir=args.output_dir,
        credentials_dir=args.credentials_dir,
        enable_platforms=platforms
    )
    
    # Prepare metadata
    metadata = {}
    for platform in platforms:
        metadata[platform.value] = PlatformMetadata(
            title=args.title,
            description=args.description,
            tags=args.tags,
            privacy=args.privacy
        )
    
    # Publish
    print(f"\n{'='*70}")
    print(f"Publishing: {args.video_path}")
    print(f"Platforms: {', '.join(p.value for p in platforms)}")
    print(f"{'='*70}\n")
    
    results = publisher.publish_to_all(args.video_path, metadata, platforms)
    
    # Print results
    print(f"\n{'='*70}")
    print("Upload Results")
    print(f"{'='*70}\n")
    
    for result in results:
        status_icon = "✓" if result.status == UploadStatus.SUCCESS else "✗"
        print(f"{status_icon} {result.platform.value.upper()}")
        if result.status == UploadStatus.SUCCESS:
            print(f"   URL: {result.url}")
            print(f"   Video ID: {result.video_id}")
        else:
            print(f"   Error: {result.error}")
        print()
    
    # Summary
    success_count = sum(1 for r in results if r.status == UploadStatus.SUCCESS)
    print(f"Summary: {success_count}/{len(results)} successful\n")
    
    return 0 if success_count == len(results) else 1


if __name__ == '__main__':
    exit(main())
