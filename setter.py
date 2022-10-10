from users import get_count_of, update_user

def setter(users_in_work, temp_users, what):
    for user in users_in_work:
        temp_users[user] = get_count_of(user, what)
    min_of = min(temp_users, key=temp_users.get)
    update_user(min_of, what)
    print(f"Tuto {what} by dostal {min_of}")
    return ["#"+min_of]