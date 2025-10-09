"""
YouTube Channel Scraper

Scrapes titles, subtitles text, descriptions, tags, and other useful metadata
from the top N videos on a YouTube channel.

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
    view_count: int
    like_count: Optional[int]
    comment_count: Optional[int]
    upload_date: str
    url: str
    thumbnail_url: str
    subtitles_available: bool
    subtitle_text: Optional[str]
    
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
            
            # Create metadata object
            metadata = VideoMetadata(
                video_id=video_id,
                title=info.get('title', ''),
                description=info.get('description', ''),
                tags=info.get('tags', []),
                duration=self._format_duration(info.get('duration', 0)),
                view_count=info.get('view_count', 0),
                like_count=info.get('like_count'),
                comment_count=info.get('comment_count'),
                upload_date=info.get('upload_date', ''),
                url=video_url,
                thumbnail_url=info.get('thumbnail', ''),
                subtitles_available=subtitle_text is not None,
                subtitle_text=subtitle_text
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
        
        report = f"""# YouTube Channel Scraping Report

## Summary

- **Total Videos Scraped**: {len(self.videos)}
- **Videos with Subtitles**: {sum(1 for v in self.videos if v.subtitles_available)}
- **Total Views**: {sum(v.view_count for v in self.videos):,}
- **Average Views**: {sum(v.view_count for v in self.videos) // len(self.videos):,}

## Video Details

"""
        
        for i, video in enumerate(self.videos, 1):
            report += f"""### {i}. {video.title}

**Metadata:**
- **Video ID**: {video.video_id}
- **URL**: {video.url}
- **Duration**: {video.duration}
- **Views**: {video.view_count:,}
- **Likes**: {video.like_count if video.like_count else 'N/A'}
- **Comments**: {video.comment_count if video.comment_count else 'N/A'}
- **Upload Date**: {video.upload_date}
- **Subtitles Available**: {'Yes' if video.subtitles_available else 'No'}

**Description:**
```
{video.description[:300]}{'...' if len(video.description) > 300 else ''}
```

**Tags:**
{', '.join(video.tags[:10])}{'...' if len(video.tags) > 10 else ''}

**Subtitle Text (First 200 words):**
```
{' '.join((video.subtitle_text or '').split()[:200])}{'...' if video.subtitle_text and len(video.subtitle_text.split()) > 200 else ''}
```

---

"""
        
        report += f"""## Common Patterns

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
        
        report += f"""

### Title Patterns

Common words in titles:
"""
        
        # Analyze title patterns
        all_title_words = []
        for video in self.videos:
            # Remove common words
            words = video.title.lower().split()
            words = [w for w in words if len(w) > 3 and w not in ['the', 'and', 'for', 'with', 'this', 'that']]
            all_title_words.extend(words)
        
        word_counts = Counter(all_title_words)
        
        for word, count in word_counts.most_common(20):
            report += f"- **{word}**: {count} times\n"
        
        report += f"""

### Performance Metrics

**Top Performing Videos (by views):**
"""
        
        sorted_videos = sorted(self.videos, key=lambda v: v.view_count, reverse=True)
        
        for i, video in enumerate(sorted_videos[:5], 1):
            report += f"{i}. **{video.title}** - {video.view_count:,} views\n"
        
        report += """

## Data Files

All scraped data has been saved to:
- **JSON format**: `channel_data.json` - Machine-readable data
- **Individual video info**: `{video_id}.info.json` - Full metadata per video
- **Subtitles**: `{video_id}.srt` - Subtitle files where available

## Usage in StoryGenerator

This data can be used to:
1. Analyze successful content patterns
2. Extract common themes and topics
3. Identify effective titles and descriptions
4. Study subtitle patterns
5. Benchmark performance metrics

---

**Scraping Date**: {self._get_timestamp()}
**Videos Analyzed**: {len(self.videos)}
**Success Rate**: {sum(1 for v in self.videos if v.subtitles_available) / len(self.videos) * 100:.1f}% with subtitles
"""
        
        if output_path:
            Path(output_path).write_text(report, encoding='utf-8')
            print(f"\n✅ Report saved to: {output_path}")
        
        return report
    
    def save_json(self, output_path: str):
        """Save all video metadata as JSON."""
        data = {
            'videos': [v.to_dict() for v in self.videos],
            'summary': {
                'total_videos': len(self.videos),
                'videos_with_subtitles': sum(1 for v in self.videos if v.subtitles_available),
                'total_views': sum(v.view_count for v in self.videos),
                'average_views': sum(v.view_count for v in self.videos) // len(self.videos) if self.videos else 0,
            },
            'timestamp': self._get_timestamp()
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
        
        print(f"✅ JSON data saved to: {output_path}")
    
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
