import argparse

from audio import NUM_FRAMES, SAMPLE_RATE, read_mfcc, sample_from_mfcc
from model_evaluation_runner import run_user_evaluation
from sql_utils import create_db_table, insert_db_row, select_db_row


def validate_id(id):
    """assert that input id is castable to int and 9 characters long."""
    try:
        val = int(id)
        assert len(id) == 9

    except ValueError:
        print("User Input Not a Valid ID.")
        raise
    except AssertionError:
        print("User Input Not a Valid length. ID must have a length of 9.")
        raise


def enroll_new_user(args):
    validate_id(args.id)
    mfcc = sample_from_mfcc(read_mfcc(args.audio_path, SAMPLE_RATE), NUM_FRAMES)
    insert_db_row("users", args.id, mfcc)


def validate_user(args):
    validate_id(args.id)
    user_row = select_db_row("users", args.id)
    mfcc = user_row[1]
    score = run_user_evaluation(mfcc, args.audio_path)
    print("score: ", score)


parser = argparse.ArgumentParser(
    description="A cli tool for enrolling and running speaker verification on registered users."
)

parser.add_argument(
    "--id", type=str, required=True, help="User identification for a new user.",
)

parser.add_argument(
    "--audio-path",
    type=str,
    required=True,
    help="Path to enrollment audio, required for baseline verification.",
)

subparsers = parser.add_subparsers()

enrollment_parser = subparsers.add_parser(
    "enroll", help="Process new user enrolment for speaker verification"
)
enrollment_parser.set_defaults(func=enroll_new_user)

validation_parser = subparsers.add_parser(
    "validate", help="Validate user based off enrolment for speaker verification"
)
validation_parser.set_defaults(func=validate_user)

args = parser.parse_args()
args.func(args)
