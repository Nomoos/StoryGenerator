"""
SRT subtitle tools for building, merging, and manipulating subtitle files.
Research prototype for subtitle processing and synchronization.
"""

import re
from typing import List, Dict, Optional
from pathlib import Path
from dataclasses import dataclass
import json


@dataclass
class SubtitleEntry:
    """Represents a single subtitle entry."""
    index: int
    start_time: float  # in seconds
    end_time: float    # in seconds
    text: str
    
    def to_srt_timestamp(self, seconds: float) -> str:
        """Convert seconds to SRT timestamp format (HH:MM:SS,mmm)."""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        millis = int((seconds % 1) * 1000)
        return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"
    
    def to_srt_block(self) -> str:
        """Convert to SRT format block."""
        start = self.to_srt_timestamp(self.start_time)
        end = self.to_srt_timestamp(self.end_time)
        return f"{self.index}\n{start} --> {end}\n{self.text}\n"
    
    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            "index": self.index,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "text": self.text,
            "duration": self.end_time - self.start_time
        }


class SRTTools:
    """
    Tools for working with SRT subtitle files.
    
    This is a research prototype demonstrating how to:
    - Parse SRT files
    - Build SRT from timing data
    - Merge multiple SRT files
    - Adjust timing and synchronization
    - Convert between SRT and JSON formats
    """
    
    @staticmethod
    def parse_srt(srt_path: str) -> List[SubtitleEntry]:
        """
        Parse an SRT file into subtitle entries.
        
        Args:
            srt_path: Path to SRT file
            
        Returns:
            List of SubtitleEntry objects
        """
        content = Path(srt_path).read_text(encoding="utf-8")
        entries = []
        
        # Split into blocks (separated by blank lines)
        blocks = re.split(r'\n\s*\n', content.strip())
        
        for block in blocks:
            if not block.strip():
                continue
            
            lines = block.strip().split('\n')
            if len(lines) < 3:
                continue
            
            try:
                # Parse index
                index = int(lines[0])
                
                # Parse timestamps
                timestamp_line = lines[1]
                match = re.match(
                    r'(\d{2}):(\d{2}):(\d{2}),(\d{3})\s*-->\s*(\d{2}):(\d{2}):(\d{2}),(\d{3})',
                    timestamp_line
                )
                if not match:
                    continue
                
                # Convert to seconds
                start_h, start_m, start_s, start_ms = map(int, match.groups()[:4])
                end_h, end_m, end_s, end_ms = map(int, match.groups()[4:])
                
                start_time = start_h * 3600 + start_m * 60 + start_s + start_ms / 1000
                end_time = end_h * 3600 + end_m * 60 + end_s + end_ms / 1000
                
                # Get text (may span multiple lines)
                text = '\n'.join(lines[2:])
                
                entries.append(SubtitleEntry(
                    index=index,
                    start_time=start_time,
                    end_time=end_time,
                    text=text
                ))
            except (ValueError, IndexError):
                continue
        
        return entries
    
    @staticmethod
    def build_srt(
        entries: List[SubtitleEntry],
        output_path: Optional[str] = None
    ) -> str:
        """
        Build SRT content from subtitle entries.
        
        Args:
            entries: List of SubtitleEntry objects
            output_path: Optional path to save SRT file
            
        Returns:
            SRT content as string
        """
        srt_blocks = []
        for entry in entries:
            srt_blocks.append(entry.to_srt_block())
        
        srt_content = "\n".join(srt_blocks)
        
        if output_path:
            Path(output_path).write_text(srt_content, encoding="utf-8")
        
        return srt_content
    
    @staticmethod
    def merge_srt_files(
        srt_paths: List[str],
        output_path: str,
        time_offsets: Optional[List[float]] = None
    ) -> str:
        """
        Merge multiple SRT files into one.
        
        Args:
            srt_paths: List of SRT file paths to merge
            output_path: Path to save merged SRT
            time_offsets: Optional list of time offsets (in seconds) for each file
            
        Returns:
            Merged SRT content
        """
        if time_offsets is None:
            time_offsets = [0.0] * len(srt_paths)
        
        all_entries = []
        
        for srt_path, offset in zip(srt_paths, time_offsets):
            entries = SRTTools.parse_srt(srt_path)
            
            # Apply time offset
            for entry in entries:
                entry.start_time += offset
                entry.end_time += offset
                all_entries.append(entry)
        
        # Sort by start time
        all_entries.sort(key=lambda e: e.start_time)
        
        # Reindex
        for i, entry in enumerate(all_entries, 1):
            entry.index = i
        
        return SRTTools.build_srt(all_entries, output_path)
    
    @staticmethod
    def adjust_timing(
        srt_path: str,
        output_path: str,
        offset: float = 0.0,
        speed_factor: float = 1.0
    ) -> str:
        """
        Adjust timing of all subtitles.
        
        Args:
            srt_path: Input SRT file
            output_path: Output SRT file
            offset: Time offset in seconds (positive = delay, negative = advance)
            speed_factor: Speed multiplier (1.0 = normal, 2.0 = double speed)
            
        Returns:
            Adjusted SRT content
        """
        entries = SRTTools.parse_srt(srt_path)
        
        for entry in entries:
            # Apply speed factor (relative to start of subtitle)
            entry.start_time = entry.start_time * speed_factor
            entry.end_time = entry.end_time * speed_factor
            
            # Apply offset
            entry.start_time += offset
            entry.end_time += offset
        
        return SRTTools.build_srt(entries, output_path)
    
    @staticmethod
    def srt_to_json(srt_path: str, output_path: Optional[str] = None) -> str:
        """
        Convert SRT file to JSON format.
        
        Args:
            srt_path: Input SRT file
            output_path: Optional output JSON file path
            
        Returns:
            JSON string
        """
        entries = SRTTools.parse_srt(srt_path)
        data = {
            "subtitles": [entry.to_dict() for entry in entries],
            "total_entries": len(entries),
            "duration": entries[-1].end_time if entries else 0
        }
        
        json_str = json.dumps(data, indent=2, ensure_ascii=False)
        
        if output_path:
            Path(output_path).write_text(json_str, encoding="utf-8")
        
        return json_str
    
    @staticmethod
    def json_to_srt(json_path: str, output_path: Optional[str] = None) -> str:
        """
        Convert JSON format to SRT file.
        
        Args:
            json_path: Input JSON file
            output_path: Optional output SRT file path
            
        Returns:
            SRT content
        """
        data = json.loads(Path(json_path).read_text(encoding="utf-8"))
        
        entries = []
        for item in data["subtitles"]:
            entries.append(SubtitleEntry(
                index=item["index"],
                start_time=item["start_time"],
                end_time=item["end_time"],
                text=item["text"]
            ))
        
        return SRTTools.build_srt(entries, output_path)
    
    @staticmethod
    def filter_by_time(
        srt_path: str,
        start_time: float,
        end_time: float,
        output_path: Optional[str] = None
    ) -> str:
        """
        Extract subtitles within a time range.
        
        Args:
            srt_path: Input SRT file
            start_time: Start time in seconds
            end_time: End time in seconds
            output_path: Optional output SRT file path
            
        Returns:
            Filtered SRT content
        """
        entries = SRTTools.parse_srt(srt_path)
        
        filtered = []
        for entry in entries:
            # Keep entries that overlap with the time range
            if entry.end_time >= start_time and entry.start_time <= end_time:
                # Adjust timing relative to start_time
                new_entry = SubtitleEntry(
                    index=len(filtered) + 1,
                    start_time=max(0, entry.start_time - start_time),
                    end_time=entry.end_time - start_time,
                    text=entry.text
                )
                filtered.append(new_entry)
        
        return SRTTools.build_srt(filtered, output_path)
    
    @staticmethod
    def get_statistics(srt_path: str) -> Dict:
        """
        Get statistics about an SRT file.
        
        Args:
            srt_path: Path to SRT file
            
        Returns:
            Dictionary with statistics
        """
        entries = SRTTools.parse_srt(srt_path)
        
        if not entries:
            return {
                "total_entries": 0,
                "total_duration": 0,
                "avg_duration": 0,
                "total_words": 0,
                "avg_words_per_entry": 0
            }
        
        durations = [e.end_time - e.start_time for e in entries]
        word_counts = [len(e.text.split()) for e in entries]
        
        return {
            "total_entries": len(entries),
            "total_duration": entries[-1].end_time,
            "avg_duration": sum(durations) / len(durations),
            "min_duration": min(durations),
            "max_duration": max(durations),
            "total_words": sum(word_counts),
            "avg_words_per_entry": sum(word_counts) / len(word_counts),
            "first_entry_time": entries[0].start_time,
            "last_entry_time": entries[-1].end_time
        }


# Example usage
if __name__ == "__main__":
    # Parse existing SRT
    entries = SRTTools.parse_srt("input.srt")
    print(f"Parsed {len(entries)} subtitle entries")
    
    # Build new SRT
    new_entries = [
        SubtitleEntry(1, 0.0, 2.5, "Hello, world!"),
        SubtitleEntry(2, 2.5, 5.0, "This is a test subtitle."),
        SubtitleEntry(3, 5.5, 8.0, "Research prototype demo.")
    ]
    SRTTools.build_srt(new_entries, "output.srt")
    
    # Convert to JSON
    SRTTools.srt_to_json("input.srt", "subtitles.json")
    
    # Merge multiple SRT files
    SRTTools.merge_srt_files(
        ["part1.srt", "part2.srt"],
        "merged.srt",
        time_offsets=[0.0, 30.0]  # Second file starts at 30s
    )
    
    # Get statistics
    stats = SRTTools.get_statistics("input.srt")
    print(f"\nSRT Statistics:")
    print(f"  Total entries: {stats['total_entries']}")
    print(f"  Total duration: {stats['total_duration']:.2f}s")
    print(f"  Avg words per entry: {stats['avg_words_per_entry']:.1f}")
