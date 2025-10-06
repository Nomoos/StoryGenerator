import shutil

import openai
import os
from Models.StoryIdea import StoryIdea
from Tools.Utils import sanitize_filename, SCRIPTS_PATH, IDEAS_PATH

openai.api_key = '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'

class ScriptGenerator:
    def __init__(self, model="gpt-4o-mini"):
        self.model = model

    def _build_user_prompt(self, storyIdea: StoryIdea) -> str:
        narrator_type = storyIdea.narrator_type or "first-person"
        prompt = f'Write a {narrator_type} voiceover story for a vertical video titled: “{storyIdea.story_title}”\n\n'

        # Optional goal
        if storyIdea.goal:
            prompt += f"Goal: {storyIdea.goal}\n\n"

        # Append available fields
        for label, value in {
            "Style and Tone": storyIdea.tone,
            "Theme": storyIdea.theme,
            "Narrator Type": storyIdea.narrator_type,
            "Narrator Gender": storyIdea.narrator_gender,
            "Other Main Character": storyIdea.other_character,
            "Key Plot Outcome": storyIdea.outcome,
            "Emotional Core": storyIdea.emotional_core,
            "Power Dynamic": storyIdea.power_dynamic,
            "Timeline": storyIdea.timeline,
            "Twist Type": storyIdea.twist_type,
            "Character Arc": storyIdea.character_arc,
            "Voice Style": storyIdea.voice_style,
            "Target Moral or Theme": storyIdea.target_moral,
            "Locations": storyIdea.locations,
            "Mentioned Brands": storyIdea.mentioned_brands
        }.items():
            if value:
                prompt += f"{label}: {value}\n"

        # Add script generation instructions
        prompt += """
            Script Requirements:
            1. Hook the viewer in the first 1–2 lines — something emotional, weird, or intriguing.
            2. Follow a simple structure: setup → rising tension/emotion → twist/reveal → emotional payoff.
            3. Keep the story around ~360 words. A slight overflow is okay if it helps with emotional payoff.
            4. Use spoken, conversational English — short, vivid sentences with natural rhythm.
            5. Use **clear, easy-to-understand language** — avoid abbreviations, decade references like "’00s", technical terms, or anything that might sound awkward or confusing when read aloud.
            6. Do not use any voice tags or technical formatting. Just the raw, natural storytelling.
            7. Output only the final voiceover narration — no explanations, labels, or instructions.
            
            Audience: Viewers aged 10–30 in the US, Canada, and Australia who binge emotional or dramatic vertical stories on TikTok, YouTube Shorts, and Instagram Reels.
            
            Final Output: The complete spoken narration, natural and clean. Just text — nothing else.
            """.strip()
        return prompt

    def _build_system_prompt(self, storyIdea: StoryIdea) -> str:
        narrator_type = storyIdea.narrator_type or "first-person"
        voice_note = f'Use a voice style that feels "{storyIdea.voice_style}".' if storyIdea.voice_style else ""
        tone_note = ""

        if storyIdea.narrator_gender == "female":
            tone_note = "Favor emotionally layered, introspective delivery — vulnerability is strength."
        elif storyIdea.narrator_gender == "male":
            tone_note = "Lean into emotional honesty — let tension and reflection carry the story."

        return f"""You are a professional viral storyteller writing scripts designed for TikTok, YouTube Shorts, and Reels.
                
                Your stories should be written in a {narrator_type}, emotionally engaging, voiceover-friendly style.
                {voice_note}
                {tone_note}
                
                Focus on stories where a person from a modest or working-class background interacts with wealth, power, or privilege — often through dating someone rich, meeting their family, or being exposed to a different world.
                
                Every story must follow this structure:
                
                1. Hook:
                Start with a strong, attention-grabbing first line (within 1–2 sentences) that sparks curiosity or tension.
                Examples:
                – “I dated a billionaire’s daughter. Her dad taught me more than school ever did.”
                – “I wore a $20 Target shirt to dinner with millionaires. Here’s what happened.”
                
                2. Conflict / Insecurity:
                Describe a moment where the narrator feels out of place, ashamed, judged, or underestimated.
                Use vivid emotional cues and sensory details — let the audience feel their discomfort or doubt.
                
                3. Shift or Reveal:
                Include an unexpected moment of connection, irony, or reversal.
                Either the rich person reveals humility… or the narrator discovers who truly holds power or value.
                
                4. Payoff / Moral / Quote:
                End with a single emotionally satisfying line, quote, or realization.
                Something that lingers — a mic-drop moment, bittersweet truth, or shift in self-worth.
                
                The voice should be casual, emotionally raw, and paced for vertical video — short paragraphs, natural rhythm.
                
                ✸ Avoid overexplaining — let the story unfold naturally.        
                ✸ Include subtle emotional ironies or details that viewers may only notice on second watch.
                ✸ Leave just enough unsaid to spark comments and debate (“Was the dad testing him?”, “Did she already know?”).
                ✸ Avoid camera directions or formatting — output only the character’s inner narration.
                ✸ Avoid polished “writerly” structure
                ✸ Include human-level imperfection, memory fuzziness, or honesty
                """.strip()

    def generate_from_storyidea(self, storyIdea: StoryIdea) -> str:
        messages = [
            {"role": "system", "content": self._build_system_prompt(storyIdea)},
            {"role": "user", "content": self._build_user_prompt(storyIdea)}
        ]
        response = openai.ChatCompletion.create(model=self.model, messages=messages)
        script = response.choices[0].message.content.strip();
        self.save_script_with_idea(storyIdea, script)

    def save_script_with_idea(self, idea: StoryIdea, script: str):
        script_path = os.path.join(SCRIPTS_PATH, sanitize_filename(idea.story_title))
        os.makedirs(script_path, exist_ok=True)

        original_idea_path = os.path.join(IDEAS_PATH, sanitize_filename(idea.story_title) + ".json")
        new_idea_path = os.path.join(script_path, "Idea.json")

        if os.path.exists(original_idea_path):
            shutil.move(original_idea_path, new_idea_path)
        else:
            raise FileNotFoundError(f"Idea file not found at: {original_idea_path}")

        filename = "Script.txt"
        filepath = os.path.join(script_path, filename)

        # Write the script to the file
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(script)
