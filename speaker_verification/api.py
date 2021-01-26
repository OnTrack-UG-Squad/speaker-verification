import os
import time
import pathlib
import pickle

from flask import Flask, abort, request, jsonify, g, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_httpauth import HTTPBasicAuth
import jwt
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash

from audio import NUM_FRAMES, SAMPLE_RATE, read_mfcc, sample_from_mfcc

"""This api script is currently not being used in the project,
   I will be keeping it as a working prototype for a RESTful service.
"""

UPLOAD_FOLDER = "./uploads"
ALLOWED_EXTENSIONS = {"mp3", "flac", "wav"}

# initialization
app = Flask(__name__)
app.config["SECRET_KEY"] = "the quick brown fox jumps over the lazy dog"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite"
app.config["SQLALCHEMY_COMMIT_ON_TEARDOWN"] = True

# extensions
db = SQLAlchemy(app)
auth = HTTPBasicAuth()


class InputAudioError(Exception):
    pass


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), index=True)
    password_hash = db.Column(db.String(128))

    def hash_password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_auth_token(self, expires_in=600):
        return jwt.encode(
            {"id": self.id, "exp": time.time() + expires_in},
            app.config["SECRET_KEY"],
            algorithm="HS256",
        )

    @staticmethod
    def verify_auth_token(token):
        try:
            data = jwt.decode(token, app.config["SECRET_KEY"], algorithms=["HS256"])
        except:
            return
        return User.query.get(data["id"])


@auth.verify_password
def verify_password(username_or_token, password):
    # first try to authenticate by token
    user = User.verify_auth_token(username_or_token)
    if not user:
        # try to authenticate with username/password
        user = User.query.filter_by(username=username_or_token).first()
        if not user or not user.verify_password(password):
            return False
    g.user = user
    return True


@app.route("/api/users", methods=["POST"])
def new_user():
    username = request.json.get("username")
    password = request.json.get("password")
    if username is None or password is None:
        abort(400)  # missing arguments
    if User.query.filter_by(username=username).first() is not None:
        abort(400)  # existing user
    user = User(username=username)
    user.hash_password(password)
    db.session.add(user)
    db.session.commit()
    return (
        jsonify({"username": user.username}),
        201,
        {"Location": url_for("get_user", id=user.id, _external=True)},
    )


@app.route("/api/users/<int:id>")
def get_user(id):
    user = User.query.get(id)
    if not user:
        abort(400)
    return jsonify({"username": user.username})


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/api/uploads", methods=["POST"])
@auth.login_required
def upload_file():
    # check if the post request has the file part
    id = g.user.username
    if "file" not in request.files:
        resp = jsonify({"message": "No file part in the request"})
        resp.status_code = 400
        return resp
    file_ = request.files["file"]
    if file_.filename == "":
        resp = jsonify({"message": "No file selected for uploading"})
        resp.status_code = 400
        return resp
    if file_ and allowed_file(file_.filename):
        filename = secure_filename(file_.filename)
        output_path = pathlib.Path(f"./api/uploads/{id}")
        output_path.mkdir(parents=True, exist_ok=True)

        resp = convert_input_to_mfcc(file_, output_path)
        # file.save(pathlib.Path(f"./api/uploads/{id}", f"{filename}"))
        return resp
    else:
        resp = jsonify({"message": "Allowed file types are mp3, wav and flac"})
        resp.status_code = 400
        return resp


@auth.login_required
def convert_input_to_mfcc(audio, output_path):
    try:
        if audio is not None:
            mfcc = sample_from_mfcc(read_mfcc(audio, SAMPLE_RATE), NUM_FRAMES)
            with open(pathlib.Path(output_path, f"{audio.filename}.pkl"), "wb") as pkl:
                pickle.dump(mfcc, pkl)

            return (
                jsonify(
                    {
                        "message": f"{audio.filename} successfully uploaded for {output_path}"
                    }
                ),
                201,
            )

    except InputAudioError:
        return jsonify({"message": f"Allowed file types are {ALLOWED_EXTENSIONS}"}), 400


@app.route("/api/token")
@auth.login_required
def get_auth_token():
    token = g.user.generate_auth_token(600)
    return jsonify({"token": token.decode("ascii"), "duration": 600})


@app.route("/api/resource")
@auth.login_required
def get_resource():
    return jsonify({"data": "Hello, %s!" % g.user.username})


if __name__ == "__main__":
    if not os.path.exists("db.sqlite"):
        db.create_all()
    app.run(debug=True)
