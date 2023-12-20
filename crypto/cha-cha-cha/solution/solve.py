#!/usr/bin/env python3

import pwnlib.tubes
from tokens import tokens
from ct import ciphertexts


def guess_token(conn):
    cts = ciphertexts["0"]
    ind = 0
    for i in range(len(cts)):
        conn.sendlineafter(b">>: ", b"2")
        conn.sendlineafter(b"ciphertext (hex): ", cts[i].encode())
        resp = conn.recvuntil(b"\n")
        if resp.startswith(b"decrypted"):
            # print (f"{i}: {str(tokens[str(0)][i])}")
            ind = 2 * i
            break

    for i in range(1, 6):
        cts = ciphertexts[str(i)]
        conn.sendlineafter(b">>: ", b"2")
        conn.sendlineafter(b"ciphertext (hex): ", cts[ind].encode())
        resp = conn.recvuntil(b"\n")
        # print (f"{i}: {str(tokens[str(i)][ind])}")
        if resp.startswith(b"decrypted"):
            if i < 5:
                ind = 2 * ind
        else:
            if i < 5:
                ind = 2 * (ind + 1)
            else:
                ind = ind + 1
    token = tokens["5"][ind][0]
    return token


def main():
    conn = pwnlib.tubes.remote.remote("127.0.0.1", 1339)

    final_token = ""
    for i in range(6):
        conn.sendlineafter(b">>: ", b"1")
        conn.sendlineafter(b">>: ", (str(i + 1)).encode())
        token = guess_token(conn)
        final_token += token

    conn.sendlineafter(b">>: ", b"3")
    conn.sendlineafter(b"enter token: ", final_token.encode())
    flag = conn.recvuntil(b"\n")
    print(flag)


if __name__ == "__main__":
    main()
