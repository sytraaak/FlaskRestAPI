from flask import Flask
from flask_restful import Api, Resource
from flask import request

app = Flask(__name__)
api = Api(app)

users = {"Veronika Lolova": {"iss": 0, "rez": 0}, "Anna Pospisilova": {"iss": 0, "rez": 0}, "Anna Zemanova": {"iss": 0, "rez": 0}}
users_in_work = []

class User(Resource):
    #todo resetování bych mohl vyřešit na základě porovnání self.date s today, které budou poskytovat SmartButtons a zde bude uloženo poslední datum
    #todo vyhodnotit, zda se nejedná o kradače - list mailů - tyto rezervace by se vůbec nezapočítávali do rozhozu i přes to, že budou rozhozeny, bude např vrace příznak kradač
    #todo časem můžu přejit k nějakému analyzátoru textu, který bude vyhodnocovat *VR případně další věci, co se dají zautomatizovat (např. duplicity apod.)
    #todo nutno vyřešit, pokud bude chtít hodit někdo konkrétní počet nějakému zaměstnanci
    #todo kontrola mobilní aplikace a podobných hovadin, zda je vyhodnocování správně - mobilní app vyřešena přes tel číslo
    #todo nevím jak vyřešit ukládání dat do databáze
    #todo rovnou mazat propadlé rezervace a NDC-čka, který se mají smazat - na vyřešení ve smartbuttons přímo
    #todo počet rezervací, které byly ráno na 80

    def user_already(self, prgt, hte):
        for user_name in users:
            if user_name in prgt.lower().title():
                if hte == "True":
                    hte_word = "letenka"
                    users[user_name]["iss"] += 1
                else:
                    hte_word = "rezervace"
                    users[user_name]["rez"] += 1
                print(f"Tato {hte_word} již byla přiřazena a proto bude přiřazena {user_name}")
                return user_name

    def get(self):
        global users_in_work
        query_args = request.args
        query_keys = [key for key in query_args.keys()]
        url = request.url
        url_root = request.url_root
        url_path = request.path
        print(f"{url} {url_root} {url_path}")

        #POST METODY
        if "in_work" in query_keys:
            users_in_work = query_args["in_work"].split(";")
            return users_in_work

        #GET METODY
        #VRACÍ VŠECHNY EXISTUJÍCÍ UŽIVATELE - VE SMARTBUTTONS SE VYTVÁŘÍ SEZNAM, ZE KTERÉHO VYBÍRÁ UŽIVATEL KDO JE V PRÁCI
        if url == f"{url_root}users":
            list_of_users = [user for user in users.keys()]
            return list_of_users

        # prochází uživatele, kteří jsou v práci, vytváří dict buď iss nebo rez a následně vyhodnocuje, kdo má nejméně
        #VRACÍ CELÉ JMÉNO UŽIVATELE ABY MOHL BÝT SPUŠTĚN SMARTBUTTON STEJNÉHO JMÉNA
        if "HTE" in query_keys:
            hte = query_args["HTE"]
            prgt = query_args["PRGT"]
        #PŘIDĚLENÍ REZERVACE KONKRÉTNÍMU UŽIVATELI
            if "user" in query_keys:
                user = query_args["user"]
                if hte == "False":
                    users[user]["rez"] += 1
                    hte_word = "rezervaci"
                else:
                    users[user]["iss"] += 1
                    hte_word = "letenku"
                return [f"""Tuto {hte_word} by dostal {query_args["user"]}"""]
        #AUTOMATICKÝ ROZHOZ
            else:
                temp_users = {}
                if "STUDENT" not in prgt:
                    if hte == "True":
                        for user in users_in_work:
                            temp_users[user] = users[user]["iss"]
                        min_iss = min(temp_users, key=temp_users.get)
                        users[min_iss]["iss"] += 1
                        print(f"Tuto letenku by dostal {min_iss}")
                        return [min_iss]
                    elif hte == "False":
                        for user in users_in_work:
                            temp_users[user] = users[user]["rez"]
                        min_rez = min(temp_users, key=temp_users.get)
                        users[min_rez]["rez"] += 1
                        print(f"Tuto rezervaci by dostal {min_rez}")
                        return [min_rez]
        # AUTOMATICKÉ PŘIŘAZENÍ JIŽ PODEPSANÉ REZERVACE / LETENKY
                else:
                    user_name = self.user_already(prgt, hte)
                    return [user_name]

        #VRÁTÍ UŽIVATELE A POČET REZERVACÍ A LETENEK JAKO VALUE**KEY POKUD NENÍ ZADÁN JINÝ PARAMETR
        name = query_args["name"].replace("+", " ")
        print(name)
        if name not in users.keys():
            return "User does not exist"
        elif url == f"""{url_root}users?name={name.replace(" ", "+")}""":
            print([f"user**{name}", f"""iss**{users[name]["iss"]}""", f"""rez**{users[name]["rez"]}"""])
            return [f"user**{name}",f"""iss**{users[name]["iss"]}""", f"""rez**{users[name]["rez"]}"""]

api.add_resource(User, "/users")

class Stats(Resource):
    def get(self):
        """
        ZOBRAZUJE STATISTIKY UŽIVATELŮ
        :return: list
        """
        users_stats = []
        for name in users:
            users_stats.append(f"""{name}:\nVystaveno: {users[name]["iss"]}\nNevystaveno: {users[name]["rez"]}""")
        return users_stats

api.add_resource(Stats, "/stats")

if __name__ == "__main__":
    #todo debug
    app.run(debug=True)
