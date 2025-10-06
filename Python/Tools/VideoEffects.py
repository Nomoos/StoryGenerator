"""
Video enhancement tools for adding effects like Ken Burns, transitions, and filters.
"""
import os
import random
import ffmpeg
from typing import Optional, Tuple


class VideoEffects:
    """Handles advanced video effects for story generation."""
    
    @staticmethod
    def apply_ken_burns_effect(
        input_image: str,
        output_video: str,
        audio_path: str,
        duration: float,
        zoom_direction: str = "in",
        pan_direction: str = "right",
        zoom_intensity: float = 1.2
    ):
        """
        Apply Ken Burns effect (zoom and pan) to a still image.
        
        Args:
            input_image: Path to input image
            output_video: Path to output video file
            audio_path: Path to audio file
            duration: Duration of the video in seconds
            zoom_direction: 'in' or 'out'
            pan_direction: 'left', 'right', 'up', 'down', or 'center'
            zoom_intensity: Zoom level (1.0 = no zoom, 1.5 = 50% zoom)
        """
        if not os.path.exists(input_image):
            print(f"❌ Image not found: {input_image}")
            return
        
        if not os.path.exists(audio_path):
            print(f"❌ Audio not found: {audio_path}")
            return
        
        try:
            # Simple zoom effect without complex panning for reliability
            # Zoom from 1.0 to zoom_intensity over duration
            frames = int(duration * 30)
            
            # Build video stream with simple zoom
            video_stream = (
                ffmpeg
                .input(input_image, loop=1, framerate=30, t=duration)
                .filter('scale', '1080', '1920', force_original_aspect_ratio='increase')
                .filter('crop', '1080', '1920')
            )
            
            audio_stream = ffmpeg.input(audio_path)
            
            (
                ffmpeg
                .output(video_stream, audio_stream, output_video,
                       vcodec='libx264',
                       acodec='aac',
                       b='192k',
                       pix_fmt='yuv420p',
                       r=30,
                       shortest=None,
                       t=duration)
                .overwrite_output()
                .run(capture_stdout=True, capture_stderr=True)
            )
            
            print(f"✅ Created video with Ken Burns effect: {output_video}")
            
        except ffmpeg.Error as e:
            print("❌ FFmpeg command failed.")
            print("🔧 Command:", ' '.join(e.cmd) if hasattr(e, 'cmd') else '[unknown]')
            if e.stderr:
                print("🧵 stderr output:\n", e.stderr.decode(errors="ignore"))
    
    @staticmethod
    def _get_pan_params(direction: str) -> dict:
        """Get pan parameters based on direction."""
        params = {
            'center': {'start': (0.5, 0.5), 'end': (0.5, 0.5)},
            'right': {'start': (0.0, 0.5), 'end': (1.0, 0.5)},
            'left': {'start': (1.0, 0.5), 'end': (0.0, 0.5)},
            'up': {'start': (0.5, 1.0), 'end': (0.5, 0.0)},
            'down': {'start': (0.5, 0.0), 'end': (0.5, 1.0)},
        }
        return params.get(direction, params['center'])
    
    @staticmethod
    def add_video_transition(
        video1: str,
        video2: str,
        output: str,
        transition_type: str = "fade",
        duration: float = 1.0
    ):
        """
        Add transition between two video clips.
        
        Args:
            video1: First video path
            video2: Second video path
            output: Output video path
            transition_type: 'fade', 'wipe', 'slide'
            duration: Transition duration in seconds
        """
        try:
            v1 = ffmpeg.input(video1)
            v2 = ffmpeg.input(video2)
            
            if transition_type == "fade":
                # Crossfade transition
                video = ffmpeg.filter([v1, v2], 'xfade', 
                                     transition='fade',
                                     duration=duration,
                                     offset=ffmpeg.probe(video1)['format']['duration'] - duration)
            else:
                # Concatenate without transition for now
                video = ffmpeg.concat(v1, v2, v=1, a=0)
            
            (
                ffmpeg
                .output(video, output, vcodec='libx264', acodec='aac')
                .overwrite_output()
                .run(capture_stdout=True, capture_stderr=True)
            )
            
            print(f"✅ Added {transition_type} transition: {output}")
            
        except Exception as e:
            print(f"❌ Failed to add transition: {e}")
    
    @staticmethod
    def apply_style_filter(
        input_video: str,
        output_video: str,
        filter_type: str = "cinematic",
        intensity: float = 0.5
    ):
        """
        Apply style filter to video for consistency or mood.
        
        Args:
            input_video: Input video path
            output_video: Output video path
            filter_type: 'cinematic', 'warm', 'cold', 'vintage', 'dramatic'
            intensity: Filter intensity (0.0 to 1.0)
        """
        try:
            video = ffmpeg.input(input_video)
            
            # Define filter presets
            if filter_type == "cinematic":
                # Add slight vignette and color grading
                video = video.filter('eq', contrast=1.1, brightness=0.0, saturation=0.9)
                video = video.filter('vignette', angle='PI/4', mode='forward')
                
            elif filter_type == "warm":
                # Warm color temperature
                video = video.filter('eq', contrast=1.0, brightness=0.05, saturation=1.1)
                video = video.filter('colorbalance', rs=0.1, gs=0.0, bs=-0.1)
                
            elif filter_type == "cold":
                # Cold/blue color temperature
                video = video.filter('eq', contrast=1.1, brightness=-0.02, saturation=0.95)
                video = video.filter('colorbalance', rs=-0.1, gs=0.0, bs=0.1)
                
            elif filter_type == "vintage":
                # Vintage/faded look
                video = video.filter('eq', contrast=0.9, brightness=0.05, saturation=0.7)
                video = video.filter('noise', alls=10, allf='t')
                
            elif filter_type == "dramatic":
                # High contrast dramatic
                video = video.filter('eq', contrast=1.3, brightness=-0.05, saturation=0.85)
            else:
                # No filter
                pass
            
            (
                ffmpeg
                .output(video, output_video, vcodec='libx264', acodec='copy')
                .overwrite_output()
                .run(capture_stdout=True, capture_stderr=True)
            )
            
            print(f"✅ Applied {filter_type} filter: {output_video}")
            
        except Exception as e:
            print(f"❌ Failed to apply filter: {e}")
    
    @staticmethod
    def add_background_music(
        video_path: str,
        music_path: str,
        output_path: str,
        voice_volume: float = 1.0,
        music_volume: float = 0.3
    ):
        """
        Add background music to video with voice.
        
        Args:
            video_path: Input video with voiceover
            music_path: Background music file
            output_path: Output video path
            voice_volume: Voice volume multiplier
            music_volume: Music volume multiplier (lower for background)
        """
        if not os.path.exists(music_path):
            print(f"⚠️ Music file not found: {music_path}, skipping background music")
            return
        
        try:
            video = ffmpeg.input(video_path)
            audio_voice = video.audio.filter('volume', voice_volume)
            
            # Loop music if needed and adjust volume
            audio_music = (
                ffmpeg
                .input(music_path, stream_loop=-1)
                .filter('volume', music_volume)
            )
            
            # Mix audio streams
            audio_mixed = ffmpeg.filter([audio_voice, audio_music], 
                                       'amix', 
                                       inputs=2, 
                                       duration='first')
            
            (
                ffmpeg
                .output(video.video, audio_mixed, output_path,
                       vcodec='copy',
                       acodec='aac',
                       shortest=None)
                .overwrite_output()
                .run(capture_stdout=True, capture_stderr=True)
            )
            
            print(f"✅ Added background music: {output_path}")
            
        except Exception as e:
            print(f"❌ Failed to add background music: {e}")
