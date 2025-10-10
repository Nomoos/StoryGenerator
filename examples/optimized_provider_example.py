"""
Example: Using OptimizedOpenAIProvider with caching and cost tracking.

This example demonstrates the key features of the OptimizedOpenAIProvider:
- Token counting
- Cost tracking
- Response caching
- Usage statistics
"""

import os
from providers import OptimizedOpenAIProvider


def example_basic_usage():
    """Basic usage of OptimizedOpenAIProvider."""
    print("=" * 60)
    print("Example 1: Basic Usage")
    print("=" * 60)
    
    # Initialize provider (ensure OPENAI_API_KEY is set)
    provider = OptimizedOpenAIProvider(
        model="gpt-4o-mini",
        enable_cache=False  # Disable cache for this example
    )
    
    # Generate a simple completion
    prompt = "Write a haiku about programming"
    print(f"\nPrompt: {prompt}")
    
    response = provider.generate_completion(prompt)
    print(f"Response: {response}")
    
    # Check usage statistics
    stats = provider.get_usage_stats()
    print(f"\nUsage Statistics:")
    print(f"  Input tokens: {stats['total_input_tokens']}")
    print(f"  Output tokens: {stats['total_output_tokens']}")
    print(f"  Total tokens: {stats['total_tokens']}")
    print(f"  Cost: ${stats['total_cost']:.6f}")
    print()


def example_token_counting():
    """Demonstrate token counting before API calls."""
    print("=" * 60)
    print("Example 2: Token Counting")
    print("=" * 60)
    
    provider = OptimizedOpenAIProvider(model="gpt-4o-mini")
    
    # Count tokens in a simple text
    text = "Hello, world! This is a test of token counting."
    token_count = provider.count_tokens(text)
    print(f"\nText: '{text}'")
    print(f"Token count: {token_count}")
    
    # Count tokens in messages
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "What is the capital of France?"}
    ]
    message_tokens = provider.count_messages_tokens(messages)
    print(f"\nMessages token count: {message_tokens}")
    
    # Estimate cost before making the call
    estimated_output_tokens = 50
    estimated_cost = provider.estimate_cost(message_tokens, estimated_output_tokens)
    print(f"Estimated cost: ${estimated_cost:.6f}")
    print()


def example_caching():
    """Demonstrate response caching."""
    print("=" * 60)
    print("Example 3: Response Caching")
    print("=" * 60)
    
    # Initialize with caching enabled
    provider = OptimizedOpenAIProvider(
        model="gpt-4o-mini",
        enable_cache=True,
        cache_ttl=3600,  # Cache for 1 hour
        cache_backend="file"
    )
    
    prompt = "What is artificial intelligence?"
    
    # First call - makes API request
    print(f"\nFirst call with prompt: '{prompt}'")
    print("Making API request...")
    response1 = provider.generate_completion(prompt)
    print(f"Response: {response1[:100]}...")
    
    stats1 = provider.get_usage_stats()
    print(f"Requests made: {stats1['request_count']}")
    
    # Second call - uses cache
    print(f"\nSecond call with same prompt...")
    print("Checking cache...")
    response2 = provider.generate_completion(prompt)
    print(f"Response: {response2[:100]}...")
    
    stats2 = provider.get_usage_stats()
    print(f"Requests made: {stats2['request_count']}")  # Should be same as before
    
    # Verify responses are identical
    assert response1 == response2, "Responses should be identical!"
    print("\n✓ Responses are identical (from cache)")
    
    # Show cache statistics
    cache_stats = stats2['cache_stats']
    print(f"\nCache Statistics:")
    print(f"  Hits: {cache_stats['hits']}")
    print(f"  Misses: {cache_stats['misses']}")
    print(f"  Hit rate: {cache_stats['hit_rate']:.2%}")
    print()


def example_cost_tracking():
    """Demonstrate cost tracking across multiple requests."""
    print("=" * 60)
    print("Example 4: Cost Tracking")
    print("=" * 60)
    
    provider = OptimizedOpenAIProvider(
        model="gpt-4o-mini",
        enable_cache=False
    )
    
    # Make multiple requests
    topics = ["AI", "Machine Learning", "Deep Learning"]
    
    print("\nGenerating summaries for multiple topics...")
    for topic in topics:
        prompt = f"Explain {topic} in one sentence"
        response = provider.generate_completion(prompt)
        print(f"\n{topic}: {response}")
    
    # Get comprehensive statistics
    stats = provider.get_usage_stats()
    
    print("\n" + "=" * 60)
    print("Final Usage Statistics:")
    print("=" * 60)
    print(f"Total requests: {stats['request_count']}")
    print(f"Total input tokens: {stats['total_input_tokens']}")
    print(f"Total output tokens: {stats['total_output_tokens']}")
    print(f"Total tokens: {stats['total_tokens']}")
    print(f"Total cost: ${stats['total_cost']:.6f}")
    print(f"Average tokens per request: {stats['average_tokens_per_request']:.2f}")
    print(f"Average cost per request: ${stats['total_cost']/stats['request_count']:.6f}")
    print()


def example_batch_with_monitoring():
    """Demonstrate batch processing with cost monitoring."""
    print("=" * 60)
    print("Example 5: Batch Processing with Cost Monitoring")
    print("=" * 60)
    
    provider = OptimizedOpenAIProvider(model="gpt-4o-mini")
    
    # Set a cost threshold
    cost_threshold = 0.01  # $0.01 limit for demo
    
    items = [
        "Write a tagline for a coffee shop",
        "Write a tagline for a bookstore",
        "Write a tagline for a gym",
        "Write a tagline for a restaurant",
        "Write a tagline for a tech startup"
    ]
    
    results = []
    
    print(f"\nProcessing {len(items)} items with cost threshold: ${cost_threshold:.2f}")
    print("-" * 60)
    
    for i, item in enumerate(items, 1):
        # Check cost before processing
        current_stats = provider.get_usage_stats()
        
        if current_stats['total_cost'] > cost_threshold:
            print(f"\n⚠️  Cost threshold reached!")
            print(f"Processed {i-1}/{len(items)} items")
            break
        
        # Process item
        response = provider.generate_completion(item)
        results.append(response)
        
        # Show progress
        stats = provider.get_usage_stats()
        print(f"{i}. {response}")
        print(f"   Cost so far: ${stats['total_cost']:.6f}")
    
    # Final report
    final_stats = provider.get_usage_stats()
    print("\n" + "=" * 60)
    print("Batch Processing Complete")
    print("=" * 60)
    print(f"Items processed: {len(results)}/{len(items)}")
    print(f"Total cost: ${final_stats['total_cost']:.6f}")
    print(f"Average cost per item: ${final_stats['total_cost']/len(results):.6f}")
    print()


def example_chat_completion():
    """Demonstrate chat completion with conversation context."""
    print("=" * 60)
    print("Example 6: Chat Completion")
    print("=" * 60)
    
    provider = OptimizedOpenAIProvider(model="gpt-4o-mini")
    
    # Create a conversation
    messages = [
        {"role": "system", "content": "You are a helpful coding assistant."},
        {"role": "user", "content": "How do I sort a list in Python?"},
    ]
    
    print("\nConversation:")
    print(f"System: {messages[0]['content']}")
    print(f"User: {messages[1]['content']}")
    
    # Generate response
    response = provider.generate_chat(messages, temperature=0.7)
    print(f"Assistant: {response}")
    
    # Show usage
    stats = provider.get_usage_stats()
    print(f"\nTokens used: {stats['total_tokens']}")
    print(f"Cost: ${stats['total_cost']:.6f}")
    print()


def main():
    """Run all examples."""
    # Check for API key
    if not os.getenv("OPENAI_API_KEY"):
        print("Error: OPENAI_API_KEY environment variable not set")
        print("Please set it to run these examples:")
        print("  export OPENAI_API_KEY='your-key-here'")
        return
    
    print("\n" + "=" * 60)
    print("OptimizedOpenAIProvider Examples")
    print("=" * 60)
    print()
    
    try:
        # Note: These examples make real API calls if you have an API key
        # Comment out examples you don't want to run
        
        example_basic_usage()
        example_token_counting()
        # example_caching()  # Uncomment to test caching
        # example_cost_tracking()  # Uncomment to track costs
        # example_batch_with_monitoring()  # Uncomment for batch processing
        # example_chat_completion()  # Uncomment for chat example
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("Make sure your OPENAI_API_KEY is valid and you have sufficient credits.")


if __name__ == "__main__":
    main()
