"""
Tests for the caching module.
"""

import json
import time
from pathlib import Path

import pytest

from core.cache import CacheManager, get_cache


@pytest.fixture
def temp_cache_dir(tmp_path):
    """Create a temporary cache directory."""
    cache_dir = tmp_path / "test_cache"
    cache_dir.mkdir()
    return cache_dir


@pytest.fixture
def file_cache(temp_cache_dir):
    """Create a file-based cache manager."""
    return CacheManager(backend="file", cache_dir=str(temp_cache_dir))


def test_cache_initialization_file(file_cache):
    """Test cache initialization with file backend."""
    assert file_cache.backend == "file"
    assert file_cache.cache_dir.exists()
    assert file_cache._redis_client is None


def test_cache_set_and_get(file_cache):
    """Test setting and getting values from cache."""
    key = "test_key"
    value = {"data": "test_value", "number": 42}
    
    file_cache.set(key, value, ttl=3600)
    result = file_cache.get(key)
    
    assert result == value


def test_cache_miss(file_cache):
    """Test cache miss returns None."""
    result = file_cache.get("nonexistent_key")
    assert result is None


def test_cache_expiration(file_cache, temp_cache_dir):
    """Test that expired cache entries return None."""
    key = "expiring_key"
    value = "test_value"
    
    # Set with 1 second TTL
    file_cache.set(key, value, ttl=1)
    
    # Should be available immediately
    assert file_cache.get(key) == value
    
    # Wait for expiration
    time.sleep(1.5)
    
    # Should be expired
    assert file_cache.get(key) is None


def test_cache_decorator(file_cache):
    """Test cache decorator functionality."""
    call_count = 0
    
    @file_cache.cached(ttl=3600)
    def expensive_function(x: int) -> int:
        nonlocal call_count
        call_count += 1
        return x * 2
    
    # First call - should execute function
    result1 = expensive_function(5)
    assert result1 == 10
    assert call_count == 1
    
    # Second call with same argument - should use cache
    result2 = expensive_function(5)
    assert result2 == 10
    assert call_count == 1  # Function not called again
    
    # Different argument - should execute function again
    result3 = expensive_function(10)
    assert result3 == 20
    assert call_count == 2


def test_cache_invalidation(file_cache, temp_cache_dir):
    """Test cache invalidation."""
    # Set multiple cache entries
    file_cache.set("key1", "value1")
    file_cache.set("key2", "value2")
    file_cache.set("key3", "value3")
    
    # Verify they exist
    assert file_cache.get("key1") == "value1"
    assert file_cache.get("key2") == "value2"
    
    # Invalidate all
    file_cache.invalidate()
    
    # Verify they're gone
    assert file_cache.get("key1") is None
    assert file_cache.get("key2") is None
    assert file_cache.get("key3") is None


def test_cache_stats(file_cache):
    """Test cache statistics tracking."""
    @file_cache.cached(ttl=3600)
    def test_func(x: int) -> int:
        return x * 2
    
    # Reset stats
    file_cache.clear_stats()
    
    # First call - cache miss
    test_func(5)
    stats = file_cache.get_stats()
    assert stats["misses"] == 1
    assert stats["hits"] == 0
    
    # Second call with same arg - cache hit
    test_func(5)
    stats = file_cache.get_stats()
    assert stats["misses"] == 1
    assert stats["hits"] == 1
    
    # Check hit rate
    assert stats["hit_rate"] == 0.5


def test_get_cache_singleton():
    """Test that get_cache returns a singleton."""
    cache1 = get_cache()
    cache2 = get_cache()
    
    assert cache1 is cache2


def test_cache_with_different_args(file_cache):
    """Test that cache distinguishes between different arguments."""
    @file_cache.cached(ttl=3600)
    def func(a: int, b: int) -> int:
        return a + b
    
    result1 = func(1, 2)
    result2 = func(2, 1)
    
    # These should be different results (not from cache)
    assert result1 == 3
    assert result2 == 3
    
    # Same arguments should use cache
    call_count = 0
    
    @file_cache.cached(ttl=3600)
    def func2(a: int, b: int) -> int:
        nonlocal call_count
        call_count += 1
        return a + b
    
    func2(5, 10)
    func2(5, 10)
    
    assert call_count == 1  # Only called once, second was cached


def test_cache_with_complex_types(file_cache):
    """Test caching with complex data types."""
    complex_value = {
        "list": [1, 2, 3],
        "nested": {"a": "b", "c": "d"},
        "string": "test",
        "number": 42
    }
    
    file_cache.set("complex_key", complex_value)
    result = file_cache.get("complex_key")
    
    assert result == complex_value
    assert isinstance(result, dict)
    assert result["list"] == [1, 2, 3]


def test_cache_error_handling(file_cache, temp_cache_dir):
    """Test that cache errors are handled gracefully."""
    # Try to get from invalid cache
    result = file_cache.get("key")
    assert result is None  # Should return None, not raise
    
    # Stats should track errors if any occur
    stats = file_cache.get_stats()
    assert "errors" in stats
