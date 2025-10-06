"""
Video Generator - Minimal Pipeline for Short Video Creation (1080×1920)

This module implements a pipeline that transforms:
story_text + (optional images) → audio (voice) + visuals → alignment/subtitles → assembly & rendering → final video

The pipeline integrates with existing generators:
- Uses audio from GVoice (ElevenLabs TTS)
- Uses subtitles from GTitles (WhisperX alignment)
- Creates 1080×1920 (portrait) videos for TikTok/YouTube Shorts
"""

import os
from typing import List, Dict, Optional
from moviepy.editor import (
    AudioFileClip, ImageClip, TextClip, CompositeVideoClip, concatenate_videoclips
)
from PIL import Image

from Tools.Utils import (
    TITLES_PATH,
    RESOURCES_PATH,
    sanitize_filename,
)


class VideoGenerator:
    """
    Generates short-form vertical videos (1080×1920) with subtitles.
    
    Uses MoviePy to assemble:
    - Background images
    - Audio voiceover
    - Word-by-word subtitles
    """
    
    def __init__(self, width: int = 1080, height: int = 1920, fps: int = 30):
        """
        Initialize the video generator.
        
        Args:
            width: Video width in pixels (default: 1080)
            height: Video height in pixels (default: 1920)
            fps: Frames per second (default: 30)
        """
        self.width = width
        self.height = height
        self.fps = fps
        self._ensure_paths()
    
    def _ensure_paths(self):
        """Ensure required directories exist."""
        os.makedirs(TITLES_PATH, exist_ok=True)
        os.makedirs(RESOURCES_PATH, exist_ok=True)
    
    def make_scene_clip(
        self,
        image_path: str,
        subtitle: str,
        start: float,
        duration: float
    ) -> CompositeVideoClip:
        """
        Create a single scene clip with image and subtitle overlay.
        
        Args:
            image_path: Path to background image
            subtitle: Text to display as subtitle
            start: Start time in seconds
            duration: Duration in seconds
            
        Returns:
            CompositeVideoClip with image and text overlay
        """
        # Load and resize image to fill screen (1080×1920)
        img = ImageClip(image_path).set_duration(duration)
        img = img.resize(height=self.height)
        
        # Center crop if image is wider than target
        if img.w > self.width:
            x_center = img.w // 2
            img = img.crop(
                x_center=x_center,
                width=self.width,
                height=self.height
            )
        
        # Create subtitle text overlay
        # Position at 80% down the screen for readability
        try:
            txt = TextClip(
                subtitle,
                fontsize=48,
                color='white',
                stroke_color='black',
                stroke_width=2,
                method='caption',
                size=(int(self.width * 0.9), None),
                font='Arial'
            ).set_position(("center", self.height * 0.8)).set_start(start).set_duration(duration)
        except Exception as e:
            print(f"⚠️ Warning: Could not create text clip (font issue?): {e}")
            # Create without text if font not available
            txt = None
        
        # Composite the image and text
        if txt:
            return CompositeVideoClip([img, txt], size=(self.width, self.height))
        else:
            return CompositeVideoClip([img], size=(self.width, self.height))
    
    def parse_srt_file(self, srt_path: str) -> List[Dict[str, any]]:
        """
        Parse SRT subtitle file into segments.
        
        Args:
            srt_path: Path to SRT file
            
        Returns:
            List of subtitle segments with text, start, and end times
        """
        segments = []
        
        if not os.path.exists(srt_path):
            print(f"⚠️ SRT file not found: {srt_path}")
            return segments
        
        with open(srt_path, 'r', encoding='utf-8') as f:
            content = f.read().strip()
        
        # Parse SRT format
        blocks = content.split('\n\n')
        for block in blocks:
            lines = block.strip().split('\n')
            if len(lines) >= 3:
                # Line 0: index
                # Line 1: timestamp (00:00:00,000 --> 00:00:05,000)
                # Line 2+: text
                timestamp_line = lines[1]
                text = ' '.join(lines[2:])
                
                try:
                    time_parts = timestamp_line.split(' --> ')
                    start_time = self._parse_srt_time(time_parts[0])
                    end_time = self._parse_srt_time(time_parts[1])
                    
                    segments.append({
                        'text': text,
                        'start': start_time,
                        'end': end_time,
                        'duration': end_time - start_time
                    })
                except Exception as e:
                    print(f"⚠️ Could not parse SRT block: {e}")
                    continue
        
        return segments
    
    def _parse_srt_time(self, time_str: str) -> float:
        """
        Convert SRT timestamp (HH:MM:SS,mmm) to seconds.
        
        Args:
            time_str: Time string in format HH:MM:SS,mmm
            
        Returns:
            Time in seconds as float
        """
        time_str = time_str.strip().replace(',', '.')
        parts = time_str.split(':')
        hours = int(parts[0])
        minutes = int(parts[1])
        seconds = float(parts[2])
        return hours * 3600 + minutes * 60 + seconds
    
    def assemble_video(
        self,
        scenes: List[Dict[str, any]],
        audio_path: str,
        output_path: str
    ):
        """
        Assemble final video from scenes and audio.
        
        Args:
            scenes: List of scene dictionaries with keys:
                   - image: path to background image
                   - text: subtitle text
                   - start: start time in seconds
                   - duration: duration in seconds
            audio_path: Path to audio file (MP3)
            output_path: Path for output video file
        """
        print(f"🎬 Assembling video: {output_path}")
        
        if not os.path.exists(audio_path):
            print(f"❌ Audio file not found: {audio_path}")
            return
        
        # Load audio
        audio = AudioFileClip(audio_path)
        
        # Create video clips for each scene
        clips = []
        for scene in scenes:
            clip = self.make_scene_clip(
                scene['image'],
                scene['text'],
                scene['start'],
                scene['duration']
            )
            clips.append(clip)
        
        if not clips:
            print("❌ No clips to assemble")
            return
        
        # Concatenate all clips
        video = concatenate_videoclips(clips, method="compose")
        
        # Set audio
        video = video.set_audio(audio)
        
        # Render video
        print(f"🎥 Rendering video to {output_path}...")
        video.write_videofile(
            output_path,
            fps=self.fps,
            codec="libx264",
            audio_codec="aac",
            temp_audiofile="/tmp/temp-audio.m4a",
            remove_temp=True,
            threads=4,
            preset='medium',
            bitrate='5000k'
        )
        
        print(f"✅ Video created: {output_path}")
    
    def create_video_from_folder(
        self,
        folder_name: str,
        background_image: Optional[str] = None
    ):
        """
        Create video from a story folder in TITLES_PATH.
        
        Args:
            folder_name: Name of folder in TITLES_PATH
            background_image: Optional path to background image.
                            If None, uses default from RESOURCES_PATH
        """
        folder_path = os.path.join(TITLES_PATH, folder_name)
        
        if not os.path.isdir(folder_path):
            print(f"❌ Folder not found: {folder_path}")
            return
        
        # Locate required files
        audio_path = os.path.join(folder_path, "voiceover_normalized.mp3")
        srt_path = os.path.join(folder_path, "Subtitles_Word_By_Word.txt")
        output_path = os.path.join(folder_path, "video_final.mp4")
        
        if not os.path.exists(audio_path):
            print(f"⚠️ Skipping '{folder_name}': voiceover_normalized.mp3 not found")
            return
        
        if not os.path.exists(srt_path):
            print(f"⚠️ Skipping '{folder_name}': Subtitles_Word_By_Word.txt not found")
            return
        
        # Check if video already exists
        if os.path.exists(output_path):
            print(f"✅ Video already exists: {output_path}")
            return
        
        # Use default background if not specified
        if background_image is None:
            background_image = os.path.join(RESOURCES_PATH, "baground.jpg")
        
        if not os.path.exists(background_image):
            print(f"❌ Background image not found: {background_image}")
            return
        
        # Parse subtitles
        segments = self.parse_srt_file(srt_path)
        
        if not segments:
            print(f"⚠️ No subtitle segments found in {srt_path}")
            return
        
        # Get audio duration
        audio = AudioFileClip(audio_path)
        audio_duration = audio.duration
        audio.close()
        
        # Create scenes - simple approach: one scene per subtitle segment
        scenes = []
        for seg in segments:
            scenes.append({
                'image': background_image,
                'text': seg['text'],
                'start': seg['start'],
                'duration': seg['duration']
            })
        
        # Assemble video
        self.assemble_video(scenes, audio_path, output_path)
    
    def batch_create_videos(self, background_image: Optional[str] = None):
        """
        Create videos for all folders in TITLES_PATH.
        
        Args:
            background_image: Optional path to background image for all videos
        """
        print("🎬 Starting batch video creation...")
        
        if not os.path.exists(TITLES_PATH):
            print(f"❌ TITLES_PATH not found: {TITLES_PATH}")
            return
        
        folders = [f for f in os.listdir(TITLES_PATH) if os.path.isdir(os.path.join(TITLES_PATH, f))]
        
        if not folders:
            print(f"⚠️ No folders found in {TITLES_PATH}")
            return
        
        print(f"📁 Found {len(folders)} folders to process")
        
        for folder_name in folders:
            print(f"\n{'='*60}")
            print(f"Processing: {folder_name}")
            print(f"{'='*60}")
            self.create_video_from_folder(folder_name, background_image)
        
        print("\n✅ Batch video creation complete!")
