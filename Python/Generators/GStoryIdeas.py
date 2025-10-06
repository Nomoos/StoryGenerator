import openai
import json
from typing import List, Optional
from Models.StoryIdea import StoryIdea

openai.api_key = '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'

class StoryIdeasGenerator:
    def __init__(self, model: str = "gpt-4o-mini"):
        self.model = model

    def generate_ideas(
        self,
        topic: str,
        count: int = 5,
        tone: Optional[str] = None,
        theme: Optional[str] = None
    ) -> List[StoryIdea]:
        prompt = self._build_prompt(topic, count, tone, theme)

        try:
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.9
            )
        except Exception as e:
            raise RuntimeError(f"Failed to generate ideas: {e}")

        reply = response.choices[0].message['content']

        try:
            cleaned = reply.strip().strip('```json').strip('```').strip()
            ideas_data = json.loads(cleaned)
        except json.JSONDecodeError:
            raise ValueError(f"Invalid JSON from ChatGPT:\n{reply}")

        if not isinstance(ideas_data, list):
            raise ValueError("Expected a JSON array (list of story ideas).")

        valid_ideas = []
        for item in ideas_data:
            if isinstance(item, dict) and 'story_title' in item:
                idea = StoryIdea(**item)
                idea.to_file()  # ✅ delegate saving to the model itself
                valid_ideas.append(idea)
            else:
                raise ValueError(f"Invalid idea format: {item}")

        return valid_ideas

    def _build_prompt(self, topic: str, count: int, tone: Optional[str], theme: Optional[str]) -> str:
        prompt = f"""
You are a viral story idea generator for short vertical video scripts (TikTok, Reels, Shorts).

Your task is to generate exactly {count} unique, dramatic story ideas inspired by this topic: "{topic}".

Each idea must be a JSON object with the following structure:

- story_title: string (REQUIRED)  
  – should be longer than a short phrase (ideally 70–100 characters)  
  – must follow YouTube title standards: emotionally engaging, curiosity-driven, yet clear and natural  
  – avoid clickbait, all caps, emojis, or excessive punctuation
- tone: string (optional)
- theme: string (optional)
- narrator_type: string (optional)
- narrator_gender: string (REQUIRED, male or female)
- other_character: string (optional)
- outcome: string (optional)
- emotional_core: string (optional)
- power_dynamic: string (optional)
- timeline: string (optional)
- twist_type: string (optional)
- character_arc: string (optional)
- voice_style: string (optional)
- target_moral: string (optional)
- locations: string (optional)
- mentioned_brands: string (optional)
- goal: string (optional)
- potencial: object (REQUIRED) – pessimistic virality estimate with the following structure:

   "potencial": {{
            "platforms": {{
              "youtube": integer (0–100),
              "tiktok": integer (0–100),
              "instagram": integer (0–100)
            }},
            "regions": {{
              "US": integer (0–100),
              "AU": integer (0–100),
              "GB": integer (0–100)
            }},
            "age_groups": {{
              "10_15": integer (0–100),
              "15_20": integer (0–100),
              "20_25": integer (0–100),
              "25_30": integer (0–100),
              "30_50": integer (0–100),
              "50_70": integer (0–100)
            }},
            "gender": {{
              "man": integer (0–100),
              "woman": integer (0–100)
            }}
          }}

All numbers represent pessimistic estimates of how viral the idea could be in that segment.

Respond with a JSON array containing exactly {count} story idea objects, and nothing else. Do not explain the list.

Optional context:
Tone: {tone or "any"}
Theme: {theme or "any"}
""".strip()
        return prompt
