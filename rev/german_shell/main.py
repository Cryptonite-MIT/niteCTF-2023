#!/usr/local/bin/python

import subprocess
import string
from datetime import datetime, timezone
import time

TIMEOUT = 0.5
SLEEP_TIME = 0.1


def timeout(proc):
    count = 0
    while proc.poll() == None:
        time.sleep(SLEEP_TIME)
        count += SLEEP_TIME
        if count > TIMEOUT:
            proc.terminate()
            return True


def indexedTranslate(input):
    out = ""
    for i, character in enumerate(input):
        if character in string.ascii_lowercase:
            out += chr(97 + (ord(character) + i - 97) % 26)
        elif character in string.ascii_uppercase:
            out += chr(65 + (ord(character) + i - 65) % 26)
        elif character in string.digits:
            out += chr(48 + (ord(character) + i - 48) % 10)
        else:
            out += character
    return out


def hyphenateTime(input):
    hyphenOffset = datetime.now(timezone.utc).second
    return "".join(
        [
            chr(32 + (ord(character) + hyphenOffset - 32) % 17)
            if ord(character) in range(32, 48)
            else character
            for character in input
        ]
    )


def reverse(input):
    return input[::-1]


def run(cmd):
    proc = subprocess.Popen(
        cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )

    if timeout(proc):
        return "Timeout"

    try:
        output = proc.communicate()[0].decode()
    except Exception:
        output = ""

    if not output:
        try:
            output = proc.communicate()[1].decode()
        except Exception:
            output = ""

    return output


while True:
    try:
        inp = input("$ ")
        if inp.lower() == "exit":
            break
        sanitized = reverse(hyphenateTime(indexedTranslate(inp)))
        if sanitized == "exit":
            break
        output = run(sanitized)
        print(output)
        if output == "Timeout":
            break
    except EOFError:
        break
    except KeyboardInterrupt:
        break
