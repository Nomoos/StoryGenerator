"""
YouTube Channel Scraper

Scrapes comprehensive metadata from the top N videos on a YouTube channel,
including titles, subtitles, descriptions, tags, engagement metrics, video quality,
and performance analytics similar to VidIQ and TubeBuddy.

Features:
- Video metadata (title, description, tags, duration)
- Engagement metrics (views, likes, comments, engagement rate)
- Performance analytics (views per day/hour, like ratios)
- Video quality info (resolution, FPS, aspect ratio)
- Content analysis (title/description length, tag count, chapters)
- Channel information (name, ID, follower count)
- Comprehensive reporting with insights

Usage:
    # Interactive mode (prompts for channel)
    python youtube_channel_scraper.py
    
    # With channel argument
    python youtube_channel_scraper.py <channel_url_or_id> [--top N]
    python youtube_channel_scraper.py https://www.youtube.com/@channelname --top 10
    python youtube_channel_scraper.py UC1234567890 --top 20
"""

import os
import sys
import json
import argparse
from pathlib import Path
from typing import List, Dict, Optional
from dataclasses import dataclass, asdict
import subprocess
import re


@dataclass
class VideoMetadata:
    """Metadata for a single video."""
    video_id: str
    title: str
    description: str
    tags: List[str]
    duration: str
    duration_seconds: int
    view_count: int
    like_count: Optional[int]
    comment_count: Optional[int]
    upload_date: str
    url: str
    thumbnail_url: str
    subtitles_available: bool
    subtitle_text: Optional[str]
    
    # Channel information
    channel_id: Optional[str] = None
    channel_name: Optional[str] = None
    channel_follower_count: Optional[int] = None
    
    # Additional metadata
    categories: Optional[List[str]] = None
    age_limit: Optional[int] = None
    average_rating: Optional[float] = None
    dislike_count: Optional[int] = None
    
    # Video quality metrics
    resolution: Optional[str] = None
    fps: Optional[int] = None
    aspect_ratio: Optional[str] = None
    video_format: Optional[str] = None  # "short" or "long"
    
    # Engagement metrics (calculated)
    engagement_rate: Optional[float] = None
    like_to_view_ratio: Optional[float] = None
    comment_to_view_ratio: Optional[float] = None
    views_per_day: Optional[float] = None
    views_per_hour: Optional[float] = None
    
    # Content analysis
    title_length: Optional[int] = None
    description_length: Optional[int] = None
    tag_count: Optional[int] = None
    has_chapters: bool = False
    chapter_count: Optional[int] = None
    
    # Story detection
    is_story_video: Optional[bool] = None
    story_confidence_score: Optional[float] = None
    story_indicators: Optional[List[str]] = None
    
    def to_dict(self):
        return asdict(self)


class YouTubeChannelScraper:
    """Scrapes metadata from YouTube channel videos."""
    
    # Constants
    SHORTS_FETCH_MULTIPLIER = 3  # Fetch 3x shorts to compensate for potential filtering/unavailable videos
    SHORTS_MAX_DURATION = 180  # YouTube Shorts max duration is 3 minutes (as of October 2024)
    
    # Story detection keywords (weighted by importance)
    STORY_TITLE_KEYWORDS = {
        # High confidence indicators (weight: 3)
        'story': 3, 'storytime': 3, 'aita': 3, 'am i the': 3,
        'tifu': 3, 'confession': 3, 'revenge': 3,
        
        # Medium confidence indicators (weight: 2)
        'relationship': 2, 'breakup': 2, 'cheating': 2, 'caught': 2,
        'ex boyfriend': 2, 'ex girlfriend': 2, 'my wife': 2, 'my husband': 2,
        'family drama': 2, 'toxic': 2, 'entitled': 2, 'karen': 2,
        
        # Low confidence indicators (weight: 1)
        'experience': 1, 'happened': 1, 'crazy': 1, 'insane': 1,
        'unbelievable': 1, 'shocking': 1, 'drama': 1, 'betrayed': 1,
    }
    
    STORY_DESCRIPTION_KEYWORDS = [
        'story', 'storytime', 'experience', 'happened to me', 'true story',
        'real story', 'my story', 'i want to share', 'let me tell you',
        'this is about', 'backstory', 'narrative', 'tale',
    ]
    
    STORY_TAGS = [
        'story', 'storytime', 'storytelling', 'true story', 'real story',
        'personal story', 'life story', 'story time', 'aita', 'reddit story',
        'relationship story', 'revenge story', 'confession',
    ]
    
    # Anti-patterns (likely NOT story videos)
    NON_STORY_KEYWORDS = [
        'tutorial', 'how to', 'review', 'unboxing', 'haul', 'vlog',
        'gameplay', 'walkthrough', 'guide', 'tips', 'tricks', 'reaction',
        'news', 'update', 'announcement', 'trailer', 'teaser', 'music video',
        'podcast', 'interview', 'q&a', 'q and a', 'challenge', 'prank',
    ]
    
    def __init__(self, output_dir: str = "/tmp/youtube_channel_data", story_only: bool = False):
        """
        Initialize scraper.
        
        Args:
            output_dir: Directory to store scraped data
            story_only: If True, only include videos detected as story videos
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.videos: List[VideoMetadata] = []
        self.channel_id: Optional[str] = None
        self.channel_name: Optional[str] = None
        self.story_only = story_only
        self.filtered_count = 0  # Track how many videos were filtered out
    
    def check_dependencies(self) -> bool:
        """Check if required dependencies are installed."""
        try:
            result = subprocess.run(
                ["yt-dlp", "--version"],
                capture_output=True,
                text=True
            )
            if result.returncode != 0:
                print("❌ yt-dlp is not installed")
                print("Install with: pip install yt-dlp")
                return False
            return True
        except FileNotFoundError:
            print("❌ yt-dlp is not installed")
            print("Install with: pip install yt-dlp")
            return False
    
    def extract_channel_url(self, input_str: str) -> str:
        """
        Extract or construct channel URL from various input formats.
        
        Args:
            input_str: Channel URL, handle, or ID
            
        Returns:
            Properly formatted channel URL
        """
        # If it's already a full URL, return it
        if input_str.startswith('http'):
            return input_str
        
        # If it starts with @, it's a handle
        if input_str.startswith('@'):
            return f"https://www.youtube.com/{input_str}"
        
        # If it looks like a channel ID (UC...)
        if input_str.startswith('UC'):
            return f"https://www.youtube.com/channel/{input_str}"
        
        # Otherwise assume it's a handle without @
        return f"https://www.youtube.com/@{input_str}"
    
    def get_channel_videos(self, channel_url: str, top_n: int = 10) -> Dict[str, List[str]]:
        """
        Get list of video IDs from channel (shorts only).
        
        Args:
            channel_url: Channel URL
            top_n: Number of shorts to retrieve
            
        Returns:
            Dict with 'shorts' list of video IDs
        """
        print(f"📺 Fetching top {top_n} shorts from channel...")
        
        all_videos = {'shorts': []}
        
        # Fetch shorts
        print(f"  🎬 Fetching shorts...")
        shorts_url = channel_url.rstrip('/') + "/shorts"
        shorts_cmd = [
            "yt-dlp",
            "--flat-playlist",
            "--print", "id",
            "--playlist-end", str(top_n * self.SHORTS_FETCH_MULTIPLIER),
            "--playlist-reverse",  # Get most recent first
            shorts_url
        ]
        
        try:
            result = subprocess.run(
                shorts_cmd,
                capture_output=True,
                text=True,
                timeout=60
            )
            
            if result.returncode == 0:
                shorts = [line.strip() for line in result.stdout.split('\n') if line.strip()]
                all_videos['shorts'] = shorts[:top_n]
                print(f"  ✅ Found {len(all_videos['shorts'])} shorts")
            else:
                print(f"  ⚠️ Error fetching shorts: {result.stderr}")
                
        except subprocess.TimeoutExpired:
            print("  ⚠️ Timeout while fetching shorts")
        except Exception as e:
            print(f"  ⚠️ Error fetching shorts: {e}")
        
        total = len(all_videos['shorts'])
        print(f"✅ Found total of {total} shorts")
        return all_videos
    
    def extract_video_metadata(self, video_id: str, expected_format: Optional[str] = None) -> Optional[VideoMetadata]:
        """
        Extract comprehensive metadata for a single video.
        
        Args:
            video_id: YouTube video ID
            expected_format: Expected format ('short' or 'long'), optional
            
        Returns:
            VideoMetadata object or None on failure
        """
        print(f"  📹 Extracting metadata for: {video_id}")
        
        video_url = f"https://www.youtube.com/watch?v={video_id}"
        
        # Use absolute path for output
        output_path = self.output_dir.resolve() / video_id
        print(f"     💾 Output path: {output_path}")
        
        # Get metadata using yt-dlp
        cmd = [
            "yt-dlp",
            "--skip-download",
            "--write-info-json",
            "--write-auto-sub",
            "--sub-lang", "en",
            "--sub-format", "srt",
            "-o", str(output_path),
            video_url
        ]
        
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=60
            )
            
            # Load the info JSON
            info_json_path = self.output_dir.resolve() / f"{video_id}.info.json"
            print(f"     📄 Info JSON: {info_json_path}")
            if not info_json_path.exists():
                print(f"    ⚠️ Could not retrieve metadata for {video_id}")
                return None
            
            with open(info_json_path, 'r', encoding='utf-8') as f:
                info = json.load(f)
            
            # Extract subtitle text if available
            subtitle_text = None
            subtitle_files = list(self.output_dir.glob(f"{video_id}*.srt"))
            if subtitle_files:
                subtitle_path = subtitle_files[0].resolve()
                print(f"     📝 Subtitle file: {subtitle_path}")
                with open(subtitle_files[0], 'r', encoding='utf-8') as f:
                    subtitle_text = self._parse_srt_to_text(f.read())
            
            # Extract video quality info from formats
            resolution = None
            fps = None
            aspect_ratio = None
            video_format = expected_format  # Use expected format if provided
            
            # Get duration early as it's needed for format detection
            duration_seconds = info.get('duration', 0)
            
            if 'formats' in info and info['formats']:
                # Get the best quality format
                formats = [f for f in info['formats'] if f.get('vcodec') != 'none']
                if formats:
                    best_format = max(formats, key=lambda f: f.get('height', 0) or 0)
                    resolution = f"{best_format.get('width', '?')}x{best_format.get('height', '?')}"
                    fps = best_format.get('fps')
                    if best_format.get('width') and best_format.get('height'):
                        width = best_format['width']
                        height = best_format['height']
                        aspect_ratio = f"{width}:{height}"
                        
                        # Determine video format based on duration and aspect ratio
                        # YouTube Shorts: <= 3 minutes (180s) and vertical (height > width)
                        # Source: https://support.google.com/youtube/answer/15424877
                        if not video_format:  # Only determine if not already set
                            if duration_seconds <= self.SHORTS_MAX_DURATION and height > width:
                                video_format = "short"
                            else:
                                video_format = "long"
            
            # Extract chapters information
            chapters = info.get('chapters', [])
            has_chapters = len(chapters) > 0
            chapter_count = len(chapters) if has_chapters else None
            
            # Get basic metadata
            view_count = info.get('view_count', 0)
            like_count = info.get('like_count')
            comment_count = info.get('comment_count')
            upload_date_str = info.get('upload_date', '')
            
            # Calculate engagement metrics
            engagement_rate = None
            like_to_view_ratio = None
            comment_to_view_ratio = None
            views_per_day = None
            views_per_hour = None
            
            if view_count and view_count > 0:
                if like_count is not None:
                    like_to_view_ratio = (like_count / view_count) * 100
                if comment_count is not None:
                    comment_to_view_ratio = (comment_count / view_count) * 100
                
                # Calculate engagement rate (likes + comments) / views
                if like_count is not None and comment_count is not None:
                    engagement_rate = ((like_count + comment_count) / view_count) * 100
                
                # Calculate views per day/hour based on upload date
                if upload_date_str:
                    try:
                        from datetime import datetime
                        upload_date = datetime.strptime(upload_date_str, '%Y%m%d')
                        days_since_upload = (datetime.now() - upload_date).days
                        if days_since_upload > 0:
                            views_per_day = view_count / days_since_upload
                            views_per_hour = views_per_day / 24
                    except Exception:
                        pass
            
            # Get categories
            categories = info.get('categories', [])
            if isinstance(categories, str):
                categories = [categories]
            
            # Create metadata object
            metadata = VideoMetadata(
                video_id=video_id,
                title=info.get('title', ''),
                description=info.get('description', ''),
                tags=info.get('tags', []),
                duration=self._format_duration(duration_seconds),
                duration_seconds=duration_seconds,
                view_count=view_count,
                like_count=like_count,
                comment_count=comment_count,
                upload_date=upload_date_str,
                url=video_url,
                thumbnail_url=info.get('thumbnail', ''),
                subtitles_available=subtitle_text is not None,
                subtitle_text=subtitle_text,
                
                # Channel information
                channel_id=info.get('channel_id'),
                channel_name=info.get('channel', info.get('uploader')),
                channel_follower_count=info.get('channel_follower_count'),
                
                # Additional metadata
                categories=categories if categories else None,
                age_limit=info.get('age_limit'),
                average_rating=info.get('average_rating'),
                dislike_count=info.get('dislike_count'),
                
                # Video quality metrics
                resolution=resolution,
                fps=fps,
                aspect_ratio=aspect_ratio,
                video_format=video_format,
                
                # Engagement metrics
                engagement_rate=engagement_rate,
                like_to_view_ratio=like_to_view_ratio,
                comment_to_view_ratio=comment_to_view_ratio,
                views_per_day=views_per_day,
                views_per_hour=views_per_hour,
                
                # Content analysis
                title_length=len(info.get('title', '')),
                description_length=len(info.get('description', '')),
                tag_count=len(info.get('tags', [])),
                has_chapters=has_chapters,
                chapter_count=chapter_count
            )
            
            # Detect if this is a story video
            is_story, confidence, indicators = self.detect_story_video(metadata)
            metadata.is_story_video = is_story
            metadata.story_confidence_score = confidence
            metadata.story_indicators = indicators
            
            # If story_only mode is enabled, filter out non-story videos
            if self.story_only and not is_story:
                self.filtered_count += 1
                print(f"    ⏭️  Filtered (not a story, confidence: {confidence:.2f}): {metadata.title[:50]}...")
                return None
            
            self.videos.append(metadata)
            
            # Save video info as markdown for easier viewing
            self._save_video_info_as_markdown(metadata)
            
            format_emoji = "🎬" if video_format == "short" else "📹"
            story_emoji = "📖" if is_story else "❓"
            story_info = f"{story_emoji} Story: {confidence:.2f}" if confidence > 0 else ""
            print(f"    ✅ Extracted ({format_emoji} {video_format}): {metadata.title[:50]}... [{metadata.duration}] {story_info}")
            return metadata
            
        except subprocess.TimeoutExpired:
            print(f"    ⚠️ Timeout for {video_id}")
            return None
        except Exception as e:
            print(f"    ⚠️ Error for {video_id}: {e}")
            return None
    
    def _parse_srt_to_text(self, srt_content: str) -> str:
        """
        Parse SRT subtitle file to plain text.
        
        Args:
            srt_content: Raw SRT file content
            
        Returns:
            Plain text of subtitles
        """
        # Remove timestamp lines and index numbers
        lines = srt_content.split('\n')
        text_lines = []
        
        for line in lines:
            line = line.strip()
            # Skip empty lines, numbers, and timestamp lines
            if not line or line.isdigit() or '-->' in line:
                continue
            text_lines.append(line)
        
        return ' '.join(text_lines)
    
    def _save_video_info_as_markdown(self, video: VideoMetadata):
        """
        Save individual video metadata as markdown for easier viewing.
        
        Args:
            video: VideoMetadata object
        """
        format_icon = "🎬" if video.video_format == "short" else "📹"
        
        md_content = f"""# {format_icon} {video.title}

## Basic Information

- **Video ID**: {video.video_id}
- **URL**: {video.url}
- **Format**: {video.video_format.upper() if video.video_format else 'N/A'}
- **Channel**: {video.channel_name or 'N/A'}
- **Channel ID**: {video.channel_id or 'N/A'}
- **Upload Date**: {video.upload_date}
- **Duration**: {video.duration} ({video.duration_seconds} seconds)

## Viewership & Engagement

- **Views**: {video.view_count:,}
- **Likes**: {video.like_count if video.like_count else 'N/A'}
- **Comments**: {video.comment_count if video.comment_count else 'N/A'}
- **Engagement Rate**: {f"{video.engagement_rate:.2f}%" if video.engagement_rate else 'N/A'}
- **Like-to-View Ratio**: {f"{video.like_to_view_ratio:.3f}%" if video.like_to_view_ratio else 'N/A'}
- **Comment-to-View Ratio**: {f"{video.comment_to_view_ratio:.3f}%" if video.comment_to_view_ratio else 'N/A'}
- **Views Per Day**: {f"{video.views_per_day:.0f}" if video.views_per_day else 'N/A'}
- **Views Per Hour**: {f"{video.views_per_hour:.1f}" if video.views_per_hour else 'N/A'}

## Video Quality

- **Resolution**: {video.resolution or 'N/A'}
- **FPS**: {video.fps or 'N/A'}
- **Aspect Ratio**: {video.aspect_ratio or 'N/A'}

## Content Analysis

- **Title Length**: {video.title_length} characters
- **Description Length**: {video.description_length} characters
- **Tag Count**: {video.tag_count}
- **Has Chapters**: {'Yes' if video.has_chapters else 'No'}
- **Chapter Count**: {video.chapter_count if video.chapter_count else 'N/A'}
- **Subtitles Available**: {'Yes' if video.subtitles_available else 'No'}
- **Categories**: {', '.join(video.categories) if video.categories else 'N/A'}

## Description

```
{video.description[:500]}{'...' if len(video.description) > 500 else ''}
```

## Tags

{', '.join(video.tags[:20])}{'...' if len(video.tags) > 20 else ''}

## Subtitle Text (First 300 words)

```
{' '.join((video.subtitle_text or '').split()[:300])}{'...' if video.subtitle_text and len(video.subtitle_text.split()) > 300 else ''}
```

---

*This is a markdown representation of video metadata.*  
*For complete data, see `{video.video_id}.info.json`*
"""
        
        md_path = self.output_dir / f"{video.video_id}.info.md"
        with open(md_path, 'w', encoding='utf-8') as f:
            f.write(md_content)
    
    def _format_duration(self, seconds: int) -> str:
        """Format duration in seconds to HH:MM:SS."""
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        secs = seconds % 60
        
        if hours > 0:
            return f"{hours:02d}:{minutes:02d}:{secs:02d}"
        else:
            return f"{minutes:02d}:{secs:02d}"
    
    def detect_story_video(self, video_metadata: VideoMetadata) -> tuple[bool, float, List[str]]:
        """
        Detect if a video is likely a story video based on metadata.
        
        Args:
            video_metadata: Video metadata to analyze
            
        Returns:
            Tuple of (is_story, confidence_score, indicators_found)
            - is_story: True if video is likely a story (confidence > 0.3)
            - confidence_score: Score between 0 and 1
            - indicators_found: List of matched story indicators
        """
        score = 0.0
        indicators = []
        
        # Check title for story keywords
        title_lower = video_metadata.title.lower()
        
        # First check for anti-patterns (non-story content)
        for keyword in self.NON_STORY_KEYWORDS:
            if keyword in title_lower:
                # Strong negative signal - likely not a story
                return False, 0.0, [f"non-story keyword: {keyword}"]
        
        # Check title keywords with weights
        title_score = 0
        for keyword, weight in self.STORY_TITLE_KEYWORDS.items():
            if keyword in title_lower:
                title_score += weight
                indicators.append(f"title: {keyword}")
        
        # If we have strong title indicators, boost the score significantly
        if title_score >= 3:  # At least one high-confidence keyword
            score += 0.5
        elif title_score >= 2:  # Medium confidence
            score += 0.3
        elif title_score >= 1:  # Low confidence
            score += 0.15
        
        # Check description
        if video_metadata.description:
            desc_lower = video_metadata.description.lower()
            
            # Check for anti-patterns in description
            anti_pattern_count = sum(1 for keyword in self.NON_STORY_KEYWORDS if keyword in desc_lower)
            if anti_pattern_count >= 2:
                # Multiple anti-patterns in description
                return False, 0.0, [f"non-story keywords in description: {anti_pattern_count}"]
            
            # Check for story keywords in description
            desc_matches = 0
            for keyword in self.STORY_DESCRIPTION_KEYWORDS:
                if keyword in desc_lower:
                    desc_matches += 1
                    indicators.append(f"description: {keyword}")
                    if desc_matches >= 2:  # Stop after 2 matches
                        break
            
            if desc_matches >= 2:
                score += 0.2
            elif desc_matches >= 1:
                score += 0.1
        
        # Check tags
        if video_metadata.tags:
            tags_lower = [tag.lower() for tag in video_metadata.tags]
            tag_matches = 0
            for tag in self.STORY_TAGS:
                if tag in tags_lower:
                    tag_matches += 1
                    indicators.append(f"tag: {tag}")
            
            if tag_matches >= 2:
                score += 0.2
            elif tag_matches >= 1:
                score += 0.1
        
        # Check subtitle text for story patterns (if available)
        if video_metadata.subtitle_text:
            subtitle_lower = video_metadata.subtitle_text.lower()[:500]  # Check first 500 chars
            
            # Story often starts with first-person narrative
            first_person_indicators = [
                'i was', 'i had', 'i went', 'i got', 'i decided', 'i thought',
                'my story', 'this happened', 'so this happened',
            ]
            
            subtitle_matches = 0
            for indicator in first_person_indicators:
                if indicator in subtitle_lower:
                    subtitle_matches += 1
                    indicators.append(f"subtitle: {indicator}")
                    if subtitle_matches >= 2:  # Stop after 2 matches
                        break
            
            if subtitle_matches >= 1:
                score += 0.15
        
        # Normalize confidence to 0-1 range (cap at 1.0)
        confidence = min(score, 1.0)
        
        # Determine if it's a story (threshold: 0.3 for permissive matching)
        is_story = confidence >= 0.3
        
        return is_story, confidence, indicators
    
    def scrape_channel(self, channel_input: str, top_n: int = 10) -> List[VideoMetadata]:
        """
        Scrape top N shorts from a channel.
        
        Args:
            channel_input: Channel URL, handle, or ID
            top_n: Number of shorts to scrape
            
        Returns:
            List of VideoMetadata objects
        """
        # Check dependencies
        if not self.check_dependencies():
            return []
        
        # Extract channel URL
        channel_url = self.extract_channel_url(channel_input)
        print(f"📺 Channel URL: {channel_url}")
        print(f"📁 Output directory: {self.output_dir.resolve()}")
        
        # Get video IDs (shorts only)
        video_ids_by_format = self.get_channel_videos(channel_url, top_n)
        
        total_videos = len(video_ids_by_format['shorts'])
        if total_videos == 0:
            print("❌ No shorts found")
            return []
        
        # Extract metadata for each video
        print(f"\n📊 Extracting metadata for {total_videos} shorts...\n")
        
        # Process shorts
        if video_ids_by_format['shorts']:
            print(f"🎬 Processing {len(video_ids_by_format['shorts'])} shorts...")
            for i, video_id in enumerate(video_ids_by_format['shorts'], 1):
                print(f"[Short {i}/{len(video_ids_by_format['shorts'])}]")
                self.extract_video_metadata(video_id, expected_format='short')
        
        # Process long videos
        if video_ids_by_format['long']:
            print(f"\n📹 Processing {len(video_ids_by_format['long'])} long videos...")
            for i, video_id in enumerate(video_ids_by_format['long'], 1):
                print(f"[Long {i}/{len(video_ids_by_format['long'])}]")
                self.extract_video_metadata(video_id, expected_format='long')
        
        # Capture channel information from first video
        if self.videos:
            self.channel_id = self.videos[0].channel_id
            self.channel_name = self.videos[0].channel_name
        
        return self.videos
    
    def generate_report(self, output_path: Optional[str] = None) -> str:
        """
        Generate comprehensive report of scraped data.
        
        Args:
            output_path: Path to save markdown report (if None, uses channel-specific dir)
            
        Returns:
            Markdown report text
        """
        if not self.videos:
            return "No videos scraped"
        
        # Use channel-specific directory if no output path specified
        if output_path is None:
            channel_dir = self._get_channel_output_dir()
            output_path = str(channel_dir / "channel_report.md")
        
        # Calculate aggregate statistics
        total_views = sum(v.view_count for v in self.videos)
        total_likes = sum(v.like_count for v in self.videos if v.like_count)
        total_comments = sum(v.comment_count for v in self.videos if v.comment_count)
        avg_engagement = sum(v.engagement_rate for v in self.videos if v.engagement_rate) / len([v for v in self.videos if v.engagement_rate]) if any(v.engagement_rate for v in self.videos) else 0
        videos_with_subtitles = sum(1 for v in self.videos if v.subtitles_available)
        
        # Calculate format-specific statistics
        shorts = [v for v in self.videos if v.video_format == 'short']
        
        # Build report title with channel info
        channel_info = ""
        if self.channel_name:
            channel_info = f" - {self.channel_name}"
        if self.channel_id:
            channel_info += f" ({self.channel_id})"
        
        report = f"""# YouTube Channel Scraping Report{channel_info}

## Channel Information

- **Channel Name**: {self.channel_name or 'N/A'}
- **Channel ID**: {self.channel_id or 'N/A'}
- **Scrape Date**: {self._get_timestamp()}
        # Calculate story video statistics
        story_videos = [v for v in self.videos if v.is_story_video]
        non_story_videos = [v for v in self.videos if not v.is_story_video]
        avg_story_confidence = sum(v.story_confidence_score for v in self.videos if v.story_confidence_score) / len(self.videos) if self.videos else 0
        
        report = f"""# YouTube Channel Scraping Report (Shorts Only)

## Summary Statistics

- **Total Shorts Scraped**: {len(self.videos)}
- **Total Views**: {total_views:,}
- **Average Views**: {total_views // len(self.videos):,}
- **Total Likes**: {total_likes:,}
- **Total Comments**: {total_comments:,}
- **Average Engagement Rate**: {avg_engagement:.2f}%
- **Shorts with Subtitles**: {videos_with_subtitles} ({videos_with_subtitles/len(self.videos)*100:.1f}%)
"""
        
        # Add story filtering information if story_only mode was used
        if self.story_only:
            report += f"""
## Story Filtering (Story-Only Mode: ENABLED)

- **Story Videos Included**: {len(story_videos)} ({len(story_videos)/len(self.videos)*100:.1f}% of scraped)
- **Non-Story Videos Filtered Out**: {self.filtered_count}
- **Average Story Confidence**: {avg_story_confidence:.2f}
"""
        else:
            report += f"""
## Story Video Analysis

- **Story Videos Detected**: {len(story_videos)} ({len(story_videos)/len(self.videos)*100:.1f}% of total)
- **Non-Story Videos**: {len(non_story_videos)} ({len(non_story_videos)/len(self.videos)*100:.1f}% of total)
- **Average Story Confidence**: {avg_story_confidence:.2f}
"""
        
        report += f"""
## Shorts Analysis

All videos are YouTube Shorts (≤3min, Vertical format):
- **Count**: {len(shorts)}
- **Total Views**: {sum(v.view_count for v in shorts):,}
- **Avg Views**: {sum(v.view_count for v in shorts) // len(shorts) if shorts else 0:,}

## Engagement Metrics Overview

"""
        
        for video in self.videos:
            if video.engagement_rate:
                report += f"- **{video.title[:50]}...**: {video.engagement_rate:.2f}% engagement\n"
        
        report += f"""

## Video Details

"""
        
        for i, video in enumerate(self.videos, 1):
            format_icon = "🎬" if video.video_format == "short" else "📹"
            report += f"""### {i}. {format_icon} {video.title}

**Basic Information:**
- **Video ID**: {video.video_id}
- **URL**: {video.url}
- **Format**: {video.video_format.upper() if video.video_format else 'N/A'}
- **Channel**: {video.channel_name or 'N/A'}
- **Upload Date**: {video.upload_date}
- **Duration**: {video.duration}

**Story Classification:**
- **Is Story Video**: {'✅ Yes' if video.is_story_video else '❌ No'}
- **Story Confidence Score**: {f"{video.story_confidence_score:.2f}" if video.story_confidence_score is not None else 'N/A'}
- **Story Indicators**: {', '.join(video.story_indicators) if video.story_indicators else 'None detected'}

**Viewership & Engagement:**
- **Views**: {video.view_count:,}
- **Likes**: {video.like_count if video.like_count else 'N/A'}
- **Comments**: {video.comment_count if video.comment_count else 'N/A'}
- **Engagement Rate**: {f"{video.engagement_rate:.2f}%" if video.engagement_rate else 'N/A'}
- **Like-to-View Ratio**: {f"{video.like_to_view_ratio:.3f}%" if video.like_to_view_ratio else 'N/A'}
- **Comment-to-View Ratio**: {f"{video.comment_to_view_ratio:.3f}%" if video.comment_to_view_ratio else 'N/A'}
- **Views Per Day**: {f"{video.views_per_day:.0f}" if video.views_per_day else 'N/A'}
- **Views Per Hour**: {f"{video.views_per_hour:.1f}" if video.views_per_hour else 'N/A'}

**Video Quality:**
- **Resolution**: {video.resolution or 'N/A'}
- **FPS**: {video.fps or 'N/A'}
- **Aspect Ratio**: {video.aspect_ratio or 'N/A'}

**Content Analysis:**
- **Title Length**: {video.title_length} characters
- **Description Length**: {video.description_length} characters
- **Tag Count**: {video.tag_count}
- **Has Chapters**: {'Yes' if video.has_chapters else 'No'}
- **Chapter Count**: {video.chapter_count if video.chapter_count else 'N/A'}
- **Subtitles Available**: {'Yes' if video.subtitles_available else 'No'}
- **Categories**: {', '.join(video.categories) if video.categories else 'N/A'}

**Channel Information:**
- **Channel ID**: {video.channel_id or 'N/A'}
- **Channel Followers**: {f"{video.channel_follower_count:,}" if video.channel_follower_count else 'N/A'}

**Description:**
```
{video.description[:300]}{'...' if len(video.description) > 300 else ''}
```

**Tags:**
{', '.join(video.tags[:15])}{'...' if len(video.tags) > 15 else ''}

**Subtitle Text (First 200 words):**
```
{' '.join((video.subtitle_text or '').split()[:200])}{'...' if video.subtitle_text and len(video.subtitle_text.split()) > 200 else ''}
```

---

"""
        
        report += self._generate_performance_analysis()
        report += self._generate_content_patterns_analysis()
        
        channel_dir = self._get_channel_output_dir()
        report += f"""

## Data Files

All scraped data has been saved to channel-specific directory: `{channel_dir.name}/`

Files:
- **Markdown Report**: `channel_report.md` - This comprehensive report
- **JSON Data**: `channel_data.json` - Machine-readable data with all metrics
- **JSON Summary**: `channel_data_summary.md` - JSON data converted to Markdown for easy viewing
- **Individual Video Info**: `{{video_id}}.info.json` - Full metadata per video
- **Video Info Markdown**: `{{video_id}}.info.md` - Video metadata in Markdown format
- **Subtitles**: `{{video_id}}.srt` - Subtitle files where available

## Key Insights

### Top Performing Videos by Views
"""
        
        sorted_by_views = sorted(self.videos, key=lambda v: v.view_count, reverse=True)[:5]
        for i, video in enumerate(sorted_by_views, 1):
            report += f"{i}. **{video.title}** - {video.view_count:,} views\n"
        
        report += """

### Highest Engagement Rates
"""
        
        sorted_by_engagement = sorted([v for v in self.videos if v.engagement_rate], 
                                     key=lambda v: v.engagement_rate, reverse=True)[:5]
        for i, video in enumerate(sorted_by_engagement, 1):
            report += f"{i}. **{video.title}** - {video.engagement_rate:.2f}% engagement\n"
        
        report += """

### Most Viewed Per Day
"""
        
        sorted_by_daily_views = sorted([v for v in self.videos if v.views_per_day], 
                                      key=lambda v: v.views_per_day, reverse=True)[:5]
        for i, video in enumerate(sorted_by_daily_views, 1):
            report += f"{i}. **{video.title}** - {video.views_per_day:.0f} views/day\n"
        
        report += f"""

---

**Scraping Date**: {self._get_timestamp()}
**Videos Analyzed**: {len(self.videos)}
**Success Rate**: {videos_with_subtitles / len(self.videos) * 100:.1f}% with subtitles
"""
        
        if output_path:
            Path(output_path).write_text(report, encoding='utf-8')
            print(f"\n✅ Report saved to: {output_path}")
        
        return report
    
    def _generate_performance_analysis(self) -> str:
        """Generate performance analysis section."""
        if not self.videos:
            return ""
        
        report = """
## Performance Analysis

### Engagement Metrics Distribution
"""
        
        # Calculate engagement distribution
        high_engagement = sum(1 for v in self.videos if v.engagement_rate and v.engagement_rate > 5)
        medium_engagement = sum(1 for v in self.videos if v.engagement_rate and 2 < v.engagement_rate <= 5)
        low_engagement = sum(1 for v in self.videos if v.engagement_rate and v.engagement_rate <= 2)
        
        report += f"""
- **High Engagement (>5%)**: {high_engagement} videos
- **Medium Engagement (2-5%)**: {medium_engagement} videos
- **Low Engagement (<2%)**: {low_engagement} videos

### Views Performance
"""
        
        avg_views = sum(v.view_count for v in self.videos) / len(self.videos)
        above_avg = sum(1 for v in self.videos if v.view_count > avg_views)
        below_avg = len(self.videos) - above_avg
        
        report += f"""
- **Average Views**: {avg_views:,.0f}
- **Videos Above Average**: {above_avg}
- **Videos Below Average**: {below_avg}

### Content Quality Indicators
"""
        
        videos_with_chapters = sum(1 for v in self.videos if v.has_chapters)
        avg_title_length = sum(v.title_length for v in self.videos) / len(self.videos)
        avg_tag_count = sum(v.tag_count for v in self.videos) / len(self.videos)
        
        report += f"""
- **Videos with Chapters**: {videos_with_chapters} ({videos_with_chapters/len(self.videos)*100:.1f}%)
- **Average Title Length**: {avg_title_length:.0f} characters
- **Average Tag Count**: {avg_tag_count:.1f} tags
- **Videos with Subtitles**: {sum(1 for v in self.videos if v.subtitles_available)}

"""
        
        return report
    
    def _generate_content_patterns_analysis(self) -> str:
        """Generate content patterns analysis section."""
        report = """
## Content Patterns Analysis

### Video Format Distribution
"""
        
        shorts = [v for v in self.videos if v.video_format == 'short']
        longs = [v for v in self.videos if v.video_format == 'long']
        unknown = [v for v in self.videos if not v.video_format]
        
        report += f"""
- **Shorts (≤3min, Vertical)**: {len(shorts)} videos
- **Long Videos**: {len(longs)} videos
- **Unknown Format**: {len(unknown)} videos

### Most Common Tags
"""
        
        # Analyze common tags
        all_tags = []
        for video in self.videos:
            all_tags.extend(video.tags)
        
        from collections import Counter
        tag_counts = Counter(all_tags)
        
        for tag, count in tag_counts.most_common(20):
            report += f"- **{tag}**: {count} videos\n"
        
        report += """

### Title Patterns

Common words in titles:
"""
        
        # Analyze title patterns
        all_title_words = []
        for video in self.videos:
            # Remove common words
            words = video.title.lower().split()
            words = [w for w in words if len(w) > 3 and w not in ['the', 'and', 'for', 'with', 'this', 'that', 'from', 'your']]
            all_title_words.extend(words)
        
        word_counts = Counter(all_title_words)
        
        for word, count in word_counts.most_common(20):
            report += f"- **{word}**: {count} times\n"
        
        report += """

### Video Duration Distribution
"""
        
        short_videos = sum(1 for v in self.videos if v.duration_seconds < 300)
        medium_videos = sum(1 for v in self.videos if 300 <= v.duration_seconds < 900)
        long_videos = sum(1 for v in self.videos if v.duration_seconds >= 900)
        
        report += f"""
- **Short (<5 min)**: {short_videos} videos
- **Medium (5-15 min)**: {medium_videos} videos
- **Long (>15 min)**: {long_videos} videos

"""
        
        return report
    
    def save_json(self, output_path: Optional[str] = None):
        """
        Save all video metadata as JSON with comprehensive analytics.
        Also creates a markdown version for easier viewing on GitHub.
        
        Args:
            output_path: Path to save JSON file (if None, uses channel-specific dir)
        """
        # Use channel-specific directory if no output path specified
        if output_path is None:
            channel_dir = self._get_channel_output_dir()
            output_path = str(channel_dir / "channel_data.json")
        
        # Calculate aggregate statistics
        total_likes = sum(v.like_count for v in self.videos if v.like_count)
        total_comments = sum(v.comment_count for v in self.videos if v.comment_count)
        avg_engagement = sum(v.engagement_rate for v in self.videos if v.engagement_rate) / len([v for v in self.videos if v.engagement_rate]) if any(v.engagement_rate for v in self.videos) else 0
        avg_views_per_day = sum(v.views_per_day for v in self.videos if v.views_per_day) / len([v for v in self.videos if v.views_per_day]) if any(v.views_per_day for v in self.videos) else 0
        
        # Format-specific statistics
        shorts = [v for v in self.videos if v.video_format == 'short']
        
        # Story video statistics
        story_videos = [v for v in self.videos if v.is_story_video]
        non_story_videos = [v for v in self.videos if not v.is_story_video]
        avg_story_confidence = sum(v.story_confidence_score for v in self.videos if v.story_confidence_score) / len(self.videos) if self.videos else 0
        
        data = {
            'channel_id': self.channel_id,
            'channel_name': self.channel_name,
            'videos': [v.to_dict() for v in self.videos],
            'summary': {
                'total_shorts': len(self.videos),
                'shorts_with_subtitles': sum(1 for v in self.videos if v.subtitles_available),
                'total_views': sum(v.view_count for v in self.videos),
                'average_views': sum(v.view_count for v in self.videos) // len(self.videos) if self.videos else 0,
                'total_likes': total_likes,
                'total_comments': total_comments,
                'average_engagement_rate': round(avg_engagement, 2),
                'average_views_per_day': round(avg_views_per_day, 2),
                'shorts_with_chapters': sum(1 for v in self.videos if v.has_chapters),
            },
            'story_analysis': {
                'story_only_mode': self.story_only,
                'story_videos_count': len(story_videos),
                'non_story_videos_count': len(non_story_videos),
                'filtered_out_count': self.filtered_count,
                'average_story_confidence': round(avg_story_confidence, 2),
                'story_videos_percentage': round(len(story_videos) / len(self.videos) * 100, 1) if self.videos else 0,
            },
            'shorts_breakdown': {
                'count': len(shorts),
                'total_views': sum(v.view_count for v in shorts),
                'average_views': sum(v.view_count for v in shorts) // len(shorts) if shorts else 0,
                'average_duration': round(sum(v.duration_seconds for v in shorts) / len(shorts), 1) if shorts else 0,
            },
            'engagement_metrics': {
                'high_engagement_videos': sum(1 for v in self.videos if v.engagement_rate and v.engagement_rate > 5),
                'medium_engagement_videos': sum(1 for v in self.videos if v.engagement_rate and 2 < v.engagement_rate <= 5),
                'low_engagement_videos': sum(1 for v in self.videos if v.engagement_rate and v.engagement_rate <= 2),
            },
            'content_quality': {
                'average_title_length': round(sum(v.title_length for v in self.videos) / len(self.videos), 1),
                'average_description_length': round(sum(v.description_length for v in self.videos) / len(self.videos), 1),
                'average_tag_count': round(sum(v.tag_count for v in self.videos) / len(self.videos), 1),
            },
            'shorts_durations': {
                'under_1_min': sum(1 for v in self.videos if v.duration_seconds < 60),
                'one_to_two_min': sum(1 for v in self.videos if 60 <= v.duration_seconds < 120),
                'two_to_three_min': sum(1 for v in self.videos if 120 <= v.duration_seconds <= 180),
                'average_duration_seconds': round(sum(v.duration_seconds for v in self.videos) / len(self.videos)),
            },
            'timestamp': self._get_timestamp(),
            'output_directory': str(self.output_dir.resolve())
        }
        
        # Save JSON
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
        
        print(f"✅ JSON data saved to: {output_path}")
        print(f"   📊 Included {len(self.videos)} videos with comprehensive analytics")
        print(f"   🎬 Shorts: {len(shorts)}, 📹 Long: {len(longs)}")
        
        # Create markdown version for easier GitHub viewing
        md_path = output_path.replace('.json', '_summary.md')
        self._save_json_as_markdown(data, md_path)
        print(f"   📄 Markdown version saved to: {md_path}")
        print(f"   📊 Included {len(self.videos)} shorts with comprehensive analytics")
        print(f"   🎬 All videos are shorts")
    
    def _get_timestamp(self):
        """Get current timestamp."""
        from datetime import datetime
        return datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    def _save_json_as_markdown(self, data: dict, output_path: str):
        """
        Convert JSON data to a readable Markdown format.
        
        Args:
            data: Dictionary containing channel data
            output_path: Path to save markdown file
        """
        md_content = f"""# Channel Data Summary

**Generated**: {data.get('timestamp', 'N/A')}  
**Channel**: {data.get('channel_name', 'N/A')} ({data.get('channel_id', 'N/A')})

## Summary Statistics

"""
        
        summary = data.get('summary', {})
        for key, value in summary.items():
            label = key.replace('_', ' ').title()
            md_content += f"- **{label}**: {value:,}\n" if isinstance(value, (int, float)) else f"- **{label}**: {value}\n"
        
        md_content += "\n## Format Breakdown\n\n"
        format_breakdown = data.get('format_breakdown', {})
        for format_type, stats in format_breakdown.items():
            md_content += f"### {format_type.title()}\n\n"
            for key, value in stats.items():
                label = key.replace('_', ' ').title()
                md_content += f"- **{label}**: {value:,}\n" if isinstance(value, (int, float)) else f"- **{label}**: {value}\n"
            md_content += "\n"
        
        md_content += "## Engagement Metrics\n\n"
        engagement = data.get('engagement_metrics', {})
        for key, value in engagement.items():
            label = key.replace('_', ' ').title()
            md_content += f"- **{label}**: {value}\n"
        
        md_content += "\n## Content Quality\n\n"
        quality = data.get('content_quality', {})
        for key, value in quality.items():
            label = key.replace('_', ' ').title()
            md_content += f"- **{label}**: {value}\n"
        
        md_content += "\n## Video Durations\n\n"
        durations = data.get('video_durations', {})
        for key, value in durations.items():
            label = key.replace('_', ' ').title()
            md_content += f"- **{label}**: {value}\n"
        
        md_content += f"""

## Videos List

Total videos: {len(data.get('videos', []))}

"""
        
        for i, video in enumerate(data.get('videos', []), 1):
            format_icon = "🎬" if video.get('video_format') == "short" else "📹"
            md_content += f"""### {i}. {format_icon} {video.get('title', 'N/A')}

- **Video ID**: {video.get('video_id', 'N/A')}
- **URL**: {video.get('url', 'N/A')}
- **Views**: {video.get('view_count', 0):,}
- **Duration**: {video.get('duration', 'N/A')}
- **Engagement Rate**: {video.get('engagement_rate', 'N/A')}%
- **Upload Date**: {video.get('upload_date', 'N/A')}

"""
        
        md_content += """
---

*This file is a Markdown representation of the JSON data for easier viewing on GitHub.*  
*For complete data, see `channel_data.json`*
"""
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(md_content)
    
    def _get_channel_output_dir(self) -> Path:
        """
        Get channel-specific output directory.
        Creates a subdirectory using channel ID and name for organization.
        
        Returns:
            Path to channel-specific directory
        """
        if self.channel_id and self.channel_name:
            # Sanitize channel name for filesystem
            safe_name = "".join(c if c.isalnum() or c in (' ', '-', '_') else '_' for c in self.channel_name)
            safe_name = safe_name.replace(' ', '_')
            channel_dir = self.output_dir / f"{self.channel_id}_{safe_name}"
        elif self.channel_id:
            channel_dir = self.output_dir / self.channel_id
        else:
            # Fallback to timestamp if no channel info
            from datetime import datetime
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            channel_dir = self.output_dir / f"channel_{timestamp}"
        
        channel_dir.mkdir(parents=True, exist_ok=True)
        return channel_dir


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Scrape metadata from YouTube channel videos'
    )
    parser.add_argument(
        'channel',
        nargs='?',
        help='Channel URL, handle (@username), or ID (optional - will prompt if not provided)'
    )
    parser.add_argument(
        '--top',
        type=int,
        default=10,
        help='Number of top shorts to scrape (default: 10)'
    )
    parser.add_argument(
        '--output',
        default='/tmp/youtube_channel_data',
        help='Output directory (default: /tmp/youtube_channel_data)'
    )
    parser.add_argument(
        '--story-only',
        action='store_true',
        help='Only include videos detected as story videos in the analysis (filters out non-story content)'
    )
    
    args = parser.parse_args()
    
    # Interactive mode: prompt for channel if not provided
    channel = args.channel
    if not channel:
        print("\n🔬 YouTube Channel Scraper")
        print("=" * 60)
        print("\nNo channel provided. Please enter the channel information.")
        print("\nYou can provide:")
        print("  • Full channel URL: https://www.youtube.com/@channelname")
        print("  • Channel handle: @channelname")
        print("  • Channel ID: UC1234567890")
        print("  • Just the channel name: channelname")
        print()

        while True:
            channel = input("Enter channel URL, handle, or name: ").strip()
            if channel:
                break
            print("❌ Channel cannot be empty. Please try again.")
        print()
    else:
        print("\n🔬 YouTube Channel Scraper")

    print(f"📺 Channel: {channel}")
    print(f"📊 Shorts to scrape: Top {args.top}")
    if args.story_only:
        print("📖 Story-Only Mode: ENABLED (will filter out non-story videos)\n")
    else:
        print("📖 Story-Only Mode: DISABLED (will include all videos)\n")
    
    scraper = YouTubeChannelScraper(output_dir=args.output, story_only=args.story_only)
    videos = scraper.scrape_channel(channel, args.top)
    
    if videos:
        # Get channel-specific output directory
        channel_dir = scraper._get_channel_output_dir()
        
        # Generate report (will automatically use channel-specific dir)
        scraper.generate_report()
        
        # Save JSON (will automatically use channel-specific dir)
        scraper.save_json()
        
        print("\n✅ Scraping complete!")
        print(f"📁 Channel-specific output directory: {channel_dir}")
        print(f"📄 Report: {channel_dir / 'channel_report.md'}")
        print(f"💾 JSON data: {channel_dir / 'channel_data.json'}")
        print(f"📄 Markdown summary: {channel_dir / 'channel_data_summary.md'}")
        print(f"📁 Output directory: {args.output}")
        print(f"📄 Report: {report_path}")
        print(f"💾 JSON data: {json_path}")
        if args.story_only and scraper.filtered_count > 0:
            print(f"📖 Filtered out {scraper.filtered_count} non-story videos")
    else:
        print("\n❌ No videos scraped")
        sys.exit(1)


if __name__ == "__main__":
    main()
