import os
from typing import List, Optional, Dict, Any
from dataclasses import dataclass
import json


@dataclass
class Scene:
    """Represents a single scene in a video."""
    text: str
    duration: float
    image_path: Optional[str] = None
    transition: str = "fade"
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'text': self.text,
            'duration': self.duration,
            'image_path': self.image_path,
            'transition': self.transition
        }


class SceneComposer:
    """
    Manages scenes for video composition.
    Handles scene creation, transitions, and composition planning.
    """
    
    def __init__(self):
        self.scenes: List[Scene] = []
    
    def add_scene(self, 
                  text: str,
                  duration: float,
                  image_path: Optional[str] = None,
                  transition: str = "fade") -> None:
        """
        Add a scene to the composition.
        
        Args:
            text: Text content for the scene
            duration: Duration of the scene in seconds
            image_path: Optional path to image for this scene
            transition: Transition effect (fade, cut, etc.)
        """
        scene = Scene(text=text, duration=duration, image_path=image_path, transition=transition)
        self.scenes.append(scene)
        print(f"✅ Added scene: {text[:50]}... ({duration}s)")
    
    def clear_scenes(self) -> None:
        """Clear all scenes from the composition."""
        self.scenes.clear()
        print("🗑️ Cleared all scenes")
    
    def get_total_duration(self) -> float:
        """
        Calculate total duration of all scenes.
        
        Returns:
            Total duration in seconds
        """
        return sum(scene.duration for scene in self.scenes)
    
    def get_scene_count(self) -> int:
        """
        Get the number of scenes.
        
        Returns:
            Number of scenes
        """
        return len(self.scenes)
    
    def save_composition(self, output_path: str) -> bool:
        """
        Save the scene composition to a JSON file.
        
        Args:
            output_path: Path to save the composition file
            
        Returns:
            True if successful, False otherwise
        """
        try:
            composition_data = {
                'total_duration': self.get_total_duration(),
                'scene_count': self.get_scene_count(),
                'scenes': [scene.to_dict() for scene in self.scenes]
            }
            
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(composition_data, f, indent=2, ensure_ascii=False)
            
            print(f"✅ Saved composition to: {output_path}")
            return True
        except Exception as e:
            print(f"❌ Failed to save composition: {e}")
            return False
    
    def load_composition(self, input_path: str) -> bool:
        """
        Load a scene composition from a JSON file.
        
        Args:
            input_path: Path to the composition file
            
        Returns:
            True if successful, False otherwise
        """
        if not os.path.exists(input_path):
            print(f"❌ Composition file not found: {input_path}")
            return False
        
        try:
            with open(input_path, 'r', encoding='utf-8') as f:
                composition_data = json.load(f)
            
            self.clear_scenes()
            
            for scene_data in composition_data.get('scenes', []):
                self.add_scene(
                    text=scene_data['text'],
                    duration=scene_data['duration'],
                    image_path=scene_data.get('image_path'),
                    transition=scene_data.get('transition', 'fade')
                )
            
            print(f"✅ Loaded composition from: {input_path}")
            print(f"📊 Total duration: {self.get_total_duration():.2f}s, Scenes: {self.get_scene_count()}")
            return True
        except Exception as e:
            print(f"❌ Failed to load composition: {e}")
            return False
    
    def split_text_into_scenes(self, 
                               text: str,
                               total_duration: float,
                               sentences_per_scene: int = 2) -> None:
        """
        Automatically split text into scenes based on sentences.
        
        Args:
            text: Full text to split
            total_duration: Total duration to distribute across scenes
            sentences_per_scene: Number of sentences per scene
        """
        # Simple sentence splitting (can be improved with NLP)
        sentences = [s.strip() for s in text.replace('!', '.').replace('?', '.').split('.') if s.strip()]
        
        # Group sentences into scenes
        scene_texts = []
        for i in range(0, len(sentences), sentences_per_scene):
            scene_text = '. '.join(sentences[i:i+sentences_per_scene]) + '.'
            scene_texts.append(scene_text)
        
        # Calculate duration per scene
        if scene_texts:
            duration_per_scene = total_duration / len(scene_texts)
            
            self.clear_scenes()
            for scene_text in scene_texts:
                self.add_scene(scene_text, duration_per_scene)
            
            print(f"✅ Split text into {len(scene_texts)} scenes")
    
    def generate_scene_plan(self, output_dir: str) -> Dict[str, Any]:
        """
        Generate a plan for scene images that need to be created.
        
        Args:
            output_dir: Directory where scene images will be stored
            
        Returns:
            Dictionary with scene plan information
        """
        plan = {
            'scenes': [],
            'total_scenes': self.get_scene_count(),
            'total_duration': self.get_total_duration(),
            'output_dir': output_dir
        }
        
        for i, scene in enumerate(self.scenes):
            scene_info = {
                'scene_number': i + 1,
                'text': scene.text,
                'duration': scene.duration,
                'image_path': scene.image_path or os.path.join(output_dir, f"scene_{i+1:03d}.jpg"),
                'needs_generation': scene.image_path is None or not os.path.exists(scene.image_path)
            }
            plan['scenes'].append(scene_info)
        
        return plan
    
    def validate_scenes(self) -> bool:
        """
        Validate that all scenes have valid images or can use fallback.
        
        Returns:
            True if all scenes are valid, False otherwise
        """
        if not self.scenes:
            print("⚠️ No scenes to validate")
            return False
        
        missing_images = []
        for i, scene in enumerate(self.scenes):
            if scene.image_path and not os.path.exists(scene.image_path):
                missing_images.append(f"Scene {i+1}: {scene.image_path}")
        
        if missing_images:
            print(f"⚠️ {len(missing_images)} scenes have missing images (will use fallback):")
            for missing in missing_images[:5]:  # Show first 5
                print(f"  - {missing}")
            if len(missing_images) > 5:
                print(f"  ... and {len(missing_images) - 5} more")
            return True  # Still valid, just uses fallback
        
        print(f"✅ All {len(self.scenes)} scenes validated")
        return True
