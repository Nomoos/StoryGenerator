"""
Vision Guidance Generator using LLaVA-OneVision or Phi-3.5-vision.
Provides image captioning, quality assessment, and consistency validation.
"""

import os
import sys
from typing import List, Optional, Tuple, Union
from pathlib import Path
import torch
from PIL import Image

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from Models.VisionAnalysis import (
    VisionAnalysisResult,
    QualityScore,
    ConsistencyScore,
    ImageCaption,
    StoryboardValidation
)
from Tools.VisionUtils import (
    load_image,
    load_images,
    resize_image_for_vision_model,
    parse_quality_scores,
    parse_consistency_scores,
    check_gpu_available,
    estimate_vram_usage
)
from Tools.Monitor import logger, log_info, log_error
from Tools.Retry import retry_with_exponential_backoff

try:
    from transformers import AutoProcessor, AutoModelForVision2Seq
    TRANSFORMERS_AVAILABLE = True
except ImportError:
    TRANSFORMERS_AVAILABLE = False
    print("⚠️ transformers not installed. Install with: pip install transformers")


class GVision:
    """
    Vision guidance generator supporting multiple vision-language models.
    """
    
    SUPPORTED_MODELS = {
        "llava-onevision": "llava-hf/llava-onevision-qwen2-7b-ov-hf",
        "phi-3.5-vision": "microsoft/Phi-3.5-vision-instruct",
        "llava-v1.5-7b": "llava-hf/llava-1.5-7b-hf",
    }
    
    def __init__(
        self,
        model_name: str = "phi-3.5-vision",
        device: str = None,
        load_model: bool = False
    ):
        """
        Initialize vision guidance generator.
        
        Args:
            model_name: Name of vision model to use (llava-onevision, phi-3.5-vision, etc.)
            device: Device to run on ('cuda' or 'cpu'). Auto-detects if None.
            load_model: Whether to load the model immediately (can be expensive)
        """
        self.model_name = model_name
        self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")
        
        # Check GPU availability
        gpu_available, device_name = check_gpu_available()
        if self.device == "cuda" and not gpu_available:
            log_info("CUDA requested but not available, falling back to CPU")
            self.device = "cpu"
        
        log_info(f"Vision guidance initialized with device: {self.device}")
        if gpu_available:
            log_info(f"GPU: {device_name}")
            log_info(f"Estimated VRAM usage for {model_name}: {estimate_vram_usage(model_name)}")
        
        self.processor = None
        self.model = None
        
        if load_model:
            if not TRANSFORMERS_AVAILABLE:
                raise ImportError(
                    "transformers library is required for model loading. "
                    "Install with: pip install transformers"
                )
            self._load_model()
    
    def _load_model(self):
        """Load the vision model and processor."""
        if self.model is not None:
            return  # Already loaded
        
        if not TRANSFORMERS_AVAILABLE:
            raise ImportError(
                "transformers library is required for model loading. "
                "Install with: pip install transformers"
            )
        
        try:
            # Get model ID
            if self.model_name in self.SUPPORTED_MODELS:
                model_id = self.SUPPORTED_MODELS[self.model_name]
            else:
                # Assume it's a full HuggingFace model ID
                model_id = self.model_name
            
            log_info(f"Loading vision model: {model_id}")
            
            # Load processor
            self.processor = AutoProcessor.from_pretrained(
                model_id,
                trust_remote_code=True
            )
            
            # Load model with appropriate dtype
            dtype = torch.float16 if self.device == "cuda" else torch.float32
            
            self.model = AutoModelForVision2Seq.from_pretrained(
                model_id,
                torch_dtype=dtype,
                trust_remote_code=True,
                low_cpu_mem_usage=True
            )
            
            self.model = self.model.to(self.device)
            self.model.eval()
            
            log_info(f"✅ Vision model loaded successfully on {self.device}")
            
        except Exception as e:
            log_error(f"Failed to load vision model: {e}")
            raise
    
    @retry_with_exponential_backoff(
        max_retries=2,
        base_delay=1.0,
        max_delay=10.0,
        exceptions=(Exception,)
    )
    def generate_response(
        self,
        image: Union[str, Image.Image],
        prompt: str,
        max_new_tokens: int = 512
    ) -> str:
        """
        Generate a text response for an image and prompt.
        
        Args:
            image: PIL Image or path to image file
            prompt: Text prompt for the vision model
            max_new_tokens: Maximum tokens to generate
            
        Returns:
            Generated text response
        """
        # Ensure model is loaded
        if self.model is None:
            self._load_model()
        
        # Load image if path provided
        if isinstance(image, str):
            image = load_image(image)
            if image is None:
                raise ValueError(f"Failed to load image: {image}")
        
        # Resize for optimal processing
        image = resize_image_for_vision_model(image, max_size=1024)
        
        try:
            # Prepare inputs
            inputs = self.processor(
                text=prompt,
                images=image,
                return_tensors="pt"
            ).to(self.device)
            
            # Generate response
            with torch.no_grad():
                output = self.model.generate(
                    **inputs,
                    max_new_tokens=max_new_tokens,
                    do_sample=False,
                    temperature=0.7
                )
            
            # Decode response
            response = self.processor.decode(output[0], skip_special_tokens=True)
            
            # Clean up response (remove prompt echo if present)
            if prompt in response:
                response = response.replace(prompt, "").strip()
            
            return response
            
        except Exception as e:
            log_error(f"Error generating vision response: {e}")
            raise
    
    def generate_caption(
        self,
        image: Union[str, Image.Image],
        prompt_type: str = "caption"
    ) -> ImageCaption:
        """
        Generate a descriptive caption for an image.
        
        Args:
            image: PIL Image or path to image file
            prompt_type: Type of caption prompt to use
            
        Returns:
            ImageCaption object with generated caption
        """
        from config.vision_prompts import get_prompt
        
        try:
            prompt = get_prompt(prompt_type)
            response = self.generate_response(image, prompt, max_new_tokens=256)
            
            caption = ImageCaption(
                caption=response,
                confidence=1.0,  # Could be enhanced with actual confidence scores
                model_used=self.model_name
            )
            
            return caption
            
        except Exception as e:
            log_error(f"Failed to generate caption: {e}")
            raise
    
    def assess_quality(
        self,
        image: Union[str, Image.Image]
    ) -> QualityScore:
        """
        Assess the quality of an image.
        
        Args:
            image: PIL Image or path to image file
            
        Returns:
            QualityScore object with quality metrics
        """
        from config.vision_prompts import get_prompt
        
        try:
            prompt = get_prompt("quality")
            response = self.generate_response(image, prompt, max_new_tokens=512)
            
            # Parse scores from response
            parsed = parse_quality_scores(response)
            
            quality_score = QualityScore(
                overall_quality=parsed.get("overall_quality", 0.0),
                sharpness=parsed.get("overall_quality", 0.0),  # Approximation
                clarity=parsed.get("overall_quality", 0.0),  # Approximation
                composition=parsed.get("composition", 0.0),
                lighting=parsed.get("lighting", 0.0),
                subject_clarity=parsed.get("subject_clarity", 0.0),
                artifacts_detected=parsed.get("artifacts_detected", False),
                reasoning=parsed.get("reasoning", "")
            )
            
            return quality_score
            
        except Exception as e:
            log_error(f"Failed to assess quality: {e}")
            raise
    
    def check_consistency(
        self,
        image1: Union[str, Image.Image],
        image2: Union[str, Image.Image]
    ) -> ConsistencyScore:
        """
        Check consistency between two consecutive images.
        
        Args:
            image1: First image (PIL Image or path)
            image2: Second image (PIL Image or path)
            
        Returns:
            ConsistencyScore object with consistency metrics
        """
        from config.vision_prompts import get_prompt
        
        try:
            # Load images if paths provided
            if isinstance(image1, str):
                image1 = load_image(image1)
            if isinstance(image2, str):
                image2 = load_image(image2)
            
            if image1 is None or image2 is None:
                raise ValueError("Failed to load one or both images")
            
            # For now, we'll analyze them separately and compare
            # True multi-image support depends on model capabilities
            prompt = get_prompt("consistency")
            
            # Concatenate images side by side for comparison
            width1, height1 = image1.size
            width2, height2 = image2.size
            max_height = max(height1, height2)
            
            # Resize to same height
            if height1 != max_height:
                image1 = image1.resize((int(width1 * max_height / height1), max_height))
            if height2 != max_height:
                image2 = image2.resize((int(width2 * max_height / height2), max_height))
            
            # Create combined image
            combined = Image.new('RGB', (image1.width + image2.width, max_height))
            combined.paste(image1, (0, 0))
            combined.paste(image2, (image1.width, 0))
            
            response = self.generate_response(combined, prompt, max_new_tokens=512)
            
            # Parse scores from response
            parsed = parse_consistency_scores(response)
            
            consistency_score = ConsistencyScore(
                character_consistency=parsed.get("character_consistency", 0.0),
                style_consistency=parsed.get("style_consistency", 0.0),
                lighting_consistency=parsed.get("lighting_consistency", 0.0),
                visual_continuity=parsed.get("visual_continuity", 0.0),
                inconsistencies=parsed.get("inconsistencies", []),
                reasoning=parsed.get("reasoning", "")
            )
            
            return consistency_score
            
        except Exception as e:
            log_error(f"Failed to check consistency: {e}")
            raise
    
    def validate_image(
        self,
        image_path: str,
        check_quality: bool = True,
        quality_threshold: float = 6.0
    ) -> VisionAnalysisResult:
        """
        Perform comprehensive validation on a single image.
        
        Args:
            image_path: Path to image file
            check_quality: Whether to perform quality assessment
            quality_threshold: Minimum quality score (0-10) to pass validation
            
        Returns:
            VisionAnalysisResult object
        """
        result = VisionAnalysisResult(image_path=image_path)
        
        try:
            # Generate caption
            caption = self.generate_caption(image_path)
            result.caption = caption
            
            # Assess quality if requested
            if check_quality:
                quality = self.assess_quality(image_path)
                result.quality_score = quality
                
                # Check if quality meets threshold
                avg_quality = quality.average_score()
                if avg_quality < quality_threshold:
                    result.add_warning(
                        f"Quality score {avg_quality:.1f} below threshold {quality_threshold}"
                    )
                
                if quality.artifacts_detected:
                    result.add_warning("Artifacts detected in image")
            
        except Exception as e:
            result.add_error(f"Validation failed: {e}")
        
        return result
    
    def validate_storyboard(
        self,
        image_paths: List[str],
        check_consistency: bool = True,
        quality_threshold: float = 6.0,
        consistency_threshold: float = 6.0
    ) -> StoryboardValidation:
        """
        Validate an entire storyboard sequence.
        
        Args:
            image_paths: List of image file paths in sequence order
            check_consistency: Whether to check consistency between frames
            quality_threshold: Minimum quality score to pass
            consistency_threshold: Minimum consistency score to pass
            
        Returns:
            StoryboardValidation object
        """
        validation = StoryboardValidation(
            story_name=Path(image_paths[0]).parent.name if image_paths else "unknown",
            scene_count=len(image_paths)
        )
        
        log_info(f"Validating storyboard with {len(image_paths)} scenes")
        
        # Validate each image
        for i, image_path in enumerate(image_paths):
            log_info(f"Processing scene {i+1}/{len(image_paths)}: {Path(image_path).name}")
            
            result = self.validate_image(
                image_path,
                check_quality=True,
                quality_threshold=quality_threshold
            )
            
            # Check consistency with previous frame
            if check_consistency and i > 0:
                try:
                    consistency = self.check_consistency(
                        image_paths[i-1],
                        image_path
                    )
                    result.consistency_score = consistency
                    
                    avg_consistency = consistency.average_score()
                    if avg_consistency < consistency_threshold:
                        result.add_warning(
                            f"Consistency score {avg_consistency:.1f} below threshold {consistency_threshold}"
                        )
                except Exception as e:
                    result.add_error(f"Consistency check failed: {e}")
            
            validation.add_scene_analysis(result)
        
        # Generate recommendations
        if validation.overall_quality_avg < quality_threshold:
            validation.add_recommendation(
                f"Average quality {validation.overall_quality_avg:.1f} is below threshold. "
                "Consider regenerating low-quality frames."
            )
        
        if validation.overall_consistency_avg < consistency_threshold:
            validation.add_recommendation(
                f"Average consistency {validation.overall_consistency_avg:.1f} is below threshold. "
                "Check for visual discontinuities between scenes."
            )
        
        log_info(f"Storyboard validation complete. Passed: {validation.validation_passed}")
        
        return validation
    
    def cleanup(self):
        """Clean up model resources."""
        if self.model is not None:
            del self.model
            del self.processor
            self.model = None
            self.processor = None
            
            if torch.cuda.is_available():
                torch.cuda.empty_cache()
            
            log_info("Vision model resources cleaned up")


def main():
    """Example usage of GVision."""
    print("Vision Guidance Generator")
    print("=" * 60)
    
    # Check if transformers is available
    if not TRANSFORMERS_AVAILABLE:
        print("❌ transformers library not available")
        print("Install with: pip install transformers")
        return
    
    # Check GPU
    gpu_available, device_name = check_gpu_available()
    print(f"Device: {device_name}")
    
    # Initialize generator (without loading model by default)
    generator = GVision(model_name="phi-3.5-vision", load_model=False)
    
    print("\n✅ Vision guidance generator initialized")
    print("\nSupported models:")
    for name, model_id in GVision.SUPPORTED_MODELS.items():
        vram = estimate_vram_usage(name)
        print(f"  - {name}: {model_id} (VRAM: {vram})")
    
    print("\nNote: Model will be loaded on first use")
    print("For actual inference, ensure you have sufficient VRAM/RAM")


if __name__ == "__main__":
    main()
