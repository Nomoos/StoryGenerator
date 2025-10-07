"""
Custom Thumbnail Generator - Multiple timestamp selections and frame analysis.
"""

import os
import subprocess
from typing import List, Tuple, Optional
from PIL import Image
import numpy as np


class ThumbnailGenerator:
    """
    Advanced thumbnail generation with multiple options and frame selection.
    """
    
    def __init__(self, width: int = 1080, height: int = 1920):
        """
        Initialize thumbnail generator.
        
        Args:
            width: Thumbnail width (default: 1080)
            height: Thumbnail height (default: 1920)
        """
        self.width = width
        self.height = height
    
    def generate_at_timestamps(
        self,
        video_path: str,
        output_dir: str,
        timestamps: List[float],
        prefix: str = "thumb"
    ) -> List[str]:
        """
        Generate thumbnails at multiple timestamps.
        
        Args:
            video_path: Path to video file
            output_dir: Directory to save thumbnails
            timestamps: List of timestamps in seconds
            prefix: Prefix for thumbnail filenames
            
        Returns:
            List of generated thumbnail paths
        """
        if not os.path.exists(video_path):
            raise FileNotFoundError(f"Video not found: {video_path}")
        
        os.makedirs(output_dir, exist_ok=True)
        thumbnails = []
        
        print(f"📸 Generating {len(timestamps)} thumbnails...")
        
        for i, timestamp in enumerate(timestamps, 1):
            output_path = os.path.join(output_dir, f"{prefix}_{i:02d}_t{timestamp:.1f}s.jpg")
            
            try:
                cmd = [
                    'ffmpeg', '-y',
                    '-ss', str(timestamp),
                    '-i', video_path,
                    '-vframes', '1',
                    '-vf', f'scale={self.width}:{self.height}',
                    '-q:v', '2',
                    output_path
                ]
                
                subprocess.run(cmd, check=True, capture_output=True)
                thumbnails.append(output_path)
                print(f"  ✅ Generated thumbnail {i}/{len(timestamps)} at {timestamp}s")
                
            except subprocess.CalledProcessError as e:
                print(f"  ❌ Failed to generate thumbnail at {timestamp}s: {e}")
        
        return thumbnails
    
    def generate_grid(
        self,
        video_path: str,
        output_path: str,
        grid_size: Tuple[int, int] = (3, 3),
        start_time: float = 0.0,
        end_time: Optional[float] = None
    ) -> str:
        """
        Generate a grid of thumbnails from evenly spaced frames.
        
        Args:
            video_path: Path to video file
            output_path: Path to save grid image
            grid_size: Grid dimensions (rows, cols)
            start_time: Start time in seconds
            end_time: End time in seconds (None for video end)
            
        Returns:
            Path to generated grid image
        """
        if not os.path.exists(video_path):
            raise FileNotFoundError(f"Video not found: {video_path}")
        
        rows, cols = grid_size
        num_frames = rows * cols
        
        # Get video duration if end_time not specified
        if end_time is None:
            end_time = self._get_video_duration(video_path)
        
        # Calculate timestamps
        duration = end_time - start_time
        interval = duration / (num_frames + 1)
        timestamps = [start_time + interval * (i + 1) for i in range(num_frames)]
        
        print(f"📸 Generating {rows}x{cols} thumbnail grid...")
        
        # Generate individual thumbnails
        temp_dir = os.path.join(os.path.dirname(output_path), "temp_thumbs")
        thumbnails = self.generate_at_timestamps(video_path, temp_dir, timestamps, "grid")
        
        # Create grid
        try:
            grid_image = self._create_grid_image(thumbnails, rows, cols)
            grid_image.save(output_path, quality=95)
            print(f"✅ Grid saved to: {output_path}")
            
            # Clean up temp thumbnails
            for thumb in thumbnails:
                try:
                    os.remove(thumb)
                except:
                    pass
            try:
                os.rmdir(temp_dir)
            except:
                pass
            
            return output_path
            
        except Exception as e:
            print(f"❌ Error creating grid: {e}")
            raise
    
    def find_best_frame(
        self,
        video_path: str,
        output_path: str,
        num_candidates: int = 30,
        method: str = "brightness"
    ) -> str:
        """
        Find and extract the best frame from video using image analysis.
        
        Args:
            video_path: Path to video file
            output_path: Path to save best frame
            num_candidates: Number of frames to analyze
            method: Selection method ('brightness', 'sharpness', 'contrast')
            
        Returns:
            Path to best frame thumbnail
        """
        if not os.path.exists(video_path):
            raise FileNotFoundError(f"Video not found: {video_path}")
        
        print(f"🔍 Analyzing {num_candidates} frames to find best thumbnail...")
        
        # Get video duration
        duration = self._get_video_duration(video_path)
        
        # Generate candidate timestamps (avoid first and last 10%)
        start_time = duration * 0.1
        end_time = duration * 0.9
        interval = (end_time - start_time) / num_candidates
        timestamps = [start_time + interval * i for i in range(num_candidates)]
        
        # Generate candidate thumbnails
        temp_dir = os.path.join(os.path.dirname(output_path), "temp_candidates")
        candidates = self.generate_at_timestamps(video_path, temp_dir, timestamps, "candidate")
        
        # Analyze and select best frame
        best_frame = None
        best_score = -1
        
        for i, candidate in enumerate(candidates):
            try:
                score = self._analyze_frame(candidate, method)
                if score > best_score:
                    best_score = score
                    best_frame = candidate
            except Exception as e:
                print(f"  ⚠️ Error analyzing frame {i+1}: {e}")
        
        if best_frame is None:
            raise RuntimeError("Could not find suitable frame")
        
        # Copy best frame to output
        import shutil
        shutil.copy2(best_frame, output_path)
        
        print(f"✅ Best frame saved (score: {best_score:.2f}): {output_path}")
        
        # Clean up candidates
        for candidate in candidates:
            try:
                os.remove(candidate)
            except:
                pass
        try:
            os.rmdir(temp_dir)
        except:
            pass
        
        return output_path
    
    def generate_multiple_options(
        self,
        video_path: str,
        output_dir: str,
        title_id: str,
        num_options: int = 5
    ) -> List[str]:
        """
        Generate multiple thumbnail options for selection.
        
        Args:
            video_path: Path to video file
            output_dir: Directory to save thumbnails
            title_id: Title identifier for naming
            num_options: Number of options to generate
            
        Returns:
            List of generated thumbnail paths
        """
        os.makedirs(output_dir, exist_ok=True)
        
        # Get video duration
        duration = self._get_video_duration(video_path)
        
        # Generate timestamps at different parts of video
        # Start, 1/4, 1/2, 3/4, end positions
        positions = [0.1, 0.25, 0.5, 0.75, 0.9][:num_options]
        timestamps = [duration * pos for pos in positions]
        
        thumbnails = []
        
        for i, timestamp in enumerate(timestamps, 1):
            output_path = os.path.join(output_dir, f"{title_id}_option{i}.jpg")
            
            try:
                cmd = [
                    'ffmpeg', '-y',
                    '-ss', str(timestamp),
                    '-i', video_path,
                    '-vframes', '1',
                    '-vf', f'scale={self.width}:{self.height}',
                    '-q:v', '2',
                    output_path
                ]
                
                subprocess.run(cmd, check=True, capture_output=True)
                thumbnails.append(output_path)
                print(f"  ✅ Generated option {i} at {int(positions[i-1]*100)}% of video")
                
            except subprocess.CalledProcessError as e:
                print(f"  ❌ Failed to generate option {i}: {e}")
        
        return thumbnails
    
    def _get_video_duration(self, video_path: str) -> float:
        """Get video duration in seconds."""
        try:
            cmd = [
                'ffprobe',
                '-v', 'error',
                '-show_entries', 'format=duration',
                '-of', 'default=noprint_wrappers=1:nokey=1',
                video_path
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            return float(result.stdout.strip())
            
        except Exception as e:
            print(f"⚠️ Error getting video duration: {e}")
            return 60.0  # Default fallback
    
    def _create_grid_image(
        self,
        image_paths: List[str],
        rows: int,
        cols: int
    ) -> Image.Image:
        """Create a grid image from individual thumbnails."""
        # Load first image to get dimensions
        first_img = Image.open(image_paths[0])
        thumb_width, thumb_height = first_img.size
        
        # Create grid canvas
        grid_width = thumb_width * cols
        grid_height = thumb_height * rows
        grid = Image.new('RGB', (grid_width, grid_height))
        
        # Place thumbnails in grid
        for i, img_path in enumerate(image_paths):
            if i >= rows * cols:
                break
            
            row = i // cols
            col = i % cols
            
            img = Image.open(img_path)
            x = col * thumb_width
            y = row * thumb_height
            grid.paste(img, (x, y))
        
        return grid
    
    def _analyze_frame(self, image_path: str, method: str) -> float:
        """
        Analyze frame quality using different methods.
        
        Args:
            image_path: Path to image file
            method: Analysis method
            
        Returns:
            Quality score
        """
        img = Image.open(image_path)
        img_array = np.array(img)
        
        if method == "brightness":
            # Calculate average brightness
            gray = np.mean(img_array, axis=2)
            brightness = np.mean(gray)
            # Prefer medium brightness (avoid too dark or too bright)
            ideal = 128
            score = 100 - abs(brightness - ideal) / ideal * 100
            return max(0, score)
        
        elif method == "sharpness":
            # Calculate sharpness using Laplacian variance
            gray = np.mean(img_array, axis=2).astype(np.float32)
            laplacian = np.array([[0, 1, 0], [1, -4, 1], [0, 1, 0]])
            
            # Simple convolution
            h, w = gray.shape
            result = np.zeros_like(gray)
            for i in range(1, h-1):
                for j in range(1, w-1):
                    result[i, j] = np.sum(gray[i-1:i+2, j-1:j+2] * laplacian)
            
            return np.var(result)
        
        elif method == "contrast":
            # Calculate contrast
            gray = np.mean(img_array, axis=2)
            return np.std(gray)
        
        else:
            return 0.0
