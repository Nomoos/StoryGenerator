"""
Image utility functions for keyframe processing.

This module provides utilities for image manipulation, scaling, and cropping
to ensure proper aspect ratios and resolutions for video generation.
"""

from PIL import Image
from typing import Tuple
import os


def scale_to_aspect_ratio(
    image: Image.Image,
    target_width: int,
    target_height: int,
    maintain_quality: bool = True
) -> Image.Image:
    """
    Scale image to target aspect ratio while maintaining quality.
    
    Args:
        image: PIL Image object
        target_width: Target width in pixels
        target_height: Target height in pixels
        maintain_quality: Use high-quality resampling
        
    Returns:
        Scaled PIL Image
    """
    target_ratio = target_width / target_height
    current_ratio = image.width / image.height
    
    # Determine scaling factor
    if current_ratio > target_ratio:
        # Image is wider than target, scale by height
        scale_factor = target_height / image.height
    else:
        # Image is taller than target, scale by width
        scale_factor = target_width / image.width
    
    new_width = int(image.width * scale_factor)
    new_height = int(image.height * scale_factor)
    
    resampling = Image.Resampling.LANCZOS if maintain_quality else Image.Resampling.BILINEAR
    
    return image.resize((new_width, new_height), resampling)


def crop_to_aspect_ratio(
    image: Image.Image,
    target_width: int,
    target_height: int,
    center_crop: bool = True
) -> Image.Image:
    """
    Crop image to exact target dimensions.
    
    Args:
        image: PIL Image object
        target_width: Target width in pixels
        target_height: Target height in pixels
        center_crop: Whether to crop from center (True) or top (False)
        
    Returns:
        Cropped PIL Image
    """
    if center_crop:
        # Center crop
        left = (image.width - target_width) // 2
        top = (image.height - target_height) // 2
    else:
        # Top crop (useful for portraits)
        left = (image.width - target_width) // 2
        top = 0
    
    right = left + target_width
    bottom = top + target_height
    
    return image.crop((left, top, right, bottom))


def scale_and_crop(
    image: Image.Image,
    target_width: int,
    target_height: int,
    center_crop: bool = True
) -> Image.Image:
    """
    Scale and crop image to exact target dimensions maintaining aspect ratio.
    
    This is the recommended method for preparing keyframes for video.
    
    Args:
        image: PIL Image object
        target_width: Target width in pixels
        target_height: Target height in pixels
        center_crop: Whether to crop from center (True) or top (False)
        
    Returns:
        Processed PIL Image with exact target dimensions
    """
    # First scale to maintain aspect ratio
    scaled = scale_to_aspect_ratio(image, target_width, target_height)
    
    # Then crop to exact dimensions
    if scaled.width != target_width or scaled.height != target_height:
        return crop_to_aspect_ratio(scaled, target_width, target_height, center_crop)
    
    return scaled


def resize_for_9_16(
    image: Image.Image,
    target_height: int = 1920,
    maintain_quality: bool = True
) -> Image.Image:
    """
    Resize image to 9:16 aspect ratio (vertical video format).
    
    Args:
        image: PIL Image object
        target_height: Target height (default 1920 for 1080x1920)
        maintain_quality: Use high-quality resampling
        
    Returns:
        Resized PIL Image in 9:16 format
    """
    target_width = int(target_height * 9 / 16)
    return scale_and_crop(image, target_width, target_height)


def save_image(
    image: Image.Image,
    filepath: str,
    format: str = "PNG",
    quality: int = 95
) -> str:
    """
    Save image to disk with specified format and quality.
    
    Args:
        image: PIL Image object
        filepath: Output file path
        format: Image format (PNG, JPEG, etc.)
        quality: JPEG quality (1-100, only used for JPEG)
        
    Returns:
        Path to saved image
    """
    # Ensure directory exists
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    
    if format.upper() == "JPEG" or format.upper() == "JPG":
        # Convert RGBA to RGB for JPEG
        if image.mode == "RGBA":
            rgb_image = Image.new("RGB", image.size, (255, 255, 255))
            rgb_image.paste(image, mask=image.split()[3])
            image = rgb_image
        image.save(filepath, format="JPEG", quality=quality)
    else:
        image.save(filepath, format=format)
    
    return filepath


def load_and_prepare_image(
    filepath: str,
    target_width: int = 1080,
    target_height: int = 1920
) -> Image.Image:
    """
    Load image and prepare it for video generation.
    
    Args:
        filepath: Path to image file
        target_width: Target width in pixels
        target_height: Target height in pixels
        
    Returns:
        Prepared PIL Image
    """
    image = Image.open(filepath)
    return scale_and_crop(image, target_width, target_height)


def get_image_info(filepath: str) -> dict:
    """
    Get basic information about an image file.
    
    Args:
        filepath: Path to image file
        
    Returns:
        Dictionary with image information
    """
    image = Image.open(filepath)
    
    return {
        "width": image.width,
        "height": image.height,
        "format": image.format,
        "mode": image.mode,
        "size_bytes": os.path.getsize(filepath),
        "aspect_ratio": image.width / image.height
    }
