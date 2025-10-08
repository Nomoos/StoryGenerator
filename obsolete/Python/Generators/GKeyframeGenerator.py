import os
import torch
import json
import time
from typing import List, Tuple, Optional
from diffusers import DiffusionPipeline, DPMSolverMultistepScheduler
from PIL import Image
from Models.StoryIdea import StoryIdea
from Models.Keyframe import Keyframe
from Generators.GSceneAnalyzer import Scene, SceneAnalyzer
from Tools.Utils import TITLES_PATH, sanitize_filename
from Tools.ImageUtils import scale_and_crop
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from config import sdxl_config


class KeyframeGenerator:
    """
    Generates keyframe images for each scene using Stable Diffusion XL (SDXL).
    Creates high-quality keyframes at 1080x1920 resolution (9:16 aspect ratio).
    Supports base + refiner pipeline for maximum quality.
    """

    def __init__(
        self,
        model_id: str = None,
        device: str = None,
        num_inference_steps: int = None,
        use_refiner: bool = None,
        style_preset: str = None
    ):
        """
        Initialize the keyframe generator with SDXL
        
        Args:
            model_id: HuggingFace model ID for SDXL (default: from config)
            device: Device to run on ('cuda' or 'cpu'). Auto-detects if None
            num_inference_steps: Number of denoising steps (default: from config)
            use_refiner: Whether to use refiner model (default: from config)
            style_preset: Default style preset (default: from config)
        """
        # Load configuration
        self.config = sdxl_config
        
        # Set parameters from config or arguments
        self.model_id = model_id or self.config.SDXL_BASE_MODEL
        self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")
        self.num_inference_steps = num_inference_steps or self.config.DEFAULT_STEPS
        self.use_refiner = use_refiner if use_refiner is not None else self.config.USE_REFINER
        self.style_preset = style_preset or self.config.DEFAULT_STYLE
        
        # Load style presets
        self._load_style_presets()
        
        # Load negative prompts
        self._load_negative_prompts()
        
        print(f"🎨 Loading SDXL model on {self.device}...")
        print(f"   Model: {self.model_id}")
        print(f"   Refiner: {'Enabled' if self.use_refiner else 'Disabled'}")
        print(f"   Style: {self.style_preset}")
        
        # Determine torch dtype
        torch_dtype = torch.float16 if self.device == "cuda" else torch.float32
        
        # Load the base SDXL model
        self.pipe = DiffusionPipeline.from_pretrained(
            self.model_id,
            torch_dtype=torch_dtype,
            use_safetensors=True,
            variant="fp16" if self.device == "cuda" else None
        )
        
        self.pipe = self.pipe.to(self.device)
        
        # Enable memory optimizations
        if self.device == "cuda":
            if self.config.ENABLE_ATTENTION_SLICING:
                self.pipe.enable_attention_slicing()
            if self.config.ENABLE_VAE_SLICING:
                self.pipe.enable_vae_slicing()
            if self.config.ENABLE_CPU_OFFLOAD:
                self.pipe.enable_model_cpu_offload()
        
        # Load refiner if enabled
        self.refiner = None
        if self.use_refiner:
            print(f"🔧 Loading SDXL refiner model...")
            self.refiner = DiffusionPipeline.from_pretrained(
                self.config.SDXL_REFINER_MODEL,
                text_encoder_2=self.pipe.text_encoder_2,
                vae=self.pipe.vae,
                torch_dtype=torch_dtype,
                use_safetensors=True,
                variant="fp16" if self.device == "cuda" else None
            )
            self.refiner = self.refiner.to(self.device)
            
            # Enable optimizations for refiner
            if self.device == "cuda":
                if self.config.ENABLE_ATTENTION_SLICING:
                    self.refiner.enable_attention_slicing()
                if self.config.ENABLE_VAE_SLICING:
                    self.refiner.enable_vae_slicing()
        
        self.analyzer = SceneAnalyzer()
        print("✅ SDXL model loaded successfully")
    
    def _load_style_presets(self):
        """Load style presets from JSON file"""
        presets_path = os.path.join(
            os.path.dirname(__file__), '..', '..', 'prompts', 'style_presets.json'
        )
        try:
            with open(presets_path, 'r', encoding='utf-8') as f:
                self.style_presets = json.load(f)
        except FileNotFoundError:
            print(f"⚠️ Style presets not found at {presets_path}, using defaults")
            self.style_presets = {
                "cinematic": {
                    "prompt_additions": "cinematic lighting, professional photography",
                    "guidance_scale": 7.5,
                    "steps": 40
                }
            }
    
    def _load_negative_prompts(self):
        """Load negative prompts from file"""
        neg_prompts_path = os.path.join(
            os.path.dirname(__file__), '..', '..', 'prompts', 'negative_prompts.txt'
        )
        try:
            with open(neg_prompts_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                # Filter out comments and empty lines
                prompt_lines = [
                    line.strip() for line in lines 
                    if line.strip() and not line.strip().startswith('#')
                ]
                self.default_negative_prompt = ', '.join(prompt_lines)
        except FileNotFoundError:
            print(f"⚠️ Negative prompts not found at {neg_prompts_path}, using defaults")
            self.default_negative_prompt = (
                "blurry, low quality, distorted, deformed, ugly, bad anatomy, "
                "watermark, text, signature, horizontal format, landscape"
            )

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
            num_keyframes = self.config.KEYFRAMES_SHORT_SCENE
        elif duration < 10:
            num_keyframes = self.config.KEYFRAMES_MEDIUM_SCENE
        else:
            # Add one keyframe per 4 seconds for long scenes
            num_keyframes = min(
                int(duration / 4) + 1, 
                self.config.MAX_KEYFRAMES_PER_SCENE
            )
        
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
                start_time = time.time()
                
                # Generate image with SDXL
                image = self._generate_image(prompt)
                
                generation_time = time.time() - start_time
                
                # Ensure proper resolution
                if image.width != self.config.DEFAULT_WIDTH or image.height != self.config.DEFAULT_HEIGHT:
                    image = scale_and_crop(
                        image, 
                        self.config.DEFAULT_WIDTH, 
                        self.config.DEFAULT_HEIGHT
                    )
                
                # Save image
                image.save(filepath, self.config.IMAGE_FORMAT)
                
                # Create Keyframe object with metadata
                keyframe = Keyframe(
                    scene_id=scene_id,
                    image_path=filepath,
                    prompt=prompt,
                    negative_prompt=self.default_negative_prompt,
                    seed=self.config.SEED if self.config.SEED else -1,
                    width=self.config.DEFAULT_WIDTH,
                    height=self.config.DEFAULT_HEIGHT,
                    steps=self.num_inference_steps,
                    guidance_scale=self._get_guidance_scale(),
                    style_preset=self.style_preset,
                    generation_time=generation_time,
                    keyframe_index=i,
                    timestamp=timestamp,
                    position=position,
                    use_refiner=self.use_refiner,
                    refiner_steps=self.config.DEFAULT_REFINER_STEPS if self.use_refiner else 0
                )
                
                # Save metadata
                metadata_path = filepath.replace('.png', '.json').replace('.jpg', '.json')
                keyframe.save_metadata(metadata_path)
                
                print(f"    ✅ Generated: {filename} ({generation_time:.2f}s)")
                keyframe_paths.append(filepath)
                
            except Exception as e:
                print(f"    ❌ Failed to generate {filename}: {e}")
                import traceback
                traceback.print_exc()
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
        
        # Add style preset enhancements
        style_additions = ""
        if self.style_preset in self.style_presets:
            style_additions = self.style_presets[self.style_preset].get("prompt_additions", "")
        
        # Add quality boost keywords
        quality_boost = self.config.QUALITY_BOOST_KEYWORDS
        
        # Add vertical format reminder
        format_spec = self.config.FORMAT_SPECIFICATION
        
        # Combine all elements
        full_prompt = f"{base_prompt}, {modifiers}, {style_additions}, {quality_boost}, {format_spec}"
        
        return full_prompt
    
    def _get_guidance_scale(self) -> float:
        """Get guidance scale from style preset or config"""
        if self.style_preset in self.style_presets:
            return self.style_presets[self.style_preset].get(
                "guidance_scale", 
                self.config.DEFAULT_GUIDANCE_SCALE
            )
        return self.config.DEFAULT_GUIDANCE_SCALE

    def _generate_image(self, prompt: str) -> Image.Image:
        """
        Generate a single image from a prompt using SDXL
        
        Args:
            prompt: Text prompt for image generation
            
        Returns:
            PIL Image object
        """
        # Get generation parameters
        guidance_scale = self._get_guidance_scale()
        seed = self.config.SEED
        
        # Create generator for reproducibility
        generator = None
        if seed is not None:
            generator = torch.Generator(device=self.device).manual_seed(seed)
        
        # Generate with base model
        with torch.no_grad():
            if self.use_refiner:
                # Two-stage generation: base + refiner
                # Generate latents with base model
                base_output = self.pipe(
                    prompt=prompt,
                    negative_prompt=self.default_negative_prompt,
                    num_inference_steps=self.num_inference_steps,
                    guidance_scale=guidance_scale,
                    height=self.config.DEFAULT_HEIGHT,
                    width=self.config.DEFAULT_WIDTH,
                    generator=generator,
                    output_type="latent",  # Return latents for refiner
                    denoising_end=0.8  # Stop at 80% for refiner to take over
                )
                
                # Refine with refiner model
                image = self.refiner(
                    prompt=prompt,
                    negative_prompt=self.default_negative_prompt,
                    num_inference_steps=self.config.DEFAULT_REFINER_STEPS,
                    guidance_scale=self.config.DEFAULT_REFINER_GUIDANCE_SCALE,
                    image=base_output.images,
                    denoising_start=0.8  # Start where base left off
                ).images[0]
            else:
                # Single-stage generation with base model only
                result = self.pipe(
                    prompt=prompt,
                    negative_prompt=self.default_negative_prompt,
                    num_inference_steps=self.num_inference_steps,
                    guidance_scale=guidance_scale,
                    height=self.config.DEFAULT_HEIGHT,
                    width=self.config.DEFAULT_WIDTH,
                    generator=generator
                )
                image = result.images[0]
        
        return image

    def apply_style_preset(self, style_name: str):
        """
        Apply a style preset to the generator
        
        Args:
            style_name: Name of the style preset to apply
        """
        if style_name in self.style_presets:
            self.style_preset = style_name
            
            # Update steps if specified in preset
            preset = self.style_presets[style_name]
            if "steps" in preset:
                self.num_inference_steps = preset["steps"]
            
            print(f"✨ Applied style preset: {style_name}")
            print(f"   Description: {preset.get('description', 'N/A')}")
        else:
            print(f"⚠️ Style preset '{style_name}' not found. Available: {list(self.style_presets.keys())}")
    
    def cleanup(self):
        """Clean up GPU memory"""
        if hasattr(self, 'pipe'):
            del self.pipe
        if hasattr(self, 'refiner') and self.refiner is not None:
            del self.refiner
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
            print("🧹 GPU memory cleaned up")
