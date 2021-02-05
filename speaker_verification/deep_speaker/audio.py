""" This script contains open source components
    from audio.py, developed by @philipperemy in
    the deep-speaker project.

    See the original project here:
    https://github.com/philipperemy/deep-speaker/
"""

import logging
import os
from glob import glob
from random import choice

import librosa
import numpy as np
from python_speech_features import fbank

logger = logging.getLogger(__name__)
SAMPLE_RATE = 16000
NUM_FRAMES = 300
NUM_FBANKS = 64


def sample_from_mfcc(mfcc, max_length):
    if mfcc.shape[0] >= max_length:
        r = choice(range(0, len(mfcc) - max_length + 1))
        s = mfcc[r : r + max_length]
    else:
        s = pad_mfcc(mfcc, max_length)
    return np.expand_dims(s, axis=-1)


def pad_mfcc(mfcc, max_length):
    if len(mfcc) < max_length:
        mfcc = np.vstack(
            (mfcc, np.tile(np.zeros(mfcc.shape[1]), (max_length - len(mfcc), 1)))
        )
    return mfcc


def audio_read(filename, sample_rate=SAMPLE_RATE):
    audio, sr = librosa.load(filename, sr=sample_rate, mono=True, dtype=np.float32)
    assert sr == sample_rate
    return audio


def read_mfcc(input_filename, sample_rate):
    audio = audio_read(input_filename, sample_rate)
    energy = np.abs(audio)
    silence_threshold = np.percentile(energy, 95)
    offsets = np.where(energy > silence_threshold)[0]
    audio_voice_only = audio[offsets[0] : offsets[-1]]
    mfcc = mfcc_fbank(audio_voice_only, sample_rate)
    return mfcc


def mfcc_fbank(signal: np.array, sample_rate: int):  # 1D signal array.
    # Returns MFCC with shape (num_frames, n_filters, 3).
    filter_banks, energies = fbank(signal, samplerate=sample_rate, nfilt=NUM_FBANKS)
    frames_features = normalize_frames(filter_banks)
    return np.array(frames_features, dtype=np.float32)


def normalize_frames(m, epsilon=1e-12):
    return [(v - np.mean(v)) / max(np.std(v), epsilon) for v in m]


def find_files(directory, ext="wav"):
    return sorted(glob(directory + f"/**/*.{ext}", recursive=True))


def ensures_dir(directory: str):
    if len(directory) > 0 and not os.path.exists(directory):
        os.makedirs(directory)
