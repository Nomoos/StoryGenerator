# Distribution: Multi-Platform Publisher

**Group:** group_4  
**Priority:** P2 (Medium)  
**Status:** ✅ Complete  
**Estimated Effort:** 10-12 hours  
**Completed:** 2025-10-10  

## Description

Implement multi-platform video publishing system that automates upload to YouTube, TikTok, Instagram, and Facebook. Includes platform-specific optimization, scheduling, and metadata management.

## Acceptance Criteria

- [x] YouTube upload with API integration
- [x] TikTok upload with API integration
- [x] Instagram Reels upload
- [x] Facebook video upload
- [x] Platform-specific video optimization
- [x] Metadata and thumbnail upload
- [x] Upload scheduling and queue management
- [x] Error handling and retry logic
- [x] Upload tracking and reporting

## Implementation

**Location:** `src/Python/Tools/MultiPlatformPublisher.py`  
**Script:** `scripts/publish_video.py`  
**Dependencies:** Existing providers in `PrismQ/Providers/` directory

The MultiPlatformPublisher has been successfully implemented with:
- Unified interface for uploading to YouTube, TikTok, Instagram, and Facebook
- Platform-specific metadata handling via PlatformMetadata class
- Upload scheduling and queue management
- Error handling with detailed UploadResult objects
- Upload tracking and JSON report generation
- CLI tool for command-line publishing
- Support for batch uploads and scheduled publishing

**Integration**: Uses existing platform provider implementations:
- `PrismQ/Providers/youtube_provider.py` (YouTubeUploader)
- `PrismQ/Providers/tiktok_provider.py` (TikTokUploader)
- `PrismQ/Providers/instagram_provider.py` (InstagramUploader)
- `PrismQ/Providers/facebook_provider.py` (FacebookUploader)

## Dependencies

- Install: `google-api-python-client>=2.0.0 instagrapi>=1.16.0`
- Requires: QC-passed videos from Group 4
- Requires: API credentials for each platform

## Implementation Notes

Create `core/distribution/multi_platform_publisher.py`:

```python
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from instagrapi import Client
from pathlib import Path
from typing import Dict, List
from enum import Enum

class Platform(Enum):
    YOUTUBE = "youtube"
    TIKTOK = "tiktok"
    INSTAGRAM = "instagram"
    FACEBOOK = "facebook"

class MultiPlatformPublisher:
    def __init__(self):
        self.youtube = self._init_youtube()
        self.instagram = self._init_instagram()
        self.upload_queue = []
    
    def _init_youtube(self):
        """Initialize YouTube API client"""
        return build('youtube', 'v3', credentials=self._get_youtube_credentials())
    
    def _init_instagram(self):
        """Initialize Instagram client"""
        client = Client()
        client.login(username, password)
        return client
    
    def publish_to_youtube(self, 
                          video_path: Path,
                          title: str,
                          description: str,
                          tags: List[str],
                          thumbnail: Path = None) -> Dict:
        """Upload video to YouTube"""
        
        body = {
            'snippet': {
                'title': title,
                'description': description,
                'tags': tags,
                'categoryId': '24'  # Entertainment
            },
            'status': {
                'privacyStatus': 'public',
                'selfDeclaredMadeForKids': False
            }
        }
        
        media = MediaFileUpload(
            str(video_path),
            mimetype='video/mp4',
            resumable=True
        )
        
        request = self.youtube.videos().insert(
            part='snippet,status',
            body=body,
            media_body=media
        )
        
        response = request.execute()
        
        # Upload thumbnail if provided
        if thumbnail:
            self.youtube.thumbnails().set(
                videoId=response['id'],
                media_body=MediaFileUpload(str(thumbnail))
            ).execute()
        
        return {
            'platform': 'youtube',
            'video_id': response['id'],
            'url': f"https://youtube.com/watch?v={response['id']}"
        }
    
    def publish_to_instagram(self,
                            video_path: Path,
                            caption: str) -> Dict:
        """Upload Reel to Instagram"""
        
        media = self.instagram.clip_upload(
            str(video_path),
            caption=caption
        )
        
        return {
            'platform': 'instagram',
            'media_id': media.pk,
            'url': f"https://instagram.com/reel/{media.code}/"
        }
    
    def publish_to_all(self,
                      video_path: Path,
                      metadata: Dict) -> List[Dict]:
        """Publish to all configured platforms"""
        
        results = []
        
        # YouTube
        if 'youtube' in metadata:
            result = self.publish_to_youtube(
                video_path,
                metadata['youtube']['title'],
                metadata['youtube']['description'],
                metadata['youtube']['tags'],
                metadata['youtube'].get('thumbnail')
            )
            results.append(result)
        
        # Instagram
        if 'instagram' in metadata:
            result = self.publish_to_instagram(
                video_path,
                metadata['instagram']['caption']
            )
            results.append(result)
        
        # Add TikTok, Facebook similarly
        
        return results
    
    def schedule_upload(self,
                       video_path: Path,
                       platforms: List[Platform],
                       metadata: Dict,
                       scheduled_time: datetime = None):
        """Schedule video upload for later"""
        
        self.upload_queue.append({
            'video_path': video_path,
            'platforms': platforms,
            'metadata': metadata,
            'scheduled_time': scheduled_time or datetime.now()
        })
```

## Output Files

**Directory:** `data/distribution/{date}/`
**Files:**
- `upload_results.json` - Upload results for all platforms
- `upload_queue.json` - Pending uploads
- `upload_log.txt` - Detailed upload log

## Links

- Related: [HYBRID_ROADMAP.md](../../../docs/roadmaps/HYBRID_ROADMAP.md)
- Related: P2 distribution issues in [p2-medium/distribution](../../../p2-medium/distribution/)
