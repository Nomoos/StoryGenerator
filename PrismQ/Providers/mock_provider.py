"""
Mock LLM Provider for testing.

This module provides a mock implementation of the ILLMProvider interface
for use in unit tests and development.
"""

from typing import Dict, List, Optional
from PrismQ.Shared.interfaces.llm_provider import ILLMProvider, IAsyncLLMProvider


class MockLLMProvider(ILLMProvider):
    """
    Mock LLM provider for testing.

    Returns predefined responses for testing without making actual API calls.

    Example:
        >>> provider = MockLLMProvider(response="Test response")
        >>> result = provider.generate_completion("prompt")
        >>> assert result == "Test response"
    """

    def __init__(self, model: str = "mock-model", response: str = "Mock response"):
        """
        Initialize mock provider.

        Args:
            model: Model name to report
            response: Default response to return
        """
        self.model = model
        self.response = response
        self.call_count = 0
        self.last_prompt = None
        self.last_messages = None
        self._smart_mode = False  # Enable smart responses

    @property
    def model_name(self) -> str:
        """Get the name of the model being used."""
        return self.model

    def generate_completion(
        self,
        prompt: str,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        **kwargs,
    ) -> str:
        """
        Generate a mock completion from a prompt.

        Args:
            prompt: The input prompt text
            temperature: Sampling temperature (ignored)
            max_tokens: Maximum tokens (ignored)
            **kwargs: Additional parameters (ignored)

        Returns:
            The predefined mock response or smart response
        """
        self.call_count += 1
        self.last_prompt = prompt
        
        # Try to provide smart responses based on prompt
        if "cluster" in prompt.lower() or "topic" in prompt.lower():
            return """Topic 1: Relationships and Personal Connections
Theme: Stories about love, friendships, and family dynamics
Ideas: 1, 2

Topic 2: Career and Success
Theme: Stories about professional growth and achievement
Ideas: 3"""
        elif "title" in prompt.lower():
            return """1. Why nobody tells you about this shocking secret
2. The truth about relationships that changed everything
3. 5 things I discovered that blew my mind"""
        
        return self.response

    def generate_chat(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        **kwargs,
    ) -> str:
        """
        Generate a mock chat completion from messages.

        Args:
            messages: List of message dicts
            temperature: Sampling temperature (ignored)
            max_tokens: Maximum tokens (ignored)
            **kwargs: Additional parameters (ignored)

        Returns:
            The predefined mock response
        """
        self.call_count += 1
        self.last_messages = messages
        return self.response


class AsyncMockLLMProvider(IAsyncLLMProvider):
    """
    Async mock LLM provider for testing.

    Returns predefined responses for testing without making actual API calls.
    """

    def __init__(self, model: str = "mock-model", response: str = "Mock response"):
        """
        Initialize async mock provider.

        Args:
            model: Model name to report
            response: Default response to return
        """
        self.model = model
        self.response = response
        self.call_count = 0
        self.last_prompt = None
        self.last_messages = None

    @property
    def model_name(self) -> str:
        """Get the name of the model being used."""
        return self.model

    async def generate_completion(
        self,
        prompt: str,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        **kwargs,
    ) -> str:
        """
        Generate an async mock completion from a prompt.

        Args:
            prompt: The input prompt text
            temperature: Sampling temperature (ignored)
            max_tokens: Maximum tokens (ignored)
            **kwargs: Additional parameters (ignored)

        Returns:
            The predefined mock response
        """
        self.call_count += 1
        self.last_prompt = prompt
        return self.response

    async def generate_chat(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        **kwargs,
    ) -> str:
        """
        Generate an async mock chat completion from messages.

        Args:
            messages: List of message dicts
            temperature: Sampling temperature (ignored)
            max_tokens: Maximum tokens (ignored)
            **kwargs: Additional parameters (ignored)

        Returns:
            The predefined mock response
        """
        self.call_count += 1
        self.last_messages = messages
        return self.response
