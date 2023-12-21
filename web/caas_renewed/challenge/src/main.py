from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import PlainTextResponse
import subprocess
import time
import os
from uvicorn.workers import UvicornWorker


# remove server header
# gunicorn  -k main.ServerlessUvicornWorker main:app -b "0.0.0.0:1337" --access-logfile '-'
class ServerlessUvicornWorker(UvicornWorker):
    def __init__(self, *args, **kwargs):
        self.CONFIG_KWARGS["server_header"] = False
        super().__init__(*args, **kwargs)


TIMEOUT = 5
SLEEP_TIME = 0.1
DEBUG = False

BLACKLIST = [x[:-1] for x in open("./blacklist.txt").readlines()][:-1]

BLACKLIST.append("/")
BLACKLIST.append("\\")
BLACKLIST.append(" ")
BLACKLIST.append("\t")
BLACKLIST.append("\n")
BLACKLIST.append("tc")

ALLOW = [
    "{",
    "}",
    "[",
    "pwd",
    "-",
    "if",
    "tac",
    "ac",
    "cd",
    "tree",
    "ls",
    "echo",
    "tee",
    "touch",
    "mkdir",
    "dir",
    "mv",
    "chmod",
    "ping",
]

for a in ALLOW:
    try:
        BLACKLIST.remove(a)
    except ValueError:
        pass


def isClean(input):
    input = input.lower().strip()
    if any(x in input for x in BLACKLIST):
        if DEBUG:
            for i in BLACKLIST:
                if i in input:
                    print("Banned reason:", i)
                    break
        return False
    return True


def timeout(proc):
    count = 0
    while proc.poll() == None:
        time.sleep(SLEEP_TIME)
        count += SLEEP_TIME
        if count > TIMEOUT:
            proc.terminate()


app = FastAPI()
api = FastAPI()

pwd = os.path.dirname(os.path.realpath(__file__))

app.mount("/cowsay", api)
app.mount("/", StaticFiles(directory="{}/static".format(pwd), html=True))

os.chdir("/usr/games")


@api.get("/{user_input}")
def response(user_input):
    if not isClean(user_input):
        cmd = "cowsay {}".format("'Whoops! I cannot say that'")

        p = subprocess.Popen(
            cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        output = p.communicate()[0]

        return PlainTextResponse(output)
    else:
        cmd = "cowsay {}".format(user_input)

        p = subprocess.Popen(
            cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )

        timeout(p)

        if DEBUG:
            try:
                output = "\n".join(x.decode() for x in p.communicate())
            except (UnicodeDecodeError, AttributeError):
                try:
                    output = p.communicate()[1].decode()
                except:
                    output = p.communicate()[1]

        else:
            output = p.communicate()[0].decode()

        if DEBUG:
            print("OUTPUT:", output)

        if len(output):
            return PlainTextResponse(output)

        else:
            if "denied" in output:
                cmd = "cowsay {}{}".format('"permission denied"', user_input)
            else:
                cmd = "cowsay {}{}".format(
                    '"Oops! Something went wrong. You said "', user_input
                )

            p = subprocess.Popen(
                cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
            )

            output = p.communicate()[0]

        return PlainTextResponse(output)
