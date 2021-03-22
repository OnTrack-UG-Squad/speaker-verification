import argparse
from speaker_verification import enroll_new_user, validate_user


def add_enrollment_args(subparser):
    enrollment_parser = subparser.add_parser(
        "enroll",
        help="enroll help",
        description="Process new user enrolment for speaker verification",
    )
    enrollment_parser.set_defaults(func=enroll_new_user)

    enrollment_parser.add_argument(
        "--id",
        type=str,
        required=True,
        help="User identification for a new user.",
    )

    enrollment_parser.add_argument(
        "--audio-path",
        type=str,
        required=True,
        help="Path to enrollment audio, required for baseline verification.",
    )

    enrollment_parser.add_argument(
        "--db-table",
        type=str,
        default="users",
        help="Name of database table to contain user enrollment data.",
    )

    return enrollment_parser


def add_verification_args(subparser):
    validation_parser = subparser.add_parser(
        "validate",
        help="validate help",
        description="Validate user based off enrolment for speaker verification",
    )
    validation_parser.set_defaults(func=validate_user)

    validation_parser.add_argument(
        "-i",
        "--id",
        type=str,
        required=True,
        help="User identification for a registered user.",
    )

    validation_parser.add_argument(
        "-a",
        "--audio-path",
        type=str,
        required=True,
        help="Path to verification audio, required for verification against enrollment audio.",
    )

    validation_parser.add_argument(
        "--db-table",
        type=str,
        default="users",
        help="Name of database table to contain user validation data.",
    )

    return validation_parser


def main():
    parser = argparse.ArgumentParser(
        description="A CLI tool for enrollment and validation on registered users for speaker verification."
    )
    subparsers = parser.add_subparsers()

    enrollment_parser = add_enrollment_args(subparsers)
    validation_parser = add_verification_args(subparsers)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
