import socket
import sys

BOT_TIMEOUT_SECONDS = 20

try:
    conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    conn.settimeout(BOT_TIMEOUT_SECONDS)

    conn.connect(("localhost", 1338))  # puppeteer bot
    conn.send(sys.argv[1].encode())

    conn.close()
except Exception as e:
    print("Error while reporting:", e)
