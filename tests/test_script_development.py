"""
Tests for script development module.
"""

import pytest
import tempfile
import json
from pathlib import Path
from unittest.mock import Mock, MagicMock

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'core'))

from script_development import (
    Script, ScriptQualityScores, ScriptGenerator, ScriptScorer,
    ScriptIterator, ScriptEnhancer, TitleOptimizer, develop_script
)


@pytest.fixture
def mock_llm_provider():
    """Create mock LLM provider."""
    mock = Mock()
    mock.model_name = "test-model"
    mock.generate_completion = MagicMock(return_value="Mock response")
    return mock


@pytest.fixture
def sample_idea():
    """Sample video idea for testing."""
    return {
        'id': 'test_idea_001',
        'content': 'A story about overcoming adversity through persistence',
        'title': 'Never Give Up',
        'target_gender': 'women',
        'target_age': '18-23'
    }


@pytest.fixture
def sample_script():
    """Sample script for testing."""
    content = """Have you ever felt like giving up? Like the world is against you? 
    
Let me tell you about Sarah. She failed her driving test five times. Five times! 
Her friends laughed. Her family worried. But Sarah? She kept going.

On her sixth try, she passed with flying colors. Why? Because she learned from every failure.

Your setbacks aren't stopping points. They're stepping stones. Keep pushing forward."""
    
    return Script(
        script_id="test_001",
        content=content,
        title="Never Give Up",
        target_gender="women",
        target_age="18-23",
        version=0,
        word_count=len(content.split()),
        estimated_duration=30.0
    )


class TestScriptQualityScores:
    """Test ScriptQualityScores dataclass."""
    
    def test_overall_score_calculation(self):
        """Test weighted overall score calculation."""
        scores = ScriptQualityScores(
            engagement=80.0,
            clarity=90.0,
            pacing=85.0,
            demographic_fit=75.0,
            storytelling=80.0,
            hook_strength=95.0
        )
        
        # Calculate expected weighted average
        expected = (80 * 0.25 + 90 * 0.15 + 85 * 0.15 + 75 * 0.15 + 80 * 0.20 + 95 * 0.10)
        
        assert abs(scores.overall_score - expected) < 0.1
        assert 75 <= scores.overall_score <= 90
    
    def test_to_dict(self):
        """Test conversion to dictionary."""
        scores = ScriptQualityScores(
            engagement=80.0,
            clarity=90.0,
            pacing=85.0,
            demographic_fit=75.0,
            storytelling=80.0,
            hook_strength=95.0
        )
        
        data = scores.to_dict()
        
        assert 'engagement' in data
        assert 'overall_score' in data
        assert data['engagement'] == 80.0
        assert isinstance(data['overall_score'], float)


class TestScript:
    """Test Script dataclass."""
    
    def test_script_creation(self, sample_script):
        """Test script object creation."""
        assert sample_script.script_id == "test_001"
        assert sample_script.version == 0
        assert sample_script.word_count > 0
        assert sample_script.estimated_duration > 0
    
    def test_script_to_dict(self, sample_script):
        """Test script to dictionary conversion."""
        data = sample_script.to_dict()
        
        assert data['script_id'] == "test_001"
        assert data['content']
        assert data['word_count'] > 0
    
    def test_script_to_json(self, sample_script):
        """Test script to JSON conversion."""
        json_str = sample_script.to_json()
        data = json.loads(json_str)
        
        assert data['script_id'] == "test_001"
        assert isinstance(json_str, str)
    
    def test_script_with_quality_scores(self, sample_script):
        """Test script with quality scores."""
        scores = ScriptQualityScores(
            engagement=80.0,
            clarity=90.0,
            pacing=85.0,
            demographic_fit=75.0,
            storytelling=80.0,
            hook_strength=95.0
        )
        
        sample_script.quality_scores = scores
        data = sample_script.to_dict()
        
        assert 'quality_scores' in data
        assert data['quality_scores']['engagement'] == 80.0


class TestScriptGenerator:
    """Test ScriptGenerator class."""
    
    def test_generator_initialization(self, mock_llm_provider):
        """Test generator initialization."""
        with tempfile.TemporaryDirectory() as tmpdir:
            generator = ScriptGenerator(mock_llm_provider, tmpdir)
            
            assert generator.llm == mock_llm_provider
            assert generator.output_root == Path(tmpdir)
    
    def test_generate_script(self, mock_llm_provider, sample_idea):
        """Test script generation."""
        mock_llm_provider.generate_completion.return_value = """Have you ever wondered what's possible?
        
Let me show you something amazing. This is the story of transformation."""
        
        with tempfile.TemporaryDirectory() as tmpdir:
            generator = ScriptGenerator(mock_llm_provider, tmpdir)
            script = generator.generate_script(sample_idea, target_duration=30.0)
            
            assert script.script_id == sample_idea['id']
            assert script.content
            assert script.word_count > 0
            assert script.version == 0
            assert script.target_gender == 'women'
            assert script.target_age == '18-23'
    
    def test_clean_script(self, mock_llm_provider):
        """Test script cleaning."""
        with tempfile.TemporaryDirectory() as tmpdir:
            generator = ScriptGenerator(mock_llm_provider, tmpdir)
            
            # Test removing markdown
            dirty = "**Bold text** and *italic* text"
            clean = generator._clean_script(dirty)
            assert '**' not in clean
            assert '*' not in clean
            
            # Test removing stage directions
            dirty = "[Camera zooms] Some narration (pause for effect)"
            clean = generator._clean_script(dirty)
            assert '[' not in clean
            assert '(' not in clean
    
    def test_save_script(self, mock_llm_provider, sample_script):
        """Test saving script to file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            generator = ScriptGenerator(mock_llm_provider, tmpdir)
            output_path = generator.save_script(sample_script, "v0")
            
            assert output_path.exists()
            assert output_path.suffix == '.json'
            
            # Verify content
            with open(output_path, 'r') as f:
                data = json.load(f)
                assert data['script_id'] == "test_001"


class TestScriptScorer:
    """Test ScriptScorer class."""
    
    def test_scorer_initialization(self, mock_llm_provider):
        """Test scorer initialization."""
        scorer = ScriptScorer(mock_llm_provider)
        assert scorer.llm == mock_llm_provider
    
    def test_score_script(self, mock_llm_provider, sample_script):
        """Test script scoring."""
        mock_llm_provider.generate_completion.return_value = """
ENGAGEMENT: 85
CLARITY: 90
PACING: 80
DEMOGRAPHIC_FIT: 75
STORYTELLING: 82
HOOK_STRENGTH: 88

The script has a strong hook and clear narrative."""
        
        scorer = ScriptScorer(mock_llm_provider)
        scores = scorer.score_script(sample_script)
        
        assert isinstance(scores, ScriptQualityScores)
        assert scores.engagement == 85.0
        assert scores.clarity == 90.0
        assert scores.pacing == 80.0
        assert scores.overall_score > 0
    
    def test_parse_scores(self, mock_llm_provider):
        """Test score parsing."""
        scorer = ScriptScorer(mock_llm_provider)
        
        response = """
ENGAGEMENT: 85
CLARITY: 90
PACING: 80
DEMOGRAPHIC_FIT: 75
STORYTELLING: 82
HOOK_STRENGTH: 88
"""
        
        scores = scorer._parse_scores(response)
        
        assert scores.engagement == 85.0
        assert scores.clarity == 90.0
        assert scores.demographic_fit == 75.0
    
    def test_parse_scores_with_missing_values(self, mock_llm_provider):
        """Test score parsing with missing values."""
        scorer = ScriptScorer(mock_llm_provider)
        
        response = """
ENGAGEMENT: 85
CLARITY: 90
"""
        
        scores = scorer._parse_scores(response)
        
        assert scores.engagement == 85.0
        assert scores.clarity == 90.0
        assert scores.pacing == 50.0  # Default value
        assert scores.demographic_fit == 50.0  # Default value


class TestScriptIterator:
    """Test ScriptIterator class."""
    
    def test_iterator_initialization(self, mock_llm_provider):
        """Test iterator initialization."""
        iterator = ScriptIterator(mock_llm_provider)
        assert iterator.llm == mock_llm_provider
    
    def test_identify_weaknesses(self, mock_llm_provider):
        """Test weakness identification."""
        iterator = ScriptIterator(mock_llm_provider)
        
        scores = ScriptQualityScores(
            engagement=85.0,
            clarity=65.0,  # Weak
            pacing=60.0,   # Weak
            demographic_fit=75.0,
            storytelling=55.0,  # Weakest
            hook_strength=90.0
        )
        
        weaknesses = iterator._identify_weaknesses(scores)
        
        # Should identify 3 weak dimensions
        assert len(weaknesses) == 3
        # Should be sorted by score (weakest first)
        assert weaknesses[0][0] == 'storytelling'
        assert weaknesses[0][1] == 55.0
    
    def test_improve_script_single_iteration(self, mock_llm_provider, sample_script):
        """Test single script improvement iteration."""
        # Mock scoring responses
        mock_llm_provider.generate_completion.side_effect = [
            # First call: initial scoring
            """ENGAGEMENT: 70
CLARITY: 65
PACING: 60
DEMOGRAPHIC_FIT: 75
STORYTELLING: 68
HOOK_STRENGTH: 72""",
            # Second call: improved script generation
            """Have you ever felt like giving up? Ever felt completely stuck?
            
Let me share Sarah's incredible journey. She failed her driving test FIVE times. 
Each time, people doubted her. But she refused to quit.

On her sixth attempt, she didn't just pass - she aced it. Her secret? 
She learned from every single mistake.

Remember: Your failures are lessons in disguise. Keep moving forward.""",
            # Third call: scoring improved script
            """ENGAGEMENT: 85
CLARITY: 80
PACING: 82
DEMOGRAPHIC_FIT: 78
STORYTELLING: 83
HOOK_STRENGTH: 88"""
        ]
        
        iterator = ScriptIterator(mock_llm_provider)
        versions = iterator.improve_script(sample_script, max_iterations=1, target_score=80.0)
        
        assert len(versions) >= 1
        assert versions[0] == sample_script
        
        if len(versions) > 1:
            assert versions[-1].version > versions[0].version


class TestScriptEnhancer:
    """Test ScriptEnhancer class."""
    
    def test_enhancer_initialization(self, mock_llm_provider):
        """Test enhancer initialization."""
        enhancer = ScriptEnhancer(mock_llm_provider)
        assert enhancer.llm == mock_llm_provider
    
    def test_enhance_script(self, mock_llm_provider, sample_script):
        """Test script enhancement."""
        mock_llm_provider.generate_completion.return_value = """Have you ever felt like giving up? Like every door is slammed in your face?
        
Listen to Sarah's story. She failed her driving test five consecutive times. 
Her friends mocked her. Her family lost faith. But Sarah? She never stopped believing.

On her sixth attempt, she didn't just pass—she excelled. Why? 
Because she transformed each failure into a powerful lesson.

Your setbacks aren't roadblocks. They're stepping stones to greatness. Never stop pushing forward."""
        
        enhancer = ScriptEnhancer(mock_llm_provider)
        enhanced = enhancer.enhance_script(sample_script)
        
        assert enhanced.script_id == sample_script.script_id
        assert enhanced.version == sample_script.version + 1
        assert enhanced.content
        assert enhanced.metadata.get('enhanced') == True


class TestTitleOptimizer:
    """Test TitleOptimizer class."""
    
    def test_optimizer_initialization(self, mock_llm_provider):
        """Test optimizer initialization."""
        optimizer = TitleOptimizer(mock_llm_provider)
        assert optimizer.llm == mock_llm_provider
    
    def test_generate_title_variants(self, mock_llm_provider, sample_script):
        """Test title variant generation."""
        mock_llm_provider.generate_completion.return_value = """
TITLE: What Happens When You Fail 5 Times?
STYLE: Curiosity Gap
RATIONALE: Creates intrigue and promises a story

TITLE: How I Turned 5 Failures Into Success
STYLE: How-To/Value
RATIONALE: Offers transformation story and value

TITLE: Nobody Talks About Failing This Much
STYLE: Shocking/Controversial
RATIONALE: Breaks taboo about failure

TITLE: 3 Lessons From Failing 5 Times
STYLE: Listicle/Number
RATIONALE: Promises specific, actionable insights

TITLE: I Failed 5 Times and Here's What I Learned
STYLE: Personal Story
RATIONALE: Authentic personal experience"""
        
        optimizer = TitleOptimizer(mock_llm_provider)
        variants = optimizer.generate_title_variants(sample_script, num_variants=5)
        
        assert len(variants) > 0
        assert all('title' in v for v in variants)
        assert all('style' in v for v in variants)
    
    def test_parse_title_variants(self, mock_llm_provider):
        """Test title variant parsing."""
        optimizer = TitleOptimizer(mock_llm_provider)
        
        response = """
TITLE: What Happens When You Fail?
STYLE: Curiosity Gap
RATIONALE: Creates intrigue

TITLE: How I Turned Failure Into Success
STYLE: How-To
RATIONALE: Offers value"""
        
        variants = optimizer._parse_title_variants(response)
        
        assert len(variants) == 2
        assert variants[0]['title'] == "What Happens When You Fail?"
        assert variants[0]['style'] == "Curiosity Gap"
        assert variants[1]['title'] == "How I Turned Failure Into Success"


class TestDevelopScript:
    """Test complete script development workflow."""
    
    def test_develop_script_workflow(self, mock_llm_provider, sample_idea):
        """Test complete workflow."""
        # Mock multiple LLM calls
        mock_llm_provider.generate_completion.side_effect = [
            # Initial generation
            "Generated script content",
            # Initial scoring
            """ENGAGEMENT: 70
CLARITY: 75
PACING: 72
DEMOGRAPHIC_FIT: 68
STORYTELLING: 70
HOOK_STRENGTH: 65""",
            # Improvement generation
            "Improved script content",
            # Improved scoring
            """ENGAGEMENT: 82
CLARITY: 85
PACING: 80
DEMOGRAPHIC_FIT: 78
STORYTELLING: 83
HOOK_STRENGTH: 88""",
            # Enhancement
            "Enhanced script content",
            # Title generation
            """TITLE: Amazing Title 1
STYLE: Curiosity
RATIONALE: Works well"""
        ]
        
        with tempfile.TemporaryDirectory() as tmpdir:
            result = develop_script(
                idea=sample_idea,
                llm_provider=mock_llm_provider,
                output_root=tmpdir,
                target_score=80.0,
                max_iterations=1,
                enhance=True,
                generate_titles=True
            )
            
            assert 'scripts' in result
            assert 'best_script' in result
            assert 'titles' in result
            assert 'summary' in result
            assert result['best_script'].content


class TestIntegration:
    """Integration tests."""
    
    def test_full_pipeline(self, mock_llm_provider, sample_idea):
        """Test full pipeline integration."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Generate
            generator = ScriptGenerator(mock_llm_provider, tmpdir)
            mock_llm_provider.generate_completion.return_value = "Test script content"
            script = generator.generate_script(sample_idea)
            
            assert script.content
            assert script.script_id
            
            # Score
            scorer = ScriptScorer(mock_llm_provider)
            mock_llm_provider.generate_completion.return_value = """
ENGAGEMENT: 80
CLARITY: 85
PACING: 78
DEMOGRAPHIC_FIT: 75
STORYTELLING: 80
HOOK_STRENGTH: 82"""
            
            scores = scorer.score_script(script)
            assert scores.overall_score > 0
            
            # Save
            output_path = generator.save_script(script, "v0")
            assert output_path.exists()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
