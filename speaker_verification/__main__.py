import argparse
from speaker_verification import enroll_new_user, validate_user

if __name__ == "__main__":

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
