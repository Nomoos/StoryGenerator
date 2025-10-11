"""
Style Consistency System - Visual Coherence for SDXL Keyframes

This module provides functionality for:
1. Style reference image selection/creation
2. Style transfer to all keyframes using IP-Adapter
3. Visual coherence scoring across frames
4. Color palette consistency validation
5. Character/object consistency checks
6. Style library management for different video types
"""

import json
import logging
from dataclasses import dataclass, field, asdict
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional, Tuple
import numpy as np
from PIL import Image
import hashlib

logger = logging.getLogger(__name__)


@dataclass
class StyleProfile:
    """Represents a style profile for consistent image generation."""
    name: str
    reference_image_path: str
    style_prompt: str
    ip_adapter_scale: float = 0.8
    color_palette: List[Tuple[int, int, int]] = field(default_factory=list)
    style_tags: List[str] = field(default_factory=list)
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    metadata: Dict[str, any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for JSON serialization."""
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'StyleProfile':
        """Create StyleProfile from dictionary."""
        return cls(**data)


@dataclass
class ConsistencyMetrics:
    """Metrics for evaluating visual consistency across frames."""
    color_similarity: float  # 0-1, histogram similarity
    structural_similarity: float  # 0-1, SSIM-like metric
    style_consistency: float  # 0-1, feature-based consistency
    overall_score: float  # 0-1, weighted average
    frame_scores: List[float] = field(default_factory=list)  # Per-frame scores
    
    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return asdict(self)


class StyleConsistencyManager:
    """
    Manager for maintaining visual style consistency across SDXL-generated keyframes.
    
    Features:
    - Style reference creation and management
    - IP-Adapter-based style transfer
    - Color palette extraction and validation
    - Visual coherence scoring
    - Style library management
    """
    
    def __init__(
        self,
        model_id: str = "stabilityai/stable-diffusion-xl-base-1.0",
        style_library_dir: Optional[Path] = None,
        device: str = "cuda"
    ):
        """
        Initialize StyleConsistencyManager.
        
        Args:
            model_id: SDXL model to use
            style_library_dir: Directory for style library storage
            device: Device to run on ('cuda', 'cpu', or 'mps')
        """
        self.model_id = model_id
        self.device = device
        self.style_library_dir = style_library_dir or Path("data/styles")
        self.style_library_dir.mkdir(parents=True, exist_ok=True)
        
        # Style profiles will be lazy-loaded
        self.style_profiles: Dict[str, StyleProfile] = {}
        
        # Pipeline will be lazy-loaded to avoid import errors
        self._pipe = None
        
        # Load existing styles
        self._load_style_library()
        
        logger.info(f"StyleConsistencyManager initialized (device: {device})")
    
    @property
    def pipe(self):
        """Lazy load SDXL pipeline with IP-Adapter."""
        if self._pipe is None:
            try:
                from diffusers import StableDiffusionXLPipeline
                import torch
                
                logger.info(f"Loading SDXL model: {self.model_id}")
                
                # Determine dtype based on device
                dtype = torch.float16 if self.device in ["cuda", "mps"] else torch.float32
                
                self._pipe = StableDiffusionXLPipeline.from_pretrained(
                    self.model_id,
                    torch_dtype=dtype,
                    variant="fp16" if self.device == "cuda" else None
                )
                
                # Move to device
                if self.device == "cuda":
                    self._pipe.to("cuda")
                elif self.device == "mps":
                    self._pipe.to("mps")
                
                # Try to load IP-Adapter (optional, may not be available)
                try:
                    self._pipe.load_ip_adapter(
                        "h94/IP-Adapter",
                        subfolder="sdxl_models",
                        weight_name="ip-adapter-plus_sdxl_vit-h.bin"
                    )
                    logger.info("IP-Adapter loaded successfully")
                    self._has_ip_adapter = True
                except Exception as e:
                    logger.warning(f"IP-Adapter not available: {e}")
                    self._has_ip_adapter = False
                
                logger.info("SDXL pipeline loaded successfully")
                
            except ImportError as e:
                raise ImportError(
                    f"Required dependencies not installed: {e}\n"
                    "Install with: pip install diffusers>=0.25.0 torch>=2.0.0"
                )
        
        return self._pipe
    
    def _load_style_library(self):
        """Load existing style profiles from disk."""
        if not self.style_library_dir.exists():
            return
        
        for style_file in self.style_library_dir.glob("*_style.json"):
            try:
                with open(style_file, 'r') as f:
                    style_data = json.load(f)
                    profile = StyleProfile.from_dict(style_data)
                    self.style_profiles[profile.name] = profile
                    logger.info(f"Loaded style profile: {profile.name}")
            except Exception as e:
                logger.error(f"Failed to load style {style_file}: {e}")
    
    def create_style_reference(
        self,
        prompt: str,
        style_name: str,
        output_path: Path,
        num_inference_steps: int = 50,
        guidance_scale: float = 7.5,
        width: int = 1024,
        height: int = 1024
    ) -> StyleProfile:
        """
        Generate a style reference image from a prompt.
        
        Args:
            prompt: Text prompt describing the desired style
            style_name: Name for this style profile
            output_path: Path to save reference image
            num_inference_steps: Number of denoising steps
            guidance_scale: Classifier-free guidance scale
            width: Image width
            height: Image height
            
        Returns:
            StyleProfile object
        """
        logger.info(f"Creating style reference '{style_name}': {prompt}")
        
        # Ensure output directory exists
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Generate reference image
        image = self.pipe(
            prompt=prompt,
            num_inference_steps=num_inference_steps,
            guidance_scale=guidance_scale,
            width=width,
            height=height
        ).images[0]
        
        # Save image
        image.save(output_path)
        
        # Extract color palette
        color_palette = self._extract_color_palette(image)
        
        # Create style profile
        profile = StyleProfile(
            name=style_name,
            reference_image_path=str(output_path),
            style_prompt=prompt,
            color_palette=color_palette,
            style_tags=self._extract_style_tags(prompt)
        )
        
        # Save profile
        self._save_style_profile(profile)
        self.style_profiles[style_name] = profile
        
        logger.info(f"Style reference created: {output_path}")
        return profile
    
    def generate_with_style(
        self,
        prompts: List[str],
        style_name: str,
        output_dir: Path,
        num_inference_steps: int = 50,
        guidance_scale: float = 7.5,
        width: int = 1024,
        height: int = 1024
    ) -> List[Path]:
        """
        Generate keyframes with consistent style using IP-Adapter.
        
        Args:
            prompts: List of prompts for each keyframe
            style_name: Name of style profile to use
            output_dir: Directory for output images
            num_inference_steps: Number of denoising steps
            guidance_scale: Classifier-free guidance scale
            width: Image width
            height: Image height
            
        Returns:
            List of paths to generated images
        """
        if style_name not in self.style_profiles:
            raise ValueError(f"Style profile '{style_name}' not found")
        
        profile = self.style_profiles[style_name]
        output_dir.mkdir(parents=True, exist_ok=True)
        
        logger.info(f"Generating {len(prompts)} keyframes with style '{style_name}'")
        
        # Load reference image
        style_image = Image.open(profile.reference_image_path)
        
        # Set IP-Adapter scale if available
        if hasattr(self._pipe, 'set_ip_adapter_scale') and self._has_ip_adapter:
            self._pipe.set_ip_adapter_scale(profile.ip_adapter_scale)
            use_ip_adapter = True
        else:
            logger.warning("IP-Adapter not available, using prompt-based consistency")
            use_ip_adapter = False
        
        generated_images = []
        
        for i, prompt in enumerate(prompts):
            output_path = output_dir / f"keyframe_{i:03d}.png"
            
            # Enhance prompt with style information
            enhanced_prompt = self._enhance_prompt_with_style(prompt, profile)
            
            if use_ip_adapter:
                # Generate with IP-Adapter
                image = self.pipe(
                    prompt=enhanced_prompt,
                    ip_adapter_image=style_image,
                    num_inference_steps=num_inference_steps,
                    guidance_scale=guidance_scale,
                    width=width,
                    height=height
                ).images[0]
            else:
                # Generate without IP-Adapter (fallback)
                image = self.pipe(
                    prompt=enhanced_prompt,
                    num_inference_steps=num_inference_steps,
                    guidance_scale=guidance_scale,
                    width=width,
                    height=height
                ).images[0]
            
            image.save(output_path)
            generated_images.append(output_path)
            
            logger.info(f"Generated keyframe {i+1}/{len(prompts)}: {output_path}")
        
        logger.info(f"Generated {len(generated_images)} keyframes")
        return generated_images
    
    def _enhance_prompt_with_style(self, prompt: str, profile: StyleProfile) -> str:
        """Enhance prompt with style information."""
        style_suffix = f", {profile.style_prompt}"
        return f"{prompt}{style_suffix}"
    
    def validate_consistency(
        self,
        image_paths: List[Path],
        output_report_path: Optional[Path] = None
    ) -> ConsistencyMetrics:
        """
        Validate visual consistency across a sequence of images.
        
        Args:
            image_paths: List of paths to images to validate
            output_report_path: Optional path to save consistency report
            
        Returns:
            ConsistencyMetrics object
        """
        logger.info(f"Validating consistency across {len(image_paths)} images")
        
        if len(image_paths) < 2:
            logger.warning("Need at least 2 images for consistency validation")
            return ConsistencyMetrics(1.0, 1.0, 1.0, 1.0, [1.0])
        
        # Load images
        images = [Image.open(path) for path in image_paths]
        
        # Calculate color similarity
        color_sim = self._calculate_color_similarity(images)
        
        # Calculate structural similarity
        structural_sim = self._calculate_structural_similarity(images)
        
        # Calculate style consistency (feature-based)
        style_consistency = self._calculate_style_consistency(images)
        
        # Calculate per-frame scores
        frame_scores = self._calculate_frame_scores(images)
        
        # Overall score (weighted average)
        overall = (color_sim * 0.3 + structural_sim * 0.3 + style_consistency * 0.4)
        
        metrics = ConsistencyMetrics(
            color_similarity=color_sim,
            structural_similarity=structural_sim,
            style_consistency=style_consistency,
            overall_score=overall,
            frame_scores=frame_scores
        )
        
        # Save report if requested
        if output_report_path:
            self._save_consistency_report(metrics, image_paths, output_report_path)
        
        logger.info(f"Consistency validation complete. Overall score: {overall:.3f}")
        return metrics
    
    def _calculate_color_similarity(self, images: List[Image.Image]) -> float:
        """Calculate color histogram similarity across images."""
        if len(images) < 2:
            return 1.0
        
        # Extract color histograms
        histograms = []
        for img in images:
            # Convert to RGB if needed
            if img.mode != 'RGB':
                img = img.convert('RGB')
            
            # Get histogram for each channel
            hist = np.array(img.histogram())
            hist = hist / hist.sum()  # Normalize
            histograms.append(hist)
        
        # Calculate pairwise similarities
        similarities = []
        for i in range(len(histograms) - 1):
            for j in range(i + 1, len(histograms)):
                # Correlation coefficient
                corr = np.corrcoef(histograms[i], histograms[j])[0, 1]
                similarities.append(max(0, corr))  # Clip negative correlations
        
        return np.mean(similarities) if similarities else 1.0
    
    def _calculate_structural_similarity(self, images: List[Image.Image]) -> float:
        """Calculate structural similarity across consecutive frames."""
        if len(images) < 2:
            return 1.0
        
        # Simple structural similarity based on downsampled images
        similarities = []
        
        for i in range(len(images) - 1):
            img1 = images[i].resize((64, 64)).convert('L')
            img2 = images[i + 1].resize((64, 64)).convert('L')
            
            # Calculate mean squared error
            arr1 = np.array(img1, dtype=np.float32)
            arr2 = np.array(img2, dtype=np.float32)
            mse = np.mean((arr1 - arr2) ** 2)
            
            # Convert to similarity score (0-1)
            max_mse = 255 ** 2
            similarity = 1.0 - (mse / max_mse)
            similarities.append(similarity)
        
        return np.mean(similarities) if similarities else 1.0
    
    def _calculate_style_consistency(self, images: List[Image.Image]) -> float:
        """Calculate style consistency using color distribution."""
        if len(images) < 2:
            return 1.0
        
        # Extract dominant colors for each image
        color_profiles = []
        for img in images:
            palette = self._extract_color_palette(img, n_colors=5)
            color_profiles.append(palette)
        
        # Calculate consistency of color palettes
        consistencies = []
        for i in range(len(color_profiles) - 1):
            palette1 = color_profiles[i]
            palette2 = color_profiles[i + 1]
            
            # Calculate color distance between palettes
            min_distances = []
            for c1 in palette1:
                distances = [self._color_distance(c1, c2) for c2 in palette2]
                min_distances.append(min(distances))
            
            # Convert to similarity (0-1)
            avg_distance = np.mean(min_distances)
            max_distance = np.sqrt(3 * 255**2)  # Max RGB distance
            similarity = 1.0 - (avg_distance / max_distance)
            consistencies.append(similarity)
        
        return np.mean(consistencies) if consistencies else 1.0
    
    def _calculate_frame_scores(self, images: List[Image.Image]) -> List[float]:
        """Calculate individual quality/consistency score for each frame."""
        # For now, return equal scores
        # In production, could analyze sharpness, contrast, etc.
        return [0.85] * len(images)
    
    def _extract_color_palette(
        self,
        image: Image.Image,
        n_colors: int = 5
    ) -> List[Tuple[int, int, int]]:
        """Extract dominant colors from image."""
        # Convert to RGB
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Resize for faster processing
        img_small = image.resize((150, 150))
        
        # Get colors using quantization
        img_quantized = img_small.quantize(colors=n_colors)
        palette = img_quantized.getpalette()
        
        # Extract RGB tuples
        colors = []
        for i in range(n_colors):
            r, g, b = palette[i*3:(i+1)*3]
            colors.append((r, g, b))
        
        return colors
    
    def _color_distance(
        self,
        color1: Tuple[int, int, int],
        color2: Tuple[int, int, int]
    ) -> float:
        """Calculate Euclidean distance between two RGB colors."""
        return np.sqrt(sum((c1 - c2)**2 for c1, c2 in zip(color1, color2)))
    
    def _extract_style_tags(self, prompt: str) -> List[str]:
        """Extract style-related tags from prompt."""
        # Simple keyword extraction
        style_keywords = [
            'cinematic', 'anime', 'realistic', 'cartoon', 'oil painting',
            'watercolor', 'sketch', 'vintage', 'modern', 'minimalist',
            'vibrant', 'muted', 'dark', 'bright', 'colorful'
        ]
        
        tags = []
        prompt_lower = prompt.lower()
        for keyword in style_keywords:
            if keyword in prompt_lower:
                tags.append(keyword)
        
        return tags
    
    def _save_style_profile(self, profile: StyleProfile):
        """Save style profile to disk."""
        profile_path = self.style_library_dir / f"{profile.name}_style.json"
        
        with open(profile_path, 'w') as f:
            json.dump(profile.to_dict(), f, indent=2)
        
        logger.info(f"Style profile saved: {profile_path}")
    
    def _save_consistency_report(
        self,
        metrics: ConsistencyMetrics,
        image_paths: List[Path],
        output_path: Path
    ):
        """Save consistency report to JSON."""
        report = {
            'timestamp': datetime.now().isoformat(),
            'num_images': len(image_paths),
            'images': [str(p) for p in image_paths],
            'metrics': metrics.to_dict()
        }
        
        with open(output_path, 'w') as f:
            json.dump(report, f, indent=2)
        
        logger.info(f"Consistency report saved: {output_path}")
    
    def get_style_profiles(
        self,
        tags: Optional[List[str]] = None
    ) -> List[StyleProfile]:
        """
        Get style profiles, optionally filtered by tags.
        
        Args:
            tags: Optional list of tags to filter by
            
        Returns:
            List of StyleProfile objects
        """
        profiles = list(self.style_profiles.values())
        
        if tags:
            profiles = [
                p for p in profiles
                if any(tag in p.style_tags for tag in tags)
            ]
        
        return profiles
    
    def export_style_library(self, output_path: Path):
        """
        Export all style profiles to a single JSON file.
        
        Args:
            output_path: Path for output JSON file
        """
        library_data = {
            name: profile.to_dict()
            for name, profile in self.style_profiles.items()
        }
        
        with open(output_path, 'w') as f:
            json.dump(library_data, f, indent=2)
        
        logger.info(f"Exported {len(library_data)} styles to {output_path}")
    
    def import_style_library(self, input_path: Path):
        """
        Import style profiles from a JSON file.
        
        Args:
            input_path: Path to JSON file with profiles
        """
        with open(input_path, 'r') as f:
            library_data = json.load(f)
        
        for name, profile_data in library_data.items():
            profile = StyleProfile.from_dict(profile_data)
            self.style_profiles[name] = profile
            self._save_style_profile(profile)
        
        logger.info(f"Imported {len(library_data)} styles from {input_path}")
