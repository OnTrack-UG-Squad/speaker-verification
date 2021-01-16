import os
import urllib.request
from flask import Flask, flash, request, redirect, url_for, send_from_directory, jsonify
from werkzeug.utils import secure_filename
from flask_restful import reqparse, abort, Api, Resource


UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = {'mp3', 'flac', 'wav'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
api = Api(app)

USERS = {
    'id1' : {
                'audio_file': "mfcc obj",
                'mfcc': "path/to/mfcc"
            }
}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/file-upload', methods=['POST'])
def upload_file():
	# check if the post request has the file parti
	if 'file' not in request.files:
		resp = jsonify({'message' : 'No file part in the request'})
		resp.status_code = 400
		return resp
	file = request.files['file']
	if file.filename == '':
		resp = jsonify({'message' : 'No file selected for uploading'})
		resp.status_code = 400
		return resp
	if file and allowed_file(file.filename):
		filename = secure_filename(file.filename)
		file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
		resp = jsonify({'message' : f'{filename} File successfully uploaded'})
		resp.status_code = 201
		return resp
	else:
		resp = jsonify({'message' : 'Allowed file types are txt, pdf, png, jpg, jpeg, gif'})
		resp.status_code = 400
		return resp


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

def check_if_user_exists(user_id):
    if user_id not in USERS:
        abort(404, message="User {} doesn't exist".format(user_id))


@app.route('/file-upload', methods=['POST'])
def upload_file(self, user_id):
    # check if the post request has the file part
    if 'file' not in request.files:
        resp = jsonify({'message' : 'No file part in the request'})
        resp.status_code = 400
        return resp
    file = request.files['file']
    if file.filename == '':
        resp = jsonify({'message' : 'No file selected for uploading'})
        resp.status_code = 400
        return resp
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], f"{user_id}-{filename}"))
        resp = jsonify({'message' : f'{filename} File successfully uploaded'})
        resp.status_code = 201
        return resp
    else:
        resp = jsonify({'message' : 'Allowed file types are txt, pdf, png, jpg, jpeg, gif'})
        resp.status_code = 400
        return resp

parser = reqparse.RequestParser()
parser.add_argument('user_id')
parser.add_argument('audio_file')
parser.add_argument('mfcc')

class User(Resource):
    def get(self, user_id):
        check_if_user_exists(user_id)
        return USERS[user_id]

    def delete(self, user_id):
        check_if_user_exists(user_id)
        del USERS[user_id]
        return '', 204

    def put(self, user_id):
        args = parser.parse_args()
        task = {
                'audio_file': args['audio_file'],
                'mfcc': "path/to/pickle_file"
               }
        USERS[user_id] = task
        return task, 201

#    @app.route('/file-upload', methods=['POST'])
#    def upload_file(self, user_id):
#         # check if the post request has the file part
#         if 'file' not in request.files:
#                 resp = jsonify({'message' : 'No file part in the request'})
##                 resp.status_code = 400
#                 return resp
#         file = request.files['file']
#         if file.filename == '':
#                 resp = jsonify({'message' : 'No file selected for uploading'})
#                 resp.status_code = 400
#                 return resp
#         if file and allowed_file(file.filename):
#                 filename = secure_filename(file.filename)
#                 file.save(os.path.join(app.config['UPLOAD_FOLDER'], f"{user_id}-{filename}"))
#                 resp = jsonify({'message' : f'{filename} File successfully uploaded'})
#                 resp.status_code = 201
#                 return resp
#         else:
#                 resp = jsonify({'message' : 'Allowed file types are txt, pdf, png, jpg, jpeg, gif'})
#                 resp.status_code = 400
#                 return resp


class UserList(Resource):
    def get(self):
        return USERS

    def post(self):
        args = parser.parse_args()
        # revist later as this info should not be depending of user input
        #user_id = int(max(USERS.keys()).lstrip('id')) + 1
        #user_id = 'id%i' % user_id
        user_id = args['user_id']
        USERS[user_id] = {
            'audio_file': args['audio_file'],
            'mfcc': "path/to/pickle_file"
            }
        return USERS[user_id], 201

"""Setup the Api resource routing here"""
api.add_resource(UserList, '/users')
api.add_resource(User, '/users/<user_id>')

if __name__ == '__main__':
    app.run(debug=True)
