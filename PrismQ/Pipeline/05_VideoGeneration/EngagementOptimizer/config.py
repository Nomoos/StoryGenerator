"""
Configuration for video generation parameters.
"""
from dataclasses import dataclass
from typing import Tuple, List


@dataclass
class GenerationConfig:
    """Configuration for video generation."""
    
    # Video output settings
    output_resolution: Tuple[int, int] = (1080, 1920)  # 9:16 vertical
    fps: int = 30
    target_duration: int = 27  # seconds (middle of 24-30s range)
    base_clip_duration: int = 3  # seconds for initial generation
    
    # SDXL/AnimateDiff settings
    model_name: str = "stabilityai/stable-diffusion-xl-base-1.0"
    seed: int = 42  # Locked seed for consistency
    cfg_scale: float = 7.0  # Low CFG for creative variation
    num_inference_steps: int = 30
    
    # Motion settings
    motion_threshold_ms: int = 300  # Nothing static for >300ms
    micro_movement_amplitude: float = 2.0  # pixels
    micro_movement_frequency: float = 1.0  # Hz
    parallax_speed: float = 0.3  # pixels per frame
    
    # Zoom settings
    micro_zoom_range: Tuple[float, float] = (1.0, 1.05)  # 0-5% zoom
    zoom_cycle_duration: int = 90  # frames
    
    # Pattern break settings
    minor_break_interval: int = 40  # frames (~1.3s)
    major_break_interval: int = 80  # frames (~2.7s)
    break_duration: int = 5  # frames
    
    # Visual style settings
    base_darkness: Tuple[int, int] = (20, 60)  # RGB range for dark base
    neon_colors: List[Tuple[int, int, int]] = None  # Set in __post_init__
    accent_coverage: float = 0.12  # 12% of frame
    contrast_boost: float = 1.5
    saturation_boost: float = 1.4
    
    # Overlay settings
    caption_font_size: int = 48
    caption_duration: float = 2.5  # seconds
    
    # Progress bar settings (optimized for retention & engagement)
    progress_bar_height: int = 3  # pixels (2-3px slim design)
    progress_bar_opacity: float = 0.85  # Higher opacity for better visibility
    progress_bar_y_offset: int = 0  # Offset from bottom edge (0 = very bottom)
    progress_bar_full_width: bool = True  # Span full width of frame
    
    # Progress bar colors (deep red/burgundy for drama/engagement)
    progress_bar_fg_color: Tuple[int, int, int] = (25, 25, 139)  # BGR: Deep red/burgundy
    progress_bar_bg_color: Tuple[int, int, int] = (60, 60, 60)  # Translucent gray
    progress_bar_bg_opacity: float = 0.4  # Background track opacity
    
    # Progress bar end marker (glowing dot)
    progress_bar_marker_enabled: bool = True
    progress_bar_marker_radius: int = 5  # Radius of glowing dot
    progress_bar_marker_glow_radius: int = 10  # Glow effect radius
    progress_bar_marker_color: Tuple[int, int, int] = (50, 50, 200)  # Brighter red for marker
    
    # Goal-gradient effect (acceleration at ~80%)
    progress_bar_gradient_start: float = 0.80  # Start acceleration at 80%
    progress_bar_gradient_factor: float = 1.2  # Slight acceleration multiplier
    
    # Shadow/contrast settings
    progress_bar_shadow_enabled: bool = True
    progress_bar_shadow_offset: int = 1  # Shadow offset in pixels
    progress_bar_shadow_opacity: float = 0.6
    
    def __post_init__(self):
        """Initialize default neon colors if not provided."""
        if self.neon_colors is None:
            self.neon_colors = [
                (0, 255, 255),    # Cyan
                (255, 0, 255),    # Magenta
                (0, 128, 255),    # Electric Blue
                (0, 255, 0),      # Neon Green
                (255, 20, 147),   # Hot Pink
            ]
    
    @property
    def total_frames(self) -> int:
        """Calculate total frames for target duration."""
        return self.target_duration * self.fps
    
    @property
    def base_frames(self) -> int:
        """Calculate frames for base clip."""
        return self.base_clip_duration * self.fps
    
    @property
    def tiles_needed(self) -> int:
        """Calculate number of tiles needed."""
        return (self.total_frames + self.base_frames - 1) // self.base_frames
