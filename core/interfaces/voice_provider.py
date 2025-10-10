"""
Voice/TTS Provider Interface.

This module defines the abstract interface for Text-to-Speech providers,
enabling easy swapping between different TTS implementations (ElevenLabs, Google, etc.).
"""

from abc import ABC, abstractmethod
from typing import Optional


class IVoiceProvider(ABC):
    """
    Abstract interface for Text-to-Speech providers.

    This interface defines the contract that all TTS providers must implement,
    allowing for easy swapping between ElevenLabs, Google TTS, or other providers.

    Example:
        >>> class MyVoiceProvider(IVoiceProvider):
        ...     def synthesize(self, text: str, voice_id: str) -> bytes:
        ...         # Implementation here
        ...         pass
    """

    @abstractmethod
    def synthesize(
        self,
        text: str,
        voice_id: str,
        stability: float = 0.5,
        similarity_boost: float = 0.75,
        **kwargs,
    ) -> bytes:
        """
        Synthesize speech from text.

        Args:
            text: Text to convert to speech
            voice_id: ID or name of the voice to use
            stability: Voice stability (0-1, default: 0.5)
            similarity_boost: Similarity to original voice (0-1, default: 0.75)
            **kwargs: Additional provider-specific parameters

        Returns:
            Audio data as bytes

        Raises:
            Exception: If synthesis fails
        """
        pass

    @abstractmethod
    def list_voices(self) -> list[dict]:
        """
        List available voices.

        Returns:
            List of dictionaries with voice information:
            - voice_id: Unique identifier
            - name: Display name
            - language: Language code (e.g., 'en-US')
            - gender: Voice gender (optional)
            - preview_url: URL to voice preview (optional)

        Raises:
            Exception: If listing fails
        """
        pass

    @abstractmethod
    def get_voice_info(self, voice_id: str) -> dict:
        """
        Get detailed information about a voice.

        Args:
            voice_id: ID of the voice

        Returns:
            Dictionary with voice information

        Raises:
            ValueError: If voice_id not found
            Exception: If request fails
        """
        pass

    @property
    @abstractmethod
    def provider_name(self) -> str:
        """
        Get the name of the TTS provider.

        Returns:
            Provider name string (e.g., 'ElevenLabs', 'Google TTS')
        """
        pass


class IVoiceCloningProvider(IVoiceProvider):
    """
    Extended interface for voice cloning capabilities.

    Adds methods for creating custom voices from audio samples.
    """

    @abstractmethod
    def clone_voice(
        self,
        name: str,
        audio_files: list[str],
        description: Optional[str] = None,
    ) -> str:
        """
        Clone a voice from audio samples.

        Args:
            name: Name for the cloned voice
            audio_files: List of paths to audio files for training
            description: Optional description of the voice

        Returns:
            Voice ID of the cloned voice

        Raises:
            ValueError: If audio files are invalid
            Exception: If cloning fails
        """
        pass

    @abstractmethod
    def delete_voice(self, voice_id: str) -> bool:
        """
        Delete a custom voice.

        Args:
            voice_id: ID of the voice to delete

        Returns:
            True if deletion was successful

        Raises:
            ValueError: If voice_id not found or is a default voice
            Exception: If deletion fails
        """
        pass
