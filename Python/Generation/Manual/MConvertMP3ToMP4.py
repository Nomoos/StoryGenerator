import os

from Tools.Utils import VOICEOVER_PATH, convert_to_mp4, TITLES_PATH


def batch_convert_all_voiceovers():
    """
    Converts all 'voiceover_normalized.mp3' files under 3_VoiceOver to 'video.mp4'.
    """
    for folder_name in os.listdir(TITLES_PATH):
        folder_path = os.path.join(TITLES_PATH, folder_name)
        if not os.path.isdir(folder_path):
            continue

        mp3_file = os.path.join(folder_path, "voiceover_normalized.mp3")
        output_file = os.path.join(folder_path, "voiceover_with_image.mp4")

        if os.path.exists(output_file):
            print(f"✅ Already exists: {output_file}")
            continue

        convert_to_mp4(mp3_file, output_file)

batch_convert_all_voiceovers()