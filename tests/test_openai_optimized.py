"""
Tests for the optimized OpenAI provider.
"""

import os
from unittest.mock import Mock, patch, MagicMock

import pytest

from providers.openai_optimized import OptimizedOpenAIProvider, PRICING


@pytest.fixture
def mock_tiktoken():
    """Mock tiktoken encoder."""
    with patch("providers.openai_optimized.tiktoken") as mock_tk:
        mock_encoder = Mock()
        mock_encoder.encode.return_value = [1, 2, 3, 4, 5]  # 5 tokens
        mock_tk.encoding_for_model.return_value = mock_encoder
        mock_tk.get_encoding.return_value = mock_encoder
        yield mock_tk


@pytest.fixture
def mock_openai_client():
    """Mock OpenAI client for testing."""
    with patch("providers.openai_optimized.OpenAI") as mock_client_class:
        mock_client = Mock()
        mock_client_class.return_value = mock_client
        
        # Mock response
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "This is a test response"
        
        mock_client.chat.completions.create.return_value = mock_response
        
        yield mock_client


@pytest.fixture
def provider(mock_openai_client, mock_tiktoken):
    """Create an optimized provider with mocked client."""
    with patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"}):
        provider = OptimizedOpenAIProvider(
            model="gpt-4o-mini",
            enable_cache=False  # Disable cache for basic tests
        )
        return provider


def test_provider_initialization(provider):
    """Test provider initialization."""
    assert provider.model == "gpt-4o-mini"
    assert provider.enable_cache is False
    assert provider.total_input_tokens == 0
    assert provider.total_output_tokens == 0
    assert provider.total_cost == 0.0
    assert provider.request_count == 0


def test_provider_requires_api_key(mock_tiktoken):
    """Test that provider requires API key."""
    with patch.dict(os.environ, {}, clear=True):
        with pytest.raises(ValueError, match="OpenAI API key is required"):
            OptimizedOpenAIProvider()


def test_count_tokens(provider):
    """Test token counting."""
    text = "Hello, world!"
    tokens = provider.count_tokens(text)
    
    assert isinstance(tokens, int)
    assert tokens == 5  # Mocked to return 5 tokens


def test_count_messages_tokens(provider):
    """Test token counting for messages."""
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Hello!"}
    ]
    
    tokens = provider.count_messages_tokens(messages)
    
    assert isinstance(tokens, int)
    assert tokens > 0


def test_estimate_cost(provider):
    """Test cost estimation."""
    input_tokens = 100
    output_tokens = 50
    
    cost = provider.estimate_cost(input_tokens, output_tokens)
    
    # Cost should be positive and calculated from pricing
    assert cost > 0
    
    # Verify calculation
    pricing = PRICING["gpt-4o-mini"]
    expected_cost = (
        (input_tokens / 1_000_000) * pricing["input"] +
        (output_tokens / 1_000_000) * pricing["output"]
    )
    assert cost == expected_cost


def test_generate_completion(provider, mock_openai_client):
    """Test generating a completion."""
    prompt = "Hello, world!"
    
    result = provider.generate_completion(prompt)
    
    assert result == "This is a test response"
    assert provider.request_count == 1
    assert provider.total_input_tokens > 0
    assert provider.total_output_tokens > 0
    assert provider.total_cost > 0


def test_generate_chat(provider, mock_openai_client):
    """Test generating a chat completion."""
    messages = [
        {"role": "user", "content": "Hello!"}
    ]
    
    result = provider.generate_chat(messages)
    
    assert result == "This is a test response"
    assert provider.request_count == 1


def test_usage_tracking(provider, mock_openai_client):
    """Test that usage is tracked correctly."""
    # Make a few requests
    provider.generate_completion("First request")
    provider.generate_completion("Second request")
    provider.generate_completion("Third request")
    
    stats = provider.get_usage_stats()
    
    assert stats["request_count"] == 3
    assert stats["total_input_tokens"] > 0
    assert stats["total_output_tokens"] > 0
    assert stats["total_cost"] > 0
    assert stats["model"] == "gpt-4o-mini"
    assert "average_tokens_per_request" in stats


def test_reset_stats(provider, mock_openai_client):
    """Test resetting usage statistics."""
    # Make a request
    provider.generate_completion("Test")
    
    assert provider.request_count > 0
    
    # Reset
    provider.reset_stats()
    
    assert provider.request_count == 0
    assert provider.total_input_tokens == 0
    assert provider.total_output_tokens == 0
    assert provider.total_cost == 0


def test_caching_enabled(mock_tiktoken):
    """Test that caching can be enabled."""
    with patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"}):
        with patch("providers.openai_optimized.OpenAI"):
            provider = OptimizedOpenAIProvider(enable_cache=True)
            
            assert provider.enable_cache is True
            assert provider.cache is not None


def test_cached_responses(mock_openai_client, mock_tiktoken):
    """Test that identical requests are cached."""
    with patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"}):
        provider = OptimizedOpenAIProvider(enable_cache=True)
        
        messages = [{"role": "user", "content": "Test"}]
        
        # First call
        result1 = provider.generate_chat(messages)
        first_call_count = mock_openai_client.chat.completions.create.call_count
        
        # Second call with same messages - should be cached
        result2 = provider.generate_chat(messages)
        second_call_count = mock_openai_client.chat.completions.create.call_count
        
        # Results should be the same
        assert result1 == result2
        
        # API should only be called once (second was cached)
        assert second_call_count == first_call_count


def test_cache_stats_in_usage_stats(mock_tiktoken):
    """Test that cache stats are included when caching is enabled."""
    with patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"}):
        with patch("providers.openai_optimized.OpenAI"):
            provider = OptimizedOpenAIProvider(enable_cache=True)
            
            stats = provider.get_usage_stats()
            
            assert "cache_stats" in stats


def test_model_name_property(provider):
    """Test model_name property."""
    assert provider.model_name == "gpt-4o-mini"


def test_temperature_parameter(provider, mock_openai_client):
    """Test that temperature is passed to API."""
    provider.generate_completion("Test", temperature=0.9)
    
    # Verify temperature was passed
    call_args = mock_openai_client.chat.completions.create.call_args
    assert call_args[1]["temperature"] == 0.9


def test_max_tokens_parameter(provider, mock_openai_client):
    """Test that max_tokens is passed to API."""
    provider.generate_completion("Test", max_tokens=100)
    
    # Verify max_tokens was passed
    call_args = mock_openai_client.chat.completions.create.call_args
    assert call_args[1]["max_tokens"] == 100


def test_retry_on_rate_limit(mock_openai_client, mock_tiktoken):
    """Test that rate limit errors trigger retry."""
    from openai import RateLimitError
    
    with patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"}):
        provider = OptimizedOpenAIProvider(enable_cache=False)
        
        # Create a mock response object
        mock_response = Mock()
        mock_response.request = Mock()
        
        # First call raises rate limit, second succeeds
        mock_openai_client.chat.completions.create.side_effect = [
            RateLimitError("Rate limited", response=mock_response, body=None),
            Mock(choices=[Mock(message=Mock(content="Success"))])
        ]
        
        # Should succeed after retry
        result = provider.generate_completion("Test")
        assert result == "Success"
        
        # Should have been called twice (original + 1 retry)
        assert mock_openai_client.chat.completions.create.call_count == 2
