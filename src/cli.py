import argparse
from subprocess import Popen

parser = argparse.ArgumentParser(
         description="Process new user enrollment for speaker verification validation"
     )
parser.add_argument(
         "--username",
         type=str,
         required=True,
         help="User identifying name for a new user.",
     )
parser.add_argument(
          "--password",
          type=str,
          required=True,
          help="User identifying password for new user.",
      )
parser.add_argument(
         "--audio-path",
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
    try:
        enroll_user = Popen(["curl", "-i", "-X", "POST", "-H", "Content-Type: application/json", "-d", "\'{\"username\":\"{args.username}\",\"password\":\"{args.password}\"}\'", f"localhost:{args.port}/api/users"])
    except Exception:
        print("BAD USER ENROLLMENT")
    try:
        upload_file = Popen(["curl", "-u", f"{args.username}:{args.password}", "-X", "POST", "-F",  f"file=@{args.audio_path} http://localhost:5000/api/uploads"])
    except Exception:
        print("BAD UPLOAD OF FILE!")

if __name__ == "__main__":
    process_new_user()


    """

    curl -i -X POST -H "Content-Type: application/json" -d '{"username":"jacob","password":"python"}' http://127.0.0.1:5000/api/users

    curl -u aidan:python -X POST -F file=@./p225_012_mic1.flac http://localhost:5000/api/uploads
    """
