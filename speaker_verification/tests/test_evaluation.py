import pytest
import numpy as np
from os.path import join, abspath, dirname
import pathlib

from speaker_verification.model_evaluation import (
    MODEL_PATH,
    run_model_evaluation,
    batch_cosine_similarity,
)
from speaker_verification.deep_speaker.rescnn_model import DeepSpeakerModel


TEST_PATH = join(abspath(dirname(__file__)), "input")


def test_model_evaluation_scores():
    np.random.seed(123)
    model = DeepSpeakerModel()
    model.rescnn.load_weights(MODEL_PATH, by_name=True)
    audio_list = [
        pathlib.Path(TEST_PATH, "enrollment.flac"),
        pathlib.Path(TEST_PATH, "validation.flac"),
    ]
    results = []
    for audio_file in audio_list:
        if audio_file.is_file():
            results.append(run_model_evaluation(audio_file, model, raw_audio=True))

    s1_to_s1 = batch_cosine_similarity(results[0], results[1])
    is_above_cosine_threshold(s1_to_s1[0])


def is_above_cosine_threshold(input_value):
    assert input_value > np.float32(0.75)


@pytest.mark.parametrize("input_1", [np.arange(9).reshape(3, 3)])
@pytest.mark.parametrize("input_2", [np.arange(3)])
def test_batch_cosine_threshold(input_1, input_2):
    np.random.seed(123)
    np.testing.assert_allclose(batch_cosine_similarity(input_1, input_2), [5, 14, 23])
    

