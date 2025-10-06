#!/usr/bin/env python3
"""
Test script for configuration YAML files.
Validates that pipeline.yaml and scoring.yaml can be loaded and contain expected structure.
"""

import os
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("PyYAML not installed. Installing...")
    os.system(f"{sys.executable} -m pip install PyYAML")
    import yaml


def test_pipeline_config():
    """Test pipeline.yaml configuration."""
    print("\n" + "="*60)
    print("Testing pipeline.yaml")
    print("="*60)
    
    config_path = Path(__file__).parent / "config" / "pipeline.yaml"
    
    # Check if file exists
    if not config_path.exists():
        print(f"   ❌ File not found: {config_path}")
        return False
    
    # Load YAML
    try:
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
        print("   ✅ YAML file loaded successfully")
    except Exception as e:
        print(f"   ❌ Failed to load YAML: {e}")
        return False
    
    # Validate structure
    required_sections = ['models', 'video', 'audio', 'seeds', 'paths', 'switches']
    for section in required_sections:
        if section not in config:
            print(f"   ❌ Missing section: {section}")
            return False
        print(f"   ✅ Section '{section}' present")
    
    # Validate models section
    required_models = ['llm', 'vision', 'tts', 'asr', 'image', 'video']
    for model in required_models:
        if model not in config['models']:
            print(f"   ❌ Missing model: {model}")
            return False
        print(f"   ✅ Model '{model}': {config['models'][model]}")
    
    # Validate video section
    video_keys = ['width', 'height', 'fps', 'safe_margins_pct']
    for key in video_keys:
        if key not in config['video']:
            print(f"   ❌ Missing video key: {key}")
            return False
    
    if 'top' not in config['video']['safe_margins_pct'] or 'bottom' not in config['video']['safe_margins_pct']:
        print("   ❌ Missing safe_margins_pct.top or safe_margins_pct.bottom")
        return False
    
    print(f"   ✅ Video config: {config['video']['width']}x{config['video']['height']} @ {config['video']['fps']}fps")
    print(f"   ✅ Safe margins: top={config['video']['safe_margins_pct']['top']}%, bottom={config['video']['safe_margins_pct']['bottom']}%")
    
    # Validate audio section
    audio_keys = ['target_lufs', 'sample_rate']
    for key in audio_keys:
        if key not in config['audio']:
            print(f"   ❌ Missing audio key: {key}")
            return False
    print(f"   ✅ Audio config: {config['audio']['sample_rate']}Hz @ {config['audio']['target_lufs']} LUFS")
    
    # Validate seeds section
    seed_keys = ['image', 'video', 'llm']
    for key in seed_keys:
        if key not in config['seeds']:
            print(f"   ❌ Missing seed: {key}")
            return False
    print(f"   ✅ Seeds: image={config['seeds']['image']}, video={config['seeds']['video']}, llm={config['seeds']['llm']}")
    
    # Validate paths section
    path_keys = ['weights', 'cache', 'tmp']
    for key in path_keys:
        if key not in config['paths']:
            print(f"   ❌ Missing path: {key}")
            return False
    print(f"   ✅ Paths configured: {', '.join(path_keys)}")
    
    # Validate switches section
    switch_keys = ['use_ltx', 'use_interpolation']
    for key in switch_keys:
        if key not in config['switches']:
            print(f"   ❌ Missing switch: {key}")
            return False
    print(f"   ✅ Switches: use_ltx={config['switches']['use_ltx']}, use_interpolation={config['switches']['use_interpolation']}")
    
    return True


def test_scoring_config():
    """Test scoring.yaml configuration."""
    print("\n" + "="*60)
    print("Testing scoring.yaml")
    print("="*60)
    
    config_path = Path(__file__).parent / "config" / "scoring.yaml"
    
    # Check if file exists
    if not config_path.exists():
        print(f"   ❌ File not found: {config_path}")
        return False
    
    # Load YAML
    try:
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
        print("   ✅ YAML file loaded successfully")
    except Exception as e:
        print(f"   ❌ Failed to load YAML: {e}")
        return False
    
    # Validate structure
    if 'viral' not in config:
        print("   ❌ Missing 'viral' section")
        return False
    print("   ✅ Section 'viral' present")
    
    # Validate viral scoring weights
    required_weights = ['novelty', 'emotional', 'clarity', 'replay', 'share']
    weights_sum = 0.0
    for weight in required_weights:
        if weight not in config['viral']:
            print(f"   ❌ Missing weight: {weight}")
            return False
        value = config['viral'][weight]
        weights_sum += value
        print(f"   ✅ Weight '{weight}': {value}")
    
    # Check if weights sum to 1.0 (with small tolerance for floating point)
    if abs(weights_sum - 1.0) > 0.001:
        print(f"   ⚠️  Warning: Weights sum to {weights_sum}, expected 1.0")
    else:
        print(f"   ✅ Weights sum to {weights_sum} (normalized)")
    
    return True


def main():
    """Main test runner."""
    print("\n" + "="*60)
    print("Configuration YAML Files Test")
    print("="*60)
    
    results = []
    
    # Test pipeline.yaml
    results.append(("pipeline.yaml", test_pipeline_config()))
    
    # Test scoring.yaml
    results.append(("scoring.yaml", test_scoring_config()))
    
    # Summary
    print("\n" + "="*60)
    print("Test Summary")
    print("="*60)
    
    all_passed = True
    for name, passed in results:
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"{status}: {name}")
        if not passed:
            all_passed = False
    
    if all_passed:
        print("\n✨ All tests passed!")
        return 0
    else:
        print("\n❌ Some tests failed!")
        return 1


if __name__ == "__main__":
    sys.exit(main())
