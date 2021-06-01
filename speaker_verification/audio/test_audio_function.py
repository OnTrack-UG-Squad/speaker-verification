import pathlib
from os.path import join, abspath, dirname

import numpy as np

from speaker_verification.audio.audio import preprocess_wav
from speaker_verification.audio.voice_encoder import VoiceEncoder


def test_voice_encoder():
    fpath = join(abspath(dirname(__file__)), "input")
    fpath = pathlib.Path(fpath, "enrollment.flac"),
    wav = preprocess_wav(fpath)

    encoder = VoiceEncoder()
    embed = encoder.embed_utterance(wav)
    np.set_printoptions(precision=3, suppress=True)
    print(embed)
