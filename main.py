from flask import Flask, request
from flask_restful import Api, Resource, reqparse

app = Flask(__name__)
api = Api(app)

video_put_args = reqparse.RequestParser()
video_put_args.add_argument("name", type=str, help="Name of the video is required", required=True)
video_put_args.add_argument("views", type=str, help="Views of the video is required", required=True)
video_put_args.add_argument("likes", type=str, help="Likes of the video is required", required=True)

videos = {}

#vytvořím třídu, která je Resource
class Video(Resource):
    def get(self, video_id):
        return videos[video_id]

    def put(self, video_id):
        args = video_put_args.parse_args()
        videos[video_id] = args
        return videos[video_id], 201

#nastavím zdroj do API a cestu k němu - jako zdroj se zadává třída - každá třída může mít různé metody, potom si
# volám API přes requesty a definuju vždy cestu a následně taky metodu
api.add_resource(Video, "/video/<int:video_id>")


if __name__ == "__main__":
    # spouští server, nspouštět na reálném serveru debug
    app.run(debug=True)
