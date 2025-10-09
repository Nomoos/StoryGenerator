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
    
    def to_dict(self):
        return asdict(self)


class YouTubeChannelScraper:
    """Scrapes metadata from YouTube channel videos."""
    
    def __init__(self, output_dir: str = "/tmp/youtube_channel_data"):
        """
        Initialize scraper.
        
        Args:
            output_dir: Directory to store scraped data
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.videos: List[VideoMetadata] = []
    
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
    
    def get_channel_videos(self, channel_url: str, top_n: int = 10) -> List[str]:
        """
        Get list of video IDs from channel.
        
        Args:
            channel_url: Channel URL
            top_n: Number of top videos to retrieve
            
        Returns:
            List of video IDs
        """
        print(f"📺 Fetching top {top_n} videos from channel...")
        
        # Use yt-dlp to get video list sorted by views
        cmd = [
            "yt-dlp",
            "--flat-playlist",
            "--print", "id",
            "--playlist-end", str(top_n),
            "--playlist-reverse",  # Get most recent first
            channel_url + "/videos"
        ]
        
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=60
            )
            
            if result.returncode != 0:
                print(f"⚠️ Error fetching videos: {result.stderr}")
                return []
            
            video_ids = [line.strip() for line in result.stdout.split('\n') if line.strip()]
            print(f"✅ Found {len(video_ids)} videos")
            return video_ids[:top_n]
            
        except subprocess.TimeoutExpired:
            print("⚠️ Timeout while fetching videos")
            return []
        except Exception as e:
            print(f"⚠️ Error: {e}")
            return []
    
    def extract_video_metadata(self, video_id: str) -> Optional[VideoMetadata]:
        """
        Extract comprehensive metadata for a single video.
        
        Args:
            video_id: YouTube video ID
            
        Returns:
            VideoMetadata object or None on failure
        """
        print(f"  📹 Extracting metadata for: {video_id}")
        
        video_url = f"https://www.youtube.com/watch?v={video_id}"
        
        # Get metadata using yt-dlp
        cmd = [
            "yt-dlp",
            "--skip-download",
            "--write-info-json",
            "--write-auto-sub",
            "--sub-lang", "en",
            "--sub-format", "srt",
            "-o", str(self.output_dir / f"{video_id}"),
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
            info_json_path = self.output_dir / f"{video_id}.info.json"
            if not info_json_path.exists():
                print(f"    ⚠️ Could not retrieve metadata for {video_id}")
                return None
            
            with open(info_json_path, 'r', encoding='utf-8') as f:
                info = json.load(f)
            
            # Extract subtitle text if available
            subtitle_text = None
            subtitle_files = list(self.output_dir.glob(f"{video_id}*.srt"))
            if subtitle_files:
                with open(subtitle_files[0], 'r', encoding='utf-8') as f:
                    subtitle_text = self._parse_srt_to_text(f.read())
            
            # Extract video quality info from formats
            resolution = None
            fps = None
            aspect_ratio = None
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
            
            # Extract chapters information
            chapters = info.get('chapters', [])
            has_chapters = len(chapters) > 0
            chapter_count = len(chapters) if has_chapters else None
            
            # Get basic metadata
            duration_seconds = info.get('duration', 0)
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
            
            self.videos.append(metadata)
            print(f"    ✅ Extracted: {metadata.title[:50]}...")
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
    
    def _format_duration(self, seconds: int) -> str:
        """Format duration in seconds to HH:MM:SS."""
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        secs = seconds % 60
        
        if hours > 0:
            return f"{hours:02d}:{minutes:02d}:{secs:02d}"
        else:
            return f"{minutes:02d}:{secs:02d}"
    
    def scrape_channel(self, channel_input: str, top_n: int = 10) -> List[VideoMetadata]:
        """
        Scrape top N videos from a channel.
        
        Args:
            channel_input: Channel URL, handle, or ID
            top_n: Number of videos to scrape
            
        Returns:
            List of VideoMetadata objects
        """
        # Check dependencies
        if not self.check_dependencies():
            return []
        
        # Extract channel URL
        channel_url = self.extract_channel_url(channel_input)
        print(f"📺 Channel URL: {channel_url}")
        
        # Get video IDs
        video_ids = self.get_channel_videos(channel_url, top_n)
        
        if not video_ids:
            print("❌ No videos found")
            return []
        
        # Extract metadata for each video
        print(f"\n📊 Extracting metadata for {len(video_ids)} videos...\n")
        
        for i, video_id in enumerate(video_ids, 1):
            print(f"[{i}/{len(video_ids)}]")
            self.extract_video_metadata(video_id)
        
        return self.videos
    
    def generate_report(self, output_path: Optional[str] = None) -> str:
        """
        Generate comprehensive report of scraped data.
        
        Args:
            output_path: Path to save markdown report
            
        Returns:
            Markdown report text
        """
        if not self.videos:
            return "No videos scraped"
        
        # Calculate aggregate statistics
        total_views = sum(v.view_count for v in self.videos)
        total_likes = sum(v.like_count for v in self.videos if v.like_count)
        total_comments = sum(v.comment_count for v in self.videos if v.comment_count)
        avg_engagement = sum(v.engagement_rate for v in self.videos if v.engagement_rate) / len([v for v in self.videos if v.engagement_rate]) if any(v.engagement_rate for v in self.videos) else 0
        videos_with_subtitles = sum(1 for v in self.videos if v.subtitles_available)
        
        report = f"""# YouTube Channel Scraping Report

## Summary Statistics

- **Total Videos Scraped**: {len(self.videos)}
- **Total Views**: {total_views:,}
- **Average Views**: {total_views // len(self.videos):,}
- **Total Likes**: {total_likes:,}
- **Total Comments**: {total_comments:,}
- **Average Engagement Rate**: {avg_engagement:.2f}%
- **Videos with Subtitles**: {videos_with_subtitles} ({videos_with_subtitles/len(self.videos)*100:.1f}%)

## Engagement Metrics Overview

"""
        
        for video in self.videos:
            if video.engagement_rate:
                report += f"- **{video.title[:50]}...**: {video.engagement_rate:.2f}% engagement\n"
        
        report += f"""

## Video Details

"""
        
        for i, video in enumerate(self.videos, 1):
            report += f"""### {i}. {video.title}

**Basic Information:**
- **Video ID**: {video.video_id}
- **URL**: {video.url}
- **Channel**: {video.channel_name or 'N/A'}
- **Upload Date**: {video.upload_date}
- **Duration**: {video.duration}

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
        
        report += f"""

## Data Files

All scraped data has been saved to:
- **JSON format**: `channel_data.json` - Machine-readable data with all metrics
- **Individual video info**: `{{video_id}}.info.json` - Full metadata per video
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
    
    def save_json(self, output_path: str):
        """Save all video metadata as JSON with comprehensive analytics."""
        # Calculate aggregate statistics
        total_likes = sum(v.like_count for v in self.videos if v.like_count)
        total_comments = sum(v.comment_count for v in self.videos if v.comment_count)
        avg_engagement = sum(v.engagement_rate for v in self.videos if v.engagement_rate) / len([v for v in self.videos if v.engagement_rate]) if any(v.engagement_rate for v in self.videos) else 0
        avg_views_per_day = sum(v.views_per_day for v in self.videos if v.views_per_day) / len([v for v in self.videos if v.views_per_day]) if any(v.views_per_day for v in self.videos) else 0
        
        data = {
            'videos': [v.to_dict() for v in self.videos],
            'summary': {
                'total_videos': len(self.videos),
                'videos_with_subtitles': sum(1 for v in self.videos if v.subtitles_available),
                'total_views': sum(v.view_count for v in self.videos),
                'average_views': sum(v.view_count for v in self.videos) // len(self.videos) if self.videos else 0,
                'total_likes': total_likes,
                'total_comments': total_comments,
                'average_engagement_rate': round(avg_engagement, 2),
                'average_views_per_day': round(avg_views_per_day, 2),
                'videos_with_chapters': sum(1 for v in self.videos if v.has_chapters),
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
            'video_durations': {
                'short_videos': sum(1 for v in self.videos if v.duration_seconds < 300),
                'medium_videos': sum(1 for v in self.videos if 300 <= v.duration_seconds < 900),
                'long_videos': sum(1 for v in self.videos if v.duration_seconds >= 900),
                'average_duration_seconds': round(sum(v.duration_seconds for v in self.videos) / len(self.videos)),
            },
            'timestamp': self._get_timestamp()
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
        
        print(f"✅ JSON data saved to: {output_path}")
        print(f"   📊 Included {len(self.videos)} videos with comprehensive analytics")
    
    def _get_timestamp(self):
        """Get current timestamp."""
        from datetime import datetime
        return datetime.now().strftime('%Y-%m-%d %H:%M:%S')


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
        help='Number of top videos to scrape (default: 10)'
    )
    parser.add_argument(
        '--output',
        default='/tmp/youtube_channel_data',
        help='Output directory (default: /tmp/youtube_channel_data)'
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
    print(f"📊 Top Videos: {args.top}\n")
    
    scraper = YouTubeChannelScraper(output_dir=args.output)
    videos = scraper.scrape_channel(channel, args.top)
    
    if videos:
        # Generate report
        report_path = Path(args.output) / 'channel_report.md'
        scraper.generate_report(str(report_path))
        
        # Save JSON
        json_path = Path(args.output) / 'channel_data.json'
        scraper.save_json(str(json_path))
        
        print("\n✅ Scraping complete!")
        print(f"📁 Output directory: {args.output}")
        print(f"📄 Report: {report_path}")
        print(f"💾 JSON data: {json_path}")
    else:
        print("\n❌ No videos scraped")
        sys.exit(1)


if __name__ == "__main__":
    main()
