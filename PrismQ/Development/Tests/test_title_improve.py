#!/usr/bin/env python3
"""
Tests for title improvement functionality.
"""

import sys
import os
import json
import tempfile
import shutil
from pathlib import Path
from datetime import datetime


def test_imports():
    """Test that title_improve module can be imported."""
    print("=" * 60)
    print("TEST: Module Imports")
    print("=" * 60)
    
    try:
        import title_improve
        print("✅ title_improve module imported successfully")
        return True
    except ImportError as e:
        print(f"❌ Import failed: {e}")
        return False


def test_generate_variants_local():
    """Test local variant generation."""
    print("\n" + "=" * 60)
    print("TEST: Local Variant Generation")
    print("=" * 60)
    
    try:
        import title_improve
        
        original_title = "5 Ways to Improve Your Life"
        variants = title_improve.generate_title_variants_local(
            original_title,
            "women",
            "18-23",
            count=5
        )
        
        assert len(variants) == 5, f"Expected 5 variants, got {len(variants)}"
        assert all(isinstance(v, str) for v in variants), "All variants should be strings"
        assert all(len(v) > 0 for v in variants), "All variants should be non-empty"
        
        print(f"✅ Generated {len(variants)} local variants:")
        for i, variant in enumerate(variants, 1):
            print(f"   {i}. {variant}")
        
        return True
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_score_and_select():
    """Test scoring and selection of best variant."""
    print("\n" + "=" * 60)
    print("TEST: Score and Select Best Variant")
    print("=" * 60)
    
    try:
        import title_improve
        import title_score
        
        # Load config
        config_path = Path(__file__).parent.parent / "data" / "config" / "scoring.yaml"
        scoring_config = title_score.load_scoring_config(str(config_path))
        
        original_title = "Simple Tips for Life"
        variants = [
            "5 Life-Changing Secrets You Need to Know",
            "The Truth About Living Your Best Life",
            "How I Transformed My Life in 30 Days",
            "Why Everyone Is Talking About These Tips",
            "You Won't Believe These Life Hacks"
        ]
        
        best_title, best_score, all_scores = title_improve.score_and_select_best_variant(
            original_title,
            variants,
            "women",
            "18-23",
            scoring_config
        )
        
        assert best_title is not None, "Best title should not be None"
        assert isinstance(best_score, dict), "Best score should be a dictionary"
        assert 'overall_score' in best_score, "Best score should have overall_score"
        assert len(all_scores) == len(variants) + 1, "All scores should include original + variants"
        
        print(f"✅ Selected best title: {best_title}")
        print(f"   Score: {best_score['overall_score']:.1f}/100")
        print(f"   Total scored: {len(all_scores)}")
        
        return True
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_improve_title():
    """Test end-to-end title improvement."""
    print("\n" + "=" * 60)
    print("TEST: End-to-End Title Improvement")
    print("=" * 60)
    
    try:
        import title_improve
        import title_score
        
        # Create temporary directories and files
        with tempfile.TemporaryDirectory() as tmpdir:
            tmppath = Path(tmpdir)
            
            # Create test title file
            titles_dir = tmppath / "titles" / "women" / "18-23"
            titles_dir.mkdir(parents=True)
            
            test_title_file = titles_dir / "test_title_001.json"
            with open(test_title_file, 'w') as f:
                json.dump({
                    'title': '5 Tips for Success',
                    'created_at': datetime.now().isoformat()
                }, f)
            
            # Load configs
            config_path = Path(__file__).parent.parent / "data" / "config" / "scoring.yaml"
            scoring_config = title_score.load_scoring_config(str(config_path))
            llm_config = title_improve.load_llm_config()
            
            # Improve the title
            result = title_improve.improve_title(
                test_title_file,
                "women",
                "18-23",
                tmppath / "titles",
                llm_config,
                scoring_config,
                variant_count=5
            )
            
            assert result is not None, "Result should not be None"
            assert 'metadata' in result, "Result should have metadata"
            assert 'original_title' in result, "Result should have original_title"
            assert 'best_title' in result, "Result should have best_title"
            assert 'all_variants' in result, "Result should have all_variants"
            
            # Check output file exists
            output_file = tmppath / "titles" / "women" / "18-23" / "test_title_001_improved.json"
            assert output_file.exists(), "Output file should be created"
            
            with open(output_file, 'r') as f:
                saved_data = json.load(f)
            
            assert saved_data == result, "Saved data should match result"
            
            print(f"✅ Title improvement successful")
            print(f"   Original: {result['original_title']['title']}")
            print(f"   Best: {result['best_title']['title']}")
            print(f"   Improvement: {result['best_title']['improvement_pct']:.1f}%")
            print(f"   Variants tested: {len(result['all_variants'])}")
            
            return True
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_update_registry():
    """Test title registry update."""
    print("\n" + "=" * 60)
    print("TEST: Update Title Registry")
    print("=" * 60)
    
    try:
        import title_improve
        
        # Create temporary directory
        with tempfile.TemporaryDirectory() as tmpdir:
            tmppath = Path(tmpdir)
            registry_path = tmppath / "title_registry.json"
            
            # Create test results
            test_results = [
                {
                    'metadata': {
                        'title_id': 'test_001',
                        'segment': 'women',
                        'age': '18-23',
                        'improved_at': datetime.now().isoformat(),
                        'variant_count': 5
                    },
                    'original_title': {
                        'title': 'Simple Tips',
                        'score': 60.0
                    },
                    'best_title': {
                        'title': '5 Life-Changing Tips You Need to Know',
                        'score': 75.0,
                        'is_original': False,
                        'improvement_pct': 25.0
                    }
                },
                {
                    'metadata': {
                        'title_id': 'test_002',
                        'segment': 'men',
                        'age': '24-30',
                        'improved_at': datetime.now().isoformat(),
                        'variant_count': 5
                    },
                    'original_title': {
                        'title': 'Career Success Secrets',
                        'score': 80.0
                    },
                    'best_title': {
                        'title': 'Career Success Secrets',
                        'score': 80.0,
                        'is_original': True,
                        'improvement_pct': 0.0
                    }
                }
            ]
            
            # Update registry
            title_improve.update_title_registry(test_results, registry_path)
            
            assert registry_path.exists(), "Registry file should be created"
            
            with open(registry_path, 'r') as f:
                registry = json.load(f)
            
            assert 'metadata' in registry, "Registry should have metadata"
            assert 'titles' in registry, "Registry should have titles"
            assert len(registry['titles']) == 2, "Registry should have 2 titles"
            assert registry['metadata']['total_titles'] == 2, "Metadata should show 2 titles"
            
            # Check first title
            key1 = 'women/18-23/test_001'
            assert key1 in registry['titles'], f"Registry should contain {key1}"
            assert registry['titles'][key1]['is_changed'] == True, "First title should be marked as changed"
            assert 'slug' in registry['titles'][key1], "Title should have slug"
            
            # Check second title
            key2 = 'men/24-30/test_002'
            assert key2 in registry['titles'], f"Registry should contain {key2}"
            assert registry['titles'][key2]['is_changed'] == False, "Second title should not be marked as changed"
            
            print(f"✅ Registry updated successfully")
            print(f"   Total titles: {registry['metadata']['total_titles']}")
            print(f"   Changed: 1")
            print(f"   Unchanged: 1")
            
            return True
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def run_all_tests():
    """Run all tests."""
    print("\n" + "=" * 60)
    print("TITLE IMPROVEMENT TEST SUITE")
    print("=" * 60)
    
    # Change to scripts directory so imports work
    script_dir = Path(__file__).parent.parent / "scripts"
    sys.path.insert(0, str(script_dir))
    os.chdir(script_dir)
    
    tests = [
        ("Module Imports", test_imports),
        ("Local Variant Generation", test_generate_variants_local),
        ("Score and Select", test_score_and_select),
        ("End-to-End Improvement", test_improve_title),
        ("Registry Update", test_update_registry),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"\n❌ Test '{test_name}' crashed: {e}")
            import traceback
            traceback.print_exc()
            results.append((test_name, False))
    
    # Print summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{status}: {test_name}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    return passed == total


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
