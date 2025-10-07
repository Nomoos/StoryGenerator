#!/usr/bin/env python3
"""
Example script demonstrating the monitoring, retry, and validation features.
This can be run without API keys to test the monitoring infrastructure.
"""

import os
import sys
import time

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Tools.Monitor import (
    PerformanceMonitor, 
    log_info, 
    log_warning, 
    log_error, 
    time_operation,
    get_performance_summary
)
from Tools.Retry import retry_with_exponential_backoff
from Tools.Validator import OutputValidator

# Example 1: Manual performance logging
def example_manual_logging():
    print("\n" + "="*60)
    print("Example 1: Manual Performance Logging")
    print("="*60)
    
    start = time.time()
    log_info("Starting example operation...")
    
    # Simulate some work
    time.sleep(0.5)
    
    duration = time.time() - start
    
    PerformanceMonitor.log_operation(
        operation="Example_Operation",
        story_title="Test Story",
        duration=duration,
        success=True,
        metrics={
            "items_processed": 10,
            "cache_hits": 7
        }
    )
    
    print("✅ Operation logged successfully")

# Example 2: Using the decorator
@time_operation("Decorated_Operation")
def example_decorated_function(story_title: str):
    print("\n" + "="*60)
    print("Example 2: Using @time_operation Decorator")
    print("="*60)
    
    log_info(f"Processing story: {story_title}")
    time.sleep(0.3)
    return {"status": "success"}

# Example 3: Retry logic demonstration
@retry_with_exponential_backoff(max_retries=3, base_delay=0.5)
def example_flaky_operation(attempt_counter):
    print("\n" + "="*60)
    print("Example 3: Retry Logic with Exponential Backoff")
    print("="*60)
    
    attempt_counter['count'] += 1
    print(f"Attempt {attempt_counter['count']}")
    
    # Fail on first two attempts, succeed on third
    if attempt_counter['count'] < 3:
        raise Exception("Simulated failure")
    
    print("✅ Operation succeeded after retries")
    return "success"

# Example 4: Validation demonstrations
def example_validation():
    print("\n" + "="*60)
    print("Example 4: Output Validation")
    print("="*60)
    
    # Test text validation with this script itself
    script_path = __file__
    is_valid, metrics = OutputValidator.validate_text_file(script_path, min_length=100)
    
    print(f"\nValidating this script file:")
    print(f"  Valid: {is_valid}")
    print(f"  Size: {metrics['size_bytes']} bytes")
    print(f"  Words: {metrics['word_count']}")
    print(f"  Lines: {metrics['line_count']}")
    
    # Test with non-existent file
    is_valid, metrics = OutputValidator.validate_text_file("nonexistent.txt")
    print(f"\nValidating non-existent file:")
    print(f"  Valid: {is_valid}")
    print(f"  Exists: {metrics['exists']}")

# Example 5: Error logging
def example_error_logging():
    print("\n" + "="*60)
    print("Example 5: Error Logging")
    print("="*60)
    
    try:
        # Simulate an error
        raise ValueError("This is a simulated error for demonstration")
    except Exception as e:
        log_error("Demo_Operation", "Test Story", e)
        print("✅ Error logged successfully")

# Example 6: View metrics summary
def example_view_summary():
    print("\n" + "="*60)
    print("Example 6: Performance Summary")
    print("="*60 + "\n")
    
    summary = get_performance_summary()
    
    if "message" in summary:
        print(f"⚠️  {summary['message']}")
        return
    
    print(f"Total Operations: {summary['total_operations']}")
    print(f"Successful: {summary['successful']}")
    print(f"Failed: {summary['failed']}")
    print(f"Success Rate: {summary['success_rate']}%")
    
    if summary['by_operation']:
        print("\nBy Operation Type:")
        for op_type, stats in summary['by_operation'].items():
            print(f"  {op_type}: {stats['count']} operations, avg {stats['avg_time']}s")

def main():
    print("\n" + "="*60)
    print("🎬 StoryGenerator Monitoring Features Demo")
    print("="*60)
    
    # Run all examples
    example_manual_logging()
    
    result = example_decorated_function("Demo Story")
    
    try:
        example_flaky_operation({'count': 0})
    except Exception as e:
        print(f"Note: If this fails, it's expected (demonstrating retries)")
    
    example_validation()
    
    example_error_logging()
    
    # Small delay to ensure all async operations complete
    time.sleep(0.5)
    
    example_view_summary()
    
    print("\n" + "="*60)
    print("✅ Demo Complete!")
    print("="*60)
    print("\nCheck the logs/ directory for generated log files:")
    print("  - storygen_YYYYMMDD.log (daily logs)")
    print("  - metrics.json (structured metrics)")
    print("\nRun 'python Tools/view_metrics.py' for detailed statistics")
    print("="*60 + "\n")

if __name__ == "__main__":
    main()
