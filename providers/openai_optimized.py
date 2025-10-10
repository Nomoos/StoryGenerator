"""
Optimized OpenAI Provider with token counting, cost tracking, and caching.

This module extends the base OpenAI provider with advanced features:
- Token counting before API calls
- Cost tracking per operation
- Response caching for identical requests
- Usage monitoring and alerts
"""

import logging
import os
from typing import Optional

import tiktoken
from openai import OpenAI, AsyncOpenAI
from openai import OpenAIError, RateLimitError, APIError, APIConnectionError
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type,
)

from core.cache import CacheManager
from core.interfaces.llm_provider import ILLMProvider, IAsyncLLMProvider, ChatMessage

logger = logging.getLogger(__name__)


# Pricing per 1M tokens (as of October 2024) - can be moved to config
# Standard API pricing for real-time/synchronous requests
PRICING = {
    "gpt-4o-mini": {
        "standard": {"input": 0.15, "output": 0.60},
        "batch": {"input": 0.075, "output": 0.30},  # 50% discount
    },
    "gpt-4o": {
        "standard": {"input": 2.50, "output": 10.0},
        "batch": {"input": 1.25, "output": 5.0},  # 50% discount
    },
    "gpt-4-turbo": {
        "standard": {"input": 10.0, "output": 30.0},
        "batch": {"input": 5.0, "output": 15.0},  # 50% discount
    },
    "gpt-3.5-turbo": {
        "standard": {"input": 0.50, "output": 1.50},
        "batch": {"input": 0.25, "output": 0.75},  # 50% discount
    },
}


class OptimizedOpenAIProvider(ILLMProvider):
    """
    Optimized OpenAI provider with token counting and cost tracking.
    
    Features:
    - Automatic token counting using tiktoken
    - Cost tracking per operation and cumulative
    - Response caching for identical requests
    - Usage monitoring and statistics
    - Automatic retry with exponential backoff
    
    Example:
        >>> provider = OptimizedOpenAIProvider(model="gpt-4o-mini", enable_cache=True)
        >>> response = provider.generate_completion("Hello, world!")
        >>> print(f"Tokens used: {provider.get_usage_stats()['total_tokens']}")
        >>> print(f"Total cost: ${provider.get_usage_stats()['total_cost']:.4f}")
    """

    def __init__(
        self,
        api_key: str | None = None,
        model: str = "gpt-4o-mini",
        enable_cache: bool = True,
        cache_ttl: int = 3600,
        cache_backend: str = "file",
        pricing_tier: str = "standard",
    ):
        """
        Initialize optimized OpenAI provider.
        
        Args:
            api_key: OpenAI API key (defaults to OPENAI_API_KEY env var)
            model: Model to use for completions (default: gpt-4o-mini)
            enable_cache: Enable response caching (default: True)
            cache_ttl: Cache time-to-live in seconds (default: 3600)
            cache_backend: Cache backend ('redis' or 'file', default: 'file')
            pricing_tier: Pricing tier to use for cost calculation ('standard' or 'batch', default: 'standard')
            
        Raises:
            ValueError: If API key is not provided and not found in environment
        """
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError(
                "OpenAI API key is required. Set OPENAI_API_KEY environment variable "
                "or pass api_key parameter."
            )

        self.model = model
        
        # Validate and store pricing tier
        if pricing_tier not in ["standard", "batch"]:
            raise ValueError(
                f"Invalid pricing_tier '{pricing_tier}'. Must be 'standard' or 'batch'."
            )
        self.pricing_tier = pricing_tier
        
        self.client = OpenAI(api_key=self.api_key)
        
        # Initialize token encoder
        try:
            self.encoding = tiktoken.encoding_for_model(model)
        except KeyError:
            # Fallback to cl100k_base for newer models
            logger.warning(f"Model {model} not found in tiktoken, using cl100k_base encoding")
            self.encoding = tiktoken.get_encoding("cl100k_base")
        
        # Cache setup
        self.enable_cache = enable_cache
        self.cache_ttl = cache_ttl
        self.cache = None
        if enable_cache:
            self.cache = CacheManager(backend=cache_backend, cache_dir="./cache/openai")
        
        # Usage tracking
        self.total_input_tokens = 0
        self.total_output_tokens = 0
        self.total_cost = 0.0
        self.request_count = 0
        
        logger.info(
            f"Initialized OptimizedOpenAIProvider: model={model}, "
            f"pricing_tier={pricing_tier}, cache={enable_cache}, backend={cache_backend}"
        )

    @property
    def model_name(self) -> str:
        """Get the name of the model being used."""
        return self.model

    def count_tokens(self, text: str) -> int:
        """
        Count tokens in text.
        
        Args:
            text: Text to count tokens for
            
        Returns:
            Number of tokens
        """
        return len(self.encoding.encode(text))

    def count_messages_tokens(self, messages: list[ChatMessage]) -> int:
        """
        Count tokens in a list of messages.
        
        Args:
            messages: List of ChatMessage TypedDicts
            
        Returns:
            Approximate number of tokens (includes message formatting overhead)
        """
        # Each message has some overhead: role, formatting, etc.
        tokens_per_message = 3  # Approximate overhead per message
        tokens = 0
        
        for message in messages:
            tokens += tokens_per_message
            tokens += self.count_tokens(message.get("content", ""))
            if "name" in message:
                tokens += self.count_tokens(message["name"])
        
        tokens += 3  # Every reply is primed with assistant
        return tokens

    def estimate_cost(self, input_tokens: int, output_tokens: int, pricing_tier: str | None = None) -> float:
        """
        Estimate cost for a request.
        
        Args:
            input_tokens: Number of input tokens
            output_tokens: Number of output tokens
            pricing_tier: Pricing tier to use ('standard' or 'batch'). 
                         If None, uses the provider's default pricing tier.
            
        Returns:
            Estimated cost in USD
        """
        tier = pricing_tier or self.pricing_tier
        
        # Get model pricing with fallback to gpt-4o-mini
        model_pricing = PRICING.get(self.model, PRICING["gpt-4o-mini"])
        
        # Get tier pricing with fallback to standard
        tier_pricing = model_pricing.get(tier, model_pricing.get("standard", {"input": 0.15, "output": 0.60}))
        
        input_cost = (input_tokens / 1_000_000) * tier_pricing["input"]
        output_cost = (output_tokens / 1_000_000) * tier_pricing["output"]
        return input_cost + output_cost

    def _track_usage(self, input_tokens: int, output_tokens: int):
        """Track token usage and cost."""
        self.total_input_tokens += input_tokens
        self.total_output_tokens += output_tokens
        self.request_count += 1
        
        cost = self.estimate_cost(input_tokens, output_tokens)
        self.total_cost += cost
        
        logger.debug(
            f"Request #{self.request_count}: {input_tokens} input + {output_tokens} output tokens, "
            f"cost: ${cost:.6f}, total cost: ${self.total_cost:.6f}"
        )

    def generate_completion(
        self,
        prompt: str,
        temperature: float = 0.7,
        max_tokens: int | None = None,
        **kwargs,
    ) -> str:
        """
        Generate completion from a single prompt (implements ILLMProvider).
        
        Args:
            prompt: The prompt text
            temperature: Sampling temperature (0-2, default: 0.7)
            max_tokens: Maximum tokens in response (optional)
            **kwargs: Additional parameters to pass to the API
            
        Returns:
            Generated text content as string
        """
        messages: list[ChatMessage] = [{"role": "user", "content": prompt}]
        return self.generate_chat(messages, temperature, max_tokens, **kwargs)

    def generate_chat(
        self,
        messages: list[ChatMessage],
        temperature: float = 0.7,
        max_tokens: int | None = None,
        **kwargs,
    ) -> str:
        """
        Generate chat completion with caching and usage tracking (implements ILLMProvider).
        
        Args:
            messages: List of ChatMessage TypedDicts with role and content
            temperature: Sampling temperature (0-2, default: 0.7)
            max_tokens: Maximum tokens in response (optional)
            **kwargs: Additional parameters to pass to the API
            
        Returns:
            Generated text content as string
        """
        # Check cache first if enabled
        if self.enable_cache and self.cache:
            cache_key = f"{self.model}_{messages}_{temperature}_{max_tokens}"
            cached = self.cache.get(cache_key)
            if cached:
                logger.debug("Using cached response")
                return cached
        
        # Count input tokens
        input_tokens = self.count_messages_tokens(messages)
        logger.debug(f"Input tokens: {input_tokens}")
        
        # Make API call
        response_text = self._chat_completion_with_retry(
            messages, temperature, max_tokens, **kwargs
        )
        
        # Count output tokens
        output_tokens = self.count_tokens(response_text)
        
        # Track usage
        self._track_usage(input_tokens, output_tokens)
        
        # Cache response if enabled
        if self.enable_cache and self.cache:
            self.cache.set(cache_key, response_text, self.cache_ttl)
        
        return response_text

    @retry(
        retry=retry_if_exception_type((RateLimitError, APIConnectionError)),
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10),
    )
    def _chat_completion_with_retry(
        self,
        messages: list[ChatMessage],
        temperature: float = 0.7,
        max_tokens: int | None = None,
        **kwargs,
    ) -> str:
        """
        Make chat completion API call with automatic retry.
        
        Args:
            messages: List of ChatMessage TypedDicts
            temperature: Sampling temperature
            max_tokens: Maximum tokens in response
            **kwargs: Additional parameters
            
        Returns:
            Generated text content
        """
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
                **kwargs,
            )
            
            content = response.choices[0].message.content
            return content

        except RateLimitError as e:
            logger.warning(f"Rate limit hit: {e}. Retrying...")
            raise

        except APIConnectionError as e:
            logger.warning(f"API connection error: {e}. Retrying...")
            raise

        except APIError as e:
            logger.error(f"OpenAI API error: {e}")
            raise

        except OpenAIError as e:
            logger.error(f"OpenAI error: {e}")
            raise

        except Exception as e:
            logger.error(f"Unexpected error during OpenAI API call: {e}")
            raise

    def get_usage_stats(self) -> dict:
        """
        Get usage statistics.
        
        Returns:
            Dictionary with usage statistics including:
            - total_input_tokens
            - total_output_tokens
            - total_tokens
            - total_cost
            - request_count
            - average_tokens_per_request
            - pricing_tier
            - cache_stats (if caching enabled)
        """
        total_tokens = self.total_input_tokens + self.total_output_tokens
        avg_tokens = total_tokens / self.request_count if self.request_count > 0 else 0
        
        stats = {
            "total_input_tokens": self.total_input_tokens,
            "total_output_tokens": self.total_output_tokens,
            "total_tokens": total_tokens,
            "total_cost": round(self.total_cost, 6),
            "request_count": self.request_count,
            "average_tokens_per_request": round(avg_tokens, 2),
            "model": self.model,
            "pricing_tier": self.pricing_tier,
        }
        
        if self.enable_cache and self.cache:
            stats["cache_stats"] = self.cache.get_stats()
        
        return stats
    
    def compare_pricing_tiers(self, input_tokens: int, output_tokens: int) -> dict:
        """
        Compare costs between standard and batch pricing tiers.
        
        Args:
            input_tokens: Number of input tokens
            output_tokens: Number of output tokens
            
        Returns:
            Dictionary with cost comparison:
            - standard_cost: Cost using standard pricing
            - batch_cost: Cost using batch pricing
            - savings: Amount saved using batch pricing
            - savings_percent: Percentage saved using batch pricing
        """
        standard_cost = self.estimate_cost(input_tokens, output_tokens, pricing_tier="standard")
        batch_cost = self.estimate_cost(input_tokens, output_tokens, pricing_tier="batch")
        savings = standard_cost - batch_cost
        savings_percent = (savings / standard_cost * 100) if standard_cost > 0 else 0
        
        return {
            "standard_cost": round(standard_cost, 6),
            "batch_cost": round(batch_cost, 6),
            "savings": round(savings, 6),
            "savings_percent": round(savings_percent, 2),
        }
    
    def estimate_video_cost(
        self,
        avg_input_tokens_per_request: int,
        avg_output_tokens_per_request: int,
        requests_per_video: int,
        pricing_tier: str | None = None,
    ) -> dict:
        """
        Estimate the cost per video based on average token usage.
        
        Args:
            avg_input_tokens_per_request: Average input tokens per API request
            avg_output_tokens_per_request: Average output tokens per API request
            requests_per_video: Number of API requests needed per video
            pricing_tier: Pricing tier to use ('standard' or 'batch'). 
                         If None, uses the provider's default pricing tier.
            
        Returns:
            Dictionary with video cost breakdown:
            - cost_per_request: Cost per API request
            - cost_per_video: Total cost per video
            - total_tokens_per_video: Total tokens used per video
            - pricing_tier: Pricing tier used for calculation
        """
        tier = pricing_tier or self.pricing_tier
        
        cost_per_request = self.estimate_cost(
            avg_input_tokens_per_request, 
            avg_output_tokens_per_request,
            pricing_tier=tier
        )
        
        cost_per_video = cost_per_request * requests_per_video
        total_tokens = (avg_input_tokens_per_request + avg_output_tokens_per_request) * requests_per_video
        
        return {
            "cost_per_request": round(cost_per_request, 6),
            "cost_per_video": round(cost_per_video, 6),
            "total_tokens_per_video": total_tokens,
            "requests_per_video": requests_per_video,
            "pricing_tier": tier,
            "model": self.model,
        }

    def reset_stats(self):
        """Reset usage statistics."""
        self.total_input_tokens = 0
        self.total_output_tokens = 0
        self.total_cost = 0.0
        self.request_count = 0
        
        if self.enable_cache and self.cache:
            self.cache.clear_stats()
        
        logger.info("Usage statistics reset")
