# Batch API Pricing Example

This example demonstrates OpenAI's Batch API pricing (50% discount) and how to calculate video generation costs.

## Features

1. **Batch API Pricing Comparison** - Compare standard vs batch pricing
2. **Video Cost Estimation** - Calculate per-video costs based on token usage
3. **Bulk Production Analysis** - Analyze costs at different production scales
4. **Model Comparison** - Compare costs across different GPT models

## Running the Example

```bash
python examples/batch_pricing_example.py
```

No API key is required - this example only performs cost calculations without making actual API calls.

## Key Findings

### Cost Per Video (gpt-4o-mini)

Based on typical story generation pipeline:
- Average: ~1,067 input tokens per request
- Average: ~1,350 output tokens per request  
- Requests per video: 3 (script generation, revision, titles)

| Pricing Tier | Cost per Video | Cost for 1000 Videos |
|--------------|----------------|---------------------|
| Standard API | $0.00291       | $2.91               |
| Batch API    | $0.00146       | $1.46               |
| **Savings**  | **$0.00146 (50%)** | **$1.46 (50%)** |

### Model Comparison (Batch Pricing)

| Model | Cost per Video | Notes |
|-------|----------------|-------|
| gpt-4o-mini | $0.00146 | Best value for most use cases |
| gpt-3.5-turbo | $0.00384 | Good balance of cost and quality |
| gpt-4o | $0.02425 | Premium quality, higher cost |

## When to Use Batch API

The Batch API is ideal for:
- **Bulk video generation** where real-time responses aren't needed
- **Overnight processing** of large batches
- **Cost-sensitive operations** that can tolerate asynchronous processing
- **High-volume production** (100+ videos)

## Integration

To use batch pricing in your code:

```python
from PrismQ.Providers import OptimizedOpenAIProvider

# Initialize with batch pricing
provider = OptimizedOpenAIProvider(
    model="gpt-4o-mini",
    pricing_tier="batch"  # 50% discount
)

# All cost estimates will use batch pricing
stats = provider.get_usage_stats()
print(f"Total cost: ${stats['total_cost']:.4f}")
```

## See Also

- [OPTIMIZED_OPENAI_GUIDE.md](../PrismQ/Providers/OPTIMIZED_OPENAI_GUIDE.md) - Full documentation
- [OpenAI Batch API Documentation](https://platform.openai.com/docs/guides/batch)
- [OpenAI Pricing](https://openai.com/api/pricing/)
