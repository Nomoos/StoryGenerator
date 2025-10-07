#!/usr/bin/env python3
"""
Basic functionality test for the Video pipeline modules.
Tests core features without requiring full story pipeline.
"""

import os
import sys
import tempfile
import shutil
from pathlib import Path

# Add src/Python directory to path
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'src', 'Python'))

from Video.VideoRenderer import VideoRenderer
from Video.SceneComposer import SceneComposer


def test_video_renderer():
    """Test VideoRenderer basic functionality."""
    print("\n" + "="*60)
    print("Testing VideoRenderer")
    print("="*60)
    
    renderer = VideoRenderer(
        default_resolution=(640, 480),  # Smaller for testing
        default_fps=10,
        default_bitrate="64k"
    )
    
    # Test 1: Create fallback image
    print("\n1. Testing fallback image creation...")
    with tempfile.TemporaryDirectory() as tmpdir:
        fallback_path = os.path.join(tmpdir, "fallback.jpg")
        result = renderer.create_fallback_image(
            output_path=fallback_path,
            text="Test Story",
            resolution=(640, 480)
        )
        
        if os.path.exists(result) and os.path.getsize(result) > 0:
            print("   ✅ Fallback image created successfully")
            print(f"   Size: {os.path.getsize(result)} bytes")
        else:
            print("   ❌ Failed to create fallback image")
            return False
    
    # Test 2: Check video rendering validation (without actual video)
    print("\n2. Testing video validation...")
    with tempfile.TemporaryDirectory() as tmpdir:
        fake_audio = os.path.join(tmpdir, "fake_audio.mp3")
        output_video = os.path.join(tmpdir, "output.mp4")
        
        # Should fail gracefully with missing audio
        result = renderer.render_video(
            audio_file=fake_audio,
            output_file=output_video,
            title="Test"
        )
        
        if not result:  # Expected to fail
            print("   ✅ Validation works correctly (rejected missing audio)")
        else:
            print("   ❌ Validation should have rejected missing audio")
            return False
    
    print("\n✅ VideoRenderer tests passed!")
    return True


def test_scene_composer():
    """Test SceneComposer basic functionality."""
    print("\n" + "="*60)
    print("Testing SceneComposer")
    print("="*60)
    
    composer = SceneComposer()
    
    # Test 1: Add scenes
    print("\n1. Testing scene addition...")
    composer.add_scene("Scene 1", duration=5.0)
    composer.add_scene("Scene 2", duration=7.0)
    composer.add_scene("Scene 3", duration=3.0)
    
    if composer.get_scene_count() == 3:
        print("   ✅ Added 3 scenes successfully")
    else:
        print(f"   ❌ Expected 3 scenes, got {composer.get_scene_count()}")
        return False
    
    # Test 2: Calculate duration
    print("\n2. Testing duration calculation...")
    total = composer.get_total_duration()
    expected = 15.0
    
    if abs(total - expected) < 0.01:
        print(f"   ✅ Total duration correct: {total}s")
    else:
        print(f"   ❌ Expected {expected}s, got {total}s")
        return False
    
    # Test 3: Save and load composition
    print("\n3. Testing save/load composition...")
    with tempfile.TemporaryDirectory() as tmpdir:
        comp_path = os.path.join(tmpdir, "composition.json")
        
        # Save
        if not composer.save_composition(comp_path):
            print("   ❌ Failed to save composition")
            return False
        
        if not os.path.exists(comp_path):
            print("   ❌ Composition file not created")
            return False
        
        # Load in new composer
        new_composer = SceneComposer()
        if not new_composer.load_composition(comp_path):
            print("   ❌ Failed to load composition")
            return False
        
        if new_composer.get_scene_count() == 3:
            print("   ✅ Saved and loaded composition successfully")
        else:
            print(f"   ❌ Expected 3 scenes after load, got {new_composer.get_scene_count()}")
            return False
    
    # Test 4: Split text into scenes
    print("\n4. Testing text splitting...")
    composer.clear_scenes()
    text = "First sentence. Second sentence. Third sentence. Fourth sentence."
    composer.split_text_into_scenes(text, total_duration=20.0, sentences_per_scene=2)
    
    if composer.get_scene_count() == 2:
        print(f"   ✅ Split text into {composer.get_scene_count()} scenes")
    else:
        print(f"   ⚠️  Expected 2 scenes, got {composer.get_scene_count()}")
    
    # Test 5: Generate scene plan
    print("\n5. Testing scene plan generation...")
    with tempfile.TemporaryDirectory() as tmpdir:
        plan = composer.generate_scene_plan(tmpdir)
        
        if 'scenes' in plan and 'total_scenes' in plan:
            print(f"   ✅ Generated plan with {plan['total_scenes']} scenes")
        else:
            print("   ❌ Invalid scene plan structure")
            return False
    
    # Test 6: Validate scenes
    print("\n6. Testing scene validation...")
    if composer.validate_scenes():
        print("   ✅ Scene validation works")
    else:
        print("   ❌ Scene validation failed")
        return False
    
    print("\n✅ SceneComposer tests passed!")
    return True


def test_imports():
    """Test that all modules can be imported."""
    print("\n" + "="*60)
    print("Testing Module Imports")
    print("="*60)
    
    try:
        from Video.VideoRenderer import VideoRenderer
        print("✅ VideoRenderer imported")
    except Exception as e:
        print(f"❌ Failed to import VideoRenderer: {e}")
        return False
    
    try:
        from Video.SceneComposer import SceneComposer
        print("✅ SceneComposer imported")
    except Exception as e:
        print(f"❌ Failed to import SceneComposer: {e}")
        return False
    
    try:
        from Video.VideoPipeline import VideoPipeline
        print("✅ VideoPipeline imported")
    except Exception as e:
        print(f"❌ Failed to import VideoPipeline: {e}")
        return False
    
    print("\n✅ All imports successful!")
    return True


def main():
    """Run all tests."""
    print("\n" + "="*60)
    print("VIDEO PIPELINE - BASIC FUNCTIONALITY TESTS")
    print("="*60)
    
    results = []
    
    # Test imports first
    results.append(("Module Imports", test_imports()))
    
    # Test VideoRenderer
    results.append(("VideoRenderer", test_video_renderer()))
    
    # Test SceneComposer
    results.append(("SceneComposer", test_scene_composer()))
    
    # Print summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {test_name}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    print("="*60 + "\n")
    
    return passed == total


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
