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
VIDEOS_PATH = os.path.join(STORY_ROOT, "5_Videos")
SUBTITLES_NAME = "Subtitles.txt"
SUBTITLESWBW_NAME = "Subtitles_Word_By_Word.txt"
RESOURCES_PATH = os.path.join(STORY_ROOT, "Resources")

def sanitize_filename(title):
    """Sanitize the title for safe filename usage."""
    return re.sub(r'[\\/*?:"<>|]', "", title).strip().replace(" ", "_")

def convert_to_mp4(mp3_file: str, output_file: str):
    """
    Converts an MP3 and a still image into a basic MP4 video.
    Ensures video is valid length and resolution.
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
        video_stream = (
            ffmpeg
            .input(img_path, loop=1, framerate=30, t=duration)
            .filter('scale', 'trunc(iw/2)*2', 'trunc(ih/2)*2')
        )

        audio_stream = ffmpeg.input(mp3_file)

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
