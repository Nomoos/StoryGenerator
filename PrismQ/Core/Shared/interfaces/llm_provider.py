"""
LLM Provider Interface.

This module defines the abstract interface for Language Model providers,
enabling easy swapping between different LLM implementations (OpenAI, local models, etc.).
"""

from abc import ABC, abstractmethod
import sys

# NotRequired is only in typing module in Python 3.11+
if sys.version_info >= (3, 11):
    from typing import TypedDict, NotRequired
else:
    from typing import TypedDict
    from typing_extensions import NotRequired


class ChatMessage(TypedDict):
    """
    Structured message format for chat completions.
    
    This TypedDict ensures type safety when building chat messages
    for LLM providers following OpenAI's chat format.
    """
    role: str  # "system", "user", or "assistant"
    content: str
    name: NotRequired[str]  # Optional: name of the message author


class ILLMProvider(ABC):
    """
    Abstract interface for Language Model providers.

    This interface defines the contract that all LLM providers must implement,
    allowing for easy swapping between OpenAI, local models, or other providers.

    Example:
        >>> class MyLLMProvider(ILLMProvider):
        ...     def generate_completion(self, prompt: str, **kwargs) -> str:
        ...         # Implementation here
        ...         pass
    """

    @abstractmethod
    def generate_completion(
        self,
        prompt: str,
        temperature: float = 0.7,
        max_tokens: int | None = None,
        **kwargs,
    ) -> str:
        """
        Generate a completion from a single prompt.

        Args:
            prompt: The input prompt text
            temperature: Sampling temperature (0-2, default: 0.7)
            max_tokens: Maximum tokens in response (optional)
            **kwargs: Additional provider-specific parameters

        Returns:
            Generated text content as string

        Raises:
            Exception: If generation fails
        """
        pass

    @abstractmethod
    def generate_chat(
        self,
        messages: list[ChatMessage],
        temperature: float = 0.7,
        max_tokens: int | None = None,
        **kwargs,
    ) -> str:
        """
        Generate a chat completion from a conversation history.

        Args:
            messages: List of ChatMessage TypedDicts with role and content
            temperature: Sampling temperature (0-2, default: 0.7)
            max_tokens: Maximum tokens in response (optional)
            **kwargs: Additional provider-specific parameters

        Returns:
            Generated text content as string

        Raises:
            Exception: If generation fails
        """
        pass

    @property
    @abstractmethod
    def model_name(self) -> str:
        """
        Get the name of the model being used.

        Returns:
            Model name string
        """
        pass


class IAsyncLLMProvider(ABC):
    """
    Abstract interface for asynchronous Language Model providers.

    This interface defines the async contract for LLM providers,
    enabling high-throughput applications with async/await.
    """

    @abstractmethod
    async def generate_completion(
        self,
        prompt: str,
        temperature: float = 0.7,
        max_tokens: int | None = None,
        **kwargs,
    ) -> str:
        """
        Generate an async completion from a single prompt.

        Args:
            prompt: The input prompt text
            temperature: Sampling temperature (0-2, default: 0.7)
            max_tokens: Maximum tokens in response (optional)
            **kwargs: Additional provider-specific parameters

        Returns:
            Generated text content as string

        Raises:
            Exception: If generation fails
        """
        pass

    @abstractmethod
    async def generate_chat(
        self,
        messages: list[ChatMessage],
        temperature: float = 0.7,
        max_tokens: int | None = None,
        **kwargs,
    ) -> str:
        """
        Generate an async chat completion from a conversation history.

        Args:
            messages: List of ChatMessage TypedDicts with role and content
            temperature: Sampling temperature (0-2, default: 0.7)
            max_tokens: Maximum tokens in response (optional)
            **kwargs: Additional provider-specific parameters

        Returns:
            Generated text content as string

        Raises:
            Exception: If generation fails
        """
        pass

    @property
    @abstractmethod
    def model_name(self) -> str:
        """
        Get the name of the model being used.

        Returns:
            Model name string
        """
        pass
