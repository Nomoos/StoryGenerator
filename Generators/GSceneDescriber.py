import os
import openai
from typing import List
from Models.StoryIdea import StoryIdea
from Generators.GSceneAnalyzer import Scene, SceneAnalyzer
from Tools.Utils import TITLES_PATH, sanitize_filename

openai.api_key = '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'


class SceneDescriber:
    """
    Generates visual descriptions for each scene using GPT.
    Creates detailed prompts suitable for image generation models like Stable Diffusion.
    """

    def __init__(self, model: str = "gpt-4o-mini"):
        self.model = model
        self.analyzer = SceneAnalyzer()

    def describe_scenes(self, story_idea: StoryIdea) -> List[Scene]:
        """
        Generate visual descriptions for all scenes in a story
        
        Args:
            story_idea: StoryIdea object for the story
            
        Returns:
            List of Scene objects with descriptions filled in
        """
        # Load scenes
        scenes = self.analyzer.load_scenes(story_idea)

        # Load full script for context
        folder_path = os.path.join(TITLES_PATH, sanitize_filename(story_idea.story_title))
        script_path = os.path.join(folder_path, "Revised.txt")
        
        with open(script_path, 'r', encoding='utf-8') as f:
            full_script = f.read()

        print(f"🎨 Generating visual descriptions for {len(scenes)} scenes...")

        # Generate descriptions for each scene
        for i, scene in enumerate(scenes):
            print(f"  Scene {scene.scene_id}/{len(scenes)}: {scene.text[:50]}...")
            
            description = self._generate_scene_description(
                scene=scene,
                story_idea=story_idea,
                full_script=full_script,
                scene_index=i,
                total_scenes=len(scenes)
            )
            
            scene.description = description

        # Save updated scenes
        self.analyzer._save_scenes(scenes, folder_path)
        
        print(f"✅ Generated descriptions for all {len(scenes)} scenes")
        return scenes

    def _generate_scene_description(
        self,
        scene: Scene,
        story_idea: StoryIdea,
        full_script: str,
        scene_index: int,
        total_scenes: int
    ) -> str:
        """Generate a single scene description using GPT"""
        
        messages = [
            {"role": "system", "content": self._build_system_prompt(story_idea)},
            {"role": "user", "content": self._build_user_prompt(
                scene, full_script, scene_index, total_scenes
            )}
        ]
        
        response = openai.ChatCompletion.create(model=self.model, messages=messages)
        return response.choices[0].message.content.strip()

    def _build_system_prompt(self, story_idea: StoryIdea) -> str:
        """Build system prompt for scene description generation"""
        
        narrator_gender = story_idea.narrator_gender or "female"
        narrator_type = story_idea.narrator_type or "first-person"
        
        return f"""You are a professional visual director for short-form vertical video content (TikTok, YouTube Shorts, Reels).

Your task is to create detailed visual descriptions for scenes in a {narrator_type} story told by a {narrator_gender} narrator.

🎯 Key Requirements:

**Format & Composition:**
- All visuals must be designed for 1080×1920 vertical format (9:16 aspect ratio)
- Frame subjects prominently with proper headroom for vertical viewing
- Consider mobile viewing - keep important elements in the center safe zone
- Use shallow depth of field to focus attention

**Visual Style:**
- Photorealistic, cinematic quality (like film photography)
- Natural lighting with emotional undertones
- 35mm film aesthetic with soft, natural colors
- Subtle film grain for authenticity
- Shallow depth of field (f/1.8 - f/2.8) for emotional focus

**Emotional Tone:**
- Match the emotional beat of the narration
- Use lighting, color temperature, and framing to convey feeling
- Show character emotions through body language and facial expressions
- Create visual metaphors that enhance the story

**Character Consistency:**
- Maintain consistent appearance of the narrator throughout
- Age: teens to early 20s
- Style should match the story's context (casual, formal, etc.)
- Natural, relatable appearance - not overly styled

**Technical Specifications:**
- Output prompts suitable for Stable Diffusion or similar image generation
- Include: subject, action, setting, lighting, mood, camera angle, technical details
- Keep prompts clear and well-structured
- Use descriptive language that image models understand well

🚫 Avoid:
- Generic or vague descriptions
- Overly complex or cluttered compositions
- Unrealistic or fantasy elements (unless story-appropriate)
- Multiple disconnected subjects in one frame
- Horizontal or landscape framing

Output only the visual description prompt, nothing else.""".strip()

    def _build_user_prompt(
        self,
        scene: Scene,
        full_script: str,
        scene_index: int,
        total_scenes: int
    ) -> str:
        """Build user prompt for a specific scene"""
        
        # Determine scene position in narrative arc
        position = "opening"
        if scene_index < total_scenes * 0.2:
            position = "opening"
        elif scene_index < total_scenes * 0.5:
            position = "rising action"
        elif scene_index < total_scenes * 0.8:
            position = "climax/reveal"
        else:
            position = "resolution"

        return f"""Create a detailed visual description for this scene from a short-form vertical video story.

**Story Context:**
This is scene {scene.scene_id} of {total_scenes} (narrative position: {position})

**Scene Duration:** {scene.duration:.1f} seconds

**Scene Narration:**
"{scene.text}"

**Full Story Context (for reference):**
{full_script[:500]}...

🎯 Your Task:
Create a detailed image generation prompt that:
1. Captures the emotional tone of this specific moment
2. Maintains visual continuity with the story's overall arc
3. Works perfectly in 1080×1920 vertical format
4. Is technically precise for Stable Diffusion image generation
5. Shows (don't tell) - visual storytelling through composition, lighting, expressions

**Prompt Structure Example:**
[Subject and action], [setting and environment], [lighting and mood], [camera angle and framing], [technical details: photorealistic, 35mm, shallow depth of field, etc.], [vertical format, 9:16 aspect ratio]

Output only the image generation prompt - no explanations, no quotes, no formatting.""".strip()
