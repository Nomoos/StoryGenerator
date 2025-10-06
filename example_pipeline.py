"""
Complete Video Pipeline Example

This script demonstrates the full pipeline from story idea to final video:
story_text + (optional images) → audio (voice) + visuals → alignment/subtitles → assembly & rendering → final video

This is a demonstration of how all components work together.
"""

from Models.StoryIdea import StoryIdea
from Generators.GScript import ScriptGenerator
from Generators.GVoice import VoiceMaker
from Generators.GTitles import TitleGenerator
from Generators.GVideo import VideoGenerator


def run_complete_pipeline():
    """
    Run the complete video generation pipeline.
    
    Pipeline stages:
    1. Story script generation (GScript) - 100-200 words
    2. Text-to-speech audio (GVoice) - ElevenLabs TTS
    3. Forced alignment/subtitles (GTitles) - WhisperX word-level timing
    4. Video assembly (GVideo) - MoviePy composition
    5. Final render - 1080×1920 MP4
    """
    
    print("=" * 70)
    print("COMPLETE VIDEO GENERATION PIPELINE")
    print("=" * 70)
    print()
    
    # Example story idea
    # In production, this would come from GStoryIdeas generator
    story_idea = StoryIdea(
        story_title="My First Short Video",
        narrator_gender="female",
        tone="inspirational",
        theme="overcoming obstacles"
    )
    
    print("📝 STAGE 1: Script Generation")
    print("-" * 70)
    print("Generating story script (100-200 words)...")
    script_gen = ScriptGenerator()
    # script_gen.generate_from_storyidea(story_idea)  # Requires OpenAI API
    print("✅ Script saved to Stories/1_Scripts/")
    print()
    
    print("🎤 STAGE 2: Voice Generation (Text-to-Speech)")
    print("-" * 70)
    print("Generating voiceover with ElevenLabs TTS...")
    voice_maker = VoiceMaker()
    # voice_maker.generate_audio()  # Requires ElevenLabs API
    # voice_maker.normalize_audio()  # Normalize audio levels
    print("✅ Voiceover saved to Stories/3_VoiceOver/")
    print()
    
    print("🎬 STAGE 3: Subtitle Alignment (Forced Alignment)")
    print("-" * 70)
    print("Aligning script to audio using WhisperX...")
    print("Creating word-by-word timestamps for subtitles...")
    title_gen = TitleGenerator()
    # title_gen.generate_titles()  # Requires WhisperX and CUDA
    print("✅ Subtitles saved to Stories/4_Titles/")
    print()
    
    print("🎥 STAGE 4: Video Assembly & Rendering")
    print("-" * 70)
    print("Assembling final video...")
    print("- Resolution: 1080×1920 (portrait)")
    print("- Frame rate: 30 fps")
    print("- Codec: H.264 + AAC")
    print("- Subtitles: Burned-in captions")
    video_gen = VideoGenerator(width=1080, height=1920, fps=30)
    # video_gen.batch_create_videos()  # Requires MoviePy and background images
    print("✅ Video saved to Stories/4_Titles/*/video_final.mp4")
    print()
    
    print("=" * 70)
    print("PIPELINE COMPLETE!")
    print("=" * 70)
    print()
    print("Output: 1080×1920 MP4 video with:")
    print("  ✓ High-quality voiceover")
    print("  ✓ Word-by-word synced subtitles")
    print("  ✓ Background visuals")
    print("  ✓ Professional encoding")
    print()


def run_video_only():
    """
    Run only the video generation stage.
    
    Use this when you already have:
    - Audio files in Stories/3_VoiceOver/
    - Subtitle files in Stories/4_Titles/
    """
    
    print("=" * 70)
    print("VIDEO GENERATION ONLY")
    print("=" * 70)
    print()
    print("This assumes you already have:")
    print("  1. Audio: Stories/4_Titles/*/voiceover_normalized.mp3")
    print("  2. Subtitles: Stories/4_Titles/*/Subtitles_Word_By_Word.txt")
    print("  3. Background: Stories/Resources/baground.jpg")
    print()
    
    video_gen = VideoGenerator(width=1080, height=1920, fps=30)
    
    # Process all folders in TITLES_PATH
    print("🎬 Starting batch video creation...")
    # video_gen.batch_create_videos()  # Uncomment when ready to generate
    
    print("✅ All videos created!")
    print()


if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("VIDEO PIPELINE DEMONSTRATION")
    print("=" * 70)
    print()
    print("This script shows the complete pipeline architecture.")
    print("To actually run it, uncomment the generator calls and ensure")
    print("you have the required API keys and dependencies installed.")
    print()
    
    # Show complete pipeline structure
    run_complete_pipeline()
    
    print("\n" + "=" * 70)
    print()
    
    # Show video-only workflow
    run_video_only()
