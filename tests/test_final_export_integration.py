#!/usr/bin/env python3
"""
Integration test for final video export with mock video file.
Tests the complete export flow including video copy, thumbnail generation, and metadata creation.
"""

import os
import sys
import json
import tempfile
import shutil
import subprocess
from pathlib import Path

# Add src/Python directory to path
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'src', 'Python'))

from Models.StoryIdea import StoryIdea
from Generators.GVideoCompositor import VideoCompositor
from Tools.Utils import generate_title_id, FINAL_PATH


def create_test_video(output_path: str, duration: float = 2.0):
    """
    Create a simple test video using FFmpeg.
    
    Args:
        output_path: Path to save the test video
        duration: Duration of video in seconds
    """
    try:
        # Create a simple colored video with FFmpeg
        cmd = [
            'ffmpeg', '-y',
            '-f', 'lavfi',
            '-i', f'color=c=blue:s=1080x1920:d={duration}',
            '-c:v', 'libx264',
            '-pix_fmt', 'yuv420p',
            '-t', str(duration),
            output_path
        ]
        
        result = subprocess.run(cmd, capture_output=True, check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to create test video: {e}")
        print(f"   stderr: {e.stderr.decode()}")
        return False
    except FileNotFoundError:
        print("❌ FFmpeg not found. Please install FFmpeg to run this test.")
        return False


def test_export_integration():
    """Test complete export flow with a real video file."""
    print("\n" + "="*60)
    print("Integration Test: Complete Export Flow")
    print("="*60)
    
    # Create a test StoryIdea
    story = StoryIdea(
        story_title="Integration Test Story",
        narrator_gender="F",
        tone="inspiring",
        theme="personal growth",
        goal="Share an inspiring story about overcoming challenges",
        potencial={
            "age_groups": {
                "10_15": 15,
                "15_20": 25,
                "20_25": 85,  # Target
                "25_30": 40,
                "30_50": 20,
                "50_70": 10
            }
        }
    )
    
    print(f"\n📝 Test Story: {story.story_title}")
    print(f"   Gender: {story.narrator_gender}")
    print(f"   Theme: {story.theme}")
    
    # Create temporary directory for test
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create a test video file
        test_video_path = os.path.join(tmpdir, "test_video.mp4")
        print(f"\n📹 Creating test video: {test_video_path}")
        
        if not create_test_video(test_video_path, duration=2.0):
            print("❌ Could not create test video - skipping integration test")
            return False
        
        if not os.path.exists(test_video_path):
            print("❌ Test video not created")
            return False
        
        print(f"✅ Test video created: {os.path.getsize(test_video_path)} bytes")
        
        # Initialize VideoCompositor
        print(f"\n🎬 Initializing VideoCompositor...")
        compositor = VideoCompositor()
        
        # Perform export
        print(f"\n📦 Performing export...")
        try:
            video_path, thumbnail_path, metadata_path = compositor.export_final_video(
                story_idea=story,
                source_video_path=test_video_path,
                export_thumbnail=True,
                export_metadata=True
            )
            
            # Verify outputs
            print(f"\n✅ Export completed!")
            
            # Check video
            if os.path.exists(video_path):
                size = os.path.getsize(video_path)
                print(f"   ✅ Video exported: {video_path} ({size} bytes)")
            else:
                print(f"   ❌ Video not found: {video_path}")
                return False
            
            # Check thumbnail
            if thumbnail_path and os.path.exists(thumbnail_path):
                size = os.path.getsize(thumbnail_path)
                print(f"   ✅ Thumbnail generated: {thumbnail_path} ({size} bytes)")
            else:
                print(f"   ⚠️ Thumbnail not found: {thumbnail_path}")
            
            # Check metadata
            if metadata_path and os.path.exists(metadata_path):
                size = os.path.getsize(metadata_path)
                print(f"   ✅ Metadata generated: {metadata_path} ({size} bytes)")
                
                # Read and validate metadata
                with open(metadata_path, 'r') as f:
                    metadata = json.load(f)
                
                print(f"\n📄 Metadata contents:")
                print(f"   Title ID: {metadata.get('title_id')}")
                print(f"   Title: {metadata.get('title')}")
                print(f"   Segment: {metadata.get('segment')}")
                print(f"   Age Group: {metadata.get('age_group')}")
                print(f"   Tags: {', '.join(metadata.get('tags', []))}")
                
                # Validate required fields
                required_fields = ['title_id', 'title', 'segment', 'age_group', 'tags']
                missing_fields = [f for f in required_fields if f not in metadata]
                
                if missing_fields:
                    print(f"   ❌ Missing fields: {missing_fields}")
                    return False
                else:
                    print(f"   ✅ All required fields present")
            else:
                print(f"   ❌ Metadata not found: {metadata_path}")
                return False
            
            # Verify path structure
            title_id = generate_title_id(story.story_title)
            expected_segment = "women"
            expected_age = "18-23"
            
            print(f"\n🔍 Verifying path structure:")
            print(f"   Expected segment: {expected_segment}")
            print(f"   Expected age: {expected_age}")
            print(f"   Expected ID: {title_id}")
            
            checks = [
                (expected_segment in video_path, f"Video path contains segment '{expected_segment}'"),
                (expected_age in video_path, f"Video path contains age '{expected_age}'"),
                (title_id in video_path, f"Video path contains title ID '{title_id}'"),
            ]
            
            all_checks_pass = True
            for check, description in checks:
                status = "✅" if check else "❌"
                print(f"   {status} {description}")
                if not check:
                    all_checks_pass = False
            
            return all_checks_pass
            
        except Exception as e:
            print(f"❌ Export failed with error: {e}")
            import traceback
            traceback.print_exc()
            return False


def test_cleanup():
    """Clean up test files from final directory."""
    print("\n" + "="*60)
    print("Cleaning up test files")
    print("="*60)
    
    try:
        # Find and remove test files
        test_pattern = generate_title_id("Integration Test Story")
        
        for root, dirs, files in os.walk(FINAL_PATH):
            for file in files:
                if test_pattern in file:
                    file_path = os.path.join(root, file)
                    os.remove(file_path)
                    print(f"   🗑️ Removed: {file_path}")
        
        print("   ✅ Cleanup complete")
        return True
    except Exception as e:
        print(f"   ⚠️ Cleanup warning: {e}")
        return True  # Don't fail test on cleanup issues


def main():
    """Run integration test."""
    print("\n" + "="*60)
    print("FINAL EXPORT - INTEGRATION TEST")
    print("="*60)
    
    success = test_export_integration()
    
    # Clean up regardless of test result
    test_cleanup()
    
    # Print summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    if success:
        print("✅ PASS: Integration test")
    else:
        print("❌ FAIL: Integration test")
    
    print("="*60 + "\n")
    
    return success


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
