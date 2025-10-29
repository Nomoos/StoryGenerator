"""
Main video processing pipeline.
Orchestrates generation, effects, and export.
"""
import cv2
import numpy as np
from typing import List, Optional
import os
import sys

# Support both package and standalone execution
if __name__ == '__main__' or '.' not in __name__:
    from config import GenerationConfig
    from generator import VideoGenerator
    from motion import MotionEffects
    from visual_style import VisualStyle
    from overlay import Overlay
else:
    from .config import GenerationConfig
    from .generator import VideoGenerator
    from .motion import MotionEffects
    from .visual_style import VisualStyle
    from .overlay import Overlay


class VideoPipeline:
    """Complete video generation and processing pipeline."""
    
    def __init__(self, config: Optional[GenerationConfig] = None):
        """Initialize video pipeline.
        
        Args:
            config: GenerationConfig instance (optional, uses defaults if not provided)
        """
        self.config = config or GenerationConfig()
        
        # Initialize components
        self.generator = VideoGenerator(self.config)
        self.motion = MotionEffects(self.config)
        self.style = VisualStyle(self.config)
        self.overlay = Overlay(self.config)
        
        # State
        self.frames = []
        self.current_break = None
        self.break_start_frame = None
        
    def generate_base_video(self) -> None:
        """Generate base 3-second video clip."""
        print("=" * 60)
        print("STEP 1: Generating base video clip")
        print("=" * 60)
        
        base_frames = self.generator.generate_base_clip()
        self.frames = self.generator.tile_clip(base_frames)
        
        print(f"✓ Base video ready: {len(self.frames)} frames\n")
    
    def apply_visual_style(self) -> None:
        """Apply high-contrast neon visual style."""
        print("=" * 60)
        print("STEP 2: Applying visual style (high contrast + neon)")
        print("=" * 60)
        
        styled_frames = []
        total = len(self.frames)
        
        for i, frame in enumerate(self.frames):
            styled = self.style.apply_full_style(frame)
            styled_frames.append(styled)
            
            if (i + 1) % 100 == 0:
                print(f"  Styled {i + 1}/{total} frames")
        
        self.frames = styled_frames
        print(f"✓ Visual style applied\n")
    
    def apply_motion_effects(self) -> None:
        """Apply constant motion and pattern breaks."""
        print("=" * 60)
        print("STEP 3: Applying motion effects")
        print("=" * 60)
        
        motion_frames = []
        total = len(self.frames)
        
        for i, frame in enumerate(self.frames):
            # Apply base motion effects
            frame = self.motion.apply_micro_movement(frame, i)
            frame = self.motion.apply_parallax(frame, i)
            frame = self.motion.apply_micro_zoom(frame, i, total)
            
            # Check for pattern breaks
            should_break, break_type = self.motion.should_apply_pattern_break(i)
            
            if should_break:
                self.current_break = break_type
                self.break_start_frame = i
                print(f"  Pattern break at frame {i}: {break_type}")
            
            # Apply pattern break if active
            if self.current_break is not None:
                frames_into_break = i - self.break_start_frame
                if frames_into_break < self.config.break_duration:
                    progress = frames_into_break / self.config.break_duration
                    frame = self.motion.apply_pattern_break(
                        frame, i, self.current_break, progress
                    )
                else:
                    self.current_break = None
            
            motion_frames.append(frame)
            
            if (i + 1) % 100 == 0:
                print(f"  Processed {i + 1}/{total} frames")
        
        self.frames = motion_frames
        print(f"✓ Motion effects applied\n")
    
    def add_captions(self, captions: List[tuple]) -> None:
        """Add caption overlays.
        
        Args:
            captions: List of (text, start_frame) tuples
        """
        print("=" * 60)
        print("STEP 4: Adding captions")
        print("=" * 60)
        
        for text, start_frame in captions:
            self.overlay.add_caption(text, start_frame)
            print(f"  Caption at frame {start_frame}: {text}")
        
        print(f"✓ {len(captions)} captions added\n")
    
    def apply_overlays(self) -> None:
        """Apply caption and progress bar overlays."""
        print("=" * 60)
        print("STEP 5: Applying overlays")
        print("=" * 60)
        
        overlay_frames = []
        total = len(self.frames)
        
        for i, frame in enumerate(self.frames):
            frame = self.overlay.apply_overlays(frame, i, total)
            overlay_frames.append(frame)
            
            if (i + 1) % 100 == 0:
                print(f"  Overlaid {i + 1}/{total} frames")
        
        self.frames = overlay_frames
        print(f"✓ Overlays applied\n")
    
    def export_video(self, output_path: str) -> None:
        """Export final video.
        
        Args:
            output_path: Path to save video file
        """
        print("=" * 60)
        print("STEP 6: Exporting video")
        print("=" * 60)
        
        # Ensure output directory exists
        os.makedirs(os.path.dirname(output_path) if os.path.dirname(output_path) else '.', 
                   exist_ok=True)
        
        # Set up video writer
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        w, h = self.config.output_resolution
        out = cv2.VideoWriter(output_path, fourcc, self.config.fps, (w, h))
        
        print(f"  Resolution: {w}×{h}")
        print(f"  FPS: {self.config.fps}")
        print(f"  Frames: {len(self.frames)}")
        print(f"  Duration: {len(self.frames) / self.config.fps:.1f}s")
        
        # Write frames
        for i, frame in enumerate(self.frames):
            out.write(frame)
            
            if (i + 1) % 100 == 0:
                print(f"  Wrote {i + 1}/{len(self.frames)} frames")
        
        out.release()
        print(f"✓ Video exported to: {output_path}\n")
    
    def run_full_pipeline(self, output_path: str, 
                         captions: Optional[List[tuple]] = None) -> None:
        """Run complete video generation pipeline.
        
        Args:
            output_path: Path to save final video
            captions: Optional list of (text, start_frame) captions
        """
        print("\n" + "=" * 60)
        print("VISUAL ENGAGEMENT VIDEO GENERATOR")
        print("=" * 60 + "\n")
        
        # Generate base video
        self.generate_base_video()
        
        # Apply visual style
        self.apply_visual_style()
        
        # Apply motion effects
        self.apply_motion_effects()
        
        # Add captions if provided
        if captions:
            self.add_captions(captions)
        
        # Apply overlays
        self.apply_overlays()
        
        # Export
        self.export_video(output_path)
        
        print("=" * 60)
        print("PIPELINE COMPLETE!")
        print("=" * 60)
        print(f"\nOutput video: {output_path}")
        print(f"Duration: {self.config.target_duration}s")
        print(f"Resolution: {self.config.output_resolution[0]}×{self.config.output_resolution[1]}")
        print(f"FPS: {self.config.fps}")
