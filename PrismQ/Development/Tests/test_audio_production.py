"""
Tests for audio production module.
"""

import pytest
import tempfile
import json
from pathlib import Path
from unittest.mock import Mock, MagicMock, patch
import subprocess

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'core'))

from audio_production import (
    AudioMetadata, VoiceoverAudio, TTSGenerator, AudioNormalizer, produce_audio
)


@pytest.fixture
def sample_script():
    """Sample script for testing."""
    return {
        'script_id': 'test_script_001',
        'content': 'This is a test script for audio generation. It should be converted to speech.',
        'title': 'Test Script',
        'target_gender': 'women',
        'target_age': '18-23',
        'version': 1
    }


@pytest.fixture
def mock_audio_file():
    """Create a mock audio file for testing."""
    with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as f:
        # Write some dummy data
        f.write(b'ID3\x04\x00\x00\x00\x00\x00\x00' + b'\x00' * 1000)
        return f.name


class TestAudioMetadata:
    """Test AudioMetadata dataclass."""
    
    def test_audio_metadata_creation(self):
        """Test audio metadata object creation."""
        metadata = AudioMetadata(
            duration_seconds=30.5,
            sample_rate=44100,
            channels=1,
            lufs=-14.2
        )
        
        assert metadata.duration_seconds == 30.5
        assert metadata.sample_rate == 44100
        assert metadata.lufs == -14.2
    
    def test_metadata_to_dict(self):
        """Test metadata to dictionary conversion."""
        metadata = AudioMetadata(duration_seconds=30.0)
        data = metadata.to_dict()
        
        assert 'duration_seconds' in data
        assert data['duration_seconds'] == 30.0


class TestVoiceoverAudio:
    """Test VoiceoverAudio dataclass."""
    
    def test_voiceover_audio_creation(self):
        """Test voiceover audio object creation."""
        metadata = AudioMetadata(duration_seconds=25.5)
        audio = VoiceoverAudio(
            audio_id="test_001_tts",
            script_id="test_001",
            content_text="Test content",
            voice_gender="female",
            voice_provider="elevenlabs",
            metadata=metadata
        )
        
        assert audio.audio_id == "test_001_tts"
        assert audio.voice_gender == "female"
        assert audio.metadata.duration_seconds == 25.5
    
    def test_voiceover_to_dict(self):
        """Test voiceover to dictionary conversion."""
        audio = VoiceoverAudio(
            audio_id="test_001_tts",
            script_id="test_001",
            content_text="Test",
            voice_gender="male",
            voice_provider="openai"
        )
        
        data = audio.to_dict()
        
        assert data['audio_id'] == "test_001_tts"
        assert data['voice_gender'] == "male"
        assert 'metadata' in data
    
    def test_voiceover_to_json(self):
        """Test voiceover to JSON conversion."""
        audio = VoiceoverAudio(
            audio_id="test_001_tts",
            script_id="test_001",
            content_text="Test",
            voice_gender="female",
            voice_provider="elevenlabs"
        )
        
        json_str = audio.to_json()
        data = json.loads(json_str)
        
        assert data['audio_id'] == "test_001_tts"
        assert isinstance(json_str, str)


class TestTTSGenerator:
    """Test TTSGenerator class."""
    
    def test_generator_initialization(self):
        """Test TTS generator initialization."""
        with tempfile.TemporaryDirectory() as tmpdir:
            generator = TTSGenerator(
                provider="mock",
                output_root=tmpdir
            )
            
            assert generator.provider == "mock"
            assert generator.output_root == Path(tmpdir)
    
    def test_select_voice_elevenlabs(self):
        """Test voice selection for ElevenLabs."""
        generator = TTSGenerator(provider="elevenlabs")
        
        female_voice = generator._select_voice("female")
        male_voice = generator._select_voice("male")
        
        assert female_voice
        assert male_voice
        assert female_voice != male_voice
    
    def test_select_voice_openai(self):
        """Test voice selection for OpenAI."""
        generator = TTSGenerator(provider="openai")
        
        female_voice = generator._select_voice("female")
        male_voice = generator._select_voice("male")
        
        assert female_voice == "nova"
        assert male_voice == "onyx"
    
    @patch('subprocess.run')
    def test_get_audio_metadata(self, mock_run):
        """Test audio metadata extraction."""
        # Mock ffprobe output
        mock_run.return_value = Mock(
            returncode=0,
            stdout="30.5\n"
        )
        
        generator = TTSGenerator(provider="mock")
        
        with tempfile.NamedTemporaryFile(suffix='.mp3') as f:
            f.write(b'test')
            f.flush()
            
            metadata = generator._get_audio_metadata(Path(f.name))
            
            assert metadata.duration_seconds == 30.5
    
    def test_generate_tts_mock(self, sample_script):
        """Test TTS generation with mock provider."""
        with tempfile.TemporaryDirectory() as tmpdir:
            generator = TTSGenerator(
                provider="mock",
                output_root=tmpdir
            )
            
            with patch.object(generator, '_get_audio_metadata') as mock_metadata:
                mock_metadata.return_value = AudioMetadata(duration_seconds=25.0)
                
                audio = generator.generate_tts(
                    script=sample_script,
                    voice_gender="female"
                )
                
                assert audio.script_id == "test_script_001"
                assert audio.voice_gender == "female"
                assert audio.raw_path
                assert Path(audio.raw_path).exists()
    
    def test_save_raw_audio(self, sample_script):
        """Test saving raw TTS audio."""
        with tempfile.TemporaryDirectory() as tmpdir:
            generator = TTSGenerator(output_root=tmpdir)
            
            audio_data = b"MOCK_AUDIO_DATA"
            path = generator._save_raw_audio(
                audio_data=audio_data,
                script_id="test_001",
                target_gender="women",
                target_age="18-23"
            )
            
            assert path.exists()
            assert path.suffix == '.mp3'
            
            with open(path, 'rb') as f:
                assert f.read() == audio_data


class TestAudioNormalizer:
    """Test AudioNormalizer class."""
    
    def test_normalizer_initialization(self):
        """Test audio normalizer initialization."""
        with tempfile.TemporaryDirectory() as tmpdir:
            normalizer = AudioNormalizer(output_root=tmpdir)
            
            assert normalizer.output_root == Path(tmpdir)
    
    @patch('subprocess.run')
    def test_measure_lufs(self, mock_run):
        """Test LUFS measurement."""
        # Mock ffmpeg loudnorm output
        mock_output = """
        [Parsed_loudnorm_0 @ 0x123] {
          "input_i": "-18.50",
          "input_tp": "-3.20",
          "input_lra": "7.50",
          "input_thresh": "-28.90",
          "output_i": "-14.00",
          "output_tp": "-1.00",
          "output_lra": "7.50",
          "output_thresh": "-24.40"
        }
        """
        mock_run.return_value = Mock(
            returncode=0,
            stderr=mock_output
        )
        
        normalizer = AudioNormalizer()
        
        with tempfile.NamedTemporaryFile(suffix='.mp3') as f:
            lufs = normalizer._measure_lufs(Path(f.name))
            
            assert lufs == -18.5
    
    @patch('subprocess.run')
    def test_normalize_audio(self, mock_run):
        """Test audio normalization."""
        # Mock successful ffmpeg commands
        mock_run.return_value = Mock(
            returncode=0,
            stderr='{"input_i": "-20.0"}',
            stdout=""
        )
        
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create mock raw audio file
            raw_dir = Path(tmpdir) / "tts" / "women" / "18-23" / "raw"
            raw_dir.mkdir(parents=True)
            raw_path = raw_dir / "test_001.mp3"
            raw_path.write_bytes(b"MOCK_AUDIO")
            
            # Create voiceover audio object
            audio = VoiceoverAudio(
                audio_id="test_001_tts",
                script_id="test_001",
                content_text="Test",
                voice_gender="female",
                voice_provider="mock",
                raw_path=str(raw_path)
            )
            
            normalizer = AudioNormalizer(output_root=tmpdir)
            
            # Mock the actual ffmpeg file creation
            with patch.object(normalizer, '_apply_loudnorm') as mock_apply:
                def create_output(input_path, output_path, target_lufs, true_peak):
                    output_path.write_bytes(b"NORMALIZED_AUDIO")
                
                mock_apply.side_effect = create_output
                
                normalized = normalizer.normalize_audio(audio, target_lufs=-14.0)
                
                assert normalized.normalized_path
                assert Path(normalized.normalized_path).exists()
    
    def test_normalize_audio_missing_file(self):
        """Test normalization with missing file."""
        audio = VoiceoverAudio(
            audio_id="test_001_tts",
            script_id="test_001",
            content_text="Test",
            voice_gender="female",
            voice_provider="mock",
            raw_path="/nonexistent/file.mp3"
        )
        
        normalizer = AudioNormalizer()
        
        with pytest.raises(FileNotFoundError):
            normalizer.normalize_audio(audio)


class TestProduceAudio:
    """Test complete audio production workflow."""
    
    @patch('subprocess.run')
    def test_produce_audio_workflow(self, mock_run, sample_script):
        """Test complete audio production workflow."""
        # Mock ffmpeg/ffprobe commands - need different returns for different calls
        mock_returns = [
            Mock(returncode=0, stdout="25.0\n", stderr=""),  # get_audio_metadata for raw
            Mock(returncode=0, stderr='{"input_i": "-18.0"}'),  # measure_lufs (first)
            Mock(returncode=0, stderr='{"input_i": "-18.0"}'),  # apply_loudnorm (first pass)
            Mock(returncode=0, stderr=""),  # apply_loudnorm (second pass)
            Mock(returncode=0, stderr='{"input_i": "-14.0"}'),  # measure_lufs (final)
        ]
        mock_run.side_effect = mock_returns
        
        with tempfile.TemporaryDirectory() as tmpdir:
            # Mock TTS generation
            with patch('core.audio_production.TTSGenerator._generate_audio') as mock_gen:
                mock_gen.return_value = b"MOCK_AUDIO_DATA"
                
                audio = produce_audio(
                    script=sample_script,
                    tts_provider="mock",
                    voice_gender="female",
                    target_lufs=-14.0,
                    output_root=tmpdir
                )
                
                assert audio.script_id == "test_script_001"
                assert audio.raw_path
                assert audio.normalized_path
                assert Path(audio.raw_path).exists()
                # The normalized file will be created by ffmpeg subprocess, which we're mocking
                # In a real scenario it would exist, but in test we just verify the path is set


class TestIntegration:
    """Integration tests."""
    
    @patch('subprocess.run')
    def test_full_pipeline(self, mock_run, sample_script):
        """Test full audio production pipeline."""
        mock_run.return_value = Mock(
            returncode=0,
            stdout="30.0\n",
            stderr='{"input_i": "-20.0"}'
        )
        
        with tempfile.TemporaryDirectory() as tmpdir:
            # Generate TTS
            generator = TTSGenerator(provider="mock", output_root=tmpdir)
            
            with patch.object(generator, '_get_audio_metadata') as mock_metadata:
                mock_metadata.return_value = AudioMetadata(duration_seconds=30.0)
                
                audio = generator.generate_tts(sample_script, voice_gender="female")
                
                assert audio.raw_path
                
                # Normalize
                normalizer = AudioNormalizer(output_root=tmpdir)
                
                with patch.object(normalizer, '_apply_loudnorm') as mock_apply:
                    def create_output(input_path, output_path, target_lufs, true_peak):
                        output_path.write_bytes(b"NORMALIZED")
                    
                    mock_apply.side_effect = create_output
                    
                    normalized = normalizer.normalize_audio(audio)
                    
                    assert normalized.normalized_path
                    assert Path(normalized.normalized_path).exists()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
