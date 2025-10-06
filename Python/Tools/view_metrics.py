#!/usr/bin/env python3
"""
View performance metrics and statistics from the StoryGenerator.
"""

import json
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Tools.Monitor import get_performance_summary, METRICS_FILE

def main():
    """Display performance summary."""
    print("\n" + "=" * 70)
    print("📊 StoryGenerator Performance Summary")
    print("=" * 70 + "\n")
    
    summary = get_performance_summary()
    
    if "message" in summary:
        print(f"⚠️  {summary['message']}")
        return
    
    print(f"Total Operations: {summary['total_operations']}")
    print(f"Successful: {summary['successful']} ✅")
    print(f"Failed: {summary['failed']} ❌")
    print(f"Success Rate: {summary['success_rate']}%\n")
    
    print("-" * 70)
    print("📈 Performance by Operation Type:")
    print("-" * 70)
    
    for op_type, stats in summary['by_operation'].items():
        print(f"\n{op_type}:")
        print(f"  Count: {stats['count']}")
        print(f"  Failures: {stats['failures']}")
        print(f"  Avg Time: {stats['avg_time']}s")
        success_rate = ((stats['count'] - stats['failures']) / stats['count'] * 100) if stats['count'] > 0 else 0
        print(f"  Success Rate: {success_rate:.1f}%")
    
    print("\n" + "=" * 70)
    print(f"📁 Full metrics available at: {METRICS_FILE}")
    print("=" * 70 + "\n")

if __name__ == "__main__":
    main()
