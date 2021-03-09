from speaker_verification.deep_speaker.audio import NUM_FRAMES, SAMPLE_RATE, read_mfcc, sample_from_mfcc
from speaker_verification.model_evaluation import run_user_evaluation
from speaker_verification.sql_utils import establish_sqlite_db, create_db_table, insert_db_row, select_db_row


def validate_id(id):
    """assert that input id is castable to int and 9 characters long."""
    try:
        int(id)
        assert len(id) == 9

    except ValueError:
        print("User Input Not a Valid ID.")
        raise
    except AssertionError:
        print("User Input Not a Valid length. ID must have a length of 9.")
        raise


def enroll_new_user(args):
    """
    enroll_new_user requires a unique meric id with a length of 9 characters and a path to a
    wav/flac file of the users voice.

    Parameters
    ----------
    args : str
        Commandline arguments passed with argparse. Required arguments are args.id and args.audio_path
    """
    establish_sqlite_db(args.db_table)
    validate_id(args.id)
    mfcc = sample_from_mfcc(read_mfcc(args.audio_path, SAMPLE_RATE), NUM_FRAMES)
    insert_db_row(args.db_table, args.id, mfcc)


def validate_user(args):
    """
    validate_user retrives a user enrollment based on the args.id parameter and uses args.audio_path to
    accept an audio file as speaker input to verify against the id enrollment.

    Parameters
    ----------
    args : str
        Commandline arguments passed with argparse. Required arguments are args.id and args.audio_path
    """
    validate_id(args.id)
    user_row = select_db_row(args.db_table, args.id)
    mfcc = user_row[1]
    score = run_user_evaluation(mfcc, args.audio_path)
    print(f"User evaluation for {args.id} has a confidence of:")
    print(f"{round(score[0]*100, 2)}%")
