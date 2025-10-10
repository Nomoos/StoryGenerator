# Optimized OpenAI Provider - Usage Guide

## Overview

The `OptimizedOpenAIProvider` extends the basic OpenAI provider with advanced features including token counting, cost tracking, and built-in response caching. It's designed to help you monitor and optimize your OpenAI API usage while reducing costs.

## Features

- 🔢 **Token Counting** - Count tokens before making API calls using tiktoken
- 💰 **Cost Tracking** - Track costs per operation and cumulative costs
- 🚀 **Built-in Caching** - Cache identical requests to reduce API calls
- 📊 **Usage Statistics** - Monitor requests, tokens, and costs
- 🔄 **Automatic Retry** - Retry on rate limits with exponential backoff
- ⚡ **Interface Compatible** - Implements `ILLMProvider` interface

## Installation

Required dependencies:

```bash
pip install openai>=1.50.0 tiktoken>=0.5.0 tenacity>=8.0.0
```

Optional for caching:

```bash
pip install redis>=5.0.0  # For Redis cache backend
```

## Quick Start

### Basic Usage

```python
from providers import OptimizedOpenAIProvider

# Initialize provider with caching enabled
provider = OptimizedOpenAIProvider(
    model="gpt-4o-mini",
    enable_cache=True,
    cache_ttl=3600  # Cache for 1 hour
)

# Generate completion
response = provider.generate_completion("Write a haiku about coding")
print(response)

# Check usage statistics
stats = provider.get_usage_stats()
print(f"Tokens used: {stats['total_tokens']}")
print(f"Cost: ${stats['total_cost']:.4f}")
print(f"Cache hit rate: {stats['cache_stats']['hit_rate']:.2%}")
```

### Chat Completions

```python
# Chat completion
messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Explain quantum computing in simple terms."}
]

response = provider.generate_chat(messages, temperature=0.7)
print(response)
```

## Advanced Features

### Token Counting

Count tokens before making API calls to estimate costs:

```python
provider = OptimizedOpenAIProvider()

# Count tokens in text
text = "Hello, world! This is a test."
token_count = provider.count_tokens(text)
print(f"Tokens: {token_count}")

# Count tokens in messages
messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Hello!"}
]
token_count = provider.count_messages_tokens(messages)
print(f"Total tokens in messages: {token_count}")

# Estimate cost before making call
input_tokens = 100
output_tokens = 50
estimated_cost = provider.estimate_cost(input_tokens, output_tokens)
print(f"Estimated cost: ${estimated_cost:.6f}")
```

### Cost Tracking

Track costs across multiple requests:

```python
provider = OptimizedOpenAIProvider(model="gpt-4o-mini")

# Make multiple requests
for topic in ["AI", "ML", "NLP"]:
    provider.generate_completion(f"Explain {topic} in one sentence")

# Get comprehensive statistics
stats = provider.get_usage_stats()
print(f"""
Usage Statistics:
- Total requests: {stats['request_count']}
- Input tokens: {stats['total_input_tokens']}
- Output tokens: {stats['total_output_tokens']}
- Total tokens: {stats['total_tokens']}
- Total cost: ${stats['total_cost']:.4f}
- Average tokens per request: {stats['average_tokens_per_request']:.2f}
""")

# Reset statistics for new tracking period
provider.reset_stats()
```

### Caching

Enable caching to avoid duplicate API calls:

```python
# Initialize with caching
provider = OptimizedOpenAIProvider(
    enable_cache=True,
    cache_ttl=7200,  # Cache for 2 hours
    cache_backend="file"  # or "redis"
)

# First call makes API request
result1 = provider.generate_completion("What is Python?")
print(f"Request count: {provider.request_count}")  # 1

# Second identical call uses cache (no API call!)
result2 = provider.generate_completion("What is Python?")
print(f"Request count: {provider.request_count}")  # Still 1

# Results are identical
assert result1 == result2

# Check cache statistics
cache_stats = provider.get_usage_stats()["cache_stats"]
print(f"Cache hit rate: {cache_stats['hit_rate']:.2%}")
```

### Batch API Pricing

Use the batch pricing tier to calculate costs for asynchronous batch operations (50% discount):

```python
# Initialize with batch pricing tier
provider = OptimizedOpenAIProvider(
    model="gpt-4o-mini",
    pricing_tier="batch"
)

# Cost estimation uses batch pricing
input_tokens = 1000
output_tokens = 500
cost = provider.estimate_cost(input_tokens, output_tokens)
print(f"Batch API cost: ${cost:.6f}")

# Compare standard vs batch pricing
comparison = provider.compare_pricing_tiers(input_tokens, output_tokens)
print(f"""
Pricing Comparison:
- Standard API: ${comparison['standard_cost']:.6f}
- Batch API: ${comparison['batch_cost']:.6f}
- Savings: ${comparison['savings']:.6f} ({comparison['savings_percent']:.1f}%)
""")
```

### Video Cost Estimation

Calculate the estimated cost per video based on average token usage:

```python
provider = OptimizedOpenAIProvider(
    model="gpt-4o-mini",
    pricing_tier="batch"  # Use batch pricing for cost savings
)

# Estimate cost per video
# Typical video generation might use:
# - Script generation: ~500 input, ~2000 output tokens
# - Script revision: ~2500 input, ~2000 output tokens
# - Title generation: ~200 input, ~50 output tokens
video_cost = provider.estimate_video_cost(
    avg_input_tokens_per_request=1067,  # Average across all requests
    avg_output_tokens_per_request=1350,  # Average across all requests
    requests_per_video=3  # Number of API calls per video
)

print(f"""
Video Cost Estimate:
- Model: {video_cost['model']}
- Pricing tier: {video_cost['pricing_tier']}
- Cost per request: ${video_cost['cost_per_request']:.6f}
- Cost per video: ${video_cost['cost_per_video']:.6f}
- Total tokens per video: {video_cost['total_tokens_per_video']:,}
- Requests per video: {video_cost['requests_per_video']}
""")

# Compare costs for 100 videos
videos = 100
total_batch = video_cost['cost_per_video'] * videos
print(f"Cost for {videos} videos (batch pricing): ${total_batch:.2f}")

# Compare with standard pricing
video_cost_standard = provider.estimate_video_cost(
    avg_input_tokens_per_request=1067,
    avg_output_tokens_per_request=1350,
    requests_per_video=3,
    pricing_tier="standard"
)
total_standard = video_cost_standard['cost_per_video'] * videos
print(f"Cost for {videos} videos (standard pricing): ${total_standard:.2f}")
print(f"Total savings with batch API: ${total_standard - total_batch:.2f}")
```

## Real-World Examples

### Example 1: Story Generation Pipeline

```python
from providers import OptimizedOpenAIProvider

class StoryGenerator:
    def __init__(self):
        self.provider = OptimizedOpenAIProvider(
            model="gpt-4o-mini",
            enable_cache=True,
            cache_ttl=86400  # Cache for 24 hours
        )
    
    def generate_story_ideas(self, topic: str, count: int = 3) -> list[str]:
        """Generate multiple story ideas with cost tracking."""
        ideas = []
        
        for i in range(count):
            messages = [
                {"role": "system", "content": "You are a creative writer."},
                {"role": "user", "content": f"Generate story idea #{i+1} about {topic}"}
            ]
            idea = self.provider.generate_chat(messages)
            ideas.append(idea)
        
        # Log costs
        stats = self.provider.get_usage_stats()
        print(f"Generated {count} ideas")
        print(f"Cost: ${stats['total_cost']:.4f}")
        print(f"Tokens: {stats['total_tokens']}")
        
        return ideas
    
    def get_daily_cost(self) -> float:
        """Get total cost for the day."""
        return self.provider.get_usage_stats()["total_cost"]

# Usage
generator = StoryGenerator()
ideas = generator.generate_story_ideas("space exploration", count=5)
print(f"Total daily cost: ${generator.get_daily_cost():.4f}")
```

### Example 2: Batch Processing with Cost Monitoring

```python
from providers import OptimizedOpenAIProvider

def process_batch_with_monitoring(items: list[str]) -> list[str]:
    """Process items with cost monitoring and alerts."""
    provider = OptimizedOpenAIProvider(
        model="gpt-4o-mini",
        enable_cache=True
    )
    
    results = []
    cost_threshold = 1.00  # Alert if cost exceeds $1.00
    
    for item in items:
        # Process item
        result = provider.generate_completion(f"Process: {item}")
        results.append(result)
        
        # Check cost after each item
        stats = provider.get_usage_stats()
        if stats['total_cost'] > cost_threshold:
            print(f"⚠️ WARNING: Cost threshold exceeded!")
            print(f"Current cost: ${stats['total_cost']:.4f}")
            # Could pause processing, send alert, etc.
            break
    
    # Final report
    final_stats = provider.get_usage_stats()
    print(f"""
Batch Processing Complete:
- Items processed: {len(results)}/{len(items)}
- Total cost: ${final_stats['total_cost']:.4f}
- Cache hit rate: {final_stats['cache_stats']['hit_rate']:.2%}
- Average cost per item: ${final_stats['total_cost']/len(results):.4f}
    """)
    
    return results

# Usage
items = ["item1", "item2", "item3", "item4", "item5"]
results = process_batch_with_monitoring(items)
```

### Example 3: Cost Comparison Between Models

```python
from providers import OptimizedOpenAIProvider

def compare_model_costs(prompt: str, models: list[str]) -> dict:
    """Compare costs and performance across different models."""
    results = {}
    
    for model in models:
        provider = OptimizedOpenAIProvider(
            model=model,
            enable_cache=False  # Disable to get accurate comparison
        )
        
        # Generate completion
        response = provider.generate_completion(prompt)
        stats = provider.get_usage_stats()
        
        results[model] = {
            "response": response,
            "tokens": stats['total_tokens'],
            "cost": stats['total_cost'],
            "cost_per_token": stats['total_cost'] / stats['total_tokens']
        }
    
    # Print comparison
    print("\nModel Comparison:")
    print("-" * 60)
    for model, data in results.items():
        print(f"{model}:")
        print(f"  Tokens: {data['tokens']}")
        print(f"  Cost: ${data['cost']:.6f}")
        print(f"  Cost/Token: ${data['cost_per_token']:.8f}")
    
    return results

# Usage
models = ["gpt-4o-mini", "gpt-3.5-turbo"]
prompt = "Explain machine learning in 100 words"
comparison = compare_model_costs(prompt, models)
```

## Configuration

### Model Pricing

The provider includes pricing for common models (per 1M tokens) with support for both standard and batch API pricing:

#### Standard API Pricing (Real-time/Synchronous)

| Model | Input Price | Output Price |
|-------|------------|--------------|
| gpt-4o-mini | $0.15 | $0.60 |
| gpt-4o | $2.50 | $10.00 |
| gpt-4-turbo | $10.00 | $30.00 |
| gpt-3.5-turbo | $0.50 | $1.50 |

#### Batch API Pricing (50% Discount - Asynchronous)

| Model | Input Price | Output Price | Savings |
|-------|------------|--------------|---------|
| gpt-4o-mini | $0.075 | $0.30 | 50% |
| gpt-4o | $1.25 | $5.00 | 50% |
| gpt-4-turbo | $5.00 | $15.00 | 50% |
| gpt-3.5-turbo | $0.25 | $0.75 | 50% |

**Note:** The Batch API offers 50% cost savings for asynchronous bulk operations. Use `pricing_tier="batch"` when initializing the provider to calculate costs using batch pricing.

Update pricing in `providers/openai_optimized.py` if needed.

### Environment Variables

```bash
# Required
OPENAI_API_KEY=sk-your-key-here

# Optional
CACHE_BACKEND=file  # or 'redis'
CACHE_DIR=./cache
REDIS_HOST=localhost
REDIS_PORT=6379
```

### Initialization Options

```python
OptimizedOpenAIProvider(
    api_key=None,              # API key (or from OPENAI_API_KEY env)
    model="gpt-4o-mini",       # Model to use
    enable_cache=True,         # Enable response caching
    cache_ttl=3600,            # Cache TTL in seconds
    cache_backend="file",      # Cache backend: 'file' or 'redis'
    pricing_tier="standard"    # Pricing tier: 'standard' or 'batch'
)
```

## Best Practices

### 1. Enable Caching for Repeated Queries

```python
# Good - caching enabled
provider = OptimizedOpenAIProvider(enable_cache=True)
for _ in range(10):
    result = provider.generate_completion("What is AI?")
# Only 1 API call made!
```

### 2. Monitor Costs Regularly

```python
# Add cost monitoring to your application
def log_usage_stats(provider):
    stats = provider.get_usage_stats()
    logger.info(f"OpenAI usage - Cost: ${stats['total_cost']:.4f}, "
                f"Requests: {stats['request_count']}")
```

### 3. Use Appropriate Models

```python
# Use cheaper models for simple tasks
simple_provider = OptimizedOpenAIProvider(model="gpt-4o-mini")

# Use powerful models only when needed
complex_provider = OptimizedOpenAIProvider(model="gpt-4o")
```

### 4. Count Tokens Before Long Requests

```python
provider = OptimizedOpenAIProvider()

# Check token count first
messages = [...]
token_count = provider.count_messages_tokens(messages)

if token_count > 8000:
    print("Warning: Large request, high cost expected")
    estimated_cost = provider.estimate_cost(token_count, 500)
    print(f"Estimated cost: ${estimated_cost:.4f}")
```

### 5. Reset Stats for Different Tracking Periods

```python
# Daily tracking
provider = OptimizedOpenAIProvider()

# ... do work ...

daily_cost = provider.get_usage_stats()["total_cost"]
print(f"Daily cost: ${daily_cost:.2f}")

# Reset for next day
provider.reset_stats()
```

## Troubleshooting

### High Costs

1. Check if caching is enabled
2. Review token counts - are prompts too long?
3. Consider using a cheaper model (gpt-4o-mini)
4. Reduce max_tokens parameter

### Cache Not Working

1. Verify `enable_cache=True`
2. Check cache_ttl isn't too short
3. Ensure identical inputs for cache hits
4. Check cache directory permissions

### Token Count Mismatch

Token counting is approximate. OpenAI's actual count may differ slightly due to:
- Message formatting overhead
- Special tokens
- Model-specific encoding

## API Reference

### Class: OptimizedOpenAIProvider

Implements `ILLMProvider` interface.

#### Methods

##### `__init__(api_key, model, enable_cache, cache_ttl, cache_backend)`
Initialize provider.

##### `generate_completion(prompt, temperature, max_tokens, **kwargs) -> str`
Generate completion from prompt.

##### `generate_chat(messages, temperature, max_tokens, **kwargs) -> str`
Generate chat completion.

##### `count_tokens(text: str) -> int`
Count tokens in text.

##### `count_messages_tokens(messages: list) -> int`
Count tokens in messages.

##### `estimate_cost(input_tokens: int, output_tokens: int) -> float`
Estimate cost for given token counts.

##### `get_usage_stats() -> dict`
Get usage statistics.

##### `reset_stats()`
Reset usage statistics.

#### Properties

##### `model_name -> str`
Get the model name.

## See Also

- [Caching Guide](./CACHING_GUIDE.md) - Detailed caching documentation
- [OpenAI Provider](../providers/openai_provider.py) - Basic provider implementation
- [Core Interfaces](../core/interfaces/llm_provider.py) - Interface definitions
