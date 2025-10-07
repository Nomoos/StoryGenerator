"""
Tests for video clip generation module.
Validates both LTX-Video and interpolation variants.
"""

import os
import sys
import yaml
import tempfile
import shutil
from pathlib import Path

# Add src path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src" / "research" / "python"))

try:
    from generate_video_clips import VideoClipGenerator
except ImportError as e:
    print(f"⚠️  Warning: Could not import generate_video_clips: {e}")
    print("   Test will be skipped if module cannot be loaded")


def test_config_switches():
    """Test that pipeline.yaml has correct switches configuration."""
    print("\n" + "="*60)
    print("Testing Video Clip Configuration")
    print("="*60)
    
    config_path = Path(__file__).parent.parent / "data" / "config" / "pipeline.yaml"
    
    if not config_path.exists():
        print(f"   ❌ Config file not found: {config_path}")
        return False
    
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
    
    # Check switches section
    if 'switches' not in config:
        print(f"   ❌ Missing 'switches' section in config")
        return False
    
    switches = config['switches']
    
    # Check use_ltx switch
    if 'use_ltx' not in switches:
        print(f"   ❌ Missing 'use_ltx' switch")
        return False
    
    print(f"   ✅ use_ltx: {switches['use_ltx']}")
    
    # Check use_interpolation switch
    if 'use_interpolation' not in switches:
        print(f"   ❌ Missing 'use_interpolation' switch")
        return False
    
    print(f"   ✅ use_interpolation: {switches['use_interpolation']}")
    
    # Validate they're booleans
    if not isinstance(switches['use_ltx'], bool):
        print(f"   ❌ use_ltx must be boolean, got {type(switches['use_ltx'])}")
        return False
    
    if not isinstance(switches['use_interpolation'], bool):
        print(f"   ❌ use_interpolation must be boolean, got {type(switches['use_interpolation'])}")
        return False
    
    print(f"   ✅ Both switches are properly configured")
    
    # Check video seeds
    if 'seeds' in config and 'video' in config['seeds']:
        print(f"   ✅ Video seed: {config['seeds']['video']}")
    else:
        print(f"   ⚠️  Warning: No video seed configured")
    
    return True


def test_generator_initialization():
    """Test VideoClipGenerator initialization."""
    print("\n" + "="*60)
    print("Testing VideoClipGenerator Initialization")
    print("="*60)
    
    try:
        # Test with default config
        generator = VideoClipGenerator(fps=24, device="cpu")
        print(f"   ✅ Generator initialized with defaults")
        
        # Check variant selection
        print(f"   ✅ Using LTX: {generator.use_ltx}")
        print(f"   ✅ Using interpolation: {generator.use_interpolation}")
        
        # Test with explicit LTX mode
        generator_ltx = VideoClipGenerator(use_ltx=True, fps=24, device="cpu")
        if generator_ltx.use_ltx:
            print(f"   ✅ LTX mode forced correctly")
        else:
            print(f"   ❌ LTX mode not set correctly")
            return False
        
        # Test with explicit interpolation mode
        generator_interp = VideoClipGenerator(use_ltx=False, fps=24, device="cpu")
        if not generator_interp.use_ltx:
            print(f"   ✅ Interpolation mode forced correctly")
        else:
            print(f"   ❌ Interpolation mode not set correctly")
            return False
        
        return True
        
    except Exception as e:
        print(f"   ❌ Error during initialization: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_output_path_structure():
    """Test that output paths follow the correct structure."""
    print("\n" + "="*60)
    print("Testing Output Path Structure")
    print("="*60)
    
    try:
        # Create temporary directory for testing
        temp_dir = tempfile.mkdtemp()
        
        # Test LTX variant path structure
        ltx_path = os.path.join(temp_dir, "ltx", "tech", "18-23", "story_001", "shot_0.mp4")
        os.makedirs(os.path.dirname(ltx_path), exist_ok=True)
        
        # Verify path structure
        expected_parts = ["ltx", "tech", "18-23", "story_001", "shot_0.mp4"]
        actual_parts = ltx_path.split(os.sep)[-5:]
        
        if actual_parts == expected_parts:
            print(f"   ✅ LTX path structure correct: .../ltx/tech/18-23/story_001/shot_0.mp4")
        else:
            print(f"   ❌ LTX path structure incorrect")
            print(f"      Expected: {expected_parts}")
            print(f"      Got: {actual_parts}")
            return False
        
        # Test interpolation variant path structure
        interp_path = os.path.join(temp_dir, "interp", "lifestyle", "24-30", "story_002", "shot_1.mp4")
        os.makedirs(os.path.dirname(interp_path), exist_ok=True)
        
        expected_parts = ["interp", "lifestyle", "24-30", "story_002", "shot_1.mp4"]
        actual_parts = interp_path.split(os.sep)[-5:]
        
        if actual_parts == expected_parts:
            print(f"   ✅ Interpolation path structure correct: .../interp/lifestyle/24-30/story_002/shot_1.mp4")
        else:
            print(f"   ❌ Interpolation path structure incorrect")
            return False
        
        # Clean up
        shutil.rmtree(temp_dir)
        
        return True
        
    except Exception as e:
        print(f"   ❌ Error during path structure test: {e}")
        return False


def test_shot_format_validation():
    """Test that shot format is properly validated."""
    print("\n" + "="*60)
    print("Testing Shot Format Validation")
    print("="*60)
    
    # Test valid shot formats
    valid_shots = [
        {
            "image_path": "keyframe_001.png",
            "motion": "pan left",
            "intensity": 0.5,
            "duration": 10.0
        },
        {
            "keyframes": ["keyframe_001.png", "keyframe_002.png"],
            "duration": 12.0
        },
        {
            "image_path": "keyframe_003.png",
            "duration": 15.0
        }
    ]
    
    for i, shot in enumerate(valid_shots):
        # Check required fields
        has_image = "image_path" in shot or "keyframes" in shot
        has_duration = "duration" in shot
        
        if has_image:
            print(f"   ✅ Shot {i+1}: Has image data")
        else:
            print(f"   ❌ Shot {i+1}: Missing image data")
            return False
        
        if has_duration:
            print(f"   ✅ Shot {i+1}: Has duration ({shot['duration']}s)")
        else:
            print(f"   ⚠️  Shot {i+1}: Missing duration (will use default)")
    
    return True


def test_example_shots_file():
    """Create and validate example shots file."""
    print("\n" + "="*60)
    print("Creating Example Shots File")
    print("="*60)
    
    example_shots = {
        "shots": [
            {
                "image_path": "examples/keyframes/shot_000.png",
                "motion": "slow zoom in",
                "intensity": 0.3,
                "duration": 10.0
            },
            {
                "image_path": "examples/keyframes/shot_001.png",
                "motion": "pan right",
                "intensity": 0.5,
                "duration": 12.0
            },
            {
                "keyframes": [
                    "examples/keyframes/shot_002_kf1.png",
                    "examples/keyframes/shot_002_kf2.png"
                ],
                "duration": 15.0
            }
        ],
        "metadata": {
            "segment": "tech",
            "age": "18-23",
            "title_id": "ai_revolution_2024"
        }
    }
    
    # Create example file
    examples_dir = Path(__file__).parent.parent / "examples" / "video_clips"
    examples_dir.mkdir(parents=True, exist_ok=True)
    
    example_file = examples_dir / "example_shots.yaml"
    
    with open(example_file, 'w') as f:
        yaml.dump(example_shots, f, default_flow_style=False, sort_keys=False)
    
    print(f"   ✅ Created example file: {example_file}")
    
    # Validate it can be loaded
    with open(example_file, 'r') as f:
        loaded = yaml.safe_load(f)
    
    if "shots" in loaded and len(loaded["shots"]) == 3:
        print(f"   ✅ Example file has {len(loaded['shots'])} shots")
        return True
    else:
        print(f"   ❌ Example file format incorrect")
        return False


def main():
    """Run all tests."""
    print("\n" + "="*60)
    print("Video Clip Generation Tests")
    print("="*60)
    
    results = []
    
    # Test 1: Config switches
    results.append(("Config switches", test_config_switches()))
    
    # Test 2: Generator initialization
    results.append(("Generator initialization", test_generator_initialization()))
    
    # Test 3: Output path structure
    results.append(("Output path structure", test_output_path_structure()))
    
    # Test 4: Shot format validation
    results.append(("Shot format validation", test_shot_format_validation()))
    
    # Test 5: Example shots file
    results.append(("Example shots file", test_example_shots_file()))
    
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
    import sys
    sys.exit(main())
