"""
Audio Production Module - TTS Generation and Audio Normalization

This module provides functionality for:
1. Text-to-speech generation from scripts using ElevenLabs or OpenAI
2. Audio normalization to broadcast standards (LUFS)
3. Voice recommendation integration
4. Multi-format audio output
"""

import json
import logging
import subprocess
from dataclasses import dataclass, field, asdict
from datetime import datetime
from pathlib import Path
import tempfile

logger = logging.getLogger(__name__)


@dataclass
class AudioMetadata:
    """Metadata for generated audio."""
    duration_seconds: float
    sample_rate: int = 44100
    channels: int = 1  # Mono for voice
    bit_depth: int = 16
    lufs: float | None = None  # Loudness Units relative to Full Scale
    peak_db: float | None = None
    
    def to_dict(self) -> dict[str, object]:
        """Convert to dictionary."""
        return asdict(self)


@dataclass
class VoiceoverAudio:
    """Represents generated voiceover audio."""
    audio_id: str
    script_id: str
    content_text: str
    voice_gender: str
    voice_provider: str  # 'elevenlabs', 'openai', 'local'
    voice_id: str | None = None  # Provider-specific voice ID
    raw_path: str | None = None  # Path to raw TTS output
    normalized_path: str | None = None  # Path to normalized audio
    metadata: AudioMetadata = field(default_factory=lambda: AudioMetadata(0.0))
    generated_at: str = field(default_factory=lambda: datetime.now().isoformat())
    
    def to_dict(self) -> dict[str, object]:
        """Convert to dictionary."""
        data = asdict(self)
        data['metadata'] = self.metadata.to_dict()
        return data
    
    def to_json(self, indent: int = 2) -> str:
        """Convert to JSON string."""
        return json.dumps(self.to_dict(), indent=indent)


class TTSGenerator:
    """
    Generate text-to-speech audio from scripts.
    
    Supports multiple TTS providers (ElevenLabs, OpenAI TTS, local models)
    with voice selection based on demographics and content.
    """
    
    def __init__(
        self,
        provider: str = "elevenlabs",
        api_key: str | None = None,
        output_root: str | None = None
    ):
        """
        Initialize TTSGenerator.
        
        Args:
            provider: TTS provider ('elevenlabs', 'openai', 'local')
            api_key: API key for cloud providers
            output_root: Root directory for audio output
        """
        self.provider = provider
        self.api_key = api_key
        self.output_root = Path(output_root) if output_root else Path("Generator/audio")
        self._client = None
        
        logger.info(f"Initialized TTSGenerator with provider: {provider}")
    
    def _init_client(self) -> None:
        """Initialize TTS client based on provider."""
        if self._client is not None:
            return
        
        if self.provider == "elevenlabs":
            try:
                from elevenlabs.client import ElevenLabs
                self._client = ElevenLabs(api_key=self.api_key)
                logger.info("Initialized ElevenLabs client")
            except ImportError:
                logger.error("ElevenLabs not installed. Install with: pip install elevenlabs")
                raise
        elif self.provider == "openai":
            try:
                from openai import OpenAI
                self._client = OpenAI(api_key=self.api_key)
                logger.info("Initialized OpenAI TTS client")
            except ImportError:
                logger.error("OpenAI not installed. Install with: pip install openai")
                raise
        else:
            logger.warning(f"Provider {self.provider} not implemented, using mock")
    
    def generate_tts(
        self,
        script: dict[str, object],
        voice_gender: str = "female",
        voice_id: str | None = None,
        model: str = "eleven_turbo_v2"
    ) -> VoiceoverAudio:
        """
        Generate TTS audio from script.
        
        Args:
            script: Script dict with 'script_id', 'content', etc.
            voice_gender: 'male' or 'female'
            voice_id: Specific voice ID (provider-dependent)
            model: TTS model to use
        
        Returns:
            VoiceoverAudio object with generated audio
        """
        self._init_client()
        
        script_id = script.get('script_id', 'unknown')
        content = script.get('content', '')
        target_gender = script.get('target_gender', 'all')
        target_age = script.get('target_age', 'all')
        
        if not content:
            raise ValueError("Script content is empty")
        
        # Select voice
        if voice_id is None:
            voice_id = self._select_voice(voice_gender)
        
        logger.info(f"Generating TTS for script {script_id} with voice {voice_id}")
        
        # Generate audio
        audio_data = self._generate_audio(content, voice_id, model)
        
        # Save raw audio
        raw_path = self._save_raw_audio(
            audio_data,
            script_id,
            target_gender,
            target_age
        )
        
        # Get audio metadata
        metadata = self._get_audio_metadata(raw_path)
        
        audio = VoiceoverAudio(
            audio_id=f"{script_id}_tts",
            script_id=script_id,
            content_text=content[:100] + "..." if len(content) > 100 else content,
            voice_gender=voice_gender,
            voice_provider=self.provider,
            voice_id=voice_id,
            raw_path=str(raw_path),
            metadata=metadata
        )
        
        logger.info(f"Generated TTS audio: {raw_path} ({metadata.duration_seconds:.1f}s)")
        return audio
    
    def _select_voice(self, gender: str) -> str:
        """Select appropriate voice ID based on gender and provider."""
        # ElevenLabs voice IDs (popular voices)
        elevenlabs_voices = {
            'female': 'EXAVITQu4vr4xnSDxMaL',  # Bella - warm, friendly
            'male': 'TxGEqnHWrfWFTfGW9XjX'     # Josh - clear, professional
        }
        
        # OpenAI TTS voices
        openai_voices = {
            'female': 'nova',  # Friendly female voice
            'male': 'onyx'     # Deep male voice
        }
        
        if self.provider == "elevenlabs":
            return elevenlabs_voices.get(gender, elevenlabs_voices['female'])
        elif self.provider == "openai":
            return openai_voices.get(gender, openai_voices['female'])
        else:
            return f"{gender}_voice"
    
    def _generate_audio(self, text: str, voice_id: str, model: str) -> bytes:
        """Generate audio using the configured provider."""
        if self.provider == "elevenlabs":
            return self._generate_elevenlabs(text, voice_id, model)
        elif self.provider == "openai":
            return self._generate_openai(text, voice_id)
        else:
            # Mock for testing
            return b"MOCK_AUDIO_DATA"
    
    def _generate_elevenlabs(self, text: str, voice_id: str, model: str) -> bytes:
        """Generate audio using ElevenLabs."""
        try:
            audio_generator = self._client.text_to_speech.convert(
                voice_id=voice_id,
                text=text,
                model_id=model,
                output_format="mp3_44100_128"
            )
            
            # Collect audio chunks
            audio_data = b"".join(audio_generator)
            return audio_data
        except Exception as e:
            logger.error(f"ElevenLabs TTS error: {e}")
            raise
    
    def _generate_openai(self, text: str, voice_id: str) -> bytes:
        """Generate audio using OpenAI TTS."""
        try:
            response = self._client.audio.speech.create(
                model="tts-1-hd",  # or "tts-1" for faster/cheaper
                voice=voice_id,
                input=text,
                response_format="mp3"
            )
            return response.content
        except Exception as e:
            logger.error(f"OpenAI TTS error: {e}")
            raise
    
    def _save_raw_audio(
        self,
        audio_data: bytes,
        script_id: str,
        target_gender: str,
        target_age: str
    ) -> Path:
        """Save raw TTS audio to file."""
        output_dir = self.output_root / "tts" / target_gender / target_age / "raw"
        output_dir.mkdir(parents=True, exist_ok=True)
        
        output_file = output_dir / f"{script_id}.mp3"
        
        with open(output_file, 'wb') as f:
            f.write(audio_data)
        
        logger.debug(f"Saved raw audio: {output_file}")
        return output_file
    
    def _get_audio_metadata(self, audio_path: Path) -> AudioMetadata:
        """Extract audio metadata using ffprobe."""
        try:
            # Use ffprobe to get duration
            result = subprocess.run(
                [
                    'ffprobe',
                    '-v', 'error',
                    '-show_entries', 'format=duration',
                    '-of', 'default=noprint_wrappers=1:nokey=1',
                    str(audio_path)
                ],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode == 0:
                duration = float(result.stdout.strip())
                return AudioMetadata(
                    duration_seconds=duration,
                    sample_rate=44100,
                    channels=1
                )
        except (subprocess.TimeoutExpired, FileNotFoundError, ValueError) as e:
            logger.warning(f"Could not extract metadata: {e}")
        
        # Fallback: estimate based on file size (rough approximation)
        file_size = audio_path.stat().st_size
        # MP3 128kbps ≈ 16KB/s
        estimated_duration = file_size / (16 * 1024)
        return AudioMetadata(duration_seconds=estimated_duration)


class AudioNormalizer:
    """
    Normalize audio to broadcast standards.
    
    Applies LUFS (Loudness Units relative to Full Scale) normalization
    for consistent volume across videos. Standard: -14 LUFS for YouTube/TikTok.
    """
    
    def __init__(self, output_root: str | None = None):
        """
        Initialize AudioNormalizer.
        
        Args:
            output_root: Root directory for normalized audio output
        """
        self.output_root = Path(output_root) if output_root else Path("Generator/audio")
        logger.info("Initialized AudioNormalizer")
    
    def normalize_audio(
        self,
        audio: VoiceoverAudio,
        target_lufs: float = -14.0,
        true_peak: float = -1.0
    ) -> VoiceoverAudio:
        """
        Normalize audio to target LUFS level.
        
        Args:
            audio: VoiceoverAudio object with raw audio
            target_lufs: Target loudness in LUFS (default: -14.0 for social media)
            true_peak: True peak limit in dB (default: -1.0)
        
        Returns:
            Updated VoiceoverAudio with normalized path
        """
        if not audio.raw_path:
            raise ValueError("Audio must have raw_path set")
        
        raw_path = Path(audio.raw_path)
        if not raw_path.exists():
            raise FileNotFoundError(f"Raw audio file not found: {raw_path}")
        
        logger.info(f"Normalizing audio {audio.audio_id} to {target_lufs} LUFS")
        
        # Measure current loudness
        current_lufs = self._measure_lufs(raw_path)
        logger.info(f"Current LUFS: {current_lufs:.1f}")
        
        # Calculate volume adjustment
        adjustment_db = target_lufs - current_lufs
        
        # Create normalized output path
        script_id = audio.script_id
        target_gender = raw_path.parent.parent.parent.name
        target_age = raw_path.parent.parent.name
        
        output_dir = self.output_root / "normalized" / target_gender / target_age
        output_dir.mkdir(parents=True, exist_ok=True)
        
        normalized_path = output_dir / f"{script_id}_normalized.mp3"
        
        # Apply normalization using FFmpeg loudnorm filter
        self._apply_loudnorm(
            input_path=raw_path,
            output_path=normalized_path,
            target_lufs=target_lufs,
            true_peak=true_peak
        )
        
        # Update audio object
        audio.normalized_path = str(normalized_path)
        
        # Measure final loudness
        final_lufs = self._measure_lufs(normalized_path)
        audio.metadata.lufs = final_lufs
        
        logger.info(
            f"Normalized audio saved: {normalized_path} "
            f"(adjusted {adjustment_db:+.1f}dB, final LUFS: {final_lufs:.1f})"
        )
        
        return audio
    
    def _measure_lufs(self, audio_path: Path) -> float:
        """Measure audio loudness in LUFS using ffmpeg."""
        try:
            # Use ffmpeg loudnorm filter in measurement mode
            result = subprocess.run(
                [
                    'ffmpeg',
                    '-i', str(audio_path),
                    '-af', 'loudnorm=print_format=json',
                    '-f', 'null',
                    '-'
                ],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            # Parse JSON output from stderr
            output = result.stderr
            
            # Extract JSON from output
            json_start = output.rfind('{')
            json_end = output.rfind('}') + 1
            
            if json_start >= 0 and json_end > json_start:
                json_str = output[json_start:json_end]
                data = json.loads(json_str)
                
                # Get input integrated loudness
                input_i = float(data.get('input_i', '-23.0'))
                return input_i
            
        except (subprocess.TimeoutExpired, FileNotFoundError, ValueError, json.JSONDecodeError) as e:
            logger.warning(f"Could not measure LUFS: {e}")
        
        # Return default if measurement fails
        return -23.0  # Typical default
    
    def _apply_loudnorm(
        self,
        input_path: Path,
        output_path: Path,
        target_lufs: float,
        true_peak: float
    ):
        """Apply loudness normalization using FFmpeg."""
        try:
            # Two-pass loudnorm for best results
            # First pass: analyze
            result = subprocess.run(
                [
                    'ffmpeg',
                    '-i', str(input_path),
                    '-af', f'loudnorm=print_format=json:I={target_lufs}:TP={true_peak}',
                    '-f', 'null',
                    '-'
                ],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            # Parse first pass results
            output = result.stderr
            json_start = output.rfind('{')
            json_end = output.rfind('}') + 1
            
            if json_start >= 0 and json_end > json_start:
                json_str = output[json_start:json_end]
                stats = json.loads(json_str)
                
                # Second pass: apply normalization
                measured_i = stats.get('input_i', '-23.0')
                measured_tp = stats.get('input_tp', '-5.0')
                measured_lra = stats.get('input_lra', '7.0')
                measured_thresh = stats.get('input_thresh', '-34.0')
                
                subprocess.run(
                    [
                        'ffmpeg',
                        '-i', str(input_path),
                        '-af', (
                            f'loudnorm=I={target_lufs}:TP={true_peak}:'
                            f'measured_I={measured_i}:'
                            f'measured_TP={measured_tp}:'
                            f'measured_LRA={measured_lra}:'
                            f'measured_thresh={measured_thresh}:'
                            'print_format=summary'
                        ),
                        '-ar', '44100',
                        '-c:a', 'libmp3lame',
                        '-b:a', '128k',
                        str(output_path)
                    ],
                    capture_output=True,
                    timeout=60,
                    check=True
                )
                
                logger.debug(f"Applied loudnorm: {input_path} -> {output_path}")
            else:
                # Fallback: simple normalization
                logger.warning("Could not parse loudnorm stats, using simple normalization")
                subprocess.run(
                    [
                        'ffmpeg',
                        '-i', str(input_path),
                        '-af', f'loudnorm=I={target_lufs}:TP={true_peak}',
                        '-ar', '44100',
                        '-c:a', 'libmp3lame',
                        '-b:a', '128k',
                        str(output_path)
                    ],
                    capture_output=True,
                    timeout=60,
                    check=True
                )
        
        except (subprocess.TimeoutExpired, subprocess.CalledProcessError, FileNotFoundError) as e:
            logger.error(f"Loudness normalization failed: {e}")
            raise


# Convenience function for complete audio production workflow
def produce_audio(
    script: dict[str, object],
    tts_provider: str = "elevenlabs",
    api_key: str | None = None,
    voice_gender: str = "female",
    voice_id: str | None = None,
    target_lufs: float = -14.0,
    output_root: str | None = None
) -> VoiceoverAudio:
    """
    Complete audio production workflow: TTS generation + normalization.
    
    Args:
        script: Script dict to convert to audio
        tts_provider: TTS provider ('elevenlabs', 'openai')
        api_key: API key for provider
        voice_gender: 'male' or 'female'
        voice_id: Specific voice ID (optional)
        target_lufs: Target loudness level (default: -14.0)
        output_root: Root directory for output
    
    Returns:
        VoiceoverAudio with both raw and normalized audio
    """
    # Generate TTS
    generator = TTSGenerator(
        provider=tts_provider,
        api_key=api_key,
        output_root=output_root
    )
    audio = generator.generate_tts(
        script=script,
        voice_gender=voice_gender,
        voice_id=voice_id
    )
    
    # Normalize audio
    normalizer = AudioNormalizer(output_root=output_root)
    audio = normalizer.normalize_audio(audio, target_lufs=target_lufs)
    
    # Save metadata
    if output_root:
        metadata_dir = Path(output_root) / "metadata"
        metadata_dir.mkdir(parents=True, exist_ok=True)
        metadata_file = metadata_dir / f"{audio.audio_id}.json"
        
        with open(metadata_file, 'w', encoding='utf-8') as f:
            f.write(audio.to_json())
        
        logger.info(f"Saved audio metadata: {metadata_file}")
    
    return audio
