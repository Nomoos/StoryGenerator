#!/usr/bin/env python3
"""
Tests for Content Ranking Module
"""

import os
import json
import tempfile
import shutil
from pathlib import Path
from datetime import datetime

# Add parent directory to path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

import content_ranking


def test_imports():
    """Test that all required modules can be imported."""
    print("✓ Testing imports...")
    assert hasattr(content_ranking, 'load_config')
    assert hasattr(content_ranking, 'find_latest_file')
    assert hasattr(content_ranking, 'rank_content')
    assert hasattr(content_ranking, 'calculate_final_score')
    print("  ✅ All imports successful")


def test_calculate_final_score():
    """Test final score calculation."""
    print("\n✓ Testing final score calculation...")
    
    config = {
        'viral': {
            'novelty': 0.25,
            'emotional': 0.25,
            'clarity': 0.20,
            'replay': 0.15,
            'share': 0.15,
        }
    }
    
    # Test with component scores
    item1 = {
        'id': 'test-001',
        'novelty': 80,
        'emotional_impact': 90,
        'clarity': 85,
        'replay_value': 75,
        'shareability': 88
    }
    
    score1 = content_ranking.calculate_final_score(item1, config)
    assert 75 <= score1 <= 95, f"Expected score between 75-95, got {score1}"
    print(f"  ✅ Component score calculation: {score1:.2f}")
    
    # Test with existing final_score
    item2 = {
        'id': 'test-002',
        'final_score': 87.5
    }
    
    score2 = content_ranking.calculate_final_score(item2, config)
    assert score2 == 87.5, f"Expected 87.5, got {score2}"
    print(f"  ✅ Existing final_score preserved: {score2:.2f}")
    
    # Test with quality_score fallback
    item3 = {
        'id': 'test-003',
        'quality_score': 72
    }
    
    score3 = content_ranking.calculate_final_score(item3, config)
    assert score3 == 72, f"Expected 72, got {score3}"
    print(f"  ✅ Fallback to quality_score: {score3:.2f}")


def test_get_duplicate_ids():
    """Test duplicate ID extraction."""
    print("\n✓ Testing duplicate ID extraction...")
    
    # Test with list of dict duplicates
    dedup_report1 = {
        'duplicates': [
            {'id': 'dup-001'},
            {'id': 'dup-002'},
            {'duplicate_id': 'dup-003'}
        ]
    }
    
    dup_ids1 = content_ranking.get_duplicate_ids(dedup_report1)
    assert len(dup_ids1) == 3
    assert 'dup-001' in dup_ids1
    assert 'dup-003' in dup_ids1
    print(f"  ✅ Extracted {len(dup_ids1)} duplicate IDs")
    
    # Test with list of strings
    dedup_report2 = {
        'duplicates': ['dup-004', 'dup-005']
    }
    
    dup_ids2 = content_ranking.get_duplicate_ids(dedup_report2)
    assert len(dup_ids2) == 2
    assert 'dup-004' in dup_ids2
    print(f"  ✅ Extracted {len(dup_ids2)} duplicate IDs from string list")


def test_rank_content():
    """Test content ranking."""
    print("\n✓ Testing content ranking...")
    
    config = {
        'viral': {
            'novelty': 0.25,
            'emotional': 0.25,
            'clarity': 0.20,
            'replay': 0.15,
            'share': 0.15,
        }
    }
    
    content = [
        {
            'id': 'content-001',
            'quality_score': 85
        },
        {
            'id': 'content-002',
            'quality_score': 92
        },
        {
            'id': 'content-003',  # This is a duplicate
            'quality_score': 88
        },
        {
            'id': 'content-004',
            'quality_score': 78
        },
    ]
    
    dedup_report = {
        'duplicates': [
            {'id': 'content-003'}
        ]
    }
    
    ranked = content_ranking.rank_content(content, dedup_report, config)
    
    # Should have 3 items (one filtered as duplicate)
    assert len(ranked) == 3, f"Expected 3 items, got {len(ranked)}"
    
    # Should be sorted by score (descending)
    assert ranked[0]['id'] == 'content-002', "Highest score should be first"
    assert ranked[0]['rank'] == 1, "First item should have rank 1"
    assert ranked[1]['id'] == 'content-001', "Second highest should be second"
    assert ranked[2]['id'] == 'content-004', "Lowest score should be last"
    
    # content-003 should be filtered out
    for item in ranked:
        assert item['id'] != 'content-003', "Duplicate should be filtered"
    
    print(f"  ✅ Ranked {len(ranked)} items correctly")
    print(f"     Rank 1: {ranked[0]['id']} (score: {ranked[0]['final_score']:.2f})")
    print(f"     Rank 2: {ranked[1]['id']} (score: {ranked[1]['final_score']:.2f})")
    print(f"     Rank 3: {ranked[2]['id']} (score: {ranked[2]['final_score']:.2f})")


def test_find_latest_file():
    """Test finding latest file."""
    print("\n✓ Testing find latest file...")
    
    import time
    
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir)
        
        # Create test files with different timestamps
        file1 = tmp_path / "content_scores_2025-01-01.json"
        file1.write_text("{}")
        time.sleep(0.01)  # Ensure different timestamps
        
        file2 = tmp_path / "content_scores_2025-01-02.json"
        file2.write_text("{}")
        time.sleep(0.01)
        
        file3 = tmp_path / "content_scores_2025-01-03.json"
        file3.write_text("{}")
        
        # Find latest (by modification time, which should be file3)
        latest = content_ranking.find_latest_file(tmp_path, "content_scores_*.json")
        
        assert latest is not None, "Should find a file"
        # The latest by modification time should be file3
        assert latest == file3, f"Should find latest file, expected {file3.name} but got {latest.name}"
        
        print(f"  ✅ Found latest file: {latest.name}")


def test_end_to_end_ranking():
    """Test end-to-end ranking workflow."""
    print("\n✓ Testing end-to-end ranking workflow...")
    
    with tempfile.TemporaryDirectory() as tmpdir:
        base_path = Path(tmpdir) / "Generator"
        scores_path = base_path / "scores" / "women" / "18-23"
        scores_path.mkdir(parents=True, exist_ok=True)
        
        # Create test data files
        date_str = datetime.now().strftime("%Y-%m-%d")
        
        # Content scores file
        content_scores = [
            {
                'id': 'story-001',
                'title': 'The Secret Letter',
                'quality_score': 87,
                'viral_score': 85,
                'novelty': 82,
                'emotional_impact': 90,
                'clarity': 88,
                'replay_value': 85,
                'shareability': 86
            },
            {
                'id': 'story-002',
                'title': 'A Shocking Discovery',
                'quality_score': 92,
                'viral_score': 90,
                'novelty': 90,
                'emotional_impact': 93,
                'clarity': 91,
                'replay_value': 92,
                'shareability': 90
            },
            {
                'id': 'story-003',
                'title': 'The Truth Revealed',
                'quality_score': 78,
                'viral_score': 75,
                'novelty': 76,
                'emotional_impact': 79,
                'clarity': 80,
                'replay_value': 75,
                'shareability': 77
            },
            {
                'id': 'story-004',  # Duplicate
                'title': 'Similar Story',
                'quality_score': 85,
                'viral_score': 82
            }
        ]
        
        scores_file = scores_path / f"content_scores_{date_str}.json"
        with open(scores_file, 'w') as f:
            json.dump(content_scores, f)
        
        # Dedup report file
        dedup_report = {
            'duplicates': [
                {'id': 'story-004', 'reason': 'similar to story-001'}
            ],
            'retained_items': ['story-001', 'story-002', 'story-003']
        }
        
        dedup_file = scores_path / f"dedup_report_{date_str}.json"
        with open(dedup_file, 'w') as f:
            json.dump(dedup_report, f)
        
        # Run ranking
        config = content_ranking.load_config()
        success = content_ranking.rank_content_for_segment(
            base_path, 'women', '18-23', config
        )
        
        assert success, "Ranking should succeed"
        
        # Check output file
        output_file = scores_path / f"ranked_content_{date_str}.json"
        assert output_file.exists(), "Output file should be created"
        
        with open(output_file, 'r') as f:
            output_data = json.load(f)
        
        assert 'content' in output_data, "Output should have 'content' field"
        assert len(output_data['content']) == 3, "Should have 3 items (1 duplicate filtered)"
        
        # Check ranking order
        ranked_content = output_data['content']
        assert ranked_content[0]['id'] == 'story-002', "Highest score should be first"
        assert ranked_content[0]['rank'] == 1, "First item should have rank 1"
        assert ranked_content[1]['id'] == 'story-001', "Second highest should be second"
        assert ranked_content[2]['id'] == 'story-003', "Lowest should be last"
        
        # Check that duplicate was filtered
        for item in ranked_content:
            assert item['id'] != 'story-004', "Duplicate should be filtered"
        
        print(f"  ✅ End-to-end ranking successful")
        print(f"     Output file: {output_file.name}")
        print(f"     Total items ranked: {len(ranked_content)}")
        print(f"     Top item: {ranked_content[0]['id']} (rank {ranked_content[0]['rank']})")


def run_all_tests():
    """Run all tests."""
    print("="*60)
    print("Running Content Ranking Tests")
    print("="*60)
    
    tests = [
        test_imports,
        test_calculate_final_score,
        test_get_duplicate_ids,
        test_rank_content,
        test_find_latest_file,
        test_end_to_end_ranking,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except Exception as e:
            print(f"\n❌ FAILED: {test.__name__}")
            print(f"   Error: {e}")
            failed += 1
    
    print("\n" + "="*60)
    print(f"Test Results: {passed} passed, {failed} failed")
    print("="*60)
    
    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
