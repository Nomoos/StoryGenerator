# VoiceOverGenerator

Audio production, voice synthesis, and voice recommendation.

## Purpose

Handles all voice and audio-related functionality:
- Voice recommendation based on content
- Text-to-speech generation
- Audio normalization
- Voice cloning utilities

## Modules

- **voice_recommendation.py**: Recommend voices for content
  - `VoiceRecommender`: Match voices to content and audience

- **audio_production.py**: TTS generation and normalization
  - `AudioProducer`: Generate and normalize audio
  - `AudioNormalizer`: Normalize to broadcast standards

- **voice_cloning.py**: Voice cloning utilities
  - `VoiceCloner`: Clone and manage voice profiles

## Usage

```python
from PrismQ.VoiceOverGenerator.voice_recommendation import VoiceRecommender
from PrismQ.VoiceOverGenerator.audio_production import AudioProducer

# Recommend voice
recommender = VoiceRecommender()
voice = recommender.recommend_voice(content, target_gender="female")

# Generate audio
producer = AudioProducer()
audio_path = producer.generate_audio(script, voice_id=voice['voice_id'])
```
