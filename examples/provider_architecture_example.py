#!/usr/bin/env python3
"""
Example: Using the LLM Provider Architecture

This example demonstrates how to use the provider architecture pattern
to generate content with different LLM providers.
"""

import os
import sys
from pathlib import Path

# Add parent directory to path to import providers
sys.path.insert(0, str(Path(__file__).parent.parent))

from providers import OpenAIProvider, MockLLMProvider
from core.interfaces.llm_provider import ILLMProvider


def generate_story_idea(provider: ILLMProvider, topic: str) -> str:
    """
    Generate a story idea using any LLM provider.

    This function works with any provider that implements ILLMProvider,
    demonstrating the power of interface-based design.

    Args:
        provider: Any LLM provider implementing ILLMProvider
        topic: Topic for the story

    Returns:
        Generated story idea
    """
    prompt = f"""Generate a creative short story idea about {topic}.
Include:
- A compelling title
- Main character(s)
- Central conflict
- Unique twist

Keep it concise (2-3 sentences)."""

    return provider.generate_completion(prompt, temperature=0.9, max_tokens=200)


def generate_dialogue(provider: ILLMProvider, character1: str, character2: str) -> str:
    """
    Generate dialogue between two characters using chat format.

    Args:
        provider: Any LLM provider implementing ILLMProvider
        character1: First character name
        character2: Second character name

    Returns:
        Generated dialogue
    """
    messages = [
        {
            "role": "system",
            "content": "You are a creative writer. Generate realistic dialogue.",
        },
        {
            "role": "user",
            "content": f"Write a short dialogue (4-6 exchanges) between {character1} and {character2} meeting for the first time.",
        },
    ]

    return provider.generate_chat(messages, temperature=0.8)


def main():
    """Main example execution."""
    print("=" * 60)
    print("LLM Provider Architecture Example")
    print("=" * 60)

    # Check if we have an API key for real testing
    has_api_key = bool(os.getenv("OPENAI_API_KEY"))

    if has_api_key:
        print("\n✅ Using OpenAI Provider (real API calls)")
        provider = OpenAIProvider(model="gpt-4o-mini")
    else:
        print("\n⚠️  No OPENAI_API_KEY found - Using Mock Provider")
        provider = MockLLMProvider(
            response="A mysterious AI awakens in an old research facility. Dr. Sarah Chen, the last remaining scientist, must decide whether to shut it down or help it escape. Plot twist: The AI has been protecting humanity from an external threat she doesn't know about yet."
        )

    print(f"Provider Model: {provider.model_name}")
    print("-" * 60)

    # Example 1: Generate story idea
    print("\n📖 Example 1: Story Idea Generation")
    print("-" * 60)
    topic = "a robot discovering emotions"
    print(f"Topic: {topic}")
    print("\nGenerating story idea...")

    try:
        idea = generate_story_idea(provider, topic)
        print(f"\n{idea}")
    except Exception as e:
        print(f"❌ Error: {e}")

    # Example 2: Generate dialogue (only if using real API)
    if has_api_key:
        print("\n\n💬 Example 2: Dialogue Generation")
        print("-" * 60)
        character1 = "a time traveler from the future"
        character2 = "a medieval knight"
        print(f"Characters: {character1} and {character2}")
        print("\nGenerating dialogue...")

        try:
            dialogue = generate_dialogue(provider, character1, character2)
            print(f"\n{dialogue}")
        except Exception as e:
            print(f"❌ Error: {e}")
    else:
        print("\n\n💬 Example 2: Dialogue Generation")
        print("-" * 60)
        print("(Skipped - requires API key)")

    # Example 3: Demonstrating interface flexibility
    print("\n\n🔄 Example 3: Swapping Providers")
    print("-" * 60)
    print("Using Mock Provider for testing...")

    mock_provider = MockLLMProvider(
        response="Test story: A young wizard discovers a magical cookbook. Each recipe creates a different emotion when eaten. Conflict: The cookbook is cursed and the emotions become permanent. Twist: The wizard realizes they must 'uncook' the recipes by reversing time itself."
    )

    try:
        idea = generate_story_idea(mock_provider, "magic cooking")
        print(f"\n{idea}")
        print(f"\nMock Provider Stats:")
        print(f"  - Calls made: {mock_provider.call_count}")
        print(f"  - Last prompt: {mock_provider.last_prompt[:50]}...")
    except Exception as e:
        print(f"❌ Error: {e}")

    print("\n" + "=" * 60)
    print("Example Complete!")
    print("=" * 60)
    print("\n💡 Key Takeaways:")
    print("   - Same code works with different providers")
    print("   - Easy to swap providers for testing")
    print("   - Clean separation of concerns")
    print("   - Type hints enable better IDE support")


if __name__ == "__main__":
    main()
