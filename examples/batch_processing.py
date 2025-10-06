# Example: Batch Processing Multiple Stories

"""
This example demonstrates how to batch process multiple stories through the pipeline.
Useful for generating multiple videos at once.
"""

from Models.StoryIdea import StoryIdea
from Generators.GScript import ScriptGenerator
from Generators.GRevise import RevisedScriptGenerator
from Generators.GVoice import VoiceMaker
from Generators.GTitles import TitleGenerator
from typing import List
import time

def create_story_ideas() -> List[StoryIdea]:
    """Create multiple story ideas for batch processing"""
    stories = [
        StoryIdea(
            story_title="The Secret Note",
            narrator_gender="female",
            tone="mysterious, emotional",
            theme="romance, secrets",
            narrator_type="first-person",
            emotional_core="curiosity, anticipation, surprise",
            twist_type="identity reveal",
            locations="high school, library"
        ),
        StoryIdea(
            story_title="The Last Text",
            narrator_gender="male",
            tone="emotional, heartfelt",
            theme="friendship, loss",
            narrator_type="first-person",
            emotional_core="grief, acceptance, gratitude",
            twist_type="emotional reveal",
            locations="bedroom, coffee shop"
        ),
        StoryIdea(
            story_title="Wrong Number",
            narrator_gender="female",
            tone="light, comedic, heartwarming",
            theme="unexpected connection",
            narrator_type="first-person",
            emotional_core="awkwardness, curiosity, joy",
            twist_type="positive surprise",
            locations="home, park"
        ),
    ]
    return stories

def process_batch(stories: List[StoryIdea]):
    """Process multiple stories through the pipeline"""
    print("🎬 Batch Processing Pipeline")
    print("=" * 60)
    print(f"📊 Processing {len(stories)} stories\n")
    
    # Initialize generators once (reuse for all stories)
    script_gen = ScriptGenerator(model="gpt-4o-mini")
    revise_gen = RevisedScriptGenerator(model="gpt-4o-mini")
    voice_maker = VoiceMaker()
    title_gen = TitleGenerator(model_size="large-v2")
    
    start_time = time.time()
    
    for idx, story in enumerate(stories, 1):
        print(f"\n{'='*60}")
        print(f"Processing Story {idx}/{len(stories)}: {story.story_title}")
        print(f"{'='*60}")
        
        try:
            # Save story idea
            print(f"\n📝 Saving story idea...")
            story.to_file()
            
            # Generate script
            print(f"📝 Generating script...")
            script_gen.generate_from_storyidea(story)
            print(f"✅ Script generated")
            
            # Revise script
            print(f"✏️  Revising script...")
            revise_gen.Revise(story)
            print(f"✅ Script revised")
            
            # Generate voiceover
            print(f"🎤 Generating voiceover...")
            voice_maker.generate_audio()
            print(f"✅ Voiceover generated")
            
            # Generate subtitles
            print(f"💬 Generating subtitles...")
            title_gen.generate_titles()
            print(f"✅ Subtitles generated")
            
            print(f"\n✨ Story '{story.story_title}' completed!")
            
        except Exception as e:
            print(f"\n❌ Error processing '{story.story_title}': {e}")
            print(f"⏭️  Continuing with next story...")
            continue
    
    elapsed_time = time.time() - start_time
    print(f"\n{'='*60}")
    print(f"🎉 Batch processing complete!")
    print(f"⏱️  Total time: {elapsed_time/60:.1f} minutes")
    print(f"📊 Average time per story: {elapsed_time/len(stories)/60:.1f} minutes")
    print(f"📁 Check output in: Stories/4_Titles/")

def main():
    # Create story ideas
    stories = create_story_ideas()
    
    # Show preview
    print("📋 Stories to be processed:")
    for idx, story in enumerate(stories, 1):
        print(f"  {idx}. {story.story_title} ({story.tone})")
    
    input("\n⏸️  Press Enter to start batch processing...")
    
    # Process batch
    process_batch(stories)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Batch processing interrupted by user")
    except Exception as e:
        print(f"\n\n❌ Batch processing failed: {e}")
        import traceback
        traceback.print_exc()
