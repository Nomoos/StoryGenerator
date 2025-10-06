import json
import os
from typing import Optional, Dict, Any
from Tools.Utils import sanitize_filename, IDEAS_PATH


class StoryIdea:
    def __init__(
        self,
        story_title: str,
        narrator_gender: str,
        tone: Optional[str] = None,
        theme: Optional[str] = None,
        narrator_type: Optional[str] = None,
        other_character: Optional[str] = None,
        outcome: Optional[str] = None,
        emotional_core: Optional[str] = None,
        power_dynamic: Optional[str] = None,
        timeline: Optional[str] = None,
        twist_type: Optional[str] = None,
        character_arc: Optional[str] = None,
        voice_style: Optional[str] = None,
        target_moral: Optional[str] = None,
        locations: Optional[str] = None,
        mentioned_brands: Optional[str] = None,
        goal: Optional[str] = None,
        potencial: Optional[Dict[str, Any]] = None
    ):
        self.story_title = story_title
        self.narrator_gender = narrator_gender
        self.tone = tone
        self.theme = theme
        self.narrator_type = narrator_type
        self.other_character = other_character
        self.outcome = outcome
        self.emotional_core = emotional_core
        self.power_dynamic = power_dynamic
        self.timeline = timeline
        self.twist_type = twist_type
        self.character_arc = character_arc
        self.voice_style = voice_style
        self.target_moral = target_moral
        self.locations = locations
        self.mentioned_brands = mentioned_brands
        self.goal = goal

        # Default potencial structure
        self.potencial = {
            "platforms": {
                "youtube": 0,
                "tiktok": 0,
                "instagram": 0,
            },
            "regions": {
                "US": 0,
                "AU": 0,
                "GB": 0,
            },
            "age_groups": {
                "10_15": 0,
                "15_20": 0,
                "20_25": 0,
                "25_30": 0,
                "30_50": 0,
                "50_70": 0
            },
            "gender": {
                "woman": 0,
                "man": 0
            }
        }

        # Merge provided potencial if present
        if potencial:
            for category in self.potencial:
                if category in potencial and isinstance(potencial[category], dict):
                    for key in self.potencial[category]:
                        self.potencial[category][key] = int(potencial[category].get(key, 0))

        # Compute overall score
        self.potencial["overall"] = self.calculate_overall_potencial()

    def calculate_overall_potencial(self) -> int:
        scores = [
            self.potencial["age_groups"].get("10_15", 0),
            self.potencial["age_groups"].get("15_20", 0),
            self.potencial["regions"].get("US", 0),
            self.potencial["platforms"].get("youtube", 0),
            self.potencial["platforms"].get("woman", 0)
        ]
        return round(sum(scores) / len(scores)) if scores else 0

    @classmethod
    def from_file(cls, filepath: str) -> "StoryIdea":
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return cls(**data)

    def to_dict(self) -> Dict[str, Any]:
        return self.__dict__

    def to_file(self):
        os.makedirs(IDEAS_PATH, exist_ok=True)
        filename = sanitize_filename(self.story_title) + ".json"
        full_path = os.path.join(IDEAS_PATH, filename)
        with open(full_path, 'w', encoding='utf-8') as f:
            json.dump(self.to_dict(), f, indent=2, ensure_ascii=False)
        print(f"Story saved to: {full_path}")

    def __repr__(self):
        overall = self.potencial.get("overall", 0)
        return f"StoryIdea(story_title={self.story_title!r}, overall_potencial={overall})"
