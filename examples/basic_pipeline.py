# Example: Basic Pipeline Usage

"""
This example demonstrates basic usage of the StoryGenerator pipeline.
Currently runs the existing components: Story Idea, Script, Revision, Voice, and Subtitles.
"""

from Models.StoryIdea import StoryIdea
from Generators.GScript import ScriptGenerator
from Generators.GRevise import RevisedScriptGenerator
from Generators.GVoice import VoiceMaker
from Generators.GTitles import TitleGenerator

def main():
    print("🎬 StoryGenerator - Basic Pipeline Example")
    print("=" * 60)
    
    # Step 1: Create a story idea
    print("\n📝 Step 1: Creating story idea...")
    story_idea = StoryIdea(
        story_title="The Unexpected Friend",
        narrator_gender="female",
        tone="emotional, heartwarming",
        theme="friendship, acceptance",
        narrator_type="first-person",
        other_character="a shy classmate",
        outcome="positive, emotional revelation",
        emotional_core="loneliness, connection, acceptance",
        power_dynamic="equals discovering common ground",
        timeline="one school day",
        twist_type="emotional reveal - shared struggles",
        character_arc="isolation to connection",
        voice_style="conversational, vulnerable, authentic",
        target_moral="we're not as alone as we think",
        locations="school cafeteria, library, hallway",
        mentioned_brands=None,
        goal="Create an emotionally engaging story about unexpected friendship"
    )
    
    # Save the story idea
    story_idea.to_file()
    print(f"✅ Story idea created: {story_idea.story_title}")
    print(f"   Overall potential score: {story_idea.potencial['overall']}")
    
    # Step 2: Generate initial script
    print("\n📝 Step 2: Generating script...")
    script_gen = ScriptGenerator(model="gpt-4o-mini")
    script_gen.generate_from_storyidea(story_idea)
    print("✅ Script generated")
    
    # Step 3: Revise the script
    print("\n✏️  Step 3: Revising script for voice clarity...")
    revise_gen = RevisedScriptGenerator(model="gpt-4o-mini")
    revise_gen.Revise(story_idea)
    print("✅ Script revised")
    
    # Step 4: Generate voiceover
    print("\n🎤 Step 4: Generating voiceover...")
    voice_maker = VoiceMaker()
    voice_maker.generate_audio()
    print("✅ Voiceover generated and normalized")
    
    # Step 5: Generate word-level subtitles
    print("\n💬 Step 5: Generating word-level subtitles...")
    title_gen = TitleGenerator(model_size="large-v2")
    title_gen.generate_titles()
    print("✅ Subtitles generated with word-level timing")
    
    print("\n" + "=" * 60)
    print("🎉 Pipeline completed successfully!")
    print(f"📁 Check output in: Stories/4_Titles/{story_idea.story_title}/")
    print("\nGenerated files:")
    print("  - Revised.txt (final script)")
    print("  - voiceover_normalized.mp3 (audio)")
    print("  - Subtitles_Word_By_Word.txt (SRT file)")
    print("  - idea.json (story metadata)")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Pipeline interrupted by user")
    except Exception as e:
        print(f"\n\n❌ Pipeline failed with error: {e}")
        import traceback
        traceback.print_exc()
