"""
Mock OpenAI provider for testing without API keys.

This module provides a mock implementation of the OpenAI provider that can be used
in tests without requiring actual API keys or making real API calls.
"""

from typing import List, Dict, Any, Optional
from dataclasses import dataclass


@dataclass
class MockChatMessage:
    """Mock chat message."""
    role: str
    content: str


@dataclass
class MockChoice:
    """Mock choice from API response."""
    message: MockChatMessage
    finish_reason: str = "stop"
    index: int = 0


@dataclass
class MockChatCompletion:
    """Mock chat completion response."""
    id: str = "mock-completion-id"
    choices: List[MockChoice] = None
    model: str = "gpt-4o-mini"
    usage: Dict[str, int] = None
    
    def __post_init__(self):
        if self.choices is None:
            self.choices = [
                MockChoice(
                    message=MockChatMessage(role="assistant", content="This is a mock response."),
                    finish_reason="stop",
                    index=0
                )
            ]
        if self.usage is None:
            self.usage = {"prompt_tokens": 10, "completion_tokens": 20, "total_tokens": 30}


class MockOpenAIProvider:
    """
    Mock OpenAI provider for testing.
    
    This provider simulates the OpenAI API without making actual API calls.
    You can configure it to return specific responses for testing.
    
    Example:
        >>> provider = MockOpenAIProvider()
        >>> provider.set_response("Custom test response")
        >>> messages = [{"role": "user", "content": "Hello"}]
        >>> response = provider.generate_chat(messages)
        >>> print(response)
        Custom test response
    """
    
    def __init__(self, api_key: str = "mock-api-key", model: str = "gpt-4o-mini"):
        """
        Initialize mock provider.
        
        Args:
            api_key: Ignored, accepts any value
            model: Model name (for testing purposes)
        """
        self.api_key = api_key
        self.model = model
        self.responses = []
        self.call_count = 0
        self.last_messages = None
        self.last_kwargs = None
        
        # Default responses
        self.default_response = "This is a mock response from the OpenAI provider."
    
    def set_response(self, response: str) -> None:
        """
        Set a single response to return.
        
        Args:
            response: Response text to return
        """
        self.responses = [response]
    
    def set_responses(self, responses: List[str]) -> None:
        """
        Set multiple responses to return in sequence.
        
        Args:
            responses: List of response texts
        """
        self.responses = responses.copy()
    
    def generate_chat(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        **kwargs
    ) -> str:
        """
        Generate a mock chat completion.
        
        Args:
            messages: List of message dictionaries
            temperature: Temperature parameter (logged but not used)
            max_tokens: Max tokens parameter (logged but not used)
            **kwargs: Additional parameters (logged but not used)
            
        Returns:
            str: Mock response text
        """
        self.call_count += 1
        self.last_messages = messages
        self.last_kwargs = {"temperature": temperature, "max_tokens": max_tokens, **kwargs}
        
        # Return next queued response or default
        if self.responses:
            return self.responses.pop(0)
        return self.default_response
    
    def generate_completion(
        self,
        prompt: str,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        **kwargs
    ) -> MockChatCompletion:
        """
        Generate a mock completion object.
        
        Args:
            prompt: Prompt text
            temperature: Temperature parameter (logged but not used)
            max_tokens: Max tokens parameter (logged but not used)
            **kwargs: Additional parameters (logged but not used)
            
        Returns:
            MockChatCompletion: Mock completion object
        """
        self.call_count += 1
        self.last_kwargs = {"temperature": temperature, "max_tokens": max_tokens, **kwargs}
        
        # Return response
        response_text = self.responses.pop(0) if self.responses else self.default_response
        
        return MockChatCompletion(
            choices=[
                MockChoice(
                    message=MockChatMessage(role="assistant", content=response_text)
                )
            ]
        )
    
    def reset(self) -> None:
        """Reset the mock provider state."""
        self.responses = []
        self.call_count = 0
        self.last_messages = None
        self.last_kwargs = None


class MockAsyncOpenAIProvider(MockOpenAIProvider):
    """
    Async version of mock OpenAI provider.
    
    Example:
        >>> provider = MockAsyncOpenAIProvider()
        >>> provider.set_response("Async response")
        >>> response = await provider.generate_chat_async([...])
    """
    
    async def generate_chat_async(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        **kwargs
    ) -> str:
        """Async version of generate_chat."""
        return self.generate_chat(messages, temperature, max_tokens, **kwargs)
    
    async def generate_completion_async(
        self,
        prompt: str,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        **kwargs
    ) -> MockChatCompletion:
        """Async version of generate_completion."""
        return self.generate_completion(prompt, temperature, max_tokens, **kwargs)


def create_mock_provider(responses: Optional[List[str]] = None) -> MockOpenAIProvider:
    """
    Factory function to create a mock provider.
    
    Args:
        responses: Optional list of responses to return
        
    Returns:
        MockOpenAIProvider: Configured mock provider
        
    Example:
        >>> provider = create_mock_provider(["Response 1", "Response 2"])
        >>> print(provider.generate_chat([{"role": "user", "content": "Hello"}]))
        Response 1
    """
    provider = MockOpenAIProvider()
    if responses:
        provider.set_responses(responses)
    return provider
