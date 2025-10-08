import os

from Tools.Utils import TITLES_PATH
from Video.VideoRenderer import VideoRenderer


def batch_convert_all_voiceovers():
    """
    Converts all 'voiceover_normalized.mp3' files under 4_Titles to 'voiceover_with_image.mp4'.
    Uses the new VideoRenderer for better error handling and fallback support.
    """
    renderer = VideoRenderer()
    
    for folder_name in os.listdir(TITLES_PATH):
        folder_path = os.path.join(TITLES_PATH, folder_name)
        if not os.path.isdir(folder_path):
            continue

        mp3_file = os.path.join(folder_path, "voiceover_normalized.mp3")
        output_file = os.path.join(folder_path, "voiceover_with_image.mp4")

        if os.path.exists(output_file):
            print(f"✅ Already exists: {output_file}")
            continue

        # Use VideoRenderer with automatic fallback
        renderer.render_video(
            audio_file=mp3_file,
            output_file=output_file,
            title=folder_name
        )

batch_convert_all_voiceovers()