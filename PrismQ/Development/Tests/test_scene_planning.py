"""
Tests for scene planning module - beat sheets, shot lists, and draft subtitles.
"""

import pytest
import tempfile
import json
from pathlib import Path

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'core'))

from scene_planning import ScenePlanner, BeatSheet, Shot, SubtitleEntry


@pytest.fixture
def scene_planner():
    """Create scene planner with temp directory."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield ScenePlanner(output_root=tmpdir)


@pytest.fixture
def sample_script():
    """Sample script text for testing."""
    return """In a world where books are banned, one woman fights to preserve knowledge. 
She discovers a hidden library beneath the city. 
Every night, she risks her life to share stories with those who dare to listen. 
But the authorities are closing in. 
Will she escape, or will the last library burn?"""


class TestScenePlanner:
    """Test ScenePlanner functionality."""
    
    def test_split_into_sentences(self, scene_planner, sample_script):
        """Test sentence splitting."""
        sentences = scene_planner.split_into_sentences(sample_script)
        
        assert len(sentences) == 5
        assert "In a world where books are banned" in sentences[0]
        assert "hidden library" in sentences[1]
    
    def test_estimate_duration(self, scene_planner):
        """Test duration estimation."""
        # Test with 150 words - should be ~60 seconds
        text = " ".join(["word"] * 150)
        duration = scene_planner.estimate_duration(text)
        
        assert 58 <= duration <= 62  # Allow some variance
    
    def test_generate_beat_sheet(self, scene_planner, sample_script):
        """Test beat sheet generation."""
        beat_sheet = scene_planner.generate_beat_sheet(
            script_text=sample_script,
            title_id="test_001",
            total_duration=30.0
        )
        
        assert beat_sheet.title_id == "test_001"
        assert beat_sheet.total_duration == 30.0
        assert beat_sheet.total_shots > 0
        assert len(beat_sheet.shots) == beat_sheet.total_shots
        
        # Check shots are sequential and cover full duration
        assert beat_sheet.shots[0].start_time == 0.0
        assert beat_sheet.shots[-1].end_time == 30.0
        
        # Check each shot has required fields
        for shot in beat_sheet.shots:
            assert shot.shot_number > 0
            assert shot.duration > 0
            assert shot.narration
            assert shot.visual_prompt
            assert shot.scene_description
    
    def test_beat_sheet_to_json(self, scene_planner, sample_script):
        """Test beat sheet JSON serialization."""
        beat_sheet = scene_planner.generate_beat_sheet(
            script_text=sample_script,
            title_id="test_001",
            total_duration=30.0
        )
        
        json_str = beat_sheet.to_json()
        data = json.loads(json_str)
        
        assert data['titleId'] == "test_001"
        assert data['totalDuration'] == 30.0
        assert 'shots' in data
        assert len(data['shots']) > 0
    
    def test_generate_draft_subtitles(self, scene_planner, sample_script):
        """Test draft subtitle generation."""
        subtitles = scene_planner.generate_draft_subtitles(
            script_text=sample_script,
            total_duration=30.0
        )
        
        assert len(subtitles) > 0
        
        # Check subtitle structure
        for i, sub in enumerate(subtitles):
            assert sub.index == i + 1
            assert sub.start_time >= 0
            assert sub.end_time > sub.start_time
            assert sub.text
            assert len(sub.text) <= scene_planner.MAX_CHARS_PER_SUBTITLE + 10  # Some tolerance
        
        # Check timing is sequential
        for i in range(len(subtitles) - 1):
            assert subtitles[i].end_time <= subtitles[i + 1].start_time + 0.1  # Small overlap OK
    
    def test_subtitle_srt_format(self, scene_planner):
        """Test SRT format generation."""
        subtitle = SubtitleEntry(
            index=1,
            start_time=0.0,
            end_time=5.5,
            text="Test subtitle"
        )
        
        srt_block = subtitle.to_srt_block()
        
        assert "1\n" in srt_block
        assert "00:00:00,000 --> 00:00:05,500" in srt_block
        assert "Test subtitle" in srt_block
    
    def test_save_beat_sheet(self, scene_planner, sample_script):
        """Test saving beat sheet to file."""
        beat_sheet = scene_planner.generate_beat_sheet(
            script_text=sample_script,
            title_id="test_001",
            total_duration=30.0
        )
        
        output_path = scene_planner.save_beat_sheet(
            beat_sheet=beat_sheet,
            gender="women",
            age="18-24"
        )
        
        assert output_path.exists()
        assert output_path.name == "test_001_shots.json"
        
        # Verify content
        with open(output_path, 'r') as f:
            data = json.load(f)
            assert data['titleId'] == "test_001"
    
    def test_save_draft_subtitles(self, scene_planner, sample_script):
        """Test saving draft subtitles to file."""
        subtitles = scene_planner.generate_draft_subtitles(
            script_text=sample_script,
            total_duration=30.0
        )
        
        output_path = scene_planner.save_draft_subtitles(
            subtitles=subtitles,
            title_id="test_001",
            gender="women",
            age="18-24"
        )
        
        assert output_path.exists()
        assert output_path.name == "test_001_draft.srt"
        
        # Verify SRT format
        content = output_path.read_text()
        assert "1\n" in content
        assert "-->" in content
    
    def test_generate_scene_plan(self, scene_planner, sample_script):
        """Test complete scene plan generation."""
        paths = scene_planner.generate_scene_plan(
            script_text=sample_script,
            title_id="test_001",
            gender="women",
            age="18-24",
            total_duration=30.0
        )
        
        assert 'beat_sheet' in paths
        assert 'subtitles' in paths
        assert paths['beat_sheet'].exists()
        assert paths['subtitles'].exists()
    
    def test_long_text_subtitle_splitting(self, scene_planner):
        """Test that long text is split into proper subtitle chunks."""
        long_text = "This is a very long sentence that definitely exceeds the maximum character limit for subtitles and should be split into multiple subtitle entries automatically."
        
        subtitles = scene_planner.generate_draft_subtitles(
            script_text=long_text,
            total_duration=10.0
        )
        
        # Should be split into multiple subtitles
        assert len(subtitles) > 1
        
        # Each should be under limit (with some tolerance)
        for sub in subtitles:
            assert len(sub.text) <= scene_planner.MAX_CHARS_PER_SUBTITLE + 10


class TestShot:
    """Test Shot dataclass."""
    
    def test_shot_to_dict(self):
        """Test shot dictionary conversion."""
        shot = Shot(
            shot_number=1,
            start_time=0.0,
            end_time=5.0,
            duration=5.0,
            scene_description="Test scene",
            visual_prompt="Test prompt",
            narration="Test narration"
        )
        
        shot_dict = shot.to_dict()
        
        assert shot_dict['shotNumber'] == 1
        assert shot_dict['startTime'] == 0.0
        assert shot_dict['duration'] == 5.0


class TestSubtitleEntry:
    """Test SubtitleEntry dataclass."""
    
    def test_srt_timestamp_conversion(self):
        """Test SRT timestamp formatting."""
        subtitle = SubtitleEntry(1, 0.0, 5.5, "Test")
        
        timestamp = subtitle.to_srt_timestamp(65.5)
        assert timestamp == "00:01:05,500"
        
        timestamp = subtitle.to_srt_timestamp(3661.250)
        assert timestamp == "01:01:01,250"
    
    def test_srt_block_format(self):
        """Test SRT block formatting."""
        subtitle = SubtitleEntry(
            index=2,
            start_time=5.0,
            end_time=10.0,
            text="Second subtitle"
        )
        
        block = subtitle.to_srt_block()
        lines = block.split('\n')
        
        assert lines[0] == "2"
        assert "00:00:05,000 --> 00:00:10,000" in lines[1]
        assert lines[2] == "Second subtitle"


class TestBeatSheet:
    """Test BeatSheet dataclass."""
    
    def test_beat_sheet_to_dict(self):
        """Test beat sheet dictionary conversion."""
        shot = Shot(1, 0.0, 5.0, 5.0, "desc", "prompt", "narration")
        beat_sheet = BeatSheet(
            title_id="test_001",
            total_duration=30.0,
            total_shots=1,
            generated_at="2024-01-01T00:00:00Z",
            shots=[shot]
        )
        
        beat_dict = beat_sheet.to_dict()
        
        assert beat_dict['titleId'] == "test_001"
        assert beat_dict['totalDuration'] == 30.0
        assert len(beat_dict['shots']) == 1
    
    def test_beat_sheet_json_serialization(self):
        """Test beat sheet JSON conversion."""
        shot = Shot(1, 0.0, 5.0, 5.0, "desc", "prompt", "narration")
        beat_sheet = BeatSheet(
            title_id="test_001",
            total_duration=30.0,
            total_shots=1,
            generated_at="2024-01-01T00:00:00Z",
            shots=[shot]
        )
        
        json_str = beat_sheet.to_json()
        data = json.loads(json_str)
        
        assert isinstance(data, dict)
        assert data['titleId'] == "test_001"


if __name__ == "__main__":
    # Run tests with pytest
    pytest.main([__file__, "-v"])
