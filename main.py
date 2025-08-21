import httpx
import datetime as dt


panel_url = input("Введите url панели: ")
token = input("Введите токен авторизации: ")
count_days = int(input("Введите количество дней, которые нужно прибавить: "))

print("Обновление началось...")


endpoint = panel_url + "/api"

remna = httpx.Client(headers={
    "Authorization": "Bearer " + token
})

if panel_url.startswith("http://"):
    remna.headers += {
        "X-Forwarded-Proto": "https",
        "X-Forwarded-For": "127.0.0.1"
    }

total_users = remna.get(endpoint+"/users",
    params={
      "size": 1,
      "start": 0
    }
).json()["response"]["total"]

for x in range(0, total_users, 1000):
    users = remna.get(endpoint+"/users",
        params={
            "size": 1000,
            "start": x
        }
    ).json()["response"]["users"]
    for user in users:
        expire_at = dt.datetime.fromisoformat(user["expireAt"].replace("Z", "+00:00"))
        if expire_at.year != 2099:
            new_expire_at = expire_at + dt.timedelta(days=count_days)
            remna.patch(endpoint+"/users/", json={
                "uuid": user["uuid"],
                "expireAt": new_expire_at.isoformat()
            })
