import os
import json
from typing import List, Dict, Any
from dataclasses import dataclass, asdict
from Models.StoryIdea import StoryIdea
from Tools.Utils import TITLES_PATH, sanitize_filename, SUBTITLESWBW_NAME


@dataclass
class Scene:
    """Represents a scene segment with timing and description"""
    scene_id: int
    start_time: float
    end_time: float
    duration: float
    text: str
    description: str = ""
    emotion: str = "neutral"
    intensity: float = 0.5
    keyframes: List[str] = None

    def __post_init__(self):
        if self.keyframes is None:
            self.keyframes = []

    def to_dict(self):
        return asdict(self)


class SceneAnalyzer:
    """
    Analyzes subtitle timing to create scene segments with descriptions.
    Segments stories into natural narrative beats for visual generation.
    """

    def __init__(self, min_scene_duration: float = 3.0, max_scene_duration: float = 15.0):
        """
        Args:
            min_scene_duration: Minimum scene length in seconds
            max_scene_duration: Maximum scene length in seconds
        """
        self.min_scene_duration = min_scene_duration
        self.max_scene_duration = max_scene_duration

    def parse_srt(self, srt_path: str) -> List[Dict[str, Any]]:
        """Parse SRT file into structured subtitle data"""
        with open(srt_path, 'r', encoding='utf-8') as f:
            content = f.read()

        subtitles = []
        blocks = content.strip().split('\n\n')

        for block in blocks:
            lines = block.strip().split('\n')
            if len(lines) < 3:
                continue

            try:
                # Parse timing line: "00:00:01,234 --> 00:00:02,345"
                timing = lines[1].split(' --> ')
                start = self._parse_timestamp(timing[0])
                end = self._parse_timestamp(timing[1])
                text = ' '.join(lines[2:])

                subtitles.append({
                    'start': start,
                    'end': end,
                    'text': text
                })
            except (IndexError, ValueError) as e:
                print(f"⚠️ Warning: Could not parse subtitle block: {e}")
                continue

        return subtitles

    def _parse_timestamp(self, timestamp: str) -> float:
        """Convert SRT timestamp to seconds"""
        # Format: "00:01:23,456"
        time_part, ms = timestamp.split(',')
        h, m, s = map(int, time_part.split(':'))
        return h * 3600 + m * 60 + s + int(ms) / 1000

    def analyze_story(self, story_idea: StoryIdea) -> List[Scene]:
        """
        Analyze a story's subtitles and create scene segments
        
        Args:
            story_idea: StoryIdea object for the story
            
        Returns:
            List of Scene objects with timing and descriptions
        """
        folder_path = os.path.join(TITLES_PATH, sanitize_filename(story_idea.story_title))
        srt_path = os.path.join(folder_path, SUBTITLESWBW_NAME)
        script_path = os.path.join(folder_path, "Revised.txt")

        if not os.path.exists(srt_path):
            raise FileNotFoundError(f"Subtitle file not found: {srt_path}")

        if not os.path.exists(script_path):
            raise FileNotFoundError(f"Script file not found: {script_path}")

        # Load subtitles and script
        subtitles = self.parse_srt(srt_path)
        with open(script_path, 'r', encoding='utf-8') as f:
            script_text = f.read()

        # Create scenes based on natural pauses and content
        scenes = self._segment_into_scenes(subtitles, script_text)

        # Save scenes to file
        self._save_scenes(scenes, folder_path)

        print(f"✅ Created {len(scenes)} scenes for '{story_idea.story_title}'")
        return scenes

    def _segment_into_scenes(self, subtitles: List[Dict], script_text: str) -> List[Scene]:
        """
        Segment subtitles into logical scenes based on timing and content
        
        Strategy:
        1. Look for natural pauses (gaps > 0.5s between words)
        2. Respect min/max duration constraints
        3. Try to break at sentence/phrase boundaries
        """
        scenes = []
        current_scene_words = []
        current_scene_start = None
        scene_id = 1

        for i, subtitle in enumerate(subtitles):
            if current_scene_start is None:
                current_scene_start = subtitle['start']

            current_scene_words.append(subtitle['text'])
            current_duration = subtitle['end'] - current_scene_start

            # Check if we should end this scene
            should_end = False

            # Force break if max duration reached
            if current_duration >= self.max_scene_duration:
                should_end = True

            # Natural break if min duration met and there's a pause
            elif current_duration >= self.min_scene_duration:
                # Check for pause after this word
                if i < len(subtitles) - 1:
                    gap = subtitles[i + 1]['start'] - subtitle['end']
                    if gap > 0.5:  # 500ms pause
                        should_end = True

            # Last subtitle
            if i == len(subtitles) - 1:
                should_end = True

            if should_end and current_scene_words:
                scene_text = ' '.join(current_scene_words)
                scenes.append(Scene(
                    scene_id=scene_id,
                    start_time=current_scene_start,
                    end_time=subtitle['end'],
                    duration=subtitle['end'] - current_scene_start,
                    text=scene_text,
                    description="",  # Will be filled by GPT
                    emotion="neutral",
                    intensity=0.5
                ))
                scene_id += 1
                current_scene_words = []
                current_scene_start = None

        return scenes

    def _save_scenes(self, scenes: List[Scene], folder_path: str):
        """Save scene analysis to JSON file"""
        scenes_file = os.path.join(folder_path, "scenes.json")
        scenes_data = [scene.to_dict() for scene in scenes]

        with open(scenes_file, 'w', encoding='utf-8') as f:
            json.dump(scenes_data, f, indent=2, ensure_ascii=False)

        print(f"💾 Saved scene analysis to: {scenes_file}")

    def load_scenes(self, story_idea: StoryIdea) -> List[Scene]:
        """Load previously analyzed scenes from file"""
        folder_path = os.path.join(TITLES_PATH, sanitize_filename(story_idea.story_title))
        scenes_file = os.path.join(folder_path, "scenes.json")

        if not os.path.exists(scenes_file):
            raise FileNotFoundError(f"Scenes file not found: {scenes_file}")

        with open(scenes_file, 'r', encoding='utf-8') as f:
            scenes_data = json.load(f)

        return [Scene(**scene_data) for scene_data in scenes_data]
