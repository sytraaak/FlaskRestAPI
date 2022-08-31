from flask import Flask
from flask_restful import Api, Resource, reqparse

app = Flask(__name__)
api = Api(app)

honzik_rez = 0
honzik_iss = 0
pepik_rez = 1
pepik_iss = 1

class User(Resource):
    def get(self, user_name, count):
        if count == "rezervace":
            return f"""{user_name}_rez**{eval(f"{user_name}_rez")}"""
        elif count == "vystaveno":
            return f"""{user_name}_iss**{eval(f"{user_name}_iss")}"""

    def post(self, video_id, name):
        return

#nastavím zdroj do API a cestu k němu - jako zdroj se zadává třída - každá třída může mít různé metody, potom si
# volám API přes requesty a definuju vždy cestu a následně taky metodu
api.add_resource(User, "/user/<string:user_name>/<string:count>")

if __name__ == "__main__":
    # spouští server, nspouštět na reálném serveru debug
    app.run(debug=True)
