import os
import re
import time

import ffmpeg

from Tools.Monitor import logger, PerformanceMonitor, log_error, log_info
from Tools.Validator import OutputValidator

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

def convert_to_mp4(mp3_file: str, output_file: str):
    """
    Converts an MP3 and a still image into a basic MP4 video.
    Ensures video is valid length and resolution.
    """
    render_start = time.time()
    success = False
    error_msg = None
    metrics = {}
    
    try:
        if not os.path.exists(mp3_file):
            error_msg = f"MP3 file not found: {mp3_file}"
            print(f"❌ {error_msg}")
            log_error("Video Rendering", mp3_file, Exception(error_msg))
            return

        if os.path.getsize(mp3_file) == 0:
            error_msg = f"MP3 file is empty (0 KB): {mp3_file}"
            print(f"⚠️ {error_msg}")
            log_error("Video Rendering", mp3_file, Exception(error_msg))
            return

        try:
            duration = float(ffmpeg.probe(mp3_file)['format']['duration'])
            metrics['audio_duration'] = round(duration, 2)
        except Exception as e:
            error_msg = f"Could not read MP3 duration: {e}"
            print(f"❌ {error_msg}")
            log_error("Video Rendering", mp3_file, e)
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

            render_duration = time.time() - render_start
            metrics['render_duration'] = round(render_duration, 2)
            
            # Validate output video
            is_valid, validation_metrics = OutputValidator.validate_video_file(output_file)
            metrics.update(validation_metrics)
            
            if not is_valid:
                error_msg = "Generated video file failed validation"
                log_error("Video Validation", output_file, Exception(error_msg))
            else:
                success = True
                print(f"✅ Created MP4: {output_file}")
                log_info(f"✅ Video rendered in {render_duration:.2f}s")

        except ffmpeg.Error as e:
            error_msg = "FFmpeg command failed"
            print(f"❌ {error_msg}")
            print("🔧 Command:", ' '.join(e.cmd) if hasattr(e, 'cmd') else '[unknown]')
            if e.stderr:
                print("🧵 stderr output:\n", e.stderr.decode(errors="ignore"))
            else:
                print("⚠️ No stderr available.")
            log_error("Video Rendering", mp3_file, e)
    
    finally:
        # Log performance metrics
        total_duration = time.time() - render_start
        PerformanceMonitor.log_operation(
            operation="Video_Rendering",
            story_title=os.path.basename(mp3_file),
            duration=total_duration,
            success=success,
            error=error_msg,
            metrics=metrics
        )
