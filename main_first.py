from flask import Flask
from flask_restful import Api, Resource, reqparse

app = Flask(__name__)
api = Api(app)

user_put_args = reqparse.RequestParser()
user_put_args.add_argument("age", type=int, help="Age is required", required=True)
user_put_args.add_argument("sex", type=str, help="Sex is required", required=True)
user_put_args.add_argument("nickname", type=str, help="Nickname is required", required=True)

users = {"Honzik": {"nickname": "sytrak", "age": 15, "sex": "male"}}

class Users(Resource):
    def get(self, name):
        return f"{name}: {users[name]}"

    def put(self, name):
        args = user_put_args.parse_args()
        users[name] = args

api.add_resource(Users, "/users/<string:name>")

class UserList(Resource):
    def get(self):
        return f"""Počet uživatelů: {len(users)}\nSeznam uživatelů: {users}\n{60*"*"}"""

api.add_resource(UserList, "/users")

if __name__ == "__main__":
    # spouští server, nspouštět na reálném serveru debug
    app.run(debug=True)
