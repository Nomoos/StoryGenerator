"""
Example demonstrating personalized and multi-lingual story generation.
"""
from Models.StoryIdea import StoryIdea
from Generators.GScript import ScriptGenerator


def generate_personalized_story():
    """Generate a story with user personalization."""
    
    # Example 1: English story with personalization
    idea_personalized = StoryIdea(
        story_title="My Friend {friend_name} Changed My Life",
        narrator_gender="female",
        tone="emotional, heartwarming",
        theme="friendship, personal growth",
        narrator_type="first-person",
        emotional_core="gratitude and transformation",
        goal="Tell a touching story about friendship",
        language="en",
        personalization={
            "friend_name": "Sarah",
            "city": "Seattle",
            "age": "sixteen"
        },
        voice_stability=0.6,  # More stable for emotional story
        voice_similarity_boost=0.8,  # Higher similarity
        voice_style_exaggeration=0.2,  # Slight style variation
        video_style="warm"
    )
    
    print("=" * 60)
    print("Generating PERSONALIZED English story...")
    print("=" * 60)
    generator = ScriptGenerator()
    generator.generate_from_storyidea(idea_personalized)
    print("\n✅ Personalized story generated!\n")


def generate_spanish_story():
    """Generate a Spanish language story."""
    
    idea_spanish = StoryIdea(
        story_title="El Secreto de Mi Hermana",
        narrator_gender="male",
        tone="misterioso, dramático",
        theme="family secrets, betrayal",
        narrator_type="first-person",
        emotional_core="shock and forgiveness",
        goal="Contar una historia dramática sobre secretos familiares",
        language="es",  # Spanish
        voice_stability=0.5,
        voice_similarity_boost=0.75,
        voice_style_exaggeration=0.3,
        video_style="dramatic"
    )
    
    print("=" * 60)
    print("Generating SPANISH story...")
    print("=" * 60)
    generator = ScriptGenerator()
    generator.generate_from_storyidea(idea_spanish)
    print("\n✅ Spanish story generated!\n")


def generate_french_story():
    """Generate a French language story."""
    
    idea_french = StoryIdea(
        story_title="L'Amour à Paris",
        narrator_gender="female",
        tone="romantique, poétique",
        theme="first love, cultural differences",
        narrator_type="first-person",
        emotional_core="romantic discovery",
        goal="Raconter une histoire d'amour à Paris",
        language="fr",  # French
        voice_stability=0.7,
        voice_similarity_boost=0.8,
        voice_style_exaggeration=0.1,
        video_style="cinematic"
    )
    
    print("=" * 60)
    print("Generating FRENCH story...")
    print("=" * 60)
    generator = ScriptGenerator()
    generator.generate_from_storyidea(idea_french)
    print("\n✅ French story generated!\n")


def generate_personalized_multilingual():
    """Generate a multi-lingual story with personalization."""
    
    idea_multi = StoryIdea(
        story_title="When I Met {person_name} in {city}",
        narrator_gender="female",
        tone="witty, chaotic, emotional",
        theme="mixed signals, unexpected confessions",
        narrator_type="first-person",
        emotional_core="confusion and clarity",
        goal="Tell a relatable teen romance story",
        language="en",
        personalization={
            "person_name": "Alex",
            "city": "Tokyo",
            "hobby": "anime"
        },
        locations="coffee shop, train station, rooftop",
        voice_stability=0.4,  # More variation for chaotic tone
        voice_similarity_boost=0.7,
        voice_style_exaggeration=0.4,  # More expressive
        video_style="dramatic"
    )
    
    print("=" * 60)
    print("Generating PERSONALIZED & MULTI-CULTURAL story...")
    print("=" * 60)
    generator = ScriptGenerator()
    generator.generate_from_storyidea(idea_multi)
    print("\n✅ Personalized multi-cultural story generated!\n")


if __name__ == "__main__":
    print("\n🌟 ENHANCED STORY GENERATION EXAMPLES 🌟\n")
    print("This script demonstrates:")
    print("  ✓ User personalization (name insertion)")
    print("  ✓ Multi-lingual support (Spanish, French)")
    print("  ✓ Voice inflection control (stability, similarity, style)")
    print("  ✓ Video style presets")
    print("\n" + "=" * 60 + "\n")
    
    # Uncomment the examples you want to run:
    generate_personalized_story()
    # generate_spanish_story()
    # generate_french_story()
    # generate_personalized_multilingual()
    
    print("\n" + "=" * 60)
    print("✨ All examples completed! Check the Scripts folder.")
    print("=" * 60)
