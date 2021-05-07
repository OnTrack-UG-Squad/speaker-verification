import argparse
import csv
import logging
import pathlib
from os.path import join, abspath, dirname

import numpy as np

from speaker_verification.deep_speaker.audio import (
    NUM_FRAMES,
    SAMPLE_RATE,
    read_mfcc,
    sample_from_mfcc,
)
from speaker_verification.deep_speaker.rescnn_model import DeepSpeakerModel
from speaker_verification.utils.logger import SpeakerVerificationLogger

MODEL_PATH = join(
    abspath(dirname(__file__)), "models", "ResCNN_triplet_training_checkpoint_265.h5"
)

logger = SpeakerVerificationLogger(name=__file__)
logger.setLevel(logging.INFO)


def run_VCSK_Corpus_data(speaker_1, speaker_2, to_csv, dataset_path):
    np.random.seed(123)

    model = DeepSpeakerModel()
    model.rescnn.load_weights(MODEL_PATH, by_name=True)
    audio_list = [
        pathlib.Path(f"{dataset_path}/{speaker_1}/{speaker_1}_004_mic1.flac"),
        pathlib.Path(f"{dataset_path}/{speaker_1}/{speaker_1}_008_mic1.flac"),
        pathlib.Path(f"{dataset_path}/{speaker_2}/{speaker_2}_012_mic1.flac"),
    ]

    audio_results = []
    for audio_file in audio_list:
        logger.info(f"audio file: {audio_file}")
        if audio_file.is_file():
            audio_results.append(run_model_evaluation(audio_file, model, raw_audio=True))

        else:
            return 0

    s1_to_s1 = batch_cosine_similarity(audio_results[0], audio_results[1])
    s1_to_s2 = batch_cosine_similarity(audio_results[0], audio_results[2])

    if to_csv is True:
        append_results_to_csv((speaker_1, speaker_2), (s1_to_s1, s1_to_s2))
    else:
        logger.info(f"{speaker_1} and {speaker_2} complete")
        logger.info(f"{speaker_1} baseline score: {s1_to_s1}")
        logger.info(f"{speaker_1} and {speaker_2}  simularity score: {s1_to_s2}")


def run_model_evaluation(audio_input, model, raw_audio=False):
    """run_model_evaluation.

    Parameters
    ----------
    audio_input : str, Path-like
        Path to audio input for evaluation on prediction value.
    model : DeepSpeakerModel
        Instantiated model with required weights for speaker verification.
    raw_audio : bool
        Boolean value on whether the input audio path is mfcc or raw wav/flac.
    """
    if raw_audio is True:
        mfcc = sample_from_mfcc(read_mfcc(audio_input, SAMPLE_RATE), NUM_FRAMES)
    else:
        mfcc = audio_input
    prediction = model.rescnn.predict(np.expand_dims(mfcc, axis=0))
    return prediction


def run_user_evaluation(enrolment_mfcc, input_audio):
    """run_user_evaluation.

    Instanstiate project model and run evaulation on parameter inputs.

    Parameters
    ----------
    enrolment_mfcc : numpy.array
        MFCC array from sqlite user table for model evaluation.
    input_audio : str, Path-like
        Path to audio input for evaluation on prediction value.
    """
    model = DeepSpeakerModel()
    model.rescnn.load_weights(MODEL_PATH, by_name=True)
    enrolment_evaluation = run_model_evaluation(enrolment_mfcc, model)
    input_evaluation = run_model_evaluation(input_audio, model, raw_audio=True)

    return batch_cosine_similarity(enrolment_evaluation, input_evaluation)


def batch_cosine_similarity(x1, x2):
    """ https://en.wikipedia.org/wiki/Cosine_similarity """

    mul = np.multiply(x1, x2)
    s = np.sum(mul, axis=1)
    return s


def append_results_to_csv(names, scores):
    with open(r"precompiled_checks.csv", "a") as f:
        writer = csv.writer(f)
        writer.writerow([names[0], names[1], scores[0], scores[1]])


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Process speaker recognition on audio files from 2 different speakers"
    )
    parser.add_argument(
        "--speaker-1",
        type=str,
        default="p255",
        help="Name of the folder for first (baseline) speaker.",
    )
    parser.add_argument(
        "--speaker-2",
        type=str,
        default="p226",
        help="Name of the folder for second speaker.",
    )
    parser.add_argument(
        "--run_all",
        type=bool,
        default=False,
        help="Run speaker recognition for all known subjects.",
    )
    parser.add_argument(
        "--to_csv", type=bool, default=False, help="Append all results to csv file."
    )
    args = parser.parse_args()
    dataset_path = "INSERT_PATH_HERE"
    if args.run_all is True:
        for i in range(255, 360):
            run_VCSK_Corpus_data(f"p{i}", f"p{i + 1}", args.to_csv, dataset_path)

    else:
        run_VCSK_Corpus_data(args.speaker_1, args.speaker_2, args.to_csv, dataset_path)
