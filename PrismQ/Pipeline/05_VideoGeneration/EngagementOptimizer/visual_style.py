"""
Visual style processing: high contrast, neon accents, edge effects.
"""
import numpy as np
import cv2
from typing import Tuple, List


class VisualStyle:
    """Applies high-contrast neon visual style."""
    
    def __init__(self, config):
        """Initialize visual style processor.
        
        Args:
            config: GenerationConfig instance
        """
        self.config = config
        
    def apply_dark_base(self, frame: np.ndarray) -> np.ndarray:
        """Apply dark midtone base layer.
        
        Args:
            frame: Input frame (H, W, C) in BGR
            
        Returns:
            Frame with darkened base
        """
        # Convert to float for processing
        frame_float = frame.astype(np.float32) / 255.0
        
        # Crush blacks and compress midtones
        min_dark, max_dark = self.config.base_darkness
        target_mid = (min_dark + max_dark) / 2 / 255.0
        
        # Apply curve: darken everything below 50% luminance
        frame_float = np.power(frame_float, 1.3)  # Gamma correction
        frame_float = frame_float * 0.7 + target_mid * 0.3
        
        # Clip and convert back
        frame_float = np.clip(frame_float, 0, 1)
        result = (frame_float * 255).astype(np.uint8)
        
        return result
    
    def detect_edges(self, frame: np.ndarray) -> np.ndarray:
        """Detect edges for neon effect.
        
        Args:
            frame: Input frame (H, W, C) in BGR
            
        Returns:
            Edge mask (H, W) with edge intensity
        """
        # Convert to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Apply Gaussian blur to reduce noise
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        
        # Canny edge detection
        edges = cv2.Canny(blurred, 50, 150)
        
        # Dilate edges slightly
        kernel = np.ones((3, 3), np.uint8)
        edges = cv2.dilate(edges, kernel, iterations=1)
        
        return edges
    
    def apply_neon_edges(self, frame: np.ndarray, edges: np.ndarray) -> np.ndarray:
        """Apply neon glow effect to edges.
        
        Args:
            frame: Input frame (H, W, C) in BGR
            edges: Edge mask (H, W)
            
        Returns:
            Frame with neon edges
        """
        result = frame.copy()
        
        # Select random neon color
        color_idx = np.random.randint(0, len(self.config.neon_colors))
        neon_color = self.config.neon_colors[color_idx]
        # Convert RGB to BGR for OpenCV
        neon_color_bgr = (neon_color[2], neon_color[1], neon_color[0])
        
        # Create colored edge layer
        edge_layer = np.zeros_like(frame)
        edge_layer[edges > 0] = neon_color_bgr
        
        # Apply glow effect (multiple blur passes)
        glow = edge_layer.copy().astype(np.float32)
        for i in range(3):
            kernel_size = 7 + i * 4
            glow = cv2.GaussianBlur(glow, (kernel_size, kernel_size), 0)
        
        # Blend edge layer and glow with original
        edge_alpha = 0.8
        glow_alpha = 0.4
        
        result = result.astype(np.float32)
        result = result * (1 - edge_alpha) + edge_layer.astype(np.float32) * edge_alpha
        result = result + glow * glow_alpha
        
        result = np.clip(result, 0, 255).astype(np.uint8)
        
        return result
    
    def boost_contrast_saturation(self, frame: np.ndarray) -> np.ndarray:
        """Boost contrast and saturation.
        
        Args:
            frame: Input frame (H, W, C) in BGR
            
        Returns:
            Frame with boosted contrast and saturation
        """
        # Convert to HSV for saturation adjustment
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV).astype(np.float32)
        
        # Boost saturation
        hsv[:, :, 1] = hsv[:, :, 1] * self.config.saturation_boost
        hsv[:, :, 1] = np.clip(hsv[:, :, 1], 0, 255)
        
        # Convert back to BGR
        frame = cv2.cvtColor(hsv.astype(np.uint8), cv2.COLOR_HSV2BGR)
        
        # Boost contrast using CLAHE
        lab = cv2.cvtColor(frame, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab)
        
        clahe = cv2.createCLAHE(clipLimit=self.config.contrast_boost, 
                                tileGridSize=(8, 8))
        l = clahe.apply(l)
        
        lab = cv2.merge([l, a, b])
        result = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)
        
        return result
    
    def apply_full_style(self, frame: np.ndarray) -> np.ndarray:
        """Apply complete visual style pipeline.
        
        Args:
            frame: Input frame (H, W, C) in BGR
            
        Returns:
            Styled frame
        """
        # Step 1: Dark base
        frame = self.apply_dark_base(frame)
        
        # Step 2: Boost contrast and saturation
        frame = self.boost_contrast_saturation(frame)
        
        # Step 3: Detect edges
        edges = self.detect_edges(frame)
        
        # Step 4: Apply neon edges
        frame = self.apply_neon_edges(frame, edges)
        
        return frame
