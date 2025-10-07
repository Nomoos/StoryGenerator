import os

from Generators.GVoice import VoiceMaker


def manual_voice_generation():
    maker = VoiceMaker()
    maker.generate_audio()
    maker.normalize_audio()


if __name__ == "__main__":
    manual_voice_generation()