import os
import ffmpeg
from typing import Optional, Tuple
from PIL import Image, ImageDraw, ImageFont
import json


class VideoRenderer:
    """
    Handles video rendering from audio and visual elements.
    Includes error handling and fallback mechanisms.
    """
    
    def __init__(self, 
                 default_resolution: Tuple[int, int] = (1080, 1920),
                 default_fps: int = 30,
                 default_bitrate: str = "192k"):
        """
        Initialize VideoRenderer with default settings.
        
        Args:
            default_resolution: Video resolution as (width, height), default is 1080x1920 for vertical video
            default_fps: Frames per second, default is 30
            default_bitrate: Audio bitrate, default is "192k"
        """
        self.default_resolution = default_resolution
        self.default_fps = default_fps
        self.default_bitrate = default_bitrate
    
    def create_fallback_image(self, 
                              output_path: str,
                              text: str = "",
                              resolution: Optional[Tuple[int, int]] = None) -> str:
        """
        Create a solid background image with optional text as fallback.
        
        Args:
            output_path: Path to save the fallback image
            text: Optional text to display on the image
            resolution: Image resolution, uses default if not provided
            
        Returns:
            Path to the created fallback image
        """
        if resolution is None:
            resolution = self.default_resolution
        
        # Create solid color background (dark blue-gray)
        img = Image.new('RGB', resolution, color=(25, 35, 45))
        
        if text:
            draw = ImageDraw.Draw(img)
            # Try to use a default font, fallback to default if not available
            try:
                font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 60)
            except:
                font = ImageFont.load_default()
            
            # Calculate text position (centered)
            bbox = draw.textbbox((0, 0), text, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            position = ((resolution[0] - text_width) // 2, (resolution[1] - text_height) // 2)
            
            # Draw text in white
            draw.text(position, text, fill=(255, 255, 255), font=font)
        
        img.save(output_path)
        print(f"✅ Created fallback image: {output_path}")
        return output_path
    
    def render_video(self,
                    audio_file: str,
                    output_file: str,
                    image_file: Optional[str] = None,
                    title: str = "",
                    metadata: Optional[dict] = None) -> bool:
        """
        Render video from audio and image with error handling and fallback.
        
        Args:
            audio_file: Path to the audio file (MP3)
            output_file: Path for the output video file (MP4)
            image_file: Optional path to image file. If None or fails, uses fallback
            title: Title for fallback image if needed
            metadata: Optional metadata dict with 'title' and 'description'
            
        Returns:
            True if successful, False otherwise
        """
        # Validate audio file
        if not os.path.exists(audio_file):
            print(f"❌ Audio file not found: {audio_file}")
            return False
        
        if os.path.getsize(audio_file) == 0:
            print(f"⚠️ Audio file is empty: {audio_file}")
            return False
        
        # Get audio duration
        try:
            duration = float(ffmpeg.probe(audio_file)['format']['duration'])
        except Exception as e:
            print(f"❌ Could not read audio duration: {e}")
            return False
        
        # Determine image to use - with fallback
        image_to_use = image_file
        used_fallback = False
        
        if image_file is None or not os.path.exists(image_file):
            print(f"⚠️ Image file not found or not provided, using fallback")
            fallback_dir = os.path.dirname(output_file)
            fallback_path = os.path.join(fallback_dir, "fallback_background.jpg")
            image_to_use = self.create_fallback_image(fallback_path, title)
            used_fallback = True
        
        # Render video
        try:
            video_stream = (
                ffmpeg
                .input(image_to_use, loop=1, framerate=self.default_fps, t=duration)
                .filter('scale', 'trunc(iw/2)*2', 'trunc(ih/2)*2')
            )
            
            audio_stream = ffmpeg.input(audio_file)
            
            # Prepare metadata for ffmpeg
            output_options = {
                'vcodec': 'libx264',
                'acodec': 'aac',
                'b:a': self.default_bitrate,
                'pix_fmt': 'yuv420p',
                'shortest': None,
                'r': self.default_fps,
                't': duration
            }
            
            # Add metadata if provided
            if metadata:
                if 'title' in metadata:
                    output_options['metadata:g'] = f'title={metadata["title"]}'
                if 'description' in metadata:
                    output_options['metadata:g:1'] = f'description={metadata["description"]}'
            
            (
                ffmpeg
                .output(video_stream, audio_stream, output_file, **output_options)
                .overwrite_output()
                .run(capture_stdout=True, capture_stderr=True)
            )
            
            print(f"✅ Created video: {output_file}")
            if used_fallback:
                print(f"⚠️ Used fallback background image")
            return True
            
        except ffmpeg.Error as e:
            print("❌ FFmpeg command failed.")
            print("🔧 Command:", ' '.join(e.cmd) if hasattr(e, 'cmd') else '[unknown]')
            if e.stderr:
                print("🧵 stderr output:\n", e.stderr.decode(errors="ignore"))
            return False
        except Exception as e:
            print(f"❌ Unexpected error during video rendering: {e}")
            return False
    
    def generate_thumbnail(self,
                          video_file: str,
                          output_file: str,
                          timestamp: float = 0.0) -> bool:
        """
        Generate a thumbnail from a video at a specific timestamp.
        
        Args:
            video_file: Path to the video file
            output_file: Path for the output thumbnail
            timestamp: Timestamp in seconds to extract frame from
            
        Returns:
            True if successful, False otherwise
        """
        if not os.path.exists(video_file):
            print(f"❌ Video file not found: {video_file}")
            return False
        
        try:
            (
                ffmpeg
                .input(video_file, ss=timestamp)
                .filter('scale', self.default_resolution[0], self.default_resolution[1])
                .output(output_file, vframes=1)
                .overwrite_output()
                .run(capture_stdout=True, capture_stderr=True)
            )
            print(f"✅ Created thumbnail: {output_file}")
            return True
        except ffmpeg.Error as e:
            print(f"❌ Failed to generate thumbnail: {e}")
            return False
    
    def embed_metadata(self,
                      video_file: str,
                      metadata: dict,
                      output_file: Optional[str] = None) -> bool:
        """
        Embed metadata into an existing video file.
        
        Args:
            video_file: Path to the input video file
            metadata: Dictionary with metadata (title, description, artist, etc.)
            output_file: Optional output path. If None, overwrites input
            
        Returns:
            True if successful, False otherwise
        """
        if not os.path.exists(video_file):
            print(f"❌ Video file not found: {video_file}")
            return False
        
        if output_file is None:
            output_file = video_file + ".tmp"
            will_replace = True
        else:
            will_replace = False
        
        try:
            input_stream = ffmpeg.input(video_file)
            
            # Build metadata options
            meta_options = {}
            for key, value in metadata.items():
                meta_options[f'metadata'] = f'{key}={value}'
            
            (
                ffmpeg
                .output(input_stream, output_file, codec='copy', **meta_options)
                .overwrite_output()
                .run(capture_stdout=True, capture_stderr=True)
            )
            
            if will_replace:
                os.replace(output_file, video_file)
                print(f"✅ Embedded metadata in: {video_file}")
            else:
                print(f"✅ Created video with metadata: {output_file}")
            
            return True
        except ffmpeg.Error as e:
            print(f"❌ Failed to embed metadata: {e}")
            if will_replace and os.path.exists(output_file):
                os.remove(output_file)
            return False
