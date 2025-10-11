"""
Mock ElevenLabs provider for testing without API keys.

This module provides a mock implementation of the ElevenLabs provider that can be used
in tests without requiring actual API keys or making real API calls.
"""

from typing import Optional, Dict, Any
from dataclasses import dataclass
import io


@dataclass
class MockAudioMetadata:
    """Mock audio metadata."""
    duration_seconds: float = 5.0
    sample_rate: int = 44100
    channels: int = 1
    bit_depth: int = 16


class MockElevenLabsProvider:
    """
    Mock ElevenLabs provider for testing.
    
    This provider simulates the ElevenLabs API without making actual API calls.
    It returns mock audio data for testing purposes.
    
    Example:
        >>> provider = MockElevenLabsProvider()
        >>> audio_data = provider.generate(text="Hello world", voice_id="voice-123")
        >>> assert isinstance(audio_data, bytes)
    """
    
    def __init__(self, api_key: str = "mock-api-key"):
        """
        Initialize mock provider.
        
        Args:
            api_key: Ignored, accepts any value
        """
        self.api_key = api_key
        self.call_count = 0
        self.last_text = None
        self.last_voice_id = None
        self.last_kwargs = None
        
        # Mock audio data (just a simple byte pattern)
        self.mock_audio_data = b"MOCK_AUDIO_DATA" * 100
    
    def set_audio_data(self, audio_data: bytes) -> None:
        """
        Set custom audio data to return.
        
        Args:
            audio_data: Audio data bytes to return
        """
        self.mock_audio_data = audio_data
    
    def generate(
        self,
        text: str,
        voice_id: str = "BZgkqPqms7Kj9ulSkVzn",
        model: str = "eleven_v3",
        stability: float = 0.5,
        similarity_boost: float = 0.75,
        **kwargs
    ) -> bytes:
        """
        Generate mock audio from text.
        
        Args:
            text: Text to convert to speech
            voice_id: Voice ID (logged but not used)
            model: Model name (logged but not used)
            stability: Voice stability (logged but not used)
            similarity_boost: Similarity boost (logged but not used)
            **kwargs: Additional parameters (logged but not used)
            
        Returns:
            bytes: Mock audio data
        """
        self.call_count += 1
        self.last_text = text
        self.last_voice_id = voice_id
        self.last_kwargs = {
            "model": model,
            "stability": stability,
            "similarity_boost": similarity_boost,
            **kwargs
        }
        
        return self.mock_audio_data
    
    def generate_stream(
        self,
        text: str,
        voice_id: str = "BZgkqPqms7Kj9ulSkVzn",
        chunk_size: int = 1024,
        **kwargs
    ):
        """
        Generate mock audio stream.
        
        Args:
            text: Text to convert to speech
            voice_id: Voice ID (logged but not used)
            chunk_size: Size of chunks to yield
            **kwargs: Additional parameters (logged but not used)
            
        Yields:
            bytes: Audio data chunks
        """
        self.call_count += 1
        self.last_text = text
        self.last_voice_id = voice_id
        self.last_kwargs = {"chunk_size": chunk_size, **kwargs}
        
        # Yield audio data in chunks
        audio_data = self.mock_audio_data
        for i in range(0, len(audio_data), chunk_size):
            yield audio_data[i:i + chunk_size]
    
    def get_voices(self) -> list:
        """
        Get list of available voices.
        
        Returns:
            list: List of mock voice dictionaries
        """
        self.call_count += 1
        
        return [
            {
                "voice_id": "voice-1",
                "name": "Mock Voice 1",
                "category": "generated",
                "labels": {"accent": "american", "age": "young"}
            },
            {
                "voice_id": "voice-2",
                "name": "Mock Voice 2",
                "category": "premade",
                "labels": {"accent": "british", "age": "middle_aged"}
            }
        ]
    
    def get_voice(self, voice_id: str) -> dict:
        """
        Get details for a specific voice.
        
        Args:
            voice_id: Voice ID
            
        Returns:
            dict: Mock voice details
        """
        self.call_count += 1
        
        return {
            "voice_id": voice_id,
            "name": f"Mock Voice {voice_id}",
            "category": "generated",
            "labels": {"accent": "american", "age": "young"}
        }
    
    def get_metadata(self) -> MockAudioMetadata:
        """
        Get metadata for the last generated audio.
        
        Returns:
            MockAudioMetadata: Audio metadata
        """
        return MockAudioMetadata()
    
    def reset(self) -> None:
        """Reset the mock provider state."""
        self.call_count = 0
        self.last_text = None
        self.last_voice_id = None
        self.last_kwargs = None


class MockAsyncElevenLabsProvider(MockElevenLabsProvider):
    """
    Async version of mock ElevenLabs provider.
    
    Example:
        >>> provider = MockAsyncElevenLabsProvider()
        >>> audio = await provider.generate_async("Hello world")
    """
    
    async def generate_async(
        self,
        text: str,
        voice_id: str = "BZgkqPqms7Kj9ulSkVzn",
        **kwargs
    ) -> bytes:
        """Async version of generate."""
        return self.generate(text, voice_id, **kwargs)
    
    async def generate_stream_async(
        self,
        text: str,
        voice_id: str = "BZgkqPqms7Kj9ulSkVzn",
        chunk_size: int = 1024,
        **kwargs
    ):
        """Async version of generate_stream."""
        for chunk in self.generate_stream(text, voice_id, chunk_size, **kwargs):
            yield chunk


def create_mock_provider(audio_data: Optional[bytes] = None) -> MockElevenLabsProvider:
    """
    Factory function to create a mock provider.
    
    Args:
        audio_data: Optional custom audio data to return
        
    Returns:
        MockElevenLabsProvider: Configured mock provider
        
    Example:
        >>> provider = create_mock_provider(b"custom_audio")
        >>> audio = provider.generate("Test text")
        >>> assert audio == b"custom_audio"
    """
    provider = MockElevenLabsProvider()
    if audio_data:
        provider.set_audio_data(audio_data)
    return provider
