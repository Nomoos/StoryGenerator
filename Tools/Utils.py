import os
import re

import ffmpeg

STORY_ROOT = "C:\\Users\\hittl\\PROJECTS\\VideoMaking\\StoryGenerator\\Stories"
IDEAS_PATH = os.path.join(STORY_ROOT, "0_Ideas")
SCRIPTS_PATH = os.path.join(STORY_ROOT, "1_Scripts")
REVISED_PATH = os.path.join(STORY_ROOT, "2_Revised")
REVISED_NAME = "Revised.txt"
ENHANCED_NAME = "Revised_with_eleven_labs_tags.txt"
VOICEOVER_PATH = os.path.join(STORY_ROOT, "3_VoiceOver")
TITLES_PATH = os.path.join(STORY_ROOT, "4_Titles")
SUBTITLES_NAME = "Subtitles.txt"
SUBTITLESWBW_NAME = "Subtitles_Word_By_Word.txt"
RESOURCES_PATH = os.path.join(STORY_ROOT, "Resources")

def sanitize_filename(title):
    """Sanitize the title for safe filename usage."""
    return re.sub(r'[\\/*?:"<>|]', "", title).strip().replace(" ", "_")

def convert_to_mp4(mp3_file: str, output_file: str, use_ken_burns: bool = False, 
                   video_style: str = "cinematic", background_music: str = None):
    """
    Converts an MP3 and a still image into a basic MP4 video.
    Ensures video is valid length and resolution.
    
    Args:
        mp3_file: Path to the MP3 audio file
        output_file: Path to output video file
        use_ken_burns: Apply Ken Burns zoom/pan effect
        video_style: Style filter to apply ('cinematic', 'warm', 'cold', 'vintage', 'dramatic', 'none')
        background_music: Path to background music file (optional)
    """
    if not os.path.exists(mp3_file):
        print(f"❌ MP3 file not found: {mp3_file}")
        return

    if os.path.getsize(mp3_file) == 0:
        print(f"⚠️ MP3 file is empty (0 KB): {mp3_file}")
        return

    try:
        duration = float(ffmpeg.probe(mp3_file)['format']['duration'])
    except Exception as e:
        print(f"❌ Could not read MP3 duration: {e}")
        return

    img_path = os.path.join(RESOURCES_PATH, "baground.jpg")

    try:
        # Build video stream with optional Ken Burns effect
        if use_ken_burns:
            # Apply Ken Burns zoom effect
            video_stream = (
                ffmpeg
                .input(img_path, loop=1, framerate=30, t=duration)
                .filter('scale', '1080:1920:force_original_aspect_ratio=increase')
                .filter('crop', '1080', '1920')
                .filter('zoompan', f"z='min(zoom+0.0015,1.2)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={int(duration * 30)}:s=1080x1920:fps=30")
            )
        else:
            # Basic static image
            video_stream = (
                ffmpeg
                .input(img_path, loop=1, framerate=30, t=duration)
                .filter('scale', 'trunc(iw/2)*2', 'trunc(ih/2)*2')
            )
        
        # Apply style filter if specified
        if video_style and video_style != "none":
            if video_style == "cinematic":
                video_stream = video_stream.filter('eq', contrast=1.1, brightness=0.0, saturation=0.9)
            elif video_style == "warm":
                video_stream = video_stream.filter('eq', contrast=1.0, brightness=0.05, saturation=1.1)
            elif video_style == "cold":
                video_stream = video_stream.filter('eq', contrast=1.1, brightness=-0.02, saturation=0.95)
            elif video_style == "vintage":
                video_stream = video_stream.filter('eq', contrast=0.9, brightness=0.05, saturation=0.7)
            elif video_style == "dramatic":
                video_stream = video_stream.filter('eq', contrast=1.3, brightness=-0.05, saturation=0.85)

        audio_stream = ffmpeg.input(mp3_file)
        
        # Add background music if provided
        if background_music and os.path.exists(background_music):
            music_stream = ffmpeg.input(background_music, stream_loop=-1).filter('volume', 0.3)
            audio_stream = ffmpeg.filter([audio_stream.filter('volume', 1.0), music_stream], 
                                         'amix', inputs=2, duration='first')

        (
            ffmpeg
            .output(video_stream, audio_stream, output_file,
                    vcodec='libx264',
                    acodec='aac',
                    b='192k',
                    pix_fmt='yuv420p',
                    shortest=None,
                    r=30,
                    t=duration)
            .overwrite_output()
            .run()
        )

        print(f"✅ Created MP4: {output_file}")
    except ffmpeg.Error as e:
        print("❌ FFmpeg command failed.")
        print("🔧 Command:", ' '.join(e.cmd) if hasattr(e, 'cmd') else '[unknown]')
        if e.stderr:
            print("🧵 stderr output:\n", e.stderr.decode(errors="ignore"))
        else:
            print("⚠️ No stderr available.")
