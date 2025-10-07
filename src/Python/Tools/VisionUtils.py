"""
Utility functions for vision guidance operations.
Handles image loading, preprocessing, and caption validation.
"""

import os
import re
from typing import List, Tuple, Optional, Dict, Any
from pathlib import Path
from PIL import Image
import torch


def load_image(image_path: str) -> Optional[Image.Image]:
    """
    Load an image from file path.
    
    Args:
        image_path: Path to image file
        
    Returns:
        PIL Image or None if loading fails
    """
    try:
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image not found: {image_path}")
        
        image = Image.open(image_path)
        
        # Convert to RGB if necessary
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        return image
    except Exception as e:
        print(f"Error loading image {image_path}: {e}")
        return None


def load_images(image_paths: List[str]) -> List[Tuple[str, Image.Image]]:
    """
    Load multiple images from file paths.
    
    Args:
        image_paths: List of paths to image files
        
    Returns:
        List of tuples (path, image) for successfully loaded images
    """
    images = []
    for path in image_paths:
        img = load_image(path)
        if img is not None:
            images.append((path, img))
        else:
            print(f"⚠️ Skipping failed image: {path}")
    
    return images


def validate_image_dimensions(
    image: Image.Image, 
    min_width: int = 512, 
    min_height: int = 512,
    max_width: int = 4096,
    max_height: int = 4096
) -> Tuple[bool, str]:
    """
    Validate image dimensions are within acceptable range.
    
    Args:
        image: PIL Image
        min_width: Minimum acceptable width
        min_height: Minimum acceptable height
        max_width: Maximum acceptable width
        max_height: Maximum acceptable height
        
    Returns:
        Tuple of (is_valid, message)
    """
    width, height = image.size
    
    if width < min_width or height < min_height:
        return False, f"Image too small: {width}x{height} (min: {min_width}x{min_height})"
    
    if width > max_width or height > max_height:
        return False, f"Image too large: {width}x{height} (max: {max_width}x{max_height})"
    
    return True, f"Valid dimensions: {width}x{height}"


def resize_image_for_vision_model(
    image: Image.Image,
    max_size: int = 1024,
    maintain_aspect: bool = True
) -> Image.Image:
    """
    Resize image for optimal vision model processing.
    
    Args:
        image: PIL Image
        max_size: Maximum dimension (width or height)
        maintain_aspect: Whether to maintain aspect ratio
        
    Returns:
        Resized PIL Image
    """
    width, height = image.size
    
    # If image is already smaller than max_size, return as-is
    if width <= max_size and height <= max_size:
        return image
    
    if maintain_aspect:
        # Calculate new dimensions maintaining aspect ratio
        if width > height:
            new_width = max_size
            new_height = int(height * (max_size / width))
        else:
            new_height = max_size
            new_width = int(width * (max_size / height))
    else:
        new_width = max_size
        new_height = max_size
    
    return image.resize((new_width, new_height), Image.Resampling.LANCZOS)


def parse_quality_scores(response_text: str) -> Dict[str, Any]:
    """
    Parse quality scores from vision model response.
    
    Args:
        response_text: Text response from vision model
        
    Returns:
        Dictionary with parsed scores and information
    """
    result = {
        "overall_quality": 0.0,
        "composition": 0.0,
        "lighting": 0.0,
        "subject_clarity": 0.0,
        "artifacts_detected": False,
        "reasoning": ""
    }
    
    # Extract scores using regex
    patterns = {
        "overall_quality": r"Overall:\s*(\d+(?:\.\d+)?)",
        "composition": r"Composition:\s*(\d+(?:\.\d+)?)",
        "lighting": r"Lighting:\s*(\d+(?:\.\d+)?)",
        "subject_clarity": r"Subject:\s*(\d+(?:\.\d+)?)",
    }
    
    for key, pattern in patterns.items():
        match = re.search(pattern, response_text, re.IGNORECASE)
        if match:
            result[key] = float(match.group(1))
    
    # Check for artifacts
    artifacts_match = re.search(r"Artifacts:\s*(yes|no)", response_text, re.IGNORECASE)
    if artifacts_match:
        result["artifacts_detected"] = artifacts_match.group(1).lower() == "yes"
    
    # Extract reasoning
    reasoning_match = re.search(r"Reasoning:\s*(.+?)(?:\n|$)", response_text, re.IGNORECASE | re.DOTALL)
    if reasoning_match:
        result["reasoning"] = reasoning_match.group(1).strip()
    
    return result


def parse_consistency_scores(response_text: str) -> Dict[str, Any]:
    """
    Parse consistency scores from vision model response.
    
    Args:
        response_text: Text response from vision model
        
    Returns:
        Dictionary with parsed scores and information
    """
    result = {
        "character_consistency": 0.0,
        "style_consistency": 0.0,
        "lighting_consistency": 0.0,
        "visual_continuity": 0.0,
        "inconsistencies": [],
        "reasoning": ""
    }
    
    # Extract scores using regex
    patterns = {
        "character_consistency": r"Character:\s*(\d+(?:\.\d+)?)",
        "style_consistency": r"Style:\s*(\d+(?:\.\d+)?)",
        "lighting_consistency": r"Lighting:\s*(\d+(?:\.\d+)?)",
        "visual_continuity": r"Continuity:\s*(\d+(?:\.\d+)?)",
    }
    
    for key, pattern in patterns.items():
        match = re.search(pattern, response_text, re.IGNORECASE)
        if match:
            result[key] = float(match.group(1))
    
    # Extract inconsistencies
    inconsistencies_match = re.search(
        r"Inconsistencies:\s*(.+?)(?=Reasoning:|$)", 
        response_text, 
        re.IGNORECASE | re.DOTALL
    )
    if inconsistencies_match:
        inconsistencies_text = inconsistencies_match.group(1).strip()
        # Split by newlines or commas
        result["inconsistencies"] = [
            item.strip() 
            for item in re.split(r'[,\n]', inconsistencies_text)
            if item.strip() and not item.strip().lower() in ['none', 'n/a', 'na']
        ]
    
    # Extract reasoning
    reasoning_match = re.search(r"Reasoning:\s*(.+?)(?:\n|$)", response_text, re.IGNORECASE | re.DOTALL)
    if reasoning_match:
        result["reasoning"] = reasoning_match.group(1).strip()
    
    return result


def validate_caption_alignment(
    caption: str,
    expected_keywords: List[str],
    min_keyword_matches: int = 2
) -> Tuple[bool, List[str], List[str]]:
    """
    Validate that a caption aligns with expected content.
    
    Args:
        caption: Generated caption text
        expected_keywords: List of expected keywords/concepts
        min_keyword_matches: Minimum number of keyword matches required
        
    Returns:
        Tuple of (is_valid, matched_keywords, missing_keywords)
    """
    caption_lower = caption.lower()
    matched = []
    missing = []
    
    for keyword in expected_keywords:
        keyword_lower = keyword.lower()
        if keyword_lower in caption_lower:
            matched.append(keyword)
        else:
            missing.append(keyword)
    
    is_valid = len(matched) >= min_keyword_matches
    
    return is_valid, matched, missing


def calculate_image_quality_heuristics(image: Image.Image) -> Dict[str, float]:
    """
    Calculate simple heuristic quality metrics for an image.
    Provides basic quality indicators without ML models.
    
    Args:
        image: PIL Image
        
    Returns:
        Dictionary with quality metrics
    """
    import numpy as np
    
    # Convert to numpy array
    img_array = np.array(image)
    
    metrics = {}
    
    # Calculate sharpness (using Laplacian variance)
    try:
        from scipy import ndimage
        gray = np.mean(img_array, axis=2) if len(img_array.shape) == 3 else img_array
        laplacian = ndimage.laplace(gray)
        metrics["sharpness"] = float(np.var(laplacian))
    except ImportError:
        metrics["sharpness"] = 0.0
    
    # Calculate brightness
    metrics["brightness"] = float(np.mean(img_array))
    
    # Calculate contrast
    metrics["contrast"] = float(np.std(img_array))
    
    # Color diversity (for RGB images)
    if len(img_array.shape) == 3:
        metrics["color_diversity"] = float(np.std(img_array, axis=(0, 1)).mean())
    else:
        metrics["color_diversity"] = 0.0
    
    return metrics


def find_keyframe_images(
    story_folder: str,
    keyframe_pattern: str = "*.jpg"
) -> List[str]:
    """
    Find all keyframe images in a story folder.
    
    Args:
        story_folder: Path to story folder
        keyframe_pattern: Glob pattern for keyframe files
        
    Returns:
        List of image file paths
    """
    folder_path = Path(story_folder)
    
    if not folder_path.exists():
        return []
    
    # Look for images in common locations
    search_paths = [
        folder_path,
        folder_path / "keyframes",
        folder_path / "images",
        folder_path / "scenes"
    ]
    
    image_paths = []
    for search_path in search_paths:
        if search_path.exists():
            image_paths.extend([str(p) for p in search_path.glob(keyframe_pattern)])
            image_paths.extend([str(p) for p in search_path.glob("*.png")])
    
    # Remove duplicates and sort
    image_paths = sorted(list(set(image_paths)))
    
    return image_paths


def check_gpu_available() -> Tuple[bool, str]:
    """
    Check if GPU is available for vision model inference.
    
    Returns:
        Tuple of (is_available, device_name)
    """
    if torch.cuda.is_available():
        device_name = torch.cuda.get_device_name(0)
        return True, device_name
    else:
        return False, "CPU"


def estimate_vram_usage(model_name: str) -> str:
    """
    Estimate VRAM usage for different vision models.
    
    Args:
        model_name: Name of the vision model
        
    Returns:
        Estimated VRAM usage as string
    """
    vram_estimates = {
        "llava-onevision": "~14GB",
        "phi-3.5-vision": "~8GB",
        "llava-v1.5-7b": "~14GB",
        "llava-v1.5-13b": "~26GB",
    }
    
    model_lower = model_name.lower()
    for key, vram in vram_estimates.items():
        if key in model_lower:
            return vram
    
    return "Unknown"
