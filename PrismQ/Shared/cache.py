"""
Caching layer for expensive operations.

This module provides caching functionality for expensive operations like LLM calls
and image generation to reduce costs and improve performance. Supports both Redis
and file-based caching with TTL and cache invalidation.
"""

import hashlib
import json
import logging
import time
from functools import wraps
from pathlib import Path
from typing import Any, Callable, Optional

logger = logging.getLogger(__name__)


class CacheManager:
    """
    Cache manager for storing and retrieving expensive operation results.
    
    Supports both Redis and file-based backends. Falls back to file-based
    caching if Redis is not available.
    
    Example:
        >>> cache = CacheManager(backend="file")
        >>> 
        >>> @cache.cached(ttl=3600)
        >>> def expensive_operation(param: str) -> str:
        ...     return f"Result for {param}"
    """

    def __init__(self, backend: str = "file", cache_dir: str = "./cache"):
        """
        Initialize cache manager.
        
        Args:
            backend: Cache backend ('redis' or 'file', default: 'file')
            cache_dir: Directory for file-based cache (default: './cache')
        """
        self.backend = backend
        self.cache_dir = Path(cache_dir)
        self._redis_client = None
        self._stats = {
            "hits": 0,
            "misses": 0,
            "errors": 0,
        }
        
        if backend == "redis":
            try:
                import redis
                self._redis_client = redis.Redis(
                    host='localhost',
                    port=6379,
                    db=0,
                    decode_responses=True
                )
                # Test connection
                self._redis_client.ping()
                logger.info("Initialized Redis cache backend")
            except Exception as e:
                logger.warning(
                    f"Failed to connect to Redis: {e}. Falling back to file-based cache."
                )
                self.backend = "file"
                self._redis_client = None
        
        if self.backend == "file":
            self.cache_dir.mkdir(parents=True, exist_ok=True)
            logger.info(f"Initialized file-based cache at {self.cache_dir}")

    def _generate_key(self, func_name: str, args: tuple, kwargs: dict) -> str:
        """
        Generate cache key from function call.
        
        Args:
            func_name: Name of the function
            args: Positional arguments
            kwargs: Keyword arguments
            
        Returns:
            MD5 hash of the function call parameters
        """
        # Convert args and kwargs to a stable string representation
        key_data = {
            'func': func_name,
            'args': str(args),
            'kwargs': str(sorted(kwargs.items()))
        }
        key_str = json.dumps(key_data, sort_keys=True)
        return hashlib.md5(key_str.encode()).hexdigest()

    def cached(self, ttl: int = 3600):
        """
        Decorator for caching function results.
        
        Args:
            ttl: Time-to-live in seconds (default: 3600)
            
        Returns:
            Decorator function
            
        Example:
            >>> @cache.cached(ttl=7200)
            >>> def expensive_llm_call(prompt: str) -> str:
            ...     return llm.generate(prompt)
        """
        def decorator(func: Callable) -> Callable:
            @wraps(func)
            def wrapper(*args, **kwargs):
                cache_key = self._generate_key(func.__name__, args, kwargs)
                
                # Try to get from cache
                cached_result = self.get(cache_key)
                if cached_result is not None:
                    logger.debug(f"Cache hit for {func.__name__}")
                    self._stats["hits"] += 1
                    return cached_result
                
                # Cache miss - call function
                logger.debug(f"Cache miss for {func.__name__}")
                self._stats["misses"] += 1
                result = func(*args, **kwargs)
                
                # Store in cache
                self.set(cache_key, result, ttl)
                
                return result
            return wrapper
        return decorator

    def get(self, key: str) -> Any:
        """
        Get value from cache.
        
        Args:
            key: Cache key
            
        Returns:
            Cached value or None if not found or expired
        """
        try:
            if self._redis_client:
                value = self._redis_client.get(key)
                if value:
                    return json.loads(value)
                return None
            else:
                cache_file = self.cache_dir / f"{key}.json"
                if cache_file.exists():
                    # Check if file has expired
                    metadata_file = self.cache_dir / f"{key}.meta"
                    if metadata_file.exists():
                        with open(metadata_file, 'r') as f:
                            metadata = json.load(f)
                            if time.time() > metadata.get('expires_at', 0):
                                # Expired - remove files
                                cache_file.unlink()
                                metadata_file.unlink()
                                return None
                    
                    with open(cache_file, 'r') as f:
                        return json.load(f)
                return None
        except Exception as e:
            logger.error(f"Error reading from cache: {e}")
            self._stats["errors"] += 1
            return None

    def set(self, key: str, value: Any, ttl: int = 3600):
        """
        Set value in cache.
        
        Args:
            key: Cache key
            value: Value to cache (must be JSON serializable)
            ttl: Time-to-live in seconds
        """
        try:
            if self._redis_client:
                self._redis_client.setex(
                    key,
                    ttl,
                    json.dumps(value)
                )
            else:
                cache_file = self.cache_dir / f"{key}.json"
                with open(cache_file, 'w') as f:
                    json.dump(value, f)
                
                # Store metadata with expiration time
                metadata_file = self.cache_dir / f"{key}.meta"
                with open(metadata_file, 'w') as f:
                    json.dump({
                        'expires_at': time.time() + ttl,
                        'created_at': time.time()
                    }, f)
        except Exception as e:
            logger.warning(f"Error writing to cache: {e}")
            self._stats["errors"] += 1
            # Fail silently for cache errors

    def invalidate(self, pattern: str = "*"):
        """
        Invalidate cache entries matching pattern.
        
        Args:
            pattern: Pattern to match cache keys (default: '*' for all)
        """
        try:
            if self._redis_client:
                keys = self._redis_client.keys(pattern)
                if keys:
                    self._redis_client.delete(*keys)
                    logger.info(f"Invalidated {len(keys)} cache entries")
            else:
                # For file-based cache, delete all .json files
                count = 0
                for cache_file in self.cache_dir.glob("*.json"):
                    cache_file.unlink()
                    count += 1
                    # Also remove metadata file
                    meta_file = cache_file.with_suffix('.meta')
                    if meta_file.exists():
                        meta_file.unlink()
                logger.info(f"Invalidated {count} cache entries")
        except Exception as e:
            logger.error(f"Error invalidating cache: {e}")
            self._stats["errors"] += 1

    def get_stats(self) -> dict:
        """
        Get cache statistics.
        
        Returns:
            Dictionary with cache statistics (hits, misses, errors, hit_rate)
        """
        total = self._stats["hits"] + self._stats["misses"]
        hit_rate = self._stats["hits"] / total if total > 0 else 0.0
        
        return {
            "hits": self._stats["hits"],
            "misses": self._stats["misses"],
            "errors": self._stats["errors"],
            "hit_rate": hit_rate,
            "total_requests": total,
        }

    def clear_stats(self):
        """Reset cache statistics."""
        self._stats = {
            "hits": 0,
            "misses": 0,
            "errors": 0,
        }


# Global cache instance - can be configured via environment
_default_cache: Optional[CacheManager] = None


def get_cache(backend: str = "file", cache_dir: str = "./cache") -> CacheManager:
    """
    Get or create the default cache instance.
    
    Args:
        backend: Cache backend ('redis' or 'file')
        cache_dir: Directory for file-based cache
        
    Returns:
        CacheManager instance
    """
    global _default_cache
    if _default_cache is None:
        _default_cache = CacheManager(backend=backend, cache_dir=cache_dir)
    return _default_cache
