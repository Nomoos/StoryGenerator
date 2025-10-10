# Caching Module - Usage Guide

## Overview

The caching module provides a simple yet powerful way to cache expensive operations like LLM API calls, image generation, and other costly computations. It supports both file-based and Redis backends with automatic TTL (Time-To-Live) management.

## Features

- 🚀 **Simple Decorator API** - Add `@cache.cached()` to any function
- 💾 **Multiple Backends** - File-based or Redis storage
- ⏰ **TTL Support** - Automatic expiration of cached entries
- 📊 **Statistics** - Track cache hits, misses, and hit rate
- 🔄 **Cache Invalidation** - Clear all or specific cache entries
- 🛡️ **Error Handling** - Fails gracefully without breaking your application

## Installation

The cache module is included in the core package. For Redis support:

```bash
pip install redis>=5.0.0
```

## Basic Usage

### File-Based Cache (Default)

```python
from core.cache import CacheManager

# Initialize cache with file backend
cache = CacheManager(backend="file", cache_dir="./cache")

# Use as a decorator
@cache.cached(ttl=3600)  # Cache for 1 hour
def expensive_operation(param: str) -> str:
    # This expensive operation will only run once per unique input
    result = some_expensive_computation(param)
    return result

# First call - executes function and caches result
result1 = expensive_operation("input1")

# Second call with same input - returns cached result
result2 = expensive_operation("input1")  # Fast! From cache
```

### Redis Cache

```python
from core.cache import CacheManager

# Initialize cache with Redis backend
cache = CacheManager(backend="redis", cache_dir="./cache")

@cache.cached(ttl=7200)  # Cache for 2 hours
def fetch_data_from_api(endpoint: str) -> dict:
    response = requests.get(f"https://api.example.com/{endpoint}")
    return response.json()
```

### Global Cache Instance

```python
from core.cache import get_cache

# Get the default cache instance (singleton)
cache = get_cache(backend="file", cache_dir="./cache")

@cache.cached(ttl=1800)  # Cache for 30 minutes
def process_data(data_id: int) -> dict:
    return {"processed": True, "id": data_id}
```

## Advanced Usage

### Manual Cache Control

```python
from core.cache import CacheManager

cache = CacheManager()

# Manually set a value
cache.set("my_key", {"data": "value"}, ttl=3600)

# Manually get a value
value = cache.get("my_key")
if value:
    print(f"Found in cache: {value}")
else:
    print("Cache miss")

# Invalidate specific or all entries
cache.invalidate()  # Clear all cache
```

### Cache Statistics

```python
cache = CacheManager()

@cache.cached(ttl=3600)
def my_function(x: int) -> int:
    return x * 2

# Make some calls
my_function(1)
my_function(1)  # Hit
my_function(2)  # Miss

# Get statistics
stats = cache.get_stats()
print(f"Hit rate: {stats['hit_rate']:.2%}")
print(f"Total hits: {stats['hits']}")
print(f"Total misses: {stats['misses']}")
print(f"Total requests: {stats['total_requests']}")

# Reset statistics
cache.clear_stats()
```

## Real-World Examples

### Example 1: Caching LLM Responses

```python
from core.cache import get_cache
from providers import OptimizedOpenAIProvider

cache = get_cache(backend="file", cache_dir="./cache/llm")
provider = OptimizedOpenAIProvider()

@cache.cached(ttl=86400)  # Cache for 24 hours
def generate_story_idea(topic: str) -> str:
    """Generate a story idea. Cached to avoid duplicate API calls."""
    messages = [
        {"role": "system", "content": "You are a creative story writer."},
        {"role": "user", "content": f"Generate a story idea about {topic}"}
    ]
    return provider.generate_chat(messages)

# First call makes API request
idea1 = generate_story_idea("space exploration")

# Second call returns cached result (no API call!)
idea2 = generate_story_idea("space exploration")

assert idea1 == idea2
```

### Example 2: Caching Database Queries

```python
from core.cache import CacheManager

cache = CacheManager(backend="redis")

@cache.cached(ttl=300)  # Cache for 5 minutes
def get_user_profile(user_id: int) -> dict:
    """Fetch user profile from database."""
    # Expensive database query
    result = database.query(
        "SELECT * FROM users WHERE id = ?", 
        user_id
    )
    return result.to_dict()
```

### Example 3: Caching API Responses

```python
import requests
from core.cache import get_cache

cache = get_cache()

@cache.cached(ttl=1800)  # Cache for 30 minutes
def fetch_trending_topics() -> list:
    """Fetch trending topics from external API."""
    response = requests.get("https://api.example.com/trending")
    return response.json()["topics"]

# Efficient - only calls API once per 30 minutes
topics = fetch_trending_topics()
```

## Configuration

### Cache Directory Structure

File-based cache creates the following structure:

```
./cache/
├── abc123.json       # Cached value
├── abc123.meta       # Metadata (expiration time)
├── def456.json
└── def456.meta
```

### Environment Variables

You can configure caching behavior through environment variables:

```bash
# Default cache backend
CACHE_BACKEND=file  # or 'redis'

# Redis configuration (if using Redis)
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0
```

## Best Practices

1. **Choose Appropriate TTL**: Balance between freshness and cache efficiency
   - Frequently changing data: 5-30 minutes
   - Stable data: 1-24 hours
   - Static data: 7+ days

2. **Cache Key Uniqueness**: The cache automatically generates keys from function arguments
   - Different arguments = different cache entries
   - Same arguments = same cache entry

3. **Memory Management**: 
   - Use shorter TTLs for large objects
   - Periodically invalidate cache if memory is constrained
   - Consider Redis for production (better memory management)

4. **Error Handling**: Cache operations fail gracefully
   - Cache errors don't break your application
   - Function still executes even if caching fails

5. **Testing**: Use file-based cache in tests for simplicity
   ```python
   # In tests
   cache = CacheManager(backend="file", cache_dir="/tmp/test_cache")
   ```

## Troubleshooting

### Cache Not Working

1. Check cache directory permissions
2. Verify TTL is not too short
3. Check if function arguments are hashable

### High Memory Usage

1. Reduce TTL values
2. Implement periodic cache invalidation
3. Switch to Redis for better memory management

### Redis Connection Issues

```python
# The cache automatically falls back to file-based cache if Redis is unavailable
cache = CacheManager(backend="redis")  
# Will use file-based cache if Redis connection fails
```

## API Reference

### CacheManager

#### `__init__(backend: str = "file", cache_dir: str = "./cache")`

Initialize cache manager.

**Parameters:**
- `backend`: Cache backend ('file' or 'redis')
- `cache_dir`: Directory for file-based cache

#### `cached(ttl: int = 3600)`

Decorator for caching function results.

**Parameters:**
- `ttl`: Time-to-live in seconds

#### `get(key: str) -> Any`

Get value from cache.

**Returns:** Cached value or None if not found/expired

#### `set(key: str, value: Any, ttl: int = 3600)`

Set value in cache.

#### `invalidate(pattern: str = "*")`

Invalidate cache entries matching pattern.

#### `get_stats() -> dict`

Get cache statistics.

**Returns:** Dict with hits, misses, hit_rate, total_requests

#### `clear_stats()`

Reset cache statistics.

## Performance Tips

1. **Use Redis for Production**: Better performance and memory management
2. **Tune TTL**: Longer TTL = better cache hit rate but less fresh data
3. **Monitor Hit Rate**: Aim for >70% hit rate for good cache efficiency
4. **Cache Warm-up**: Pre-populate cache for frequently accessed data

## See Also

- [OptimizedOpenAIProvider](./OPTIMIZED_OPENAI_GUIDE.md) - Uses caching internally
- [Core Interfaces](../core/interfaces/) - Interface definitions
- [Architecture Guide](../docs/ARCHITECTURE.md) - Overall system architecture
