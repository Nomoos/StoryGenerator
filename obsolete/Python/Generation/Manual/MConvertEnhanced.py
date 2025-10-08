"""
Enhanced video conversion with Ken Burns effect, filters, and background music.
Demonstrates the new enhancement features.
"""
import os
from Tools.Utils import TITLES_PATH, convert_to_mp4, RESOURCES_PATH


def batch_convert_enhanced_videos():
    """
    Converts all voiceover files to enhanced videos with effects.
    Uses Ken Burns effect, style filters, and background music.
    """
    # Optional: path to background music (royalty-free)
    background_music_path = os.path.join(RESOURCES_PATH, "background_music.mp3")
    if not os.path.exists(background_music_path):
        background_music_path = None
        print("⚠️ No background music found. Videos will be created without music.")
    
    for folder_name in os.listdir(TITLES_PATH):
        folder_path = os.path.join(TITLES_PATH, folder_name)
        if not os.path.isdir(folder_path):
            continue

        mp3_file = os.path.join(folder_path, "voiceover_normalized.mp3")
        
        # Create different versions with different effects
        versions = [
            ("voiceover_basic.mp4", False, "none", None),
            ("voiceover_cinematic.mp4", True, "cinematic", None),
            ("voiceover_warm.mp4", True, "warm", None),
            ("voiceover_dramatic.mp4", True, "dramatic", background_music_path),
        ]
        
        for output_name, use_ken_burns, style, music in versions:
            output_file = os.path.join(folder_path, output_name)
            
            if os.path.exists(output_file):
                print(f"✅ Already exists: {output_file}")
                continue
            
            if not os.path.exists(mp3_file):
                print(f"⚠️ Skipping {folder_name}/{output_name}: voiceover not found")
                continue
            
            effect_desc = []
            if use_ken_burns:
                effect_desc.append("Ken Burns")
            if style != "none":
                effect_desc.append(f"{style} filter")
            if music:
                effect_desc.append("background music")
            
            print(f"🎬 Creating {output_name} with: {', '.join(effect_desc) if effect_desc else 'basic'}")
            convert_to_mp4(mp3_file, output_file, use_ken_burns, style, music)


if __name__ == "__main__":
    batch_convert_enhanced_videos()
