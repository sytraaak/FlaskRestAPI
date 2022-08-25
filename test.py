import requests

BASE = "http://127.0.0.1:5000/"

#TOHLE JE K MAIN_FIRST.PY
print(requests.get(BASE + "users").json())
print(requests.get(BASE + "users/Honzik").json())
requests.put(BASE + "users/Pepik", {"nickname": "prasak123", "age": 25, "sex": "male"})
print(requests.get(BASE + "users/Pepik").json())
print(requests.get(BASE + "users").json())
# print(requests.post(BASE + "helloworld/Frantík"))
# print(requests.get(BASE + "helloworld/users").json())
# print(requests.get(BASE + "helloworld/Pepík/17").json())
# print(requests.post(BASE + "helloworld/Honzík/32").json())
# print(response_1.json())
#TOHLE JE K MAIN.PY
# print(requests.put(BASE + "video/1", {"likes": 10, "name": "Nějaký video", "views": 100000}).json())
# print(requests.get(BASE + "video/1").json())


