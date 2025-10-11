"""
YouTube Video Subtitle Analyzer

This research tool analyzes YouTube videos to understand subtitle implementation,
timing, formatting, and styling techniques. It helps inform subtitle generation
for the StoryGenerator pipeline.

Features:
- Download YouTube videos and extract subtitles
- Analyze subtitle timing (duration, gaps, overlaps)
- Extract formatting and styling information
- Analyze subtitle readability metrics
- Generate comprehensive analysis reports

Usage:
    python youtube_subtitle_analyzer.py <youtube_url>
    python youtube_subtitle_analyzer.py https://www.youtube.com/shorts/41QD8C6tqIU
"""

import os
import json
import re
import subprocess
import sys
from dataclasses import dataclass, asdict
from typing import List, Dict, Optional
from pathlib import Path
from datetime import datetime


@dataclass
class SubtitleSegment:
    """Represents a single subtitle segment."""
    index: int
    start_time: float
    end_time: float
    duration: float
    text: str
    word_count: int
    char_count: int
    
    @property
    def words_per_second(self) -> float:
        """Calculate reading speed in words per second."""
        return self.word_count / self.duration if self.duration > 0 else 0


@dataclass
class SubtitleAnalysis:
    """Complete analysis of subtitle data."""
    video_id: str
    video_url: str
    total_segments: int
    total_duration: float
    avg_segment_duration: float
    min_segment_duration: float
    max_segment_duration: float
    avg_words_per_segment: float
    avg_chars_per_segment: float
    avg_reading_speed_wps: float  # words per second
    total_gaps: int
    avg_gap_duration: float
    overlaps: int
    segments: List[SubtitleSegment]
    
    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization."""
        data = asdict(self)
        data['segments'] = [asdict(seg) for seg in self.segments]
        return data


class YouTubeSubtitleAnalyzer:
    """Analyzer for YouTube video subtitles."""
    
    def __init__(self, output_dir: str = "/tmp/youtube_research"):
        """
        Initialize the analyzer.
        
        Args:
            output_dir: Directory to store downloaded videos and analysis results
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
    def check_dependencies(self) -> bool:
        """Check if required dependencies are installed."""
        try:
            # Check for yt-dlp
            result = subprocess.run(
                ["yt-dlp", "--version"],
                capture_output=True,
                text=True
            )
            if result.returncode != 0:
                print("❌ yt-dlp is not installed")
                print("Install with: pip install yt-dlp")
                return False
                
            # Check for ffmpeg
            result = subprocess.run(
                ["ffmpeg", "-version"],
                capture_output=True,
                text=True
            )
            if result.returncode != 0:
                print("❌ ffmpeg is not installed")
                return False
                
            return True
            
        except FileNotFoundError:
            print("❌ Required dependencies not found")
            print("Install yt-dlp: pip install yt-dlp")
            print("Install ffmpeg: apt-get install ffmpeg (Linux) or brew install ffmpeg (Mac)")
            return False
    
    def extract_video_id(self, url: str) -> Optional[str]:
        """
        Extract video ID from YouTube URL.
        
        Args:
            url: YouTube URL (supports various formats)
            
        Returns:
            Video ID or None if invalid
        """
        patterns = [
            r'(?:youtube\.com\/watch\?v=|youtu\.be\/|youtube\.com\/shorts\/)([a-zA-Z0-9_-]{11})',
            r'youtube\.com\/embed\/([a-zA-Z0-9_-]{11})',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
        
        return None
    
    def download_video_and_subtitles(self, url: str) -> tuple[Optional[str], Optional[str]]:
        """
        Download video and extract subtitles using yt-dlp.
        
        Args:
            url: YouTube video URL
            
        Returns:
            Tuple of (video_path, subtitle_path) or (None, None) on failure
        """
        video_id = self.extract_video_id(url)
        if not video_id:
            print(f"❌ Invalid YouTube URL: {url}")
            return None, None
        
        print(f"📹 Downloading video {video_id}...")
        
        video_path = self.output_dir / f"{video_id}.mp4"
        subtitle_path = self.output_dir / f"{video_id}.srt"
        
        # Download video
        video_cmd = [
            "yt-dlp",
            "-f", "best[ext=mp4]",
            "-o", str(video_path),
            url
        ]
        
        try:
            result = subprocess.run(video_cmd, capture_output=True, text=True, timeout=60)
            if result.returncode != 0:
                print(f"⚠️ Video download failed: {result.stderr}")
                # Continue to try subtitles even if video fails
        except subprocess.TimeoutExpired:
            print("⚠️ Video download timed out")
        
        # Download subtitles
        subtitle_cmd = [
            "yt-dlp",
            "--write-auto-sub",
            "--sub-lang", "en",
            "--sub-format", "srt",
            "--skip-download",
            "-o", str(self.output_dir / video_id),
            url
        ]
        
        try:
            result = subprocess.run(subtitle_cmd, capture_output=True, text=True, timeout=30)
            
            # Check for subtitle file with various naming patterns
            possible_subtitle_files = [
                self.output_dir / f"{video_id}.en.srt",
                self.output_dir / f"{video_id}.srt",
            ]
            
            for sub_file in possible_subtitle_files:
                if sub_file.exists():
                    # Rename to standard name
                    if sub_file != subtitle_path:
                        sub_file.rename(subtitle_path)
                    print(f"✅ Subtitles downloaded to {subtitle_path}")
                    break
            else:
                print("⚠️ No subtitles found for this video")
                subtitle_path = None
                
        except subprocess.TimeoutExpired:
            print("⚠️ Subtitle download timed out")
            subtitle_path = None
        
        return (str(video_path) if video_path.exists() else None, 
                str(subtitle_path) if subtitle_path and subtitle_path.exists() else None)
    
    def parse_srt_time(self, time_str: str) -> float:
        """
        Parse SRT timestamp to seconds.
        
        Args:
            time_str: Timestamp in format HH:MM:SS,mmm
            
        Returns:
            Time in seconds as float
        """
        time_str = time_str.strip().replace(',', '.')
        parts = time_str.split(':')
        hours = int(parts[0])
        minutes = int(parts[1])
        seconds = float(parts[2])
        return hours * 3600 + minutes * 60 + seconds
    
    def parse_srt_file(self, srt_path: str) -> List[SubtitleSegment]:
        """
        Parse SRT subtitle file into segments.
        
        Args:
            srt_path: Path to SRT file
            
        Returns:
            List of SubtitleSegment objects
        """
        segments = []
        
        with open(srt_path, 'r', encoding='utf-8') as f:
            content = f.read().strip()
        
        # Split into blocks (separated by blank lines)
        blocks = re.split(r'\n\s*\n', content)
        
        for block in blocks:
            lines = block.strip().split('\n')
            if len(lines) < 3:
                continue
            
            try:
                # Parse index
                index = int(lines[0])
                
                # Parse timestamps (HH:MM:SS,mmm --> HH:MM:SS,mmm)
                timestamp_match = re.match(
                    r'(\d{2}:\d{2}:\d{2},\d{3})\s*-->\s*(\d{2}:\d{2}:\d{2},\d{3})',
                    lines[1]
                )
                
                if not timestamp_match:
                    continue
                
                start_time = self.parse_srt_time(timestamp_match.group(1))
                end_time = self.parse_srt_time(timestamp_match.group(2))
                duration = end_time - start_time
                
                # Join text lines
                text = ' '.join(lines[2:])
                word_count = len(text.split())
                char_count = len(text)
                
                segment = SubtitleSegment(
                    index=index,
                    start_time=start_time,
                    end_time=end_time,
                    duration=duration,
                    text=text,
                    word_count=word_count,
                    char_count=char_count
                )
                
                segments.append(segment)
                
            except (ValueError, IndexError) as e:
                print(f"⚠️ Could not parse SRT block: {e}")
                continue
        
        return segments
    
    def analyze_subtitles(self, segments: List[SubtitleSegment], 
                         video_id: str, video_url: str) -> SubtitleAnalysis:
        """
        Analyze subtitle segments to extract metrics.
        
        Args:
            segments: List of subtitle segments
            video_id: YouTube video ID
            video_url: YouTube video URL
            
        Returns:
            SubtitleAnalysis object with comprehensive metrics
        """
        if not segments:
            return None
        
        # Calculate basic metrics
        total_segments = len(segments)
        durations = [seg.duration for seg in segments]
        word_counts = [seg.word_count for seg in segments]
        char_counts = [seg.char_count for seg in segments]
        reading_speeds = [seg.words_per_second for seg in segments]
        
        total_duration = segments[-1].end_time - segments[0].start_time
        avg_segment_duration = sum(durations) / len(durations)
        min_segment_duration = min(durations)
        max_segment_duration = max(durations)
        
        avg_words_per_segment = sum(word_counts) / len(word_counts)
        avg_chars_per_segment = sum(char_counts) / len(char_counts)
        avg_reading_speed = sum(reading_speeds) / len(reading_speeds)
        
        # Analyze gaps and overlaps
        total_gaps = 0
        gap_durations = []
        overlaps = 0
        
        for i in range(len(segments) - 1):
            current = segments[i]
            next_seg = segments[i + 1]
            
            gap = next_seg.start_time - current.end_time
            
            if gap > 0.01:  # Gap larger than 10ms
                total_gaps += 1
                gap_durations.append(gap)
            elif gap < -0.01:  # Overlap
                overlaps += 1
        
        avg_gap_duration = sum(gap_durations) / len(gap_durations) if gap_durations else 0
        
        return SubtitleAnalysis(
            video_id=video_id,
            video_url=video_url,
            total_segments=total_segments,
            total_duration=total_duration,
            avg_segment_duration=avg_segment_duration,
            min_segment_duration=min_segment_duration,
            max_segment_duration=max_segment_duration,
            avg_words_per_segment=avg_words_per_segment,
            avg_chars_per_segment=avg_chars_per_segment,
            avg_reading_speed_wps=avg_reading_speed,
            total_gaps=total_gaps,
            avg_gap_duration=avg_gap_duration,
            overlaps=overlaps,
            segments=segments
        )
    
    def generate_report(self, analysis: SubtitleAnalysis, output_path: Optional[str] = None):
        """
        Generate a comprehensive analysis report.
        
        Args:
            analysis: SubtitleAnalysis object
            output_path: Optional path to save report (markdown format)
        """
        report = f"""# YouTube Video Subtitle Analysis Report

## Video Information
- **Video ID**: {analysis.video_id}
- **Video URL**: {analysis.video_url}
- **Analysis Date**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Summary Statistics

### Segment Overview
- **Total Segments**: {analysis.total_segments}
- **Total Duration**: {analysis.total_duration:.2f} seconds
- **Average Segment Duration**: {analysis.avg_segment_duration:.2f} seconds
- **Min Segment Duration**: {analysis.min_segment_duration:.2f} seconds
- **Max Segment Duration**: {analysis.max_segment_duration:.2f} seconds

### Text Metrics
- **Average Words per Segment**: {analysis.avg_words_per_segment:.1f}
- **Average Characters per Segment**: {analysis.avg_chars_per_segment:.1f}
- **Average Reading Speed**: {analysis.avg_reading_speed_wps:.2f} words/second

### Timing Analysis
- **Total Gaps**: {analysis.total_gaps}
- **Average Gap Duration**: {analysis.avg_gap_duration:.3f} seconds
- **Overlapping Segments**: {analysis.overlaps}

## Detailed Segment Breakdown

| Index | Start | End | Duration | Text | Words | Chars | WPS |
|-------|-------|-----|----------|------|-------|-------|-----|
"""
        
        # Add segment details (show first 10 for brevity)
        for seg in analysis.segments[:10]:
            report += f"| {seg.index} | {seg.start_time:.2f}s | {seg.end_time:.2f}s | {seg.duration:.2f}s | {seg.text[:50]}... | {seg.word_count} | {seg.char_count} | {seg.words_per_second:.2f} |\n"
        
        if len(analysis.segments) > 10:
            report += f"\n*...and {len(analysis.segments) - 10} more segments*\n"
        
        report += f"""

## Key Findings

### Subtitle Duration Guidelines
Based on this video's analysis:
- Optimal segment duration: {analysis.avg_segment_duration:.2f} seconds
- Recommended range: {analysis.min_segment_duration:.2f}s - {analysis.max_segment_duration:.2f}s

### Text Length Guidelines
- Words per segment: ~{int(analysis.avg_words_per_segment)} words
- Characters per segment: ~{int(analysis.avg_chars_per_segment)} characters

### Reading Speed
- Average reading speed: {analysis.avg_reading_speed_wps:.2f} words/second
- This corresponds to about {analysis.avg_reading_speed_wps * 60:.0f} words/minute

### Timing Recommendations
- Gap between segments: ~{analysis.avg_gap_duration:.3f} seconds
- Avoid overlapping segments (found {analysis.overlaps} overlaps in this video)

## Application to StoryGenerator Pipeline

### Subtitle Timing Module (`Generators/GTitles.py`)
```python
# Recommended settings based on this analysis
SUBTITLE_CONFIG = {{
    'min_duration': {analysis.min_segment_duration:.2f},
    'max_duration': {analysis.max_segment_duration:.2f},
    'target_duration': {analysis.avg_segment_duration:.2f},
    'max_words_per_segment': {int(analysis.avg_words_per_segment + 5)},
    'max_chars_per_segment': {int(analysis.avg_chars_per_segment + 10)},
    'gap_between_segments': {analysis.avg_gap_duration:.3f},
    'target_reading_speed_wps': {analysis.avg_reading_speed_wps:.2f}
}}
```

### Quality Check Criteria
- ✅ Segment duration between {analysis.min_segment_duration:.2f}s and {analysis.max_segment_duration:.2f}s
- ✅ Reading speed around {analysis.avg_reading_speed_wps:.2f} words/second
- ✅ No overlapping segments
- ✅ Consistent gaps between segments (~{analysis.avg_gap_duration:.3f}s)

"""
        
        print(report)
        
        if output_path:
            output_file = Path(output_path)
            output_file.write_text(report)
            print(f"\n✅ Report saved to {output_path}")
        
        # Also save JSON data
        json_path = self.output_dir / f"{analysis.video_id}_analysis.json"
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(analysis.to_dict(), f, indent=2)
        print(f"✅ JSON data saved to {json_path}")
    
    def analyze_video(self, url: str) -> Optional[SubtitleAnalysis]:
        """
        Complete analysis pipeline for a YouTube video.
        
        Args:
            url: YouTube video URL
            
        Returns:
            SubtitleAnalysis object or None on failure
        """
        print(f"\n🔬 Starting YouTube Subtitle Analysis")
        print(f"📺 URL: {url}\n")
        
        # Check dependencies
        if not self.check_dependencies():
            return None
        
        # Extract video ID
        video_id = self.extract_video_id(url)
        if not video_id:
            print("❌ Could not extract video ID from URL")
            return None
        
        # Download video and subtitles
        video_path, subtitle_path = self.download_video_and_subtitles(url)
        
        if not subtitle_path:
            print("❌ Could not retrieve subtitles for analysis")
            return None
        
        print(f"\n📊 Parsing subtitles...")
        
        # Parse subtitles
        segments = self.parse_srt_file(subtitle_path)
        
        if not segments:
            print("❌ No subtitle segments found")
            return None
        
        print(f"✅ Parsed {len(segments)} subtitle segments\n")
        
        # Analyze subtitles
        analysis = self.analyze_subtitles(segments, video_id, url)
        
        # Generate report
        report_path = self.output_dir / f"{video_id}_report.md"
        self.generate_report(analysis, str(report_path))
        
        return analysis


def main():
    """Main entry point for the script."""
    if len(sys.argv) < 2:
        print("Usage: python youtube_subtitle_analyzer.py <youtube_url>")
        print("Example: python youtube_subtitle_analyzer.py https://www.youtube.com/shorts/41QD8C6tqIU")
        sys.exit(1)
    
    url = sys.argv[1]
    
    analyzer = YouTubeSubtitleAnalyzer()
    analysis = analyzer.analyze_video(url)
    
    if analysis:
        print("\n✅ Analysis complete!")
        print(f"📁 Results saved to {analyzer.output_dir}")
    else:
        print("\n❌ Analysis failed")
        sys.exit(1)


if __name__ == "__main__":
    main()
