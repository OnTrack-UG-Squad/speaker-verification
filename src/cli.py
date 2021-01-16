import argparse

parser = argparse.ArgumentParser(
         description="Process new user enrollment for speaker verification validation"
     )
     parser.add_argument(
         "--user-id",
         type=str,
         required=True,
         help="User identification number for new user.",
     )
     parser.add_argument(
         "--audiofile-path",
         type=str,
         required=True,
         help="Path to enrollment audio, required for baseline verification.",
     )

     parser.add_argument(
          "--port",
          type=int,
          default=5000,
          help="local port number to flask instance (default = 5000).",
      )

     args = parser.parse_args()

def process_new_user():
    args.user_id
    Popen(f"curl -X POST localhost:{port}/users -d \"user_id={user_id}\""
    Popen(f"curl -X POST localhost:{port}/users -d \"audio_file={audiofile_path}\""
    Popen(f"curl -X POST -F file=@./test.wav http://localhost:5000/file-upload"
    args.audiofile_path
    return 0

def put_user_en


