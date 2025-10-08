"""
Keyframe data model for SDXL-generated images.

This module defines the Keyframe class for storing metadata about generated keyframes.
"""

from dataclasses import dataclass, asdict
from typing import Optional
import json


@dataclass
class Keyframe:
    """
    Represents a generated keyframe image with its metadata.
    
    Attributes:
        scene_id: Scene identifier
        image_path: Path to the generated image file
        prompt: Text prompt used for generation
        negative_prompt: Negative prompt used for generation
        seed: Random seed used for reproducibility
        width: Image width in pixels
        height: Image height in pixels
        steps: Number of inference steps used
        guidance_scale: Guidance scale parameter
        style_preset: Name of the style preset used
        generation_time: Time taken to generate in seconds
        quality_score: Optional quality score (e.g., from vision guidance)
        keyframe_index: Index of this keyframe within the scene
        timestamp: Timestamp in the video where this keyframe appears
        position: Normalized position (0.0-1.0) within the scene
        use_refiner: Whether the refiner model was used
        refiner_steps: Number of refiner steps (if used)
    """
    
    scene_id: int
    image_path: str
    prompt: str
    negative_prompt: str
    seed: int
    width: int
    height: int
    steps: int
    guidance_scale: float
    style_preset: str
    generation_time: float
    quality_score: Optional[float] = None
    keyframe_index: int = 0
    timestamp: float = 0.0
    position: float = 0.0
    use_refiner: bool = False
    refiner_steps: int = 0
    
    def to_dict(self) -> dict:
        """Convert keyframe to dictionary."""
        return asdict(self)
    
    def to_json(self) -> str:
        """Convert keyframe to JSON string."""
        return json.dumps(self.to_dict(), indent=2)
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Keyframe':
        """Create Keyframe from dictionary."""
        return cls(**data)
    
    @classmethod
    def from_json(cls, json_str: str) -> 'Keyframe':
        """Create Keyframe from JSON string."""
        data = json.loads(json_str)
        return cls.from_dict(data)
    
    def save_metadata(self, filepath: str) -> None:
        """
        Save keyframe metadata to a JSON file.
        
        Args:
            filepath: Path where to save the metadata JSON
        """
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(self.to_json())
    
    @classmethod
    def load_metadata(cls, filepath: str) -> 'Keyframe':
        """
        Load keyframe metadata from a JSON file.
        
        Args:
            filepath: Path to the metadata JSON file
            
        Returns:
            Keyframe object with loaded metadata
        """
        with open(filepath, 'r', encoding='utf-8') as f:
            return cls.from_json(f.read())
