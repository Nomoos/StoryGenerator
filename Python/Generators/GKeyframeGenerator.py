import os
import torch
import json
from typing import List, Tuple
from diffusers import StableDiffusionPipeline, DPMSolverMultistepScheduler
from PIL import Image
from Models.StoryIdea import StoryIdea
from Generators.GSceneAnalyzer import Scene, SceneAnalyzer
from Tools.Utils import TITLES_PATH, sanitize_filename


class KeyframeGenerator:
    """
    Generates keyframe images for each scene using Stable Diffusion.
    Creates start, middle, and end keyframes for smooth video interpolation.
    """

    def __init__(
        self,
        model_id: str = "runwayml/stable-diffusion-v1-5",
        device: str = None,
        num_inference_steps: int = 30
    ):
        """
        Initialize the keyframe generator with Stable Diffusion
        
        Args:
            model_id: HuggingFace model ID for Stable Diffusion
            device: Device to run on ('cuda' or 'cpu'). Auto-detects if None
            num_inference_steps: Number of denoising steps for image generation
        """
        self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")
        self.num_inference_steps = num_inference_steps
        
        print(f"🎨 Loading Stable Diffusion model on {self.device}...")
        
        # Load the model with optimizations
        self.pipe = StableDiffusionPipeline.from_pretrained(
            model_id,
            torch_dtype=torch.float16 if self.device == "cuda" else torch.float32,
            safety_checker=None  # Disable for speed
        )
        
        # Use DPM-Solver for faster generation
        self.pipe.scheduler = DPMSolverMultistepScheduler.from_config(
            self.pipe.scheduler.config
        )
        
        self.pipe = self.pipe.to(self.device)
        
        # Enable memory optimizations
        if self.device == "cuda":
            self.pipe.enable_attention_slicing()
            # self.pipe.enable_vae_slicing()  # Optional: saves more memory
        
        self.analyzer = SceneAnalyzer()
        print("✅ Stable Diffusion model loaded successfully")

    def generate_keyframes(self, story_idea: StoryIdea) -> List[Scene]:
        """
        Generate keyframe images for all scenes in a story
        
        Args:
            story_idea: StoryIdea object for the story
            
        Returns:
            List of Scene objects with keyframe paths populated
        """
        # Load scenes with descriptions
        scenes = self.analyzer.load_scenes(story_idea)
        
        folder_path = os.path.join(TITLES_PATH, sanitize_filename(story_idea.story_title))
        keyframes_dir = os.path.join(folder_path, "keyframes")
        os.makedirs(keyframes_dir, exist_ok=True)
        
        print(f"🎬 Generating keyframes for {len(scenes)} scenes...")
        
        for scene in scenes:
            if not scene.description:
                print(f"⚠️ Scene {scene.scene_id} has no description. Skipping...")
                continue
            
            print(f"  Scene {scene.scene_id}/{len(scenes)}: Generating keyframes...")
            
            # Generate keyframes based on scene duration
            keyframe_paths = self._generate_scene_keyframes(
                scene=scene,
                output_dir=keyframes_dir,
                story_idea=story_idea
            )
            
            scene.keyframes = keyframe_paths
        
        # Save updated scenes with keyframe paths
        self.analyzer._save_scenes(scenes, folder_path)
        
        print(f"✅ Generated all keyframes for '{story_idea.story_title}'")
        return scenes

    def _generate_scene_keyframes(
        self,
        scene: Scene,
        output_dir: str,
        story_idea: StoryIdea
    ) -> List[str]:
        """
        Generate keyframes for a single scene
        
        Strategy:
        - Short scenes (< 5s): 2 keyframes (start, end)
        - Medium scenes (5-10s): 3 keyframes (start, middle, end)
        - Long scenes (> 10s): 4+ keyframes (start, mid1, mid2, end)
        """
        duration = scene.duration
        scene_id = scene.scene_id
        
        # Determine number of keyframes based on duration
        if duration < 5:
            num_keyframes = 2  # start, end
        elif duration < 10:
            num_keyframes = 3  # start, middle, end
        else:
            # Add one keyframe per 4 seconds
            num_keyframes = min(int(duration / 4) + 1, 6)
        
        keyframe_paths = []
        
        for i in range(num_keyframes):
            # Calculate position in scene (0.0 to 1.0)
            if num_keyframes == 1:
                position = 0.5
            else:
                position = i / (num_keyframes - 1)
            
            # Generate timestamp for this keyframe
            timestamp = scene.start_time + (position * duration)
            
            # Create position-specific prompt variation
            prompt = self._create_keyframe_prompt(scene, position, story_idea)
            
            # Generate image
            filename = f"scene_{scene_id:03d}_keyframe_{i:02d}_t{timestamp:.2f}.png"
            filepath = os.path.join(output_dir, filename)
            
            # Skip if already exists
            if os.path.exists(filepath):
                print(f"    ⏭️  Keyframe already exists: {filename}")
                keyframe_paths.append(filepath)
                continue
            
            try:
                image = self._generate_image(prompt)
                
                # Save image with metadata
                image.save(filepath, "PNG")
                
                # Save metadata
                metadata = {
                    "scene_id": scene_id,
                    "keyframe_index": i,
                    "timestamp": timestamp,
                    "position": position,
                    "prompt": prompt
                }
                
                metadata_path = filepath.replace('.png', '.json')
                with open(metadata_path, 'w', encoding='utf-8') as f:
                    json.dump(metadata, f, indent=2)
                
                print(f"    ✅ Generated: {filename}")
                keyframe_paths.append(filepath)
                
            except Exception as e:
                print(f"    ❌ Failed to generate {filename}: {e}")
                continue
        
        return keyframe_paths

    def _create_keyframe_prompt(
        self,
        scene: Scene,
        position: float,
        story_idea: StoryIdea
    ) -> str:
        """
        Create a position-specific prompt variation for a keyframe
        
        Args:
            scene: Scene object with base description
            position: Position in scene (0.0 = start, 1.0 = end)
            story_idea: Story context
        """
        base_prompt = scene.description
        
        # Add position-specific modifiers
        if position < 0.3:
            # Early in scene - focus on establishing shot
            modifiers = "establishing shot, scene opening, wide framing"
        elif position > 0.7:
            # Late in scene - focus on reaction/result
            modifiers = "close-up reaction, emotional moment, intimate framing"
        else:
            # Middle - balanced composition
            modifiers = "medium shot, natural transition, balanced composition"
        
        # Add vertical format reminder
        format_spec = "vertical format 9:16 aspect ratio, 1080x1920 resolution"
        
        # Combine
        full_prompt = f"{base_prompt}, {modifiers}, {format_spec}"
        
        return full_prompt

    def _generate_image(self, prompt: str) -> Image.Image:
        """
        Generate a single image from a prompt
        
        Args:
            prompt: Text prompt for image generation
            
        Returns:
            PIL Image object
        """
        # Negative prompt to avoid common issues
        negative_prompt = (
            "blurry, low quality, distorted, deformed, ugly, bad anatomy, "
            "watermark, text, signature, multiple people, crowd, "
            "horizontal format, landscape, low resolution"
        )
        
        # Generate image
        with torch.no_grad():
            result = self.pipe(
                prompt=prompt,
                negative_prompt=negative_prompt,
                num_inference_steps=self.num_inference_steps,
                guidance_scale=7.5,
                height=1920,  # Vertical format
                width=1080,
                generator=torch.Generator(device=self.device).manual_seed(42)
            )
        
        return result.images[0]

    def cleanup(self):
        """Clean up GPU memory"""
        if hasattr(self, 'pipe'):
            del self.pipe
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
