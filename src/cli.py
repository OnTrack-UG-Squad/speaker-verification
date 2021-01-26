import argparse
from subprocess import Popen
import sqlite3
import numpy as np
import io

from model_evaluation_runner import run_user_evaluation
from audio import sample_from_mfcc, read_mfcc, SAMPLE_RATE, NUM_FRAMES
from sql_utils import select_db_row, insert_db_row, create_db_table


def enroll_new_user(args):
    mfcc = sample_from_mfcc(read_mfcc(args.audio_path, SAMPLE_RATE), NUM_FRAMES)
    current_user = {"id": args.id, "mfcc": mfcc}
    insert_db_row("users", current_user["id"], current_user["mfcc"])


def validate_user(args):
    user_row = select_db_row("users", args.id)
    mfcc = user_row[1]
    score = run_user_evaluation(mfcc, args.audio_path)


parser = argparse.ArgumentParser(
    description="Process new user enrollment for speaker verification validation"
)

parser.add_argument(
    "--id", type=str, required=True, help="User identifying name for a new user.",
)
parser.add_argument(
    "--password", type=str, help="User identifying password for new user.",
)
parser.add_argument(
    "--audio-path",
    type=str,
    required=True,
    help="Path to enrollment audio, required for baseline verification.",
)

subparsers = parser.add_subparsers()

enrollment_parser = subparsers.add_parser(
    "enrollment", help="Process new user enrollment for speaker verification"
)
enrollment_parser.set_defaults(func=enroll_new_user)

validation_parser = subparsers.add_parser(
    "validate", help="Validate user based off enrollment for speaker verification"
)
validation_parser.set_defaults(func=validate_user)

args = parser.parse_args()
args.func(args)
