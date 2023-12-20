#!/usr/bin/env python3

import pwnlib.tubes
import hashlib
import json
from ecdsa import SigningKey, VerifyingKey
from ecdsa.util import sigdecode_der, sigencode_der
from ecdsa.numbertheory import inverse_mod
from untwister import Untwister


with open("users.json", "r") as f:
    users = json.load(f)

with open("public.pem") as f:
    public_key = VerifyingKey.from_pem(f.read())

PRIVATE_KEY = 38275640257672751576046816922735783673766900722684007344399172352889340435090571346567077937303667594010522343766121
order = public_key.curve.order


def chk_nonce_reuse():
    r_vals = {}
    for userid in users:
        sig = bytes.fromhex(users[userid]["sign"])
        (r, s) = sigdecode_der(sig, order)
        for uid in r_vals:
            if r_vals[uid] == r:
                return [userid, uid]
        r_vals[userid] = r
    return None


def recover_priv_key():
    u1, u2 = chk_nonce_reuse()
    m1 = f'{users[u1]["name"]} | {u1}'.encode()
    m2 = f'{users[u2]["name"]} | {u2}'.encode()
    n = order
    sig1 = bytes.fromhex(users[u1]["sign"])
    sig2 = bytes.fromhex(users[u2]["sign"])

    (r1, s1) = sigdecode_der(sig1, order)
    (r2, s2) = sigdecode_der(sig2, order)

    h1 = int.from_bytes(hashlib.sha256(m1).digest(), byteorder="big")
    h2 = int.from_bytes(hashlib.sha256(m2).digest(), byteorder="big")

    k = ((h2 - h1) * inverse_mod(s2 - s1, n)) % n
    r_inv = inverse_mod(r1, n)
    d = ((s1 * k - h1) * r_inv) % n
    assert d == PRIVATE_KEY
    return SigningKey.from_secret_exponent(d, public_key.curve)


def forge_sign(name, userid):
    pk = recover_priv_key()
    data = f"{name} | {userid}".encode()
    sig = pk.sign(data, hashfunc=hashlib.sha256, sigencode=sigencode_der)
    assert public_key.verify(sig, data, hashlib.sha256, sigdecode=sigdecode_der)
    return sig.hex()


def reconstruct_rng(random_bits):
    ut = Untwister()
    for b in random_bits:
        ut.submit(b + "?" * 8)
    r = ut.get_random()
    return r


def main():
    conn = pwnlib.tubes.remote.remote("127.0.0.1", 8080)

    key = "00112233445566778899aabbccddeeff"  # random key
    userid = list(users.keys())[0]
    conn.sendlineafter("name: ", f"{users[userid]['name']}")
    conn.sendlineafter("userid: ", f"{userid}")
    conn.sendlineafter("signature: ", f"{users[userid]['sign']}")

    # get outputs of getrandbits(24)
    random_vals = []
    for i in range(400):
        conn.sendlineafter(">> ", "1")
        conn.sendlineafter("key (hex): ", key)
        conn.sendlineafter("plaintext: ", "plaintext")
        conn.recvuntil("encrypted: ")
        enc = bytes.fromhex(conn.recvuntil("\n").decode())
        iv = enc[:16]
        arr = [iv[i : i + 3] for i in range(0, 12, 3)]
        for val in arr:
            bin = "".join(format(byte, "08b") for byte in val)
            random_vals.append(bin)
            assert len(bin) == 24
    r = reconstruct_rng(random_vals)
    key = r.getrandbits(128).to_bytes(16, byteorder="big")

    # get encrypted flag
    conn.sendlineafter(">> ", "3")
    sig = forge_sign("FUTURE ADMIN", "SONY953")
    conn.sendlineafter("name: ", "FUTURE ADMIN")
    conn.sendlineafter("userid: ", "SONY953")
    conn.sendlineafter("signature: ", sig)
    conn.sendlineafter(">> ", "1")
    conn.recvuntil("encrypted: ").decode()
    enc_flag = conn.recvuntil("\n").decode()
    conn.sendlineafter(">> ", "2")

    conn.sendlineafter("name: ", f"{users[userid]['name']}")
    conn.sendlineafter("userid: ", f"{userid}")
    conn.sendlineafter("signature: ", f"{users[userid]['sign']}")
    conn.sendlineafter(">> ", "2")
    conn.sendlineafter("key (hex): ", key.hex())
    conn.sendlineafter("ciphertext (hex): ", f"{enc_flag}")
    conn.recvuntil("decrypted: ")
    flag = conn.recvuntil("\n")
    print(flag)


if __name__ == "__main__":
    main()
