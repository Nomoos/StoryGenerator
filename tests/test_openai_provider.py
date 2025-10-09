"""
Tests for OpenAI Provider.

This module tests the OpenAIProvider and AsyncOpenAIProvider classes,
including initialization, API calls, error handling, and retry logic.
"""

import pytest
from unittest.mock import Mock, patch, AsyncMock
from openai import APIError, RateLimitError, APIConnectionError
from providers.openai_provider import OpenAIProvider, AsyncOpenAIProvider
from providers.mock_provider import MockLLMProvider, AsyncMockLLMProvider
from core.interfaces.llm_provider import ILLMProvider, IAsyncLLMProvider


class TestOpenAIProvider:
    """Tests for synchronous OpenAIProvider."""

    def test_initialization_with_api_key(self):
        """Test provider initializes correctly with explicit API key."""
        provider = OpenAIProvider(api_key="test-key", model="gpt-4o-mini")
        assert provider.model == "gpt-4o-mini"
        assert provider.api_key == "test-key"
        assert provider.client is not None
        assert isinstance(provider, ILLMProvider)
        assert provider.model_name == "gpt-4o-mini"

    def test_initialization_from_env(self, monkeypatch):
        """Test provider initializes from environment variable."""
        monkeypatch.setenv("OPENAI_API_KEY", "env-test-key")
        provider = OpenAIProvider(model="gpt-4o-mini")
        assert provider.api_key == "env-test-key"

    def test_initialization_without_api_key(self, monkeypatch):
        """Test provider raises error when no API key is provided."""
        monkeypatch.delenv("OPENAI_API_KEY", raising=False)
        with pytest.raises(ValueError, match="OpenAI API key is required"):
            OpenAIProvider()

    def test_generate_chat_interface_method(self):
        """Test generate_chat interface method."""
        provider = OpenAIProvider(api_key="test-key", model="gpt-4o-mini")

        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "Interface response"

        with patch.object(provider.client.chat.completions, "create", return_value=mock_response):
            messages = [{"role": "user", "content": "Test"}]
            result = provider.generate_chat(messages)
            assert result == "Interface response"

    def test_generate_completion_interface_method(self):
        """Test generate_completion interface method."""
        provider = OpenAIProvider(api_key="test-key", model="gpt-4o-mini")

        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "Interface response"

        with patch.object(provider.client.chat.completions, "create", return_value=mock_response):
            result = provider.generate_completion("Test prompt")
            assert result == "Interface response"

    def test_chat_completion_success(self):
        """Test successful chat completion."""
        provider = OpenAIProvider(api_key="test-key", model="gpt-4o-mini")

        # Mock the client's chat completions
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "Test response"

        with patch.object(provider.client.chat.completions, "create", return_value=mock_response):
            messages = [{"role": "user", "content": "Test prompt"}]
            result = provider.chat_completion(messages)

            assert result == "Test response"

    def test_chat_completion_with_parameters(self):
        """Test chat completion with custom parameters."""
        provider = OpenAIProvider(api_key="test-key", model="gpt-4o-mini")

        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "Test response"

        with patch.object(
            provider.client.chat.completions, "create", return_value=mock_response
        ) as mock_create:
            messages = [{"role": "user", "content": "Test"}]
            result = provider.chat_completion(messages, temperature=0.9, max_tokens=100)

            assert result == "Test response"
            mock_create.assert_called_once()
            call_kwargs = mock_create.call_args.kwargs
            assert call_kwargs["temperature"] == 0.9
            assert call_kwargs["max_tokens"] == 100

    def test_completion_convenience_method(self):
        """Test completion convenience method."""
        provider = OpenAIProvider(api_key="test-key", model="gpt-4o-mini")

        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "Response"

        with patch.object(provider.client.chat.completions, "create", return_value=mock_response):
            result = provider.completion("Test prompt")
            assert result == "Response"

    def test_chat_completion_api_error(self):
        """Test error handling for API errors."""
        provider = OpenAIProvider(api_key="test-key", model="gpt-4o-mini")

        # Create a mock request and APIError properly
        mock_request = Mock()
        with patch.object(
            provider.client.chat.completions,
            "create",
            side_effect=APIError("Test error", request=mock_request, body=None),
        ):
            messages = [{"role": "user", "content": "Test"}]
            with pytest.raises(APIError):
                provider.chat_completion(messages)

    def test_chat_completion_rate_limit_retry(self):
        """Test retry logic for rate limit errors."""
        provider = OpenAIProvider(api_key="test-key", model="gpt-4o-mini")

        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "Success after retry"

        # Create properly formatted RateLimitError
        mock_http_response = Mock()
        mock_http_response.status_code = 429

        # First two calls raise RateLimitError, third succeeds
        with patch.object(
            provider.client.chat.completions,
            "create",
            side_effect=[
                RateLimitError("Rate limit", response=mock_http_response, body=None),
                RateLimitError("Rate limit", response=mock_http_response, body=None),
                mock_response,
            ],
        ):
            messages = [{"role": "user", "content": "Test"}]
            result = provider.chat_completion(messages)
            assert result == "Success after retry"

    def test_chat_completion_max_retries_exceeded(self):
        """Test that retries stop after maximum attempts."""
        from tenacity import RetryError

        provider = OpenAIProvider(api_key="test-key", model="gpt-4o-mini")

        # Create properly formatted RateLimitError
        mock_http_response = Mock()
        mock_http_response.status_code = 429

        with patch.object(
            provider.client.chat.completions,
            "create",
            side_effect=RateLimitError("Rate limit", response=mock_http_response, body=None),
        ):
            messages = [{"role": "user", "content": "Test"}]
            # After max retries, tenacity wraps the exception in a RetryError
            with pytest.raises(RetryError):
                provider.chat_completion(messages)


class TestAsyncOpenAIProvider:
    """Tests for asynchronous AsyncOpenAIProvider."""

    def test_initialization_with_api_key(self):
        """Test async provider initializes correctly with explicit API key."""
        provider = AsyncOpenAIProvider(api_key="test-key", model="gpt-4o-mini")
        assert provider.model == "gpt-4o-mini"
        assert provider.api_key == "test-key"
        assert provider.client is not None
        assert isinstance(provider, IAsyncLLMProvider)
        assert provider.model_name == "gpt-4o-mini"

    def test_initialization_from_env(self, monkeypatch):
        """Test async provider initializes from environment variable."""
        monkeypatch.setenv("OPENAI_API_KEY", "env-test-key")
        provider = AsyncOpenAIProvider(model="gpt-4o-mini")
        assert provider.api_key == "env-test-key"

    def test_initialization_without_api_key(self, monkeypatch):
        """Test async provider raises error when no API key is provided."""
        monkeypatch.delenv("OPENAI_API_KEY", raising=False)
        with pytest.raises(ValueError, match="OpenAI API key is required"):
            AsyncOpenAIProvider()

    @pytest.mark.asyncio
    async def test_generate_chat_interface_method(self):
        """Test async generate_chat interface method."""
        provider = AsyncOpenAIProvider(api_key="test-key", model="gpt-4o-mini")

        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "Interface response"

        with patch.object(
            provider.client.chat.completions,
            "create",
            new_callable=AsyncMock,
            return_value=mock_response,
        ):
            messages = [{"role": "user", "content": "Test"}]
            result = await provider.generate_chat(messages)
            assert result == "Interface response"

    @pytest.mark.asyncio
    async def test_generate_completion_interface_method(self):
        """Test async generate_completion interface method."""
        provider = AsyncOpenAIProvider(api_key="test-key", model="gpt-4o-mini")

        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "Interface response"

        with patch.object(
            provider.client.chat.completions,
            "create",
            new_callable=AsyncMock,
            return_value=mock_response,
        ):
            result = await provider.generate_completion("Test prompt")
            assert result == "Interface response"

    @pytest.mark.asyncio
    async def test_chat_completion_success(self):
        """Test successful async chat completion."""
        provider = AsyncOpenAIProvider(api_key="test-key", model="gpt-4o-mini")

        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "Async response"

        with patch.object(
            provider.client.chat.completions,
            "create",
            new_callable=AsyncMock,
            return_value=mock_response,
        ):
            messages = [{"role": "user", "content": "Test prompt"}]
            result = await provider.chat_completion(messages)
            assert result == "Async response"

    @pytest.mark.asyncio
    async def test_completion_convenience_method(self):
        """Test async completion convenience method."""
        provider = AsyncOpenAIProvider(api_key="test-key", model="gpt-4o-mini")

        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "Response"

        with patch.object(
            provider.client.chat.completions,
            "create",
            new_callable=AsyncMock,
            return_value=mock_response,
        ):
            result = await provider.completion("Test prompt")
            assert result == "Response"

    @pytest.mark.asyncio
    async def test_chat_completion_api_error(self):
        """Test error handling for API errors in async mode."""
        provider = AsyncOpenAIProvider(api_key="test-key", model="gpt-4o-mini")

        # Create a mock request and APIError properly
        mock_request = Mock()
        with patch.object(
            provider.client.chat.completions,
            "create",
            new_callable=AsyncMock,
            side_effect=APIError("Test error", request=mock_request, body=None),
        ):
            messages = [{"role": "user", "content": "Test"}]
            with pytest.raises(APIError):
                await provider.chat_completion(messages)

    @pytest.mark.asyncio
    async def test_chat_completion_rate_limit_retry(self):
        """Test retry logic for rate limit errors in async mode."""
        provider = AsyncOpenAIProvider(api_key="test-key", model="gpt-4o-mini")

        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "Success after retry"

        # Create properly formatted RateLimitError
        mock_http_response = Mock()
        mock_http_response.status_code = 429

        # First call raises RateLimitError, second succeeds
        with patch.object(
            provider.client.chat.completions,
            "create",
            new_callable=AsyncMock,
            side_effect=[
                RateLimitError("Rate limit", response=mock_http_response, body=None),
                mock_response,
            ],
        ):
            messages = [{"role": "user", "content": "Test"}]
            result = await provider.chat_completion(messages)
            assert result == "Success after retry"


# Integration-style test (requires actual API key, marked as slow)
@pytest.mark.slow
@pytest.mark.skipif(
    "OPENAI_API_KEY" not in __import__("os").environ,
    reason="OPENAI_API_KEY not set",
)
class TestOpenAIProviderIntegration:
    """Integration tests for OpenAI provider (requires API key)."""

    def test_real_api_call(self):
        """Test actual API call (requires valid API key)."""
        provider = OpenAIProvider(model="gpt-4o-mini")
        messages = [{"role": "user", "content": "Say 'test' and nothing else."}]
        result = provider.chat_completion(messages, temperature=0.0)
        assert isinstance(result, str)
        assert len(result) > 0


class TestMockLLMProvider:
    """Tests for MockLLMProvider."""

    def test_initialization(self):
        """Test mock provider initializes correctly."""
        provider = MockLLMProvider(model="test-model", response="Test")
        assert provider.model_name == "test-model"
        assert provider.response == "Test"
        assert isinstance(provider, ILLMProvider)

    def test_generate_completion(self):
        """Test mock completion generation."""
        provider = MockLLMProvider(response="Mock response")
        result = provider.generate_completion("Test prompt")
        assert result == "Mock response"
        assert provider.call_count == 1
        assert provider.last_prompt == "Test prompt"

    def test_generate_chat(self):
        """Test mock chat generation."""
        provider = MockLLMProvider(response="Chat response")
        messages = [{"role": "user", "content": "Hello"}]
        result = provider.generate_chat(messages)
        assert result == "Chat response"
        assert provider.call_count == 1
        assert provider.last_messages == messages


class TestAsyncMockLLMProvider:
    """Tests for AsyncMockLLMProvider."""

    def test_initialization(self):
        """Test async mock provider initializes correctly."""
        provider = AsyncMockLLMProvider(model="test-model", response="Test")
        assert provider.model_name == "test-model"
        assert provider.response == "Test"
        assert isinstance(provider, IAsyncLLMProvider)

    @pytest.mark.asyncio
    async def test_generate_completion(self):
        """Test async mock completion generation."""
        provider = AsyncMockLLMProvider(response="Mock response")
        result = await provider.generate_completion("Test prompt")
        assert result == "Mock response"
        assert provider.call_count == 1
        assert provider.last_prompt == "Test prompt"

    @pytest.mark.asyncio
    async def test_generate_chat(self):
        """Test async mock chat generation."""
        provider = AsyncMockLLMProvider(response="Chat response")
        messages = [{"role": "user", "content": "Hello"}]
        result = await provider.generate_chat(messages)
        assert result == "Chat response"
        assert provider.call_count == 1
        assert provider.last_messages == messages
