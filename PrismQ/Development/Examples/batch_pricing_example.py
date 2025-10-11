"""
Example: Using Batch API Pricing and Video Cost Estimation

This example demonstrates:
- How to use batch API pricing (50% discount)
- Comparing costs between standard and batch pricing tiers
- Estimating cost per video based on token usage
- Calculating savings for bulk video production

Note: This example requires network access for tiktoken initialization.
If OPENAI_API_KEY is not set, it uses a dummy key for cost calculations only.
"""

import os
import sys

# Add parent directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from PrismQ.Providers.openai_optimized import PRICING


def calculate_cost(input_tokens, output_tokens, model, pricing_tier):
    """Calculate cost without initializing provider."""
    model_pricing = PRICING.get(model, PRICING["gpt-4o-mini"])
    tier_pricing = model_pricing.get(pricing_tier, model_pricing["standard"])
    
    input_cost = (input_tokens / 1_000_000) * tier_pricing["input"]
    output_cost = (output_tokens / 1_000_000) * tier_pricing["output"]
    return input_cost + output_cost


def example_batch_pricing():
    """Demonstrate batch API pricing."""
    print("=" * 60)
    print("Example 1: Batch API Pricing")
    print("=" * 60)
    
    # Example token counts for a typical request
    input_tokens = 1000
    output_tokens = 500
    model = "gpt-4o-mini"
    
    # Calculate costs for both tiers
    standard_cost = calculate_cost(input_tokens, output_tokens, model, "standard")
    batch_cost = calculate_cost(input_tokens, output_tokens, model, "batch")
    savings = standard_cost - batch_cost
    savings_percent = (savings / standard_cost * 100) if standard_cost > 0 else 0
    
    print(f"\nToken Usage:")
    print(f"  Input tokens: {input_tokens:,}")
    print(f"  Output tokens: {output_tokens:,}")
    print(f"\nPricing Comparison:")
    print(f"  Standard API cost: ${standard_cost:.6f}")
    print(f"  Batch API cost:    ${batch_cost:.6f}")
    print(f"  Savings:           ${savings:.6f} ({savings_percent:.1f}%)")
    print()


def example_video_cost_estimation():
    """Demonstrate video cost estimation."""
    print("=" * 60)
    print("Example 2: Video Cost Estimation")
    print("=" * 60)
    
    # Typical token usage per video generation request
    # Based on story generation pipeline:
    # - Script generation: ~500 input, ~2000 output tokens
    # - Script revision: ~2500 input, ~2000 output tokens  
    # - Title generation: ~200 input, ~50 output tokens
    # Average: ~1067 input, ~1350 output tokens per request
    
    avg_input = 1067
    avg_output = 1350
    requests_per_video = 3
    model = "gpt-4o-mini"
    
    # Calculate costs per request
    batch_cost_per_request = calculate_cost(avg_input, avg_output, model, "batch")
    standard_cost_per_request = calculate_cost(avg_input, avg_output, model, "standard")
    
    # Calculate costs per video
    batch_cost_per_video = batch_cost_per_request * requests_per_video
    standard_cost_per_video = standard_cost_per_request * requests_per_video
    
    # Calculate total tokens
    total_tokens_per_video = (avg_input + avg_output) * requests_per_video
    
    print(f"\nVideo Generation Parameters:")
    print(f"  Average input tokens per request: {avg_input:,}")
    print(f"  Average output tokens per request: {avg_output:,}")
    print(f"  API requests per video: {requests_per_video}")
    
    print(f"\nBatch API Pricing:")
    print(f"  Cost per request: ${batch_cost_per_request:.6f}")
    print(f"  Cost per video:   ${batch_cost_per_video:.6f}")
    print(f"  Total tokens:     {total_tokens_per_video:,}")
    
    print(f"\nStandard API Pricing:")
    print(f"  Cost per request: ${standard_cost_per_request:.6f}")
    print(f"  Cost per video:   ${standard_cost_per_video:.6f}")
    print(f"  Total tokens:     {total_tokens_per_video:,}")
    
    savings_per_video = standard_cost_per_video - batch_cost_per_video
    savings_percent = (savings_per_video / standard_cost_per_video * 100)
    
    print(f"\nSavings per video: ${savings_per_video:.6f} ({savings_percent:.1f}%)")
    print()


def example_bulk_production_comparison():
    """Compare costs for bulk video production."""
    print("=" * 60)
    print("Example 3: Bulk Video Production Cost Analysis")
    print("=" * 60)
    
    model = "gpt-4o-mini"
    
    # Video production parameters
    avg_input = 1067
    avg_output = 1350
    requests_per_video = 3
    
    # Calculate cost per video for both tiers
    batch_cost_per_video = calculate_cost(avg_input, avg_output, model, "batch") * requests_per_video
    standard_cost_per_video = calculate_cost(avg_input, avg_output, model, "standard") * requests_per_video
    
    # Calculate costs for different video quantities
    video_counts = [10, 50, 100, 500, 1000]
    
    print("\nCost Analysis for Different Production Scales:")
    print("-" * 60)
    print(f"{'Videos':<10} {'Standard API':<15} {'Batch API':<15} {'Savings':<15}")
    print("-" * 60)
    
    for count in video_counts:
        batch_total = batch_cost_per_video * count
        standard_total = standard_cost_per_video * count
        savings = standard_total - batch_total
        
        print(f"{count:<10} ${standard_total:<14.2f} ${batch_total:<14.2f} ${savings:<14.2f}")
    
    print()


def example_model_comparison():
    """Compare costs across different models."""
    print("=" * 60)
    print("Example 4: Model Cost Comparison")
    print("=" * 60)
    
    models = ["gpt-4o-mini", "gpt-4o", "gpt-3.5-turbo"]
    
    # Typical token usage
    avg_input = 1067
    avg_output = 1350
    requests_per_video = 3
    
    print("\nCost per Video by Model (Batch API Pricing):")
    print("-" * 60)
    print(f"{'Model':<20} {'Per Request':<15} {'Per Video':<15}")
    print("-" * 60)
    
    for model in models:
        cost_per_request = calculate_cost(avg_input, avg_output, model, "batch")
        cost_per_video = cost_per_request * requests_per_video
        
        print(f"{model:<20} ${cost_per_request:<14.6f} ${cost_per_video:<14.6f}")
    
    print("\nRecommendation: Use gpt-4o-mini with batch pricing for optimal cost efficiency.")
    print()


def main():
    """Run all examples."""
    print("\n" + "=" * 60)
    print("Batch API Pricing & Video Cost Estimation Examples")
    print("=" * 60)
    print("\nNote: These examples demonstrate cost calculations")
    print("using OpenAI's batch API pricing (50% discount).")
    print()
    
    try:
        example_batch_pricing()
        example_video_cost_estimation()
        example_bulk_production_comparison()
        example_model_comparison()
        
        print("=" * 60)
        print("Key Takeaways:")
        print("=" * 60)
        print("1. Batch API offers 50% cost savings over standard API")
        print("2. For gpt-4o-mini, typical video costs ~$0.006 (batch) vs ~$0.012 (standard)")
        print("3. For 1000 videos, batch API saves ~$6.00 compared to standard API")
        print("4. Use batch pricing for bulk operations when real-time response isn't needed")
        print()
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
