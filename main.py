from flask import Flask
from flask_restful import Api, Resource
from flask import request
from flask import send_file
from setter import setter
from user_already import user_already
from users import *

app = Flask(__name__)
api = Api(app)

users_in_work = []

class User(Resource):
    def get(self):
        global users_in_work
        query_args = request.args
        query_keys = [key for key in query_args.keys()]
        url = request.url
        url_root = request.url_root
        url_path = request.path
        print(f"{url} {url_root} {url_path}")

        # POST METODY
        if "in_work" in query_keys:
            users_in_work = query_args["in_work"].split(";")
            return users_in_work

        # GET METODY
        # VRACÍ VŠECHNY EXISTUJÍCÍ UŽIVATELE - VE SMARTBUTTONS SE VYTVÁŘÍ SEZNAM, ZE KTERÉHO VYBÍRÁ UŽIVATEL KDO JE V PRÁCI
        if url == f"{url_root}users":
            return all_users()

        # prochází uživatele users_in_work, a dle podmínek vyhodnocuje, kdo má nejméně daného typu
        # VRACÍ CELÉ JMÉNO UŽIVATELE ABY MOHL BÝT SPUŠTĚN SMARTBUTTON STEJNÉHO JMÉNA
        if "HTE" in query_keys:
            hte = query_args["HTE"]
            prgt = query_args["PRGT"]
            email = query_args["EMAIL"].lower()
            segments = int(query_args["SEGMENTS"])
            segment_status = query_args["SEGMENT_STATUS"]
            temp_users = {}
            # pokud je lowcost
            if segment_status in ["AK", "BK"]:
                # pokud nemá uživatele == if
                if "STUDENT" not in prgt:
                    return setter(users_in_work, temp_users, "lowcost")
                # pokud již má uživatele
                else:
                    return user_already(prgt, "lowcost")
            # pokud není lowcost
            else:
                # zrušena a není přiřazena
                if segments == 0 and "STUDENT" not in prgt:
                    return setter(users_in_work, temp_users, "canceled")
                # nezrušena a nepřiřazena a není fraud
                elif "STUDENT" not in prgt and email not in fraud_emails():
                    # letenka
                    if hte == "True":
                        return setter(users_in_work, temp_users, "iss")
                    # rezervace
                    elif hte == "False":
                        return setter(users_in_work, temp_users, "rez")
                # je podeřelý e-mail
                elif email in fraud_emails():
                    return setter(users_in_work, temp_users, "fraud")
                # je již přiřazena a nejedná se o lowcost
                else:
                    return user_already(prgt, hte)

api.add_resource(User, "/users")

class Stats(Resource):
    def get(self):
        return statistics()

api.add_resource(Stats, "/stats")

class DatabaseStats(Resource):
    def get(self):
        query_args = request.args
        start = query_args["start"]
        end = query_args["end"]
        return filter_database(start, end)

api.add_resource(DatabaseStats, "/databasestats")

class StatisticsByDate(Resource):
    def get(self):
        query_args = request.args
        start = query_args["start"]
        end = query_args["end"]
        return filter_by_date(start, end)

api.add_resource(StatisticsByDate, "/statisticsbydate")

class StatsSave(Resource):
    def get(self):
        save_stats()
        return ["Statistiky uloženy do databáze"]

api.add_resource(StatsSave, "/statssave")

class SaveMorningStats(Resource):
    def get(self):
        save_morning_stats()
        return ["Ranní statistiky uloženy do databáze"]

api.add_resource(SaveMorningStats, "/savemorningstats")

class AddFraud(Resource):
    def get(self):
        query_args = request.args
        fraud_email = query_args["fraud_email"]
        return add_fraud(fraud_email)

api.add_resource(AddFraud, "/addfraud")

class ShowFraud(Resource):
    def get(self):
        return fraud_emails()

api.add_resource(ShowFraud, "/showfraud")

class DelFraud(Resource):
    def get(self):
        query_args = request.args
        fraud_email = query_args["fraud_email"]
        return del_fraud(fraud_email)

api.add_resource(DelFraud, "/delfraud")

class AddUser(Resource):
    def get(self):
        query_args = request.args
        password = int(query_args["password"])
        new_user = query_args["new_user"].lower().title()
        new_svcb = int(query_args["new_svcb"])
        return add_user(new_user, new_svcb, password)

api.add_resource(AddUser, "/adduser")

class DeleteUser(Resource):
    def get(self):
        query_args = request.args
        password = int(query_args["password"])
        del_user = query_args["del_user"].lower().title()
        return delete_user(del_user, password)

api.add_resource(DeleteUser, "/deluser")

class QueueCountAdd(Resource):
    def get(self):
        query_args = request.args
        queue_count = query_args["Q_COUNT"]
        for count in queue_count.split(" "):
            if count.startswith("."):
                reservation_on_queue = count[-3:].strip(".")
        return queue_80_add(reservation_on_queue)

api.add_resource(QueueCountAdd, "/queuecountadd")

class QueueCountCheck(Resource):
    def get(self):
        return queue_80_check()

api.add_resource(QueueCountCheck, "/queuecountcheck")

class QueueCount(Resource):
    def get(self):
        query_args = request.args
        queue_count = query_args["Q_COUNT"]
        for count in queue_count.split(" "):
            if count.startswith("."):
                reservation_on_queue = count[-3:].strip(".")
        return [reservation_on_queue]

api.add_resource(QueueCount, "/queuecount")

@app.route('/download')
def download_file():
    query_args = request.args
    start = query_args["start"]
    end = query_args["end"]
    filter_by_date(start, end)
    path = "temporary_data/filtered_statistics.xls"
    return send_file(path, as_attachment=True)


if __name__ == "__main__":
    #todo debug local
    # app.run(debug=True)
    # neprodukční server
    app.run(debug=True, host="0.0.0.0", port=8080)


