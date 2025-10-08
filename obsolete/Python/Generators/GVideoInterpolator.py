import os
import cv2
import numpy as np
from typing import List, Tuple
from PIL import Image
from Models.StoryIdea import StoryIdea
from Generators.GSceneAnalyzer import Scene, SceneAnalyzer
from Tools.Utils import TITLES_PATH, sanitize_filename


class VideoInterpolator:
    """
    Creates smooth video transitions between keyframe images.
    Uses frame interpolation techniques to create fluid motion.
    """

    def __init__(self, target_fps: int = 30):
        """
        Initialize video interpolator
        
        Args:
            target_fps: Target frames per second for output video
        """
        self.target_fps = target_fps
        self.analyzer = SceneAnalyzer()

    def interpolate_scenes(self, story_idea: StoryIdea) -> str:
        """
        Create interpolated video segments for all scenes
        
        Args:
            story_idea: StoryIdea object for the story
            
        Returns:
            Path to directory containing video segments
        """
        # Load scenes with keyframes
        scenes = self.analyzer.load_scenes(story_idea)
        
        folder_path = os.path.join(TITLES_PATH, sanitize_filename(story_idea.story_title))
        videos_dir = os.path.join(folder_path, "video_segments")
        os.makedirs(videos_dir, exist_ok=True)
        
        print(f"🎬 Interpolating videos for {len(scenes)} scenes...")
        
        for scene in scenes:
            if not scene.keyframes or len(scene.keyframes) < 2:
                print(f"⚠️ Scene {scene.scene_id} has insufficient keyframes. Skipping...")
                continue
            
            print(f"  Scene {scene.scene_id}/{len(scenes)}: Creating video segment...")
            
            video_path = self._create_scene_video(
                scene=scene,
                output_dir=videos_dir
            )
            
            if video_path:
                print(f"    ✅ Created: {os.path.basename(video_path)}")
        
        print(f"✅ Created all video segments in '{videos_dir}'")
        return videos_dir

    def _create_scene_video(self, scene: Scene, output_dir: str) -> str:
        """
        Create a video segment for a single scene by interpolating between keyframes
        
        Args:
            scene: Scene object with keyframe paths
            output_dir: Directory to save video segment
            
        Returns:
            Path to created video file
        """
        output_path = os.path.join(output_dir, f"scene_{scene.scene_id:03d}.mp4")
        
        # Skip if already exists
        if os.path.exists(output_path):
            print(f"    ⏭️  Video segment already exists")
            return output_path
        
        # Calculate total frames needed
        total_frames = int(scene.duration * self.target_fps)
        
        # Load keyframe images
        keyframe_images = []
        for kf_path in scene.keyframes:
            if not os.path.exists(kf_path):
                print(f"    ⚠️ Keyframe not found: {kf_path}")
                continue
            img = cv2.imread(kf_path)
            if img is not None:
                keyframe_images.append(img)
        
        if len(keyframe_images) < 2:
            print(f"    ❌ Insufficient valid keyframes")
            return None
        
        # Setup video writer
        height, width = keyframe_images[0].shape[:2]
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(output_path, fourcc, self.target_fps, (width, height))
        
        # Distribute frames among keyframe pairs
        num_keyframes = len(keyframe_images)
        frames_per_segment = total_frames // (num_keyframes - 1)
        
        # Interpolate between each pair of keyframes
        for i in range(num_keyframes - 1):
            img1 = keyframe_images[i]
            img2 = keyframe_images[i + 1]
            
            # Calculate frames for this segment
            if i == num_keyframes - 2:
                # Last segment gets remaining frames
                segment_frames = total_frames - (i * frames_per_segment)
            else:
                segment_frames = frames_per_segment
            
            # Generate interpolated frames
            interpolated = self._interpolate_frames(img1, img2, segment_frames)
            
            # Write frames to video
            for frame in interpolated:
                out.write(frame)
        
        out.release()
        return output_path

    def _interpolate_frames(
        self,
        img1: np.ndarray,
        img2: np.ndarray,
        num_frames: int
    ) -> List[np.ndarray]:
        """
        Interpolate frames between two images using various techniques
        
        Args:
            img1: First keyframe image
            img2: Second keyframe image
            num_frames: Number of frames to generate (including endpoints)
            
        Returns:
            List of interpolated frame images
        """
        frames = []
        
        # Use different interpolation strategies based on number of frames
        if num_frames <= 2:
            # Just use the two keyframes
            return [img1, img2][:num_frames]
        
        # Linear blend interpolation with easing
        for i in range(num_frames):
            # Calculate blend factor with ease-in-out
            t = i / (num_frames - 1)
            t = self._ease_in_out(t)
            
            # Blend images
            blended = cv2.addWeighted(img1, 1 - t, img2, t, 0)
            
            # Optional: Add subtle motion blur for smoother feel
            if i > 0 and i < num_frames - 1:
                blended = self._add_motion_blur(blended, intensity=0.3)
            
            frames.append(blended)
        
        return frames

    def _ease_in_out(self, t: float) -> float:
        """
        Ease-in-out function for smoother interpolation
        
        Args:
            t: Input value between 0 and 1
            
        Returns:
            Eased value between 0 and 1
        """
        # Cubic ease-in-out
        if t < 0.5:
            return 4 * t * t * t
        else:
            p = 2 * t - 2
            return 1 + p * p * p / 2

    def _add_motion_blur(self, img: np.ndarray, intensity: float = 0.3) -> np.ndarray:
        """
        Add subtle motion blur to an image
        
        Args:
            img: Input image
            intensity: Blur intensity (0-1)
            
        Returns:
            Blurred image
        """
        kernel_size = max(3, int(5 * intensity))
        if kernel_size % 2 == 0:
            kernel_size += 1
        
        # Create horizontal motion blur kernel
        kernel = np.zeros((kernel_size, kernel_size))
        kernel[kernel_size // 2, :] = 1.0
        kernel = kernel / kernel_size
        
        # Apply blur
        blurred = cv2.filter2D(img, -1, kernel)
        
        # Blend with original
        result = cv2.addWeighted(img, 1 - intensity, blurred, intensity, 0)
        return result

    def create_latent_interpolation(
        self,
        img1: np.ndarray,
        img2: np.ndarray,
        num_frames: int,
        use_optical_flow: bool = False
    ) -> List[np.ndarray]:
        """
        Advanced interpolation using optical flow (optional future enhancement)
        
        Args:
            img1: First keyframe
            img2: Second keyframe
            num_frames: Number of frames to generate
            use_optical_flow: Whether to use optical flow (requires more computation)
            
        Returns:
            List of interpolated frames
        """
        if not use_optical_flow:
            # Fall back to simple interpolation
            return self._interpolate_frames(img1, img2, num_frames)
        
        # This is a placeholder for future optical flow implementation
        # Would use cv2.calcOpticalFlowFarneback or DIS optical flow
        # For now, use simple interpolation
        return self._interpolate_frames(img1, img2, num_frames)
