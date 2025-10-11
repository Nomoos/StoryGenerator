"""
Unit tests for Voice Cloning System

Tests cover:
- Voice cloning from reference samples
- Voice profile storage and retrieval
- TTS synthesis with cloned voices
- Voice quality validation
- A/B testing framework
- Demographic filtering
"""

import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
import numpy as np

from PrismQ.VoiceOverGenerator.voice_cloning import (
    VoiceCloner,
    VoiceProfile,
    VoiceQualityMetrics
)


class TestVoiceProfile(unittest.TestCase):
    """Test VoiceProfile dataclass."""
    
    def test_voice_profile_creation(self):
        """Test creating a voice profile."""
        embedding = [0.1, 0.2, 0.3]
        profile = VoiceProfile(
            name="test_voice",
            gender="Male",
            age_bracket="25-35",
            embedding=embedding,
            reference_audio_path="/path/to/audio.wav",
            quality_score=0.85
        )
        
        self.assertEqual(profile.name, "test_voice")
        self.assertEqual(profile.gender, "Male")
        self.assertEqual(profile.age_bracket, "25-35")
        self.assertEqual(profile.embedding, embedding)
        self.assertEqual(profile.quality_score, 0.85)
    
    def test_voice_profile_to_dict(self):
        """Test converting profile to dictionary."""
        profile = VoiceProfile(
            name="test_voice",
            gender="Female",
            age_bracket="18-25",
            embedding=[0.1, 0.2],
            reference_audio_path="/path/to/audio.wav"
        )
        
        profile_dict = profile.to_dict()
        self.assertIsInstance(profile_dict, dict)
        self.assertEqual(profile_dict['name'], "test_voice")
        self.assertEqual(profile_dict['gender'], "Female")
        self.assertIn('created_at', profile_dict)
    
    def test_voice_profile_from_dict(self):
        """Test creating profile from dictionary."""
        data = {
            'name': 'restored_voice',
            'gender': 'Male',
            'age_bracket': '36-50',
            'embedding': [0.5, 0.6],
            'reference_audio_path': '/path/audio.wav',
            'quality_score': 0.9,
            'created_at': '2024-01-01T00:00:00',
            'metadata': {}
        }
        
        profile = VoiceProfile.from_dict(data)
        self.assertEqual(profile.name, 'restored_voice')
        self.assertEqual(profile.gender, 'Male')
        self.assertEqual(profile.quality_score, 0.9)


class TestVoiceQualityMetrics(unittest.TestCase):
    """Test VoiceQualityMetrics dataclass."""
    
    def test_quality_metrics_creation(self):
        """Test creating quality metrics."""
        metrics = VoiceQualityMetrics(
            clarity_score=0.85,
            naturalness_score=0.80,
            similarity_score=0.90,
            overall_score=0.85
        )
        
        self.assertEqual(metrics.clarity_score, 0.85)
        self.assertEqual(metrics.naturalness_score, 0.80)
        self.assertEqual(metrics.similarity_score, 0.90)
        self.assertEqual(metrics.overall_score, 0.85)
    
    def test_quality_metrics_to_dict(self):
        """Test converting metrics to dictionary."""
        metrics = VoiceQualityMetrics(
            clarity_score=0.9,
            naturalness_score=0.85,
            similarity_score=0.95,
            overall_score=0.90
        )
        
        metrics_dict = metrics.to_dict()
        self.assertIsInstance(metrics_dict, dict)
        self.assertEqual(metrics_dict['clarity_score'], 0.9)
        self.assertEqual(metrics_dict['overall_score'], 0.90)


class TestVoiceCloner(unittest.TestCase):
    """Test VoiceCloner class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.profiles_dir = Path(self.temp_dir) / "voice_profiles"
        self.profiles_dir.mkdir(parents=True, exist_ok=True)
    
    def tearDown(self):
        """Clean up test fixtures."""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    @patch('core.pipeline.voice_cloning.VoiceCloner._load_existing_profiles')
    def test_voice_cloner_initialization(self, mock_load):
        """Test VoiceCloner initialization."""
        cloner = VoiceCloner(voice_profiles_dir=self.profiles_dir)
        
        self.assertEqual(cloner.model_name, "tts_models/multilingual/multi-dataset/xtts_v2")
        self.assertEqual(cloner.voice_profiles_dir, self.profiles_dir)
        self.assertIsInstance(cloner.voice_profiles, dict)
        mock_load.assert_called_once()
    
    @patch('core.pipeline.voice_cloning.VoiceCloner._extract_embedding')
    @patch('core.pipeline.voice_cloning.VoiceCloner._validate_voice_quality')
    @patch('core.pipeline.voice_cloning.VoiceCloner._save_profile')
    def test_clone_voice(self, mock_save, mock_validate, mock_extract):
        """Test voice cloning process."""
        # Setup mocks
        mock_extract.return_value = np.array([0.1, 0.2, 0.3])
        mock_validate.return_value = VoiceQualityMetrics(0.85, 0.80, 0.90, 0.85)
        
        # Create reference audio file
        ref_audio = Path(self.temp_dir) / "reference.wav"
        ref_audio.write_text("dummy audio")
        
        # Clone voice
        cloner = VoiceCloner(voice_profiles_dir=self.profiles_dir)
        profile = cloner.clone_voice(
            reference_audio=ref_audio,
            voice_name="test_voice",
            target_gender="Male",
            target_age="25-35"
        )
        
        # Verify profile
        self.assertEqual(profile.name, "test_voice")
        self.assertEqual(profile.gender, "Male")
        self.assertEqual(profile.age_bracket, "25-35")
        self.assertEqual(profile.quality_score, 0.85)
        
        # Verify mocks called
        mock_extract.assert_called_once()
        mock_validate.assert_called_once()
        mock_save.assert_called_once()
        
        # Verify profile stored
        self.assertIn("test_voice", cloner.voice_profiles)
    
    @patch('core.pipeline.voice_cloning.VoiceCloner._load_existing_profiles')
    def test_clone_voice_file_not_found(self, mock_load):
        """Test cloning with non-existent reference audio."""
        cloner = VoiceCloner(voice_profiles_dir=self.profiles_dir)
        
        with self.assertRaises(FileNotFoundError):
            cloner.clone_voice(
                reference_audio=Path("/nonexistent/audio.wav"),
                voice_name="test",
                target_gender="Male",
                target_age="25-35"
            )
    
    @patch('core.pipeline.voice_cloning.VoiceCloner._load_existing_profiles')
    def test_save_and_load_profile(self, mock_load):
        """Test saving and loading voice profiles."""
        cloner = VoiceCloner(voice_profiles_dir=self.profiles_dir)
        
        # Create a profile
        profile = VoiceProfile(
            name="saved_voice",
            gender="Female",
            age_bracket="18-25",
            embedding=[0.1, 0.2, 0.3],
            reference_audio_path="/path/to/audio.wav",
            quality_score=0.88
        )
        
        # Save profile
        cloner._save_profile(profile)
        
        # Verify file created
        profile_file = self.profiles_dir / "saved_voice_profile.json"
        self.assertTrue(profile_file.exists())
        
        # Verify content
        with open(profile_file, 'r') as f:
            data = json.load(f)
            self.assertEqual(data['name'], 'saved_voice')
            self.assertEqual(data['gender'], 'Female')
    
    @patch('core.pipeline.voice_cloning.VoiceCloner.tts')
    def test_synthesize_with_voice(self, mock_tts):
        """Test speech synthesis with cloned voice."""
        # Setup
        cloner = VoiceCloner(voice_profiles_dir=self.profiles_dir)
        
        # Add a voice profile
        profile = VoiceProfile(
            name="synth_voice",
            gender="Male",
            age_bracket="25-35",
            embedding=[0.1, 0.2, 0.3],
            reference_audio_path="/path/audio.wav"
        )
        cloner.voice_profiles["synth_voice"] = profile
        
        # Mock TTS
        mock_tts.tts_to_file = Mock()
        
        # Synthesize
        output_path = Path(self.temp_dir) / "output.wav"
        result = cloner.synthesize_with_voice(
            text="Hello world",
            voice_name="synth_voice",
            output_path=output_path
        )
        
        # Verify
        self.assertEqual(result, output_path)
        mock_tts.tts_to_file.assert_called_once()
    
    @patch('core.pipeline.voice_cloning.VoiceCloner._load_existing_profiles')
    def test_synthesize_with_unknown_voice(self, mock_load):
        """Test synthesis with unknown voice raises error."""
        cloner = VoiceCloner(voice_profiles_dir=self.profiles_dir)
        
        with self.assertRaises(ValueError) as ctx:
            cloner.synthesize_with_voice(
                text="Test",
                voice_name="unknown_voice",
                output_path=Path(self.temp_dir) / "out.wav"
            )
        
        self.assertIn("not found", str(ctx.exception))
    
    @patch('core.pipeline.voice_cloning.VoiceCloner._load_existing_profiles')
    def test_get_profiles_by_demographic(self, mock_load):
        """Test filtering profiles by demographic."""
        cloner = VoiceCloner(voice_profiles_dir=self.profiles_dir)
        
        # Add multiple profiles
        cloner.voice_profiles["voice1"] = VoiceProfile(
            "voice1", "Male", "18-25", [0.1], "/path1.wav"
        )
        cloner.voice_profiles["voice2"] = VoiceProfile(
            "voice2", "Female", "25-35", [0.2], "/path2.wav"
        )
        cloner.voice_profiles["voice3"] = VoiceProfile(
            "voice3", "Male", "25-35", [0.3], "/path3.wav"
        )
        
        # Test gender filter
        male_profiles = cloner.get_profiles_by_demographic(gender="Male")
        self.assertEqual(len(male_profiles), 2)
        
        # Test age filter
        young_profiles = cloner.get_profiles_by_demographic(age_bracket="18-25")
        self.assertEqual(len(young_profiles), 1)
        
        # Test combined filter
        male_mid = cloner.get_profiles_by_demographic(
            gender="Male",
            age_bracket="25-35"
        )
        self.assertEqual(len(male_mid), 1)
        self.assertEqual(male_mid[0].name, "voice3")
    
    @patch('core.pipeline.voice_cloning.VoiceCloner.synthesize_with_voice')
    def test_compare_voices(self, mock_synthesize):
        """Test A/B testing voice comparison."""
        cloner = VoiceCloner(voice_profiles_dir=self.profiles_dir)
        
        # Add test voices
        cloner.voice_profiles["voice_a"] = VoiceProfile(
            "voice_a", "Male", "25-35", [0.1], "/path_a.wav"
        )
        cloner.voice_profiles["voice_b"] = VoiceProfile(
            "voice_b", "Female", "25-35", [0.2], "/path_b.wav"
        )
        
        # Mock synthesis
        def mock_synth(text, voice_name, output_path, **kwargs):
            return output_path
        mock_synthesize.side_effect = mock_synth
        
        # Run comparison
        output_dir = Path(self.temp_dir) / "ab_test"
        results = cloner.compare_voices(
            voice_names=["voice_a", "voice_b"],
            test_text="Test text",
            output_dir=output_dir
        )
        
        # Verify
        self.assertEqual(len(results), 2)
        self.assertIn("voice_a", results)
        self.assertIn("voice_b", results)
        self.assertEqual(mock_synthesize.call_count, 2)
    
    @patch('core.pipeline.voice_cloning.VoiceCloner._load_existing_profiles')
    def test_export_import_profiles(self, mock_load):
        """Test exporting and importing voice profiles."""
        cloner = VoiceCloner(voice_profiles_dir=self.profiles_dir)
        
        # Add profiles
        cloner.voice_profiles["export_voice"] = VoiceProfile(
            "export_voice", "Male", "25-35", [0.5, 0.6], "/path.wav", 0.9
        )
        
        # Export
        export_path = Path(self.temp_dir) / "exported_profiles.json"
        cloner.export_profiles(export_path)
        
        # Verify export file
        self.assertTrue(export_path.exists())
        with open(export_path, 'r') as f:
            data = json.load(f)
            self.assertIn("export_voice", data)
        
        # Clear profiles
        cloner.voice_profiles.clear()
        
        # Import
        cloner.import_profiles(export_path)
        
        # Verify import
        self.assertIn("export_voice", cloner.voice_profiles)
        imported = cloner.voice_profiles["export_voice"]
        self.assertEqual(imported.quality_score, 0.9)
    
    def test_validate_voice_quality(self):
        """Test voice quality validation."""
        cloner = VoiceCloner(voice_profiles_dir=self.profiles_dir)
        
        embedding = np.array([0.1, 0.2, 0.3])
        ref_audio = Path(self.temp_dir) / "reference.wav"
        ref_audio.write_text("dummy")
        
        metrics = cloner._validate_voice_quality(embedding, ref_audio)
        
        # Check metrics are in valid range
        self.assertGreaterEqual(metrics.clarity_score, 0.0)
        self.assertLessEqual(metrics.clarity_score, 1.0)
        self.assertGreaterEqual(metrics.overall_score, 0.0)
        self.assertLessEqual(metrics.overall_score, 1.0)


class TestVoiceClonerIntegration(unittest.TestCase):
    """Integration tests for voice cloning workflow."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.profiles_dir = Path(self.temp_dir) / "profiles"
    
    def tearDown(self):
        """Clean up test fixtures."""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    @patch('core.pipeline.voice_cloning.VoiceCloner._extract_embedding')
    @patch('core.pipeline.voice_cloning.VoiceCloner.tts')
    def test_full_voice_cloning_workflow(self, mock_tts, mock_extract):
        """Test complete workflow: clone -> save -> synthesize."""
        # Setup mocks
        mock_extract.return_value = np.array([0.1, 0.2, 0.3])
        mock_tts.tts_to_file = Mock()
        
        # Create reference audio
        ref_audio = Path(self.temp_dir) / "reference.wav"
        ref_audio.write_text("dummy audio")
        
        # Initialize cloner
        cloner = VoiceCloner(voice_profiles_dir=self.profiles_dir)
        
        # Clone voice
        profile = cloner.clone_voice(
            reference_audio=ref_audio,
            voice_name="workflow_voice",
            target_gender="Female",
            target_age="18-25",
            metadata={"source": "test"}
        )
        
        # Verify profile created
        self.assertEqual(profile.name, "workflow_voice")
        self.assertEqual(profile.metadata["source"], "test")
        
        # Synthesize with cloned voice
        output_path = Path(self.temp_dir) / "synthesized.wav"
        result = cloner.synthesize_with_voice(
            text="Test synthesis",
            voice_name="workflow_voice",
            output_path=output_path
        )
        
        # Verify synthesis called
        mock_tts.tts_to_file.assert_called_once()
        
        # Export profiles
        export_path = Path(self.temp_dir) / "backup.json"
        cloner.export_profiles(export_path)
        
        # Verify export
        self.assertTrue(export_path.exists())


if __name__ == '__main__':
    unittest.main()
