"""
Unit tests for Style Consistency System

Tests cover:
- Style profile creation and management
- Style reference generation
- Keyframe generation with style consistency
- Visual coherence validation
- Color palette extraction
- Style library management
"""

import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
import numpy as np
from PIL import Image

from PrismQ.StoryGenerator.style_consistency import (
    StyleConsistencyManager,
    StyleProfile,
    ConsistencyMetrics
)


class TestStyleProfile(unittest.TestCase):
    """Test StyleProfile dataclass."""
    
    def test_style_profile_creation(self):
        """Test creating a style profile."""
        profile = StyleProfile(
            name="cinematic_style",
            reference_image_path="/path/to/ref.png",
            style_prompt="cinematic, dramatic lighting",
            ip_adapter_scale=0.8,
            color_palette=[(100, 150, 200), (50, 75, 100)],
            style_tags=["cinematic", "dramatic"]
        )
        
        self.assertEqual(profile.name, "cinematic_style")
        self.assertEqual(profile.ip_adapter_scale, 0.8)
        self.assertEqual(len(profile.color_palette), 2)
        self.assertIn("cinematic", profile.style_tags)
    
    def test_style_profile_to_dict(self):
        """Test converting profile to dictionary."""
        profile = StyleProfile(
            name="test_style",
            reference_image_path="/path/ref.png",
            style_prompt="test prompt",
            color_palette=[(255, 0, 0)]
        )
        
        profile_dict = profile.to_dict()
        self.assertIsInstance(profile_dict, dict)
        self.assertEqual(profile_dict['name'], "test_style")
        self.assertIn('created_at', profile_dict)
        self.assertEqual(profile_dict['color_palette'], [(255, 0, 0)])
    
    def test_style_profile_from_dict(self):
        """Test creating profile from dictionary."""
        data = {
            'name': 'restored_style',
            'reference_image_path': '/path/image.png',
            'style_prompt': 'artistic style',
            'ip_adapter_scale': 0.7,
            'color_palette': [(100, 100, 100)],
            'style_tags': ['artistic'],
            'created_at': '2024-01-01T00:00:00',
            'metadata': {}
        }
        
        profile = StyleProfile.from_dict(data)
        self.assertEqual(profile.name, 'restored_style')
        self.assertEqual(profile.ip_adapter_scale, 0.7)
        self.assertEqual(profile.style_tags, ['artistic'])


class TestConsistencyMetrics(unittest.TestCase):
    """Test ConsistencyMetrics dataclass."""
    
    def test_consistency_metrics_creation(self):
        """Test creating consistency metrics."""
        metrics = ConsistencyMetrics(
            color_similarity=0.85,
            structural_similarity=0.80,
            style_consistency=0.90,
            overall_score=0.85,
            frame_scores=[0.85, 0.84, 0.86]
        )
        
        self.assertEqual(metrics.color_similarity, 0.85)
        self.assertEqual(metrics.overall_score, 0.85)
        self.assertEqual(len(metrics.frame_scores), 3)
    
    def test_consistency_metrics_to_dict(self):
        """Test converting metrics to dictionary."""
        metrics = ConsistencyMetrics(
            color_similarity=0.9,
            structural_similarity=0.85,
            style_consistency=0.95,
            overall_score=0.90
        )
        
        metrics_dict = metrics.to_dict()
        self.assertIsInstance(metrics_dict, dict)
        self.assertEqual(metrics_dict['color_similarity'], 0.9)
        self.assertEqual(metrics_dict['overall_score'], 0.90)


class TestStyleConsistencyManager(unittest.TestCase):
    """Test StyleConsistencyManager class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.style_lib_dir = Path(self.temp_dir) / "styles"
        self.style_lib_dir.mkdir(parents=True, exist_ok=True)
    
    def tearDown(self):
        """Clean up test fixtures."""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    @patch('core.pipeline.style_consistency.StyleConsistencyManager._load_style_library')
    def test_manager_initialization(self, mock_load):
        """Test StyleConsistencyManager initialization."""
        manager = StyleConsistencyManager(
            style_library_dir=self.style_lib_dir,
            device="cpu"
        )
        
        self.assertEqual(manager.device, "cpu")
        self.assertEqual(manager.style_library_dir, self.style_lib_dir)
        self.assertIsInstance(manager.style_profiles, dict)
        mock_load.assert_called_once()
    
    def test_save_and_load_style_profile(self):
        """Test saving and loading style profiles."""
        manager = StyleConsistencyManager(
            style_library_dir=self.style_lib_dir,
            device="cpu"
        )
        
        # Create a profile
        profile = StyleProfile(
            name="test_style",
            reference_image_path="/path/test.png",
            style_prompt="test style prompt",
            color_palette=[(128, 128, 128)],
            style_tags=["test"]
        )
        
        # Save profile
        manager._save_style_profile(profile)
        
        # Verify file created
        profile_file = self.style_lib_dir / "test_style_style.json"
        self.assertTrue(profile_file.exists())
        
        # Verify content
        with open(profile_file, 'r') as f:
            data = json.load(f)
            self.assertEqual(data['name'], 'test_style')
            self.assertEqual(data['color_palette'], [(128, 128, 128)])
    
    @patch('core.pipeline.style_consistency.StyleConsistencyManager.pipe')
    def test_create_style_reference(self, mock_pipe):
        """Test creating style reference image."""
        manager = StyleConsistencyManager(
            style_library_dir=self.style_lib_dir,
            device="cpu"
        )
        
        # Mock pipeline output
        mock_image = Image.new('RGB', (1024, 1024), color='red')
        mock_result = MagicMock()
        mock_result.images = [mock_image]
        mock_pipe.return_value = mock_result
        
        # Create style reference
        output_path = Path(self.temp_dir) / "style_ref.png"
        profile = manager.create_style_reference(
            prompt="cinematic style",
            style_name="cinematic",
            output_path=output_path
        )
        
        # Verify
        self.assertEqual(profile.name, "cinematic")
        self.assertEqual(profile.style_prompt, "cinematic style")
        self.assertTrue(output_path.exists())
        self.assertIn("cinematic", manager.style_profiles)
    
    def test_extract_color_palette(self):
        """Test color palette extraction."""
        manager = StyleConsistencyManager(
            style_library_dir=self.style_lib_dir,
            device="cpu"
        )
        
        # Create test image with specific colors
        img = Image.new('RGB', (100, 100))
        # Fill with red
        pixels = img.load()
        for i in range(100):
            for j in range(100):
                pixels[i, j] = (255, 0, 0)
        
        palette = manager._extract_color_palette(img, n_colors=3)
        
        self.assertEqual(len(palette), 3)
        self.assertIsInstance(palette[0], tuple)
        self.assertEqual(len(palette[0]), 3)  # RGB
    
    def test_color_distance(self):
        """Test color distance calculation."""
        manager = StyleConsistencyManager(
            style_library_dir=self.style_lib_dir,
            device="cpu"
        )
        
        # Same color
        dist1 = manager._color_distance((255, 0, 0), (255, 0, 0))
        self.assertEqual(dist1, 0.0)
        
        # Different colors
        dist2 = manager._color_distance((255, 0, 0), (0, 255, 0))
        self.assertGreater(dist2, 0)
        
        # Black and white
        dist3 = manager._color_distance((0, 0, 0), (255, 255, 255))
        self.assertAlmostEqual(dist3, np.sqrt(3 * 255**2), places=1)
    
    def test_extract_style_tags(self):
        """Test style tag extraction from prompt."""
        manager = StyleConsistencyManager(
            style_library_dir=self.style_lib_dir,
            device="cpu"
        )
        
        # Test with cinematic prompt
        tags1 = manager._extract_style_tags("cinematic dramatic lighting")
        self.assertIn("cinematic", tags1)
        
        # Test with multiple tags
        tags2 = manager._extract_style_tags("vibrant colorful anime style")
        self.assertIn("vibrant", tags2)
        self.assertIn("colorful", tags2)
        self.assertIn("anime", tags2)
        
        # Test with no tags
        tags3 = manager._extract_style_tags("a simple scene")
        self.assertEqual(len(tags3), 0)
    
    def test_calculate_color_similarity(self):
        """Test color similarity calculation."""
        manager = StyleConsistencyManager(
            style_library_dir=self.style_lib_dir,
            device="cpu"
        )
        
        # Create similar images
        img1 = Image.new('RGB', (100, 100), color='red')
        img2 = Image.new('RGB', (100, 100), color='red')
        
        similarity = manager._calculate_color_similarity([img1, img2])
        
        # Should be high similarity for identical images
        self.assertGreater(similarity, 0.9)
        
        # Test with different images
        img3 = Image.new('RGB', (100, 100), color='blue')
        similarity2 = manager._calculate_color_similarity([img1, img3])
        
        # Should be lower similarity
        self.assertLess(similarity2, similarity)
    
    def test_calculate_structural_similarity(self):
        """Test structural similarity calculation."""
        manager = StyleConsistencyManager(
            style_library_dir=self.style_lib_dir,
            device="cpu"
        )
        
        # Create identical images
        img1 = Image.new('RGB', (100, 100), color='gray')
        img2 = Image.new('RGB', (100, 100), color='gray')
        
        similarity = manager._calculate_structural_similarity([img1, img2])
        
        # Should be high for identical images
        self.assertGreater(similarity, 0.95)
    
    def test_validate_consistency(self):
        """Test consistency validation."""
        manager = StyleConsistencyManager(
            style_library_dir=self.style_lib_dir,
            device="cpu"
        )
        
        # Create test images
        img_paths = []
        for i in range(3):
            img_path = Path(self.temp_dir) / f"test_{i}.png"
            img = Image.new('RGB', (100, 100), color='red')
            img.save(img_path)
            img_paths.append(img_path)
        
        # Validate consistency
        metrics = manager.validate_consistency(img_paths)
        
        # Check metrics
        self.assertIsInstance(metrics, ConsistencyMetrics)
        self.assertGreaterEqual(metrics.overall_score, 0.0)
        self.assertLessEqual(metrics.overall_score, 1.0)
        self.assertEqual(len(metrics.frame_scores), 3)
    
    def test_validate_consistency_with_single_image(self):
        """Test consistency validation with single image."""
        manager = StyleConsistencyManager(
            style_library_dir=self.style_lib_dir,
            device="cpu"
        )
        
        # Create single test image
        img_path = Path(self.temp_dir) / "single.png"
        img = Image.new('RGB', (100, 100), color='blue')
        img.save(img_path)
        
        metrics = manager.validate_consistency([img_path])
        
        # Should return perfect score for single image
        self.assertEqual(metrics.overall_score, 1.0)
    
    def test_get_style_profiles_no_filter(self):
        """Test getting all style profiles."""
        manager = StyleConsistencyManager(
            style_library_dir=self.style_lib_dir,
            device="cpu"
        )
        
        # Add test profiles
        manager.style_profiles["style1"] = StyleProfile(
            "style1", "/path1.png", "prompt1", style_tags=["cinematic"]
        )
        manager.style_profiles["style2"] = StyleProfile(
            "style2", "/path2.png", "prompt2", style_tags=["anime"]
        )
        
        profiles = manager.get_style_profiles()
        self.assertEqual(len(profiles), 2)
    
    def test_get_style_profiles_with_filter(self):
        """Test getting filtered style profiles."""
        manager = StyleConsistencyManager(
            style_library_dir=self.style_lib_dir,
            device="cpu"
        )
        
        # Add test profiles
        manager.style_profiles["style1"] = StyleProfile(
            "style1", "/path1.png", "prompt1", style_tags=["cinematic"]
        )
        manager.style_profiles["style2"] = StyleProfile(
            "style2", "/path2.png", "prompt2", style_tags=["anime"]
        )
        
        # Filter by tag
        cinematic_profiles = manager.get_style_profiles(tags=["cinematic"])
        self.assertEqual(len(cinematic_profiles), 1)
        self.assertEqual(cinematic_profiles[0].name, "style1")
    
    def test_export_import_style_library(self):
        """Test exporting and importing style library."""
        manager = StyleConsistencyManager(
            style_library_dir=self.style_lib_dir,
            device="cpu"
        )
        
        # Add test profiles
        manager.style_profiles["export_style"] = StyleProfile(
            "export_style",
            "/path/export.png",
            "export prompt",
            color_palette=[(100, 150, 200)],
            style_tags=["test"]
        )
        
        # Export
        export_path = Path(self.temp_dir) / "library.json"
        manager.export_style_library(export_path)
        
        # Verify export file
        self.assertTrue(export_path.exists())
        with open(export_path, 'r') as f:
            data = json.load(f)
            self.assertIn("export_style", data)
        
        # Clear profiles
        manager.style_profiles.clear()
        
        # Import
        manager.import_style_library(export_path)
        
        # Verify import
        self.assertIn("export_style", manager.style_profiles)
        imported = manager.style_profiles["export_style"]
        self.assertEqual(imported.color_palette, [(100, 150, 200)])
    
    @patch('core.pipeline.style_consistency.StyleConsistencyManager.pipe')
    def test_generate_with_style(self, mock_pipe):
        """Test generating keyframes with style."""
        manager = StyleConsistencyManager(
            style_library_dir=self.style_lib_dir,
            device="cpu"
        )
        
        # Create style profile
        ref_img_path = Path(self.temp_dir) / "ref.png"
        ref_img = Image.new('RGB', (100, 100), color='blue')
        ref_img.save(ref_img_path)
        
        manager.style_profiles["test_style"] = StyleProfile(
            "test_style",
            str(ref_img_path),
            "test prompt",
            style_tags=["test"]
        )
        
        # Mock pipeline
        mock_image = Image.new('RGB', (100, 100), color='green')
        mock_result = MagicMock()
        mock_result.images = [mock_image]
        mock_pipe.return_value = mock_result
        
        # Set _has_ip_adapter
        manager._has_ip_adapter = False
        
        # Generate
        output_dir = Path(self.temp_dir) / "output"
        prompts = ["prompt 1", "prompt 2"]
        result_paths = manager.generate_with_style(
            prompts,
            "test_style",
            output_dir
        )
        
        # Verify
        self.assertEqual(len(result_paths), 2)
        self.assertTrue(all(p.exists() for p in result_paths))
    
    def test_generate_with_style_missing_profile(self):
        """Test generating with non-existent style profile."""
        manager = StyleConsistencyManager(
            style_library_dir=self.style_lib_dir,
            device="cpu"
        )
        
        with self.assertRaises(ValueError) as ctx:
            manager.generate_with_style(
                ["prompt"],
                "nonexistent_style",
                Path(self.temp_dir) / "output"
            )
        
        self.assertIn("not found", str(ctx.exception))


class TestStyleConsistencyIntegration(unittest.TestCase):
    """Integration tests for style consistency workflow."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.style_lib_dir = Path(self.temp_dir) / "styles"
    
    def tearDown(self):
        """Clean up test fixtures."""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    @patch('core.pipeline.style_consistency.StyleConsistencyManager.pipe')
    def test_full_workflow(self, mock_pipe):
        """Test complete workflow: create style -> generate -> validate."""
        # Initialize manager
        manager = StyleConsistencyManager(
            style_library_dir=self.style_lib_dir,
            device="cpu"
        )
        
        # Mock pipeline
        mock_image = Image.new('RGB', (100, 100), color='red')
        mock_result = MagicMock()
        mock_result.images = [mock_image]
        mock_pipe.return_value = mock_result
        manager._has_ip_adapter = False
        
        # Create style reference
        ref_path = Path(self.temp_dir) / "style_ref.png"
        profile = manager.create_style_reference(
            "cinematic style",
            "cinematic",
            ref_path
        )
        
        # Generate keyframes
        output_dir = Path(self.temp_dir) / "keyframes"
        prompts = ["scene 1", "scene 2", "scene 3"]
        keyframe_paths = manager.generate_with_style(
            prompts,
            "cinematic",
            output_dir
        )
        
        # Validate consistency
        report_path = Path(self.temp_dir) / "report.json"
        metrics = manager.validate_consistency(keyframe_paths, report_path)
        
        # Verify
        self.assertEqual(len(keyframe_paths), 3)
        self.assertIsInstance(metrics, ConsistencyMetrics)
        self.assertTrue(report_path.exists())
        
        # Export library
        library_path = Path(self.temp_dir) / "library.json"
        manager.export_style_library(library_path)
        self.assertTrue(library_path.exists())


if __name__ == '__main__':
    unittest.main()
