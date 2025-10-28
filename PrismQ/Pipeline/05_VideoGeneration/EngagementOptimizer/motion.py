"""
Motion effects for constant movement and pattern breaks.
"""
import numpy as np
from typing import Tuple, List
import cv2


class MotionEffects:
    """Applies constant motion and pattern break effects."""
    
    def __init__(self, config):
        """Initialize motion effects with configuration.
        
        Args:
            config: GenerationConfig instance
        """
        self.config = config
        self.frame_count = 0
        
    def apply_micro_movement(self, frame: np.ndarray, frame_idx: int) -> np.ndarray:
        """Apply subtle micro-movements to prevent static appearance.
        
        Args:
            frame: Input frame (H, W, C)
            frame_idx: Current frame index
            
        Returns:
            Frame with micro-movements applied
        """
        h, w = frame.shape[:2]
        
        # Calculate oscillating offset
        t = frame_idx / self.config.fps
        freq = self.config.micro_movement_frequency
        amp = self.config.micro_movement_amplitude
        
        # Sinusoidal motion in both directions
        dx = amp * np.sin(2 * np.pi * freq * t)
        dy = amp * np.cos(2 * np.pi * freq * t * 0.7)  # Different phase
        
        # Create transformation matrix
        M = np.float32([[1, 0, dx], [0, 1, dy]])
        
        # Apply translation
        result = cv2.warpAffine(frame, M, (w, h), 
                               borderMode=cv2.BORDER_REFLECT)
        
        return result
    
    def apply_parallax(self, frame: np.ndarray, frame_idx: int) -> np.ndarray:
        """Apply slow parallax drift effect.
        
        Args:
            frame: Input frame (H, W, C)
            frame_idx: Current frame index
            
        Returns:
            Frame with parallax applied
        """
        h, w = frame.shape[:2]
        
        # Slow horizontal drift
        drift = (frame_idx * self.config.parallax_speed) % (w * 0.1)
        
        M = np.float32([[1, 0, drift], [0, 1, 0]])
        result = cv2.warpAffine(frame, M, (w, h), 
                               borderMode=cv2.BORDER_WRAP)
        
        return result
    
    def apply_micro_zoom(self, frame: np.ndarray, frame_idx: int, 
                        total_frames: int) -> np.ndarray:
        """Apply gradual micro-zoom effect.
        
        Args:
            frame: Input frame (H, W, C)
            frame_idx: Current frame index
            total_frames: Total number of frames
            
        Returns:
            Frame with zoom applied
        """
        h, w = frame.shape[:2]
        
        # Progressive zoom from 1.0 to 1.05
        min_zoom, max_zoom = self.config.micro_zoom_range
        progress = frame_idx / total_frames
        zoom = min_zoom + (max_zoom - min_zoom) * progress
        
        # Add subtle oscillation
        cycle_t = (frame_idx % self.config.zoom_cycle_duration) / self.config.zoom_cycle_duration
        oscillation = 0.002 * np.sin(2 * np.pi * cycle_t)
        zoom += oscillation
        
        # Calculate zoom matrix
        center_x, center_y = w / 2, h / 2
        M = cv2.getRotationMatrix2D((center_x, center_y), 0, zoom)
        
        result = cv2.warpAffine(frame, M, (w, h), 
                               borderMode=cv2.BORDER_REFLECT)
        
        return result
    
    def should_apply_pattern_break(self, frame_idx: int) -> Tuple[bool, str]:
        """Determine if a pattern break should occur.
        
        Args:
            frame_idx: Current frame index
            
        Returns:
            Tuple of (should_break, break_type)
        """
        # Check for major breaks
        if frame_idx % self.config.major_break_interval == 0 and frame_idx > 0:
            return True, "major"
        
        # Check for minor breaks
        if frame_idx % self.config.minor_break_interval == 0 and frame_idx > 0:
            return True, "minor"
        
        return False, None
    
    def apply_pattern_break(self, frame: np.ndarray, frame_idx: int, 
                          break_type: str, break_progress: float) -> np.ndarray:
        """Apply pattern break effect.
        
        Args:
            frame: Input frame (H, W, C)
            frame_idx: Current frame index
            break_type: Type of break ("minor" or "major")
            break_progress: Progress through break (0.0 to 1.0)
            
        Returns:
            Frame with pattern break applied
        """
        h, w = frame.shape[:2]
        center_x, center_y = w / 2, h / 2
        
        if break_type == "minor":
            # Small rotation twirl
            angle = 45 * np.sin(break_progress * np.pi)
            M = cv2.getRotationMatrix2D((center_x, center_y), angle, 1.0)
            result = cv2.warpAffine(frame, M, (w, h), 
                                   borderMode=cv2.BORDER_REFLECT)
            
        elif break_type == "major":
            # Zoom pop
            scale = 1.0 + 0.2 * np.sin(break_progress * np.pi)
            M = cv2.getRotationMatrix2D((center_x, center_y), 0, scale)
            result = cv2.warpAffine(frame, M, (w, h), 
                                   borderMode=cv2.BORDER_REFLECT)
        else:
            result = frame
        
        return result
    
    def apply_speed_pulse(self, frame_rate: float, frame_idx: int) -> float:
        """Calculate speed multiplier for current frame.
        
        Args:
            frame_rate: Base frame rate
            frame_idx: Current frame index
            
        Returns:
            Speed multiplier (1.0 = normal, >1.0 = faster)
        """
        # Apply speed pulse at major breaks
        if frame_idx % self.config.major_break_interval < 8:
            return 1.4
        
        return 1.0
