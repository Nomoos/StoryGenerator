"""
Tests for EngagementOptimizer module.
"""
import pytest
import numpy as np
import sys
import os

# Add EngagementOptimizer to path
engagement_optimizer_path = os.path.join(
    os.path.dirname(__file__), '..', '..', 'Pipeline', '05_VideoGeneration', 'EngagementOptimizer'
)
sys.path.insert(0, engagement_optimizer_path)

from config import GenerationConfig
from visual_style import VisualStyle
from motion import MotionEffects
from overlay import Overlay
from generator import VideoGenerator
from pipeline import VideoPipeline


class TestGenerationConfig:
    """Test GenerationConfig dataclass."""
    
    def test_default_config(self):
        """Test default configuration values."""
        config = GenerationConfig()
        
        assert config.output_resolution == (1080, 1920)
        assert config.fps == 30
        assert config.target_duration == 27
        assert config.seed == 42
        
    def test_total_frames_property(self):
        """Test total_frames calculation."""
        config = GenerationConfig(target_duration=10, fps=30)
        assert config.total_frames == 300
        
    def test_base_frames_property(self):
        """Test base_frames calculation."""
        config = GenerationConfig(base_clip_duration=3, fps=30)
        assert config.base_frames == 90
        
    def test_tiles_needed_property(self):
        """Test tiles_needed calculation."""
        config = GenerationConfig(target_duration=27, base_clip_duration=3, fps=30)
        # 27s = 810 frames, 3s = 90 frames, need 9 tiles
        assert config.tiles_needed == 9
        
    def test_neon_colors_initialization(self):
        """Test neon colors are initialized."""
        config = GenerationConfig()
        assert config.neon_colors is not None
        assert len(config.neon_colors) == 5


class TestVisualStyle:
    """Test VisualStyle processor."""
    
    def test_initialization(self):
        """Test VisualStyle initialization."""
        config = GenerationConfig()
        style = VisualStyle(config)
        assert style.config == config
        
    def test_apply_dark_base(self):
        """Test dark base application."""
        config = GenerationConfig()
        style = VisualStyle(config)
        
        # Create test frame
        frame = np.ones((100, 100, 3), dtype=np.uint8) * 128
        result = style.apply_dark_base(frame)
        
        assert result.shape == frame.shape
        assert result.dtype == np.uint8
        # Should be darker than original
        assert np.mean(result) < np.mean(frame)
        
    def test_detect_edges(self):
        """Test edge detection."""
        config = GenerationConfig()
        style = VisualStyle(config)
        
        # Create test frame with edges
        frame = np.zeros((100, 100, 3), dtype=np.uint8)
        frame[25:75, 25:75] = 255  # White square
        
        edges = style.detect_edges(frame)
        
        assert edges.shape == (100, 100)
        assert edges.dtype == np.uint8
        assert np.max(edges) > 0  # Should detect edges


class TestMotionEffects:
    """Test MotionEffects."""
    
    def test_initialization(self):
        """Test MotionEffects initialization."""
        config = GenerationConfig()
        motion = MotionEffects(config)
        assert motion.config == config
        
    def test_apply_micro_movement(self):
        """Test micro-movement application."""
        config = GenerationConfig()
        motion = MotionEffects(config)
        
        frame = np.random.randint(0, 255, (100, 100, 3), dtype=np.uint8)
        result = motion.apply_micro_movement(frame, 0)
        
        assert result.shape == frame.shape
        assert result.dtype == np.uint8
        
    def test_should_apply_pattern_break(self):
        """Test pattern break detection."""
        config = GenerationConfig(
            minor_break_interval=40,
            major_break_interval=80
        )
        motion = MotionEffects(config)
        
        # Test no break at start
        should_break, break_type = motion.should_apply_pattern_break(0)
        assert not should_break
        
        # Test minor break
        should_break, break_type = motion.should_apply_pattern_break(40)
        assert should_break
        assert break_type == "minor"
        
        # Test major break (overrides minor)
        should_break, break_type = motion.should_apply_pattern_break(80)
        assert should_break
        assert break_type == "major"


class TestOverlay:
    """Test Overlay system."""
    
    def test_initialization(self):
        """Test Overlay initialization."""
        config = GenerationConfig()
        overlay = Overlay(config)
        assert overlay.config == config
        assert len(overlay.captions) == 0
        
    def test_add_caption(self):
        """Test caption addition."""
        config = GenerationConfig(fps=30, caption_duration=2.5)
        overlay = Overlay(config)
        
        overlay.add_caption("Test", 0)
        
        assert len(overlay.captions) == 1
        assert overlay.captions[0]['text'] == "Test"
        assert overlay.captions[0]['start'] == 0
        assert overlay.captions[0]['end'] == int(2.5 * 30)
        
    def test_draw_progress_bar(self):
        """Test progress bar drawing."""
        config = GenerationConfig()
        overlay = Overlay(config)
        
        frame = np.zeros((1920, 1080, 3), dtype=np.uint8)
        result = overlay.draw_progress_bar(frame, 0.5)
        
        assert result.shape == frame.shape
        assert result.dtype == np.uint8
        # Progress bar should add some pixels
        assert np.sum(result) > np.sum(frame)


class TestVideoGenerator:
    """Test VideoGenerator."""
    
    def test_initialization(self):
        """Test VideoGenerator initialization."""
        config = GenerationConfig()
        generator = VideoGenerator(config)
        assert generator.config == config
        
    def test_generate_abstract_frame(self):
        """Test abstract frame generation."""
        config = GenerationConfig()
        generator = VideoGenerator(config)
        
        frame = generator.generate_abstract_frame(0, 90)
        
        h, w = config.output_resolution[1], config.output_resolution[0]
        assert frame.shape == (h, w, 3)
        assert frame.dtype == np.uint8
        
    def test_generate_base_clip(self):
        """Test base clip generation."""
        config = GenerationConfig(base_clip_duration=1, fps=10)  # Short for testing
        generator = VideoGenerator(config)
        
        frames = generator.generate_base_clip()
        
        assert len(frames) == 10
        assert all(f.shape == (1920, 1080, 3) for f in frames)


class TestVideoPipeline:
    """Test VideoPipeline."""
    
    def test_initialization(self):
        """Test VideoPipeline initialization."""
        config = GenerationConfig()
        pipeline = VideoPipeline(config)
        
        assert pipeline.config == config
        assert isinstance(pipeline.generator, VideoGenerator)
        assert isinstance(pipeline.motion, MotionEffects)
        assert isinstance(pipeline.style, VisualStyle)
        assert isinstance(pipeline.overlay, Overlay)
        
    def test_initialization_with_defaults(self):
        """Test VideoPipeline with default config."""
        pipeline = VideoPipeline()
        
        assert pipeline.config is not None
        assert pipeline.config.fps == 30


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
