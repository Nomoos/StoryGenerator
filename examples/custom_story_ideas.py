# Example: Creating Custom Story Ideas

"""
This example shows different ways to create story ideas with various parameters.
Demonstrates the flexibility of the StoryIdea model.
"""

from Models.StoryIdea import StoryIdea
import json

def example_emotional_story():
    """Emotional, heartfelt story"""
    return StoryIdea(
        story_title="The Letter I Never Sent",
        narrator_gender="female",
        tone="emotional, melancholic, bittersweet",
        theme="loss, regret, closure",
        narrator_type="first-person",
        other_character="a lost friend",
        outcome="emotional acceptance",
        emotional_core="grief, regret, healing",
        power_dynamic="remembering someone lost",
        timeline="reflection over years",
        twist_type="emotional reveal about unsent letter",
        character_arc="denial to acceptance",
        voice_style="vulnerable, reflective, sincere",
        target_moral="it's never too late to forgive yourself",
        locations="bedroom, old park bench, coffee shop",
        goal="Create a deeply emotional story about unspoken words"
    )

def example_comedy_story():
    """Light, comedic story"""
    return StoryIdea(
        story_title="The Zoom Call Disaster",
        narrator_gender="male",
        tone="comedic, light, relatable",
        theme="embarrassment, work-from-home chaos",
        narrator_type="first-person",
        other_character="boss and colleagues",
        outcome="humorous with lesson learned",
        emotional_core="embarrassment, panic, humor",
        power_dynamic="employee trying to save face",
        timeline="one morning",
        twist_type="comedic reveal of what boss actually saw",
        character_arc="panic to embracing imperfection",
        voice_style="energetic, self-deprecating, humorous",
        target_moral="everyone has embarrassing moments",
        locations="home office, kitchen",
        mentioned_brands="Zoom",
        goal="Create a relatable comedy about remote work fails"
    )

def example_mystery_story():
    """Suspenseful mystery"""
    return StoryIdea(
        story_title="The Anonymous Gift",
        narrator_gender="female",
        tone="mysterious, suspenseful, intriguing",
        theme="mystery, stalking, unexpected truth",
        narrator_type="first-person",
        other_character="unknown gift sender",
        outcome="surprising positive reveal",
        emotional_core="fear, curiosity, relief",
        power_dynamic="feeling watched, then understanding",
        timeline="one week",
        twist_type="identity reveal - caring motivation",
        character_arc="fear to gratitude",
        voice_style="tense, questioning, relieved",
        target_moral="sometimes care comes from unexpected places",
        locations="apartment, mailbox, workplace",
        goal="Create a suspenseful story with a heartwarming twist"
    )

def example_romance_story():
    """Romantic, sweet story"""
    return StoryIdea(
        story_title="Coffee Shop Conversations",
        narrator_gender="female",
        tone="romantic, sweet, hopeful",
        theme="romance, connection, courage",
        narrator_type="first-person",
        other_character="regular customer",
        outcome="positive romantic progression",
        emotional_core="attraction, nervousness, joy",
        power_dynamic="equals with mutual interest",
        timeline="three weeks",
        twist_type="mutual reveal of feelings",
        character_arc="shy observation to brave action",
        voice_style="warm, hopeful, slightly nervous",
        target_moral="taking chances can lead to beautiful connections",
        locations="coffee shop, rainy street, park",
        goal="Create a sweet romance about everyday moments"
    )

def example_minimal_story():
    """Minimal required fields only"""
    return StoryIdea(
        story_title="Simple Story",
        narrator_gender="male"
    )

def main():
    print("🎨 Creating Custom Story Ideas")
    print("=" * 60)
    
    stories = [
        ("Emotional Story", example_emotional_story()),
        ("Comedy Story", example_comedy_story()),
        ("Mystery Story", example_mystery_story()),
        ("Romance Story", example_romance_story()),
        ("Minimal Story", example_minimal_story())
    ]
    
    for category, story in stories:
        print(f"\n📖 {category}: {story.story_title}")
        print(f"   Tone: {story.tone or 'Not specified'}")
        print(f"   Theme: {story.theme or 'Not specified'}")
        print(f"   Emotional Core: {story.emotional_core or 'Not specified'}")
        
        # Save to file
        story.to_file()
        print(f"   ✅ Saved to: Stories/0_Ideas/{story.story_title}.json")
        
        # Show potential score
        print(f"   📊 Overall Potential: {story.potencial['overall']}/10")
    
    print("\n" + "=" * 60)
    print("✨ All story ideas created!")
    print("📁 Check: Stories/0_Ideas/")
    
    # Example: Load story from file
    print("\n📥 Example: Loading story from file")
    loaded_story = StoryIdea.from_file("Stories/0_Ideas/Simple_Story.json")
    print(f"   Loaded: {loaded_story.story_title}")
    print(f"   JSON content:")
    print(json.dumps(loaded_story.to_dict(), indent=2))

if __name__ == "__main__":
    main()
