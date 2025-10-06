#!/usr/bin/env python3
"""
Test suite for SDXL Keyframe Generation

This test validates the keyframe generation functionality with SDXL.
Note: Actual model loading tests require GPU and are marked as slow/integration tests.
"""

import os
import sys
import unittest
from unittest.mock import Mock, patch, MagicMock
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from Python.Models.Keyframe import Keyframe
from config import sdxl_config


class TestKeyframeModel(unittest.TestCase):
    """Test the Keyframe data model"""
    
    def test_keyframe_creation(self):
        """Test creating a Keyframe object"""
        keyframe = Keyframe(
            scene_id=1,
            image_path="/path/to/image.png",
            prompt="A beautiful scene",
            negative_prompt="blurry, low quality",
            seed=42,
            width=1080,
            height=1920,
            steps=40,
            guidance_scale=7.5,
            style_preset="cinematic",
            generation_time=10.5,
            quality_score=8.5,
            keyframe_index=0,
            timestamp=0.0,
            position=0.0,
            use_refiner=True,
            refiner_steps=20
        )
        
        self.assertEqual(keyframe.scene_id, 1)
        self.assertEqual(keyframe.width, 1080)
        self.assertEqual(keyframe.height, 1920)
        self.assertEqual(keyframe.style_preset, "cinematic")
        self.assertTrue(keyframe.use_refiner)
    
    def test_keyframe_to_dict(self):
        """Test converting Keyframe to dictionary"""
        keyframe = Keyframe(
            scene_id=1,
            image_path="/path/to/image.png",
            prompt="Test prompt",
            negative_prompt="Test negative",
            seed=42,
            width=1080,
            height=1920,
            steps=40,
            guidance_scale=7.5,
            style_preset="cinematic",
            generation_time=10.0
        )
        
        data = keyframe.to_dict()
        self.assertIsInstance(data, dict)
        self.assertEqual(data['scene_id'], 1)
        self.assertEqual(data['width'], 1080)
        self.assertEqual(data['height'], 1920)


class TestSDXLConfig(unittest.TestCase):
    """Test SDXL configuration"""
    
    def test_config_values(self):
        """Test that config has expected values"""
        self.assertEqual(sdxl_config.DEFAULT_WIDTH, 1080)
        self.assertEqual(sdxl_config.DEFAULT_HEIGHT, 1920)
        self.assertEqual(sdxl_config.TARGET_FPS, 60)
        self.assertIsNotNone(sdxl_config.SDXL_BASE_MODEL)
        self.assertIsNotNone(sdxl_config.SDXL_REFINER_MODEL)
    
    def test_resolution_aspect_ratio(self):
        """Test that default resolution is 9:16"""
        aspect_ratio = sdxl_config.DEFAULT_WIDTH / sdxl_config.DEFAULT_HEIGHT
        expected_ratio = 9 / 16
        self.assertAlmostEqual(aspect_ratio, expected_ratio, places=2)


if __name__ == "__main__":
    unittest.main()
