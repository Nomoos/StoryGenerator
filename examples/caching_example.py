"""
Example: Using the caching module.

This example demonstrates the caching functionality:
- File-based caching
- Cache decorator usage
- Cache statistics
- Manual cache operations
"""

import time
from core.cache import CacheManager, get_cache


def example_basic_caching():
    """Basic caching with decorator."""
    print("=" * 60)
    print("Example 1: Basic Caching")
    print("=" * 60)
    
    # Create cache manager
    cache = CacheManager(backend="file", cache_dir="./cache/examples")
    
    # Define an expensive function
    @cache.cached(ttl=3600)  # Cache for 1 hour
    def expensive_computation(x: int) -> int:
        """Simulate expensive computation."""
        print(f"  Computing result for {x}...")
        time.sleep(0.5)  # Simulate delay
        return x * x
    
    # First call - executes function
    print("\nFirst call with x=5:")
    result1 = expensive_computation(5)
    print(f"Result: {result1}")
    
    # Second call - uses cache
    print("\nSecond call with x=5:")
    result2 = expensive_computation(5)
    print(f"Result: {result2}")
    
    # Different input - executes function again
    print("\nCall with different input x=10:")
    result3 = expensive_computation(10)
    print(f"Result: {result3}")
    print()


def example_cache_statistics():
    """Demonstrate cache statistics tracking."""
    print("=" * 60)
    print("Example 2: Cache Statistics")
    print("=" * 60)
    
    cache = CacheManager(backend="file", cache_dir="./cache/examples")
    cache.clear_stats()  # Reset stats
    
    @cache.cached(ttl=3600)
    def process_data(data_id: int) -> dict:
        return {"id": data_id, "processed": True}
    
    # Make some calls
    print("\nMaking requests...")
    process_data(1)  # Miss
    process_data(1)  # Hit
    process_data(2)  # Miss
    process_data(1)  # Hit
    process_data(3)  # Miss
    
    # Get statistics
    stats = cache.get_stats()
    
    print("\nCache Statistics:")
    print(f"  Total requests: {stats['total_requests']}")
    print(f"  Hits: {stats['hits']}")
    print(f"  Misses: {stats['misses']}")
    print(f"  Hit rate: {stats['hit_rate']:.2%}")
    print(f"  Errors: {stats['errors']}")
    print()


def example_manual_operations():
    """Demonstrate manual cache operations."""
    print("=" * 60)
    print("Example 3: Manual Cache Operations")
    print("=" * 60)
    
    cache = CacheManager(backend="file", cache_dir="./cache/examples")
    
    # Manually set a value
    print("\nSetting value manually...")
    cache.set("user_123", {"name": "Alice", "role": "admin"}, ttl=60)
    print("✓ Value set")
    
    # Manually get a value
    print("\nGetting value...")
    value = cache.get("user_123")
    if value:
        print(f"✓ Found in cache: {value}")
    else:
        print("✗ Not found in cache")
    
    # Try to get non-existent key
    print("\nTrying to get non-existent key...")
    value = cache.get("user_999")
    if value:
        print(f"Found: {value}")
    else:
        print("✓ Not found (as expected)")
    
    print()


def example_cache_expiration():
    """Demonstrate cache expiration."""
    print("=" * 60)
    print("Example 4: Cache Expiration")
    print("=" * 60)
    
    cache = CacheManager(backend="file", cache_dir="./cache/examples")
    
    # Set with short TTL
    print("\nSetting value with 2 second TTL...")
    cache.set("temp_data", "This will expire soon", ttl=2)
    
    # Immediately retrieve
    print("Retrieving immediately...")
    value = cache.get("temp_data")
    print(f"✓ Found: {value}")
    
    # Wait for expiration
    print("\nWaiting 3 seconds for expiration...")
    time.sleep(3)
    
    print("Trying to retrieve after expiration...")
    value = cache.get("temp_data")
    if value:
        print(f"Found: {value}")
    else:
        print("✓ Not found (expired as expected)")
    
    print()


def example_cache_invalidation():
    """Demonstrate cache invalidation."""
    print("=" * 60)
    print("Example 5: Cache Invalidation")
    print("=" * 60)
    
    cache = CacheManager(backend="file", cache_dir="./cache/examples")
    
    # Set multiple values
    print("\nSetting multiple cache entries...")
    cache.set("key1", "value1")
    cache.set("key2", "value2")
    cache.set("key3", "value3")
    print("✓ 3 entries set")
    
    # Verify they exist
    print("\nVerifying entries exist...")
    assert cache.get("key1") == "value1"
    assert cache.get("key2") == "value2"
    assert cache.get("key3") == "value3"
    print("✓ All entries found")
    
    # Invalidate all
    print("\nInvalidating all cache entries...")
    cache.invalidate()
    print("✓ Cache cleared")
    
    # Verify they're gone
    print("\nVerifying entries are gone...")
    assert cache.get("key1") is None
    assert cache.get("key2") is None
    assert cache.get("key3") is None
    print("✓ All entries removed")
    print()


def example_complex_data():
    """Demonstrate caching complex data structures."""
    print("=" * 60)
    print("Example 6: Caching Complex Data")
    print("=" * 60)
    
    cache = CacheManager(backend="file", cache_dir="./cache/examples")
    
    # Cache complex data
    complex_data = {
        "user": {
            "id": 123,
            "name": "Alice",
            "preferences": {
                "theme": "dark",
                "language": "en"
            }
        },
        "posts": [
            {"id": 1, "title": "First Post"},
            {"id": 2, "title": "Second Post"}
        ],
        "metadata": {
            "created": "2024-01-01",
            "version": "1.0"
        }
    }
    
    print("\nCaching complex nested data structure...")
    cache.set("user_data_123", complex_data)
    print("✓ Complex data cached")
    
    # Retrieve and verify
    print("\nRetrieving from cache...")
    retrieved = cache.get("user_data_123")
    
    if retrieved:
        print("✓ Data retrieved successfully")
        print(f"  User name: {retrieved['user']['name']}")
        print(f"  Number of posts: {len(retrieved['posts'])}")
        print(f"  Theme preference: {retrieved['user']['preferences']['theme']}")
    else:
        print("✗ Failed to retrieve data")
    
    print()


def example_decorator_with_args():
    """Demonstrate caching with different function arguments."""
    print("=" * 60)
    print("Example 7: Caching with Different Arguments")
    print("=" * 60)
    
    cache = CacheManager(backend="file", cache_dir="./cache/examples")
    
    call_count = {}
    
    @cache.cached(ttl=3600)
    def fetch_user(user_id: int, include_posts: bool = False) -> dict:
        """Fetch user data (simulated)."""
        key = (user_id, include_posts)
        call_count[key] = call_count.get(key, 0) + 1
        
        print(f"  Fetching user {user_id} (include_posts={include_posts})...")
        return {
            "id": user_id,
            "name": f"User {user_id}",
            "posts": ["post1", "post2"] if include_posts else []
        }
    
    print("\nMaking various calls:")
    
    # Different combinations should create different cache entries
    print("\n1. fetch_user(1)")
    fetch_user(1)
    
    print("\n2. fetch_user(1) - should use cache")
    fetch_user(1)
    
    print("\n3. fetch_user(1, include_posts=True) - different args, new cache entry")
    fetch_user(1, include_posts=True)
    
    print("\n4. fetch_user(2) - different user, new cache entry")
    fetch_user(2)
    
    # Check call counts
    print("\nFunction call counts:")
    for key, count in call_count.items():
        user_id, include_posts = key
        print(f"  user_id={user_id}, include_posts={include_posts}: {count} calls")
    
    print("\nTotal unique cache entries:", len(call_count))
    print()


def example_singleton_cache():
    """Demonstrate using the singleton cache instance."""
    print("=" * 60)
    print("Example 8: Singleton Cache Instance")
    print("=" * 60)
    
    # Get the global cache instance
    cache = get_cache(backend="file", cache_dir="./cache/examples")
    
    @cache.cached(ttl=3600)
    def expensive_api_call(endpoint: str) -> dict:
        print(f"  Making API call to {endpoint}...")
        return {"endpoint": endpoint, "data": "result"}
    
    print("\nUsing global cache instance:")
    result1 = expensive_api_call("/api/users")
    result2 = expensive_api_call("/api/users")  # From cache
    
    print(f"\nFirst call made actual request")
    print(f"Second call used cache")
    print(f"Results are identical: {result1 == result2}")
    print()


def main():
    """Run all examples."""
    print("\n" + "=" * 60)
    print("Caching Module Examples")
    print("=" * 60)
    print()
    
    try:
        example_basic_caching()
        example_cache_statistics()
        example_manual_operations()
        example_cache_expiration()
        example_cache_invalidation()
        example_complex_data()
        example_decorator_with_args()
        example_singleton_cache()
        
        print("=" * 60)
        print("All examples completed successfully!")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
