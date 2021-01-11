from flask import Flask
from flask_restful import reqparse, abort, Api, Resource

app = Flask(__name__)
api = Api(app)

USERS = {
    'id1' : {'enrollment': "mfcc obj"}
}

def check_if_user_exists(user_id):
    if user_id not in USERS:
        abort(404, message="User {} doesn't exist".format(user_id))

parser = reqparse.RequestParser()
parser.add_argument('enrollment')

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
        task = {'task': args['task']}
        TODOS[todo_id] = task
        return task, 201


class UserList(Resource):
    def get(self):
        return USERS

    def post(self):
        args = parser.parse_args()
        user_id = int(max(USERS.keys()).lstrip('id')) + 1
        user_id = 'id%i' % user_id
        USERS[user_id] = {'enrollment': args['enrollment']}
        return USERS[user_id], 201

"""Setup the Api resource routing here"""
api.add_resource(UserList, '/users')
api.add_resource(User, '/users/<user_id>')


if __name__ == '__main__':
    app.run(debug=True)
