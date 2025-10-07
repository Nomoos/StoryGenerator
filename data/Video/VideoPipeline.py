"""
Video Pipeline Integration Module

This module integrates all the components of the video generation pipeline:
1. Text generation (Scripts)
2. Voice generation (TTS)
3. Video rendering with scenes
4. Thumbnail generation
5. Metadata embedding

It provides batch processing, error handling, and fallback mechanisms.
"""

import os
import shutil
from typing import Optional, Dict, Any, List
from concurrent.futures import ThreadPoolExecutor, as_completed
import json

from Models.StoryIdea import StoryIdea
from Tools.Utils import (REVISED_PATH, VOICEOVER_PATH, VIDEOS_PATH, 
                         sanitize_filename, ENHANCED_NAME, RESOURCES_PATH)
from Video.VideoRenderer import VideoRenderer
from Video.SceneComposer import SceneComposer


class VideoPipeline:
    """
    Manages the complete video generation pipeline from text to final video.
    """
    
    def __init__(self, 
                 max_workers: int = 4,
                 default_resolution: tuple = (1080, 1920)):
        """
        Initialize the video pipeline.
        
        Args:
            max_workers: Maximum number of parallel video generation tasks
            default_resolution: Default video resolution (width, height)
        """
        self.renderer = VideoRenderer(default_resolution=default_resolution)
        self.composer = SceneComposer()
        self.max_workers = max_workers
        self.default_resolution = default_resolution
        self.stats = {
            'processed': 0,
            'successful': 0,
            'failed': 0,
            'skipped': 0
        }
    
    def process_story(self, 
                     story_folder: str,
                     force_regenerate: bool = False,
                     generate_thumbnail: bool = True) -> bool:
        """
        Process a single story through the video pipeline.
        
        Args:
            story_folder: Name of the story folder
            force_regenerate: If True, regenerate video even if it exists
            generate_thumbnail: If True, generate thumbnail for the video
            
        Returns:
            True if successful, False otherwise
        """
        print(f"\n{'='*60}")
        print(f"📹 Processing: {story_folder}")
        print(f"{'='*60}")
        
        # Paths
        voiceover_folder = os.path.join(VOICEOVER_PATH, story_folder)
        video_folder = os.path.join(VIDEOS_PATH, story_folder)
        
        # Check if voiceover folder exists
        if not os.path.exists(voiceover_folder):
            print(f"⚠️ Voiceover folder not found: {voiceover_folder}")
            return False
        
        # Create video output folder
        os.makedirs(video_folder, exist_ok=True)
        
        # File paths
        idea_file = os.path.join(voiceover_folder, "idea.json")
        audio_file = os.path.join(voiceover_folder, "voiceover_normalized.mp3")
        script_file = os.path.join(voiceover_folder, ENHANCED_NAME)
        video_file = os.path.join(video_folder, "final_video.mp4")
        thumbnail_file = os.path.join(video_folder, "thumbnail.jpg")
        metadata_file = os.path.join(video_folder, "metadata.json")
        
        # Check if video already exists
        if os.path.exists(video_file) and not force_regenerate:
            print(f"✅ Video already exists: {video_file}")
            self.stats['skipped'] += 1
            return True
        
        # Load story idea
        try:
            if not os.path.exists(idea_file):
                print(f"⚠️ Idea file not found: {idea_file}")
                idea = None
                title = story_folder
                description = ""
            else:
                idea = StoryIdea.from_file(idea_file)
                title = idea.story_title
                description = f"A {idea.narrator_type or 'first-person'} story"
                if idea.theme:
                    description += f" about {idea.theme}"
        except Exception as e:
            print(f"⚠️ Could not load idea file: {e}")
            idea = None
            title = story_folder
            description = ""
        
        # Check if audio file exists
        if not os.path.exists(audio_file):
            print(f"❌ Audio file not found: {audio_file}")
            self.stats['failed'] += 1
            return False
        
        # Find or create background image
        background_image = os.path.join(RESOURCES_PATH, "baground.jpg")
        if not os.path.exists(background_image):
            print(f"⚠️ Default background not found: {background_image}")
            background_image = None
        
        # Prepare metadata
        metadata = {
            'title': title,
            'description': description,
            'artist': 'Nom',
            'album': 'Noms Stories'
        }
        
        # Render video
        print(f"🎬 Rendering video...")
        success = self.renderer.render_video(
            audio_file=audio_file,
            output_file=video_file,
            image_file=background_image,
            title=title,
            metadata=metadata
        )
        
        if not success:
            print(f"❌ Failed to render video for: {story_folder}")
            self.stats['failed'] += 1
            return False
        
        # Generate thumbnail
        if generate_thumbnail and os.path.exists(video_file):
            print(f"📸 Generating thumbnail...")
            self.renderer.generate_thumbnail(
                video_file=video_file,
                output_file=thumbnail_file,
                timestamp=0.5  # 0.5 seconds into the video
            )
        
        # Save metadata to file
        try:
            with open(metadata_file, 'w', encoding='utf-8') as f:
                json.dump(metadata, f, indent=2, ensure_ascii=False)
            print(f"✅ Saved metadata to: {metadata_file}")
        except Exception as e:
            print(f"⚠️ Could not save metadata file: {e}")
        
        # Copy script to video folder for reference
        if os.path.exists(script_file):
            try:
                shutil.copy2(script_file, os.path.join(video_folder, "script.txt"))
            except Exception as e:
                print(f"⚠️ Could not copy script: {e}")
        
        self.stats['successful'] += 1
        print(f"✅ Successfully processed: {story_folder}")
        return True
    
    def batch_process(self,
                     source_path: str = VOICEOVER_PATH,
                     parallel: bool = False,
                     force_regenerate: bool = False) -> Dict[str, Any]:
        """
        Process all stories in the voiceover folder.
        
        Args:
            source_path: Path to folder containing stories to process
            parallel: If True, process stories in parallel
            force_regenerate: If True, regenerate videos even if they exist
            
        Returns:
            Dictionary with processing statistics
        """
        print(f"\n{'='*60}")
        print(f"🎬 BATCH VIDEO PROCESSING")
        print(f"{'='*60}")
        print(f"Source: {source_path}")
        print(f"Parallel: {parallel}")
        print(f"Force Regenerate: {force_regenerate}")
        print(f"{'='*60}\n")
        
        # Reset stats
        self.stats = {
            'processed': 0,
            'successful': 0,
            'failed': 0,
            'skipped': 0
        }
        
        # Get all story folders
        if not os.path.exists(source_path):
            print(f"❌ Source path not found: {source_path}")
            return self.stats
        
        story_folders = [
            folder for folder in os.listdir(source_path)
            if os.path.isdir(os.path.join(source_path, folder))
        ]
        
        if not story_folders:
            print(f"⚠️ No story folders found in: {source_path}")
            return self.stats
        
        print(f"📂 Found {len(story_folders)} stories to process\n")
        
        if parallel and self.max_workers > 1:
            # Parallel processing
            with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
                futures = {
                    executor.submit(self.process_story, folder, force_regenerate): folder
                    for folder in story_folders
                }
                
                for future in as_completed(futures):
                    folder = futures[future]
                    self.stats['processed'] += 1
                    try:
                        future.result()
                    except Exception as e:
                        print(f"❌ Unexpected error processing {folder}: {e}")
                        self.stats['failed'] += 1
        else:
            # Sequential processing
            for folder in story_folders:
                self.stats['processed'] += 1
                try:
                    self.process_story(folder, force_regenerate)
                except Exception as e:
                    print(f"❌ Unexpected error processing {folder}: {e}")
                    self.stats['failed'] += 1
        
        # Print summary
        print(f"\n{'='*60}")
        print(f"📊 BATCH PROCESSING SUMMARY")
        print(f"{'='*60}")
        print(f"Total Processed: {self.stats['processed']}")
        print(f"Successful: {self.stats['successful']}")
        print(f"Failed: {self.stats['failed']}")
        print(f"Skipped: {self.stats['skipped']}")
        print(f"{'='*60}\n")
        
        return self.stats
    
    def cleanup_failed(self) -> int:
        """
        Remove incomplete video files from failed processing attempts.
        
        Returns:
            Number of files cleaned up
        """
        cleaned = 0
        
        if not os.path.exists(VIDEOS_PATH):
            return cleaned
        
        for folder in os.listdir(VIDEOS_PATH):
            video_folder = os.path.join(VIDEOS_PATH, folder)
            if not os.path.isdir(video_folder):
                continue
            
            video_file = os.path.join(video_folder, "final_video.mp4")
            
            # Check if video exists but is invalid (empty or corrupted)
            if os.path.exists(video_file):
                if os.path.getsize(video_file) == 0:
                    print(f"🗑️ Removing empty video: {video_file}")
                    os.remove(video_file)
                    cleaned += 1
        
        print(f"✅ Cleaned up {cleaned} failed video files")
        return cleaned


def main():
    """Example usage of the VideoPipeline."""
    pipeline = VideoPipeline(max_workers=2)
    
    # Batch process all stories
    stats = pipeline.batch_process(
        parallel=False,  # Set to True for parallel processing
        force_regenerate=False  # Set to True to regenerate existing videos
    )
    
    print(f"\n✅ Pipeline completed!")
    print(f"Success rate: {stats['successful']}/{stats['processed']} "
          f"({stats['successful']/stats['processed']*100:.1f}%)" if stats['processed'] > 0 else "No stories processed")


if __name__ == "__main__":
    main()
