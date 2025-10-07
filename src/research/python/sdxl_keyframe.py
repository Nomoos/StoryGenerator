"""
SDXL keyframe generation using Diffusers library.
Research prototype for text-to-image generation for video keyframes.
"""

from typing import Optional, List, Dict
from pathlib import Path
import random


class SDXLKeyframeGenerator:
    """
    Stable Diffusion XL wrapper for generating video keyframes.
    
    This is a research prototype demonstrating how to:
    - Load and use SDXL models with Diffusers
    - Generate high-quality images from text prompts
    - Apply styles and quality settings
    - Generate consistent keyframes for video
    """
    
    def __init__(
        self,
        model_id: str = "stabilityai/stable-diffusion-xl-base-1.0",
        device: str = "auto",
        torch_dtype: str = "float16",
        use_refiner: bool = False
    ):
        """
        Initialize SDXL model.
        
        Args:
            model_id: HuggingFace model ID
            device: Device to use ("cpu", "cuda", "auto")
            torch_dtype: Data type for model ("float16", "float32")
            use_refiner: Whether to use SDXL refiner for enhanced quality
        """
        self.model_id = model_id
        self.device = self._get_device(device)
        self.torch_dtype = torch_dtype
        self.use_refiner = use_refiner
        self.pipe = None
        self.refiner = None
        
    def _get_device(self, device: str) -> str:
        """Determine the device to use."""
        if device == "auto":
            try:
                import torch
                return "cuda" if torch.cuda.is_available() else "cpu"
            except ImportError:
                return "cpu"
        return device
    
    def load_model(self):
        """Load SDXL pipeline."""
        try:
            import torch
            from diffusers import StableDiffusionXLPipeline, DPMSolverMultistepScheduler
            
            # Determine torch dtype
            dtype = torch.float16 if self.torch_dtype == "float16" and self.device == "cuda" else torch.float32
            
            # Load base model
            self.pipe = StableDiffusionXLPipeline.from_pretrained(
                self.model_id,
                torch_dtype=dtype,
                use_safetensors=True,
                variant="fp16" if dtype == torch.float16 else None
            )
            
            # Use DPM++ scheduler for better quality
            self.pipe.scheduler = DPMSolverMultistepScheduler.from_config(
                self.pipe.scheduler.config
            )
            
            # Move to device
            self.pipe.to(self.device)
            
            # Enable memory optimizations
            if self.device == "cuda":
                self.pipe.enable_attention_slicing()
                try:
                    self.pipe.enable_xformers_memory_efficient_attention()
                except Exception:
                    pass  # xformers not available
            
            print(f"Loaded SDXL model on {self.device}")
            
            # Load refiner if requested
            if self.use_refiner:
                from diffusers import StableDiffusionXLImg2ImgPipeline
                self.refiner = StableDiffusionXLImg2ImgPipeline.from_pretrained(
                    "stabilityai/stable-diffusion-xl-refiner-1.0",
                    torch_dtype=dtype,
                    use_safetensors=True,
                    variant="fp16" if dtype == torch.float16 else None
                )
                self.refiner.to(self.device)
                print("Loaded SDXL refiner")
                
        except ImportError as e:
            raise ImportError(
                f"Required packages not installed: {e}\n"
                "Install with: pip install diffusers transformers accelerate"
            )
    
    def generate_keyframe(
        self,
        prompt: str,
        negative_prompt: Optional[str] = None,
        width: int = 1024,
        height: int = 1024,
        num_inference_steps: int = 30,
        guidance_scale: float = 7.5,
        seed: Optional[int] = None,
        output_path: Optional[str] = None
    ):
        """
        Generate a single keyframe image.
        
        Args:
            prompt: Text description of the image
            negative_prompt: Things to avoid in the image
            width: Image width (should be multiple of 8)
            height: Image height (should be multiple of 8)
            num_inference_steps: Number of denoising steps (more = better quality)
            guidance_scale: How closely to follow the prompt (7-15 typical)
            seed: Random seed for reproducibility
            output_path: Path to save the image
            
        Returns:
            PIL Image object
        """
        if self.pipe is None:
            self.load_model()
        
        # Set default negative prompt if none provided
        if negative_prompt is None:
            negative_prompt = (
                "blurry, low quality, distorted, deformed, ugly, "
                "bad anatomy, watermark, signature, text"
            )
        
        # Set random seed
        if seed is not None:
            import torch
            generator = torch.Generator(device=self.device).manual_seed(seed)
        else:
            generator = None
        
        # Generate image
        output = self.pipe(
            prompt=prompt,
            negative_prompt=negative_prompt,
            width=width,
            height=height,
            num_inference_steps=num_inference_steps,
            guidance_scale=guidance_scale,
            generator=generator
        )
        
        image = output.images[0]
        
        # Refine if refiner is loaded
        if self.refiner is not None:
            image = self.refiner(
                prompt=prompt,
                image=image,
                num_inference_steps=20,
                guidance_scale=guidance_scale,
                generator=generator
            ).images[0]
        
        # Save if path provided
        if output_path:
            Path(output_path).parent.mkdir(parents=True, exist_ok=True)
            image.save(output_path)
        
        return image
    
    def generate_keyframe_sequence(
        self,
        prompts: List[str],
        output_dir: str,
        width: int = 1024,
        height: int = 1024,
        num_inference_steps: int = 30,
        guidance_scale: float = 7.5,
        base_seed: Optional[int] = None,
        negative_prompt: Optional[str] = None
    ) -> List[str]:
        """
        Generate a sequence of keyframes from prompts.
        
        Args:
            prompts: List of text prompts for each keyframe
            output_dir: Directory to save keyframes
            width: Image width
            height: Image height
            num_inference_steps: Denoising steps
            guidance_scale: Prompt adherence
            base_seed: Base seed (incremented for each frame)
            negative_prompt: Things to avoid
            
        Returns:
            List of paths to generated keyframes
        """
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        if base_seed is None:
            base_seed = random.randint(0, 2**32 - 1)
        
        keyframe_paths = []
        
        for i, prompt in enumerate(prompts):
            output_path = output_dir / f"keyframe_{i:04d}.png"
            seed = base_seed + i
            
            print(f"Generating keyframe {i+1}/{len(prompts)}: {prompt[:50]}...")
            
            self.generate_keyframe(
                prompt=prompt,
                negative_prompt=negative_prompt,
                width=width,
                height=height,
                num_inference_steps=num_inference_steps,
                guidance_scale=guidance_scale,
                seed=seed,
                output_path=str(output_path)
            )
            
            keyframe_paths.append(str(output_path))
        
        return keyframe_paths
    
    def apply_style_preset(self, base_prompt: str, style: str = "cinematic") -> str:
        """
        Apply a style preset to a prompt.
        
        Args:
            base_prompt: Base description
            style: Style preset name
            
        Returns:
            Enhanced prompt with style
        """
        style_presets = {
            "cinematic": (
                f"{base_prompt}, cinematic lighting, film grain, "
                "depth of field, professional color grading, 8k"
            ),
            "anime": (
                f"{base_prompt}, anime style, vibrant colors, "
                "studio ghibli, detailed, high quality"
            ),
            "realistic": (
                f"{base_prompt}, photorealistic, ultra detailed, "
                "sharp focus, professional photography, DSLR"
            ),
            "artistic": (
                f"{base_prompt}, digital art, concept art, "
                "trending on artstation, detailed, vibrant"
            ),
            "dramatic": (
                f"{base_prompt}, dramatic lighting, moody atmosphere, "
                "high contrast, cinematic composition"
            )
        }
        
        return style_presets.get(style, base_prompt)
    
    def unload_model(self):
        """Free GPU memory by unloading models."""
        if self.pipe is not None:
            del self.pipe
            self.pipe = None
        if self.refiner is not None:
            del self.refiner
            self.refiner = None
        
        try:
            import torch
            if torch.cuda.is_available():
                torch.cuda.empty_cache()
        except ImportError:
            pass


# Example usage
if __name__ == "__main__":
    # Initialize generator
    generator = SDXLKeyframeGenerator(use_refiner=False)
    
    # Single keyframe
    prompt = "A majestic mountain landscape at sunset, golden hour lighting"
    image = generator.generate_keyframe(
        prompt=prompt,
        width=1024,
        height=768,
        num_inference_steps=30,
        seed=42,
        output_path="keyframe_001.png"
    )
    print("Generated keyframe saved")
    
    # Apply style
    styled_prompt = generator.apply_style_preset(
        "a robot painting on a canvas",
        style="cinematic"
    )
    print(f"Styled prompt: {styled_prompt}")
    
    # Generate sequence
    prompts = [
        "A young girl walking down a dimly lit hallway, sad expression",
        "Close-up of the girl's face, tears in her eyes",
        "The girl sitting alone in an empty classroom"
    ]
    
    keyframes = generator.generate_keyframe_sequence(
        prompts=prompts,
        output_dir="keyframes/",
        width=1024,
        height=576,  # 16:9 aspect ratio
        num_inference_steps=25,
        base_seed=12345
    )
    print(f"Generated {len(keyframes)} keyframes")
