import argparse
from os.path import join, abspath, dirname
import csv
import pathlib
from random import seed

import numpy as np
import pytest

from speaker_verification.audio import NUM_FBANKS, NUM_FRAMES, SAMPLE_RATE, read_mfcc, sample_from_mfcc
from speaker_verification.rescnn_model import DeepSpeakerModel


MODEL_PATH = join(abspath(dirname(__file__)), "models", "ResCNN_triplet_training_checkpoint_265.h5")

def run_VCSK_Corpus_data(speaker_1, speaker_2, to_csv):
    np.random.seed(123)
    seed(123)

    model = DeepSpeakerModel()
    model.rescnn.load_weights(MODEL_PATH, by_name=True)
    dataset_path = (
        "/home/aidan/dev/machine_learning/datasets/VCTK_Corpus_Fileshare/VCTK_Corpus/wav48_silence_trimmed/"
    )
    audio_list = [
        pathlib.Path(f"{dataset_path}/{speaker_1}/{speaker_1}_004_mic1.flac"),
        pathlib.Path(f"{dataset_path}/{speaker_1}/{speaker_1}_008_mic1.flac"),
        pathlib.Path(f"{dataset_path}/{speaker_2}/{speaker_2}_012_mic1.flac"),
    ]

    audio_results = []
    for audio_file in audio_list:
        print(f"audio file: {audio_file}")
        if audio_file.is_file():
            audio_results.append(run_model_evaluation(audio_file, model, raw_audio=True))

        else:
            return 0

    s1_to_s1 = batch_cosine_similarity(audio_results[0], audio_results[1])
    s1_to_s2 = batch_cosine_similarity(audio_results[0], audio_results[2])

    if to_csv == True:
        append_results_to_csv((speaker_1, speaker_2), (s1_to_s1, s1_to_s2))
    else:
        print(f"{speaker_1} and {speaker_2} complete")
        print(f"{speaker_1} baseline score: {s1_to_s1}")
        print(f"{speaker_1} and {speaker_2}  simularity score: {s1_to_s2}")


def run_model_evaluation(audio_input, model, raw_audio=False):
    if raw_audio == True:
        mfcc = sample_from_mfcc(read_mfcc(audio_input, SAMPLE_RATE), NUM_FRAMES)
    else:
        mfcc = audio_input
    prediction = model.rescnn.predict(np.expand_dims(mfcc, axis=0))
    return prediction


def run_user_evaluation(enrolment_mfcc, input_audio):
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

    if args.run_all == True:
        for i in range(255, 360):
            run_VCSK_Corpus_data(f"p{i}", f"p{i+1}", args.to_csv)

    else:
        run_VCSK_Corpus_data(args.speaker_1, args.speaker_2, args.to_csv)
