"""
Scene Planning Module - Beat Sheets, Shot Lists, and Draft Subtitles

This module provides functionality for breaking scripts into scenes, shots, and
generating draft subtitle timing for video production.
"""

import re
import json
from dataclasses import dataclass, field, asdict
from typing import List, Dict, Optional
from datetime import datetime
from pathlib import Path


@dataclass
class Shot:
    """Represents a single shot in a video scene."""
    shot_number: int
    start_time: float
    end_time: float
    duration: float
    scene_description: str
    visual_prompt: str
    narration: str
    
    def to_dict(self) -> Dict:
        """Convert shot to dictionary."""
        return {
            'shotNumber': self.shot_number,
            'startTime': self.start_time,
            'endTime': self.end_time,
            'duration': self.duration,
            'sceneDescription': self.scene_description,
            'visualPrompt': self.visual_prompt,
            'narration': self.narration
        }


@dataclass
class BeatSheet:
    """Represents a story beat sheet with timing and shots."""
    title_id: str
    total_duration: float
    total_shots: int
    generated_at: str
    shots: List[Shot] = field(default_factory=list)
    
    def to_dict(self) -> Dict:
        """Convert beat sheet to dictionary."""
        return {
            'titleId': self.title_id,
            'totalDuration': self.total_duration,
            'totalShots': self.total_shots,
            'generatedAt': self.generated_at,
            'shots': [shot.to_dict() for shot in self.shots]
        }
    
    def to_json(self, indent: int = 2) -> str:
        """Convert beat sheet to JSON string."""
        return json.dumps(self.to_dict(), indent=indent)


@dataclass
class SubtitleEntry:
    """Represents a single subtitle entry in SRT format."""
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
        """Convert subtitle entry to SRT format block."""
        start = self.to_srt_timestamp(self.start_time)
        end = self.to_srt_timestamp(self.end_time)
        return f"{self.index}\n{start} --> {end}\n{self.text}\n"


class ScenePlanner:
    """
    Generates beat sheets, shot lists, and draft subtitles from scripts.
    """
    
    AVERAGE_WORDS_PER_MINUTE = 150
    MAX_CHARS_PER_SUBTITLE = 42
    
    def __init__(self, output_root: str = "./Generator"):
        """
        Initialize scene planner.
        
        Args:
            output_root: Root directory for output files
        """
        self.output_root = Path(output_root)
    
    def split_into_sentences(self, text: str) -> List[str]:
        """
        Split text into sentences using simple rules.
        
        Args:
            text: Text to split
            
        Returns:
            List of sentences
        """
        # Simple sentence splitting on . ! ?
        sentences = re.split(r'[.!?]+', text)
        # Clean up and filter empty
        sentences = [s.strip() for s in sentences if s.strip()]
        return sentences
    
    def estimate_duration(self, text: str, total_duration: Optional[float] = None) -> float:
        """
        Estimate duration of text based on word count.
        
        Args:
            text: Text to estimate duration for
            total_duration: Optional total duration to scale to
            
        Returns:
            Estimated duration in seconds
        """
        word_count = len(text.split())
        duration = (word_count / self.AVERAGE_WORDS_PER_MINUTE) * 60
        return duration
    
    def generate_beat_sheet(
        self,
        script_text: str,
        title_id: str,
        total_duration: float,
        shots_per_minute: float = 5.0
    ) -> BeatSheet:
        """
        Generate a beat sheet from script text.
        
        Args:
            script_text: The script text
            title_id: Unique identifier for the title
            total_duration: Total duration of audio in seconds
            shots_per_minute: Target number of shots per minute
            
        Returns:
            BeatSheet object
        """
        sentences = self.split_into_sentences(script_text)
        
        # Calculate target number of shots
        target_shots = max(3, int((total_duration / 60) * shots_per_minute))
        
        # Group sentences into shots
        sentences_per_shot = max(1, len(sentences) // target_shots)
        shots = []
        
        current_time = 0.0
        shot_number = 1
        
        for i in range(0, len(sentences), sentences_per_shot):
            shot_sentences = sentences[i:i + sentences_per_shot]
            narration = '. '.join(shot_sentences) + '.'
            
            # Estimate shot duration
            shot_duration = self.estimate_duration(narration)
            
            # Scale to fit total duration
            if shots:
                # Distribute remaining time
                remaining_shots = target_shots - len(shots)
                remaining_time = total_duration - current_time
                shot_duration = min(shot_duration, remaining_time / max(1, remaining_shots))
            
            # Create visual prompt (simple version)
            visual_prompt = self._generate_visual_prompt(narration)
            
            shot = Shot(
                shot_number=shot_number,
                start_time=round(current_time, 2),
                end_time=round(current_time + shot_duration, 2),
                duration=round(shot_duration, 2),
                scene_description=narration[:100] + "..." if len(narration) > 100 else narration,
                visual_prompt=visual_prompt,
                narration=narration
            )
            
            shots.append(shot)
            current_time += shot_duration
            shot_number += 1
        
        # Adjust last shot to match total duration
        if shots:
            shots[-1].end_time = round(total_duration, 2)
            shots[-1].duration = round(shots[-1].end_time - shots[-1].start_time, 2)
        
        return BeatSheet(
            title_id=title_id,
            total_duration=total_duration,
            total_shots=len(shots),
            generated_at=datetime.now().astimezone().isoformat(),
            shots=shots
        )
    
    def _generate_visual_prompt(self, text: str) -> str:
        """
        Generate a simple visual prompt from text.
        
        Args:
            text: Narration text
            
        Returns:
            Visual prompt string
        """
        # Simple implementation - extract key words
        # In production, this could use NLP or LLM
        words = text.split()[:20]
        return ' '.join(words) + "..."
    
    def generate_draft_subtitles(
        self,
        script_text: str,
        total_duration: Optional[float] = None,
        max_chars: int = 42
    ) -> List[SubtitleEntry]:
        """
        Generate draft subtitle entries from script text.
        
        Args:
            script_text: The script text
            total_duration: Optional total duration for timing accuracy
            max_chars: Maximum characters per subtitle line
            
        Returns:
            List of SubtitleEntry objects
        """
        sentences = self.split_into_sentences(script_text)
        
        # Split long sentences into subtitle chunks
        subtitle_chunks = []
        for sentence in sentences:
            if len(sentence) <= max_chars:
                subtitle_chunks.append(sentence)
            else:
                # Split by words to fit max_chars
                words = sentence.split()
                current_chunk = []
                for word in words:
                    test_chunk = ' '.join(current_chunk + [word])
                    if len(test_chunk) <= max_chars:
                        current_chunk.append(word)
                    else:
                        if current_chunk:
                            subtitle_chunks.append(' '.join(current_chunk))
                        current_chunk = [word]
                if current_chunk:
                    subtitle_chunks.append(' '.join(current_chunk))
        
        # Generate timing for each chunk
        if total_duration:
            # Use provided duration
            total_words = sum(len(chunk.split()) for chunk in subtitle_chunks)
            time_per_word = total_duration / max(1, total_words)
        else:
            # Use average speaking rate
            time_per_word = 60 / self.AVERAGE_WORDS_PER_MINUTE
        
        subtitles = []
        current_time = 0.0
        
        for idx, chunk in enumerate(subtitle_chunks, start=1):
            word_count = len(chunk.split())
            duration = word_count * time_per_word
            
            subtitle = SubtitleEntry(
                index=idx,
                start_time=round(current_time, 3),
                end_time=round(current_time + duration, 3),
                text=chunk
            )
            subtitles.append(subtitle)
            current_time += duration
        
        return subtitles
    
    def save_beat_sheet(
        self,
        beat_sheet: BeatSheet,
        gender: str,
        age: str
    ) -> Path:
        """
        Save beat sheet to JSON file.
        
        Args:
            beat_sheet: BeatSheet object to save
            gender: Gender segment (e.g., 'men', 'women')
            age: Age range (e.g., '18-24')
            
        Returns:
            Path to saved file
        """
        output_dir = self.output_root / "scenes" / "json" / gender / age
        output_dir.mkdir(parents=True, exist_ok=True)
        
        output_path = output_dir / f"{beat_sheet.title_id}_shots.json"
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(beat_sheet.to_json())
        
        return output_path
    
    def save_draft_subtitles(
        self,
        subtitles: List[SubtitleEntry],
        title_id: str,
        gender: str,
        age: str
    ) -> Path:
        """
        Save draft subtitles to SRT file.
        
        Args:
            subtitles: List of SubtitleEntry objects
            title_id: Unique identifier for the title
            gender: Gender segment (e.g., 'men', 'women')
            age: Age range (e.g., '18-24')
            
        Returns:
            Path to saved file
        """
        output_dir = self.output_root / "subtitles" / "srt" / gender / age
        output_dir.mkdir(parents=True, exist_ok=True)
        
        output_path = output_dir / f"{title_id}_draft.srt"
        
        srt_content = '\n'.join(sub.to_srt_block() for sub in subtitles)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(srt_content)
        
        return output_path
    
    def generate_scene_plan(
        self,
        script_text: str,
        title_id: str,
        gender: str,
        age: str,
        total_duration: float
    ) -> Dict[str, Path]:
        """
        Generate complete scene plan (beat sheet + draft subtitles).
        
        Args:
            script_text: The script text
            title_id: Unique identifier for the title
            gender: Gender segment
            age: Age range
            total_duration: Total duration of audio in seconds
            
        Returns:
            Dictionary with paths to generated files
        """
        # Generate beat sheet
        beat_sheet = self.generate_beat_sheet(script_text, title_id, total_duration)
        beat_sheet_path = self.save_beat_sheet(beat_sheet, gender, age)
        
        # Generate draft subtitles
        subtitles = self.generate_draft_subtitles(script_text, total_duration)
        subtitles_path = self.save_draft_subtitles(subtitles, title_id, gender, age)
        
        return {
            'beat_sheet': beat_sheet_path,
            'subtitles': subtitles_path
        }
