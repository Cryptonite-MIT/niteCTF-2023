from typing import Annotated
from fastapi import FastAPI, Request, Form
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import subprocess
import re
import uuid
import sqlite3
import time
from uvicorn.workers import UvicornWorker
import subprocess

DEBUG = False
FLAG_PATH = "./flag.txt"
BOT_RATE_LIMIT_MIN_SECONDS = 20
BOT_TIMEOUT_SECONDS = 20
CSP_VALUE = "default-src 'self';"
DB_FILE_PATH = "/tmp/chalDb1"
SELF_URL = "http://localhost:1337"

TRIALS_LIMIT_INIT = 70
REGEX_DIGITS = re.compile("^\d+")
TRIALS_REMAINING_MESSAGE = " You have {} tries remaining."

FLAG = open(FLAG_PATH).read().strip()
BOT_AUTH_TOKEN = "bacebf6c19694952bd1e80b80b5810f8"


# remove server header
# gunicorn  -k main.ServerlessUvicornWorker main:app -b "0.0.0.0:1337" --access-logfile '-'
class ServerlessUvicornWorker(UvicornWorker):
    def __init__(self, *args, **kwargs):
        self.CONFIG_KWARGS["server_header"] = False
        super().__init__(*args, **kwargs)


app = FastAPI()
app.mount("/assets", StaticFiles(directory="templates/assets", html=True))
templates = Jinja2Templates(directory="templates")

IPs = {}
IPs_Bot = {}


def getEpoch():
    return int(time.time())


##################
# db setup start
##################
db = sqlite3.connect(DB_FILE_PATH, check_same_thread=False)
# db = sqlite3.connect("sqlite.db", check_same_thread=False)
cur = db.cursor()
cur.execute(
    """
    DROP TABLE IF EXISTS REQUESTS;
    """
)
cur.execute(
    """
    CREATE TABLE IF NOT EXISTS REQUESTS(
        RID TEXT NOT NULL,
        EMAIL TEXT NOT NULL,
        REASON TEXT NOT NULL,
        QUERY TEXT NOT NULL
    );
    """
)
db.commit()
##################
# db setup end
##################


@app.get("/")
def response(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "CSP_CONTENT": CSP_VALUE,
        },
    )


@app.post("/")
def response(request: Request, user_input: Annotated[str, Form()] = ""):
    tries_almost_over_flag = False

    ###
    # rate limiting stuff start
    ###
    if "x-RateLimit-remaining" in request.headers:
        response = templates.TemplateResponse(
            "index.html",
            {
                "request": request,
                "CSP_CONTENT": CSP_VALUE,
                "value": user_input,
                "answer": "Tread lightly you mortal creature",
            },
        )
        response.headers["x-rateLimit-remaining"] = str(IPs[user_ip])
        return response

    user_ip = request.client.host
    if user_ip in IPs:
        if IPs[user_ip] == 0:
            response = templates.TemplateResponse(
                "index.html",
                {
                    "request": request,
                    "value": user_input,
                    "answer": "You have utilized your free quota. Purchase premiumm subscription to mine more epochs.",
                },
            )
            response.headers["x-rateLimit-remaining"] = str(IPs[user_ip])
            return response
        elif IPs[user_ip] < 10:
            tries_almost_over_flag = True

        IPs[user_ip] -= 1
    else:
        IPs[user_ip] = TRIALS_LIMIT_INIT
    ###
    # rate limiting stuff end
    ###

    if not REGEX_DIGITS.match(user_input):
        response = templates.TemplateResponse(
            "index.html",
            {
                "request": request,
                "CSP_CONTENT": CSP_VALUE,
                "value": user_input,
                "answer": "Invalid epoch",
            },
        )
        response.headers["X-RateLimit-Remaining"] = str(IPs[user_ip])
        return response

    cmd = "date -d @{}".format(user_input)

    proc = subprocess.Popen(
        cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )

    if DEBUG:
        try:
            output = "\nERROR: ".join(x.decode() for x in proc.communicate())
        except (UnicodeDecodeError, AttributeError):
            try:
                output = proc.communicate()[1].decode()
            except:
                output = proc.communicate()[1]
        print("\nOutput: ", output)
    else:
        output = proc.communicate()[0].decode()

    if tries_almost_over_flag:
        output += TRIALS_REMAINING_MESSAGE.format(IPs[user_ip])

    response = templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "CSP_CONTENT": CSP_VALUE,
            "value": user_input,
            "answer": output.strip(),
        },
    )
    response.headers["X-RateLimit-Remaining"] = str(IPs[user_ip])
    return response


@app.get("/premiumm")
def response(
    request: Request,
):
    return templates.TemplateResponse(
        "premium.html",
        {
            "request": request,
            "CSP_CONTENT": CSP_VALUE,
        },
    )


@app.post("/premiumm")
def response(
    request: Request,
    email: Annotated[str, Form()] = "",
):
    if not email:
        return templates.TemplateResponse(
            "premium.html",
            {
                "request": request,
                "CSP_CONTENT": CSP_VALUE,
                "msg": "ERROR: Email not provided.",
            },
        )

    return templates.TemplateResponse(
        "premium.html",
        {
            "request": request,
            "CSP_CONTENT": CSP_VALUE,
            "msg": "Thank you for your interest in us.",
        },
    )


@app.get("/begg")
def response(
    request: Request,
):
    return templates.TemplateResponse(
        "beg.html",
        {
            "request": request,
            "CSP_CONTENT": CSP_VALUE,
        },
    )


@app.post("/begg")
def response(
    request: Request,
    email: Annotated[str, Form()] = "",
    reason: Annotated[str, Form()] = "",
    user_input: Annotated[str, Form()] = "",
):
    if not email or not reason or not user_input:
        return templates.TemplateResponse(
            "beg.html",
            {
                "request": request,
                "CSP_CONTENT": CSP_VALUE,
                "email_value": email,
                "reason_value": reason,
                "epoch": user_input,
                "answer": "Please provide all inputs.",
            },
        )

    if not REGEX_DIGITS.match(user_input):
        return templates.TemplateResponse(
            "beg.html",
            {
                "request": request,
                "CSP_CONTENT": CSP_VALUE,
                "email_value": email,
                "reason_value": reason,
                "epoch": user_input,
                "answer": "Invalid epoch",
            },
        )

    cur.execute("SELECT RID FROM REQUESTS WHERE EMAIL = ?;", (email,))
    output = cur.fetchone()

    if not output:
        request_id = uuid.uuid4().hex

        cur.execute(
            "INSERT INTO REQUESTS VALUES (?,?,?,?);",
            (request_id, email, reason, user_input),
        )
        db.commit()
    else:
        return templates.TemplateResponse(
            "beg.html",
            {
                "request": request,
                "CSP_CONTENT": CSP_VALUE,
                "email_value": email,
                "reason_value": reason,
                "epoch": user_input,
                "answer": "You have already requested. Kindly refrain from placing multiple requests.",
                "trackingUrl": output[0],
            },
        )

    return templates.TemplateResponse(
        "beg.html",
        {
            "request": request,
            "CSP_CONTENT": CSP_VALUE,
            "answer": "We will go through your request shortly. Thank you for your patience."
            if REGEX_DIGITS.match(user_input)
            else "Invalid epoch",
            "trackingUrl": request_id if REGEX_DIGITS.match(user_input) else "",
        },
    )


@app.get("/status/{request_id}")
def response(request: Request, request_id, token: str = ""):
    cur.execute(
        "SELECT EMAIL, REASON, QUERY FROM REQUESTS WHERE RID = ?;", (request_id,)
    )
    output = cur.fetchone()

    if not output:
        return templates.TemplateResponse(
            "status.html",
            {
                "request": request,
                "CSP_CONTENT": CSP_VALUE,
            },
        )

    if token == BOT_AUTH_TOKEN:
        return templates.TemplateResponse(
            "statusForBot.html",
            {
                "request": request,
                "CSP_CONTENT": CSP_VALUE,
                "email": output[0],
                "reason": output[1] if output else "",
                "epoch": output[2] if output else "",
                "status": "About to be reviewed",
                "flag": FLAG,
            },
        )
    else:
        return templates.TemplateResponse(
            "status.html",
            {
                "request": request,
                "CSP_CONTENT": CSP_VALUE,
                "email": output[0],
                "reason": output[1] if output else "",
                "epoch": output[2] if output else "",
                "status": "About to be reviewed",
                "flag": "",
            },
        )


@app.post("/status/{request_id}")
def response(request: Request, request_id):
    cur.execute(
        "SELECT EMAIL, REASON, QUERY FROM REQUESTS WHERE RID = ?;", (request_id,)
    )
    output = cur.fetchone()

    if not output:
        return templates.TemplateResponse(
            "status.html",
            {
                "request": request,
                "CSP_CONTENT": CSP_VALUE,
            },
        )

    return {"status": "error", "msg": "Unauthenticated"}


@app.get("/nudge/{request_id}")
async def response(request: Request, request_id):
    user_ip = request.client.host
    epoch = getEpoch()
    if user_ip in IPs_Bot:
        old_epoch = IPs_Bot[user_ip]
        seconds_since_last_req = epoch - int(old_epoch)
        if seconds_since_last_req < BOT_RATE_LIMIT_MIN_SECONDS:
            return {
                "status": "error",
                "message": f"You are too fast. Please wait {BOT_RATE_LIMIT_MIN_SECONDS - seconds_since_last_req} seconds"
                if DEBUG
                else "You have already nudged. Please don't overwork the kittens.",
            }
    IPs_Bot[user_ip] = epoch

    cur.execute("SELECT RID FROM REQUESTS WHERE RID = ?;", (request_id,))
    output = cur.fetchone()

    if not output:
        return {"status": "error", "message": "Invalid request ID"}

    toVisitUrl = "{}/status/{}?token={}".format(SELF_URL, output[0], BOT_AUTH_TOKEN)
    print(toVisitUrl, "\n")

    try:
        IPs_Bot[user_ip] = getEpoch()
        subprocess.Popen(["/usr/local/bin/python3", "report.py", toVisitUrl.encode()])
        return {"status": "ok"}
    except Exception as e:
        IPs_Bot[user_ip] = getEpoch()
        if DEBUG:
            return {"status": "error", "message": "error: {}".format(e)}
        else:
            return {
                "status": "error",
                "message": "please contact admin if this happens repeatedly",
            }
