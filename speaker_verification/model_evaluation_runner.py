import argparse
from os.path import join, abspath, dirname
import csv
import pathlib
from random import seed

import numpy as np
import pytest

from rescnn_model import DeepSpeakerModel
from audio import NUM_FRAMES, NUM_FBANKS, SAMPLE_RATE, read_mfcc, sample_from_mfcc

model_path = join(abspath(dirname(__file__)), "models", "ResCNN_triplet_training_checkpoint_265.h5")

def run_VCSK_Corpus_data(speaker_1, speaker_2, to_csv):
    np.random.seed(123)
    seed(123)

    model = DeepSpeakerModel()
    model.rescnn.load_weights(model_path, by_name=True)
    dataset_path = (
        "../../datasets/VCTK_Corpus_Fileshare/VCTK_Corpus/wav48_silence_trimmed"
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
            audio_results.append(
                sample_from_mfcc(
                    read_mfcc(audio_file, SAMPLE_RATE), NUM_FRAMES
                )
            )

        else:
            return 0

    predict_001 = model.rescnn.predict(np.expand_dims(audio_results[0], axis=0))
    predict_002 = model.rescnn.predict(np.expand_dims(audio_results[1], axis=0))
    predict_003 = model.rescnn.predict(np.expand_dims(audio_results[2], axis=0))

    s1_to_s1 = batch_cosine_similarity(predict_001, predict_002)
    s1_to_s2 = batch_cosine_similarity(predict_001, predict_003)

    if to_csv == True:
        append_results_to_csv((speaker_1, speaker_2), (s1_to_s1, s1_to_s2))
    else:
        print(f"{speaker_1} and {speaker_2} complete")
        print(f"{speaker_1} baseline score: {s1_to_s1}")
        print(f"{speaker_1} and {speaker_2}  simularity score: {s1_to_s2}")

    results = [s1_to_s1, s1_to_s2]
    return results


def batch_cosine_similarity(x1, x2):
    """ https://en.wikipedia.org/wiki/Cosine_similarity """

    mul = np.multiply(x1, x2)
    s = np.sum(mul, axis=1)
    return s


def append_results_to_csv(names, scores):
    with open(r"precompiled_checks.csv", "a") as f:
        writer = csv.writer(f)
        writer.writerow([names[0], names[1], scores[0], scores[1]])


def test_VCSK_Corpus_speaker_scores():
    results = run_VCSK_Corpus_data("p225", "p226", False)

    np.testing.assert_allclose(results[0][0], np.float32(0.7129393))
    np.testing.assert_allclose(results[1][0], np.float32(0.28153613))


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
