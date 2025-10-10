# Performance: Caching & Optimization Layer

**Group:** group_1  
**Priority:** P1 (High)  
**Status:** 📋 Not Started  
**Estimated Effort:** 5-7 hours  

## Description

Implement caching layer for expensive operations (LLM calls, image generation) to reduce costs and improve performance. Use Redis or file-based caching with TTL and cache invalidation.

## Acceptance Criteria

- [ ] Cache decorator for functions
- [ ] Redis or file-based cache backend
- [ ] TTL (time-to-live) configuration
- [ ] Cache hit/miss metrics
- [ ] Cache invalidation strategies
- [ ] Memory-efficient storage
- [ ] Unit tests for caching logic

## Dependencies

- Install: `redis>=5.0.0` or use file-based cache
- Can work in parallel with other Group 1 tasks

## Implementation Notes

Create `core/cache.py`:

```python
import redis
import json
import hashlib
from functools import wraps
from typing import Any, Callable
from pathlib import Path

class CacheManager:
    def __init__(self, backend: str = "redis"):
        if backend == "redis":
            self.cache = redis.Redis(host='localhost', port=6379, db=0)
        else:
            self.cache_dir = Path("./cache")
            self.cache_dir.mkdir(exist_ok=True)
    
    def _generate_key(self, func_name: str, args: tuple, kwargs: dict) -> str:
        """Generate cache key from function call"""
        key_data = {
            'func': func_name,
            'args': str(args),
            'kwargs': str(sorted(kwargs.items()))
        }
        key_str = json.dumps(key_data, sort_keys=True)
        return hashlib.md5(key_str.encode()).hexdigest()
    
    def cached(self, ttl: int = 3600):
        """Decorator for caching function results"""
        def decorator(func: Callable) -> Callable:
            @wraps(func)
            def wrapper(*args, **kwargs):
                cache_key = self._generate_key(func.__name__, args, kwargs)
                
                # Try to get from cache
                cached_result = self.get(cache_key)
                if cached_result is not None:
                    return cached_result
                
                # Call function and cache result
                result = func(*args, **kwargs)
                self.set(cache_key, result, ttl)
                
                return result
            return wrapper
        return decorator
    
    def get(self, key: str) -> Any:
        """Get value from cache"""
        try:
            if isinstance(self.cache, redis.Redis):
                value = self.cache.get(key)
                return json.loads(value) if value else None
            else:
                cache_file = self.cache_dir / f"{key}.json"
                if cache_file.exists():
                    with open(cache_file) as f:
                        return json.load(f)
        except Exception:
            return None
    
    def set(self, key: str, value: Any, ttl: int = 3600):
        """Set value in cache"""
        try:
            if isinstance(self.cache, redis.Redis):
                self.cache.setex(key, ttl, json.dumps(value))
            else:
                cache_file = self.cache_dir / f"{key}.json"
                with open(cache_file, 'w') as f:
                    json.dump(value, f)
        except Exception:
            pass  # Fail silently for cache errors
    
    def invalidate(self, pattern: str = "*"):
        """Invalidate cache entries matching pattern"""
        if isinstance(self.cache, redis.Redis):
            keys = self.cache.keys(pattern)
            if keys:
                self.cache.delete(*keys)
    
    def get_stats(self) -> dict:
        """Get cache statistics"""
        # Return hit rate, size, etc.
        pass

# Global cache instance
cache = CacheManager()

# Usage example:
@cache.cached(ttl=7200)
def expensive_llm_call(prompt: str) -> str:
    # Expensive operation that should be cached
    return llm.generate(prompt)
```

## Links

- Related: [HYBRID_ROADMAP.md](../../../docs/roadmaps/HYBRID_ROADMAP.md)
- Related: P2 features in [p2-medium/features-caching](../../../p2-medium/features-caching/)
