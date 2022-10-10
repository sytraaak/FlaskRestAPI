from users import all_users, update_user

def user_already(prgt, hte):
    for user_name in all_users():
        #pokud se jedná o online zaměstnance
        if user_name in prgt.lower().title():
            if hte == "True":
                hte_word = "letenka"
                update_user(user_name, "iss")
            elif hte == "rez":
                hte_word = "rezervace"
                update_user(user_name, "rez")
            elif hte == "lowcost":
                hte_word = "lowcost"
                update_user(user_name, "lowcost")
            elif hte == "canceled":
                hte_word = "canceled"
                update_user(user_name, "canceled")
            else:
                hte_word = "fraud"
                update_user(user_name, "fraud")

            print(f"Tato {hte_word} již byla přiřazena a proto bude přiřazena {user_name}")
            return ["#"+user_name]
        #pokud je rezervace přidělena někomu, kdo není onlinista


