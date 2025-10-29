"""
Overlay system for captions and progress bar.
"""
import numpy as np
import cv2
from typing import List, Tuple


class Overlay:
    """Handles caption and progress bar overlays."""
    
    def __init__(self, config):
        """Initialize overlay system.
        
        Args:
            config: GenerationConfig instance
        """
        self.config = config
        self.captions = []
        
    def add_caption(self, text: str, start_frame: int):
        """Add a caption to display.
        
        Args:
            text: Caption text
            start_frame: Frame to start displaying caption
        """
        end_frame = start_frame + int(self.config.caption_duration * self.config.fps)
        self.captions.append({
            'text': text,
            'start': start_frame,
            'end': end_frame
        })
    
    def draw_caption(self, frame: np.ndarray, text: str, 
                    alpha: float = 1.0) -> np.ndarray:
        """Draw caption on frame.
        
        Args:
            frame: Input frame (H, W, C) in BGR
            text: Caption text
            alpha: Opacity (0.0 to 1.0)
            
        Returns:
            Frame with caption
        """
        h, w = frame.shape[:2]
        result = frame.copy()
        
        # Position in upper third
        pos_y = int(h * 0.25)
        
        # Font settings
        font = cv2.FONT_HERSHEY_DUPLEX  # Bold-like font
        font_scale = self.config.caption_font_size / 30.0
        thickness = 3
        
        # Calculate text size
        (text_w, text_h), baseline = cv2.getTextSize(text, font, 
                                                     font_scale, thickness)
        
        # Center horizontally
        pos_x = (w - text_w) // 2
        
        # Draw shadow/outline (black)
        for dx in [-2, -1, 0, 1, 2]:
            for dy in [-2, -1, 0, 1, 2]:
                if dx != 0 or dy != 0:
                    cv2.putText(result, text, 
                              (pos_x + dx, pos_y + dy),
                              font, font_scale, (0, 0, 0),
                              thickness + 1, cv2.LINE_AA)
        
        # Draw main text (white)
        cv2.putText(result, text, (pos_x, pos_y),
                   font, font_scale, (255, 255, 255),
                   thickness, cv2.LINE_AA)
        
        # Apply alpha blending if needed
        if alpha < 1.0:
            result = cv2.addWeighted(frame, 1 - alpha, result, alpha, 0)
        
        return result
    
    def draw_progress_bar(self, frame: np.ndarray, 
                         progress: float) -> np.ndarray:
        """Draw enhanced progress bar on frame.
        
        Implements research-backed design for retention & engagement:
        - Slim horizontal line (2-3px) at bottom edge
        - Bold brand-aligned foreground color (deep red/burgundy)
        - Translucent gray background track
        - Glowing end marker dot
        - Goal-gradient effect (acceleration at ~80%)
        - Shadow for contrast
        
        Args:
            frame: Input frame (H, W, C) in BGR
            progress: Progress value (0.0 to 1.0)
            
        Returns:
            Frame with progress bar
        """
        h, w = frame.shape[:2]
        result = frame.copy()
        
        # Progress bar dimensions (full width at very bottom)
        bar_height = self.config.progress_bar_height
        if self.config.progress_bar_full_width:
            bar_width = w  # Full width
            bar_x = 0
        else:
            bar_width = int(w * 0.9)  # 90% of width
            bar_x = (w - bar_width) // 2
        
        # Position at very bottom edge
        bar_y = h - bar_height - self.config.progress_bar_y_offset
        
        # Apply goal-gradient effect (slight acceleration at ~80%)
        if progress >= self.config.progress_bar_gradient_start:
            # Calculate accelerated progress for visual effect
            base_progress = self.config.progress_bar_gradient_start
            remaining = progress - base_progress
            remaining_range = 1.0 - base_progress
            # Apply slight acceleration
            visual_progress = base_progress + (remaining / remaining_range) ** (1.0 / self.config.progress_bar_gradient_factor) * remaining_range
        else:
            visual_progress = progress
        
        # Clamp visual progress to valid range
        visual_progress = max(0.0, min(1.0, visual_progress))
        
        # Create overlay for alpha blending
        overlay = result.copy()
        
        # Draw shadow if enabled (for better contrast)
        if self.config.progress_bar_shadow_enabled:
            shadow_y = bar_y + self.config.progress_bar_shadow_offset
            # Background shadow
            cv2.rectangle(overlay,
                         (bar_x, shadow_y),
                         (bar_x + bar_width, shadow_y + bar_height),
                         (0, 0, 0), -1)
            # Apply shadow with opacity
            result = cv2.addWeighted(result, 1.0, overlay, self.config.progress_bar_shadow_opacity, 0)
            overlay = result.copy()
        
        # Draw background track (translucent gray)
        cv2.rectangle(overlay,
                     (bar_x, bar_y),
                     (bar_x + bar_width, bar_y + bar_height),
                     self.config.progress_bar_bg_color, -1)
        
        # Apply background with its opacity
        result = cv2.addWeighted(result, 1 - self.config.progress_bar_bg_opacity, 
                                overlay, self.config.progress_bar_bg_opacity, 0)
        overlay = result.copy()
        
        # Draw progress fill (bold brand color - deep red/burgundy)
        fill_width = int(bar_width * visual_progress)
        
        if fill_width > 0:
            cv2.rectangle(overlay,
                         (bar_x, bar_y),
                         (bar_x + fill_width, bar_y + bar_height),
                         self.config.progress_bar_fg_color, -1)
        
        # Apply foreground with opacity
        result = cv2.addWeighted(result, 1 - self.config.progress_bar_opacity, 
                                overlay, self.config.progress_bar_opacity, 0)
        
        # Draw glowing end marker dot if enabled and progress > 0
        if self.config.progress_bar_marker_enabled and fill_width > 0:
            overlay = result.copy()
            
            # Calculate marker position
            marker_x = bar_x + fill_width
            marker_y = bar_y + (bar_height // 2)
            
            # Draw glow effect (larger, semi-transparent)
            glow_radius = self.config.progress_bar_marker_glow_radius
            cv2.circle(overlay, (marker_x, marker_y), glow_radius,
                      self.config.progress_bar_marker_color, -1)
            result = cv2.addWeighted(result, 0.7, overlay, 0.3, 0)
            
            # Draw main marker dot (smaller, more opaque)
            overlay = result.copy()
            marker_radius = self.config.progress_bar_marker_radius
            cv2.circle(overlay, (marker_x, marker_y), marker_radius,
                      self.config.progress_bar_marker_color, -1)
            result = cv2.addWeighted(result, 0.4, overlay, 0.6, 0)
        
        return result
    
    def apply_overlays(self, frame: np.ndarray, 
                      frame_idx: int, total_frames: int) -> np.ndarray:
        """Apply all overlays to frame.
        
        Args:
            frame: Input frame (H, W, C) in BGR
            frame_idx: Current frame index
            total_frames: Total number of frames
            
        Returns:
            Frame with overlays
        """
        result = frame.copy()
        
        # Draw captions
        for caption in self.captions:
            if caption['start'] <= frame_idx < caption['end']:
                # Calculate fade in/out
                fade_frames = self.config.fps // 5  # 0.2s fade
                
                if frame_idx < caption['start'] + fade_frames:
                    # Fade in
                    alpha = (frame_idx - caption['start']) / fade_frames
                    # Scale animation
                    scale = 0.9 + 0.1 * alpha
                elif frame_idx > caption['end'] - fade_frames:
                    # Fade out
                    alpha = (caption['end'] - frame_idx) / fade_frames
                    scale = 1.0
                else:
                    alpha = 1.0
                    scale = 1.0
                
                result = self.draw_caption(result, caption['text'], alpha)
        
        # Draw progress bar
        progress = frame_idx / total_frames
        result = self.draw_progress_bar(result, progress)
        
        return result
