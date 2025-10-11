"""
OpenAI Provider - Wrapper for OpenAI API using new SDK (v1.0+).

This module provides a clean interface to the OpenAI API with proper error handling,
retry logic, and support for both synchronous and asynchronous operations.
"""

import os
import logging
from typing import Optional, List, Dict
from openai import OpenAI, AsyncOpenAI
from openai import OpenAIError, RateLimitError, APIError, APIConnectionError
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type,
)

from PrismQ.Shared.interfaces.llm_provider import ILLMProvider, IAsyncLLMProvider, ChatMessage

logger = logging.getLogger(__name__)


class OpenAIProvider(ILLMProvider):
    """
    Synchronous wrapper for OpenAI API using new SDK (v1.0+).

    This class provides a clean interface to OpenAI's chat completions API
    with automatic retry logic for rate limits and proper error handling.

    Implements the ILLMProvider interface for standardized LLM access.

    Example:
        >>> provider = OpenAIProvider(model="gpt-4o-mini")
        >>> messages = [{"role": "user", "content": "Hello!"}]
        >>> response = provider.generate_chat(messages)
        >>> print(response)
    """

    def __init__(self, api_key: str | None = None, model: str = "gpt-4o-mini"):
        """
        Initialize OpenAI provider.

        Args:
            api_key: OpenAI API key (defaults to OPENAI_API_KEY env var)
            model: Model to use for completions (default: gpt-4o-mini)

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
        self.client = OpenAI(api_key=self.api_key)
        logger.info(f"Initialized OpenAI provider with model: {model}")

    @property
    def model_name(self) -> str:
        """Get the name of the model being used."""
        return self.model

    def generate_completion(
        self,
        prompt: str,
        temperature: float = 0.7,
        max_tokens: int | None = None,
        **kwargs,
    ) -> str:
        """
        Generate completion from a single prompt (implements ILLMProvider).

        This is a convenience wrapper around generate_chat that formats
        a simple prompt as a user message.

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
        Generate chat completion (implements ILLMProvider).

        Args:
            messages: List of ChatMessage TypedDicts with role and content
            temperature: Sampling temperature (0-2, default: 0.7)
            max_tokens: Maximum tokens in response (optional)
            **kwargs: Additional parameters to pass to the API

        Returns:
            Generated text content as string

        Raises:
            RateLimitError: If rate limit exceeded after retries
            APIError: If API returns an error
            OpenAIError: For other OpenAI-related errors
        """
        return self.chat_completion(messages, temperature, max_tokens, **kwargs)

    @retry(
        retry=retry_if_exception_type((RateLimitError, APIConnectionError)),
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10),
    )
    def chat_completion(
        self,
        messages: list[ChatMessage],
        temperature: float = 0.7,
        max_tokens: int | None = None,
        **kwargs,
    ) -> str:
        """
        Generate chat completion with automatic retry on rate limits.

        Args:
            messages: List of ChatMessage TypedDicts with role and content
            temperature: Sampling temperature (0-2, default: 0.7)
            max_tokens: Maximum tokens in response (optional)
            **kwargs: Additional parameters to pass to the API

        Returns:
            Generated text content as string

        Raises:
            RateLimitError: If rate limit exceeded after retries
            APIError: If API returns an error
            OpenAIError: For other OpenAI-related errors
        """
        try:
            logger.debug(
                f"Calling OpenAI API: model={self.model}, "
                f"temperature={temperature}, messages={len(messages)}"
            )

            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
                **kwargs,
            )

            content = response.choices[0].message.content
            logger.debug(f"OpenAI API response received: {len(content)} characters")
            return content

        except RateLimitError as e:
            logger.warning(f"Rate limit hit: {e}. Retrying...")
            raise  # Will be retried by tenacity

        except APIConnectionError as e:
            logger.warning(f"API connection error: {e}. Retrying...")
            raise  # Will be retried by tenacity

        except APIError as e:
            logger.error(f"OpenAI API error: {e}")
            raise

        except OpenAIError as e:
            logger.error(f"OpenAI error: {e}")
            raise

        except Exception as e:
            logger.error(f"Unexpected error during OpenAI API call: {e}")
            raise

    def completion(
        self,
        prompt: str,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        **kwargs,
    ) -> str:
        """
        Generate completion from a single prompt (convenience method).

        This is a convenience wrapper around chat_completion that formats
        a simple prompt as a user message.

        Args:
            prompt: The prompt text
            temperature: Sampling temperature (0-2, default: 0.7)
            max_tokens: Maximum tokens in response (optional)
            **kwargs: Additional parameters to pass to the API

        Returns:
            Generated text content as string
        """
        messages = [{"role": "user", "content": prompt}]
        return self.chat_completion(messages, temperature, max_tokens, **kwargs)


class AsyncOpenAIProvider(IAsyncLLMProvider):
    """
    Asynchronous wrapper for OpenAI API using new SDK (v1.0+).

    This class provides async/await support for OpenAI API calls,
    useful for high-throughput applications.

    Implements the IAsyncLLMProvider interface for standardized async LLM access.

    Example:
        >>> provider = AsyncOpenAIProvider(model="gpt-4o-mini")
        >>> messages = [{"role": "user", "content": "Hello!"}]
        >>> response = await provider.generate_chat(messages)
        >>> print(response)
    """

    def __init__(self, api_key: str | None = None, model: str = "gpt-4o-mini"):
        """
        Initialize async OpenAI provider.

        Args:
            api_key: OpenAI API key (defaults to OPENAI_API_KEY env var)
            model: Model to use for completions (default: gpt-4o-mini)

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
        self.client = AsyncOpenAI(api_key=self.api_key)
        logger.info(f"Initialized async OpenAI provider with model: {model}")

    @property
    def model_name(self) -> str:
        """Get the name of the model being used."""
        return self.model

    async def generate_completion(
        self,
        prompt: str,
        temperature: float = 0.7,
        max_tokens: int | None = None,
        **kwargs,
    ) -> str:
        """
        Generate async completion from a single prompt (implements IAsyncLLMProvider).

        This is a convenience wrapper around generate_chat that formats
        a simple prompt as a user message.

        Args:
            prompt: The prompt text
            temperature: Sampling temperature (0-2, default: 0.7)
            max_tokens: Maximum tokens in response (optional)
            **kwargs: Additional parameters to pass to the API

        Returns:
            Generated text content as string
        """
        messages: list[ChatMessage] = [{"role": "user", "content": prompt}]
        return await self.generate_chat(messages, temperature, max_tokens, **kwargs)

    async def generate_chat(
        self,
        messages: list[ChatMessage],
        temperature: float = 0.7,
        max_tokens: int | None = None,
        **kwargs,
    ) -> str:
        """
        Generate async chat completion (implements IAsyncLLMProvider).

        Args:
            messages: List of ChatMessage TypedDicts with role and content
            temperature: Sampling temperature (0-2, default: 0.7)
            max_tokens: Maximum tokens in response (optional)
            **kwargs: Additional parameters to pass to the API

        Returns:
            Generated text content as string

        Raises:
            RateLimitError: If rate limit exceeded after retries
            APIError: If API returns an error
            OpenAIError: For other OpenAI-related errors
        """
        return await self.chat_completion(messages, temperature, max_tokens, **kwargs)

    @retry(
        retry=retry_if_exception_type((RateLimitError, APIConnectionError)),
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10),
    )
    async def chat_completion(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        **kwargs,
    ) -> str:
        """
        Generate async chat completion with automatic retry on rate limits.

        Args:
            messages: List of message dicts with 'role' and 'content' keys
            temperature: Sampling temperature (0-2, default: 0.7)
            max_tokens: Maximum tokens in response (optional)
            **kwargs: Additional parameters to pass to the API

        Returns:
            Generated text content as string

        Raises:
            RateLimitError: If rate limit exceeded after retries
            APIError: If API returns an error
            OpenAIError: For other OpenAI-related errors
        """
        try:
            logger.debug(
                f"Calling async OpenAI API: model={self.model}, "
                f"temperature={temperature}, messages={len(messages)}"
            )

            response = await self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
                **kwargs,
            )

            content = response.choices[0].message.content
            logger.debug(f"Async OpenAI API response received: {len(content)} characters")
            return content

        except RateLimitError as e:
            logger.warning(f"Rate limit hit: {e}. Retrying...")
            raise  # Will be retried by tenacity

        except APIConnectionError as e:
            logger.warning(f"API connection error: {e}. Retrying...")
            raise  # Will be retried by tenacity

        except APIError as e:
            logger.error(f"OpenAI API error: {e}")
            raise

        except OpenAIError as e:
            logger.error(f"OpenAI error: {e}")
            raise

        except Exception as e:
            logger.error(f"Unexpected error during async OpenAI API call: {e}")
            raise

    async def completion(
        self,
        prompt: str,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        **kwargs,
    ) -> str:
        """
        Generate async completion from a single prompt (convenience method).

        This is a convenience wrapper around chat_completion that formats
        a simple prompt as a user message.

        Args:
            prompt: The prompt text
            temperature: Sampling temperature (0-2, default: 0.7)
            max_tokens: Maximum tokens in response (optional)
            **kwargs: Additional parameters to pass to the API

        Returns:
            Generated text content as string
        """
        messages = [{"role": "user", "content": prompt}]
        return await self.chat_completion(messages, temperature, max_tokens, **kwargs)
